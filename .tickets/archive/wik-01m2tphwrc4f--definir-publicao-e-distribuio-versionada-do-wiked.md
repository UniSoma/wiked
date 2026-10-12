---
id: wik-01m2tphwrc4f
title: Definir publicação e distribuição versionada do Wiked
status: closed
type: task
priority: 2
mode: hitl
created: '2026-09-18T16:45:49.157947100Z'
updated: '2026-10-10T23:30:11.618602788Z'
closed: '2026-10-10T23:30:11.618602788Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- distribuicao
acceptance:
- title: Grill encerrado com artefato, origem, canais e responsabilidades aprovados
  done: true
- title: Versões fixas, compatibilidade, integridade e propriedade do manifesto definidas
  done: true
- title: Requisitos técnicos e comportamento do instalador/atualizador aprovados, incluindo plataformas e falhas parciais
  done: true
- title: Tickets executores refinados para evitar decisões implícitas
  done: true
---

## Description

Trabalho futuro no repositório autoral Wiked. A distribuição genérica e a fronteira autor/consumidor já existem; a extração local não decide nem realiza publicação. Conduzir grill para definir origem canônica, artefato, versões imutáveis, compatibilidade, integridade, licença, canais de download, propriedade do manifesto e responsabilidade por releases. Qualificar requisitos do instalador/atualizador: plataformas, versões, pré-requisitos, prompts, preservação de terceiros, falhas parciais, recuperação e passagem ao setup. Refinar os tickets executores antes da implementação. Git, publicação e instalação no host são humanos. Contexto de pesquisa suficiente: reports/investigacao-wiked.md v1.1, especialmente comparação e distribuição; a pesquisa não aprova essas decisões.

## Notes

**2026-10-10T18:40:23.311891076Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-10T23:30:05.435541097Z**

Grill metodológico encerrado em 2026-10-10: o solicitante confirmou explicitamente o resumo final e autorizou sua consolidação. Objetivo e escopo: contrato de publicação/distribuição e refinamento dos executores; implementação e publicação continuam separadas. Decisões consolidadas em docs/distribution.md, com navegação e orientação em README.md, CONTEXT-MAP.md e docs/metodologia.md. A decisão final de última release estável substitui a proposta inicial de seleção explícita de versão. uv e knot são obrigatórios antes de instalar artefatos; não há instalação de ferramentas ou inicialização Git/Knot. Destino customizado, sobrescrita aprovada, preservação de terceiros, recuperação, validação somente do contrato e ticket opcional de migração aprovados. Executores wik-01m2tpjtev7w e wik-01m4khsrmqya refinados; dependência invertida para contrato -> instalador testado -> publicação humana. Sem decisões em aberto neste objetivo; assinatura independente, Windows nativo e seleção de versões antigas ficam fora da entrega. Endereço oficial exato, licença materializada e comandos de download serão verificados/entregues pelo executor de publicação, sem afirmar release existente. Evidência: checagem textual de links Markdown locais e whitespace passou nos quatro documentos; inspeção confirmou inglês nas instruções novas, identidade autor/consumidor, propriedade preservada, ausência de dependência docs/ na skill e roteamento ao contrato local. knot check --json: ok=true, issues=[], 11 tickets ativos e 2 arquivados. Mudanças apenas documentais: rota de validação textual, sem alteração de runtime/testes.

**2026-10-10T23:30:11.618602788Z**

Contrato de publicação e distribuição aprovado e consolidado em docs/distribution.md, README e navegação autoral. Quatro critérios concluídos; executores refinados e ordenados para implementar/testar instalador antes da primeira publicação humana. Checagens textuais e integridade do tracker aprovadas.
