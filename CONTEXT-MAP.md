# Context map

## Source authority

- [Agent entrypoint](./AGENTS.md): source identity, governance, and invariants.
- [Source vocabulary](./docs/CONTEXT.md): canonical methodology-development terms.
- [Development workflow](./docs/metodologia.md): authoring, validation, and publication boundaries.
- [Distribution manifest](./distr/agents/wiked-manifest.yaml): exact versioned ownership.
- [Publication contract](./docs/distribution.md): approved release and installer requirements, pending execution.

## Product under development

[The distributed skill](./distr/agents/skills/wiked/SKILL.md) routes workflows in an
external consumer. It is maintained here as source; it must work without `docs/`.
Its source location is outside automatic skill discovery; consumers install it
under `.agents/skills/wiked/`.
Consumer configuration and operational evidence belong to that consumer and are
not prerequisites for the generic source suite.

## Historical research

[Research provenance](./reports/README.md) identifies the preserved report and
its limits. Research and tickets are not methodology approval or operational evidence.
