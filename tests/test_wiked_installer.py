from __future__ import annotations

import fcntl
import hashlib
import io
import json
import os
import pty
import select
import signal
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import time

import pytest
import yaml

from test_wiked_validator import contract


ROOT = Path(__file__).parents[1]
INSTALLER = ROOT / 'scripts/install-wiked.sh'
DISTRIBUTION = ROOT / 'distr/agents'
REPOSITORY = 'UniSoma/wiked'


def installer_module():
    """Load the embedded core without running its CLI or changing signal handlers."""
    source = INSTALLER.read_text().split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
    source = source.split('signal.signal(signal.SIGTERM', 1)[0]
    namespace = {'__name__': 'installer_test'}
    exec(compile(source, str(INSTALLER), 'exec'), namespace)
    return namespace


def release(directory, version='1.4.0', extra=None, omit=(),
            extra_member=None, prerelease=False):
    directory.mkdir(parents=True, exist_ok=True)
    manifest = yaml.safe_load((DISTRIBUTION / 'wiked-manifest.yaml').read_text())
    source_version = manifest['distribution_version']
    manifest['distribution_version'] = version
    files = {name: (DISTRIBUTION / name).read_bytes()
             for group in manifest['components'].values() for name in group}
    for name in omit:
        files.pop(name)
        for group in manifest['components'].values():
            if name in group:
                group.remove(name)
    if extra:
        files.update(extra)
        manifest['components']['instructions'].extend(extra)
    runtime = 'skills/wiked/scripts/validate_wiki.py'
    files[runtime] = files[runtime].replace(f'METHODOLOGY_VERSION = "{source_version}"'.encode(),
                                           f'METHODOLOGY_VERSION = "{version}"'.encode())
    files['wiked-manifest.yaml'] = yaml.safe_dump(manifest).encode()
    archive_name = 'distr.tar.gz'
    archive = directory / archive_name
    with tarfile.open(archive, 'w:gz') as stream:
        for name, content in files.items():
            member = tarfile.TarInfo(name)
            member.size = len(content)
            stream.addfile(member, io.BytesIO(content))
        if extra_member:
            stream.addfile(extra_member, io.BytesIO(b'x'))
    (directory / 'release.json').write_text(json.dumps({
        'tag_name': f'v{version}', 'draft': False, 'prerelease': prerelease,
        'assets': [{'name': name, 'browser_download_url':
                    f'https://github.com/{REPOSITORY}/releases/download/v{version}/{name}'}
                   for name in (archive_name,)],
    }))
    return files


@pytest.fixture
def environment(tmp_path):
    consumer = tmp_path / 'consumer'
    consumer.mkdir()
    assets = tmp_path / 'release'
    release(assets)
    tools = tmp_path / 'bin'
    tools.mkdir()
    # No real network, uv environments, installed tools, tracker, or consumer.
    (tools / 'uv').write_text(f'''#!/usr/bin/env bash
set -eu
if [[ " $* " == *" --script "* ]]; then
    while [[ "$1" != --script ]]; do shift; done
    shift
    if [[ "$1" == */interrupt.py ]]; then exec {sys.executable} "$@"; fi
    exec {shutil.which('uv')} run --no-project --no-python-downloads --script "$@"
fi
while [[ "$1" != python ]]; do shift; done
shift
exec {sys.executable} "$@"
''')
    (tools / 'curl').write_text('''#!/usr/bin/env bash
set -eu
url="${@: -1}"
printf '%s\n' "$url" >> "$REQUEST_LOG"
if [[ "$url" == https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh ]]; then
    cat "$INSTALLER_FIXTURE"
    exit
fi
while [[ "$1" != --output ]]; do shift; done
shift
out="$1"
case "$url" in
  https://api.github.com/repos/UniSoma/wiked/releases/latest) name=release.json ;;
  https://github.com/UniSoma/wiked/releases/download/*) name="${url##*/}" ;;
  *) exit 22 ;;
esac
cp "$RELEASE_FIXTURE/$name" "$out"
''')
    (tools / 'knot').write_text('''#!/usr/bin/env bash
set -eu
printf '%s\n' "$PWD" "$@" >> "$KNOT_LOG"
if [[ "$1" == info ]]; then
    printf '{"ok":true,"data":{"paths":{"project_root":"%s","config_path":"%s/.knot.edn","tickets_path":"%s/.tickets","archive_path":"%s/.tickets/archive"}}}\n' "$PWD" "$PWD" "${KNOT_TICKETS_ROOT:-$PWD}" "${KNOT_TICKETS_ROOT:-$PWD}"
fi
''')
    for tool in tools.iterdir():
        tool.chmod(0o755)
    env = {**os.environ, 'PATH': str(tools) + os.pathsep + os.environ['PATH'],
           'RELEASE_FIXTURE': str(assets), 'REQUEST_LOG': str(tmp_path / 'requests'),
           'KNOT_LOG': str(tmp_path / 'knot-log'), 'TMPDIR': str(tmp_path),
           'INSTALLER_FIXTURE': str(INSTALLER)}
    return consumer, assets, env


