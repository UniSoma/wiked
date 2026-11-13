---
id: wik-01m7at8ky3xw-dtjth
ticket: wik-01m7at8ky3xw
title: Data governance and catalog practices for mapping data sources
type: other
created: '2026-11-13T16:04:20.703819570Z'
updated: '2026-11-13T16:04:20.703819570Z'
---

# Data governance and catalog practices for mapping data sources

Ticket: wik-01m7at8ky3xw. Date: 2026-11-13. Research only, not normative guidance.

## Summary answer

No single standard defines "how to map data sources and their gaps" for a consulting engagement. The practice is assembled from several pieces:
- DAMA-DMBOK knowledge areas: governance, metadata, data quality, architecture, integration.
- Catalog vocabularies: W3C DCAT for describing a dataset or service, and W3C DQV for quality statements.
- Lineage models: OpenLineage Job, Run and Dataset.
- Data contracts (ODCS) for expectations, SLA and roles.
- Named data quality dimensions (DAMA UK / UK Government framework) that give gaps a typed vocabulary.

The common pattern has five steps:
1. Inventory sources with ownership and access metadata.
2. Separate business meaning (glossary) from technical structure (dictionary).
3. Record lineage from source to consumer (process or job, then report or tool).
4. Assess fitness for purpose per use against named quality dimensions.
5. Record gaps as explicit, owned, actionable items.

"Data gap analysis" itself has no primary standard I could find (uncertain). The closest primary anchors are the UK framework's "fitness for purpose", its action plans and root cause analysis, and DQV quality annotations.

## Practices

