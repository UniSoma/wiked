# Wiked value proposition

> **About this document.** This is a positioning document for business readers. It is not normative: Wiked's rules live in the [methodology](./metodologia.md) and in the Wiked distribution. Each capability is tagged with its maturity:
>
> - **Available today**: shipped in the current Wiked distribution.
> - **Evolving**: demonstrated in a reference instance, not yet part of the distribution.
> - **Vision**: a direction we intend to explore, with no commitment.
>
> Wiked is an open method maintained by UniSoma.

## In one sentence

**Wiked turns what an organisation knows about how it works into a governed, traceable knowledge base that people and AI agents can both rely on.**

Five messages summarise what that means:

1. **People decide meaning; agents record it.** An AI agent does the writing and linking. A qualified person confirms what is true, through a structured decision interview, before anything is recorded.
2. **Every claim has a source.** Statements point to the interview, document, or decision they came from.
3. **What is not known is explicit.** Open questions and proposed changes are first-class items linked to tickets, not remarks buried in prose.
4. **Structure is checked, not hoped for.** Each wiki declares its expected shape, and a deterministic validator checks every change against that declaration.
5. **Rigor is configurable.** The same method serves a light team knowledge base and a strict consulting map. Curation effort grows with the rigor you choose.

## The problem

Most of what an organisation knows about how it works is not written down in one place. It lives in people's heads, slide decks, spreadsheets, chat threads, and documents nobody is sure are current. When someone asks "who approves this?" or "where does this number come from?", the answer depends on whom you ask.

AI assistants make this worse as well as better. They answer fluently from whatever context they receive, true or not. When the material is inconsistent, the assistant resolves the conflict silently, at question time, with no one accountable for the choice.

Consulting work that maps an organisation has a related problem. The process maps, data inventories, and gap lists are often outdated by the time they are delivered. Clients struggle to tell which statements came from an interview, which were inferred, and which are still open.

## What Wiked is

Wiked is an open method plus a portable distribution: agent instructions, a schema, and a validator. You install it in your own Git repository. Knowledge is kept as plain Markdown pages organised for progressive navigation, so people and AI agents can find what they need without loading everything. There is no proprietary platform and no lock-in: the content stays readable without Wiked.

Wiked belongs to two established families of practice:

- **LLM-maintained wikis.** An agent keeps a wiki up to date from the material it is given. Wiked is the governed version of this pattern: the agent proposes, a person decides.
- **Docs-as-code.** Knowledge is versioned, reviewed, and validated like source code.

## The core: five pillars

| Pillar | What it means | Maturity |
|---|---|---|
| Governed knowledge | Meaning, responsibility, terminology, and scope are confirmed by a qualified person in a structured decision interview before the agent writes. | Available today |
| Traceability | Each operational page lists its sources. Each source has its own page recording its origin and dates, and links back to the pages it supports. Raw material is archived with the change that used it. | Available today |
| Explicit uncertainty | Open questions and proposed changes are listed on the page they affect and linked to tickets. The validator flags items whose ticket is closed or missing. | Available today |
| Structural consistency | Each wiki declares its page types, required sections, states, and link rules in an Instance contract. A deterministic validator checks the wiki against it. | Available today |
| Open, progressive, agent-navigable format | Markdown in Git, with indexes per area, stable anchors, and an optional map from common questions to the pages that answer them. | Available today |

Around this core sit two kinds of output. Neither ever becomes evidence in its own right:

- **Derived views:** read-only projections of the wiki, regenerated from it. Examples are a navigation map of the whole base and a curation panel showing where open items concentrate. *(Evolving)*
- **Derived artifacts:** documents and diagrams generated from validated content. *(Available today; see Use case 4.)*

## Configurable rigor

The Instance contract decides how strict a wiki is. It can require little more than titles and sources, or it can require specific sections, record structures, cardinalities (for example, exactly one accountable person per activity), and explicit empty values instead of silent omissions.

- A **light setting** suits a team knowledge base: few required sections, fast curation, and a low barrier to adding knowledge.
- A **strict setting** suits a consulting map: every activity names exactly one accountable person, every business rule names its authority, every data source has an owner, and every gap has an owner, an impact, and a cause.

The trade-off is deliberate and stated plainly. More rules mean more questions in each interview and more effort per page. In exchange, the validator can guarantee more. Each organisation chooses its point on that scale and can raise it later for the areas that need it.

## Use cases

Wiked serves two main use cases, a **Knowledge base** and **Consulting mapping**. Two more follow naturally from them: **Agent-navigable business context** and **Derived artifact production**.

### Use case 1: Knowledge base for an area, project, or product

