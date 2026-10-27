---
id: wik-01m5zb67c010
title: Definir na distribuição o vocabulário de contrato e validador necessário à instalação
status: open
type: task
priority: 3
mode: hitl
created: '2026-10-27T18:50:30.142672260Z'
updated: '2026-10-27T18:50:32.697927607Z'
links:
- wik-01m5z64vwzy0
---

## Description

Lateral de wik-01m5z64vwzy0. O que uma instalação precisa saber deve estar definido em distr/agents; o agente consumidor só enxerga a skill. Hoje distr/ usa "local contract" (guides/docsify.md, maintenance.md, setup.md), "the contract" e "distributed validator" sem defini-los explicitamente; scripts/README.md:11 usa "consumer contract", e scripts/install-wiked.sh:635 imprime "consumer contract" ao consumidor. Verificar se a distribuição define esses termos e uniformizá-los, incluindo a mensagem do instalador. Mudança em distr/ exige decisão de versão e declaração no CHANGELOG distribuído (docs/distribution.md). README.md e docs/installation.md seguem o vocabulário voltado ao consumidor.
