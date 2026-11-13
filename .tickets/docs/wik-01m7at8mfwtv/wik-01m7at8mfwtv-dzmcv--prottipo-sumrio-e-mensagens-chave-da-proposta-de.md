---
id: wik-01m7at8mfwtv-dzmcv
ticket: wik-01m7at8mfwtv
title: 'Protótipo: sumário e mensagens-chave da proposta de valor'
type: other
created: '2026-11-13T21:04:47.866487507Z'
updated: '2026-11-13T21:04:47.866487507Z'
---

# PROTOTYPE (throwaway): outline and key messages for docs/proposta_de_valor_wiked.md

> Rough outline to react to. Not the final text. English, anonymous, maintained by UniSoma.
> Maturity tags: [today] available in the distribution · [evolving] demonstrated in a reference instance · [vision] direction.

## 0. One-line pitch

**Wiked turns what an organisation knows about how it works into a governed, traceable knowledge base that people and AI agents can both rely on.**

Key messages (the five that must survive any cut):

1. **Meaning is decided by people, recorded by agents.** An LLM does the writing and linking; a qualified person confirms what is true (grill).
2. **Every claim has a source.** Statements point to the interview, document or decision they came from.
3. **What is not known is explicit.** Open questions and proposed changes are first-class items linked to tickets, not buried in prose.
4. **Structure is checked, not hoped for.** A declared Instance contract plus a deterministic validator guarantee the shape of the knowledge.
5. **Rigor is configurable.** The same method serves a light team wiki or a strict consulting map; curation effort grows with the rigor you turn on.

## 1. The problem

- Business knowledge lives in heads, slides, spreadsheets and chat threads; it drifts from reality and nobody can tell which version is right.
- AI assistants amplify the problem: they answer fluently from whatever context they get, true or not.
- Consulting mapping projects deliver documents that are outdated on hand-off and cannot be audited.

## 2. What Wiked is

- An open method plus a portable distribution (instructions, schema, validator) installed in the client's own repository.
- Plain Markdown, progressive navigation, readable by people and by agents. No proprietary platform, no lock-in.
- Positioning: the governed version of the "LLM-maintained wiki" pattern, built on docs-as-code practice.

## 3. The core (five pillars)

| Pillar | What it means | Maturity |
|---|---|---|
| Governed knowledge | Human-confirmed meaning via structured interviews (grill) before any write | [today] |
| Traceability | Provenance per statement; source pages; archived raw material | [today] |
| Explicit uncertainty | Open questions and proposals as items linked to tickets, validated | [today] |
| Structural consistency | Instance contract + Distributed validator (types, sections, cardinalities, links) | [today] |
| Open, progressive, agent-navigable format | Markdown in Git, indexes, stable anchors, intent map | [today] |

Around the core: derived views (Panorama navigation map, Curation panel with per-trunk map for curator focus) [evolving]; derived artefacts (PDF/DOCX/diagram export) [today], BPMN/DMN-style handoffs [vision].

## 4. Configurable rigor (key message 5, expanded)

- The Instance contract declares how strict the wiki is: page types, required sections, cardinalities, link targets, tracking.
- Light setting: a team knowledge base with minimal requirements and fast curation.
- Strict setting: a consulting map where every activity needs exactly one Accountable, every rule names its authority, every gap has an owner.
- Trade-off stated plainly: more relationship rules → more interview effort and stricter grills. You choose the point.

## 5. Use cases

### UC1 — Knowledge base for an area, project or product [main, the founding use case]
- Origin: the methodology was created for this case (a department knowledge base in the reference instance).
- What it covers: how the area works (processes, roles, systems, terms), decisions with rationale, open questions with owners.
- Day-to-day value: onboarding, single source of truth, answers with sources for people and agents, explicit "we do not know yet".
- Lifecycle: indexing of documents and interviews, curation of open items, post-update review; light rigor by default, raised where needed.
- Derived views [evolving]: Panorama to explore the base, Curation panel to see where open items concentrate.

