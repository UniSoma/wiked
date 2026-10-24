---
id: wik-01m5q082jdqm
title: Definir contrato mínimo e critérios de avaliação da recuperação para consulta
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-24T13:05:20.973227285Z'
updated: '2026-10-24T13:30:24.984862910Z'
parent: wik-01m5q079q8jz
tags:
- metodologia
- wiked
- projecoes
- contrato
- wayfinder:grilling
acceptance:
- title: Solicitante confirma explicitamente a decisão sobre contrato mínimo, fronteiras, alternativas consideradas e limites, sem tratá-la como implementação.
  done: false
- title: Critérios, baseline, gabarito, métricas e limites de custo/execução são definidos antes das PoCs e distinguem recuperação técnica de comportamento do agente.
  done: false
- title: A resposta explicita rastreabilidade, cobertura, revisão, falhas e preservação da autoridade do Markdown; exemplos não introduzem domínio de consumidor na metodologia.
  done: false
- title: Decisão e ativos são registrados no ticket; mapa recebe apenas síntese e ponteiro, e questões adicionais precisas ou névoa são encaminhadas sem execução implícita.
  done: false
links:
- wik-01m2tpkz9x55
---

## Question

Qual é o contrato mínimo necessário para comparar alternativas de recuperação para consulta no Wiked, e quais evidências, métricas e limites permitirão decidir se elas melhoram o baseline atual?

Decidir elegibilidade do corpus pelo contrato da instância, identificação de páginas/seções/ocorrências, rastreabilidade à revisão canônica, distinção entre sinais de recuperação, cobertura e estados de falha, e fronteira entre consulta somente leitura e construção de projeções. Definir apenas o suficiente para os experimentos: não escolher uma arquitetura geral de plugins ou a implementação definitiva antes das evidências.

A resposta deve fixar classes de perguntas, gabarito de Markdown necessário e lacunas, baseline com índices/mapa opcional/busca textual, critérios de comparação e orçamento. Considerar paráfrases, termos exatos, perguntas relacionais/transversais, exceções, ausência de resposta e conteúdo alterado. Separar qualidade da recuperação e cumprimento do protocolo pelo agente. A escolha final das capacidades pertence às decisões posteriores, não a este ticket.

## Notes

Ticket wayfinder:grilling, HITL. Esta é a fronteira inicial do mapa: critérios devem anteceder PoCs. Antes de trabalhar, obter claim por assignee e invocar grilling e domain-modeling. Investigações factuais ficam com o agente; decisões e confirmação ficam com o solicitante.

Markdown é a fonte da verdade para humanos e agentes. Similaridade sugere candidatos, não identidade ou relação operacional; nenhum sinal de recuperação é evidência autônoma. Preservar carregamento progressivo e contratos genéricos, sem consumidor obrigatório.

A resposta é uma decisão com justificativa e exemplos suficientes para os próximos tickets, não contrato/runtime implementado. Se descobrir necessidade de pesquisa externa ou PoC, especificar a pergunta e criar ticket research ou prototype apropriado antes de executar. Alterações de conteúdo governado exigem grill autoral fechado; esta reorganização não o substitui.

Na resolução, registrar resposta e ativos por nota no Knot, fechar com resumo e acrescentar ao mapa apenas ponteiro pelo nome e síntese de uma linha. Não resolver outros tickets não-research na mesma sessão.