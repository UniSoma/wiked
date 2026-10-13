---
id: wik-01m4sbvz62vp
title: Centralize Wiked version authority and define version increments
status: open
type: task
priority: 3
mode: hitl
created: '2026-10-13T00:51:14.236745554Z'
updated: '2026-10-13T00:51:14.236745554Z'
acceptance:
- title: Methodological grill decides the single version authority, increment policy and publication boundaries.
  done: false
- title: Approved implementation prevents manifest, runtime and release tag drift without duplicated manual updates.
  done: false
- title: Synthetic tests and release instructions cover the approved version workflow.
  done: false
links:
- wik-01m4sbvndyah
---

## Description

Deferred by the requester during the 2026-10-13 packaging grill. Distribution version is currently maintained in distr/agents/wiked-manifest.yaml and METHODOLOGY_VERSION in the distributed runtime; release tags must agree. Define a single authoritative version and a human-approved increment/release preparation process without embedding version literals in the packaging script. Scope and acceptance require a new Methodological grill; do not implement during packaging simplification.
