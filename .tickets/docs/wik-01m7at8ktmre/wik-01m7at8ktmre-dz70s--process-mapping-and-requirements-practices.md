---
id: wik-01m7at8ktmre-dz70s
ticket: wik-01m7at8ktmre
title: Process-mapping and requirements practices
type: other
created: '2026-11-13T16:04:32.075769196Z'
updated: '2026-11-13T16:04:32.075769196Z'
---

# Process-mapping and requirements practices: what a consulting knowledge base must hold

Ticket: wik-01m7at8ktmre. Date: 2026-11-13. Non-normative research.

## Summary answer

A consulting process-mapping engagement is expected to cover four layers that the
market bodies of knowledge already name: (1) context and scope (SIPOC, stakeholders,
RACI); (2) process models for the current and future states plus the gap between
them (ABPMP Process Analysis/Design, BABOK Strategy Analysis, BPMN); (3) decisions
and business rules kept apart from process flow (Business Rules Manifesto, SBVR,
DMN); (4) requirements classified by level and traced across those artifacts, each
passing through explicit life-cycle states (BABOK). Elicitation (interviews,
workshops) is the evidence layer underneath, with explicit unconfirmed and
confirmed results. For a structured wiki this means typed entities with
provenance, typed relations (trace links), per-entity states mirroring BABOK
outputs, and completeness criteria computed as coverage of those links.

## Artifacts and what each needs

| Artifact / practice | Source | What it requires from the knowledge base |
|---|---|---|
| BACCM (Change, Need, Solution, Stakeholder, Value, Context) | IIBA Core Standard [1] | A frame: every proposal (Change) links to a Need, Stakeholders and expected Value. IIBA states all six concepts "are equal and necessary" [1]. |
| Elicitation via interviews and workshops | IIBA [1][2] | Session records; results with states *unconfirmed* -> *confirmed* [1]; link each claim to its session (provenance). |
| Stakeholder engagement approach / stakeholder list | IIBA task 3.2 [1] | Stakeholder entity with role, interest, influence [1]. |
| RACI | PMI Lexicon [3] | Matrix Stakeholder/Role x Activity with R/A/C/I; PMI material says only one Accountable per task [3] (enforceable cardinality). |
| SIPOC (+CM) | ASQ [4] | Per process: suppliers, inputs, 5-7 core activities, outputs, customers; optional constraints and measures [4]. |
| Current-state description, future-state description, change strategy (gap analysis) | IIBA tasks 6.1, 6.2, 6.4 [1]; ABPMP CBOK v4 knowledge areas Process Analysis and Process Design [5] | Paired as-is/to-be process pages; explicit Gap entity bridging them; potential value [1]. |
| BPMN process models | OMG BPMN 2.0.2 [6] | Activities, events, gateways, pools/lanes per role (lane semantics from the spec, not re-verified here). Wiked's D2 swimlanes are a lighter analogue, not BPMN-conformant. |
| Business rules (separate from process) | Business Rules Manifesto [7]; OMG SBVR 1.5 [8] | Rule as first-class entity, referenced by many processes ("Rules apply across processes and procedures" [7]); rules built on glossary terms and fact types [7][8]; SBVR distinguishes structural (necessity) and operative (obligation) rules [9, secondary]. |
| Decisions | OMG DMN (formal 1.6 per OMG page) [10][11] | Decision entity with dependencies on Input Data, Business Knowledge Models and Knowledge Sources (authority/policy) [11]; link to the BPMN task it supports [11]. Executable decision tables/FEEL are out of scope for a wiki; the DRD level is the useful one. |
| Requirements classification | IIBA [1] | Types: business, stakeholder, solution (functional, non-functional), transition [1]. |
| Requirements life cycle and traceability | IIBA tasks 5.1-5.5, 7.2-7.3 [1] | States traced, maintained, prioritized, verified, validated, approved [1]; trace links "for impact analysis, coverage, and allocation" [1]. Relation names derive/depends/satisfy/validate are commonly attributed to BABOK v3 but were only confirmed via secondary sources [12] (uncertain). |

## Suggested entity/relationship model (input for the reference Instance contract)

Entities (page types), each with provenance to Source/Session:

- **Source** / **ElicitationSession** (interview, workshop, document review): date, participants (Stakeholder refs), state `unconfirmed|confirmed`.
- **Stakeholder** and **Role**: interest, influence; Role is the lane in diagrams.
- **Process** with `state_kind: as-is|to-be`; structured sections: SIPOC fields, activities (ordered), RACI rows (activity x role x R/A/C/I), measures/KPIs.
- **Gap**: references one as-is Process (or DataSource/Rule) and its to-be counterpart; cause, impact, proposed change.
- **BusinessRule** with `kind: structural|operative`, `status: current|proposed|retired`, statement using Glossary terms, authority (Knowledge Source).
- **Decision**: inputs (DataSource/InputData), rules/BKM used, authority, owning Role.
- **GlossaryTerm** (SBVR noun concepts) and optionally **FactType**.
- **Requirement** with `type: business|stakeholder|functional|non-functional|transition`, priority, state.
- **DataSource** and **AnalyticalTool** (to connect with sibling data-governance research).
- **Need/Objective** and **Value** (BACCM anchor), **OpenQuestion** (pendência) and **ChangeProposal** linked to tickets.