def run(environment, *args, input=''):
    root, _, env = environment
    return subprocess.run(['bash', str(INSTALLER), *args],
                          cwd=root, env=env, input=input, capture_output=True, text=True,
                          start_new_session=True)


def run_interactive(environment, *args, answers, pipe=False):
    """A controlling terminal supplies answers, independently of script stdin."""
    root, _, env = environment
    arguments = list(args)
    if pipe:
        receiver = 'bash -s -- "$@"' if arguments else 'bash'
        command = ['bash', '-c', 'set -o pipefail; curl -fsSL '
                   'https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh '
                   '| ' + receiver, 'installer-test', *arguments]
    else:
        command = ['bash', str(INSTALLER), *arguments]
    pid, terminal = pty.fork()
    if pid == 0:
        os.chdir(root)
        os.execvpe(command[0], command, env)
    output = b''
    cursor = 0
    next_answer = 0
    deadline = time.monotonic() + 45
    try:
        while time.monotonic() < deadline:
            if not select.select([terminal], [], [], 0.1)[0]:
                continue
            try:
                chunk = os.read(terminal, 65536)
            except OSError:
                break  # Linux PTYs return EIO after the last writer exits.
            if not chunk:
                break
            output += chunk
            while next_answer < len(answers):
                prompt, answer = answers[next_answer]
                position = output.find(prompt.encode(), cursor)
                if position < 0:
                    break
                os.write(terminal, (answer + '\n').encode())
                cursor = position + len(prompt)
                next_answer += 1
        else:
            os.killpg(pid, signal.SIGKILL)
            pytest.fail(f'Terminal interaction timed out: {output.decode(errors="replace")}')
    finally:
        os.close(terminal)
        _, status = os.waitpid(pid, 0)
    assert next_answer == len(answers), output.decode(errors='replace')
    return subprocess.CompletedProcess(command, os.waitstatus_to_exitcode(status),
                                       output.decode(errors='replace'), '')


def snapshot(root):
    return {str(path.relative_to(root)): (path.read_bytes(), path.stat().st_mode & 0o777)
            for path in root.rglob('*') if path.is_file()}


def test_install_pin_inventory_custom_destination_and_noop(environment):
    root, assets, env = environment
    result = run(environment, '--destination', 'custom', '--yes')
    assert result.returncode == 0, result.stderr
    target = root / 'custom'
    state = json.loads((target / '.wiked-install.json').read_text())
    files = release(assets)
    assert state['version'] == '1.4.0'
    assert state['files'] == {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}
    assert snapshot(target).keys() == {*files, '.wiked-install.json'}
    assert 'wiked-setup' in result.stdout and 'no agent has been launched' in result.stdout
    requests = Path(env['REQUEST_LOG']).read_text().splitlines()
    assert requests.count(f'https://api.github.com/repos/{REPOSITORY}/releases/latest') == 1
    assert all(url.startswith('https://') for url in requests)
    assert requests == [f'https://api.github.com/repos/{REPOSITORY}/releases/latest',
                        f'https://github.com/{REPOSITORY}/releases/download/v1.4.0/distr.tar.gz']
    before = snapshot(target)
    times = {path: path.stat().st_mtime_ns for path in target.rglob('*') if path.is_file()}
    result = run(environment, '--destination', 'custom', '--yes')
    assert result.returncode == 0 and 'no changes' in result.stdout
    assert before == snapshot(target)
    assert times == {path: path.stat().st_mtime_ns for path in target.rglob('*') if path.is_file()}


