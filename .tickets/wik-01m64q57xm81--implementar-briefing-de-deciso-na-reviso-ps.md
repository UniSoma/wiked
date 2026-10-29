---
id: wik-01m64q57xm81
title: Implementar briefing de decisão na revisão pós-atualização e changelog com Rationale
status: open
type: feature
priority: 2
mode: hitl
created: '2026-10-29T20:55:53.012263309Z'
updated: '2026-10-29T20:55:53.408325267Z'
tags:
- metodologia
- wiked
- manutencao
- changelog
acceptance:
- title: Grill curto de confirmação de escopo fechado com confirmação explícita do requisitante
  done: false
- title: Contrato do changelog em docs/distribution.md atualizado com Rationale, marcadores de natureza e vínculo de adoção opcional
  done: false
- title: Parser exige Rationale e marcadores em entradas review; uv run pytest passa
  done: false
- title: CHANGELOG 1.5.0–1.7.0 reescrito retroativamente sem mudar o significado, com texto validado pelo requisitante
  done: false
- title: maintenance.md especifica o briefing e as três respostas para adoção opcional, preservando gates e carregamento progressivo
  done: false
- title: Parágrafos de adoção em docsify.md, modeling.md#intent-map e authoring-context.md
  done: false
- title: Checagens textuais direcionadas executadas e evidência registrada no ticket
  done: false
links:
- wik-01m64g9wck6z
- wik-01m4vhpp3xyt
---

## Description

Implementa a especificação fechada no Methodological grill de wik-01m64g9wck6z (confirmado pelo requisitante em 2026-10-29). As decisões completas estão nas notas daquele ticket; antes de editar, rodar um grill curto de confirmação de escopo apoiado nelas e retomar o grill completo se surgir decisão substantiva nova.

Problema: na revisão pós-atualização, usuários não conseguem decidir sobre impactos (ex.: links navegáveis Docsify; correspondência etapa↔seção) porque o agente pergunta sem explicar, e o changelog não registra motivo nem dores resolvidas.

Escopo:
- `docs/distribution.md`: contrato do changelog com `### Rationale` (motivo + dores resolvidas, até 3 linhas por impacto) obrigatório em entradas `review`; marcadores `Required:`, `Optional adoption:`, `Informational:` no início de cada item de `### Action`; todo `Optional adoption:` aponta para seção de guia com parágrafo "o que a adoção oferece e exige". `none`/`baseline` seguem com uma frase.
- `distr/agents/skills/wiked/scripts/distribution.py` (`release_declarations`) e testes: exigir presença de `### Rationale` e dos marcadores em entradas `review` (só formato).
- `distr/agents/skills/wiked/CHANGELOG.md`: reescrita retroativa de 1.5.0, 1.5.1, 1.6.0 e 1.7.0 sem alterar o significado de Review/Action; motivo extraído do histórico real (tickets arquivados, commits, docs/distribution.md); motivo irrecuperável declarado explicitamente.
- `guides/maintenance.md` (Installed-version review): briefing antes de pedir disposição — panorama curto do intervalo, depois por impacto um parágrafo curto com natureza, regra efetiva consolidando entradas superadas, motivo/dores, efeito concreto na wiki com exemplo do próprio conteúdo, consequências de adotar/recusar (incl. responsabilidades do consumidor), recomendação explícita e então a pergunta; no idioma da instância; explica sem persuadir; não altera gates; nunca afirma estado anterior não registrado. Adoção opcional oferece adotar (correção com grill/ticket), recusar (registrado no relatório) ou adiar (ticket de acompanhamento); nenhuma bloqueia a conclusão da revisão. Aprofundamento sob demanda.
- Parágrafo "o que a adoção oferece e exige" em `guides/docsify.md`, `guides/modeling.md#intent-map` e `guides/authoring-context.md` (siglas e citações contextuais locais).

Fora do escopo: briefing na manutenção comum e no grill operacional; prompt de manutenção do instalador; fechamento de versão (recomendação atual: patch com declaração `none`, sujeita a mudar se outros itens entrarem; decisão do mantenedor).
