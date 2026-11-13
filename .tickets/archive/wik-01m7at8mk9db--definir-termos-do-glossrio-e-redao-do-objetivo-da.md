---
id: wik-01m7at8mk9db
title: Definir termos do glossário e redação do objetivo da metodologia
status: closed
type: chore
priority: 2
mode: hitl
created: '2026-11-13T16:01:18.441680361Z'
updated: '2026-11-13T21:50:07.889682431Z'
closed: '2026-11-13T21:50:07.889682431Z'
parent: wik-01m7at81hnsd
tags:
- wayfinder-grilling
deps:
- wik-01m7at8mfwtv
---

## Description

### Question

Quais termos entram no GLOSSARY.md (casos de uso, visão derivada, artefato derivado, data source × Source, pedido do cliente, ponto de curadoria) e como o Objective de docs/metodologia.md passa a reconhecer os casos de uso?

## Notes

**2026-11-13T21:50:07.763800663Z**

Resolução (grill com o requisitante, 2026-11-13; todas as recomendações aceitas). Aplicação no ticket "Escrever a proposta e ajustar o objetivo e o glossário".

GLOSSARY.md:
1. Nova seção `### Purpose and use cases` com **Use case** (genérico) e os quatro casos: **Knowledge base** (_Avoid_: team wiki, documentation), **Consulting mapping** (_Avoid_: process mapping, as-is mapping), **Agent-navigable business context** (_Avoid_: RAG, semantic layer), **Derived artifact production** (_Avoid_: export). Distinção principal × consequência fica no Objective, não no glossário.
2. **Derived view**: projeção de leitura regenerável de uma wiki de consumidor (ex.: mapa de navegação, painel de curadoria), nunca Operational evidence. **Derived artifact**: documento ou diagrama gerado de conteúdo validado, nunca Operational evidence. Sem citar Panorama/Curadoria (nomes da instância de referência; a proposta pode citá-los como exemplos dela).
3. **Source page**: página de proveniência de uma fonte primária (_Avoid_: "source" isolado). "data source" é domínio do consumidor e não entra; a distinção é explicada em prosa na proposta.
4. Pedido do cliente: não entra agora; entra quando "Controlar visibilidade por item na sincronização com plataformas externas" for implementado.
5. Ponto de curadoria: não entra; coberto por Derived view sobre pendências e propostas existentes.

docs/metodologia.md (Objective): um parágrafo após o primeiro, curto, sem maturidade nem funcionalidades, nos moldes de:
"Wiked serves two main use cases, a Knowledge base for an area, project, or product and Consulting mapping of processes, rules, data sources, tools, stakeholders, and gaps, and supports two that follow from them: Agent-navigable business context and Derived artifact production. The Instance contract sets the rigor each use case requires; derived views and artifacts never become Operational evidence."
Redação final ajustável no ticket de escrita.

**2026-11-13T21:50:07.889682431Z**

Glossário ganha seção de casos de uso (Use case + quatro casos), Derived view, Derived artifact e Source page; pedido do cliente e ponto de curadoria ficam fora; Objective ganha um parágrafo curto reconhecendo os casos de uso e o rigor via Instance contract.
