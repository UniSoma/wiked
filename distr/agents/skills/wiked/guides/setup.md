# Wiked Setup

Load this guide only for an explicit Wiked initialization or contract migration. Setup is an agent-guided governance flow over human-prepared prerequisites, not an installer.

## Preconditions

- Work from the intended consumer repository root.
- Require `uv` and `knot`; check optional `d2`, `pandoc`, `weasyprint`, and `rsvg-convert` only for requested capabilities.
- Require the distributed schema at `contracts/wiki-structure.schema.json` and validator at `scripts/validate_wiki.py`.
- Do not install tools, initialize or alter Git, replace this skill, or copy from repository-specific documentation.

## Governed Flow

1. Load `knot.md`; create or confirm an open setup ticket with objective and acceptance criteria.
2. Load `grill.md`. For an existing contract, validate compatibility and obtain explicit authorization for a defined migration before proposing migration changes. Apply [Contextual Preparation](authoring-context.md) to the existing state within that scope. Never migrate automatically.
3. Load `modeling.md` before structural or representational decisions, then resolve language, purpose, audience, scope, canonical terms and definitions, top-level branches, page types, states, provenance, Knot mappings, and whether approved local review criteria require an authoring reference. Prepare the agreed purpose, audience, scope, and terms and definitions for contract `initial_content` in the conversation or Knot records; do not write the contract or context file before explicit grill closure.
4. Close the grill with an explicit summary and confirmation.
5. After confirmation and within the confirmed scope, write the agreed values under contract `initial_content` and materialize only the configured root index, resolved context file, optional approved authoring reference, mandatory source index, agreed top-level indexes, schema-valid local contract, and fixed `raw/` and `raw/archive/` directories. The root index contains the configured title, purpose, audience, and scope and links exactly once to every configured reference and top-level index; the context contains the agreed terms and definitions. Do not create an empty authoring reference or list fictional pages.
6. Do not create fictional domain pages, placeholder operational claims, or placeholder files in the ingestion directories. Create the configured assets directory even when empty. Humans decide whether to persist ingestion material in Git.
7. Run the distributed validator with the explicit consumer root and resolve errors before acceptance.

### Contextual Preparation Exceptions

- For explicitly requested first initialization, the contract and context to be created are not prerequisites for the initial grill. Qualify initial terms in the conversation or Knot records and materialize the approved context only after explicit closure. This exception does not turn an incomplete existing instance into a new initialization.
- For an explicitly authorized migration, read the existing context and pertinent content as the prior state to preserve or change through explicit decisions. An incompatible contract does not authorize normal wiki authorship; this inspection is limited to the migration scope. If the configured context is absent, report the gap and require explicit recovery scope rather than reconstructing vocabulary automatically. Keep proposed terms in the conversation or Knot records until grill closure.

After every human-installed change of Wiked version, require a maintenance agent review through `maintenance.md` to assess content against the new methodology. An update alone authorizes neither wiki corrections nor contract migration.

Adopting `navigation.intent_map` is optional and explicitly authorized. Use a distinct, configurable root Markdown filename, such as `routes.md`, and require `methodology_version` 1.5.0 or newer while retaining `contract_version: 1.0`. Materialize the map and its one root-index link only after real intents, canonical destinations, and guidance are human-approved through `assisted-indexing.md`; use `modeling.md` for format and language. Do not create an empty or fictional map, silently adopt it on upgrade, or rewrite existing contracts. Instances without a map retain their navigation and validation behavior.

An existing contract is compatible only with `contract_version: 1.0` and a `methodology_version` in the installed major that is not newer than the distribution. Preserve and validate a compatible contract. Otherwise, stop without writing and require a separately, explicitly authorized migration scope and closed grill. Repository-specific migration and generic adoption automation are outside this flow. If the schema or validator is absent or incompatible, report failure and do not claim success. Never rewrite or migrate a contract automatically.
