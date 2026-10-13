# Wiki Modeling

Load this guide when creating pages, reviewing structure, or running a consistency check.

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

When `navigation.authoring_file` is declared, read it before creating or revising content. Its instance-local review criteria, guidance, and examples may reference the contract or canonical terms but cannot redefine deterministic structure or domain meaning.

Markdown bodies remain canonical. Configuration validates form, not operational truth.

## Structured Sections

For a page type with `structured_sections`, use its named section exclusively for immediate record subheadings. Put each field in a direct `- **Field:** value` item, or use `- **Field:**` with a nested list for multiple values. Follow configured cardinality and explicit empty values exactly. Every `page` value uses a relative canonical link; `text` is for values not modeled as pages. Keep deterministic field rules out of the local authoring reference.

## Pages and Navigation

- Start navigation at the root index and preserve progressive top-level indexes.
- Create a top-level branch only for a recurring, human-confirmed need.
- Keep wiki links relative. External links and bare URLs are informational; they do not affect structural validation.
- Use minimal frontmatter as declared by the page type.
- Keep canonical terms in the configured context (glossary): definitions, essential distinctions, synonyms, terms to avoid, and relevant links. Include only responsibilities needed to define a role, not its operating procedure.
- Indexes select destinations through useful groupings and brief descriptions; preserve the root's configured title, purpose, audience, and scope. Develop operational details in canonical pages, not navigation summaries. Evidence eligibility still follows configured roles.
- Prefer alphabetical glossary terms and index entries within useful groupings, unless a human-approved semantic sequence takes precedence. Preserve required links and topology.
- Before reducing operational detail in context or indexes, inspect the canonical destination for coverage, including conditions, exceptions, state, and provenance; a link alone proves nothing. Preserve uncovered information and resolve gaps or divergences with the human before removal. Page creation or revision requires confirmed scope, not incidental cleanup.
- Preserve current operation separately from proposals and pending questions.

## Provenance and Visuals

- Every page that the contract assigns an operational-content role must carry its configured source references.
- Use contextual citations where interpretation, currency, or divergence depends on one source page.
- Promote content to a page when independent consultation, recurring use, or a canonical place for curated relevant relationships justifies it. This does not imply a complete backlink or mention inventory. Only the contract may require a page split.
- A process diagram complements its canonical Markdown. Load `d2.md` for any diagram work.
- A configured diagram set shares one stem across required extensions and embeds exactly one configured visualization, never the maintenance source.
- Every visual fact needed to understand the operation must also appear in Markdown.

## Human Boundary

The validator checks only declared deterministic invariants. Humans decide semantics, responsibilities, sequence, conditions, names, scope, source reliability, and divergence. Read-only review needs no grill; governed-content correction requires `grill.md` to close first.