def test_dry_run_confirmation_and_collision_approval(environment):
    root, _, _ = environment
    destination = root / '.agents'
    destination.mkdir()
    (destination / 'wiked-manifest.yaml').write_text('consumer file')
    (destination / 'other.txt').write_text('third party')
    before = snapshot(destination)
    result = run(environment, '--dry-run')
    assert result.returncode == 0 and 'Collision' in result.stdout and 'Dry run' in result.stdout
    assert snapshot(destination) == before
    result = run(environment, '--yes')
    assert result.returncode == 2 and 'Explicit collision approval' in result.stderr
    assert snapshot(destination) == before
    result = run(environment, input='no\n')
    assert result.returncode == 2
    result = run(environment, '--yes', '--approve-collision', 'wiked-manifest.yaml')
    assert result.returncode == 0, result.stderr
    assert (destination / 'other.txt').read_text() == 'third party'


def test_interactive_collision_and_operation_have_separate_confirmations(environment):
    root, _, _ = environment
    (root / '.agents').mkdir()
    (root / '.agents/wiked-manifest.yaml').write_text('unowned')
    result = run_interactive(environment, answers=[
        ('Installation destination [.agents]:', ''),
        ('Continue with latest stable release 1.4.0?', 'yes'),
        ('Take ownership of collision wiked-manifest.yaml?', 'yes'),
        ('Approve this installation plan?', 'yes'),
    ])
    assert result.returncode == 0, result.stderr


def test_downgrade_is_not_offered(environment):
    _, assets, _ = environment
    release(assets, version='1.5.0')
    assert run(environment, '--yes').returncode == 0
    release(assets, version='1.4.0')
    result = run(environment, '--yes')
    assert result.returncode == 2 and 'downgrade is not supported' in result.stderr


def test_interactive_approval_and_same_version_repair(environment):
    root, _, _ = environment
    result = run_interactive(environment, answers=[
        ('Installation destination [.agents]:', ''),
        ('Continue with latest stable release 1.4.0?', 'no'),
    ])
    assert result.returncode == 2
    assert not (root / '.agents').exists()
    result = run_interactive(environment, answers=[
        ('Installation destination [.agents]:', ''),
        ('Continue with latest stable release 1.4.0?', 'yes'),
        ('Approve this installation plan?', 'yes'),
    ])
    assert result.returncode == 0, result.stdout
    target = root / '.agents/skills/wiked/SKILL.md'
    target.write_text('local edit')
    missing = root / '.agents/commands/wiked-setup.md'
    missing.unlink()
    result = run(environment, '--dry-run')
    assert 'locally modified' in result.stdout and 'Reinstall' in result.stdout
    assert target.read_text() == 'local edit' and not missing.exists()
    assert run(environment, '--yes').returncode == 0
    assert target.read_bytes() == (DISTRIBUTION / 'skills/wiked/SKILL.md').read_bytes()
    assert missing.exists()


def test_update_removes_only_intact_owned_obsolete_files(environment):
    root, assets, _ = environment
    intact = 'skills/wiked/guides/obsolete.md'
    modified = 'skills/wiked/guides/local.md'
    release(assets, extra={intact: b'obsolete', modified: b'old'})
    assert run(environment, '--yes').returncode == 0
    destination = root / '.agents'
    (destination / modified).write_text('human edit')
    (destination / 'skills/third-party').mkdir()
    (destination / 'skills/third-party/file').write_text('keep')
    release(assets, version='1.5.0')
    result = run(environment, '--yes')
    assert result.returncode == 0, result.stderr
    assert not (destination / intact).exists()
    assert (destination / modified).read_text() == 'human edit'
    assert (destination / 'skills/third-party/file').read_text() == 'keep'
    assert modified not in json.loads((destination / '.wiked-install.json').read_text())['files']


@pytest.mark.parametrize('kind', ['corrupt', 'traversal', 'link', 'unlisted', 'prerelease'])
def test_rejects_unsafe_candidates_before_installing(environment, kind):
    root, assets, _ = environment
    member = None
    if kind in ('traversal', 'link', 'unlisted'):
        member = tarfile.TarInfo('../escape' if kind == 'traversal' else 'skills/wiked/unlisted')
        member.size = 1
        if kind == 'link':
            member.type = tarfile.SYMTYPE
            member.linkname = '/tmp/escape'
    release(assets, extra_member=member, prerelease=kind == 'prerelease')
    if kind == 'corrupt':
        (assets / 'distr.tar.gz').write_bytes(b'not a tar archive')
    result = run(environment, '--yes')
    assert result.returncode == 2
    assert not (root / '.agents').exists()


