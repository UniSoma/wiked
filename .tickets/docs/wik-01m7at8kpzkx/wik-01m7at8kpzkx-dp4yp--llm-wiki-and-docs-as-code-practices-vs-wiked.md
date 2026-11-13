---
id: wik-01m7at8kpzkx-dp4yp
ticket: wik-01m7at8kpzkx
title: LLM wiki and docs-as-code practices vs Wiked
type: other
created: '2026-11-13T16:03:35.944589939Z'
updated: '2026-11-13T16:03:35.944589939Z'
---

# Market practices around LLM-maintained wikis and docs-as-code: positioning Wiked

Ticket: wik-01m7at8kpzkx. Date: 2026-11-13. Non-normative research.

## Summary answer

Wiked sits at the intersection of three established practices: (1) the "LLM wiki" pattern popularized by Andrej Karpathy (an agent compiles curated sources into a persistent, interlinked Markdown wiki instead of re-deriving answers via RAG on every query); (2) docs-as-code (plain text, Git, review, issue trackers, automated tests); and (3) agent-instruction files such as AGENTS.md. Wiked converges with all three on mechanics, and is close to a concrete, governed implementation of Karpathy's deliberately abstract pattern (raw sources / wiki / schema; ingest / query / lint; index-first navigation).

Wiked diverges where those practices are silent: meaning is decided by humans through a mandatory interview (grill) rather than delegated to the LLM; every claim carries provenance to ingested sources rather than only query-time citations; open questions and proposed changes are first-class, ticket-linked sections; structure is declared in a consumer-owned contract and checked by a deterministic validator rather than by LLM "lint" or prose conventions. Versus auto-generated wikis (DeepWiki) and graph indexes (GraphRAG), Wiked trades full automation and corpus-scale retrieval for accountable, reviewable business meaning.

## Practices found

1. **LLM wiki (Karpathy, April 2026).** A gist proposes that the LLM "incrementally builds and maintains a persistent wiki" between the user and raw sources, in contrast to RAG where knowledge is "re-derived on every query"; "the wiki is a persistent, compounding artifact." Three layers: immutable raw sources ("the LLM reads from them but never modifies them"), an LLM-owned wiki, and a schema file (CLAUDE.md / AGENTS.md) that makes the LLM "a disciplined wiki maintainer rather than a generic chatbot." Operations: ingest, query (answers with citations, good answers filed back), lint (contradictions, stale claims, orphans, gaps). Navigation via `index.md` (read first) and an append-only `log.md`. Roles: "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else." The gist is explicitly abstract; it does not define per-claim provenance, a review workflow, or an open-questions mechanism (per my reading of the gist; the last ~6% of the page was not read). [1]
   - Reach claims (e.g. millions of views) come from secondary coverage and are unverified; do not cite figures. [2]
2. **Docs-as-code.** "Writing documentation with the same tools as code": issue trackers, Git, plain-text markup, code review, automated tests [3]; keep docs near code, repeatable builds, CI testing [4].
3. **Diátaxis.** Documentation organized around user needs into four forms (tutorials, how-to guides, reference, explanation), chosen by two axes: action vs. cognition and acquisition vs. application of skill [5][6].
4. **Agent instruction files.** AGENTS.md: "a simple, open format for guiding coding agents," stewarded by the Agentic AI Foundation under the Linux Foundation [7].
5. **Auto-generated code wikis (DeepWiki / Devin).** Indexes repos and "produces wikis with architecture diagrams, links to sources, and summaries"; steerable by `.devin/wiki.json` listing page titles/purposes. Official docs describe no human approval step for generated content [8]. Launch date and scale figures appear only in secondary sources (uncertain) [9].
6. **Knowledge graphs vs RAG (GraphRAG).** Microsoft Research argues "RAG fails on global questions directed at an entire text corpus" and builds an LLM-extracted entity graph with pre-generated community summaries, improving comprehensiveness/diversity on sensemaking questions over ~1M-token corpora [10].

## Convergence / divergence vs Wiked