- **DAMA-DMBOK.** DMBOK2 is described as "the globally recognized framework for data management". A 2024 revision exists, and a 3.0 "evergreening" project began in 2025 (https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/). DAMA's page does not list the knowledge areas. Secondary sources give 11, with Data Governance at the hub: Architecture, Modeling & Design, Storage & Operations, Security, Integration & Interoperability, Document & Content, Reference & Master Data, Warehousing & BI, Metadata, and Data Quality (https://www.dawiso.com/glossary/dama-dmbok; https://datacrossroads.nl/2018/06/25/dama-dmbok-in-a-nutshell/). Treat the exact list as secondary until it is checked against the book. ISACA notes that business owners ("stewards or custodians") answer for quality, classification and access rules, and IT answers for security and backup (https://www.isaca.org/resources/isaca-journal/issues/2017/volume-3/is-audit-basics-data-management-body-of-knowledgea-summary-for-auditors).
- **DCAT 3** (W3C Recommendation, 22 Aug 2024; https://www.w3.org/TR/vocab-dcat-3/). Classes: Catalog, Resource, Dataset, Distribution, DataService and DatasetSeries. Properties that describe a source:
  - `dcterms:publisher` and `dcat:contactPoint`
  - `dcterms:temporal` and `dcterms:spatial` coverage
  - `dcterms:accrualPeriodicity` (update frequency)
  - `dcterms:conformsTo`
  - `dcat:accessURL`
  - `dcterms:license` and `dcterms:accessRights`
  - `prov:wasGeneratedBy`
  - `dcat:qualifiedRelation` for typed links
  - qualified attribution with `dcat:hadRole`
- **DQV** (W3C Working Group Note, 15 Dec 2016; https://www.w3.org/TR/vocab-dqv/). Classes:
  - Dimension and Category: the quality characteristics
  - Metric and QualityMeasurement: measured values
  - QualityAnnotation: feedback, ratings or certificates
  - QualityPolicy

  DQV is a natural model for "a known quality issue attached to a dataset" (inference).
- **OpenLineage** (https://openlineage.io/docs/spec/object-model):
  - **Job:** a process that reads or writes Datasets.
  - **Run:** one occurrence of a Job.
  - **Dataset:** an abstract collection of data. Facets include `schema`, `dataSource`, `dataQualityAssertions` and `ownership`.

  Lineage comes mainly from runtime RunEvents. Design-time JobEvent and DatasetEvent can declare static inputs, outputs and metadata. So lineage is either observed or declared, which matters for a wiki that can only hold declared lineage.
- **Data quality dimensions.** The UK Government Data Quality Framework adopts DAMA UK's six dimensions: completeness, uniqueness, consistency, timeliness, validity and accuracy. It frames quality as "fitness for purpose" and says "It is unlikely that data will be equally fit for all purposes". It recommends action plans, root cause analysis "at source", metadata that communicates quality, and a six-stage data lifecycle (https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework). ISO/IEC 25012 has 15 characteristics, split into inherent and system-dependent; I verified only partially (https://iso25000.com/en/iso-25000-standards/iso-25012).
- **Business glossary vs data dictionary vs catalog.** Practitioners broadly agree:
  - The glossary holds business terms and meaning, for business users.
  - The dictionary holds technical fields, types and constraints, for IT.
  - The catalog links both to assets, adding lineage, ownership and quality.

  Sources disagree on whether the dictionary is a subset of the glossary. These are vendor blogs, not primary sources (https://www.informatica.com/blogs/business-glossary-vs-data-catalog.html; https://analytics8.com/blog/data-dictionary-vs-data-catalog-vs-business-glossary).

  Primary product docs:
  - DataHub: glossary terms are "words or phrases with a specific business definition", with owners, Contains/Inherits relations and Draft/Published/Deprecated states (https://docs.datahub.com/docs/glossary/business-glossary).
  - Microsoft Purview: governance domains, data products, glossary terms, "critical data elements" (one logical "Customer ID" mapped to CustID and CID), data quality rules and OKRs that link data to business objectives (https://learn.microsoft.com/en-us/purview/unified-catalog). Purview data governance is being retired in favour of Fabric, with maintenance through Nov 2027 (same page).
- **Data contracts.** The Open Data Contract Standard (Bitol) is a platform-agnostic YAML contract. Sections: fundamentals, schema, data quality, SLA, team and roles, support channels, authoritative definitions (https://bitol-io.github.io/open-data-contract-standard/latest/). I could not confirm its governing body from that page.

## Minimal attribute set

**Data source page.** A business-facing synthesis of DCAT, OpenLineage and Purview; this set is an inference.

- **Identity:** name, aliases, kind (system, database, file/spreadsheet, API, external provider), and the system of record if one exists.
- **Owner:** the accountable business owner and the steward. Technical custodian is optional.
- **Content:** subjects or entities covered, linked to glossary terms; coverage (temporal, spatial, organizational); granularity.
- **Access:** access mode or location, without credentials; access restrictions and sensitivity; license or contractual basis for external data.
- **Freshness:** update frequency and latency.
- **Lineage (declared):** feeds (upstream sources or processes) and feeds-into (tools, reports, other sources).
- **Usage:** processes that produce or consume it, and business rules applied to or derived from it.
- **Quality status:** per dimension and per use, with linked gaps.
- **Lifecycle state:** e.g. proposed, confirmed, deprecated.
- **Provenance:** for each claim; Wiked Source evidence such as an interview or a document.

**Data gap page.** Modelled on DQV QualityAnnotation plus the UK framework's action plan and root cause; this structure is an inference.

- **Affected item:** the data source(s) and fields or entities affected.
- **Gap type:** one of
  - missing source or field (availability)
  - one of the six quality dimensions
  - access or permission
  - ownership undefined
  - definition conflict
  - lineage unknown
- **Impact:** the impacted use, i.e. the process, rule, analytical tool or decision. Gaps are use-relative, per "fitness for purpose".
- **Evidence and observed by:** who and when, with provenance.
- **Severity or priority:** chosen by humans. No standard scale was found.
- **Root cause hypothesis.**
- **Proposed remediation and owner.**
- **State:** e.g. open, accepted risk, remediating, resolved.
- **Linked ticket.**

## Relations

| From | Relation | To |
|---|---|---|
| Process / activity | produces, consumes | Data source |
| Business rule | defined over (term), enforced in, depends on | Glossary term, Data source |
| Analytical tool / report | reads from | Data source (declared lineage) |
| Stakeholder | owns, stewards, uses, reports gap | Data source, Gap |
| Data gap | affects | Data source, and blocks a Process, Rule or Tool |
| Glossary term | is represented by | Data source fields (CDE-like mapping) |

## Wiki vs data catalog

**A wiki can hold:**
- declared, human-validated meaning: glossary, ownership, the purpose of each source, business rules;
- the cross-links between processes, rules, sources, tools and stakeholders, which catalogs model poorly or not at all;
- gaps, with provenance and decision history;
- the state of an engagement before any catalog exists.

This fits Wiked's grill, provenance and structured sections.

**A wiki cannot replace:**
- automated technical metadata harvesting (schemas, columns);
- runtime lineage (OpenLineage RunEvents);
- measured quality metrics and monitoring (DQV measurements, Purview data quality scores);
- access policy enforcement;
- search at estate scale.

These need connectors to live systems. A wiki's lineage and quality claims are declared or observed by people, so they can drift; mark them as such.

## Value proposition implications

- **Message:** "the business map that a catalog presupposes". Catalog vendors say catalogs need a glossary and dictionary to work (DataGalaxy blog, secondary). The consultancy wiki produces those artefacts, plus process and rule context, in human-validated form.
- **Use recognised vocabulary** so clients and data teams recognise the work: DAMA dimensions for gap types, DCAT-like attributes for sources, owner/steward roles.
- **Position the wiki as a handoff:** structured fields aligned to DCAT, ODCS and OpenLineage concepts make it easier to migrate into a catalog or data contracts later. Do not claim compatibility without an export (uncertain, untested).
- **Be explicit that it is not a catalog:** no automated lineage, quality monitoring or access control.

## Sources

- https://dama.org/learning-resources/dama-data-management-body-of-knowledge-dmbok/
- https://www.dawiso.com/glossary/dama-dmbok (secondary)
- https://datacrossroads.nl/2018/06/25/dama-dmbok-in-a-nutshell/ (secondary)
- https://www.isaca.org/resources/isaca-journal/issues/2017/volume-3/is-audit-basics-data-management-body-of-knowledgea-summary-for-auditors
- https://www.w3.org/TR/vocab-dcat-3/
- https://www.w3.org/TR/vocab-dqv/
- https://openlineage.io/docs/spec/object-model
- https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework
- https://iso25000.com/en/iso-25000-standards/iso-25012 (partial)
- https://docs.datahub.com/docs/glossary/business-glossary
- https://learn.microsoft.com/en-us/purview/unified-catalog
- https://bitol-io.github.io/open-data-contract-standard/latest/
- https://www.informatica.com/blogs/business-glossary-vs-data-catalog.html (vendor blog)
- https://analytics8.com/blog/data-dictionary-vs-data-catalog-vs-business-glossary (consultancy blog)
- https://www.datagalaxy.com/en/blog/data-catalog-vs-glossary-dictionary/ (vendor blog)
