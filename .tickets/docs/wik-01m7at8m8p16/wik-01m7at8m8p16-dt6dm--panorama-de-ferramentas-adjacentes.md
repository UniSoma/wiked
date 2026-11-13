---
id: wik-01m7at8m8p16-dt6dm
ticket: wik-01m7at8m8p16
title: Panorama de ferramentas adjacentes
type: other
created: '2026-11-13T16:04:46.496629858Z'
updated: '2026-11-13T16:04:46.496629858Z'
---

# Adjacent tools landscape vs. Wiked

Ticket: wik-01m7at8m8p16. Research date: 2026-11-13. Non-normative research material.

## Summary answer

None of the adjacent categories does what Wiked does as a whole, and each does one part of it better. AI wikis (Confluence + Rovo, Notion AI, Guru) are better at search, chat over many connected sources, permissions, and collaborative editing. Their trust model is page- or card-level "verified/owner/expiry". Claim-level provenance, explicit open questions, and an interview-gated meaning decision are not documented features. Data catalogs (DataHub, Atlan, Collibra, Alation) are better at automated technical metadata, lineage, and stewardship workflows over data assets. They do not cover the narrative business knowledge of processes, rules, and stakeholders. Enterprise search (Glean) indexes and answers over existing content with source permissions. It does not curate or govern meaning. Process tools are better at evidence from event logs (Celonis) or formal BPMN/DMN models with dictionaries and publishing (Signavio, Bizagi). Docs-as-code and LLM-wiki setups (Obsidian, Docusaurus, GitHub, Karpathy's "LLM Wiki" pattern) share Wiked's open Markdown and agent maintenance. They lack a governance contract, a mandatory human meaning gate, and a deterministic validator. Wiked's honest positioning is a governed, provenance-first knowledge layer that sits in the client's repo and complements these tools. It is not a replacement for them.

## Comparison table (by category)

| Category / tools | What they do better than Wiked | Overlap with Wiked | Where Wiked differs |
|---|---|---|---|
| AI wikis: Confluence + Rovo, Notion AI, Guru | Rich WYSIWYG collaboration; search and chat across Atlassian/Notion plus connected apps (Slack, Google Drive) with permission-aware results; agents that act in Jira/Confluence; mature hosting and admin. Page/card verification with owners, expiry, and reminders (Notion verified pages; Guru verifier + interval; Confluence "Verified" status per community reports, unconfirmed in official docs). | Knowledge base; AI Q&A with citations (Notion "answers with citations"; Rovo source links per community, uncertain). | Trust is per page/card, not per claim. No documented first-class open-question/decision objects linked to tickets. No mandatory human interview before meaning changes. Proprietary storage (export exists, but not repo-native). Wiki lives in vendor SaaS, not the client's repo. |
| Data catalogs: DataHub, Atlan, Collibra, Alation | Automated ingestion of technical metadata from many connectors; lineage (incl. column-level in some); business glossary with approval states and ownership; formal stewardship/certification workflows (Collibra strongest for regulated governance, per third-party reviews). DataHub core is Apache 2.0 open source. | Glossary, ownership, data sources and gaps, governance vocabulary. | Catalogs model data assets. Wiked models business meaning around processes, rules, stakeholders, tools, and uncertainty, with prose plus provenance. Wiked does no automated metadata harvesting or lineage. |
| Enterprise search: Glean | Connectors that pull content and permission maps from source systems; knowledge graph of content, people, and activity; AI answers and agents at org scale. | Agent navigability of company knowledge. | Glean retrieves what exists. It does not decide what is true, record uncertainty, or produce a curated deliverable. Wiked pages could be one of the sources Glean indexes. |
| Process tools: Celonis (mining), SAP Signavio, Bizagi (modelling) | Celonis: discovers actual process flows from event logs (case ID, activity, timestamp; object-centric logs). Signavio: BPMN/DMN modelling, shared dictionary linked to model elements, Collaboration Hub for reader/stakeholder comments, governance workflows. Bizagi Modeler: free BPMN modelling, simulation, export to Word/PDF/SharePoint. | Process mapping, stakeholders, business rules, consulting deliverables. | Wiked is narrative and text-first and keeps no event-log evidence or executable notation. It adds provenance per claim, open questions, and decisions that BPMN tools hold only as annotations. Wiked can link to BPMN/mining artifacts as sources. |
| Docs-as-code / LLM wiki: Obsidian, Docusaurus, GitHub Markdown, Karpathy "LLM Wiki" | Obsidian: local Markdown vault, graph view, plugin ecosystem, mature reader UX. Docusaurus: polished static publishing, versioning, search. GitHub: review, history, CI. LLM Wiki pattern: low-ceremony ingest/query/lint loop, already popular. | Same substrate: open Markdown, git history, agent-maintained pages, index/log, lint for contradictions and stale claims. | The LLM Wiki gist describes no formal approval process and notes lint cannot establish factual accuracy. Wiked adds the mandatory grill, claim-level provenance, explicit open questions/proposed changes tied to tickets, consumer-defined page types, a deterministic validator, and derived curation dashboards. |

## Wiked strengths (differentiation)

- **Governance of meaning.** Humans decide meaning through a mandatory interview. Competitors govern access, ownership, and freshness, not the meaning decision itself.
- **Claim-level provenance.** AI tools cite documents in answers. Wiked keeps provenance as persisted content of the knowledge base itself.
- **Explicit uncertainty.** Open questions and proposed changes are first-class and linked to tickets. In other tools, the closest analogue is "unverified" or "expired" status.
- **Open format and lock-in.** Plain Markdown in the client's repo, readable without any vendor. Obsidian and docs-as-code share this; SaaS wikis, catalogs, and Glean do not.
- **Agent navigability.** Typed pages, a validator, and derived navigation give agents a predictable structure, beyond retrieval over unstructured pages.
- **Consulting deliverable.** One governed artifact covers processes, data sources and gaps, rules, tools, and stakeholders, and the client keeps it after the engagement.

## Wiked weaknesses (honest)

- No hosted UI, WYSIWYG editing, real-time collaboration, comments for non-technical stakeholders, or SSO/permission model. It relies on git, the repo, and the agent.
- No connectors or automated harvesting: content enters through ingestion with human gating, which is slower and does not scale like Glean or catalogs.
- No lineage or technical metadata, and no event-log process evidence, BPMN/DMN, or simulation.
- Requires an agent-capable toolchain and git literacy, plus discipline in grilling. Throughput is limited by human interview time.
- Small, new methodology with no ecosystem, certifications, or enterprise references comparable to vendors.
- Search over a large corpus depends on the agent or external tools.

## Complementarity (Wiked alongside, not instead)

- **Confluence/Notion.** Wiked is the governed source of decided meaning. Published or rendered views can be mirrored into the wiki teams already use, and SaaS pages become ingestion sources with provenance.
- **Catalogs.** Catalog entries are sources for Wiked's data-source and gap pages. Wiked's decided business terms and rules can feed the catalog glossary. Business narrative stays in Wiked and asset metadata stays in the catalog.
- **Glean/Rovo.** These index Wiked's Markdown as a high-trust source, so Wiked improves answer quality without competing on search.
- **Celonis/Signavio/Bizagi.** Mining shows what happens and models formalize it. Wiked records what people say, decide, and do not yet know, linking to models and mining results as evidence. It can be the discovery phase before modelling.
- **Obsidian/Docusaurus/GitHub.** These are viewers and publishers over Wiked's files. Wiked is the governance layer on top of the LLM Wiki pattern.

## Implications for the external value proposition

1. Position Wiked as a governed knowledge layer and consulting deliverable, not as a wiki, catalog, or search product. Competing head-on on UX or connectors loses.
2. Lead with three verifiable differences: claim-level provenance, explicit uncertainty linked to tickets, and human-decided meaning via interview. Back them with a sample page and a validator run.
3. Frame "LLM Wiki plus governance" for technical audiences. The pattern is known, and Wiked answers its stated gap (no approval process, no factual assurance).
4. State the integration story explicitly: "works with your Confluence/Notion/catalog/BPMN tool" lowers adoption risk.
5. Be upfront about weaknesses (no hosted UI, git-based, human-paced). Make the reader-facing rendering for non-technical stakeholders a roadmap or gap item.
6. Avoid superlatives. Several competitor claims here come from third-party sources, so verify them before any public comparison.

## Uncertainty notes

- Confluence native "Verified" status and Rovo source citations are confirmed only by Atlassian Community posts, not official docs.
- The Atlan, Alation, and Collibra stewardship details come mostly from third-party or competitor comparisons, except the official Collibra glossary page.
- Celonis docs were behind sign-in, so its claims come from the Celonis blog (older pages).
- Connector counts (Glean, DataHub) conflict across sources and are omitted.
- No pricing is included, except that Bizagi Modeler is officially labelled "Free Modeler".

## Sources

- Atlassian Rovo: https://support.atlassian.com/rovo/docs/what-is-rovo/
- Confluence/Rovo community (unofficial): https://community.atlassian.com/forums/Rovo-questions/How-does-Rovo-handle-conflicting-or-incomplete-information/qaa-p/3268873 ; https://community.atlassian.com/forums/App-Central-articles/Your-Rovo-Problem-Isn-t-AI-It-s-That-Nobody-Knows-Which/ba-p/3251366
- Notion AI: https://www.notion.com/help/guides/everything-you-can-do-with-notion-ai
- Notion verified pages: https://notion.com/help/wikis-and-verified-pages
- Guru verification: https://help.getguru.com/docs/verifying-and-unverifying-cards ; https://www.getguru.com/features/verification
- DataHub (Apache 2.0): https://solutions.datahub.com/lp/open-source-metadata-management ; https://datahub.com/docs/
- Collibra glossary (official): https://productresources.collibra.com/docs/collibra/2026.02/Content/Products-and-features/co_products-and-features.htm
- Catalog comparisons (third-party, low confidence): https://www.techtarget.com/data-technologies/feature/15-top-data-catalog-software-tools-to-consider-using-in-2026 ; https://data.world/resources/compare/alation-vs-collibra/
- Glean: https://docs.glean.com/connectors/about ; https://docs.glean.com/connectors/key-terms ; https://docs.glean.com/security/knowledge-graph
- Celonis: https://www.celonis.com/blog/what-is-object-centric-process-mining-ocpm ; https://www.celonis.com/insights/topics/how-does-process-mining-work
- SAP Signavio: https://help.sap.com/docs/signavio-process-manager/user-guide/intro?locale=en-US ; https://help.sap.com/docs/signavio-process-manager/user-guide/fa7396966dad1014a4730ff5fb2ca89e.html ; https://help.sap.com/doc/966865eb1a274bccadc05e0bded96694/SHIP/en-US/sap-signavio-process-collaboration-hub-user-guide-EN.pdf
- Bizagi Modeler: https://www.bizagi.com/en/platform/modeler
- Obsidian storage: https://obsidian.md/help/data-storage
- Karpathy LLM Wiki: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
