---
id: wik-01m7bckkqmn9
title: Restringir tipo ou tronco de destino em campos page de seções estruturadas
status: open
type: task
priority: 3
mode: hitl
created: '2026-11-13T21:21:52.364497087Z'
updated: '2026-11-13T21:21:52.364497087Z'
tags:
- metodologia
- wiked
- melhoria
acceptance:
- title: Grill metodológico decide escopo e compatibilidade com legado
  done: false
links:
- wik-01m7at8mpxn6
---

## Description

Lacuna do caso consultivo (UC2). Hoje um campo `page` de seção estruturada aceita link para qualquer página: no protótipo, o campo Rules de um processo aceitou um link para um papel sem diagnóstico.

Propósito: permitir que o Instance contract declare, opcionalmente, os page types ou troncos de destino aceitos por campo `page`, além de uma flag nullable explícita.

Escopo: opção no contrato, diagnóstico no Distributed validator, regressões sintéticas. Opcional e sem quebrar contratos existentes.

Insumos: documento 'Protótipo: Instance contract de referência para mapeamento consultivo' (wik-01m7at8mcfp3-d1k8n), lacuna 1.
