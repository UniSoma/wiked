#!/usr/bin/env bash
# Human-operated source packaging; never installs or publishes Wiked.
set -euo pipefail
if ! command -v uv >/dev/null 2>&1; then
    echo 'Required tool missing: uv. Install it yourself before proceeding.' >&2
    exit 2
fi
export WIKED_SOURCE_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
exec uv run --no-project --no-python-downloads --python '>=3.11' --with 'PyYAML>=6,<7' python - "$@" <<'PY'
import argparse
import os
from pathlib import Path, PurePosixPath
import re
import runpy
import sys
import tarfile
import tempfile

import yaml

MANIFEST = 'wiked-manifest.yaml'
RUNTIME = 'skills/wiked/scripts/validate_wiki.py'
SCHEMA = 'skills/wiked/contracts/wiki-structure.schema.json'
IDENTITY = 'skills/wiked/scripts/distribution.py'
CHANGELOG = 'skills/wiked/CHANGELOG.md'
SEMVER = r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)'


def fail(message):
    raise ValueError(message)


def regular_file(source, name):
    if not isinstance(name, str) or not name or '\\' in name:
        fail('Invalid manifest path.')
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in ('', '.', '..') for part in name.split('/')):
        fail(f'Unsafe manifest path: {name!r}')
    if name not in (MANIFEST, 'commands/wiked-setup.md') and not name.startswith('skills/wiked/'):
        fail(f'Path outside Wiked namespace: {name}')
    target = source / name
    for item in (target, *target.parents):
        if item.is_symlink():
            fail(f'Symlinks cannot be packaged: {item}')
    if not target.is_file() or target.stat().st_nlink != 1:
        fail(f'Expected a regular, non-hard-linked file: {name}')
    return target


def main():
    parser = argparse.ArgumentParser(description='Validate and package Wiked; does not run tests or publish.')
    parser.add_argument('--output', type=Path, help='Output directory; defaults to a new temporary directory.')
    args = parser.parse_args()
    source = Path(os.environ['WIKED_SOURCE_ROOT']) / 'distr/agents'
    manifest = yaml.safe_load(regular_file(source, MANIFEST).read_text())
    version = str(manifest['distribution_version'])
    if (manifest['namespace'] != 'wiked' or not re.fullmatch(SEMVER, version)
            or manifest['preserve_unlisted_files'] is not True
            or manifest['entrypoint'] != 'skills/wiked/SKILL.md'):
        fail('Invalid distribution identity or stable SemVer version.')
    components = manifest['components']
    if not isinstance(components, dict) or any(not isinstance(group, list) for group in components.values()):
        fail('Manifest components must be lists of file paths.')
    inventory = [name for group in components.values() for name in group]
    paths = [(name, regular_file(source, name)) for name in inventory]
    if len(inventory) != len(set(inventory)):
        fail('Duplicate manifest entries.')
    if not {MANIFEST, RUNTIME, SCHEMA, IDENTITY, CHANGELOG, manifest['entrypoint']} <= set(inventory):
        fail('Required distribution interfaces missing.')
    runpy.run_path(str(source / IDENTITY))['release_declarations'](source)
    output = args.output or Path(tempfile.mkdtemp(prefix='wiked-release-'))
    for item in (output, *output.parents):
        if item.is_symlink():
            fail(f'Symlinks are not output directories: {item}')
    output.mkdir(parents=True, exist_ok=True)
    archive = output / 'distr.tar.gz'
    # Exclusive creation preserves any existing release artifact.
    with archive.open('xb') as stream:
        try:
            with tarfile.open(fileobj=stream, mode='w:gz', format=tarfile.USTAR_FORMAT) as package:
                for name, path in sorted(paths):
                    member = tarfile.TarInfo(name)
                    member.size = path.stat().st_size
                    member.mode = 0o644
                    with path.open('rb') as content:
                        package.addfile(member, content)
        except BaseException:
            archive.unlink()
            raise
    print(f'Packaged Wiked {version}: {archive.resolve()}')
    print(f'Upload only distr.tar.gz to GitHub release tag v{version}. No release was published.')


try:
    main()
except (OSError, ValueError, KeyError, TypeError, tarfile.TarError, yaml.YAMLError, KeyboardInterrupt) as exc:
    print(f'Wiked packaging failed: {exc}', file=sys.stderr)
    sys.exit(2)
PY
