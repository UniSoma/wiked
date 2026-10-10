---
id: wik-01m2tpjtev7w
title: Implementar instalador e atualizador humano do Wiked
status: open
type: feature
priority: 2
mode: afk
created: '2026-09-18T16:46:19.574642249Z'
updated: '2026-10-10T18:40:23.994085344Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- setup
acceptance:
- title: Script implementa requisitos humanos aprovados e versões identificáveis/verificáveis
  done: false
- title: Bootstrap e atualização contemplam todas as ferramentas obrigatórias e preservam instalações/artefatos terceiros conforme política
  done: false
- title: Git/Knot são inicializados somente quando necessário pelo script executado por humano
  done: false
- title: Nenhum conteúdo de domínio é criado e término orienta wiked-setup
  done: false
- title: Testes cobrem primeira instalação, atualização, pré-requisitos ausentes e falhas parciais sem modificar host do agente
  done: false
deps:
- wik-01m4khsrmqya
---

## Description

Follow-up independente. Implementar script Bash conforme requisitos e grill do ticket de distribuição; AFK condicionado a esses requisitos já estarem resolvidos. Script será executado por humano, não pelo agente para instalar na máquina de trabalho. Verificar/instalar uv, Knot, D2, pandoc, weasyprint e rsvg-convert; inicializar Git/Knot quando necessário; instalar versão identificável e adaptadores sem afetar terceiros em .agents/. Não gerar conteúdo da wiki ou decidir domínio; orientar wiked-setup após bootstrap. Suportar atualização técnica controlada, versões fixas, integridade e recuperação de falhas conforme desenho. Testar com doubles/ambiente descartável autorizado sem instalar ferramentas no host nem executar Git pelo agente. Se requisitos insuficientes, retomar HITL antes de implementar escolhas.

## Notes

**2026-10-10T18:40:23.994085344Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.
