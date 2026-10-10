# Assisted Indexing

Load this guide only for the always human-guided incorporation of primary sources.

## Entry

1. Load `knot.md` and confirm an open ticket records the sources, objective, expected pages, and acceptance criteria.
2. Load `modeling.md` and `grill.md`, then satisfy the grill's preparation requirements for the indexing objective.
3. Read the configured local authoring reference when present, then navigate from the root index through the relevant top-level index to affected pages.
4. Only then inspect the in-scope source and compare it with consolidated content.

Before these conditions hold, do not access a source or change the wiki. Ticket context is governance, not operational evidence.
Apply existing local authoring criteria, but do not create or revise them incidentally; route candidate changes through governed maintenance.

## Decision Session

- Follow `grill.md` as the sole authority for interview mechanics, cadence, qualification, and closure.
- Separate source statements, current operation, proposed change, unresolved divergence, human decisions, and agent interpretation.
- Never decide currency, responsibility, terminology, divergence, or scope expansion silently.
- Record resolved domain terms in the configured context file only when `grill.md` permits that narrow in-session record.
- Write discussion and governed content in the configured instance language.

## Consolidate

After explicit grill closure:

1. Create one source page per primary source, preserving provenance without wholesale copying.
2. Record the configured provenance fields, including unavailable dates explicitly.
3. Update operational pages and indexes according to `modeling.md`.
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
