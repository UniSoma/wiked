# Wiked methodology evolution

This document describes how Wiked is developed in its source repository. Executable consumer workflows are authored entirely in `distr/agents/skills/wiked/` and installed under `.agents/skills/wiked/` in consumers; this document must not be copied as a runtime dependency or used as operational evidence.

## Objective

Wiked maintains operational knowledge in progressively navigated Markdown while separating operational evidence, governance records, ingestion material, configuration, and agent instructions. The generic distribution is contract-driven so that a consumer can declare its language and structure without embedding domain-specific knowledge in Wiked.

This repository authors Wiked. Consumer repositories install the distribution and own their operational knowledge. Source changes and consumer operations use distinct entrypoints, authorities, and validation routes.

## Source architecture

The canonical distribution source is `distr/agents/skills/wiked/`, outside automatic skill-discovery directories. Its `SKILL.md` classifies consumer requests and lazy-loads only the applicable guide. The distribution owns generic instructions, the contract schema, and the Distributed validator; `distr/agents/wiked-manifest.yaml` identifies every owned file and requires unrelated files to be preserved. Manifest paths are relative to `distr/agents/` at source and to `.agents/` in the consumer installation. This repository is not a consumer and does not perform operational content indexing.

A consumer owns `wiki/wiki-structure.yaml`, operational Markdown under `wiki/`, ingestion material under the fixed `raw/` workspace, and its Knot records. Pending local sources remain under `raw/`; validated indexing moves only ticket-selected material to `raw/archive/YYYY-MM-DD_<ticket-id>/`. The Instance contract configures Wiked but does not encode human qualification or ingestion paths, move consumer terminology or facts into the distribution, or decide whether ingestion material is persisted in Git. The skill must remain usable without `docs/`.

The Distributed validator and Instance contract are the active wiki-validation
interfaces. The installed metadata-only review acknowledgment command is a
separate installation-state interface, governed by the distributed maintenance
guide. Source-development documents describe their evolution but do not duplicate
their executable rules.

Consumer workflows use the Installed skill but never modify it. Before a Runtime
cutover, coexistence with a previous validator or contract authority is
temporary and must not produce wrappers or duplicated rules.

## Development workflow

### Route the request

Read `GLOSSARY.md` and this document, then distinguish
read-only methodological review from creating or changing governed content
before loading the environment-provided `grilling` skill.

Read-only review may inspect source material and report findings without an open
Knot ticket. Do not load or require `grilling` for this route unless the requester
asks to qualify the objective. Without that request, an unavailable skill does
not block review. Requested qualification requires a Methodological grill using
the skill compatibility, decision, and explicit shared-understanding confirmation
rules below; it does not by itself require a ticket or authorize edits.

If a review leads to proposed changes, enter the governed-change workflow before
editing. Review findings do not substitute for an approved open ticket or explicit
grill closure covering those changes. This source route does not authorize
consumer operations, which use the installed skill and local Instance contract.

### Governed changes

1. Confirm an open Knot ticket whose scope and acceptance criteria authorize Methodology evolution.
2. Load `GLOSSARY.md`, then invoke the environment-provided `grilling` skill. The skill is a source-authoring dependency, not part of the Wiked distribution. If it is unavailable or does not keep fact-finding with the agent, decisions with the validating requester, unresolved decisions open, and implementation blocked until explicit shared-understanding confirmation, stop without editing governed content.
3. Establish that the session is methodological, state one coherent objective and its initial file scope, and inspect the affected distribution, source guidance, tests, and Reference instance without treating consumer content as a generic requirement. Compare a proposed rule with every source or distributed guide that executes or constrains it.
4. Treat `README.md`, `AGENTS.md`, `GLOSSARY.md`, source-development instructions, tests, and the Wiked distribution as governed methodological content. Before grill closure, do not edit that content. Knot tickets and notes may preserve decisions or lateral discoveries, but must not interrupt the current decision sequence or silently expand its scope.
5. When no in-scope decision remains, summarize the objective, scope, decisions, exceptions, affected content, and lateral pending issues. The validating requester must explicitly confirm that the summary represents shared understanding before consolidation. Confirmation authorizes only the summarized objective and scope; a new substantive decision resumes the grill.
6. Change the smallest coherent source surface. Keep generic Wiked instructions and diagnostics in English and free of consumer-specific knowledge.
7. Verify the source change through the applicable route below and record evidence in the ticket.
8. Exercise consumer behavior through that repository's installed skill and Instance contract, never by importing rules from source `docs/` into the consumer workflow.

