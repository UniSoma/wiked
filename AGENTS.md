# Wiked source repository

This repository authors the Wiked methodology, distribution, schema, runtime,
tests, and development context. It does not host an operational wiki.

Read `GLOSSARY.md` and `docs/metodologia.md` before source work. Classify the
request before loading `grilling`:

- Read-only methodological review requires no ticket. Do not load or require
  `grilling` unless the requester asks to qualify the objective; that exception
  requires a Methodological grill. Otherwise, an unavailable skill does not block review.
- Creating or changing governed content, including changes arising from a review,
  requires an approved open Knot ticket and the source-authoring workflow below.

The approved ticket and validating requester define change scope and acceptance.
Before creating or changing governed content, invoke the environment-provided
`grilling` skill and explicitly close the Methodological grill as described in
`docs/metodologia.md`. If a compatible skill is unavailable, stop without editing.

## Invariants

- Generic instructions, runtime messages, schemas, and tests are in English and
  contain no consumer-specific knowledge. Preserve research in
  its original language; it is not normative guidance or operational evidence.
- Progressive disclosure is a design principle of the Wiked skill. Every
  methodology evolution must preserve lazy, objective-specific loading of its
  instructions and dependencies. Keep shared rules canonical and independently
  loadable when callers do not need the rest of a guide; do not make a workflow
  load unrelated guidance merely to reach one shared rule. Required prerequisites
  and governance gates remain mandatory.
- Use the `knot` skill and CLI for every ticket operation. Never read or edit
  `.tickets/` directly. Humans initialize the independent tracker and transfer
  its selected open tickets; never fall back to an ancestor's consumer tracker.
- Staging and committing on the official branches `develop` and `main` are
  exclusively human. Agents may create other branches and stage or commit on
  them. Pushing, merging, rebasing, tagging, publishing releases, installing
  tools, and replacing a running agent's installed skill belong to humans.
- Run all Python commands through `uv run`. Runtime or test changes require
  `uv run pytest`; instruction-only changes require targeted textual checks.
- Do not add tests that freeze methodological prose through substring, regex,
  or snapshot assertions. Literal documentation checks are for technical
  contracts (paths, identifiers, commands, and formats), not proof that an agent
  follows a rule. Apply the validation boundaries in `docs/metodologia.md`.
- `distr/agents/skills/wiked/` is the canonical source distribution here, not a local
  wiki installation. Its consumer workflows are not source-authoring instructions.
  Keep distribution sources outside automatic skill-discovery directories;
  consumers install the manifested files under their own `.agents/`.
- Preserve ownership boundaries in `distr/agents/wiked-manifest.yaml`. Consumer wiki,
  contract, ingestion material, governance, and unrelated agent files remain
  consumer-owned. Never embed a real consumer as a required source fixture.
- The Distributed validator and Instance contract are the active wiki-validation
  interfaces.
  Do not introduce wrappers or duplicate their rules in this file.

## Layout

- `distr/agents/skills/wiked/`: copyable instructions, schema, and portable runtime.
- `distr/agents/wiked-manifest.yaml`: version and exact distribution ownership.
- `distr/agents/commands/wiked-setup.md`: thin consumer setup adapter.
- `GLOSSARY.md`: canonical source-development vocabulary.
- `docs/`: source-development workflow, installation, and publication contract.
- `docs/agents/`: per-repository configuration for engineering skills.
- `tests/`: synthetic coverage and explicitly selected external integration.
- `reports/`: non-normative research and its provenance.

To operate an external consumer, work in that repository through its installed
skill and Instance contract. Source documents never authorize consumer edits.

## Agent skills

### Issue tracker

Work is tracked in the local Knot tracker through the `knot` skill and CLI. See
`docs/agents/issue-tracker.md`.

### Domain docs

Single-context: one root `GLOSSARY.md` and ADRs under `docs/adr/`. See
`docs/agents/domain.md`.