| Dimension | Market practice | Wiked | Relation |
|---|---|---|---|
| Persistent compiled knowledge vs per-query RAG | LLM wiki compiles once, keeps current [1] | Persistent governed Markdown wiki in the consumer repo | Converges |
| Source layer | Raw sources immutable [1] | Ingested sources preserved; claims trace to them | Converges, stronger |
| Provenance | Query-time citations; no per-claim tracking [1]; DeepWiki links to code [8] | Every claim carries provenance to ingested sources | Diverges (stricter) |
| Who decides meaning | LLM does "everything else" [1]; DeepWiki fully automated [8] | Humans decide meaning via mandatory grill; agents structure | Diverges (core differentiator) |
| Schema | Free-form CLAUDE.md/AGENTS.md co-evolved [1][7] | Consumer-owned YAML Instance contract (page types, states, structured sections) | Converges in intent, diverges in formality |
| Quality checks | LLM "lint" (heuristic) [1]; docs-as-code automated tests [3][4] | Deterministic validator for structure; human review for meaning | Converges with docs-as-code, diverges from LLM-lint |
| Contradictions / gaps | Flagged at ingest/lint, no mechanism [1] | Explicit pendências and proposed-change sections linked to tickets | Diverges (explicit, auditable) |
| Tooling | Git, Markdown, review, issue trackers [3] | Git, Markdown, Knot tickets, review | Converges |
| Navigation | `index.md` read first [1] | Progressive index-based navigation, lazy loading | Converges |
| Content typing | Diátaxis user-need quadrants [5][6] | Contract-declared page types for business domain knowledge (not product docs) | Adjacent; Wiked is not a Diátaxis docs system |
| Scale / global questions | GraphRAG graph + community summaries [10] | Curated pages and trunks; no graph index | Different goal; complementary |
| Viewing | Obsidian as "IDE" [1]; DeepWiki site [8] | Optional Docsify viewer, Panorama and Curation dashboards | Converges; Curation panel of pending items is distinctive |

## Implications / key messages for an external value proposition

- **Name the lineage.** "Wiked is a governed, production-grade implementation of the LLM-maintained wiki pattern, built on docs-as-code." This anchors Wiked in a recognized, current idea and familiar engineering practice, lowering adoption friction.
- **Lead with accountability, not automation.** Market tools optimize for "the LLM does everything"; Wiked's message is "AI does the structuring, your experts own the meaning." Business buyers concerned with hallucination and liability should hear: every statement traces to a source, and every interpretation was confirmed by a person.
- **Make uncertainty visible.** Unlike wikis that silently smooth over gaps, Wiked turns open questions and proposed changes into tracked work items, with a Curation panel showing what is still pending. Frame this as "knowing what you don't know."
- **Deterministic, contract-based quality.** A declared contract plus validator means structure is checked the same way every time, not judged by another model.
- **Position against RAG/GraphRAG as complementary.** Retrieval answers questions over raw corpora; Wiked produces the vetted business-context layer that retrieval and analytical agents can consume. Avoid claiming superiority on corpus-scale questions.
- **Lives in your repo, no lock-in.** Plain Markdown in Git, consumer-owned contract, open AGENTS.md-style conventions.
- **Avoid:** claiming Wiked implements Diátaxis, quoting popularity numbers for Karpathy's gist, or overstating DeepWiki's lack of review (its docs are simply silent on it).

## Sources

1. Karpathy, "LLM Wiki" gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. Secondary coverage (unverified reach claims): https://www.implicator.ai/karpathys-llm-wiki-got-16-million-views-the-code-isnt-the-point-2/
3. Write the Docs, Docs as Code: https://www.writethedocs.org/guide/docs-as-code/
4. Docs Like Code: https://www.docslikecode.com/about/
5. Diátaxis: https://diataxis.fr/
6. Diátaxis compass: https://diataxis.fr/compass/
7. AGENTS.md: https://agents.md/
8. Devin docs, DeepWiki: https://docs.devin.ai/work-with-devin/deepwiki
9. Secondary on DeepWiki (uncertain dates/figures): https://huggingface.co/blog/lynn-mikami/deepwiki
10. Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization": https://arxiv.org/abs/2404.16130
