---
id: wik-01m5q079q8jz
title: Especificar projeções e recuperação unificada para consulta no Wiked
status: open
type: epic
priority: 2
mode: hitl
created: '2026-10-24T13:04:55.528425755Z'
updated: '2026-10-24T13:28:40.053406714Z'
tags:
- metodologia
- wiked
- projecoes
- recuperacao
- arquitetura
- wayfinder:map
acceptance:
- title: Decisões necessárias à especificação estão resolvidas em seus tickets e indexadas por nome no mapa, sem duplicação de conteúdo decisório.
  done: false
- title: Não restam filhos decisórios abertos nem névoa necessária para o destino; trabalho fora de escopo permanece explicitamente separado, sem requisitos de implementação indevidos.
  done: false
- title: Especificação detalhada está vinculada à decisão final e explicitamente aprovada pelo solicitante, permitindo formalizar a implementação separadamente.
  done: false
---

## Destination

Chegar a uma especificação detalhada, explicitamente aprovada pelo solicitante, de projeções derivadas e recuperação unificada para consulta no Wiked, apoiada por investigação e PoCs quando necessárias. O mapa termina quando não resta decisão necessária para formalizar a implementação em esforço separado; não exige entregar o sistema.

## Notes

Mapa de planejamento segundo Wayfinder, mantido no Knot. Consultar as skills wayfinder, knot, grilling e domain-modeling conforme a sessão. Esta reorganização e o destino foram confirmados pelo solicitante em 2026-10-24; não constituem fechamento de grills técnicos ou autorização de implementação.

Markdown canônico é a fonte da verdade, acessível a humanos e agentes. Projeções apenas localizam conteúdo; respostas exigem leitura do Markdown. Preservar consulta somente leitura, carregamento progressivo, corpus elegível pelo contrato e distinção entre ausência de resultado e ausência de informação. Estes são limites de partida, não decisões técnicas resolvidas neste mapa.

Preferência de esforço: vetorial/híbrida P2 antes da relacional P3, sem dependência técnica artificial entre elas; demais decisões P2. Índices, mapa de intenções e busca textual existentes são baseline, não entregas a reconstruir. PoCs são opcionais, delimitadas e exploratórias; não são implementação oficial nem prova de consistência por execução isolada. Orçamento, dados autorizados, ambiente e critério de encerramento precisam ser aprovados antes da execução. Não há exceção que traga a implementação definitiva para dentro do mapa.

O mapa é índice, não repositório de decisões ou lista de tarefas abertas. Consultar os filhos abertos e suas dependências nativas para encontrar a fronteira. No Knot, usar tags wayfinder:map e wayfinder:grilling|research|prototype|task; parent define filhos e deps define bloqueios. Fronteira: filhos abertos, com todos os bloqueadores fechados e sem assignee. Atribuição é claim: atribuir antes de trabalhar, preservando claims existentes e sem assumir a fala do humano. A atribuição preexistente da decisão relacional foi mantida; esta reorganização não reivindica nem resolve tickets.

Referir-se a mapa e tickets por seus nomes, com links quando disponíveis. Em resolução, registrar resposta e ativos por nota no ticket e fechamento com resumo via Knot; no mapa acrescentar somente link pelo nome e uma linha de síntese. Não duplicar a decisão no mapa. Não resolver mais de um ticket por sessão, exceto research. Criar perguntas recém-especificáveis antes de ligar bloqueios; não pré-fatiar a névoa. Ao trabalhar, reconsultar estado e claims para respeitar sessões concorrentes.

Cada ticket decisório mantém seu próprio grill e critérios. Grilling requer grilling e domain-modeling; registrar termos e decisões na conversa/Knot até a autorização para conteúdo governado. PoCs que alterem código/instruções também exigem a governança autoral aplicável. Não manipular Git, instalar ferramentas ou substituir skill em execução. Ainda não há pesquisa externa especificada nem agentes de research a disparar nesta sessão de organização.

## Decisions so far

Nenhum ticket decisório resolvido neste mapa. Pesquisa histórica e reorganização do backlog não são decisões de arquitetura ou adoção.

## Not yet specified

Experimentos adicionais que as primeiras decisões mostrarem necessários para distinguir alternativas; sua pergunta, fidelidade e dados ainda dependerão das lacunas de evidência encontradas.

Detalhes de projeto que só se tornem necessários após escolher as capacidades e conhecer seus limites; novas perguntas devem nascer das evidências, sem presumir desde já motores, persistência, provedores ou composição de projeções. As perguntas gerais de contrato, avaliação das duas projeções, CLI/protocolo, comparação integrada e aprovação já são filhos e não pertencem a esta névoa.

## Out of scope

Implementação oficial, entrega de CLI produtiva, instalação/distribuição de capacidades, migração ou adoção operacional. Serão formalizadas após a especificação aprovada, em esforço separado.

Integração das projeções aos fluxos de indexação assistida, grill e manutenção; considerar apenas fronteiras que evitem bloquear evolução futura, sem projetar esses fluxos neste mapa.

Aplicativo Pi, arquitetura geral de skills opcionais, heurísticas de manutenção editorial e alterações em tickets já encerrados. Não são pré-requisitos implícitos. Operação de consumidor real, uso de dados ou envio a serviços externos exige autorização própria.