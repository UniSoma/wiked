# Methodology-impact changelog

Impacts on existing wiki texts; follow [version review](guides/maintenance.md#installed-version-review).

## 1.8.0 - review

### Review

- Page types may declare `external_authority`: pages whose authority lies outside
  the wiki open with a configured notice quotation and, as configured, an official link.
- `rules.external_links` may enable an offline check of external link and image
  destinations for allowed schemes and syntax.
- Changelog review entries now state their rationale and mark each action's nature.

### Rationale

- External authority: readers opening a page derived from an external official
  document could not tell, before reading, that it is not the official document,
  or reach that document; the distinction needed to be configurable and verifiable.
- External links: verifiable problems such as malformed addresses or unexpected
  schemes went unreported, because external links were only informational.
- Rationale and markers: reviewers had to decide on impacts without knowing why a
  change was made or whether adopting it was required, optional, or merely informative.

### Action

- Optional adoption: If some pages derive from an external authority, propose
  declaring it per [external authority](guides/modeling.md#external-authority);
  do not change the contract or pages automatically.
- Optional adoption: Propose enabling the offline check per
  [external links](guides/modeling.md#external-links); do not enable it automatically.
- Informational: Existing wiki texts need no change for the enriched changelog;
  earlier entries were rewritten with rationale and markers without changing their meaning.

## 1.7.0 - review

### Review

- Contextual source-page citations in page bodies are an optional local editorial
  criterion, not a universal requirement; configured source references remain mandatory.
- The optional Docsify integration example now exposes a native link to each
  enhanced diagram's original SVG.

### Rationale

- Citations: heavy body citations left their scope unclear, pulled reading from the
  current process into indexing history, and accumulated without a removal step when
  superseded; they also contradicted the query guide's sources-at-the-end presentation.
- Original SVG: after adopting navigable diagrams, users lost the browser's usual way
  to open the image on its own, needed to inspect and zoom large flows.

### Action

- Informational: Do not flag existing body citations as nonconformity or remove them
  automatically.
- Optional adoption: Maintenance may propose removing body citations or adopting a
  criterion in the local authoring reference, following
  [local contextual citations](guides/authoring-context.md#local-contextual-citations).
- Required: Review time-sensitive claims that relied on a body citation for currency
  and state their effective date or period in the text.
- Optional adoption: If the wiki already uses the Docsify integration, propose adopting
  the original-diagram link per [viewer configuration](guides/docsify.md#viewer-configuration),
  adapting its label to the instance language; do not update the viewer automatically.
  Adoption consequences: [authority and adoption](guides/docsify.md#authority-and-adoption).

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

### Rationale

- Edge labels: placement chosen by predicted edge length drifted labels away from
  the endpoint they describe; why the distance rule was dropped is not recorded beyond that.
- Navigation: ordinary Markdown images do not activate internal SVG links, so clickable
  navigation depends on the viewer; why the obligation became optional is not otherwise recorded.
- Acronyms: a local convention expanded some acronyms without defining the reading
  unit or the acronyms covered, trading repetition against standalone reading.

### Action

- Required: For existing process diagrams, review
  [edge-label placement](guides/d2.md#edge-label-placement) against canonical meaning
  and inspect SVG legibility and overlaps. Check
  [step correspondence](guides/d2.md#step-correspondence-and-navigation), including
  unambiguous associations for repeated occurrences sharing a description.
- Informational: Do not flag missing interactivity as nonconformity.
- Optional adoption: If the wiki uses Docsify, check compatibility and propose adoption
  or review the existing integration using [the optional guide](guides/docsify.md#authority-and-adoption);
  do not activate or update it automatically.
- Optional adoption: Apply acronym expansion only where locally approved, following
  [local acronym presentation](guides/authoring-context.md#local-acronym-presentation).
  Do not impose it on other outputs or use it to alter canonical titles or labels.

## 1.5.1 - review

### Review

Process diagrams: correspondence between action, decision, and subprocess nodes
and their canonical description sections; matching node labels and section
headings; stable identifiers; and links in both directions. Responsibility
containers and auxiliary markers need sections only when they have their own
canonical descriptions.

### Rationale

- The motivation is not recorded beyond the approved scope: linking each diagram
  step to its canonical description with matching titles and stable identity.

### Action

- Required: During the installed-version review, load
  [step correspondence and navigation](guides/d2.md#step-correspondence-and-navigation).
  Inventory affected diagrams and sections, differing titles, missing or ambiguous
  associations, and absent or broken links. Check the consumer viewer's support for
  stable targets and interactive SVG, and test navigation in the rendered entry;
  ordinary Markdown images do not activate internal SVG links. Report unsupported
  or untested behavior and arrange explicit integration follow-ups when needed.
- Required: Propose corrections under the consumer's governance, consolidating canonical
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

### Rationale

- Index navigation serves readers who know the taxonomy; task-shaped questions needed
  domain knowledge to pick destinations, and index shortcuts would repeat links or
  cross trunks. Intent-to-destination associations needed instance-level human curation.

### Action

- Required: If `navigation.intent_map` is declared, review the map and affected routes
  using [Modeling](guides/modeling.md#intent-map) and
  [contract requirements](contracts/README.md).
- Optional adoption: Otherwise, adoption follows [the intent map](guides/modeling.md#intent-map);
  do not adopt it automatically.

## 1.4.1 - baseline

Coverage starts at 1.4.1; its license correction did not affect wiki texts.
