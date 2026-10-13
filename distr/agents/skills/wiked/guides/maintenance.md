# Maintenance

Load this guide for consistency or structural review and correction.

## Review

- A read-only review needs no grill.
- Read the contract and complete [Contextual Preparation](authoring-context.md) before analyzing content or proposing corrections, including during read-only review.
- Load `modeling.md` for page, glossary, navigation, provenance, asset, or diagram structure; apply its content boundaries and coverage check to affected context and indexes.
- Check broken internal references, orphaned assets, incomplete diagram sets, inconsistent terms, incomplete provenance, contradictions, stale statements, and visual-only information. External links and bare URLs are informational outside typed canonical-reference fields and intent-map destination entries.
- Run the distributed validator. Errors are blocking; warnings require reporting and human disposition.
- The validator cannot decide operational meaning, ownership, order, conditions, naming, source reliability, or divergence.

After every human-installed change of Wiked version, run a maintenance agent with the installed skill and local contract to review content against the new methodology. Technical installation success does not prove content conformity. The review is required; corrections still need their own authorized scope and closed grill. A same-version repair or intact no-op does not trigger this version-change review. The optional intent map is not mandatory adoption after an update.

Load the declared intent map when proposing routes or checking associations directly affected by reviewed pages. Renames/removals require reference checks; content changes require checking continued support for guidance. Do not require a full-map review after every page change. An explicit human request, concrete query location difficulty, or a relevant uncovered need or affected route discovered here may justify a proposal, not automatic creation. Route creation/revision is assisted indexing through `assisted-indexing.md` with editorial authority, human curation, and confirmed scope; do not broaden maintenance silently.

### Installed-version review

Load [the methodology-impact changelog](../CHANGELOG.md) only for version-change
review. Read the manifest and `.wiked-install.json` at the actual installation
root, two levels above the installed skill directory, not at the consumer root.
The manifest is the version authority; metadata records the pending
`maintenance_since` (exclusive) through installed `version` (inclusive).
Review every intervening entry, including releases skipped during installation.
Successive updates, same-version repair, and no-op do not clear that pending range.

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

After disposition, give the human the installer command with
`--acknowledge-maintenance-review X.Y.Z` for the exact reviewed installed version
and the actual `--destination` if customized. The human runs it with agents
stopped, confirms completion, and records the report/follow-ups as appropriate.
This metadata-only operation downloads nothing and changes neither wiki nor
installed skill. Do not acknowledge on the human's behalf or clear metadata by
hand. A version mismatch or interrupted transaction blocks acknowledgment.

## Correct

Before changing governed content, load and satisfy `grill.md` for a coherent correction objective. Resume it for any new substantive decision.

Context or index correction may include revising or creating canonical pages within confirmed scope. Review findings may instead become a later correction ticket; discovery does not authorize edits.

A substantive change to the configured local authoring reference is governed maintenance. A review may identify a candidate criterion or conflict; only a closed grill may create, change, or remove a local criterion.

Use `knot.md` when tracking is required. Do not silently broaden a correction into unrelated cleanup. After settling canonical Markdown, load `d2.md` and update D2 with its rendered derivative.
