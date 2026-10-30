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
    printf '%s [y/yes/no] ' "$1" >&3
    read -r answer <&3 || return 1
    case "$answer" in
        [Yy]|[Yy][Ee][Ss]) return 0 ;;
        *) return 1 ;;
    esac
}
export -f wiked_confirm

arguments=("$@")
destination_given=false
prompt_parameters=true
while [[ $# -gt 0 ]]; do
    case "$1" in
        --destination|--approve-collision|--source)
            option="$1"
            [[ $# -ge 2 && "$2" != --* ]] || { prompt_parameters=false; break; }
            [[ "$option" != --destination ]] || destination_given=true
            shift 2 ;;
        --destination=*) destination_given=true; shift ;;
        --approve-collision=*|--source=*|--approve-migration-ticket) shift ;;
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
import runpy
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
from urllib.parse import urlsplit

import yaml

OFFICIAL_REPOSITORY = 'UniSoma/wiked'
RUNTIME = 'skills/wiked/scripts/validate_wiki.py'
SCHEMA = 'skills/wiked/contracts/wiki-structure.schema.json'
IDENTITY = 'skills/wiked/scripts/distribution.py'
CHANGELOG = 'skills/wiked/CHANGELOG.md'
# BEGIN GENERATED INSTALLATION STATE CORE
"""Canonical installation state and transaction core (also embedded in the installer).

Concurrency is unsupported: run one operation at a time. Review acknowledgment
does not recover transactions or verify conformity of installed content.
"""

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil

METADATA = '.wiked-install.json'
MANIFEST = 'wiked-manifest.yaml'
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


def atomic_json(path, data, staging=None, before_replace=None):
    temporary = staging or path.with_name(path.name + '.new')
    with temporary.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, sort_keys=True, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    if before_replace is not None:
        before_replace()
    os.replace(temporary, path)
    sync_directory(path.parent)


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def baseline(destination):
    path = safe_path(destination, METADATA)
    digest(path)
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


def pending_review(previous, version):
    if previous is None:
        return None
    since = previous.get('maintenance_since')
    if since is not None and (not isinstance(since, str) or not re.fullmatch(SEMVER, since)
                             or tuple(map(int, since.split('.'))) > tuple(map(int, previous['version'].split('.')))):
        fail('Invalid maintenance review metadata; repair it explicitly before proceeding.')
    if previous['version'] != version:
        return since or previous['version']
    return since


def review_notice(since, version):
    if since is not None:
        print(f'Maintenance review pending: {since} -> {version}.')


def transaction_path(destination):
    return safe_path(destination.with_name('.' + destination.name + '.wiked-transaction'), '')


def read_review_state(destination, parse_manifest):
    """Read a stable snapshot; parsing is supplied by each caller, never fetched."""
    safe_path(destination, '')
    if transaction_path(destination).exists():
        fail('Interrupted operation detected. Human recovery is required; nothing acknowledged.')
    observed = {name: digest(safe_path(destination, name)) for name in (METADATA, MANIFEST)}
    previous = baseline(destination)
    if previous is None:
        fail('Reviewed version must match a reliable installed version; nothing acknowledged.')
    since = pending_review(previous, previous['version'])
    manifest = parse_manifest(safe_path(destination, MANIFEST).read_text())
    if (not isinstance(manifest, dict) or manifest.get('namespace') != 'wiked'
            or str(manifest.get('distribution_version')) != previous['version']
            or manifest.get('entrypoint') != 'skills/wiked/SKILL.md'
            or manifest.get('preserve_unlisted_files') is not True
            or not isinstance(manifest.get('components'), dict)):
        fail('Installed manifest and metadata disagree; invalid Wiked identity; nothing acknowledged.')
    inventory = []
    for group in manifest['components'].values():
        if not isinstance(group, list):
            fail('Invalid installed manifest inventory; nothing acknowledged.')
        inventory.extend(owned_path(name) for name in group)
    if (len(inventory) != len(set(inventory)) or set(inventory) != set(previous['files'])
            or not {MANIFEST, manifest['entrypoint']} <= set(inventory)):
        fail('Installed manifest inventory and baseline disagree; nothing acknowledged.')
    assert_snapshot(destination, observed)
    token_state = {'installation_root': os.path.abspath(destination), 'files': observed}
    token = hashlib.sha256(json.dumps(token_state, sort_keys=True).encode('utf-8')).hexdigest()
    return previous, since, token, observed


def assert_snapshot(destination, observed):
    for name, checksum in observed.items():
        if digest(safe_path(destination, name)) != checksum:
            fail(f'Target changed since approval: {name}')


def acknowledge_review(destination, previous, since, token, observed, *, version,
                       approved_since, state_token, human_confirmed, dry_run=False):
    """The boolean asserts explicit human approval; it is not proof of approval."""
    if version != previous['version'] or approved_since != since or state_token != token:
        fail('Reviewed version, pending range, and state token must match; nothing acknowledged.')
    if not human_confirmed:
        fail('Explicit human confirmation after review and finding disposition is required; nothing acknowledged.')
    if transaction_path(destination).exists():
        fail('Interrupted operation detected. Human recovery is required; nothing acknowledged.')
    assert_snapshot(destination, observed)
    if since is None or dry_run:
        return False
    install(destination, transaction_path(destination), destination, previous['version'],
            previous['files'], [], observed, metadata={**previous, 'maintenance_since': None})
    return True


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


def install(destination, transaction, tree, version, hashes, changes, observed,
            maintenance_since=None, metadata=None):
    transaction.mkdir(mode=0o700)
    (transaction / 'backup').mkdir()
    records = []
    directories = set()
    journal_written = False
    mutation_started = False
    try:
        assert_snapshot(destination, observed)
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
        journal_written = True
        sync_directory(transaction.parent)
        assert_snapshot(destination, observed)
        for name in changes:
            target = safe_path(destination, name)
            if digest(target) != observed[name]:
                fail(f'Target changed since approval: {name}')
            mutation_started = True
            if name in hashes:
                target.parent.mkdir(parents=True, exist_ok=True)
                with (tree / name).open('rb') as source, target.open('wb') as output:
                    shutil.copyfileobj(source, output)
                    output.flush()
                    os.fsync(output.fileno())
                target.chmod(0o644)
            else:
                target.unlink()
            sync_directory(target.parent)
        # Bind metadata-only approval to both original files right up to replace.
        # Installation may itself replace the manifest, so only recheck unchanged
        # observed paths here (metadata is always unchanged until this point).
        assert_snapshot(destination, {name: checksum for name, checksum in observed.items()
                                      if name not in changes})
        replacement = (metadata if metadata is not None else
                       {'format': 1, 'version': version, 'files': hashes,
                        'maintenance_since': maintenance_since})
        if not changes:
            def before_metadata_replace():
                nonlocal mutation_started
                assert_snapshot(destination, observed)
                mutation_started = True

            atomic_json(destination / METADATA, replacement, transaction / 'metadata.new',
                        before_replace=before_metadata_replace)
        else:
            mutation_started = True
            atomic_json(destination / METADATA, replacement, transaction / 'metadata.new')
        data['status'] = 'committed'
        atomic_json(transaction / 'journal.json', data)
    except BaseException:
        if journal_written and not mutation_started:
            # A pre-write race must not roll back somebody else's newer state.
            shutil.rmtree(transaction)
            sync_directory(transaction.parent)
        else:
            recover(destination, transaction)
        raise
    recover(destination, transaction)
# END GENERATED INSTALLATION STATE CORE


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


def candidate(directory, approved=False, source=None):
    if source is not None:
        return local_candidate(directory, approved, source)
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
    return extract(directory, directory / archive_name, version)


def local_candidate(directory, approved, source):
    # A local clone is packaged by its own packager; its user owns that choice.
    if re.match(r'[A-Za-z][A-Za-z0-9+.-]*://', source):
        fail('--source takes a local directory, not a URL.')
    root = Path(source).resolve()
    packager = root / 'scripts/package-wiked.sh'
    if not root.is_dir() or not packager.is_file():
        fail(f'--source must be a local Wiked clone containing scripts/package-wiked.sh: {root}')
    output = directory / 'package'
    result = subprocess.run(['bash', str(packager), '--output', str(output)], cwd=root,
                            stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if result.returncode != 0:
        fail('Packaging the local source failed; nothing installed.\n' + result.stdout + result.stderr)
    archive_path = output / 'distr.tar.gz'
    with tarfile.open(archive_path, 'r:gz') as archive:
        try:
            version = str(yaml.safe_load(archive.extractfile(MANIFEST).read())['distribution_version'])
        except (KeyError, TypeError, AttributeError):
            fail('Local package manifest missing or invalid.')
    if not re.fullmatch(SEMVER, version):
        fail('Local source version is not a stable SemVer version.')
    print(f'Selected local source: {root} (version {version}; not an official release)', flush=True)
    if not approved and not confirm(f'Continue with local source version {version}?'):
        fail('Local source not approved; nothing installed.')
    return extract(directory, archive_path, version)


def extract(directory, archive_path, version):
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
        if not {MANIFEST, RUNTIME, SCHEMA, IDENTITY, CHANGELOG, manifest['entrypoint']} <= set(names):
            fail('Required distribution interfaces missing.')
        for member in members:
            target = tree / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as source, target.open('wb') as output:
                shutil.copyfileobj(source, output)
            target.chmod(0o644)
    runpy.run_path(str(tree / IDENTITY))['release_declarations'](tree)
    return version, tree, {name: digest(tree / name) for name in sorted(inventory)}


def compatibility(root, tree, version, previous, dry_run, approve_ticket=False):
    contract = root / 'wiki/wiki-structure.yaml'
    if not contract.exists():
        return None
    result = subprocess.run(['uv', 'run', '--no-project', '--no-python-downloads', '--script',
                             str(tree / RUNTIME), '--repository-root', str(root),
                             '--contract-only', '--format', 'json'], cwd=root,
                            stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            declared = json.loads(result.stdout)['contract']['methodology_version']
        except (ValueError, KeyError, TypeError):
            declared = None
        if not isinstance(declared, str) or not re.fullmatch(SEMVER, declared):
            fail('Candidate runtime did not report the contract methodology version; installation blocked.')
        return declared
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


def maintenance_prompt(since, version):
    print('\nWIKED MAINTENANCE AGENT PROMPT:')
    print('-----\n')
    print('Use the Wiked skill to perform the installed-version maintenance review')
    print('in this consumer repository, following its maintenance workflow and instance')
    print('contract. This is maintenance review, not setup.\n')
    print(f'Installed version: {version}')
    print(f'Pending methodology-impact range: {since} -> {version}')
    print('\n-----\n')


def main():
    parser = argparse.ArgumentParser(description='Human Wiked installer/updater. Stop agents and run one operation at a time; concurrency is unsupported.')
    parser.add_argument('--destination', default='.agents', help='Manifest-relative installation root; relative to consumer cwd.')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--yes', action='store_true', help='Approve the displayed operation, not collisions or migration tickets.')
    parser.add_argument('--approve-collision', action='append', default=[], metavar='PATH', help='Explicitly approve taking over this manifest-relative path.')
    parser.add_argument('--approve-migration-ticket', action='store_true', help='Separately approve a P1 HITL migration ticket, only on incompatibility with a proven local tracker.')
    parser.add_argument('--source', metavar='PATH', help='Install from a local Wiked clone, packaged by its own packager, instead of the latest official release.')
    parser.add_argument('--recover', action='store_true', help='Restore an interrupted transaction, without downloading or installing.')
    parser.add_argument('--acknowledge-maintenance-review', metavar='VERSION', help='Human confirmation of review and finding disposition for the installed version; metadata only, no download.')
    args = parser.parse_args()
    if args.acknowledge_maintenance_review and (args.recover or args.approve_collision or args.approve_migration_ticket or args.source):
        fail('Review acknowledgment cannot be combined with recovery, installation approvals, or a source.')
    if args.recover and args.source:
        fail('Recovery does not install; it cannot be combined with --source.')
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
    if args.acknowledge_maintenance_review:
        previous, since, token, observed = read_review_state(destination, yaml.safe_load)
        if args.acknowledge_maintenance_review != previous['version']:
            fail('Reviewed version must match a reliable installed version; nothing acknowledged.')
        review_notice(since, previous['version'])
        if since is None:
            print('No pending maintenance review; nothing changed.')
            return
        if args.dry_run:
            print('Dry run: no review acknowledged.')
            return
        if not args.yes and not confirm(f'Acknowledge review through {previous["version"]}, with human disposition and follow-ups for findings?'):
            fail('Review acknowledgment not approved; nothing changed.')
        acknowledge_review(destination, previous, since, token, observed,
                           version=args.acknowledge_maintenance_review, approved_since=since,
                           state_token=token, human_confirmed=True)
        print(f'Maintenance review acknowledged through {previous["version"]}; this does not establish content conformity or authorize corrections.')
        return
    metadata_observed = digest(safe_path(destination, METADATA))
    previous = baseline(destination)
    assert_snapshot(destination, {METADATA: metadata_observed})
    since = pending_review(previous, previous['version']) if previous else None
    with tempfile.TemporaryDirectory(prefix='wiked-') as temporary:
        version, tree, hashes = candidate(Path(temporary), args.yes or args.dry_run, args.source)
        if previous and tuple(map(int, previous['version'].split('.'))) > tuple(map(int, version.split('.'))):
            selected = 'The local source' if args.source else 'The latest stable release'
            fail(f'{selected} is older than the installation; downgrade is not supported.')
        since = pending_review(previous, version)
        declared = compatibility(root, tree, version, previous, args.dry_run, args.approve_migration_ticket)
        if (previous is None and declared is not None
                and tuple(map(int, declared.split('.'))) < tuple(map(int, version.split('.')))):
            since = declared  # An existing contract enters at its declared methodology version.
        old = previous['files'] if previous else {}
        observed = {name: digest(safe_path(destination, name)) for name in sorted(set(hashes) | set(old))}
        observed[METADATA] = metadata_observed
        assert_snapshot(destination, {METADATA: metadata_observed})
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
            review_notice(since, version)
            return
        if previous and previous['version'] == version:
            print('Reinstall the same version over changed, missing, or differing files.')
        if args.dry_run:
            print('Dry run: no installed files or tickets changed.')
            return
        approved = {owned_path(name) for name in args.approve_collision}
        for name in collisions:
            if name not in approved and (args.yes or not confirm(f'Take ownership of collision {name}?')):
                fail(f'Explicit collision approval required: --approve-collision {name}')
        if not args.yes and not confirm('Approve this installation plan? Stop agents before approving.'):
            fail('Operation not approved; nothing installed.')
        install(destination, transaction, tree, version, hashes, changes, observed, since)
        print(f'Installed Wiked {version}. Skill: {destination / "skills/wiked"}')
        print(f'Adapter: {destination / "commands/wiked-setup.md"}')
        print('Configure agent discovery for custom destinations; no agent has been launched.')
        if previous is None and declared is None:
            print('First installation: start wiked-setup with the installed skill to create the '
                  'instance contract (wiki/wiki-structure.yaml).')
        elif previous is None and since is None:
            print('First installation: an instance contract already exists; operate the wiki through '
                  'the installed skill. Use wiked-setup only for an authorized contract migration.')
        elif previous is None:
            print(f'First installation over an instance contract declaring methodology {declared}: '
                  'run a maintenance agent. Copy the text between the separators below.')
            maintenance_prompt(since, version)
        if previous and previous['version'] != version:
            print('Version changed: run a maintenance agent. Copy the text between the separators below.')
            maintenance_prompt(since, version)
        review_notice(since, version)


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
