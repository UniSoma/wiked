---
id: wik-01m4khsrmqya
title: Preparar primeira publicação verificável do Wiked
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-10T18:39:26.693651906Z'
updated: '2026-10-10T23:29:45.629754255Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- distribuicao
acceptance:
- title: Repositório autoral independente e custódia confirmados pelo mantenedor
  done: false
- title: Artefato preparado conforme versão, inventário, compatibilidade e integridade aprovados
  done: false
- title: Testes genéricos e prova de uso do artefato independentes de qualquer consumidor real
  done: false
- title: Publicação humana identificável registrada e documentação de release coerente
  done: false
- title: README contém origem GitHub exata, comandos verificados de download/integridade/instalação/atualização e transição ao setup, incluindo destinos alternativos e pré-requisitos
  done: false
- title: Licença MIT e avisos aplicáveis presentes; release inclui tar.gz manifestado, instalador testado e checksums SHA-256, com versão imutável aprovada pelo mantenedor
  done: false
deps:
- wik-01m2tphwrc4f
- wik-01m2tpjtev7w
---

## Description

Preparar e verificar a primeira publicação conforme docs/distribution.md, aprovado no grill de wik-01m2tphwrc4f em 2026-10-10, após implementação/testes do instalador wik-01m2tpjtev7w. Volnei Santos decide versões e aprova releases; Git e publicação são humanos. Confirmar endereço exato do repositório GitHub oficial e GitHub Releases; não deduzir origem do schema. Preparar licença MIT com atribuição e avisos de terceiros, arquivo .tar.gz exatamente com os arquivos do manifesto, instalador separado e checksums SHA-256. Versões SemVer e artefatos publicados imutáveis; correções exigem nova versão; prévias excluídas da seleção estável. Fonte atual 1.4.0 não determina automaticamente a versão a publicar: verificar coerência manifesto/runtime, mudanças entregues e decisão do mantenedor. README deve permitir adoção independente com links oficiais exatos, verificação do instalador antes de executar, pré-requisitos uv/knot, Linux/macOS/WSL, destino padrão/customizado, descoberta pelo agente e fluxo instalação/atualização/setup. Validar artefato e instalador integrados em ambiente sintético sem consumidor real nem release prévia. Registrar evidência de publicação humana identificável, não apenas existência da árvore ou arquivo local. Assinatura independente, Windows nativo e seleção de versões antigas ficam fora desta entrega. Preservar fronteiras de propriedade e não instalar ferramentas no host nem substituir skill do agente.

## Notes

**2026-10-10T18:40:31.740875930Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.
