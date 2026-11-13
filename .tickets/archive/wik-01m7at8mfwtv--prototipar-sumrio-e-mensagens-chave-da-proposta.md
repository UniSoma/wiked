---
id: wik-01m7at8mfwtv
title: Prototipar sumário e mensagens-chave da proposta de valor
status: closed
type: chore
priority: 2
mode: hitl
created: '2026-11-13T16:01:18.332138290Z'
updated: '2026-11-13T21:04:48.128202674Z'
closed: '2026-11-13T21:04:48.128202674Z'
parent: wik-01m7at81hnsd
tags:
- wayfinder-prototype
deps:
- wik-01m7at8kkdae
- wik-01m7at8kpzkx
- wik-01m7at8m1h4p
- wik-01m7at8m556c
- wik-01m7at8m8p16
- wik-01m7at8mcfp3
---

## Description

### Question

Qual estrutura e quais mensagens-chave a proposta deve ter (problema, núcleo, capacidades, casos de uso, maturidade, como um projeto funciona com o Wiked, comparação com mercado, limitações)?

## Notes

**2026-11-13T17:01:01.284548973Z**

Mensagem-chave indicada pelo requisitante: o rigor do protocolo é configurável no Instance contract (dos requisitos mínimos a regras fortes de relacionamento), o que habilita casos de uso distintos; o custo de curadoria cresce com o rigor, e wikis com muitas regras de relacionamento exigem grills mais rígidos. Ver Notes do mapa.

**2026-11-13T21:04:48.006477652Z**

Resolução (protótipo validado com o requisitante):
- Estrutura aceita: pitch + cinco mensagens-chave (significado decidido por pessoas; toda afirmação com fonte; indefinição explícita ligada a tickets; estrutura verificada; rigor configurável) → problema → o que é → núcleo em cinco pilares com maturidade → rigor configurável (seção própria) → casos de uso → como um projeto funciona → comparação com mercado (tabela) → maturidade → limitações → mantenedora.
- UC2 é a seção mais longa; UC1 também bem explorado, como caso de uso fundador da metodologia (base de conhecimento de área na instância de referência).
- Mensagem nova do requisitante: vantagem sobre RAG em fontes cruas (ex.: notebooks tipo NotebookLM/Gemini) — nada garante consistência; conflitos e ambiguidades chegam ao agente, que interpreta na consulta; no Wiked o conflito é resolvido uma vez, com uma pessoa, antes da leitura. Vantagem sobre agentes de plataformas de dados (ex.: Databricks Genie): o contexto de negócio deles vem de metadados do Unity Catalog, de knowledge store restrito ao space (descrições, sinônimos, joins, expressões SQL) e de instruções em texto (até 100), ancorados em tabelas/colunas; o Wiked carrega processos, regras, papéis, lacunas e decisões ligados às entradas do catálogo nos troncos. Verificado nas docs Databricks (docs.databricks.com/aws/genie/set-up, /genie/knowledge-store): a afirmação do requisitante se confirma com nuance — há contexto textual além das colunas, mas restrito ao space, sem proveniência por afirmação. Local: UC3 e tabela de comparação.
- Limitações: validador garante a forma, não a verdade.
- Sem modelo comercial; fechamento convida a conversa.
Protótipo: documento anexo 'Protótipo: sumário e mensagens-chave da proposta de valor'.

**2026-11-13T21:04:48.128202674Z**

Estrutura e cinco mensagens-chave validadas; UC2 mais longo e UC1 desenvolvido como caso fundador; vantagem sobre RAG cru e agentes de plataformas de dados no UC3 e na comparação; sem modelo comercial.
