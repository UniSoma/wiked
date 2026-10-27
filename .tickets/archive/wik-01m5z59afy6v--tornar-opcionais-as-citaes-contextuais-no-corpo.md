---
id: wik-01m5z59afy6v
title: Tornar opcionais as citações contextuais no corpo das páginas operacionais
status: closed
type: feature
priority: 2
mode: hitl
created: '2026-10-27T17:07:20.190030504Z'
updated: '2026-10-27T22:14:59.486460730Z'
closed: '2026-10-27T22:14:59.486460730Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
acceptance:
- title: Grill metodológico fecha a decisão sobre opcionalidade, comportamento padrão sem critério local e localização canônica da regra
  done: true
- title: Guias afetados coerentes entre si, com query.md e com a regra contextual_citation, preservando carregamento progressivo
  done: true
- title: Verificações textuais direcionadas registradas no ticket; schema, contrato e validador inalterados ou alteração justificada
  done: true
- title: Entrada de CHANGELOG (Review/Action) redigida e registrada no ticket para a próxima declaração de versão, definida pelo mantenedor
  done: true
---

## Description

Proposta externa de mudança recebida em 2026-10-27, originada na Wiki Operacional da DOI (UniSoma), sobre o Wiked 1.6.0. O conteúdo do consumidor é motivação, não fixture nem requisito genérico.

### Situação atual

- `guides/assisted-indexing.md`, Consolidate, passo 5: "Attach contextual source-page citations to interpretations, time-sensitive claims, and divergences."
- `guides/modeling.md`, Provenance and Visuals: "Use contextual citations where interpretation, currency, or divergence depends on one source page."
- A regra `contextual_citation` não exige citações no corpo; apenas exige que toda página de fonte citada no corpo também esteja na seção de fontes configurada.

### Problema relatado

Página de processo com 16 citações no corpo em 371 linhas, 11 para a mesma fonte. Efeitos: (1) escopo ambíguo da citação no fim do parágrafo; (2) leitura desviada do processo vigente para o histórico de indexação; (3) acúmulo sem passo de remoção quando fonte posterior supera a anterior; (4) incoerência com `query.md`, que manda listar fontes ao final de documentos legíveis "instead of scattering citations through its body".

### Proposta

Tornar citações contextuais no corpo uma escolha editorial da instância, declarada na referência de autoria local. Proveniência continua obrigatória na seção de fontes (regra `provenance`), atualidade expressa por data no texto, divergências como pendências configuradas (passo 4).

- assisted-indexing.md passo 5 → "Apply the local authoring reference's citation criteria, if any. Otherwise keep provenance in the configured source references, state time-sensitive claims explicitly in the text, and keep unresolved divergences as configured pending items."
- modeling.md → substituir o bullet de citações por "Contextual citations in the body are an instance editorial choice. Use them only as the local authoring reference defines; the methodology does not require them."
- Sem mudança de schema, contrato ou validador. Mudança compatível, sugerida como minor com entrada no CHANGELOG.

### Impacto declarado

Nenhuma página fica inválida; instâncias que querem manter declaram critério local; remoção de citações existentes exige manutenção governada com grill fechado.

## Notes

**2026-10-27T22:02:03.551903944Z**

Grill metodológico, rodada 1 (decisões do solicitante):
- Q1: a linha de modeling.md "Every page that the contract assigns an operational-content role must carry its configured source references" permanece; a proveniência por página segue obrigatória (regra provenance). Só as citações no corpo viram critério local.
- Q2: sem critério local, o padrão é não usar citações contextuais no corpo. Justificativa: o link ao fim da seção não garante, na prática, rastreio por afirmação e mais atrapalha do que ajuda. Uma forma de rastreio por afirmação (ex.: fontes numeradas com referências sobrescritas junto da frase) fica a cargo de cada wiki.
- Q3: a regra canônica fica numa seção de authoring-context.md, no padrão de "Local Acronym Presentation"; assisted-indexing.md e modeling.md só apontam para ela.
- Q4: o acúmulo de citações superadas fica fora do escopo; nenhum ticket novo por ora.
- Q5: a versão não será fechada agora; o mecanismo de acumular a entrada no CHANGELOG está em avaliação.

