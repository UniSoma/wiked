from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from test_wiked_installer import environment, installer_module, release, run, snapshot


ROOT = Path(__file__).parents[1]
SCRIPT = 'skills/wiked/scripts/acknowledge_review.py'


@pytest.fixture
def pending_installation(environment):
    root, assets, _ = environment
    assert run(environment, '--destination', 'custom install', '--yes').returncode == 0
    release(assets, version='1.6.0')
    result = run(environment, '--destination', 'custom install', '--yes')
    assert result.returncode == 0, result.stderr
    return root / 'custom install'


def helper(destination, *args, cwd=None, env=None):
    # The test interpreter has the installed prerequisites; no source module path
    # or dependency resolver is supplied to the portable installed command.
    return subprocess.run([sys.executable, '-B', str(destination / SCRIPT), *args],
                          cwd=cwd or destination.parent.parent,
                          env=env, capture_output=True, text=True)


def inspected(destination):
    result = helper(destination, '--inspect')
    assert result.returncode == 0, result.stderr
    state = json.loads(result.stdout)
    assert state['version'] == '1.6.0'
    assert state['maintenance_since'] == '1.4.0'
    assert state['state_token']
    return state


def approval(state):
    return ['--version', state['version'], '--since', state['maintenance_since'],
            '--state-token', state['state_token'], '--human-confirmed']


def test_installed_acknowledgment_requires_explicit_confirmation_and_is_metadata_only(
        environment, pending_installation):
    root, _, env = environment
    destination = pending_installation
    # Neither a configured wiki nor a tracker is a runtime prerequisite.
    (root / 'wiki').mkdir()
    (root / 'wiki/page.md').write_text('Untouched consumer content')
    before = snapshot(root)
    requests = Path(env['REQUEST_LOG']).read_bytes()
    state = inspected(destination)
    args = approval(state)
    missing = helper(destination, *args[:-1])
    assert missing.returncode == 2
    assert snapshot(root) == before
    dry_run = helper(destination, *args, '--dry-run')
    assert dry_run.returncode == 0, dry_run.stderr
    assert snapshot(root) == before
    result = helper(destination, *args)
    assert result.returncode == 0, result.stderr
    after = snapshot(root)
    metadata = 'custom install/.wiked-install.json'
    old_state = json.loads(before[metadata][0])
    new_state = json.loads(after[metadata][0])
    assert new_state == {**old_state, 'maintenance_since': None}
    assert {k: v for k, v in before.items() if k != metadata} == {
        k: v for k, v in after.items() if k != metadata}
    assert Path(env['REQUEST_LOG']).read_bytes() == requests
    assert not Path(env['KNOT_LOG']).exists()
    assert not destination.with_name('.' + destination.name + '.wiked-transaction').exists()
    # Replaying old approval cannot apply to the now changed metadata.
    assert helper(destination, *args).returncode == 2
    assert snapshot(root) == after


@pytest.mark.parametrize('field,value', [('version', '1.5.0'), ('since', '1.5.0'),
                                         ('state-token', '0' * 64)])
def test_stale_version_range_or_token_cannot_clear_pending_review(pending_installation, field, value):
    destination = pending_installation
    args = approval(inspected(destination))
    args[args.index('--' + field) + 1] = value
    before = snapshot(destination)
    result = helper(destination, *args)
    assert result.returncode == 2
    assert snapshot(destination) == before


@pytest.mark.parametrize('changed', ['metadata', 'manifest'])
def test_snapshot_is_bound_to_both_metadata_and_manifest(pending_installation, changed):
    destination = pending_installation
    args = approval(inspected(destination))
    # A semantically harmless byte change still invalidates the reviewed snapshot.
    target = destination / ('.wiked-install.json' if changed == 'metadata' else 'wiked-manifest.yaml')
    target.write_bytes(target.read_bytes() + b'\n')
    before = snapshot(destination)
    assert helper(destination, *args).returncode == 2
    assert snapshot(destination) == before