def test_versioned_source_archive_is_not_a_release_distribution(environment):
    root, assets, _ = environment
    path = assets / 'release.json'
    data = json.loads(path.read_text())
    data['assets'] = []
    path.write_text(json.dumps(data))
    result = run(environment, '--yes')
    assert result.returncode == 2 and 'Missing release asset: distr.tar.gz' in result.stderr
    assert not (root / '.agents').exists()


def test_beta_tag_is_rejected_even_when_not_marked_prerelease(environment):
    root, assets, _ = environment
    release(assets, version='1.4.0-beta')
    result = run(environment, '--yes')
    assert result.returncode == 2 and 'not a stable SemVer release' in result.stderr
    assert not (root / '.agents').exists()


def test_candidate_checks_only_contract_preserves_consumer_and_never_calls_tracker(environment):
    root, _, env = environment
    wiki = root / 'wiki'
    wiki.mkdir()
    (wiki / 'wiki-structure.yaml').write_text(yaml.safe_dump(contract()))
    (wiki / 'broken.md').write_bytes(b'\xff')
    before = snapshot(wiki)
    result = run(environment, '--yes')
    assert result.returncode == 0, result.stderr
    assert snapshot(wiki) == before
    assert not Path(env['KNOT_LOG']).exists()


@pytest.mark.parametrize('local,confirmation,ticket', [(False, 'yes\n', False),
                                                       (True, 'no\n', False),
                                                       (True, 'yes\n', True)])
def test_incompatibility_blocks_replacement_and_requires_separate_local_confirmation(environment, local, confirmation, ticket):
    root, _, env = environment
    assert run(environment, '--yes').returncode == 0
    before = snapshot(root / '.agents')
    (root / 'wiki').mkdir()
    value = contract()
    value['methodology_version'] = '2.0.0'
    (root / 'wiki/wiki-structure.yaml').write_text(yaml.safe_dump(value))
    # Ancestor tracker must never be used.
    (root.parent / '.knot.edn').write_text('{}')
    (root.parent / '.tickets').mkdir()
    if local:
        (root / '.knot.edn').write_text('{}')
        (root / '.tickets').mkdir()
    if local:
        result = run_interactive(environment, '--yes', answers=[
            ('Create a priority-1 HITL migration ticket in this local tracker?', confirmation.strip()),
        ])
    else:
        result = run(environment, '--yes', input=confirmation)
    assert result.returncode == 2 and 'Candidate contract validation failed' in result.stdout + result.stderr
    assert before == snapshot(root / '.agents')
    log = Path(env['KNOT_LOG'])
    assert log.exists() is ticket
    if ticket:
        text = log.read_text()
        assert text.startswith(str(root) + '\ninfo\n--json\n')
        assert str(root) + '\ncreate\n' in text
        assert '--priority\n1\n--mode\nhitl' in text
        assert '2.0.0' in text and 'requested distribution: 1.4.0' in text


def test_missing_prerequisites_do_not_install_tools(environment):
    root, _, env = environment
    tools = Path(env['PATH'].split(os.pathsep)[0])
    for missing in ('uv', 'knot'):
        isolated = root.parent / ('only-' + missing)
        isolated.mkdir()
        for name in ('uv', 'knot', 'curl'):
            if name != missing:
                (isolated / name).symlink_to(tools / name)
        result = subprocess.run(['/bin/bash', str(INSTALLER)], cwd=root,
                                env={**env, 'PATH': str(isolated)}, capture_output=True, text=True)
        assert result.returncode == 2 and f'Required tool missing: {missing}' in result.stderr
        assert not (root / '.agents').exists()


@pytest.mark.parametrize('destination', ['wiki/installed', 'raw', '.tickets', '.', '..'])
def test_rejects_consumer_owned_destinations(environment, destination):
    result = run(environment, '--yes', '--destination', destination)
    assert result.returncode == 2


