---
id: wik-01m5q3w8swpt
title: Clarify diagram-only navigation and standard return links
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-24T14:08:48.444370342Z'
updated: '2026-10-24T14:09:41.548650170Z'
closed: '2026-10-24T14:09:41.548650170Z'
acceptance:
- title: Navigation-only work preserves the visual representation, makes the node itself clickable, and forbids additional visual link affordances.
  done: true
- title: Localized standard return links distinguish a single destination, multiple steps and repeated occurrences without changing node titles.
  done: true
- title: Review criteria cover each occurrence, link wording and visual preservation; targeted textual checks and validation limits are recorded.
  done: true
---

## Description

Methodological grill explicitly closed by the requester in this session. Approved scope: only distr/agents/skills/wiked/guides/d2.md navigation requirements and review criteria. Make existing nodes themselves clickable without redesigning labels, shapes, edges, styles or layout, and without adding clickable icons, buttons, symbols or other visual link affordances. Check render-induced visual differences rather than silently accepting them; report existing discrepancies outside the approved scope. Standardize return wording in the instance language, disambiguate multiple destinations by exact visible title and repeated same-title occurrences by meaningful context. Repeated occurrences retain distinct stable identifiers and may share a canonical description. No consumer edits, runtime/tests changes, version bump or publication. Validation: targeted textual checks and semantic review, not prose-freezing tests or claims of browser coverage.

## Notes

**2026-10-24T14:09:36.318578883Z**

Implemented only distr/agents/skills/wiked/guides/d2.md. Navigation-only rules preserve labels/shapes/connections/styles/layout, forbid added visual link affordances, and require review of renderer-induced differences. Return wording is localized with exact titles and meaningful occurrence context; repeated nodes keep unique stable IDs and individual returns. Review criteria cover every occurrence and visual preservation. Targeted shell checks passed: ASCII source surface, absence of docs/ or absolute environment dependencies, referenced local guide files exist, navigation section anchor is unique. Manual semantic review checked consistency with label equality, operation boundaries, consumer-owned viewer integration and unsupported-viewer reporting. No runtime/test change: pytest not applicable. No browser, consumer diagram or behavioral agent evaluation was performed; textual checks do not prove runtime navigation or agent compliance. No version bump or publication.

**2026-10-24T14:09:41.548650170Z**

Updated the canonical D2 navigation protocol and review criteria within the explicitly confirmed scope. Targeted textual checks and semantic review passed; consumer navigation remains untested and no release/version change was made.
