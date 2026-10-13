---
id: wik-01m4sbvndyah
title: Simplify release packaging to a fixed distribution archive
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-13T00:51:04.254310470Z'
updated: '2026-10-13T02:28:43.292440647Z'
closed: '2026-10-13T02:28:43.292440647Z'
acceptance:
- title: Human-confirmed grill closure and approved scope are recorded before source edits.
  done: true
- title: One human-run packaging command validates manifest inventory and runtime version and creates only distr.tar.gz without overwriting existing output.
  done: true
- title: Installer downloads fixed-name archive from the selected stable release without release checksum assets; local baseline hashes and other safeguards remain.
  done: true
- title: Synthetic packaging and installer tests pass via uv run pytest; release contract and installation documentation agree.
  done: true
- title: Publication ticket criteria are reconciled and a separate future version-management ticket is created.
  done: true
links:
- wik-01m4sbvz62vp
---

## Description

Methodological grill explicitly closed by the requester on 2026-10-13. Implement scripts/package-wiked.sh to validate and package only distr.tar.gz; installer remains downloaded from main and selects a stable release. Remove release download checksums and versioned installer assets, retain installation baseline hashes, inventory checks, compatibility and transaction safeguards. Update tests, publication contract, installation guidance and conflicting publication ticket criteria. No Git operations or release publication. Version management is separate future work.

## Notes

**2026-10-13T00:55:22.757654366Z**

Methodological grill closure: requester chose fixed distr.tar.gz, validation/packaging only, no release download checksum, and no installer copy as a release asset. Requester explicitly confirmed the shared scope and amendment of wik-01m4khsrmqya, then switched out of Plan mode and authorized execution. Scope: scripts/package-wiked.sh, scripts/install-wiked.sh, synthetic tests, README, docs/installation.md, docs/distribution.md and the publication-boundary terminology in docs/metodologia.md. Exceptions: local installation hashes remain; versions remain in manifest/runtime pending separate ticket wik-01m4sbvz62vp. No consumer edits, Git, tooling installation or release publication.

**2026-10-13T00:56:57.256910361Z**

Implementation evidence: uv run pytest completed with 96 passed and 1 optional integration skipped. Synthetic coverage exercises the Bash packaging entrypoint, exact regular-file inventory, unlisted-file exclusion, manifest/runtime agreement, invalid inputs and links, refusal to overwrite output, fresh default output, and package-to-installer compatibility with only distr.tar.gz. Existing installer coverage still verifies local hash baselines, ownership, compatibility, transaction rollback/recovery and official pinned asset URLs. Targeted textual checks confirm obsolete installer/checksum download guidance is removed and README links the inspection section. The first test run found a collision between two synthetic fixture tool directories; isolating the packaging shim fixed it, and the complete suite passed. Publication ticket wik-01m4khsrmqya was reconciled; version work is tracked separately as wik-01m4sbvz62vp. No Git operations, release publication or real consumer installation occurred. Source work is ready for requester acceptance; ticket remains open.

**2026-10-13T02:28:43.292440647Z**

Requester accepted completion on 2026-10-13 and confirmed the remaining old-installer error was caused by cache. Delivered scripts/package-wiked.sh, fixed distr.tar.gz release downloads without checksum assets, preserved local installation hashes and safeguards, reconciled publication guidance and ticket criteria, and created future version-management ticket wik-01m4sbvz62vp. Validation: uv run pytest, 96 passed and 1 optional integration skipped. Human publication was observed separately; agents performed no Git operations or release publication.
