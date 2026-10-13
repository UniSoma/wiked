#!/usr/bin/env bash
# Human-operated, self-contained installer. Run one operation at a time, never during agent use.
set -euo pipefail
for tool in uv knot curl; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        echo "Required tool missing: $tool. Install it yourself before proceeding." >&2
        exit 2
    fi
done
# Bash owns human interaction. Never read answers from the script's stdin:
# it may contain the installer itself (curl ... | bash).
wiked_confirm() {
    local answer
    if ! { exec 3<>/dev/tty; } 2>/dev/null; then
        echo "No controlling terminal. Supply explicit approval options for automation." >&2
        return 2
    fi
    printf '%s [yes/no] ' "$1" >&3
    read -r answer <&3 || return 1
    case "$answer" in
        [Yy][Ee][Ss]) return 0 ;;
        *) return 1 ;;
    esac
}
export -f wiked_confirm

arguments=("$@")
destination_given=false
prompt_parameters=true
while [[ $# -gt 0 ]]; do
    case "$1" in
        --destination|--approve-collision)
            option="$1"
            [[ $# -ge 2 && "$2" != --* ]] || { prompt_parameters=false; break; }
            [[ "$option" != --destination ]] || destination_given=true
            shift 2 ;;
        --destination=*) destination_given=true; shift ;;
        --approve-collision=*|--approve-migration-ticket) shift ;;
        --yes|--dry-run|--recover|--help|-h) prompt_parameters=false; shift ;;
        *) prompt_parameters=false; shift ;;
    esac
done
if $prompt_parameters; then
    if ! { exec 3<>/dev/tty; } 2>/dev/null; then
        echo "No controlling terminal. Supply --destination (or use .agents) and --yes; use --dry-run to inspect without approval." >&2
        exit 2
    fi
    printf 'Consumer repository root: %s\n' "$PWD" >&3
    if ! $destination_given; then
        printf 'Installation destination [.agents]: ' >&3
        IFS= read -r destination <&3 || exit 2
        arguments+=(--destination "${destination:-.agents}")
    fi
fi
# The Python core delegates individual confirmations back to the Bash function,
# while retaining the pinned release, candidate, and plan in one process.
exec uv run --no-project --no-python-downloads --python '>=3.11' --with 'PyYAML>=6,<7' python - "${arguments[@]}" <<'PY'
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit

import yaml

METADATA = '.wiked-install.json'
OFFICIAL_REPOSITORY = 'UniSoma/wiked'
MANIFEST = 'wiked-manifest.yaml'
RUNTIME = 'skills/wiked/scripts/validate_wiki.py'
SCHEMA = 'skills/wiked/contracts/wiki-structure.schema.json'
SEMVER = r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'


def fail(message):
    raise ValueError(message)


def owned_path(value):
    if not isinstance(value, str) or not value or '\\' in value:
        fail('Invalid owned path.')
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ('', '.', '..') for part in value.split('/')):
        fail(f'Unsafe path: {value!r}')
    if value not in (MANIFEST, 'commands/wiked-setup.md') and not value.startswith('skills/wiked/'):
        fail(f'Path outside Wiked namespace: {value}')
    return value


def safe_path(root, name):
    path = root / name
    for item in (path, *path.parents):
        if item.is_symlink():
            fail(f'Symlinks are not installation targets: {item}')
    for parent in path.parents:
        if parent.exists() and not parent.is_dir():
            fail(f'Installation parent is not a directory: {parent}')
    return path


def digest(path):
    if not path.exists():
        return None
    if not path.is_file():
        fail(f'Expected a regular file: {path}')
    if path.stat().st_nlink != 1:
        fail(f'Hard-linked files are not installation targets: {path}')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_json(path, data, staging=None):
    temporary = staging or path.with_name(path.name + '.new')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, sort_keys=True, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    sync_directory(path.parent)


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def confirm(message, optional=False):
    sys.stdout.flush()
    result = subprocess.run(['bash', '--noprofile', '--norc', '-c',
                             'wiked_confirm "$1"', 'wiked-ui', message],
                            stdin=subprocess.DEVNULL)
    if result.returncode == 2:
        if optional:
            return False
        fail('No terminal available for confirmation; explicit approval required.')
    if result.returncode not in (0, 1):
        fail('Bash confirmation failed; nothing approved.')
    return result.returncode == 0


def download(url, path):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        fail('Release downloads require HTTPS without embedded credentials.')
    subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                    '--proto', '=https', '--proto-redir', '=https',
                    '--connect-timeout', '30', '--max-time', '300',
                    '--output', str(path), url], check=True)


