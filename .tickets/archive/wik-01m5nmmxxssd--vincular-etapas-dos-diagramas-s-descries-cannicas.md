---
id: wik-01m5nmmxxssd
title: Vincular etapas dos diagramas às descrições canônicas na metodologia 1.5.1
status: closed
type: feature
priority: 2
mode: hitl
created: '2026-10-24T00:23:24.857711820Z'
updated: '2026-10-24T00:25:09.302972809Z'
closed: '2026-10-24T00:25:09.302972809Z'
tags:
- metodologia
- diagramas
acceptance:
- title: Protocolo define correspondência, títulos iguais, identidade estável, navegação bidirecional e exceções sem depender de um visualizador específico
  done: true
- title: Manutenção e changelog 1.5.1 orientam inventário, proposta autorizada de adequações e verificação de suporte do visualizador e navegação
  done: true
- title: Regras preservam Markdown canônico, imagem compatível, SVG gerado sem edição manual, carregamento progressivo e fronteiras do consumidor
  done: true
- title: Verificações textuais técnicas e revisão de coerência registradas sem alegar validação de navegador ou cobertura semântica automatizada
  done: true
---

## Description

Autoridade solicitante declarou habilitação e confirmou explicitamente o fechamento do Methodological grill nesta sessão. Escopo aprovado: exigir correspondência entre ações, decisões e subprocessos e suas seções canônicas; igualdade entre rótulo e título, exceto quebras de linha visuais; identificadores estáveis independentes do título; navegação bidirecional. Contêineres e marcadores auxiliares dispensados salvo descrição própria. Atualização 1.5.1 deve inventariar divergências, propor adequações e verificar suporte do visualizador, sem autorizar correções automaticamente. Alterar apenas instruções genéricas relacionadas e changelog; não editar consumidores, instalar integrações, modificar runtime/schema nem publicar. Funcionamento no navegador será verificado no consumidor durante adequação autorizada. Validação por verificações textuais técnicas e revisão metodológica, sem testes que congelem prosa.

## Notes

**2026-10-24T00:24:56.292154560Z**

Implementação concluída em distr/agents/skills/wiked/guides/d2.md, guides/maintenance.md e CHANGELOG.md. Protocolo canônico define associação por etapa, títulos iguais exceto quebra visual, identidade estável, links D2 e retorno Markdown e exceções. Manutenção carrega a regra sob demanda. Changelog 1.5.1 alterado de none para review, orientando inventário, propostas autorizadas e verificação de capacidade e navegação do visualizador. Revisão metodológica preservou precedência do Markdown, governança, exportações estáticas temporárias, imagem reconhecida pelo validador, ausência de edição manual de SVG e propriedade do consumidor. Verificações textuais via Bash passaram: ASCII, whitespace, propriedade no manifesto, destinos locais de links Markdown, âncoras técnicas alteradas e versão 1.5.1. Nenhuma dependência nova de docs/, mudança em runtime/schema/testes ou publicação. pytest não executado: alteração apenas de instruções. Não há alegação de cobertura semântica automatizada ou teste em navegador: associação operacional e navegação efetiva serão verificadas no consumidor durante adequação autorizada. Grill explicitamente fechado pelo solicitante antes das edições.

**2026-10-24T00:25:09.302972809Z**

Evolução metodológica 1.5.1 implementada: protocolo de correspondência e navegação entre etapas e seções, manutenção orientada e changelog de revisão. Verificações textuais passaram; implementação e teste de navegação em consumidores permanecem sob adequação autorizada. Nenhuma publicação realizada.
