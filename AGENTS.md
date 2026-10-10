# Wiked source repository

This repository authors the Wiked methodology, distribution, schema, runtime,
tests, and development context. It does not host an operational wiki.

Read `CONTEXT-MAP.md`, `docs/CONTEXT.md`, and `docs/metodologia.md` before source
work. The approved Knot ticket and validating requester define scope and acceptance.
Before creating or changing governed content, invoke the environment-provided
`grilling` skill and explicitly close the Methodological grill as described in
`docs/metodologia.md`. If a compatible skill is unavailable, stop without editing.
Read-only reviews do not require a grill unless the requester asks to qualify the objective.

## Invariants

- Generic instructions, runtime messages, schemas, and tests are in English and
  contain no consumer-specific knowledge. Preserve historical research in its
  original language; it is not normative guidance or operational evidence.
- Use the `knot` skill and CLI for every ticket operation. Never read or edit
  `.tickets/` directly. Humans initialize the independent tracker and transfer
  its selected open tickets; never fall back to an ancestor's consumer tracker.
- Do not manipulate Git, publish releases, install tools, or replace a running
  agent's installed skill. Those operations belong to humans.
- Run all Python commands through `uv run`. Runtime or test changes require
  `uv run pytest`; instruction-only changes require targeted textual checks.
- `.agents/skills/wiked/` is the canonical source distribution here, not a local
  wiki installation. Its consumer workflows are not source-authoring instructions.
- Preserve ownership boundaries in `.agents/wiked-manifest.yaml`. Consumer wiki,
  contract, ingestion material, governance, and unrelated agent files remain
  consumer-owned. Never embed a real consumer as a required source fixture.
- The distributed runtime and instance contract are the active runtime interfaces.
  Do not introduce wrappers or duplicate their rules in this file.

## Layout

- `.agents/skills/wiked/`: copyable instructions, schema, and portable runtime.
- `.agents/wiked-manifest.yaml`: version and exact distribution ownership.
- `.agents/commands/wiked-setup.md`: thin consumer setup adapter.
- `docs/`: source-development vocabulary and workflow.
- `tests/`: synthetic coverage and explicitly selected external integration.
- `reports/`: historical, non-normative research and its provenance.

To operate an external consumer, work in that repository through its installed
skill and local contract. Source documents never authorize consumer edits.
