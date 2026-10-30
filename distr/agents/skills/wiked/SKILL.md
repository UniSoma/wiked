---
name: wiked
description: Operate a contract-driven, human-governed Markdown wiki. Use for querying the wiki, assisted indexing, consistency maintenance, setup, process diagrams, and requested PDF, DOCX, SVG, or PNG exports.
---

# Wiked

Wiked maintains progressively navigated operational Markdown while separating evidence, governance, and ingestion material.

## Start

1. Resolve the consumer repository root from the user's workspace. Never infer it from this skill's installation path.
2. Read `wiki/wiki-structure.yaml`, the instance contract, which configures language, version compatibility, paths, vocabulary labels, page types, states, navigation, an optional intent map and local authoring reference, and Knot mappings. It is not operational evidence.
3. If the contract is absent, use `guides/setup.md` only when the user asks to initialize Wiked. Otherwise stop and report that the instance is not configured.
4. Read the installed `distribution_version` from `../../wiked-manifest.yaml`, relative to this skill directory. Require `contract_version: 1.0` and a `methodology_version` in the installed major that is not newer than the distribution. If either version is malformed or incompatible, stop without processing wiki content; use `guides/setup.md` only for an explicitly requested migration.
   A declared `navigation.intent_map` additionally requires `methodology_version` 1.5.0 or newer, and a page type declaring `external_authority` requires 1.8.0 or newer. Do not adopt either or migrate the contract automatically.
5. Classify the request before loading any guide.

## Route

| Request | Load |
| --- | --- |
| Answer from consolidated knowledge | `guides/query.md` |
| Incorporate a source | `guides/assisted-indexing.md`, then its required guides |
| Create or revise intent routes | `guides/assisted-indexing.md`, then its required guides |
| Review or correct consistency or structure | `guides/maintenance.md`, plus `guides/modeling.md` for page structure |
| Create or revise wiki pages | `guides/modeling.md` and `guides/grill.md` |
| Initialize or migrate an instance | `guides/setup.md` and `guides/grill.md` |
| Operate or associate work tickets | `guides/knot.md` |
| Create, revise, regenerate, or review a permanent process diagram | `guides/d2.md`, then its operation-specific prerequisites |
| Propose, enable, or review optional Docsify diagram navigation | `guides/docsify.md`, then its operation-specific prerequisites |
| Produce a requested PDF, DOCX, SVG, or PNG | `guides/query.md`, then `guides/export.md`; add `guides/d2.md` only for a new or adjusted diagram |

Load only the applicable guides. A guide may explicitly require another guide; do not preload the entire directory.

## Invariants

- Only Markdown with a configured operational-content role is operational evidence. The configured context and local authoring reference govern vocabulary and authorship, respectively, but are not evidence of how the consumer operates.
- Sources, tickets, configuration, diagrams, rendered assets, and agent instructions are not operational evidence.
- The optional intent map is human-readable navigation, never operational evidence. Load it selectively under `guides/query.md` or when authoring routes or checking affected associations; it does not replace canonical pages or relax index rules.
- Query work is read-only except for an explicitly requested exported artifact.
- Creating or changing governed content, including permanent diagram sources and visualizations, requires `guides/grill.md` to close with explicit human confirmation first. Diagram operation boundaries are defined in `guides/d2.md`; requested temporary exports follow the bounded exception in `guides/export.md`.
- Before a governed workflow proceeds, the participating human must explicitly confirm that they are qualified to govern the current objective. This is session- and objective-specific, never instance configuration, and must be renewed for a new session or substantive objective.
- Assisted indexing also requires an open Knot ticket.
- Local ingestion material stays under `raw/`; successfully indexed local sources move to `raw/archive/` according to `guides/assisted-indexing.md`. Neither location is operational evidence or instance configuration.
- Humans decide meaning, responsibility, sequence, terminology, scope, source divergence, and acceptance. Automation checks only deterministic structure.
- Use the instance language from the contract for wiki content and user-facing artifacts. Keep Wiked's own instructions and diagnostics in English.
- Use only the Knot CLI for tickets. Never read or edit its storage directly.
- Never manipulate Git.
- Never modify this installed skill while operating an instance. Changes to Wiked belong to methodology evolution at its source repository.

## Versioned Interfaces

The distribution owns `contracts/wiki-structure.schema.json` and the distributed validator, `scripts/validate_wiki.py`. Validate a consumer with `uv run --script <wiked-skill>/scripts/validate_wiki.py --repository-root <consumer-root>`.
Installed-version review uses the metadata-only acknowledgment interface under
`guides/maintenance.md`; load it only for that workflow. It does not replace or
authorize modification of this skill.
