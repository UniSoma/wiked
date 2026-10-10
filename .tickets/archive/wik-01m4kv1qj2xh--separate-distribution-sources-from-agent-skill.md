---
id: wik-01m4kv1qj2xh
title: Separate distribution sources from agent skill discovery
status: closed
type: task
priority: 2
mode: afk
created: '2026-10-10T21:21:05.090199212Z'
updated: '2026-10-10T21:23:39.454611532Z'
closed: '2026-10-10T21:23:39.454611532Z'
acceptance:
- title: All 16 manifested files reside under distr/agents/ with unchanged bytes and relative manifest paths; no source-local .agents/skills/wiked remains.
  done: true
- title: Source guidance, links, and tests use the new source layout and explicitly distinguish it from consumer installation paths.
  done: true
- title: Historical report bytes are preserved and reports/README.md documents relocated references.
  done: true
- title: uv run pytest and targeted link, inventory, and consumer-path checks pass.
  done: true
---

## Description

Move the 16 owned distribution files from .agents/ to distr/agents/ so source-authoring agents do not automatically discover the consumer skill. Update source context, links, and tests; explicitly state that this repository is not a consumer. Preserve installed consumer paths, distribution contents and version, and the historical report bytes. Document historical link relocation in reports/README.md. The validating requester explicitly confirmed this scope with "de acordo", closing the Methodological grill before source edits. Publication and installer work remain separate.

## Notes

**2026-10-10T21:23:39.454611532Z**

Moved all 16 distribution files from .agents/ to distr/agents/ with identical SHA-256 hashes and unchanged version/manifest-relative paths. Updated AGENTS.md, CONTEXT-MAP.md, README.md, docs/CONTEXT.md, docs/metodologia.md, reports/README.md, and test source paths. Consumer installation references remain .agents/. Source links resolve, old discovery path is absent, and the harness removed wiked from available skills after relocation. Historical report SHA-256 remains 272b49fdd54426533aeecef9bcb0a9f814e08476a07f947f73f78d7b119e418d. uv run pytest: 31 passed, 1 optional integration skipped. uv used a successful copy fallback after an environment hardlink warning; no validation failures.
