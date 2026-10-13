# Wiki Modeling

Load this guide when creating pages, reviewing structure, or running a consistency check.

For page creation or revision and maintenance, complete [Contextual Preparation](authoring-context.md) before content analysis or authorship proposals. Initialization and migration instead apply the bounded exceptions in `setup.md`.

## Contract First

Treat `wiki/wiki-structure.yaml` as the sole machine-readable authority for deterministic instance structure. Do not duplicate its concrete values here. Read:

- wiki root, reserved files, and special directories;
- naming and navigation topology;
- frontmatter, page types, roles, states, and sections;
- optional structured record collections, field types, cardinalities, sentinels, and canonical page references;
- provenance, assets, and diagram-set policy;
- assets and diagram relationships;
- Knot mappings and diagnostic severities;
- instance language and version requirements.

Markdown bodies remain canonical. Configuration validates form, not operational truth.

## Structured Sections

For a page type with `structured_sections`, use its named section exclusively for immediate record subheadings. Put each field in a direct `- **Field:** value` item, or use `- **Field:**` with a nested list for multiple values. Follow configured cardinality and explicit empty values exactly. Every `page` value uses a relative canonical link; `text` is for values not modeled as pages. Keep deterministic field rules out of the local authoring reference.

## Pages and Navigation

- Start navigation at the root index and preserve progressive top-level indexes.
- Create a top-level branch only for a recurring, human-confirmed need.
- Keep wiki links relative. External links and bare URLs are informational outside typed canonical-reference fields and intent-map destination entries; they cannot substitute for those required canonical links.
- Use minimal frontmatter as declared by the page type.
- Keep canonical terms in the configured context (glossary): definitions, essential distinctions, synonyms, terms to avoid, and relevant links. Include only responsibilities needed to define a role, not its operating procedure.
- Indexes select destinations through useful groupings and brief descriptions; preserve the root's configured title, purpose, audience, and scope. Develop operational details in canonical pages, not navigation summaries. Evidence eligibility still follows configured roles.
- Prefer alphabetical glossary terms and index entries within useful groupings, unless a human-approved semantic sequence takes precedence. Preserve required links and topology.
- Before reducing operational detail in context or indexes, inspect the canonical destination for coverage, including conditions, exceptions, state, and provenance; a link alone proves nothing. Preserve uncovered information and resolve gaps or divergences with the human before removal. Page creation or revision requires confirmed scope, not incidental cleanup.
- Preserve current operation separately from proposals and pending questions.

## Intent Map

`navigation.intent_map` optionally names one Markdown file at the wiki root, such as `routes.md`; its path, intents, and associations belong to the instance. Link it exactly once from the root index in a useful human-readable grouping, such as the instance's transversal references when present. Do not impose a universal section title. Preserve every existing index destination and uniqueness rule: only the map permits destinations shared between intents or crossing trunks.

Use one H1 title, optional introductory paragraphs describing coverage limitations, and H2 headings expressing intents. Each intent has one or more direct bullet entries in the common form below. Write the title, intents, link labels, and guidance in the configured instance language; this English example is illustrative, not required instance content.

```markdown
# Intent routes

Selected consultation points, not exhaustive coverage.

## Understand a recurring practice

- [Operations](handbook/operations.md) - Consult the canonical description of this practice.
```

Each entry contains one relative canonical Markdown link followed by ` - ` and nonempty guidance for that destination. The label exactly matches its H1; an existing fragment may narrow consultation. Use operational pages or canonical indexes, not source pages, ingestion, governance, configuration, instructions, context, or the authoring reference. Destinations may repeat between intents, but not within one intent, even through different fragments. Do not use frontmatter, nested lists, or subordinate headings in the map; it cannot acquire an operational page role.

Keep the map small and human-curated for recurring, important, or difficult-to-locate needs. Guidance explains where to consult, not an operational sequence, responsibilities, or new rules. Do not reproduce procedures, promise completeness, or compensate for coverage limitations with invented knowledge. Humans validate meaning, usefulness, and support in the canonical destinations; automation checks only form and references. Do not reuse the local authoring reference as a domain map.

Load the map when proposing routes or checking associations directly affected by in-scope page changes. Creating or revising routes follows `assisted-indexing.md`, with editorial authority and explicit human curation. A new page or question does not automatically justify a new route.

## Provenance and Visuals

- Every page that the contract assigns an operational-content role must carry its configured source references.
- Use contextual citations where interpretation, currency, or divergence depends on one source page.
- Promote content to a page when independent consultation, recurring use, or a canonical place for curated relevant relationships justifies it. This does not imply a complete backlink or mention inventory. Only the contract may require a page split.
- A process diagram complements its canonical Markdown. Load `d2.md` for any diagram work.
- A configured diagram set shares one stem across required extensions and embeds exactly one configured visualization, never the maintenance source.
- Every visual fact needed to understand the operation must also appear in Markdown.

## Human Boundary

The validator checks only declared deterministic invariants. Humans decide semantics, responsibilities, sequence, conditions, names, scope, source reliability, and divergence. Read-only review needs no grill; governed-content correction requires `grill.md` to close first.