def test_rejects_symlink_targets_and_warns_about_invalid_baseline(environment):
    root, _, _ = environment
    (root / '.agents').symlink_to(root.parent)
    assert run(environment, '--yes').returncode == 2
    (root / '.agents').unlink()
    (root / '.agents').mkdir()
    (root / '.agents/.wiked-install.json').write_text('{}')
    obsolete = root / '.agents/skills/wiked/obsolete'
    obsolete.parent.mkdir(parents=True)
    obsolete.write_text('unproven ownership')
    result = run(environment, '--yes')
    assert result.returncode == 0 and 'Invalid metadata proves no ownership' in result.stdout
    assert obsolete.read_text() == 'unproven ownership'


def test_concurrent_operation_is_blocked(environment):
    root, _, _ = environment
    with (root / '..agents.wiked-lock').open('w') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        result = run(environment, '--yes')
    assert result.returncode == 2 and 'Another Wiked operation' in result.stderr
    assert not (root / '.agents').exists()


def transaction_fixture(tmp_path):
    module = installer_module()
    destination = tmp_path / 'installed'
    destination.mkdir()
    first = 'skills/wiked/a'
    second = 'skills/wiked/new/b'
    old = destination / first
    old.parent.mkdir(parents=True)
    old.write_bytes(b'old')
    old.chmod(0o600)
    metadata = destination / '.wiked-install.json'
    metadata.write_text('old metadata')
    candidate = tmp_path / 'candidate'
    for name in (first, second):
        path = candidate / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'new')
    hashes = {name: module['digest'](candidate / name) for name in (first, second)}
    observed = {name: module['digest'](destination / name) for name in (first, second, '.wiked-install.json')}
    transaction = tmp_path / '.installed.wiked-transaction'
    return module, destination, transaction, candidate, hashes, observed


def test_partial_failure_restores_files_modes_metadata_and_directories(tmp_path, monkeypatch):
    module, destination, transaction, candidate, hashes, observed = transaction_fixture(tmp_path)
    before = snapshot(destination)
    original = shutil.copyfileobj

    def fail_second(source, output, *args):
        if str(output.name).endswith('/new/b'):
            output.write(b'partial')
            raise OSError('synthetic write failure')
        return original(source, output, *args)

    monkeypatch.setattr(shutil, 'copyfileobj', fail_second)
    with pytest.raises(OSError, match='synthetic'):
        module['install'](destination, transaction, candidate, '1.4.0', hashes, list(hashes), observed)
    assert snapshot(destination) == before
    assert not (destination / 'skills/wiked/new').exists()
    assert not transaction.exists()


def test_abrupt_interruption_requires_recovery_before_another_install(environment):
    root, _, env = environment
    assert run(environment, '--yes').returncode == 0
    before = snapshot(root / '.agents')
    module_source = INSTALLER.read_text().split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
    module_source = module_source.split('signal.signal(signal.SIGTERM', 1)[0]
    program = root.parent / 'interrupt.py'
    # Kill a separate process after it has modified the first file.
    program.write_text(module_source + '''
destination = Path.cwd() / '.agents'
transaction = destination.with_name('..agents.wiked-transaction')
candidate_tree = Path.cwd() / 'prepared'
name = 'skills/wiked/SKILL.md'
candidate_tree.joinpath(name).parent.mkdir(parents=True)
candidate_tree.joinpath(name).write_text('new interrupted release')
old_sync = sync_directory
def crash_after_mutation(path):
    old_sync(path)
    if path == destination.joinpath(name).parent:
        os.kill(os.getpid(), signal.SIGKILL)
sync_directory = crash_after_mutation
install(destination, transaction, candidate_tree, '1.5.0',
        {name: digest(candidate_tree / name)}, [name],
        {name: digest(destination / name), METADATA: digest(destination / METADATA)})
''')
    result = subprocess.run(['uv', 'run', '--script', str(program)], cwd=root, env=env,
                            capture_output=True, text=True)
    assert result.returncode == -9, result.stderr
    assert snapshot(root / '.agents') != before
    result = run(environment, '--yes')
    assert result.returncode == 2 and 'Run --recover' in result.stderr
    result = run(environment, '--recover')
    assert result.returncode == 0, result.stderr
    assert snapshot(root / '.agents') == before
    assert run(environment, '--yes').returncode == 0


