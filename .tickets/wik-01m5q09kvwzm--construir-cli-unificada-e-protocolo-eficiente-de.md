---
id: wik-01m5q09kvwzm
title: Definir a interface da CLI e o protocolo de recuperação para agentes
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-24T13:06:11.442276799Z'
updated: '2026-10-24T13:31:14.869338386Z'
parent: wik-01m5q079q8jz
tags:
- metodologia
- wiked
- projecoes
- cli
- navegacao
- wayfinder:grilling
acceptance:
- title: Solicitante confirma a interface e o protocolo propostos, com justificativa das alternativas, exemplos representativos e comportamento das capacidades ausentes ou rejeitadas.
  done: false
- title: Desenho cobre seleção/combinação, leitura canônica, limites, expansão, parada, cobertura e falhas sem execução ou carregamento indiscriminados.
  done: false
- title: Contrato técnico e integração lazy à skill ficam suficientemente detalhados para a especificação, preservando compatibilidade, consulta somente leitura e fronteira reutilizável.
  done: false
- title: Ativos exploratórios necessários estão vinculados e distinguíveis da implementação oficial; decisão é registrada no ticket e apenas indexada no mapa.
  done: false
deps:
- wik-01m5q082jdqm
- wik-01m5q09kwfw9
- wik-01m17qfp6n6c
links:
- wik-01m4k2eg642n
---

## Question

Qual interface de CLI e qual protocolo de uso permitem ao agente localizar e ler o Markdown necessário com eficiência, combinando navegação existente e apenas as projeções escolhidas para a especificação?

Decidir operações, argumentos, envelopes e erros; raiz e compatibilidade; descoberta de capacidades/cobertura; manifesto explicável e deduplicação; separação de consulta e construção/manutenção. Definir como o agente escolhe estratégia, confirma entidades, combina ou troca mecanismos, expande contexto, lê condições/exceções, limita resultados/páginas/saltos/tokens e encerra com limitações. Não pressupor comando opaco, escada fixa ou execução de todos os mecanismos em toda pergunta.

Decidir a integração lazy à skill e o comportamento sem capacidades opcionais, mantendo fonte da verdade canônica, consulta somente leitura e fronteira reutilizável pelo eventual produto local. Nome/empacotamento e exemplos de interface são itens a decidir, não permissão para construir a CLI definitiva.

## Notes

Ticket wayfinder:grilling, HITL. Consome contrato mínimo e escolhas das projeções; seus bloqueios nativos serão ligados após criação dos tickets. Antes de trabalhar, obter claim e invocar grilling e domain-modeling. Refinar interface por esboços ou exemplos; se uma PoC for indispensável, abrir prototype delimitado e ligá-lo antes de executar. Não realizar marcos de entrega de CLI produtiva neste mapa.

Implementação do produto Pi, comandos de escrita/autorização/journal e arquitetura geral de skills não fazem parte da resposta. Preservar compatibilidade e autoridade do runtime vigente; não criar segunda validação normativa. Guias definitivos, distribuição e instalação serão trabalhos executores após a especificação aprovada.

A resolução é o desenho aprovado, com justificativa e links para ativos, não código entregue. Registrar resposta em nota do Knot e fechamento com resumo; mapa recebe apenas nome/link e síntese de uma linha. No máximo um ticket não-research resolvido por sessão. Alterações governadas de qualquer PoC dependem do grill autoral aplicável.