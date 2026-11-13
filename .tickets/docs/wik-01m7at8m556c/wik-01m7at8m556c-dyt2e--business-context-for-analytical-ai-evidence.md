---
id: wik-01m7at8m556c-dyt2e
ticket: wik-01m7at8m556c
title: Business context for analytical AI evidence
type: other
created: '2026-11-13T16:04:58.922673221Z'
updated: '2026-11-13T16:04:58.922673221Z'
---

# Business context for analytical AI: public evidence (wik-01m7at8m556c)

Researched 2026-11-13. Numbers are reported exactly as the source states them. "Verified" means the primary source was read. Anything else is marked.

## Summary answer

Public evidence consistently shows that natural-language analytics improves when a model gets curated context linked to the data, such as definitions, value meanings, formulas, mappings and metrics. The evidence comes from benchmarks and controlled comparisons, and it is strongest for **text-to-SQL accuracy on defined questions**. Two kinds of source support it:

- **Peer-reviewed benchmark evidence (strong, narrow).** BIRD (NeurIPS 2023) measured every model it tested with and without human-written "external knowledge evidence." Accuracy rose in every case. For example, GPT-4 went from 34.88% to 54.89% execution accuracy (EX) on the test set. Spider 2.0 (ICLR 2025) shows that enterprise workflows, where agents must search metadata and documentation, remain hard. The best agent solved 21.3% of tasks.
- **Preprints and vendor studies (consistent direction, weaker controls).** These include data.world's knowledge-graph study (16% to 54%), dbt Labs' semantic layer benchmark, the AtScale whitepaper and Snowflake's Cortex Analyst claims. All of them report large gains from a semantic or ontological layer. Their test sets are small and single-domain, and they are often run by the vendor.

**Qualifications.**
1. The evidence measures query correctness, not the "depth" or "quality" of an analysis.
2. Gains shrink as models improve. On the same benchmark, dbt's no-layer text-to-SQL went from 32.7% to 64.5% between 2023 and 2026.
3. Context has to be correct. About 6.8% of BIRD's human evidence was wrong, and fixing it raised accuracy.
4. Automatically generated metadata (profiling) can match or beat human evidence in some settings.
5. No public study tests a Markdown wiki like Wiked directly.

## Evidence table

| # | Source (producer) | Type | Finding | Caveats |
|---|---|---|---|---|
| 1 | BIRD, Li et al., NeurIPS 2023 (HKU, Alibaba and others) [1] | Peer-reviewed benchmark (verified, Table 2) | Evidence covers four kinds of knowledge: numeric reasoning, domain knowledge, synonyms and value illustration. Every model improved with it. GPT-4 test EX went from 34.88% to 54.89% (+20.01), and Claude-2 from 34.60% to 49.02%. Human EX is 92.96%. | 2023 models. The evidence is an oracle written for each question. Value illustration is needed by 70.1% of questions. |
| 2 | SEED, Yun & Lee (Seoul National Univ.), arXiv 2025 [2] | Preprint (verified) | On BIRD dev, every tested system drops without evidence, for example DAIL-SQL (GPT-4) from 56.32 to 35.46 EX. Auto-generated evidence recovers part of the gap and sometimes beats BIRD evidence for fine-tuned CodeS models. 9.65% of the human evidence is missing and 6.84% is wrong. Fixing it raised CodeS-15B from 44.76 to 54.29 on the affected pairs. | Not peer-reviewed. Shows that context *quality* matters, not just its presence. |
| 3 | DIVER, arXiv 2026 [3] | Preprint (abstract and snippet only) | Without expert evidence, execution accuracy drops "by over 10%". Only 5 of 52 leaderboard entries report a no-evidence result. | Not verified in full text. |
| 4 | Spider 2.0, Lei et al., ICLR 2025 oral (HKU, Salesforce and others) [4] | Peer-reviewed benchmark (abstract verified) | Enterprise tasks require searching database metadata, dialect documentation and project codebases. An o1-preview agent solves 21.3%, against 91.2% on Spider 1.0 and 73.0% on BIRD. | Shows that real enterprise context is hard to find and use. It does not isolate the effect of curated context. |
| 5 | BEAVER, Chen et al. (incl. Stonebraker, Cafarella), arXiv v3 2026 [5] | Preprint, real enterprise warehouses (abstract verified) | State-of-the-art agentic frameworks using GPT-5.2 reach 10.8%. With oracle subtask hints they reach 30.1%. The abstract cites intricate schemas, domain knowledge and complex queries. | Only 93 queries. The hints are oracle subtask annotations, not a business wiki. |
| 6 | Shkapenyuk et al. (AT&T), arXiv 2025 [6] | Preprint (abstract and secondary summary) | Notes that BIRD and Spider metadata "is generally not available in practice." LLM-generated profiling metadata took the top BIRD position in March 2025. | Fusion results come from a secondary summary and are uncertain. Supports *automated* metadata as an alternative to curation. |
| 7 | Sequeda, Allemang, Jacob (data.world), arXiv 2023 [7] | Vendor preprint | Insurance schema with GPT-4 zero-shot: 16% on SQL against 54% on an ontology/KG layer. | One domain, one model, zero-shot. Not peer-reviewed. Produced by a KG vendor. |
| 8 | Allemang & Sequeda (data.world), arXiv 2024 [8] | Vendor preprint (secondary detail) | Ontology-based query check plus LLM repair reaches about 72% overall, including 8% "I don't know," with about 20% error. | Same benchmark. Abstaining is counted as a feature. |
| 9 | dbt Labs (Ganz, Perigaud), blog, Apr 2026; open repo [9] | Vendor benchmark, open source (verified) | 11 ACME questions run 20 times each. On modeled data the semantic layer scores 98.2% (Sonnet 4.6) and 100% (GPT-5.3-Codex), against 90.0% and 84.1% for text-to-SQL. On the raw schema it scores 0% on questions with too many hops. Text-to-SQL improved from 32.7% (GPT-4, 2023) to 64.5% (2026). | Vendor and tiny. The authors note that out-of-scope questions return an error instead of a wrong number. Bodo.ai reports a 100% replication with no hand-built models [10] (unverified). |
| 10 | AtScale whitepaper, 2024 [11] | Vendor (secondary report) | TPC-DS, 40 questions, Gemini 1.5 Pro: 20% with schema only against 92.5% with the semantic layer. | Vendor, small set. AtScale itself notes that vendor accuracy claims are hard to validate. |
| 11 | Snowflake Cortex Analyst blogs, 2024 [12] | Vendor (search snippets only; the page returned HTTP 403) | Claims about 90% on an internal 150-question set and about 2x single-shot LLM SQL. | Internal benchmark, unverified. |
| 12 | Anthropic, "Effective context engineering for AI agents," 2025 [13] | Vendor engineering guidance (verified) | Context is a finite "attention budget" subject to context rot. Recommends just-in-time retrieval through lightweight identifiers, progressive disclosure through exploration and persistent notes. | Design guidance, not a measurement. Supports Wiked's loading model, not its accuracy claim. |

