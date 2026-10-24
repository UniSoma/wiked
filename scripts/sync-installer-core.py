"""Generate/check the installer's literal, standalone canonical core embedding."""

import argparse
from pathlib import Path
import sys

BEGIN = '# BEGIN GENERATED INSTALLATION STATE CORE\n'
END = '# END GENERATED INSTALLATION STATE CORE\n'
ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / 'distr/agents/skills/wiked/scripts/installation_state.py'
INSTALLER = ROOT / 'scripts/install-wiked.sh'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    source = INSTALLER.read_text()
    if source.count(BEGIN) != 1 or source.count(END) != 1:
        parser.error('Installer must contain exactly one canonical core marker pair.')
    before, remainder = source.split(BEGIN)
    embedded, after = remainder.split(END)
    expected = CORE.read_text().rstrip() + '\n'
    if args.check:
        if embedded != expected:
            print('Installer core is stale; run uv run scripts/sync-installer-core.py.', file=sys.stderr)
            return 1
    else:
        INSTALLER.write_text(before + BEGIN + expected + END + after)
    return 0


if __name__ == '__main__':
    sys.exit(main())
