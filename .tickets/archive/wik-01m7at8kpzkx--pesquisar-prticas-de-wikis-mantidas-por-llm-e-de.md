---
id: wik-01m7at8kpzkx
title: Pesquisar práticas de wikis mantidas por LLM e de docs-as-code
status: closed
type: chore
priority: 2
mode: afk
created: '2026-11-13T16:01:17.535811179Z'
updated: '2026-11-13T16:03:36.214565723Z'
closed: '2026-11-13T16:03:36.214565723Z'
parent: wik-01m7at81hnsd
tags:
- wayfinder-research
---

## Description

### Question

Que práticas de mercado (padrão LLM wiki, docs-as-code, Diátaxis, gestão de conhecimento com IA) posicionam o núcleo do Wiked, e onde ele converge ou diverge delas?

## Notes

**2026-11-13T16:03:36.080334205Z**

O Wiked é uma implementação governada do padrão LLM wiki de Karpathy (fontes imutáveis, wiki persistente, schema, ingest/query/lint, index.md) sobre práticas docs-as-code (Git, Markdown, revisão, tickets, testes). Diverge onde o mercado é omisso: significado decidido por humanos via grill, proveniência por afirmação, pendências e propostas explícitas ligadas a tickets, e contrato com validador determinístico. Frente a DeepWiki (geração automática) e GraphRAG (índice em grafo), troca automação total e escala por significado auditável; é complementar a RAG, não Diátaxis.

**2026-11-13T16:03:36.214565723Z**

Wiked posicionado como LLM wiki governado sobre docs-as-code, com diferenciais de grill humano, proveniência, pendências explícitas e validação determinística.
