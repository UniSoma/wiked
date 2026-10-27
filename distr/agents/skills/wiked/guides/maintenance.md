# Maintenance

Load this guide for consistency or structural review and correction.

## Review

- A read-only review needs no grill.
- Read the contract and complete [Contextual Preparation](authoring-context.md) before analyzing content or proposing corrections, including during read-only review.
- Load `modeling.md` for page, glossary, navigation, provenance, asset, or diagram structure; apply its content boundaries and coverage check to affected context and indexes.
- Check broken internal references, orphaned assets, incomplete diagram sets, inconsistent terms, incomplete provenance, contradictions, stale statements, and visual-only information. External links and bare URLs are informational outside typed canonical-reference fields and intent-map destination entries.
- When reviewing process diagrams, load [the diagram protocol](d2.md#step-correspondence-and-navigation)
  for step-to-section correspondence, matching titles, and stable identity.
  Interactivity is optional. During post-installation version review, identify
  whether the consumer uses Docsify from its existing viewer configuration. If it
  does, load [the optional integration guide](docsify.md), check compatibility,
  and propose adoption or review an already adopted integration. Do not enable
  it automatically, require Docsify, or flag static diagrams as nonconformant.
  Viewer configuration and content changes need authorized scope and grill
  closure; installation alone does not make images interactive. Adopt the guide's
  HTML example into a consumer-owned viewer with its adapter inline, never as a
  dependency on installed skill files. Skill removal or updates must not affect
  the adopted viewer; propose integration updates separately for authorization.
- Run the distributed validator. Errors are blocking; warnings require reporting and human disposition.
- The validator cannot decide operational meaning, ownership, order, conditions, naming, source reliability, or divergence.

After every human-installed change of Wiked version, run a maintenance agent with the installed skill and instance contract to review content against the new methodology. Technical installation success does not prove content conformity. The review is required; corrections still need their own authorized scope and closed grill. A same-version repair or intact no-op does not trigger this version-change review. The optional intent map is not mandatory adoption after an update.

Load the declared intent map when proposing routes or checking associations directly affected by reviewed pages. Renames/removals require reference checks; content changes require checking continued support for guidance. Do not require a full-map review after every page change. An explicit human request, concrete query location difficulty, or a relevant uncovered need or affected route discovered here may justify a proposal, not automatic creation. Route creation/revision is assisted indexing through `assisted-indexing.md` with editorial authority, human curation, and confirmed scope; do not broaden maintenance silently.

### Installed-version review

Load [the methodology-impact changelog](../CHANGELOG.md) only for version-change
review. Read the manifest and `.wiked-install.json` at the actual installation
root, two levels above the installed skill directory, not at the consumer root.
The manifest is the version authority; metadata records the pending
`maintenance_since` (exclusive) through installed `version` (inclusive).
Review every intervening entry, including releases skipped during installation.
Successive updates, same-version repair, and no-op do not clear that pending range.

Before reviewing, inspect the installed acknowledgment interface described in
[Runtime Interface](../scripts/README.md#maintenance-review-acknowledgment).
Retain its version, pending start, and state token for the reviewed installation.
The token identifies a state snapshot, not human consent. If inspection fails,
report the failure and leave acknowledgment pending; do not repair metadata by hand.
If no interval is pending, no acknowledgment is needed; do not invent one or
infer that a separately requested content review is unnecessary.

For a missing/invalid range, manifest/metadata mismatch, or coverage older than
the changelog baseline, report the uncertainty and seek human disposition; never
infer that no relevant change occurred. Legacy metadata without the pending field
cannot prove earlier reviews: use the recorded previous version for the new
update and ask whether earlier unreviewed changes require expanding the review.
Release declarations marked `none` do not dispense with the required maintenance
review. The changelog narrows change-specific checks, not the ordinary review
obligations above. It is methodological guidance, not operational evidence.

Report the reviewed interval, applicable impacts, affected content, validator
results, and findings. Obtain human disposition and explicit follow-ups for
unresolved findings; when appropriate, load `knot.md` and create or link correction
tickets in the consumer-local tracker so work is not forgotten. Review completion
may precede those corrections, but does not declare content conformity. A failure
that prevents completing the analysis keeps the review pending.
Reported content-validation errors remain blocking for accepting the affected
content, but can be fully analyzed findings with human-assigned follow-ups;
their presence alone is not proof that the review analysis failed. A validator
execution failure that prevents assessment does keep the review pending.

After the complete report and disposition, ask the human to explicitly confirm
completion of the review for the exact version and interval. Approval to begin
review, silence, or acceptance of individual findings is not this confirmation.
Only after receiving it, invoke the installed acknowledgment interface with the
retained snapshot and the explicit human-confirmation option. The option asserts
the confirmation already received; the program cannot establish that a human
approved or that analysis was complete. Never use it to bypass this gate.

The reviewing agent may remain active for this metadata-only operation. Do not
run it concurrently with another acknowledgment, installation, update, or recovery.
Installation, update, and recovery remain human operations with agents stopped.
The command runs offline, changes neither skill nor wiki, and creates no tickets.
It does not certify conformity or authorize corrections. Preserve the human
confirmation and report/follow-ups in the applicable governance records.
If the state changed, the version/range disagrees, or a transaction is pending,
stop and report the blocker. Never obtain a fresh token merely to bypass a stale
review; reassess the changed installation and obtain renewed human confirmation.
Other failures likewise leave acknowledgment pending until safely retried or
human recovery is complete. Never hand-edit the metadata or download an installer
to work around a missing installed interface.

## Correct

Before changing governed content, load and satisfy `grill.md` for a coherent correction objective. Resume it for any new substantive decision.

Context or index correction may include revising or creating canonical pages within confirmed scope. Review findings may instead become a later correction ticket; discovery does not authorize edits.

A substantive change to the configured local authoring reference is governed maintenance. A review may identify a candidate criterion or conflict; only a closed grill may create, change, or remove a local criterion.

Use `knot.md` when tracking is required. Do not silently broaden a correction into unrelated cleanup. After settling canonical Markdown, load `d2.md` and update D2 with its rendered derivative.
