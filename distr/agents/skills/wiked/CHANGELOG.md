# Methodology-impact changelog

Impacts on existing wiki texts; follow [version review](guides/maintenance.md#installed-version-review).

## 1.6.0 - none

No additional review of existing wiki texts is required by this release.

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
