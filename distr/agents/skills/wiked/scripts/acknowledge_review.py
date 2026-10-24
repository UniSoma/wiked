# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Inspect/acknowledge installed review metadata; invoke with uv --offline.

Run only this helper during the reviewing agent's active session. Do not run
installation, updates, recovery, or concurrent operations. --human-confirmed is
an explicit caller assertion, not machine-verifiable evidence of human approval.
Missing offline prerequisites leave the review pending.
"""

import argparse
import json
import os
from pathlib import Path
import sys

# Inspection and acknowledgment must not create installed __pycache__ files.
sys.dont_write_bytecode = True

import yaml

from installation_state import acknowledge_review, read_review_state, safe_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inspect', action='store_true', help='Read JSON version, pending range, and state token without changes.')
    parser.add_argument('--version')
    parser.add_argument('--since', help='Exact maintenance_since value approved by the human.')
    parser.add_argument('--state-token', help='Token from the inspected metadata and manifest snapshot.')
    parser.add_argument('--human-confirmed', action='store_true', help='Assert explicit human approval after complete review, report, and finding disposition.')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.inspect and any((args.version, args.since, args.state_token, args.human_confirmed, args.dry_run)):
        parser.error('--inspect cannot be combined with acknowledgment options.')
    if not args.inspect and not all((args.version, args.since, args.state_token, args.human_confirmed)):
        parser.error('Acknowledgment requires --version, --since, --state-token, and --human-confirmed.')
    # Reject symlinks before lexical normalization can hide a canceled component.
    # Normalize spelling without resolve so tokens and recovery journals use the
    # same absolute installation identity as the human installer.
    script = Path(__file__).absolute()
    safe_path(script, '')
    destination = Path(os.path.abspath(script)).parents[3]
    previous, since, token, observed = read_review_state(destination, yaml.safe_load)
    if args.inspect:
        print(json.dumps({'version': previous['version'], 'maintenance_since': since,
                          'state_token': token}, sort_keys=True))
        return
    changed = acknowledge_review(destination, previous, since, token, observed,
                                 version=args.version, approved_since=args.since,
                                 state_token=args.state_token,
                                 human_confirmed=args.human_confirmed, dry_run=args.dry_run)
    if args.dry_run:
        print('Dry run: no review acknowledged.')
    elif changed:
        print(f'Maintenance review acknowledged through {previous["version"]}; this does not establish content conformity or authorize corrections.')
    else:
        print('No pending maintenance review; nothing changed.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f'Wiked review acknowledgment failed: {exc}', file=sys.stderr)
        sys.exit(2)
