---
id: wik-01m7bckkvp2b
title: Exigir vínculo inverso e cobertura de vínculos entre páginas
status: open
type: task
priority: 3
mode: hitl
created: '2026-11-13T21:21:52.494053236Z'
updated: '2026-11-13T21:21:53.620503990Z'
tags:
- metodologia
- wiked
- melhoria
acceptance:
- title: Grill metodológico decide escopo e compatibilidade com legado
  done: false
links:
- wik-01m7at8mpxn6
- wik-01m2v2rbjgng
---

## Description

Lacuna do caso consultivo (UC2). Se uma regra diz 'Applies to: Order intake' e o processo deixa de citar a regra, nada é diagnosticado; também não há checagem de cobertura (etapa sem responsável fora de cardinalidade, requisito ou etapa órfãos).

Propósito: flag opcional de link-back no campo `page`, exigindo que a página de destino cite a origem (qualquer citação), e avaliar critérios de cobertura computáveis sobre vínculos.

Escopo: opção no contrato e diagnóstico estrutural no validador; separar de heurísticas textuais (ver ticket ligado de verificações heurísticas). Opcional e sem quebrar legado.

Insumos: protótipo UC2 (wik-01m7at8mcfp3-d1k8n), lacuna 2; pesquisa de mapeamento de processos e requisitos (wik-01m7at8ktmre), critérios de completude como cobertura de links.
