---
id: wik-01m64q57xm81
title: Implementar briefing de decisão na revisão pós-atualização e changelog com Rationale
status: closed
type: feature
priority: 2
mode: hitl
created: '2026-10-29T20:55:53.012263309Z'
updated: '2026-10-30T16:10:25.980781761Z'
closed: '2026-10-30T16:10:25.980781761Z'
tags:
- metodologia
- wiked
- manutencao
- changelog
acceptance:
- title: Grill curto de confirmação de escopo fechado com confirmação explícita do requisitante
  done: true
- title: Contrato do changelog em docs/distribution.md atualizado com Rationale, marcadores de natureza e vínculo de adoção opcional
  done: true
- title: Parser exige Rationale e marcadores em entradas review; uv run pytest passa
  done: true
- title: CHANGELOG 1.5.0–1.7.0 reescrito retroativamente sem mudar o significado, com texto validado pelo requisitante
  done: true
- title: maintenance.md especifica o briefing e as três respostas para adoção opcional, preservando gates e carregamento progressivo
  done: true
- title: Parágrafos de adoção em docsify.md, modeling.md#intent-map e authoring-context.md
  done: true
- title: Checagens textuais direcionadas executadas e evidência registrada no ticket
  done: true
- title: 'Versão 1.8.0 preparada: manifesto 1.8.0, entrada 1.8.0 - review no formato novo, uv run pytest e bash scripts/package-wiked.sh executados com resultados registrados'
  done: true
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

## Notes

**2026-10-30T15:36:09.075830885Z**

Grill curto de confirmação, rodada 1 (requisitante "de acordo" em todas): Q1 incluir a preparação da 1.8.0 neste ticket (manifesto 1.8.0, entrada 1.8.0 no formato novo, uv run pytest e package-wiked.sh; sem Git nem publicação). Q2 1.8.0 minor com declaração review: dois Optional adoption (external_authority, rules.external_links) e um Informational (briefing e changelog enriquecido). Q3 parágrafos de adoção em modeling.md#external-authority e nova seção modeling.md External Links. Q4 parser: Review, Rationale e Action obrigatórias sem ordem; Action só com itens de topo marcados Required:/Optional adoption:/Informational:, ao menos um; sem checar tamanho nem links. Q5 dividir itens retroativos de natureza mista sem mudar significado; motivo irrecuperável declarado; histórico de motivos levantado por subagente a partir de git log e Knot, sem revisar código. Q6 atualizar o contrato em docs/distribution.md e acrescentar nota de aprovação no padrão existente.

**2026-10-30T15:37:00.135311618Z**

Entendimento compartilhado confirmado explicitamente pelo requisitante em 2026-10-30 ('confirmado'); grill curto de confirmação encerrado. Escopo inclui a preparação da 1.8.0.

**2026-10-30T15:45:12.243770531Z**

Implementação na branch wik-01m64g2kj369-autoridade-externa (sem commit). Arquivos: docs/distribution.md (contrato do changelog com Rationale, marcadores e vínculo de adoção; nota de aprovação), scripts/distribution.py (review_entry: Review/Rationale/Action obrigatórias, Action só com itens de topo marcados, ao menos um), tests/test_wiked_packaging.py (casos missing-rationale, unmarked-action, action-paragraph, empty-action), CHANGELOG.md (1.8.0 - review nova; 1.5.0–1.7.0 com Rationale e marcadores, itens mistos divididos, motivos não registrados declarados; fontes: wik-01m4rt9yj681, wik-01m5nmmxxssd, wik-01m5q2xawjrj, wik-01m5q5abxefd, wik-01m2xpfdvbcq, wik-01m5z59afy6v, wik-01m5r3vepwpa, wik-01m64bng5vzs), guides/maintenance.md (briefing e três respostas para adoção opcional), parágrafos de adoção em docsify.md#authority-and-adoption, modeling.md#intent-map, #external-authority, nova #external-links, authoring-context.md (siglas e citações), manifesto 1.8.0.
Evidência: uv run pytest — 267 passed, 2 skipped, exit 0; tests/test_wiked_packaging.py reexecutado após o último ajuste do CHANGELOG — 27 passed. bash scripts/package-wiked.sh — 'Packaged Wiked 1.8.0', tag v1.8.0, nada publicado. release_declarations aceita 1.8.0..1.4.1. Targeted textual checks: links e âncoras dos arquivos distribuídos alterados resolvem (únicos 'quebrados' são exemplos ilustrativos preexistentes em blocos de código), ASCII/inglês, sem dependência de docs/, todo Optional adoption aponta para seção com parágrafo de adoção, git diff --check limpo. Pendente: validação do texto do CHANGELOG pelo requisitante (AC4).

**2026-10-30T16:10:25.980781761Z**

Briefing de decisão na revisão pós-atualização, changelog com Rationale e marcadores de natureza (parser e testes), parágrafos de adoção nos guias, reescrita retroativa 1.5.0–1.7.0 validada pelo requisitante e versão 1.8.0 preparada (pytest 267 passed/2 skipped; pacote v1.8.0, não publicado).
