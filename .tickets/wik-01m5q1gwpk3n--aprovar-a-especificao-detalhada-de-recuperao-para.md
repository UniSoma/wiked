---
id: wik-01m5q1gwpk3n
title: Aprovar a especificação detalhada de recuperação para consulta no Wiked
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-24T13:27:38.438201017Z'
updated: '2026-10-24T13:31:09.556542025Z'
parent: wik-01m5q079q8jz
tags:
- metodologia
- wiked
- projecoes
- wayfinder:grilling
acceptance:
- title: Especificação detalhada vinculada ao ticket é coerente com as decisões resolvidas e distingue requisitos, exclusões, limitações e evidências exploratórias.
  done: false
- title: Não resta decisão substantiva necessária para formalizar a implementação; decisões descobertas na consolidação foram resolvidas em tickets próprios, sem suposições silenciosas.
  done: false
- title: Solicitante aprova explicitamente a especificação final e seus limites; a aprovação não é apresentada como implementação entregue ou adoção operacional.
  done: false
- title: Resolução e ativos são registrados no ticket, com síntese e ponteiro no mapa; o próximo esforço de implementação é separado do encerramento deste mapa.
  done: false
deps:
- wik-01m5q0ay2eps
---

## Question

Que especificação detalhada de recuperação para consulta representa as decisões deste mapa e pode ser explicitamente aprovada pelo solicitante como base suficiente para formalizar a implementação separadamente?

A especificação deve ligar requisitos, interfaces e comportamentos às decisões que os justificam, distinguindo escolhas aprovadas, capacidades rejeitadas, limitações e hipóteses não comprovadas. Deve detalhar corpus e fronteiras de evidência, contrato de resultados e identidade, ciclo das projeções selecionadas, CLI, protocolo de uso pelo agente, compatibilidade, falhas/fallback, critérios de validação e plano de implementação separado. Detalhar não significa escolher uma tecnologia desnecessária: exclusões deliberadas também fazem parte da especificação.

A resolução é a aprovação humana explícita da especificação, não a entrega da CLI nem a adoção operacional de uma projeção. Se a consolidação revelar decisão substantiva ainda aberta, encaminhá-la a ticket próprio e manter esta aprovação bloqueada até a resolução; não preencher lacunas silenciosamente.

## Notes

Ticket wayfinder:grilling, HITL, do mapa “Especificar projeções e recuperação unificada para consulta no Wiked”. Antes de trabalhar, obter claim por assignee e invocar grilling e domain-modeling. Ler o mapa de baixa resolução e ampliar apenas decisões pertinentes. Especificação é conteúdo governado: sua autoria exige o Methodological grill aplicável, com confirmação explícita do entendimento compartilhado antes de escrever. Este registro de backlog não fecha esse grill nem fixa o caminho do documento.

Se necessário, criar trabalho decisório adicional apenas quando a pergunta puder ser formulada com precisão. Não executar implementação oficial, alterar skill instalada nem operar consumidor real por implicação. Ativos da especificação ficam ligados ao ticket, não colados no mapa.

Ao resolver: registrar resposta, aprovação e links dos ativos por nota de resolução do Knot; satisfazer os critérios aplicáveis; fechar com resumo; acrescentar ao mapa apenas nome, link e síntese de uma linha. No máximo um ticket não-research é resolvido por sessão. A implementação será formalizada em esforço separado após o destino alcançado.