def baseline(destination):
    path = safe_path(destination, METADATA)
    if not path.exists():
        print('Warning: no reliable baseline; local modifications may be overwritten.')
        return None
    try:
        data = json.loads(path.read_text())
        if data['format'] != 1 or not re.fullmatch(SEMVER, data['version']):
            fail('Invalid installation metadata.')
        if not isinstance(data['files'], dict) or MANIFEST not in data['files']:
            fail('Invalid installation inventory.')
        for name, checksum in data['files'].items():
            owned_path(name)
            if not isinstance(checksum, str) or not re.fullmatch('[0-9a-f]{64}', checksum):
                fail('Invalid baseline hash.')
        return data
    except (KeyError, TypeError, ValueError):
        print('Warning: no reliable baseline; local modifications may be overwritten. Invalid metadata proves no ownership.')
        return None


def candidate(directory, approved=False):
    release_path = directory / 'release.json'
    download(f'https://api.github.com/repos/{OFFICIAL_REPOSITORY}/releases/latest', release_path)
    release = json.loads(release_path.read_text())
    tag = release['tag_name']
    version = tag.removeprefix('v')
    if release.get('draft') or release.get('prerelease') or not re.fullmatch(SEMVER, version):
        fail('Latest release is not a stable SemVer release.')
    print(f'Selected stable release: {version}', flush=True)
    if not approved and not confirm(f'Continue with latest stable release {version}?'):
        fail('Latest stable release not approved; nothing installed.')
    archive_name = 'distr.tar.gz'
    assets = {item['name']: item['browser_download_url'] for item in release['assets']}
    for name in (archive_name,):
        if name not in assets:
            fail(f'Missing release asset: {name}')
        # Pin the release, not a mutable latest/download redirect.
        expected = f'https://github.com/{OFFICIAL_REPOSITORY}/releases/download/{tag}/{name}'
        if assets[name] != expected:
            fail(f'Unexpected asset URL: {name}')
        download(assets[name], directory / name)
    archive_path = directory / archive_name
    tree = directory / 'candidate'
    tree.mkdir()
    with tarfile.open(archive_path, 'r:gz') as archive:
        members = archive.getmembers()
        names = [owned_path(member.name) for member in members]
        if len(names) != len(set(names)) or any(not member.isfile() for member in members):
            fail('Archive must contain unique regular files only (no links or directories).')
        if MANIFEST not in names:
            fail('Archive manifest missing.')
        manifest = yaml.safe_load(archive.extractfile(MANIFEST).read())
        if (manifest['namespace'] != 'wiked' or str(manifest['distribution_version']) != version
                or manifest['preserve_unlisted_files'] is not True
                or manifest['entrypoint'] != 'skills/wiked/SKILL.md'):
            fail('Release manifest does not match Wiked release identity.')
        inventory = [owned_path(name) for group in manifest['components'].values() for name in group]
        if len(inventory) != len(set(inventory)) or set(names) != set(inventory):
            fail('Archive inventory does not match its manifest exactly.')
        if not {MANIFEST, RUNTIME, SCHEMA, manifest['entrypoint']} <= set(names):
            fail('Required distribution interfaces missing.')
        for member in members:
            target = tree / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as source, target.open('wb') as output:
                shutil.copyfileobj(source, output)
            target.chmod(0o644)
    runtime_text = (tree / RUNTIME).read_text()
    if f'METHODOLOGY_VERSION = "{version}"' not in runtime_text:
        fail('Runtime and manifest versions disagree.')
    return version, tree, {name: digest(tree / name) for name in sorted(inventory)}


