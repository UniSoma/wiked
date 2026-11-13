---
id: wik-01m7at8mpxn6
title: Consolidar lacunas do caso consultivo em tickets de melhoria
status: closed
type: chore
priority: 2
mode: afk
created: '2026-11-13T16:01:18.557378735Z'
updated: '2026-11-13T21:22:12.492490863Z'
closed: '2026-11-13T21:22:07.850251986Z'
parent: wik-01m7at81hnsd
tags:
- wayfinder-task
deps:
- wik-01m7at8mcfp3
- wik-01m7at8mfwtv
links:
- wik-01m7bckkqmn9
- wik-01m7bckkvp2b
- wik-01m7bckm03pa
- wik-01m7bckm4dhz
- wik-01m7bckm8m0v
- wik-01m7bckmcz4g
- wik-01m7bckmh8mq
- wik-01m7bckmnmk8
---

## Description

### Question

Quais lacunas surgidas no mapa viram tickets de melhoria próprios (com propósito, escopo e anexos relevantes), fora do destino?

## Notes

**2026-11-13T16:59:38.485581809Z**

Insumo do protótipo do contrato UC2 (wik-01m7at8mcfp3): lacunas 1) tipo/tronco de destino em campos page (+ flag nullable); 2) link-back opcional exigindo citação inversa; 3) to-be via seção estruturada opcional ligando processos, restrita por tipo; 4) proposal_tracking exige estado de proposta em todos os tipos do papel. Caminhos sugeridos pelo requisitante são opcionais e não quebram legado.

**2026-11-13T21:22:07.724606371Z**

Resolução: lacunas consolidadas em oito tickets de melhoria avulsos (fora do mapa, hitl, tags metodologia/wiked/melhoria, ligados a este ticket):
1) wik-01m7bckkqmn9 Restringir tipo ou tronco de destino em campos page de seções estruturadas (lacuna 1 do protótipo UC2).
2) wik-01m7bckkvp2b Exigir vínculo inverso e cobertura de vínculos entre páginas (lacuna 2 + checagem de cobertura; ligado ao ticket de heurísticas wik-01m2v2rbjgng).
3) wik-01m7bckm03pa Vincular processos as-is e to-be e comparar lado a lado (lacuna 3; depende de 1).
4) wik-01m7bckm4dhz Flexibilizar o estado de proposta exigido por proposal_tracking (lacuna 4, sem caminho definido).
5) wik-01m7bckm8m0v Registrar supersessão, decisores e cadência de revisão de pendências.
6) wik-01m7bckmcz4g Controlar visibilidade por item na sincronização com plataformas externas.
7) wik-01m7bckmh8mq Modelar requisitos rastreados com estados de maturidade (BABOK).
8) wik-01m7bckmnmk8 Orientar entrevistas e workshops e divergência entre entrevistados.
Não viraram tickets: A = R no RACI (erro de modelagem do protótipo, não lacuna do Wiked); modelo de referência/template oficial e implementação dos painéis/visões agregadas (já fora de escopo no mapa); data source × Source (resolvido como distinção terminológica no glossário).

**2026-11-13T21:22:07.850251986Z**

Lacunas do UC2 consolidadas em oito tickets de melhoria avulsos ligados a este ticket; A = R, template oficial e painéis não viraram tickets.

**2026-11-13T21:22:12.492490863Z**

Correção: data source × Source não está resolvido ainda; fica a cargo do ticket do mapa 'Definir termos do glossário e redação do objetivo da metodologia' (wik-01m7at8mk9db), por isso não virou ticket avulso.
