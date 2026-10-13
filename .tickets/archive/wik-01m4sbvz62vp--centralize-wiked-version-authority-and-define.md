---
id: wik-01m4sbvz62vp
title: Centralize Wiked version authority and define version increments
status: closed
type: task
priority: 3
mode: hitl
created: '2026-10-13T00:51:14.236745554Z'
updated: '2026-10-13T21:08:31.514371444Z'
closed: '2026-10-13T21:08:31.514371444Z'
acceptance:
- title: Methodological grill decides the single version authority, increment policy and publication boundaries.
  done: true
- title: Approved implementation prevents manifest, runtime and release tag drift without duplicated manual updates.
  done: true
- title: Synthetic tests and release instructions cover the approved version workflow.
  done: true
links:
- wik-01m4sbvndyah
---

## Description

Deferred by the requester during the 2026-10-13 packaging grill. Distribution version is currently maintained in distr/agents/wiked-manifest.yaml and METHODOLOGY_VERSION in the distributed runtime; release tags must agree. Define a single authoritative version and a human-approved increment/release preparation process without embedding version literals in the packaging script. Scope and acceptance require a new Methodological grill; do not implement during packaging simplification.

## Notes

**2026-10-13T20:30:23.017513913Z**

Methodological grill explicitly closed by the requester on 2026-10-13, with final adjustment: prepare 1.5.1; manifest is the sole version authority; human-approved SemVer increments and intended-release validation; distributed methodology-impact changelog covers 1.4.1 baseline and 1.5.0 onward, declaring impact or none per release; maintenance lazily reads the pending old-to-installed range, preserves the oldest unreviewed version across updates, and requires explicit human installer acknowledgment after report disposition and tracked correction follow-ups where appropriate. Review completion is not content conformity or correction authorization. Include README maintenance prompt, source/distributed instructions and synthetic tests. No Git operations, installation, tag creation or publication authorized.

**2026-10-13T20:43:38.306983603Z**

Delivery evidence: source distribution prepared as 1.5.1. Runtime reads its own installation-relative manifest through distribution.py; packaging requires explicit --release-version and installer checks release tag/manifest plus shared changelog declarations. Distributed CHANGELOG.md starts at 1.4.1, records the verifiable optional intent-map impact in 1.5.0, and declares no new wiki-text impact for 1.5.1. Installer metadata preserves maintenance_since across skipped releases, no-op and repair; --acknowledge-maintenance-review validates the exact installed version and records human acknowledgment transactionally, with no download or skill/wiki/ticket changes. Maintenance instructions cover interval selection, legacy uncertainty, finding disposition and Knot correction follow-ups; README includes a copyable governed maintenance prompt. Final validation: uv run pytest — 157 passed, 1 skipped, 90.81s. Synthetic package/install/installed-runtime proof also confirms validation does not mutate the installed distribution. No Git operations, real-consumer installation, release artifact preparation, tag creation or publication performed.

**2026-10-13T20:43:46.895315872Z**

Prepared Wiked 1.5.1 with manifest-only version authority, human-approved increment/release checks, distributed methodology-impact changelog from the 1.4.1 baseline, persistent pending maintenance ranges, explicit human acknowledgment, and README maintenance prompt with correction-ticket follow-ups. Approved source implementation verified by uv run pytest: 157 passed, 1 skipped. Publication, Git and consumer installation remain human work and were not performed.

**2026-10-13T20:58:25.614890474Z**

Requester reopened and explicitly confirmed the Methodological grill amendment: prefer the simplest interface and add contract-changing safeguards only with prior approval. Remove --release-version entirely; package-wiked.sh reads the sole manifest authority, validates the changelog and prints the matching publication tag without inspecting Git. Keep installer tag/manifest validation. Replace README maintenance procedure with the short installed-skill instruction already proposed; detailed behavior remains canonical in guides/maintenance.md. Scope is packaging CLI, README, corresponding source instructions and tests; distribution.py, review metadata, acknowledgment, 1.5.1 and changelog coverage remain unchanged. This supersedes the previous required packaging-version argument.

**2026-10-13T21:00:55.732352559Z**

Applied the explicitly approved simplification amendment: removed --release-version entirely, restoring bash scripts/package-wiked.sh with the manifest as its only version input; packaging prints the matching publication tag while installer tag/manifest validation remains intact. Replaced README maintenance procedure with a short installed-skill prompt; canonical details stay in guides/maintenance.md. Updated release instructions and regression tests, including a synthetic manifest-only version change. uv run pytest: 157 passed, 1 skipped, 98.38s. No installation, Git operations or publication performed; version remains prepared 1.5.1.

**2026-10-13T21:07:37.464062057Z**

Requester explicitly confirmed and closed the Methodological grill amendment: compact CHANGELOG.md into an impact index with a few lines per actionable change, canonical guide links, and one-sentence none/baseline entries. Record this source-authoring style in docs/distribution.md. Preserve existing release headings, review/action sections, coverage, version and behavior. No scripts, tests, interfaces or contracts are to change; no changelog filtering automation is added. Instruction-only validation uses targeted textual checks.

**2026-10-13T21:08:31.514371444Z**

Completed the explicitly approved instruction-only compact-changelog amendment. CHANGELOG.md reduced from 39 to 24 lines (82 words): short impact summary, canonical maintenance/modeling/contract links, and one-sentence none/baseline entries. Recorded concise impact-index authoring in docs/distribution.md, avoiding duplicated governance and internal-change narratives. Targeted textual checks passed for preserved release declarations/sections, local links and anchors, ownership, English/ASCII, installed maintenance routing and absence of source-document dependencies. Scripts, tests, contracts, version and behavior unchanged; no filtering automation or publication performed.
