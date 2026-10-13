from __future__ import annotations

import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tarfile

import pytest
import yaml

from test_wiked_installer import environment, run, snapshot
from test_wiked_validator import knot_environment, write_instance


ROOT = Path(__file__).parents[1]
SOURCE_VERSION = yaml.safe_load((ROOT / 'distr/agents/wiked-manifest.yaml').read_text())['distribution_version']


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
        license_text = (ROOT / 'LICENSE').read_bytes()
        assert b'Copyright (c) 2026 UniSoma' in license_text
        assert archive.extractfile('skills/wiked/LICENSE').read() == license_text
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


def test_package_reads_version_only_from_manifest_and_reports_publication_tag(packaging):
    source, _, _ = packaging
    distribution = source / 'distr/agents'
    manifest_path = distribution / 'wiked-manifest.yaml'
    manifest = yaml.safe_load(manifest_path.read_text())
    manifest['distribution_version'] = '1.5.2'
    manifest_path.write_text(yaml.safe_dump(manifest))
    changelog = distribution / 'skills/wiked/CHANGELOG.md'
    text = changelog.read_text()
    changelog.write_text(text.replace(f'## {SOURCE_VERSION} - ',
                                     f'## 1.5.2 - none\n\nNo methodological impact.\n\n## {SOURCE_VERSION} - ', 1))
    result = package(packaging)
    assert result.returncode == 0, result.stderr
    assert 'Packaged Wiked 1.5.2:' in result.stdout
    assert 'GitHub release tag v1.5.2' in result.stdout
    assert 'No release was published' in result.stdout


@pytest.mark.parametrize('kind', ['unknown', 'missing-current', 'duplicate', 'missing-baseline', 'missing-action'])
def test_invalid_changelog_blocks_packaging(packaging, kind):
    source, output, _ = packaging
    path = source / 'distr/agents/skills/wiked/CHANGELOG.md'
    text = path.read_text()
    heading = f'## {SOURCE_VERSION} - none'
    if kind == 'unknown':
        text = text.replace(heading, f'## {SOURCE_VERSION} - unknown')
    elif kind == 'missing-current':
        text = text.replace(heading, '## 9.0.0 - none')
    elif kind == 'duplicate':
        text = text.replace(heading, f'{heading}\n\nDuplicate.\n\n{heading}')
    elif kind == 'missing-baseline':
        text = text.replace('1.4.1 - baseline', '1.4.1 - none')
    else:
        text = text.replace('### Action', '### Missing')
    path.write_text(text)
    result = package(packaging)
    assert result.returncode == 2
    assert not output.exists()


def test_changelog_declarations_and_documented_dependencies():
    root = ROOT / 'distr/agents'
    metadata = runpy.run_path(str(root / 'skills/wiked/scripts/distribution.py'))
    declarations = metadata['release_declarations'](root)
    assert declarations['1.4.1'] == 'baseline'
    assert declarations['1.5.0'] == 'review'
    assert declarations[SOURCE_VERSION] in {'review', 'none'}
    maintenance = (root / 'skills/wiked/guides/maintenance.md').read_text()
    assert '../CHANGELOG.md' in maintenance
    for guide in ('SKILL.md', 'guides/query.md', 'guides/assisted-indexing.md'):
        assert 'CHANGELOG.md' not in (root / 'skills/wiked' / guide).read_text()


def test_packaged_artifact_installs_without_checksum_or_installer_assets(packaging, environment):
    _, output, _ = packaging
    assert package(packaging).returncode == 0
    consumer, assets, _ = environment
    manifest = yaml.safe_load((packaging[0] / 'distr/agents/wiked-manifest.yaml').read_text())
    release_path = assets / 'release.json'
    release_metadata = json.loads(release_path.read_text())
    version = manifest['distribution_version']
    release_metadata['tag_name'] = f'v{version}'
    release_metadata['assets'][0]['browser_download_url'] = (
        f'https://github.com/UniSoma/wiked/releases/download/v{version}/distr.tar.gz')
    release_path.write_text(json.dumps(release_metadata))
    shutil.copyfile(output / 'distr.tar.gz', assets / 'distr.tar.gz')
    result = run(environment, '--yes')
    assert result.returncode == 0, result.stderr
    assert (consumer / '.agents/skills/wiked/SKILL.md').is_file()
    assert (consumer / '.agents/skills/wiked/LICENSE').read_bytes() == (ROOT / 'LICENSE').read_bytes()

    # Operate only the installed artifact, from an unrelated cwd, with a synthetic
    # instance and tracker. No source-only docs or real consumer are required.
    assert write_instance(consumer.parent) == consumer
    unrelated = consumer.parent / 'unrelated-cwd'
    unrelated.mkdir()
    runtime_tools = consumer.parent / 'runtime-tools'
    runtime_tools.mkdir()
    installed_before_validation = snapshot(consumer / '.agents')
    result = subprocess.run(
        ['uv', 'run', '--script', str(consumer / '.agents/skills/wiked/scripts/validate_wiki.py'),
         '--repository-root', str(consumer), '--format', 'json'],
        cwd=unrelated, env=knot_environment(runtime_tools, consumer),
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    summary = json.loads(result.stdout)['summary']
    assert summary['errors'] == 0
    assert summary['warnings'] == 0
    assert summary['files_checked'] == 6
    assert snapshot(consumer / '.agents') == installed_before_validation