def test_changed_target_since_plan_blocks_write(tmp_path):
    module, destination, transaction, candidate, hashes, observed = transaction_fixture(tmp_path)
    (destination / next(iter(hashes))).write_text('concurrent human edit')
    before = snapshot(destination)
    with pytest.raises(ValueError, match='changed since approval'):
        module['install'](destination, transaction, candidate, '1.4.0', hashes, list(hashes), observed)
    assert snapshot(destination) == before
    assert not transaction.exists()


def test_runtime_failure_does_not_offer_migration_ticket(environment):
    root, assets, env = environment
    (root / 'wiki').mkdir()
    (root / 'wiki/wiki-structure.yaml').write_text(yaml.safe_dump(contract()))
    (root / '.knot.edn').write_text('{}')
    (root / '.tickets').mkdir()
    # A synthetic runtime retains the release identity but cannot perform its check.
    files = release(assets)
    runtime = 'skills/wiked/scripts/validate_wiki.py'
    files[runtime] = b'METHODOLOGY_VERSION = "1.4.0"\nraise ImportError("missing dependency")\n'
    archive = assets / 'distr.tar.gz'
    with tarfile.open(archive, 'w:gz') as stream:
        for name, content in files.items():
            member = tarfile.TarInfo(name)
            member.size = len(content)
            stream.addfile(member, io.BytesIO(content))
    result = run(environment, '--yes', '--approve-migration-ticket')
    assert result.returncode == 2 and 'No migration ticket offered' in result.stderr
    assert not Path(env['KNOT_LOG']).exists()
    assert not (root / '.agents').exists()


def test_hardlinked_collision_is_rejected_without_changing_other_file(environment):
    root, _, _ = environment
    destination = root / '.agents'
    destination.mkdir()
    third_party = root / 'third-party'
    third_party.write_text('third party')
    os.link(third_party, destination / 'wiked-manifest.yaml')
    result = run(environment, '--yes', '--approve-collision', 'wiked-manifest.yaml')
    assert result.returncode == 2 and 'Hard-linked' in result.stderr
    assert third_party.read_text() == 'third party'


def test_dry_run_incompatibility_never_creates_ticket(environment):
    root, _, env = environment
    (root / 'wiki').mkdir()
    value = contract()
    value['methodology_version'] = '2.0.0'
    (root / 'wiki/wiki-structure.yaml').write_text(yaml.safe_dump(value))
    (root / '.knot.edn').write_text('{}')
    (root / '.tickets').mkdir()
    result = run(environment, '--dry-run', '--yes', input='yes\n')
    assert result.returncode == 2
    assert not Path(env['KNOT_LOG']).exists()


def test_recovery_rejects_corrupt_backup_without_installing(environment):
    root, _, _ = environment
    module = installer_module()
    destination = root / '.agents'
    destination.mkdir()
    file = destination / 'wiked-manifest.yaml'
    file.write_text('partially replaced')
    transaction = root / '..agents.wiked-transaction'
    (transaction / 'backup').mkdir(parents=True)
    (transaction / 'backup/0').write_text('corrupted backup')
    module['atomic_json'](transaction / 'journal.json', {
        'destination': str(destination), 'status': 'pending', 'directories': [],
        'files': [{'path': 'wiked-manifest.yaml', 'existed': True, 'hash': '0' * 64},
                  {'path': '.wiked-install.json', 'existed': False, 'hash': None}],
    })
    result = run(environment, '--recover')
    assert result.returncode == 2 and 'backup integrity failure' in result.stderr
    assert file.read_text() == 'partially replaced'
    assert transaction.exists()


def test_committed_transaction_is_cleaned_without_rollback(environment):
    root, _, env = environment
    assert run(environment, '--yes').returncode == 0
    before = snapshot(root / '.agents')
    transaction = root / '..agents.wiked-transaction'
    transaction.mkdir()
    (transaction / 'journal.json').write_text(json.dumps({
        'destination': str(root / '.agents'), 'status': 'committed',
    }))
    requests = Path(env['REQUEST_LOG']).read_text()
    assert run(environment, '--recover').returncode == 0
    assert not transaction.exists()
    assert before == snapshot(root / '.agents')
    assert Path(env['REQUEST_LOG']).read_text() == requests