## Validation routes

- Instruction-only changes use Targeted textual checks. Verify active links, English generic instructions, explicit author-versus-consumer identity, absence of `docs/` dependencies from the skill, and correct routing to the Instance contract.
- Python runtime or test changes use `uv run pytest`. The default suite covers generic fixtures without a real consumer or tracker. Optional integration uses `WIKED_CONSUMER_ROOT=/absolute/path/to/consumer uv run pytest -m integration`; the named external consumer must provide its contract and Knot environment.
- The Distributed validator can be invoked directly for an authorized external proof with `uv run --script distr/agents/skills/wiked/scripts/validate_wiki.py --repository-root /absolute/path/to/consumer`. The source root is not a consumer.
- Consumer wiki changes follow the validation selected by the installed skill and the Instance contract. Do not substitute a source-development command for the consumer route.

Textual and structural checks do not prove that an agent follows methodological
instructions. Reserve literal documentation assertions for technical contracts,
such as paths, identifiers, commands, and formats. Do not freeze prose through
substring, regex, or snapshot tests: equivalent wording may fail while a
contradictory instruction may pass. Review semantic coherence and governance
boundaries methodologically rather than inferring them from phrase presence.

When removing prose assertions, record the rationale and critical behaviors that
remain unevaluated in the ticket. A replacement Behavioral evaluation need not
already exist; specify its scenarios in a linked implementation ticket with
context, user request, expected behavior, observable violations, evidence, and
evaluation method. Do not claim that specification supplies behavioral coverage.
Future evaluations must observe actions and outcomes as well as responses, use
explicit token/cost and execution limits, and distinguish exploratory single
runs from repeated measurements of consistency. Their implementation requires
its own approved scope and Methodological grill; it is not mandatory validation
for every instruction change.

Behavioral evaluation results depend on the model, harness, configuration, and
methodology version. They are not deterministic proof of instruction quality or
Operational evidence.

Do not run redundant validation commands when one route already covers the changed file types. Errors block acceptance; warnings require explicit disposition but never authorize an automated semantic decision.

## Publication boundary

The approved [publication and distribution contract](./distribution.md) defines
immutable versions, package validation, release channels, licensing, installation,
and updates. Its implementation and first publication are separately tracked
executor work. Preparing a tree does not publish it. Agents do not publish
releases, install tooling, or replace their own skill. Staging and committing on
the official branches `develop` and `main` are exclusively human. Agents may
create other branches and stage or commit on them; pushing, merging, rebasing,
tagging, and releasing remain human.

Publication may transfer only files owned by the Distribution manifest and source-development material explicitly assigned to Wiked. Consumer-owned wiki content, contracts, ingestion material, governance, and third-party agent files remain with the consumer. Humans transfer only the selected open source tickets into an independent tracker.

## Extraction Methodological grill - 2026-10-10

The validating requester explicitly confirmed the final summary of the reopened
Methodological grill. This supersedes the earlier inventory-only cleanup plan.
The approved delivery has three parts: an independent author tree, the effective
cutover of the consumer to a consumer-only layout, and self-contained open source
tickets ready for manual transfer. All three deliveries and their coordinating
epic require completion and integrated human acceptance before transfer.

The verified author tree is authorized provisional custody: source-only originals,
development automation, and approved generated residues may be removed from the
consumer now. Consumer entrypoints must rely only on its installed distribution
and local contract, never on the prepared author tree. A missing necessary
component outside the installation reopens the decision; it does not authorize
copying source instructions into the consumer. The temporary author directory's
ignore rule and historical governance records are explicit exceptions.

The manifested distribution remains unchanged. Generic tests use synthetic
fixtures; real-consumer integration is optional and requires an explicit root.
Historical research is preserved in its original language as a non-normative
exception. The requester's sandbox configuration is preserved on both sides;
its broader dependency policy remains future work. Publication and the installer
are independent future work. Git, repository creation, and physical transfer of
the author tree and selected open tickets belong to humans. Closed historical
tickets remain in the original tracker. Delivery evidence and the ticket list
belong to the governance history and handoff, not the active consumer tree.
