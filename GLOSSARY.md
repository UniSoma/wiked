# Wiked methodology evolution

Canonical vocabulary for maintaining and evolving Wiked in its source repository. It is not part of the installed runtime and is not evidence about any consumer's operation.

## Language

### Repository roles

**Source repository**:
The repository in which Wiked's distribution, schema, runtime, tests, and release material are authored and verified.
_Avoid_: author tree, author repository

**Consumer repository**:
A repository that installs Wiked and contains a configured operational wiki.

**Reference instance**:
An external Consumer repository explicitly selected to exercise Wiked integration without placing its domain knowledge in the generic distribution.

**Methodology evolution**:
An authorized change to Wiked's generic behavior, interfaces, distribution, schema, runtime, development guidance, or tests, as distinct from operating or editing a consumer wiki.

### Purpose and use cases

**Use case**:
A recurring purpose for which a consumer configures and operates a Wiked wiki.

**Knowledge base**:
The use case in which a wiki records how an area, project, or product operates, including its decisions and open questions.
_Avoid_: team wiki, documentation

**Consulting mapping**:
The use case in which a wiki maps a client organisation's processes, business rules, data sources, tools, stakeholders, and gaps, in its current and proposed states.
_Avoid_: process mapping, as-is mapping

**Agent-navigable business context**:
The use case in which agents navigate a governed wiki to obtain business meaning linked to the data it concerns.
_Avoid_: RAG, semantic layer

**Derived artifact production**:
The use case in which documents, diagrams, or exports are generated from validated wiki content.
_Avoid_: export

**Derived view**:
A read-only, regenerable projection of a consumer wiki, such as a navigation map or a curation panel; it is never Operational evidence.

**Derived artifact**:
A document or diagram generated from validated wiki content; it is never Operational evidence.

**Source page**:
A consumer wiki page that records the provenance of one primary source and lists the pages it grounds.
_Avoid_: source (alone)

### Distribution and interfaces

**Wiked distribution**:
The versioned, copyable files owned by Wiked and listed exactly in the Distribution manifest.

**Distribution manifest**:
The namespaced inventory that declares the distribution version, entrypoint, owned components, and preservation policy for unlisted files.

**Installed skill**:
The Wiked distribution as made available to an agent in a Consumer repository.

**Instance contract**:
The consumer-owned declaration of a wiki's language, compatible versions, topology, vocabulary labels, page types, states, and integration mappings.
_Avoid_: consumer contract, local contract

**Metacontract**:
Wiked's versioned schema for the shape of an Instance contract.

**Distributed validator**:
The generic wiki validator shipped with the Wiked distribution.
_Avoid_: distributed runtime, portable validator

**Review acknowledgment interface**:
The installed metadata-only command that records completion of an installed-version review.

**Harness adapter**:
A thin integration entrypoint, such as `wiked-setup`, that delegates to the Installed skill.

### Compatibility and transition

**Contract version**:
The version of the Instance contract format accepted by the Metacontract and Distributed validator.

**Methodology version**:
The Wiked behavior version required by a consumer instance.

**Runtime cutover**:
The explicit replacement of a repository's previous validator and contract authority with the Distributed validator and Instance contract.

**Portable integration**:
Verification that the distribution works from an explicit Consumer repository root, independently of its source location and of source-only documentation.

**Targeted textual check**:
A non-Python verification of instruction-only changes covering links, ownership boundaries, language, prohibited dependencies, and routing coherence.

**Behavioral evaluation**:
A scenario-based assessment of an agent operating with the installed distribution and a synthetic Instance contract, judged on responses, observable actions, and final state.

### Governance

**Methodological grill**:
The decision interview that establishes scope, authority, exceptions, and acceptance before governed source content changes.
_Avoid_: methodology grill

**Operational grill**:
The consumer-side decision interview required by Wiked before governed wiki content changes.

**Operational evidence**:
Configured Markdown in a consumer wiki that can support answers about that consumer's domain; source code, configuration, tests, instructions, tickets, ingestion material, and rendered assets are not Operational evidence.

**Ingestion workspace**:
The consumer-owned `raw/` area holding local source material selected for indexing.