def test_tracker_config_redirect_cannot_write_outside_consumer(environment):
    root, assets, env = environment
    (root / 'wiki').mkdir()
    value = contract()
    value['methodology_version'] = '2.0.0'
    (root / 'wiki/wiki-structure.yaml').write_text(yaml.safe_dump(value))
    (root / '.knot.edn').write_text('{}')
    (root / '.tickets').mkdir()
    env['KNOT_TICKETS_ROOT'] = str(root.parent)
    result = run(environment, '--yes', '--approve-migration-ticket')
    assert result.returncode == 2 and 'consumer-local tracker' in result.stderr
    assert '\ncreate\n' not in Path(env['KNOT_LOG']).read_text()


def test_real_uv_embedded_entrypoint_keeps_confirmation_input_and_script_isolation(environment):
    root, _, env = environment
    tools = Path(env['PATH'].split(os.pathsep)[0])
    (tools / 'uv').write_text(f'#!/usr/bin/env bash\nexec {shutil.which("uv")} "$@"\n')
    (root / 'wiki').mkdir()
    (root / 'wiki/wiki-structure.yaml').write_text(yaml.safe_dump(contract()))
    # A consumer Python project must not be resolved or changed by either run.
    (root / 'pyproject.toml').write_text('[project]\nname="invalid-consumer-project"\n')
    before = (root / 'pyproject.toml').read_bytes()
    result = run_interactive(environment, pipe=True, answers=[
        ('Installation destination [.agents]:', ''),
        ('Continue with latest stable release 1.4.0?', 'yes'),
        ('Approve this installation plan?', 'yes'),
    ])
    assert result.returncode == 0, result.stdout + result.stderr
    assert (root / 'pyproject.toml').read_bytes() == before
    assert not (root / 'uv.lock').exists() and not (root / '.venv').exists()


def test_failure_after_metadata_replacement_restores_previous_metadata(tmp_path):
    module, destination, transaction, candidate, hashes, observed = transaction_fixture(tmp_path)
    before = snapshot(destination)
    original = module['atomic_json']

    def fail_after_metadata(path, data, staging=None):
        original(path, data, staging)
        if path == destination / '.wiked-install.json':
            raise OSError('synthetic failure after metadata replacement')

    module['atomic_json'] = fail_after_metadata
    with pytest.raises(OSError, match='after metadata'):
        module['install'](destination, transaction, candidate, '1.4.0', hashes, list(hashes), observed)
    assert snapshot(destination) == before
    assert not transaction.exists()


def test_failure_of_first_install_removes_new_installation_directory(tmp_path, monkeypatch):
    module = installer_module()
    destination = tmp_path / 'absent'
    transaction = tmp_path / '.absent.wiked-transaction'
    candidate = tmp_path / 'candidate'
    name = 'skills/wiked/a'
    (candidate / name).parent.mkdir(parents=True)
    (candidate / name).write_text('new')

    def fail_write(source, output, *args):
        output.write(b'partial')
        raise OSError('synthetic first-install failure')

    monkeypatch.setattr(shutil, 'copyfileobj', fail_write)
    with pytest.raises(OSError, match='first-install'):
        module['install'](destination, transaction, candidate, '1.4.0',
                          {name: module['digest'](candidate / name)}, [name],
                          {name: None, '.wiked-install.json': None})
    assert not destination.exists() and not transaction.exists()


def test_pipe_entrypoint_uses_official_origin_and_asks_custom_destination(environment):
    root, _, env = environment
    result = run_interactive(environment, pipe=True, answers=[
        ('Installation destination [.agents]:', 'chosen'),
        ('Continue with latest stable release 1.4.0?', 'yes'),
        ('Approve this installation plan?', 'yes'),
    ])
    assert result.returncode == 0, result.stdout
    assert (root / 'chosen/.wiked-install.json').exists()
    assert not (root / '.agents').exists()
    assert 'Verified official GitHub repository (owner/repository):' not in result.stdout
    requests = Path(env['REQUEST_LOG']).read_text().splitlines()
    assert requests.count(f'https://api.github.com/repos/{REPOSITORY}/releases/latest') == 1


def test_explicit_parameters_skip_value_questions_but_not_approval(environment):
    root, _, _ = environment
    result = run_interactive(environment, '--destination=explicit', answers=[
        ('Continue with latest stable release 1.4.0?', 'yes'),
        ('Approve this installation plan?', 'no'),
    ])
    assert result.returncode == 2
    assert 'Verified official GitHub repository (owner/repository):' not in result.stdout
    assert 'Installation destination [.agents]:' not in result.stdout
    assert 'Destination: ' + str(root / 'explicit') in result.stdout
    assert not (root / 'explicit').exists()