Wiked was created for this use case. Its reference instance is the operational knowledge base of a department.

**What it covers**

- How the area works: processes and their steps, roles and responsibilities, policies, tools, and the terms people use.
- Decisions, with the reasoning and the source behind them.
- Open questions, each with a ticket and therefore an owner and a status.
- Proposed changes, kept apart from the description of current operation.

**Day-to-day value**

- **Onboarding.** New people read how work actually happens, with links to the sources, instead of piecing it together from conversations.
- **One place to look.** Indexes per area and an optional map from common questions to pages lead readers, and agents, to the right page quickly.
- **Answers with sources.** When a person or an agent asks "who is responsible for this step, and why?", the answer cites the pages that support it. When the wiki lacks the evidence, the agent says so instead of inventing an answer.
- **An honest "we do not know yet".** Open questions are visible on the page they affect, so readers know which parts are settled.

**How it is maintained** *(Available today)*

- **Indexing.** New documents and interview notes become source pages with provenance. Their content is then incorporated into the operational pages, after a person confirms its meaning.
- **Curation.** Curators work through open questions and proposed changes as tickets. Closing one updates the pages it affects.
- **Review after updates.** When Wiked itself is updated, a guided review checks what the change means for the wiki.
- **External documents.** A page can mirror an external document, such as an official policy. It then states that it is not the official version and links to the authority.

**Derived views** *(Evolving)*: in the reference instance, a navigation map lets readers explore the base. A curation panel shows where open items concentrate, including a visual map per area so curators can choose where to focus.

[See how it works: an illustrative knowledge-base example](./examples/knowledge-base.md)

### Use case 2: Consulting mapping

Consulting mapping documents how a client organisation operates so that it can be understood, improved, or supported by data and AI. Wiked gives this work a governed, auditable, and living form. The map does not go stale on hand-off, and every statement can be traced to the interview or document behind it.

**What gets mapped**

- **Processes.** Each process has a SIPOC summary (suppliers, inputs, outputs, customers) and activities with RACI responsibilities: exactly one accountable person and at least one responsible person, with "nobody" stated explicitly where it applies.
- **Business rules,** recorded separately from the process flow, each with its statement, its authority, where it applies, and the data it uses.
- **Data sources:** the systems, files, and feeds the business uses, each with an owner, a steward (or an explicit "not assigned"), a refresh pattern, and what uses it.
- **Analytical tools:** dashboards, models, and reports, with their purpose, users, and data sources.
- **Stakeholders and roles.**
- **Gaps** in data, process, or tooling, each with a kind, what it affects, what it impacts, its cause, and an owner.

A note on vocabulary: a **data source** is something being mapped, part of the client's domain. A **source page** is Wiked's record of where a statement came from, such as an interview or a document. The two are kept distinct.

**Current state and proposed changes**

- *(Available today)* Current operation and proposed changes are recorded separately and governed the same way. A proposed change is a ticket listed on the page it affects, and the proposed version of a process can have its own page.
- *(Evolving)* Side-by-side comparison of the current and proposed versions of a process, and a typed link between them.

**Completeness**

- *(Available today)* Required sections and record structures, cardinalities such as "exactly one accountable person", explicit empty values, and open questions recorded as tickets. Together these make missing information visible rather than silent.
- *(Evolving)* Checks that links are reciprocal and complete, for example that a rule listing the processes it applies to is also cited by those processes. Checks that a link points to the right kind of page.

**How the client follows the work**

- *(Available today)* After each validated increment, the wiki can be published as a read-only website for the client.
- *(Evolving)* Clients request corrections or new material through the collaboration platform they already use (for example, a project management tool). Each request is linked to a ticket, and the consulting team's agent synchronises requests at the curator's request. The client never needs to touch Git. Per-item control of what the client sees is under study.

**Boundaries**

- Wiked complements data catalogues: it records business meaning and links it to catalogue entries; it does not replace their connectors, lineage, or quality monitoring.
- Wiked complements process modelling tools. It is a governed source from which BPMN or DMN models can be produced; it does not generate them.

**What a strict configuration looks like**: in a reference configuration built for this use case, the validator stops a process activity that names two accountable people. It requires an explicit "none" instead of an omitted field, and warns when an open question points to a ticket that has already been closed.

[See how it works: an illustrative consulting-mapping example](./examples/consulting-mapping.md)

### Use case 3: Business context for analytical AI

This use case follows from the first two. Once processes, rules, roles, data sources, and gaps are recorded and linked, AI agents can navigate that context to answer business questions and to build better analytical queries.

