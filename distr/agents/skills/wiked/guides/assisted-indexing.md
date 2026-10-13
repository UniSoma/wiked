# Assisted Indexing

Load this guide for always human-guided incorporation of primary sources or curation of intent routes grounded in existing canonical pages.

## Entry

1. Load `knot.md` and confirm an open ticket records the sources or existing canonical destinations, objective, expected pages or routes, and acceptance criteria.
2. Load `grill.md`, then satisfy its preparation requirements for the indexing objective.
3. Complete [Contextual Preparation](authoring-context.md) for the indexing objective.
4. Only then inspect the in-scope source and compare it with consolidated content.

Before these conditions hold, do not access a source or change the wiki. Ticket context is governance, not operational evidence.
Apply existing local authoring criteria, but do not create or revise them incidentally; route candidate changes through governed maintenance.

## Intent Route Curation

- Propose routes only for an explicit human request, concrete location difficulty observed in a query, or a relevant uncovered need or affected route found during indexing or maintenance. Do not create one route per question or new page.
- Load the declared map when proposing routes or checking affected associations. Read the canonical destinations and load `modeling.md` for the common format; do not load the entire map indiscriminately for unrelated authoring.
- Creating or changing routes requires an open indexing ticket, editorial authority qualified for this objective under `grill.md`, and human curation of the intent, destinations, and support for each guidance. Do not presume a querying reader is that authority. A query opportunity alone authorizes no indexing, map write, or governance record.
- Route-only indexing uses the existing canonical pages as its basis; do not fabricate a primary source page or ingestion material. Close the grill before editing the map or adopting it through a separately approved contract migration.
- When in-scope pages change, check only directly affected routes: verify references for renames/removals and whether guidance remains supported after content changes. Do not require a full-map review for every change or silently expand scope. New or revised associations require human curation; defer unrelated opportunities.

## Decision Session

- Load `modeling.md` when analyzing or proposing page, glossary, index, or intent-route changes, not solely for contextual preparation.
- Follow `grill.md` as the sole authority for interview mechanics, cadence, qualification, and closure.
- Separate source statements, current operation, proposed change, unresolved divergence, human decisions, and agent interpretation.
- Never decide currency, responsibility, terminology, divergence, or scope expansion silently.
- Keep resolved domain terms and definitions in the conversation or Knot records until explicit grill closure, as required by `grill.md`; do not write them to the configured context file during the interview.
- Write discussion and governed content in the configured instance language.

## Consolidate

After explicit grill closure:

1. Create one source page per primary source, preserving provenance without wholesale copying. For route-only curation, skip source creation and ingestion archiving.
2. For source incorporation, record the configured provenance fields, including unavailable dates explicitly.
3. Consolidate operational pages, then agreed terms and definitions in the configured context and navigation in indexes, within the confirmed scope. Apply `modeling.md`'s content boundaries and destination coverage check. Update approved intent routes and review directly affected associations without relaxing index invariants.
4. Use the latest evidence explicitly describing current operation; retain unresolved conflicts as configured pending items.
5. Attach contextual source-page citations to interpretations, time-sensitive claims, and divergences.
6. If validated process changes affect a diagram, update canonical Markdown first, then load `d2.md`.
7. Only after validation, move each ticket-selected local source from `raw/` to `raw/archive/YYYY-MM-DD_<ticket-id>/`, where the date is the completed indexing date. It may be a file or directory at any depth below `raw/` except `raw/archive/`; preserve its name and contents, and stop rather than overwrite an existing destination. Nothing else under `raw/` enters scope implicitly. External sources remain external.

## Complete

- Keep only the same source and objective in the current ticket; record independent discoveries separately.
- Record changed pages in the ticket.
- Run the versioned validator through the command declared by the distribution and resolve all errors. Report every warning for human disposition.
- Before closing the ticket, reassess affected pages and acceptance criteria.
- A ticket with external work-item references follows the synchronization procedure in `knot.md` after successful local closure.
- The indexer and instance maintainer decide whether to persist ingestion material in Git. Never alter Git or treat `raw/` material as operational evidence.
