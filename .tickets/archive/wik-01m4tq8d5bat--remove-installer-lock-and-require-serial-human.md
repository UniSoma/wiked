---
id: wik-01m4tq8d5bat
title: Remove installer lock and require serial human operations
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-13T13:29:30.539427032Z'
updated: '2026-10-13T13:34:03.430335820Z'
closed: '2026-10-13T13:34:03.430335820Z'
acceptance:
- title: Methodological grill explicitly closed by requester confirmation of scope and exceptions.
  done: true
- title: Installer no longer creates or uses a lock file; existing lock files remain untouched and serial transaction protections are preserved.
  done: true
- title: English documentation declares serial user responsibility and unsupported concurrency without legacy cleanup guidance; synthetic tests cover absence of lock creation and preserved recovery.
  done: true
- title: uv run pytest passes and validation evidence is recorded.
  done: true
---

## Description

Requester approved removing the persistent installer lock rather than relocating or replacing it and explicitly confirmed the final Methodological grill summary. Concurrent installation, update, or recovery is unsupported user error; serial execution is the user's responsibility. Preserve transaction journal, backups, rollback, recovery and target integrity checks. Leave existing lock files untouched; no code or documentation for legacy lock removal, as the requester will guide current users. Approved scope: scripts/install-wiked.sh, docs/distribution.md, docs/installation.md and tests/test_wiked_installer.py. No consumer edits, installation, Git manipulation or publication.

## Notes

**2026-10-13T13:30:23.617524482Z**

Methodological grill explicitly closed: requester confirmed the final shared-understanding summary. Approved scope is installer, distribution/installation documentation and synthetic tests; remove locking without replacement, declare serial human responsibility, preserve journal/backups/rollback/recovery/integrity checks, leave legacy lock files untouched without cleanup guidance. No consumer operation, installation, Git manipulation or publication. No unresolved or lateral decisions.

**2026-10-13T13:33:51.546117658Z**

Implemented the confirmed scope in scripts/install-wiked.sh, docs/distribution.md, docs/installation.md and tests/test_wiked_installer.py. Removed fcntl/flock, lock path creation and lock descriptor lifetime; preserved transaction and recovery logic. CLI help and English documentation require serial operations and declare unsupported concurrency; recovery requires the previous operation to have stopped. Replaced the concurrency test with parameterized default/custom destination tests for serial dry-run, empty recovery, installation and repeat installation without lock creation, plus preservation of a preexisting lock file's bytes, inode, permissions and modification time. Validation: uv run pytest — 98 passed, 1 skipped in 83.56s. Existing interruption, rollback, backup integrity and changed-target tests passed. Targeted inspection found no remaining lock references in installer or documentation. No consumer edits, installation, Git manipulation or publication performed.

**2026-10-13T13:34:03.430335820Z**

Removed persistent installer locking, documented serial human responsibility, and preserved transactional recovery and integrity checks. Synthetic tests verify no lock creation for default/custom destinations and preservation of legacy lock files. uv run pytest: 98 passed, 1 skipped. No installation or publication performed.