## What a wiki adds compared with a semantic layer

- **Scope.** A semantic layer (MetricFlow, Cube, AtScale, Cortex semantic models) encodes *executable* metrics, dimensions and joins. A governed wiki also records context that cannot be executed: processes, business rules, *why* a number is defined that way, known data gaps and quality issues, ownership and tools. This is the kind of knowledge that BIRD's "domain knowledge" and "value illustration" evidence and BEAVER's "domain knowledge" bottleneck point to.
- **Provenance and gaps.** The wiki records where a fact came from and what is undefined. SEED's finding that wrong evidence lowers accuracy argues for governed, sourced context. dbt's "error instead of a wrong number" and data.world's "I don't know" show the value of knowing your limits. A wiki can state those limits explicitly.
- **Progressive disclosure.** Index-based lazy loading matches Anthropic's just-in-time and progressive-disclosure guidance.
- **Complementary, not a replacement.** The evidence favors executable semantic layers for exact KPI answers. A wiki should link to the semantic layer and the data catalog rather than compete with them on metric computation.
- **Unproven.** No public study measures a curated Markdown wiki, or "analytical depth," as opposed to SQL correctness.

## Defensible phrasing (external document)

> "Public benchmarks show that AI models answer data questions markedly more accurately when they are given business knowledge linked to the data. In the BIRD benchmark (NeurIPS 2023), supplying such knowledge raised GPT-4's execution accuracy from 35% to 55%, and vendor studies of semantic layers and knowledge graphs report similar gains. Wiked applies this principle: it maintains a governed, sourced map of the business (processes, rules, data sources and their gaps) that an AI agent explores on demand, complementing semantic layers and catalogs."

Avoid the following:
- quoting vendor percentages as general facts;
- claiming that Wiked itself has been measured;
- promising "depth" improvements without evidence;
- implying that the gains persist unchanged with newer models.

## Sources

1. https://arxiv.org/abs/2305.03111 (PDF v3, Table 2)
2. https://arxiv.org/html/2506.07423v1
3. https://arxiv.org/html/2602.12064
4. https://arxiv.org/abs/2411.07763
5. https://arxiv.org/abs/2409.02038
6. https://arxiv.org/abs/2505.19988
7. https://arxiv.org/abs/2311.07509
8. https://arxiv.org/abs/2405.11706 ; https://data.world/blog/genai-benchmark-ii-increased-llm-accuracy-with-ontology-based-query-checks-and-llm-repair
9. https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026 ; https://dbt-labs.github.io/dbt-llm-sl-bench
10. https://www.bodo.ai/blog/how-pydough-reached-100-accuracy-on-dbts-semantic-layer-benchmark
11. https://bigdatawire.com/2024/08/15/atscale-claims-text-to-sql-breakthrough-with-semantic-layer ; https://atscale.com/?p=24977
12. https://www.snowflake.com/en/blog/cortex-analyst-ai-self-service-analytics/ ; https://www.snowflake.com/en/blog/engineering/cortex-analyst-text-to-sql-accuracy-bi/
13. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