**Why curated context beats raw retrieval.** A retrieval tool over raw documents, such as a notebook that answers from uploaded files, gives no guarantee that its sources agree. Conflicting or ambiguous material reaches the agent, which must interpret it at question time. Wiked resolves conflicts once, with an accountable person, before any agent reads the content.

**Why it goes beyond catalogue-bound agents.** Agents built into data platforms, such as Databricks Genie, take business context mainly from catalogue metadata and from instructions attached to specific tables and columns. Wiked carries the wider context those agents lack: processes, rules, responsibilities, known gaps, and decisions. It links this context to the data sources it concerns, so an agent can understand what a figure means before querying it.

**What the evidence says.** Public research supports the premise: the BIRD text-to-SQL benchmark (NeurIPS 2023) showed that supplying business knowledge improves query accuracy. No study has yet tested a governed wiki like Wiked, and we have not run our own benchmark. We therefore position Wiked as a governed complement to semantic layers and data catalogues, and make no claims about accuracy figures.

*Maturity:* agents navigate a Wiked base today *(Available today)*; linking wiki pages to specific catalogue entries is done by convention, with no dedicated validation *(Evolving)*.

### Use case 4: Derived artifacts

Because the knowledge base is validated and structured, it can produce other material: reports, onboarding packs, process diagrams, and exports.

- *(Available today)* Diagrams generated alongside process pages; export of pages to PDF and DOCX; read-only website publication.
- *(Vision)* Export templates tailored to each use case, for example a consulting deliverable or an onboarding pack.

## How a project runs with Wiked

1. **Setup.** A decision interview declares the wiki's purpose, audience, scope, language, page types, and rigor. The result is the Instance contract.
2. **Indexing.** Documents and interview notes are registered as source pages with provenance. Their content is incorporated into operational pages after a person confirms its meaning.
3. **Curation loop.** Open questions and proposed changes are tracked as tickets. Curators decide them, and the affected pages are updated.
4. **Validation on every increment.** The validator checks structure, links, provenance, and the status of open items. The validated increment can then be published for readers.
5. **Maintenance.** After Wiked updates, a guided review checks their effect. Readers' requests are incorporated through the same governed route.

The flow throughout is the same: sources → decision interview → wiki → validator → readers, views, and agents.

## How Wiked compares

No existing category covers what Wiked does. Each is better than Wiked at something, and Wiked is designed to complement rather than replace them.

| Category | Better than Wiked at | What Wiked adds |
|---|---|---|
| AI-assisted wikis (e.g. Confluence, Notion) | User experience, hosting, permissions | Per-statement provenance, explicit uncertainty, validated structure |
| Data catalogues (e.g. DataHub, Atlan, Collibra) | Connectors, lineage, quality monitoring | Business meaning decided by people; links between processes, rules, and data |
| Enterprise search and retrieval notebooks (e.g. NotebookLM) | Scale, freshness, no curation needed | Conflicts resolved before retrieval; curated, auditable meaning |
| Agents on data platforms (e.g. Databricks Genie) | Direct querying of governed data | Business context beyond tables and columns, linked to the data |
| Process modelling and process mining tools | Executable models, evidence from event logs | A governed narrative source, with rules and gaps that have owners |
| Fully automated LLM wikis | Speed, zero human effort | Governance: people decide what is true |

## Maturity at a glance

| Available today | Evolving | Vision |
|---|---|---|
| Governed decision interviews before every change | Navigation map and curation panel (reference instance) | Export templates per use case |
| Provenance per page and per source | Side-by-side comparison of current and proposed processes | |
| Open questions and proposed changes linked to tickets | Reciprocal-link, coverage, and link-target checks | |
| Instance contract and deterministic validator | Client requests synchronised from external platforms, with per-item visibility | |
| Configurable record structures and cardinalities | Validated links to data catalogue entries | |
| Mirrors of external documents with an authority notice | | |
| Process diagrams, PDF and DOCX export, read-only website | | |

## Limitations

- **No hosted interface or connectors.** Wiked runs in a Git repository with an AI agent environment. It does not connect directly to data platforms or collaboration tools.
- **Human pace by design.** Interviews and confirmations are the bottleneck, deliberately. Wiked trades speed for knowledge someone can stand behind.
- **Form, not truth.** The validator guarantees the structure of the knowledge: required sections, links, provenance, and the status of open items. It cannot check that a statement is true. People do that.
- **No proprietary AI benchmark.** We cite public research and make no claims about accuracy figures.

## About

Wiked is an open method maintained by UniSoma. Its source, documentation, and releases are public under the MIT License.

If your organisation is considering a governed knowledge base or a consulting mapping effort and would like to explore whether Wiked fits, we would be glad to talk.
