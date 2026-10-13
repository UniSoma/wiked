from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile

import pytest
import yaml

from test_wiked_installer import environment, run


ROOT = Path(__file__).parents[1]


@pytest.fixture
def packaging(tmp_path):
    source = tmp_path / 'source'
    shutil.copytree(ROOT / 'distr/agents', source / 'distr/agents')
    (source / 'scripts').mkdir()
    shutil.copyfile(ROOT / 'scripts/package-wiked.sh', source / 'scripts/package-wiked.sh')
    tools = tmp_path / 'packaging-bin'
    tools.mkdir()
    # Exercise the Bash entrypoint without resolving dependencies or using a network.
    uv = tools / 'uv'
    uv.write_text(f'''#!/usr/bin/env bash
set -eu
while [[ "$1" != python ]]; do shift; done
shift
exec {sys.executable} "$@"
''')
    uv.chmod(0o755)
    env = {**os.environ, 'PATH': str(tools) + os.pathsep + os.environ['PATH']}
    return source, tmp_path / 'output', env


def package(packaging, *args):
    source, output, env = packaging
    return subprocess.run(['bash', str(source / 'scripts/package-wiked.sh'),
                           '--output', str(output), *args], cwd=source.parent,
                          env=env, capture_output=True, text=True)


def test_package_exact_inventory_from_another_working_directory(packaging):
    source, output, _ = packaging
    distribution = source / 'distr/agents'
    (distribution / 'unlisted.txt').write_text('not distribution-owned')
    result = package(packaging)
    assert result.returncode == 0, result.stderr
    assert [path.name for path in output.iterdir()] == ['distr.tar.gz']
    assert str(output / 'distr.tar.gz') in result.stdout
    manifest = yaml.safe_load((distribution / 'wiked-manifest.yaml').read_text())
    inventory = {name for group in manifest['components'].values() for name in group}
    with tarfile.open(output / 'distr.tar.gz') as archive:
        members = archive.getmembers()
        assert {member.name for member in members} == inventory
        assert len(members) == len(inventory)
        for member in members:
            assert member.isfile() and not member.name.startswith('./')
            assert archive.extractfile(member).read() == (distribution / member.name).read_bytes()


def test_existing_archive_is_never_overwritten(packaging):
    _, output, _ = packaging
    output.mkdir()
    archive = output / 'distr.tar.gz'
    archive.write_bytes(b'previous release')
    result = package(packaging)
    assert result.returncode == 2 and 'File exists' in result.stderr
    assert archive.read_bytes() == b'previous release'


@pytest.mark.parametrize('kind', [
    'version', 'prerelease', 'missing', 'duplicate', 'traversal', 'namespace',
    'required', 'components', 'symlink', 'parent-symlink', 'hardlink', 'directory',
])
def test_invalid_sources_fail_before_output_creation(packaging, kind):
    source, output, _ = packaging
    distribution = source / 'distr/agents'
    manifest_path = distribution / 'wiked-manifest.yaml'
    manifest = yaml.safe_load(manifest_path.read_text())
    name = 'skills/wiked/guides/query.md'
    target = distribution / name
    if kind == 'version':
        manifest['distribution_version'] = '9.0.0'
    elif kind == 'prerelease':
        manifest['distribution_version'] = '1.4.0-beta'
    elif kind == 'missing':
        target.unlink()
    elif kind == 'duplicate':
        manifest['components']['instructions'].append(name)
    elif kind == 'traversal':
        manifest['components']['instructions'].append('../escape')
    elif kind == 'namespace':
        manifest['components']['instructions'].append('other/file')
    elif kind == 'required':
        manifest['components']['runtime'].remove('skills/wiked/scripts/validate_wiki.py')
    elif kind == 'components':
        manifest['components']['runtime'] = 'not a list'
    elif kind in ('symlink', 'hardlink'):
        original = source / 'original.md'
        target.rename(original)
        if kind == 'symlink':
            target.symlink_to(original)
        else:
            os.link(original, target)
    elif kind == 'parent-symlink':
        original = source / 'guides'
        target.parent.rename(original)
        target.parent.symlink_to(original, target_is_directory=True)
    elif kind == 'directory':
        target.unlink()
        target.mkdir()
    manifest_path.write_text(yaml.safe_dump(manifest))
    result = package(packaging)
    assert result.returncode == 2, result.stdout
    assert 'Wiked packaging failed' in result.stderr
    assert not output.exists()


def test_default_output_is_fresh_and_contains_only_archive(packaging):
    source, _, env = packaging
    result = subprocess.run(['bash', str(source / 'scripts/package-wiked.sh')],
                            cwd=source.parent, env={**env, 'TMPDIR': str(source.parent)},
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    directories = list(source.parent.glob('wiked-release-*'))
    assert len(directories) == 1
    assert [path.name for path in directories[0].iterdir()] == ['distr.tar.gz']


def test_packaged_artifact_installs_without_checksum_or_installer_assets(packaging, environment):
    _, output, _ = packaging
    assert package(packaging).returncode == 0
    consumer, assets, _ = environment
    shutil.copyfile(output / 'distr.tar.gz', assets / 'distr.tar.gz')
    result = run(environment, '--yes')
    assert result.returncode == 0, result.stderr
    assert (consumer / '.agents/skills/wiked/SKILL.md').is_file()
