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