### UC2 — Consulting mapping [main, most detailed section]
- What gets mapped: processes (SIPOC, activities with RACI), business rules separate from flow, data sources with owner/steward, analytical tools, stakeholders/roles, gaps (data, process, tool) with owner, impact and cause.
- As-is / to-be: current operation and proposed changes recorded with governance [today]; side-by-side comparison [evolving].
- Completeness: required sections and cardinalities + explicit open questions [today]; link-coverage checks [evolving].
- Illustrative excerpt: short contract snippet + one example process page (anonymous, marked illustrative).
- Client follow-up: published read view per validated increment; correction requests via an external platform (e.g. Basecamp) linked to tickets; the client never touches Git.
- Boundary: complements data catalogues and BPM tools; is the governed source for BPMN/DMN, does not generate them.

### UC3 — Business context for analytical AI [consequence, differentiator]
- Agents navigate governed context that links business meaning to data sources.
- Why curated context beats raw retrieval: a RAG notebook over raw documents (e.g. NotebookLM-style tools) gives no guarantee that sources are consistent; conflicting or ambiguous material reaches the agent, which must interpret it at query time. Wiked resolves conflicts once, with a person, before the agent reads.
- Why richer than catalogue-bound agents: agents over data platforms (e.g. Databricks Genie) take business context from catalogue metadata plus a space-scoped knowledge store and instructions anchored to tables and columns; Wiked carries processes, rules, roles, gaps and decisions, and links them to the catalogue entries, so the agent can build better queries.
- Evidence: public benchmarks (BIRD, NeurIPS 2023) show business knowledge improves text-to-SQL accuracy; no study yet tests a wiki like Wiked → we claim complementarity to semantic layers, not numbers.

### UC4 — Derived artefacts [consequence]
- Reports, diagrams, onboarding material, exports generated from the validated base.

## 6. How a project runs with Wiked

1. Setup: grill to declare scope, language, page types and rigor (Instance contract).
2. Indexing: raw sources (interviews, documents) → source pages with provenance → operational pages.
3. Curation loop: open questions and proposals tracked as tickets; curator focuses via the curation views.
4. Validation on every increment; published read view for the client.
5. Maintenance: post-update review; client requests synced from the external platform.

(Diagram candidate: one-page flow, sources → grill → wiki → validator → views/agents.)

## 7. Market comparison (short, honest)

| Category | Better than Wiked at | Wiked adds |
|---|---|---|
| AI wikis (Confluence, Notion) | UX, hosting, permissions | per-claim provenance, explicit uncertainty, validated structure |
| Data catalogues (DataHub, Atlan, Collibra) | connectors, lineage, quality monitoring | human-decided business meaning, process–rule–data links |
| Enterprise search / RAG notebooks | scale, freshness, zero curation | conflicts resolved before retrieval; curated, auditable meaning |
| Agents on data platforms (e.g. Genie) | direct SQL over governed data | business context beyond table/column scope, linked to the catalogue |
| Process tools (BPM, process mining) | BPMN execution, event-log evidence | governed narrative source, rules and gaps with owners |
| LLM wiki pattern | full automation | governance |

## 8. Maturity at a glance

Three columns: Available today · Evolving · Vision (one table, no promises beyond it).

## 9. Limitations

- No hosted UI or connectors; depends on Git and an agent environment.
- Human pace: interviews and confirmations are the bottleneck by design.
- Structural, not semantic validation: the validator guarantees the form of the content, not its truth; people check truth.
- No proprietary AI benchmark.

## 10. About / maintainer and next steps

- Maintained by UniSoma; open method.
- No commercial model; invitation to a conversation.

---

### Validated choices (requester, 2026-11-13)

- Pitch and five key messages first, then the problem.
- UC2 the longest section; UC1 also well developed as the founding use case.
- Configurable rigor as its own section and fifth key message.
- Market comparison as a short table, including RAG notebooks and data-platform agents; UC3 carries the curated-context argument.
- No commercial model; closing invites a conversation.
- Limitations state that validation guarantees form, not truth.
