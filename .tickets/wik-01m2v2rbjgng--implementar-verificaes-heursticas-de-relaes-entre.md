---
id: wik-01m2v2rbjgng
title: Implementar verificações heurísticas de relações entre páginas no Wiked
status: open
type: feature
priority: 3
mode: hitl
created: '2026-09-18T20:19:03.859967985Z'
updated: '2026-10-24T13:08:04.316154815Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
acceptance:
- title: Grill metodológico decide escopo, opcionalidade e tratamento de falsos positivos
  done: false
- title: Heurísticas implementadas sem idioma ou domínio fixo, ou rejeitadas com decisão registrada
  done: false
- title: Regressões cobrem títulos duplicados, texto sem link e link semanticamente desviado
  done: false
links:
- wik-01m17qfp6n6c
---

## Description

Melhoria futura não bloqueante da fase 1. Decidir e implementar, se o benefício justificar os falsos positivos, equivalentes genéricos de unlinked-known-page e misdirected-known-page. As regras devem ser opcionais, independentes de idioma e separadas das garantias estruturais de referência. Não reintroduzir heurísticas no núcleo v1 sem grill metodológico e desenho explícito de configuração, severidade e casos de ambiguidade.

Contexto histórico suficiente: a primeira distribuição deixou as heurísticas fora do núcleo. Sua ausência não é regressão; o benefício e os falsos positivos precisam ser qualificados neste trabalho.

## Notes

**2026-10-10T18:40:26.195816261Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-24T13:07:59.337894411Z**

Reorganização autorizada do backlog em 2026-10-24: o épico wik-01m5q079q8jz reúne recuperação e projeções; seu piloto relacional é wik-01m17qfp6n6c. Este ticket permanece fora do épico, com objetivo de diagnóstico e manutenção editorial, sem nova dependência ou mudança de prioridade. Pode reutilizar identidades/ocorrências e infraestrutura aprovadas, mas heurísticas não geram relações operacionais autoritativas nem entram implicitamente no protocolo de consulta.