def compatibility(root, tree, version, previous, dry_run, approve_ticket=False):
    contract = root / 'wiki/wiki-structure.yaml'
    if not contract.exists():
        return
    result = subprocess.run(['uv', 'run', '--no-project', '--no-python-downloads', '--script',
                             str(tree / RUNTIME), '--repository-root', str(root),
                             '--contract-only', '--format', 'json'], cwd=root,
                            stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if result.returncode == 0:
        return
    details = result.stdout + result.stderr
    try:
        report = json.loads(result.stdout)
        contract_errors = [item for item in report['diagnostics']
                           if item['severity'] == 'error' and item['code'].startswith('contract.')]
    except (ValueError, KeyError, TypeError):
        contract_errors = []
    if not contract_errors:
        fail('Candidate runtime could not check the contract; repair its prerequisites before retrying. No migration ticket offered.')
    message = (f'Current installation: {previous["version"] if previous else "unknown"}; '
               f'requested distribution: {version}. Candidate contract check failed. '
               'Qualify a human-reviewed contract migration using the installed skill; '
               'do not migrate automatically.\n' + details)
    print(message)
    # Presence checks are not tracker reads. Never let Knot discover an ancestor.
    local = ((root / '.knot.edn').is_file() and not (root / '.knot.edn').is_symlink()
             and (root / '.tickets').is_dir() and not (root / '.tickets').is_symlink())
    if local and not dry_run and (approve_ticket or confirm('Create a priority-1 HITL migration ticket in this local tracker?', optional=True)):
        result = subprocess.run(['knot', 'info', '--json'], cwd=root,
                                stdin=subprocess.DEVNULL, capture_output=True, text=True, check=True)
        information = json.loads(result.stdout)
        if information.get('ok') is not True:
            fail('Knot could not verify the local tracker; no migration ticket created.')
        paths = information['data']['paths']
        tickets = Path(paths['tickets_path'])
        archive = Path(paths['archive_path'])
        if (Path(paths['project_root']) != root or Path(paths['config_path']) != root / '.knot.edn'
                or not tickets.is_absolute() or root not in tickets.parents
                or not archive.is_absolute() or root not in archive.parents):
            fail('Knot did not resolve a consumer-local tracker; no migration ticket created.')
        safe_path(tickets, '')
        safe_path(archive, '')
        subprocess.run(['knot', 'create', 'Qualify Wiked contract migration', '--type', 'task',
                        '--priority', '1', '--mode', 'hitl', '--description', message],
                       cwd=root, stdin=subprocess.DEVNULL, check=True)
    elif not local:
        print('No existing consumer-local tracker; follow the migration guidance manually.')
    fail('Candidate contract validation failed; installation blocked.')


def recover(destination, transaction):
    journal = transaction / 'journal.json'
    if not journal.exists():
        # Preparation never mutates installed files before the journal is durable.
        shutil.rmtree(transaction)
        return
    data = json.loads(journal.read_text())
    if data['destination'] != str(destination):
        fail('Recovery destination mismatch.')
    if data['status'] == 'pending':
        names = [record['path'] for record in data['files']]
        if len(names) != len(set(names)) or METADATA not in names:
            fail('Invalid recovery inventory.')
        for name in data['directories']:
            directory = Path(name)
            if directory != destination and destination not in directory.parents:
                fail('Unsafe recovery directory.')
            safe_path(directory, '')
        for index, record in enumerate(data['files']):
            name = record['path']
            if name != METADATA:
                owned_path(name)
            target = safe_path(destination, name)
            if type(record['existed']) is not bool:
                fail('Invalid recovery file state.')
            if record['existed']:
                backup = safe_path(transaction, f'backup/{index}')
                if digest(backup) != record['hash']:
                    fail('Recovery backup integrity failure; preserve transaction for manual recovery.')
            elif target.exists() and not target.is_file():
                fail('Recovery target is not a regular file.')
        for index, record in enumerate(data['files']):
            target = safe_path(destination, record['path'])
            if record['existed']:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(transaction / 'backup' / str(index), target)
                with target.open('rb') as stream:
                    os.fsync(stream.fileno())
            elif target.exists():
                target.unlink()
            if target.parent.exists():
                sync_directory(target.parent)
        for name in sorted(data['directories'], key=len, reverse=True):
            directory = Path(name)
            try:
                directory.rmdir()
            except FileNotFoundError:
                pass
            except OSError:
                if any(directory.iterdir()):
                    continue  # Preserve third-party content created in the meantime.
                raise
    elif data['status'] != 'committed':
        fail('Unknown recovery status.')
    shutil.rmtree(transaction)
    sync_directory(transaction.parent)


def install(destination, transaction, tree, version, hashes, changes, observed):
    transaction.mkdir(mode=0o700)
    (transaction / 'backup').mkdir()
    records = []
    directories = set()
    try:
        for index, name in enumerate([*changes, METADATA]):
            target = safe_path(destination, name)
            current = digest(target)
            if current != observed[name]:
                fail(f'Target changed since approval: {name}')
            records.append({'path': name, 'existed': current is not None, 'hash': current})
            if current is not None:
                backup = transaction / 'backup' / str(index)
                shutil.copy2(target, backup)
                if digest(backup) != current:
                    fail(f'Target changed during backup: {name}')
                with backup.open('rb') as stream:
                    os.fsync(stream.fileno())
            for parent in target.parents:
                if parent.exists():
                    break
                directories.add(str(parent))
        data = {'destination': str(destination), 'status': 'pending',
                'files': records, 'directories': sorted(directories)}
        sync_directory(transaction / 'backup')
        atomic_json(transaction / 'journal.json', data)
        sync_directory(transaction.parent)
        for name in changes:
            target = safe_path(destination, name)
            if digest(target) != observed[name]:
                fail(f'Target changed since approval: {name}')
            if name in hashes:
                target.parent.mkdir(parents=True, exist_ok=True)
                # Prepared files and backups exist before the first replacement.
                with (tree / name).open('rb') as source, target.open('wb') as output:
                    shutil.copyfileobj(source, output)
                    output.flush()
                    os.fsync(output.fileno())
                target.chmod(0o644)
            else:
                target.unlink()
            sync_directory(target.parent)
        atomic_json(destination / METADATA, {'format': 1, 'version': version, 'files': hashes}, transaction / 'metadata.new')
        data['status'] = 'committed'
        atomic_json(transaction / 'journal.json', data)
    except BaseException:
        recover(destination, transaction)
        raise
    recover(destination, transaction)


def main():
    parser = argparse.ArgumentParser(description='Human Wiked installer/updater. Stop agents and run one operation at a time; concurrency is unsupported.')
    parser.add_argument('--destination', default='.agents', help='Manifest-relative installation root; relative to consumer cwd.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--yes', action='store_true', help='Approve the displayed operation, not collisions or migration tickets.')
    parser.add_argument('--approve-collision', action='append', default=[], metavar='PATH', help='Explicitly approve taking over this manifest-relative path.')
    parser.add_argument('--approve-migration-ticket', action='store_true', help='Separately approve a P1 HITL migration ticket, only on incompatibility with a proven local tracker.')
    parser.add_argument('--recover', action='store_true', help='Restore an interrupted transaction, without downloading or installing.')
    args = parser.parse_args()
    root = Path.cwd().resolve()
    destination = Path(os.path.abspath(args.destination))
    safe_path(destination, '')
    if destination == root or destination in root.parents:
        fail('Installation destination must not contain the consumer repository root.')
    for area in ('wiki', 'raw', '.tickets', '.git'):
        protected = root / area
        if destination == protected or protected in destination.parents:
            fail(f'Consumer-owned area cannot be an installation destination: {area}')
    if not destination.parent.is_dir():
        fail('Destination parent must already exist.')
    transaction = destination.with_name('.' + destination.name + '.wiked-transaction')
    safe_path(transaction, '')
    if transaction.exists():
        if not args.recover:
            fail('Interrupted operation detected. Run --recover before installing again.')
        recover(destination, transaction)
        print('Recovery complete; run the installer again to plan an update.')
        return
    if args.recover:
        print('No pending operation to recover.')
        return
    previous = baseline(destination)
    with tempfile.TemporaryDirectory(prefix='wiked-') as temporary:
        version, tree, hashes = candidate(Path(temporary), args.yes or args.dry_run)
        if previous and tuple(map(int, previous['version'].split('.'))) > tuple(map(int, version.split('.'))):
            fail('The latest stable release is older than the installation; downgrade is not supported.')
        compatibility(root, tree, version, previous, args.dry_run, args.approve_migration_ticket)
        old = previous['files'] if previous else {}
        observed = {name: digest(safe_path(destination, name)) for name in sorted(set(hashes) | set(old))}
        observed[METADATA] = digest(safe_path(destination, METADATA))
        changes = []
        collisions = []
        print(f'Destination: {destination}')
        for name, checksum in hashes.items():
            current = observed[name]
            if current is not None and name not in old:
                collisions.append(name)
                print(f'Collision (unowned): {name}')
            if current != checksum:
                changes.append(name)
                action = 'Add' if current is None else 'Replace'
                modified = ' (locally modified)' if name in old and current != old[name] else ''
                print(f'{action}: {name}{modified}')
        for name in sorted(set(old) - set(hashes)):
            if observed[name] is None:
                continue
            if observed[name] == old[name]:
                changes.append(name)
                print(f'Remove obsolete: {name}')
            else:
                print(f'Preserve modified obsolete file: {name}')
        if previous and previous['version'] == version and old == hashes and not changes:
            print('Already installed and intact; no changes.')
            return
        if previous and previous['version'] == version:
            print('Reinstall requested version to repair changed or missing files.')
        if args.dry_run:
            print('Dry run: no installed files or tickets changed.')
            return
        approved = {owned_path(name) for name in args.approve_collision}
        for name in collisions:
            if name not in approved and (args.yes or not confirm(f'Take ownership of collision {name}?')):
                fail(f'Explicit collision approval required: --approve-collision {name}')
        if not args.yes and not confirm('Approve this installation plan? Stop agents before approving.'):
            fail('Operation not approved; nothing installed.')
        install(destination, transaction, tree, version, hashes, changes, observed)
        print(f'Installed Wiked {version}. Skill: {destination / "skills/wiked"}')
        print(f'Adapter: {destination / "commands/wiked-setup.md"}')
        print('Configure agent discovery for custom destinations. Start wiked-setup with the installed skill and consumer contract; no agent has been launched.')


def interrupted(signum, frame):
    raise RuntimeError(f'Interrupted by signal {signum}; restore the previous installation.')


signal.signal(signal.SIGTERM, interrupted)
signal.signal(signal.SIGHUP, interrupted)
try:
    main()
except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError, tarfile.TarError, yaml.YAMLError, RuntimeError, KeyboardInterrupt) as exc:
    print(f'Wiked installation failed: {exc}', file=sys.stderr)
    sys.exit(2)
PY