def test_pipe_can_decline_selected_version_before_artifact_download(environment):
    root, _, env = environment
    result = run_interactive(environment, '--destination', '.agents', pipe=True, answers=[
        ('Continue with latest stable release 1.4.0?', 'no'),
    ])
    assert result.returncode == 2 and 'Latest stable release not approved' in result.stdout
    assert not (root / '.agents').exists()
    assert '/releases/download/' not in Path(env['REQUEST_LOG']).read_text()


def test_no_terminal_does_not_treat_stdin_answers_as_approval(environment):
    root, _, _ = environment
    result = run(environment, '--destination', '.agents', input='yes\nyes\nyes\n')
    assert result.returncode == 2 and 'No controlling terminal' in result.stderr
    assert not (root / '.agents').exists()
    assert run(environment, '--destination', '.agents', '--yes').returncode == 0


def test_automated_migration_requires_explicit_separate_approval(environment):
    root, _, env = environment
    (root / 'wiki').mkdir()
    value = contract()
    value['methodology_version'] = '2.0.0'
    (root / 'wiki/wiki-structure.yaml').write_text(yaml.safe_dump(value))
    (root / '.knot.edn').write_text('{}')
    (root / '.tickets').mkdir()
    result = run(environment, '--yes', input='yes\n')
    assert result.returncode == 2
    assert not Path(env['KNOT_LOG']).exists()
    result = run(environment, '--yes', '--approve-migration-ticket')
    assert result.returncode == 2  # A ticket never authorizes replacement.
    assert '\ncreate\n' in Path(env['KNOT_LOG']).read_text()
    assert not (root / '.agents').exists()


@pytest.mark.parametrize('arguments', [('--repository', 'other/wiked'), ('--repository=UniSoma/wiked',)])
def test_origin_argument_is_rejected_before_any_download(environment, arguments):
    root, _, env = environment
    result = run(environment, *arguments, '--yes')
    assert result.returncode == 2 and 'unrecognized arguments: --repository' in result.stderr
    assert not (root / '.agents').exists()
    assert not Path(env['REQUEST_LOG']).exists()


def test_release_assets_cannot_redirect_to_another_repository(environment):
    root, assets, env = environment
    release_path = assets / 'release.json'
    data = json.loads(release_path.read_text())
    data['assets'][0]['browser_download_url'] = data['assets'][0]['browser_download_url'].replace('UniSoma/wiked', 'other/wiked')
    release_path.write_text(json.dumps(data))
    result = run(environment, '--yes')
    assert result.returncode == 2 and 'Unexpected asset URL' in result.stderr
    assert not (root / '.agents').exists()
    assert 'other/wiked' not in Path(env['REQUEST_LOG']).read_text()


def test_help_does_not_prompt_and_describes_explicit_approval(environment):
    result = run(environment, '--help')
    assert result.returncode == 0
    assert '--approve-migration-ticket' in result.stdout
    assert '--repository' not in result.stdout
    assert 'No controlling terminal' not in result.stderr


def test_terminal_confirmation_accepts_case_and_surrounding_spaces(environment):
    result = run_interactive(environment, '--destination', '.agents', answers=[
        ('Continue with latest stable release 1.4.0?', ' YES '),
        ('Approve this installation plan?', 'Yes'),
    ])
    assert result.returncode == 0, result.stdout


def test_publication_docs_put_direct_entry_first_and_preserve_trust_exception():
    readme = (ROOT / 'README.md').read_text()
    guide = (ROOT / 'docs/installation.md').read_text()
    contract_text = (ROOT / 'docs/distribution.md').read_text()
    assert 'curl -fsSL https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh | bash\n' in readme
    assert '--repository' not in readme
    assert 'trust their sources' in readme
    assert 'without a download checksum' in guide
    assert 'distr.tar.gz' in guide and 'distr.tar.gz' in contract_text
    assert 'never stdin' in contract_text
    assert '--approve-migration-ticket' in guide and '--approve-migration-ticket' in contract_text
    assert 'SHA256SUMS' not in guide