def test_snapshot_cannot_authorize_a_different_identical_installation(pending_installation):
    destination = pending_installation
    original = inspected(destination)
    other = destination.parent / 'other install'
    shutil.copytree(destination, other)
    relocated = inspected(other)
    assert relocated['state_token'] != original['state_token']
    before = snapshot(other)
    assert helper(other, *approval(original)).returncode == 2
    assert snapshot(other) == before
    assert helper(other, *approval(relocated)).returncode == 0


def test_noncanonical_script_path_preserves_inspection_identity(pending_installation):
    destination = pending_installation
    state = inspected(destination)
    script = destination / 'skills/../skills/wiked/scripts/acknowledge_review.py'
    before = snapshot(destination)
    result = subprocess.run([sys.executable, '-B', str(script), '--inspect'],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == state
    assert snapshot(destination) == before


def test_script_path_normalization_does_not_hide_a_symlink(pending_installation):
    destination = pending_installation
    (destination / 'linked').symlink_to(destination / 'skills', target_is_directory=True)
    script = destination / 'linked/../skills/wiked/scripts/acknowledge_review.py'
    before = snapshot(destination)
    result = subprocess.run([sys.executable, '-B', str(script), '--inspect'],
                            capture_output=True, text=True)
    assert result.returncode == 2
    assert 'Symlinks' in result.stderr
    assert snapshot(destination) == before


@pytest.mark.parametrize('kind', ['missing-baseline', 'invalid-baseline', 'invalid-range',
                                  'namespace', 'version', 'entrypoint', 'inventory',
                                  'symlink', 'hardlink', 'transaction'])
def test_unreliable_installations_block_inspection_and_acknowledgment(pending_installation, kind):
    destination = pending_installation
    args = approval(inspected(destination))
    metadata = destination / '.wiked-install.json'
    manifest = destination / 'wiked-manifest.yaml'
    if kind == 'missing-baseline':
        metadata.unlink()
    elif kind == 'invalid-baseline':
        metadata.write_text('{}')
    elif kind == 'invalid-range':
        state = json.loads(metadata.read_text())
        state['maintenance_since'] = '9.0.0'
        metadata.write_text(json.dumps(state))
    elif kind in ('namespace', 'version', 'entrypoint', 'inventory'):
        declaration = yaml.safe_load(manifest.read_text())
        if kind == 'namespace':
            declaration['namespace'] = 'other'
        elif kind == 'version':
            declaration['distribution_version'] = '1.7.0'
        elif kind == 'entrypoint':
            declaration['entrypoint'] = 'skills/other/SKILL.md'
        else:
            declaration['components']['instructions'].append('skills/wiked/unrecorded.md')
        manifest.write_text(yaml.safe_dump(declaration))
    elif kind in ('symlink', 'hardlink'):
        original = destination.parent / 'original-manifest'
        manifest.rename(original)
        if kind == 'symlink':
            manifest.symlink_to(original)
        else:
            os.link(original, manifest)
    else:
        destination.with_name('.' + destination.name + '.wiked-transaction').mkdir()
    before = snapshot(destination.parent)
    assert helper(destination, '--inspect').returncode == 2
    assert helper(destination, *args).returncode == 2
    assert snapshot(destination.parent) == before


def test_baseline_is_not_a_requirement_of_full_installed_file_conformity(pending_installation):
    destination = pending_installation
    (destination / 'skills/wiked/SKILL.md').write_text('Locally modified instruction')
    state = inspected(destination)
    before = snapshot(destination)
    assert helper(destination, *approval(state)).returncode == 0
    after = snapshot(destination)
    assert {k: v for k, v in after.items() if k != '.wiked-install.json'} == {
        k: v for k, v in before.items() if k != '.wiked-install.json'}


def test_documented_offline_invocation_ignores_consumer_python_project(environment, pending_installation):
    root, _, _ = environment
    destination = pending_installation
    (root / 'pyproject.toml').write_text('[project]\nname="invalid-project"\n')
    before = snapshot(root)
    result = subprocess.run(
        [shutil.which('uv'), 'run', '--no-project', '--no-python-downloads', '--offline',
         '--script', str(destination / SCRIPT), '--inspect'], cwd=root,
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['version'] == '1.6.0'
    assert snapshot(root) == before


def test_missing_offline_prerequisites_leave_review_pending(pending_installation):
    destination = pending_installation
    state = inspected(destination)
    before = snapshot(destination)
    empty_cache = destination.parent.parent / 'empty-offline-cache'
    result = subprocess.run(
        [shutil.which('uv'), '--cache-dir', str(empty_cache), 'run', '--no-project',
         '--no-python-downloads', '--offline', '--script', str(destination / SCRIPT),
         *approval(state)], cwd=destination.parent,
        capture_output=True, text=True)
    assert result.returncode != 0
    assert snapshot(destination) == before
    assert json.loads((destination / '.wiked-install.json').read_text())['maintenance_since'] == '1.4.0'


def test_first_install_has_no_pending_review_and_inspection_does_not_write(environment):
    root, _, _ = environment
    assert run(environment, '--yes').returncode == 0
    destination = root / '.agents'
    before = snapshot(root)
    result = helper(destination, '--inspect')
    assert result.returncode == 0, result.stderr
    state = json.loads(result.stdout)
    assert state['version'] == '1.4.0'
    assert state['maintenance_since'] is None
    assert snapshot(root) == before


def test_copy_ready_handoff_is_path_independent_for_custom_installation(environment):
    root, assets, _ = environment
    destination = root / 'custom install'
    assert run(environment, '--destination', str(destination), '--yes').returncode == 0
    release(assets, version='1.6.0')
    result = run(environment, '--destination', str(destination), '--yes')
    assert result.returncode == 0, result.stderr
    prompt = result.stdout.split('\nWIKED MAINTENANCE AGENT PROMPT:\n-----\n\n', 1)[1].split(
        '\n\n-----\n\n', 1)[0]
    assert str(root) not in prompt
    assert destination.name not in prompt
    assert 'SKILL.md' not in prompt and SCRIPT not in prompt
    assert 'uv run' not in prompt
    assert 'Installed version: 1.6.0' in prompt
    assert 'Pending methodology-impact range: 1.4.0 -> 1.6.0' in prompt
    inspected(destination)


def test_embedded_installer_core_is_synchronized():
    result = subprocess.run(
        [shutil.which('uv'), 'run', '--no-project', '--no-python-downloads', '--offline',
         'python', str(ROOT / 'scripts/sync-installer-core.py'), '--check'],
        cwd=ROOT.parent, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_sync_check_refuses_stale_core_and_generation_repairs_only_the_embedding(tmp_path):
    for relative in ('scripts/sync-installer-core.py', 'scripts/install-wiked.sh',
                     'distr/agents/skills/wiked/scripts/installation_state.py'):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    installer = tmp_path / 'scripts/install-wiked.sh'
    original = installer.read_text()
    marker = '# BEGIN GENERATED INSTALLATION STATE CORE\n'
    installer.write_text(original.replace(marker, marker + '# stale embedding\n'))
    command = [sys.executable, str(tmp_path / 'scripts/sync-installer-core.py')]
    before = snapshot(tmp_path)
    result = subprocess.run([*command, '--check'], capture_output=True, text=True)
    assert result.returncode == 1
    assert snapshot(tmp_path) == before
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert installer.read_text() == original
    after = snapshot(tmp_path)
    assert {k: v for k, v in before.items() if k != 'scripts/install-wiked.sh'} == {
        k: v for k, v in after.items() if k != 'scripts/install-wiked.sh'}


@pytest.mark.parametrize('abrupt', [False, True])
@pytest.mark.parametrize('relative_script', [SCRIPT, 'skills/../' + SCRIPT])
def test_acknowledgment_failure_uses_installer_compatible_recovery(
        environment, pending_installation, abrupt, relative_script):
    destination = pending_installation
    args = approval(inspected(destination))
    before = snapshot(destination)
    program = '''
import os
from pathlib import Path
import runpy
import signal
import sys
destination = Path(sys.argv[1])
abrupt = sys.argv[2] == 'True'
sys.path.insert(0, str(destination / 'skills/wiked/scripts'))
import installation_state
original = installation_state.atomic_json
def fail_after_metadata(path, data, staging=None, before_replace=None):
    original(path, data, staging, before_replace=before_replace)
    if path == destination / '.wiked-install.json':
        if abrupt:
            os.kill(os.getpid(), signal.SIGKILL)
        raise OSError('synthetic acknowledgment failure after metadata replacement')
installation_state.atomic_json = fail_after_metadata
script = destination / sys.argv[3]
sys.argv = [str(script), *sys.argv[4:]]
runpy.run_path(str(script), run_name='__main__')
'''
    result = subprocess.run([sys.executable, '-B', '-c', program,
                             str(destination), str(abrupt), relative_script, *args],
                            capture_output=True, text=True)
    transaction = destination.with_name('.' + destination.name + '.wiked-transaction')
    if abrupt:
        assert result.returncode == -9, result.stderr
        assert transaction.exists()
        interrupted = snapshot(destination)
        assert interrupted != before
        assert helper(destination, '--inspect').returncode == 2
        assert helper(destination, *args).returncode == 2
        assert snapshot(destination) == interrupted
        # Recovery uses only the self-contained human installer, not the helper.
        recovered = run(environment, '--destination', str(destination), '--recover')
        assert recovered.returncode == 0, recovered.stderr
    else:
        assert result.returncode != 0
        assert 'synthetic acknowledgment failure' in result.stderr
    assert snapshot(destination) == before
    assert not transaction.exists()


@pytest.mark.parametrize('changed', ['.wiked-install.json', 'wiked-manifest.yaml'])
def test_last_moment_snapshot_change_is_refused_without_overwriting_new_state(
        pending_installation, changed):
    destination = pending_installation
    core = installer_module()
    previous, since, token, observed = core['read_review_state'](destination, yaml.safe_load)
    original = core['atomic_json']
    expected = None

    def edit_before_replacement(path, data, staging=None, before_replace=None):
        nonlocal expected
        if path == destination / '.wiked-install.json':
            target = destination / changed
            target.write_bytes(target.read_bytes() + b'\n')
            expected = snapshot(destination)
        return original(path, data, staging, before_replace=before_replace)

    core['atomic_json'] = edit_before_replacement
    with pytest.raises(ValueError, match='changed since approval'):
        core['acknowledge_review'](
            destination, previous, since, token, observed,
            version=previous['version'], approved_since=since,
            state_token=token, human_confirmed=True)
    assert expected is not None
    assert snapshot(destination) == expected
    assert json.loads((destination / '.wiked-install.json').read_text())['maintenance_since'] == since
    assert not core['transaction_path'](destination).exists()


def test_human_installer_does_not_rebase_approval_over_a_changed_metadata_snapshot(
        pending_installation, monkeypatch):
    destination = pending_installation
    installer = installer_module()
    expected = None

    def confirm_then_external_change(message, optional=False):
        nonlocal expected
        metadata = destination / '.wiked-install.json'
        metadata.write_bytes(metadata.read_bytes() + b'\n')
        expected = snapshot(destination)
        return True

    installer['confirm'] = confirm_then_external_change
    monkeypatch.chdir(destination.parent)
    monkeypatch.setattr(sys, 'argv', ['installer', '--destination', str(destination),
                                    '--acknowledge-maintenance-review', '1.6.0'])
    with pytest.raises(ValueError, match='changed since approval'):
        installer['main']()
    assert expected is not None
    assert snapshot(destination) == expected
