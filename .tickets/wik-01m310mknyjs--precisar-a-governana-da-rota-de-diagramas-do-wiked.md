---
id: wik-01m310mknyjs
title: Precisar a governança da rota de diagramas do Wiked
status: open
type: task
priority: 3
mode: hitl
created: '2026-09-21T03:37:30.558065496Z'
updated: '2026-10-10T18:40:28.451016281Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
- diagrama
acceptance:
- title: Grill metodológico encerrado com decisão explícita sobre criação, ajuste visual, regeneração e exportação temporária
  done: false
- title: Rotas e guias tornam explícitos os pré-requisitos de governança e as exceções aprovadas, sem inferir autorização da ausência de mudança semântica
  done: false
- title: Verificações textuais percorrem os cenários e confirmam coerência, carga seletiva e ausência de dependências de domínio
  done: false
---

## Description

### Constatação
A avaliação metodológica identificou que o roteador encaminha criação, revisão e renderização diretamente ao guia D2. O invariante geral exige grill antes de alterar conteúdo governado, mas o guia explicita o retorno ao grill apenas para correções com escolha semântica. A aplicação da regra a criação, ajustes visuais, regeneração e exportação temporária depende de interpretação.
### Entrega
Conduzir grill metodológico e tornar inequívoco o percurso de cada classe de operação, incluindo qualificação humana, fechamento do grill e eventuais exceções aprovadas. Harmonizar roteador, D2, grill e exportação sem alterar conteúdo de uma instância. A regra global existe; o objetivo é fechar seu encadeamento, não pressupor uma autorização ausente.
### Independência
Melhoria genérica avulsa, não pré-requisito da extração ou publicação. O registro não encerra o grill nem aprova antecipadamente exceções. Executar na origem canônica vigente do Wiked.

## Notes

**2026-10-10T18:40:28.451016281Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.
