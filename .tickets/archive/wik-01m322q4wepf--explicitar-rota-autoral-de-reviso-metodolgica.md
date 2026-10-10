---
id: wik-01m322q4wepf
title: Explicitar rota autoral de revisão metodológica somente de leitura
status: closed
type: task
priority: 3
mode: hitl
created: '2026-09-21T13:33:05.249244194Z'
updated: '2026-10-10T21:12:49.778441203Z'
closed: '2026-10-10T21:12:49.778441203Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
- contexto
acceptance:
- title: A entrada autoral distingue revisão somente de leitura de criação ou alteração de conteúdo governado
  done: true
- title: A revisão somente de leitura não carrega nem exige a skill externa de grilling quando o grill está dispensado
  done: true
- title: Verificações textuais cobrem revisão e edição e preservam o isolamento entre autoria e operação
  done: true
---

## Description

Separar explicitamente a revisão metodológica somente de leitura da edição de conteúdo governado nas entradas autorais. A rota de revisão não deve carregar nem exigir a skill externa de grilling quando o grill estiver dispensado; qualquer edição continua sujeita ao workflow metodológico e ao fechamento do grill. Contexto histórico: a compressão das instruções foi concluída e esta distinção autoral foi adiada para um trabalho próprio. A extração preserva a política existente e não resolve antecipadamente este refinamento.

## Notes

**2026-10-10T18:40:30.416467924Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-10T21:11:57.747486525Z**

Methodological grill closed with explicit requester confirmation ("de acordo") on 2026-10-10. Authorized objective: distinguish read-only methodological review from governed content changes in AGENTS.md, docs/metodologia.md, and README.md. Read-only review requires no ticket and neither loads nor requires grilling, except when the requester asks to qualify the objective. Governed changes, including changes arising from review, require an approved open ticket and explicit grill closure before editing. Validation: targeted textual checks for ordinary review, requested qualification, transition to editing, links, English instructions, and source/consumer isolation. No lateral issues incorporated.

**2026-10-10T21:12:43.488990812Z**

Implemented the approved routing in AGENTS.md, docs/metodologia.md, and README.md. Targeted textual checks passed with Node.js: ticket-free read-only review, no grilling load/requirement for ordinary review, requested-qualification exception, review allowed without the skill, transition to governed editing with an approved open ticket and explicit grill closure, local Markdown links, ASCII generic instructions, explicit requester confirmation, source/consumer isolation, and no docs/ dependency in distributed Markdown. Manual scenario review confirms qualification alone does not authorize editing and the governed-change sequence follows request classification. An initial Ruby check could not execute because Ruby is unavailable; the checks were executed successfully with the existing Node.js runtime. No Python or test changes; instruction-only validation route used.

**2026-10-10T21:12:49.778441203Z**

Implemented the requester-approved read-only methodological review route in AGENTS.md, docs/metodologia.md, and README.md. Ordinary review requires neither a ticket nor loading grilling; requested qualification retains the grill exception; governed edits require an approved open ticket and explicit grill closure. All three acceptance criteria satisfied through targeted textual checks, with evidence recorded.