Relations (typed, directed, validator-checkable):
`Process -performed_by-> Role`; `Process -uses_input/produces-> DataSource`;
`Process -applies-> BusinessRule`; `Process.activity -invokes-> Decision`;
`Decision -requires-> Decision|DataSource`; `Decision -governed_by-> Source`;
`BusinessRule -defined_in_terms_of-> GlossaryTerm`;
`Gap -from-> Process(as-is)`, `Gap -to-> Process(to-be)`;
`Requirement -derives_from-> Requirement|Need`; `Requirement -addresses-> Gap`;
`Requirement -satisfied_by-> Process(to-be)|Rule|Tool`; `* -evidenced_by-> Session|Source`.

States: map BABOK outputs onto Wiked page states rather than inventing new ones:
draft (unconfirmed elicitation) -> confirmed -> verified (quality-checked) ->
validated (aligned to business requirements) -> approved (human decision via grill).

## Completeness criteria (computable)

1. Every Process has SIPOC fields filled, at least one Role, and exactly one Accountable per activity (PMI rule [3]).
2. Every as-is Process either has a to-be counterpart or an explicit "no change" decision; every Gap links both sides.
3. Every BusinessRule and Decision is referenced by at least one Process and cites an authority/source; proposed rules link to a Gap or Requirement.
4. Every rule's key terms resolve to GlossaryTerm pages (Manifesto art. 3 [7]).
5. Trace coverage: each business requirement has at least one derived stakeholder/solution requirement; each solution requirement is satisfied by a to-be element; no orphan requirements (BABOK "coverage" [1]).
6. Every claim is evidenced by a confirmed session/source; unconfirmed material appears as open questions.
7. Every Stakeholder appearing in RACI exists in the stakeholder register.
These are structural checks that suit a deterministic validator; correctness of meaning remains a human (grill) responsibility.

## Implications for a business-facing value proposition

- Wiked can be positioned as covering the BABOK "requirements life cycle" and ABPMP "analysis/design" deliverables as a *living, traced* body rather than static documents: impact analysis ("which processes change if rule X changes?") comes from typed links, which is exactly the purpose IIBA gives to tracing [1].
- Separating rules and decisions from process pages directly follows the Business Rules Manifesto and DMN/BPMN split [7][11], which clients' BA/BPM staff will recognise.
- Honest limits: Wiked does not produce BPMN-conformant or DMN-executable models; position it as the governed source from which such models can be produced, and interoperate rather than compete with BPM suites.
- Explicit confirmed/unconfirmed states and pendências map onto BABOK elicitation outputs, which is a credible argument to procurement/QA reviewers.

## Sources

1. IIBA, Global Business Analysis Core Standard (companion to BABOK v3), 2017: https://www.iiba.org/globalassets/standards-and-resources/core-standard/iiba-core-standard.pdf
2. IIBA, Elicitation and Collaboration (Business Analysis Standard): https://www.iiba.org/knowledgehub/the-business-analysis-standard/5-applying-business-analysis-tasks/5-3-business-analysis-knowledge-areas/elicitation-and-collaboration/
3. PMI Lexicon of Project Management Terms v5.0 (RACI, accountability): https://www.pmi.org/-/media/pmi/documents/registered/pdf/pmbok-standards/pmi-lexicon-pm-terms.pdf ; PMI blog on RACI: https://www.pmi.org/blog/stakeholder-management-raci (single Accountable stated via search summary; not read in full)
4. ASQ, SIPOC+CM: https://asq.org/quality-resources/sipoc
5. ABPMP, BPM CBOK 4.0 webinar (nine knowledge areas): https://www.abpmp.org/resource/resmgr/bpm_cbok_4.0_webinar_2019.pdf ; https://www.abpmp.org/page/guide_BPM_CBOK (CBOK full text is gated; contents via search summary)
6. OMG, BPMN 2.0.2 (Jan 2014): https://www.omg.org/spec/BPMN/2.0.2/About-BPMN
7. Business Rules Group, Business Rules Manifesto: https://www.businessrulesgroup.org/brmanifesto.htm
8. OMG, SBVR 1.5 (Dec 2019): https://www.omg.org/spec/SBVR/
9. Wikipedia, SBVR (secondary): https://en.wikipedia.org/wiki/Semantics_of_Business_Vocabulary_and_Business_Rules
10. OMG, DMN spec page: https://www.omg.org/spec/DMN/ (page reports formal 1.6, Sept 2026; not independently confirmed)
11. OMG, DMN data sheet: https://omg.org/intro/DMN.pdf ; Camunda DRG reference (secondary): https://docs.camunda.org/manual/7.22/reference/dmn/drg
12. Trace relation types (secondary, uncertain): https://open-exam-prep.com/study-guides/cbap/requirements-life-cycle-management/trace-requirements
