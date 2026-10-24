---
id: wik-01m2tpkz9x55
title: Definir arquitetura de skills opcionais do Wiked
status: open
type: task
priority: 3
mode: hitl
created: '2026-09-18T16:46:57.314059743Z'
updated: '2026-10-24T13:08:04.318841697Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- arquitetura
acceptance:
- title: Grill decide fronteira da skill obrigatória e contrato de composição das opcionais
  done: false
- title: Descoberta, dependências, versões e propriedade de arquivos definidas sem variantes customizadas
  done: false
- title: D2, exportação e storages examinados com migração compatível e limites de evidência
  done: false
- title: Decisões e trabalhos futuros registrados; migração completa não depende desta melhoria
  done: false
deps:
- wik-01m4khsrmqya
links:
- wik-01m5q082jdqm
---

## Description

Melhoria genérica independente, após primeira publicação Wiked. Conduzir grill para decompor capacidades em skills independentes com uma única obrigatória. Examinar D2, exportação e importação/exportação com Google Drive e outros storages. Evitar variantes customizadas ou guias instalados porém proibidos; definir composição, descoberta lazy, dependências, versões, instalação/atualização e propriedade namespaced. Preservar compatibilidade consumidora e fronteira de evidência. Não implementar antes de requisitos e permissões resolvidos. A pesquisa consolidada em reports/investigacao-wiked.md v1.1 é referência não normativa; integração de serviços continua decisão futura.

## Notes

**2026-10-10T18:40:25.335246002Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-24T13:07:59.194719064Z**

Reorganização autorizada do backlog em 2026-10-24: o épico wik-01m5q079q8jz passa a tratar projeções e recuperação unificada. O contrato mínimo wik-01m5q082jdqm deve preservar capacidades opcionais e composição compatível, mas não implementa a arquitetura geral de skills deste ticket. Os trabalhos permanecem independentes, sem nova dependência bloqueante ou expansão de escopo; eventual integração deve reutilizar as fronteiras aprovadas e manter carregamento progressivo.
