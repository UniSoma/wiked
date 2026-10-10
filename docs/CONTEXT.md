# Wiked methodology evolution context

Canonical vocabulary for maintaining and evolving Wiked at its source repository. This context governs source development; it is not part of the installed runtime and is not evidence about any consumer's operation.

## Repository roles

**Source repository**: the repository in which Wiked's distribution, schema, runtime, tests, and release material are authored and verified.

**Consumer repository**: a repository that installs Wiked and contains a configured operational wiki. A source repository may temporarily also be a consumer, but the two authorities remain separate.

**Reference instance**: an external consumer explicitly selected to exercise Wiked integration without placing its domain knowledge in the generic distribution. It is optional and never required by the default source suite.

**Methodology evolution**: an authorized change to Wiked's generic behavior, interfaces, distribution, schema, runtime, development guidance, or tests. It is distinct from operating or editing a consumer wiki.

## Distribution and interfaces

**Wiked distribution**: the versioned, copyable files owned by Wiked and listed exactly in `.agents/wiked-manifest.yaml`.

**Distribution manifest**: the namespaced inventory that declares the distribution version, entrypoint, owned components, and preservation policy for unlisted files.

**Installed skill**: the Wiked distribution available to an agent in a consumer repository. Consumer workflows may use it but must not modify it.

**Instance contract**: the consumer-owned `wiki/wiki-structure.yaml` that declares language, compatible versions, topology, vocabulary labels, page types, states, and integration mappings. It configures runtime behavior but is not operational evidence.

**Metacontract**: Wiked's versioned JSON Schema for validating the shape of an Instance contract before relational rules run.

**Distributed runtime**: the generic validator shipped with Wiked and invoked with an explicit consumer repository root.

**Harness adapter**: a thin integration entrypoint, such as `wiked-setup`, that delegates to the installed skill without copying workflow rules.

## Compatibility and transition

**Contract version**: the version of the Instance contract format accepted by the Metacontract and Distributed runtime.

**Methodology version**: the Wiked behavior version required by a consumer instance.

**Runtime cutover**: the explicit replacement of a repository's previous validator and contract authority with the Distributed runtime and Instance contract. Coexistence before cutover is temporary and must not produce wrappers or duplicated rules.

**Portable integration**: verification that the distribution works from an explicit Consumer repository root independently of the distribution's source location and without depending on source-only `docs/`.

**Targeted textual check**: a non-Python verification used for instruction-only changes, covering links, ownership boundaries, language, prohibited dependencies, and required routing statements.

## Governance

**Methodological grill**: the decision interview that establishes scope, authority, exceptions, and acceptance before governed source content changes.

**Operational grill**: the consumer-side decision interview required by Wiked before governed wiki content changes. Its authority and records come from the installed skill and Instance contract, not source-development documents.

**Operational evidence**: configured Markdown in a consumer wiki that can support answers about that consumer's domain. Source code, configuration, tests, instructions, tickets, ingestion material, and rendered assets are not Operational evidence.

**Ingestion workspace**: the consumer-owned `raw/` area for local source material selected explicitly by indexing tickets. Successfully indexed local material moves to `raw/archive/YYYY-MM-DD_<ticket-id>/`; it remains outside Operational evidence, and humans decide whether to persist it in Git.
