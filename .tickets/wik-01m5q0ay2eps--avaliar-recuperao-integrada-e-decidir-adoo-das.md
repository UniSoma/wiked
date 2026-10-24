---
id: wik-01m5q0ay2eps
title: Decidir a composição de recuperação e a suficiência das evidências
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-24T13:06:54.635498810Z'
updated: '2026-10-24T13:30:25.093236299Z'
parent: wik-01m5q079q8jz
tags:
- metodologia
- wiked
- projecoes
- evals
- recuperacao
- wayfinder:grilling
acceptance:
- title: Solicitante confirma composição e limites por classe de consulta, com inclusão/exclusão fundamentada das alternativas e ganho marginal considerado.
  done: false
- title: Evidência disponível é confrontada com critérios prévios; configurações não executadas, incertezas e limites de inferência são explicitados sem alegar implementação ou consistência inexistentes.
  done: false
- title: Questões impeditivas têm resolução em investigação/PoC apropriada antes da decisão; plano de validação futura distingue propriedades técnicas de comportamento agêntico.
  done: false
- title: Resposta e ativos são registrados no ticket e apenas indexados no mapa, deixando caminho claro para a especificação detalhada e sua aprovação separada.
  done: false
deps:
- wik-01m5q09kwfw9
- wik-01m17qfp6n6c
- wik-01m5q09kvwzm
links:
- wik-01m4vhpp3xyt
---

## Question

Quais mecanismos e comportamentos devem compor a especificação final de consulta, e as evidências disponíveis são suficientes para aprovar esse desenho ou exigem investigação adicional?

Confrontar contrato/critérios prévios, decisões sobre projeções e interface/protocolo com o baseline de navegação, mapa opcional e busca textual. Examinar ganho marginal e custo de orquestração das alternativas isoladas e combinadas quando houver evidência executável. Não exigir CLI produtiva ou implementação de capacidade rejeitada para decidir, nem contar configuração não executada como avaliada.

Avaliar descoberta, perguntas relacionais e transversais, exceções, lacunas, cobertura parcial, mudança/exclusão e indisponibilidade. Distinguir qualidade técnica de recuperação, comportamento observado do agente e expectativas ainda não testadas. Decidir inclusão, exclusão ou condicionantes das capacidades e o plano de validação da implementação futura. Se evidência insuficiente impedir uma escolha necessária, criar pergunta precisa de investigação/PoC e manter a decisão aberta; não transformar incerteza impeditiva em aprovação automática.

## Notes

Ticket wayfinder:grilling, HITL. A resolução é uma composição justificada para a especificação, não adoção operacional nem aceite de sistema entregue. A aprovação documental final pertence à decisão “Aprovar a especificação detalhada de recuperação para consulta no Wiked”. Antes de trabalhar, obter claim e invocar grilling e domain-modeling.

Desenho de comparação e orçamento são acordados na decisão inicial, antes das PoCs. Reutilizar cenários S1/S6 e infraestrutura compatível do esforço de avaliações comportamentais, sem pressupor sua implementação ou criar bloqueio obrigatório. Usar dados sintéticos; dados de consumidor e execuções agênticas precisam de autorização e limites explícitos.

Registrar evidências, versões, modelos/harness se aplicáveis, métricas, custo e incerteza. Distinguir exploração isolada, consistência medida, inconclusivo, infraestrutura e violação. Não executar agentes ou construir benchmark por organização de backlog.

Registrar resposta e links dos ativos em nota de resolução do Knot; fechar com resumo e indexar apenas nome/link e uma linha no mapa. No máximo um ticket não-research por sessão.