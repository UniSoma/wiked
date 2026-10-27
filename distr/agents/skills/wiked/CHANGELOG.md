# Methodology-impact changelog

Impacts on existing wiki texts; follow [version review](guides/maintenance.md#installed-version-review).

## 1.7.0 - review

### Review

- Contextual source-page citations in page bodies are an optional local editorial
  criterion, not a universal requirement; configured source references remain mandatory.
- The optional Docsify integration example now exposes a native link to each
  enhanced diagram's original SVG.

### Action

- Do not flag existing body citations as nonconformity or remove them automatically.
  Maintenance may propose removing them or adopting a criterion in the local authoring
  reference, following [local contextual citations](guides/authoring-context.md#local-contextual-citations).
- Review time-sensitive claims that relied on a body citation for currency and state
  their effective date or period in the text.
- If the wiki already uses the Docsify integration, propose adopting the
  original-diagram link per [viewer configuration](guides/docsify.md#viewer-configuration),
  adapting its label to the instance language; do not update the viewer automatically.

## 1.6.0 - review

### Review

- D2 edge-label placement follows the relationship's meaning; review endpoint
  association and rendered legibility.
- Diagram correspondence, matching titles, and stable identity remain required,
  including distinct identities for repeated step occurrences. Clickable nodes
  and return links are optional, superseding 1.5.1's generic navigation obligation.
- Docsify diagram navigation is an optional, consumer-owned integration.
- First-occurrence acronym expansion is an optional local editorial criterion,
  not a universal requirement.

### Action

- For existing process diagrams, review [edge-label placement](guides/d2.md#edge-label-placement)
  against canonical meaning and inspect SVG legibility and overlaps. Check
  [step correspondence](guides/d2.md#step-correspondence-and-navigation), including
  unambiguous associations for repeated occurrences sharing a description.
- Do not flag missing interactivity as nonconformity. If the wiki uses Docsify,
  check compatibility and propose adoption or review the existing integration
  using [the optional guide](guides/docsify.md); do not activate or update it automatically.
- Apply acronym expansion only where locally approved, following
  [local acronym presentation](guides/authoring-context.md#local-acronym-presentation).
  Do not impose it on other outputs or use it to alter canonical titles or labels.

## 1.5.1 - review

### Review

Process diagrams: correspondence between action, decision, and subprocess nodes
and their canonical description sections; matching node labels and section
headings; stable identifiers; and links in both directions. Responsibility
containers and auxiliary markers need sections only when they have their own
canonical descriptions.

### Action

During the installed-version review, load
[step correspondence and navigation](guides/d2.md#step-correspondence-and-navigation).
Inventory affected diagrams and sections, differing titles, missing or ambiguous
associations, and absent or broken links. Check the consumer viewer's support for
stable targets and interactive SVG, and test navigation in the rendered entry;
ordinary Markdown images do not activate internal SVG links. Report unsupported
or untested behavior and arrange explicit integration follow-ups when needed.

Propose corrections under the consumer's governance, consolidating canonical
Markdown before D2 and regenerating SVG without manual edits. Do not equate
matching titles with matching meaning or silently rename steps to conceal a
divergence. Version installation and review do not authorize content or viewer
changes; obtain confirmed scope and grill closure before applying corrections.
Keep unresolved findings and follow-ups explicit; review completion does not
declare existing diagrams conformant or their navigation functional.

## 1.5.0 - review

### Review

Optional intent maps: canonical destinations, exact H1 labels, and guidance
supported by the linked pages.

### Action

If `navigation.intent_map` is declared, review the map and affected routes using
[Modeling](guides/modeling.md#intent-map) and
[contract requirements](contracts/README.md); do not adopt it automatically.

## 1.4.1 - baseline

Coverage starts at 1.4.1; its license correction did not affect wiki texts.