**2026-10-27T22:06:48.247769032Z**

Grill metodológico, rodada 2 (decisões do solicitante):
- Q6: a entrada de CHANGELOG fica redigida no ticket; o mantenedor a insere na declaração de versão quando definir a versão. O CHANGELOG distribuído não é editado neste ticket, porque o parser em distribution.py rejeita seções sem versão.
- Q7: sem critério local, as citações no corpo não são exigidas; as existentes não são erro nem são removidas automaticamente. A Action do CHANGELOG deve dizer que a manutenção pode propor limpar essas referências ou adotar no guia da wiki um critério local de citação.
- Q8: a seção canônica em authoring-context.md não traz exemplo de formato e lembra que todo link para página-fonte no corpo precisa constar da seção de fontes de conteúdo.
- Q9: o passo 5 de Consolidate passa a exigir a data ou o período de vigência de afirmações sujeitas a mudar com o tempo; a parte sobre divergências sai, porque o passo 4 já a cobre.
- Q10: query.md e setup.md ficam sem alteração; a orientação à manutenção vai pela Action do CHANGELOG.

**2026-10-27T22:09:15.210044996Z**

Grill metodológico FECHADO, com confirmação explícita do solicitante ("de acordo com Q11 a Q13, pode fechar o grill").
- Q11: textos aprovados para authoring-context.md (nova seção "Local Contextual Citations"), assisted-indexing.md (passo 5) e modeling.md (Provenance and Visuals).
- Q13: critério de aceite 3 ajustado; validação por verificações textuais direcionadas.
- Q12: entrada de CHANGELOG aprovada, a incluir na próxima declaração de versão (definida pelo mantenedor):

### Review

- Contextual source-page citations in page bodies are an optional local editorial
  criterion, not a universal requirement; configured source references remain mandatory.

### Action

- Do not flag existing body citations as nonconformity or remove them automatically.
  Maintenance may propose removing them or adopting a criterion in the local authoring
  reference, following [local contextual citations](guides/authoring-context.md#local-contextual-citations).
- Review time-sensitive claims that relied on a body citation for currency and state
  their effective date or period in the text.

**2026-10-27T22:09:38.105465888Z**

Implementação e verificações textuais direcionadas (mudança só de instruções; sem pytest e sem testes de prosa):
- Edições aplicadas conforme Q11: authoring-context.md (nova seção "## Local Contextual Citations", linha 23), assisted-indexing.md:40 (passo 5) e modeling.md:63.
- Busca por "citation" na distribuição (exceto CHANGELOG): não sobra exigência de citação contextual. query.md:32 segue sem alteração (trata de exportações) e é coerente com o novo padrão.
- Âncora #local-contextual-citations: os dois links apontam para o título "## Local Contextual Citations", que existe.
- Escopo do diff: 3 guias, +6/-2. contracts/, scripts/ e tests/ inalterados (git diff --quiet). A regra contextual_citation do validador segue coerente: o texto novo repete a exigência de listar nas fontes toda página-fonte linkada no corpo.
- Carregamento progressivo preservado: os dois guias apontam para authoring-context.md, que já é carregado na preparação dos fluxos que os usam.
- CHANGELOG distribuído não editado (Q6); a entrada está registrada na nota de fechamento do grill.
- Desvio de processo: as edições foram aplicadas com python3 direto, não com uv run. O script só substituiu texto; o resultado foi conferido pelo diff acima.

**2026-10-27T22:14:59.486460730Z**

Citações contextuais de página-fonte no corpo viraram critério editorial local opcional: nova seção em authoring-context.md (Local Contextual Citations); assisted-indexing.md (passo 5) e modeling.md apontam para ela. Sem critério local, citações não são exigidas e as existentes não são erro. A proveniência por página continua obrigatória. A entrada de CHANGELOG está registrada no ticket para a próxima versão, a definir pelo mantenedor. Schema, contrato, validador e testes inalterados.
