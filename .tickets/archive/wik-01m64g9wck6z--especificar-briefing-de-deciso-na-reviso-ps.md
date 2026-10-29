---
id: wik-01m64g9wck6z
title: Especificar briefing de decisão na revisão pós-atualização e enriquecer o contrato do changelog
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-29T18:56:05.011374869Z'
updated: '2026-10-29T20:56:27.272256628Z'
closed: '2026-10-29T20:56:27.272256628Z'
tags:
- metodologia
- wiked
- manutencao
- changelog
acceptance:
- title: Methodological grill fechado com confirmação explícita do requisitante sobre o desenho do briefing de decisão na revisão pós-atualização
  done: true
- title: Contrato enriquecido do changelog especificado (campos de motivo e dores resolvidas, aplicabilidade por tipo de entrada, limites de tamanho) e decidida a extensão retroativa às versões publicadas
  done: true
- title: Decididos local canônico das regras, preservação do carregamento progressivo, incremento de versão e forma de avaliação
  done: true
- title: Tickets de implementação criados para o escopo aprovado, com especificação suficiente e decisões registradas neste ticket
  done: true
links:
- wik-01m64q57xm81
---

## Description

Usuários relatam dificuldade para aprovar ou recusar mudanças nas sessões de manutenção após atualização de versão: nem sempre leram as release notes nem têm em mente o funcionamento atual. Exemplos relatados: (1) links navegáveis nos diagramas (integração Docsify, 1.6.0/1.7.0) — "tive que pesquisar o que eram os tais links, para saber se eu queria adotar ou não"; (2) exigência de correspondência entre etapas dos diagramas e seções do processo (1.5.1, mantida na 1.6.0) — "como era antes mesmo e o impacto disso nas minhas páginas?".

Revisão metodológica (somente leitura) constatou:
- `guides/maintenance.md`, seção Installed-version review, exige relatar impactos e obter disposição humana, mas não exige explicar natureza, motivação, efeito concreto na wiki nem consequências de adotar/recusar antes da pergunta.
- A skill instalada só contém os guias atuais; o changelog é a única memória de versões anteriores, e seu contrato (`docs/distribution.md`, "impact index, not a second manual … omit internal-change narratives") não registra motivo nem dores resolvidas. Sem enriquecer o changelog, o agente teria de inferir ou inventar a explicação.
- Intervalos com entradas superadas (1.5.1 exigia links bidirecionais; 1.6.0 os tornou opcionais) exigem consolidar o efeito líquido.

Objetivo deste ticket: detalhamento (especificação), não implementação. Decisões já indicadas pelo requisitante: enriquecer o contrato do changelog com motivo da mudança e dores solucionadas (não necessariamente descrever o estado anterior); aplicar retroativamente às versões já publicadas, se viável.

## Notes

**2026-10-29T20:49:38.705562883Z**

Grill rodada 1 (requisitante concordou com todas as recomendações):
Q1 Escopo: briefing só na revisão pós-atualização de versão; manutenção comum e grill operacional ficam como pendências laterais.
Q2 Changelog: nova seção `### Rationale` (motivo + dores resolvidas) por entrada `review`, uma linha por impacto quando houver vários; exigida pelo parser em entradas `review`; `none`/`baseline` seguem com uma frase.
Q3 Natureza: cada item de `### Action` começa com marcador padronizado `Required:`, `Optional adoption:` ou `Informational:`; parser verifica só presença.
Q4 Briefing: panorama curto do intervalo, depois um impacto por vez com (1) natureza, (2) regra efetiva consolidando entradas superadas, (3) motivo/dores, (4) efeito concreto na wiki com exemplo do próprio conteúdo, (5) consequências de adotar e recusar, incluindo responsabilidades do consumidor, (6) recomendação explícita e só então a pergunta. Explica sem persuadir; não altera gates; nunca afirma estado anterior não registrado no changelog ou guias.
Q5 Consequências de adoção opcional: parágrafo curto "o que a adoção oferece e exige" no guia canônico da capacidade (ex. docsify.md); changelog diz o porquê.
Q6 Limites: até 3 linhas de Rationale por impacto, links em vez de repetir procedimentos; briefing com um parágrafo curto por impacto, aprofundamento sob demanda.
Fato: retroatividade viável — artefatos publicados são imutáveis, mas a revisão lê o CHANGELOG instalado; a próxima versão carrega 1.5.0–1.7.0 reescritas.

**2026-10-29T20:55:04.389954925Z**

Grill rodada 2 (requisitante concordou com as recomendações):
Q7 Todo item `Optional adoption:` aponta para seção de guia com parágrafo "o que a adoção oferece e exige"; retroativo para Docsify (docsify.md), intent map (modeling.md#intent-map), siglas e citações contextuais locais (authoring-context.md).
Q8 Adoção opcional sempre oferece adotar (correção com grill/ticket próprios), recusar (registrado no relatório, sem nova pergunta até nova entrada sobre o tema) ou adiar (ticket de acompanhamento no Knot do consumidor); nenhuma bloqueia a conclusão da revisão. `Required:` segue o fluxo atual.
Q9 Reescrita retroativa: não muda o significado de Review/Action; só acrescenta Rationale e marcadores; motivo vem do histórico real (tickets arquivados, commits, docs/distribution.md); motivo irrecuperável é declarado; requisitante valida o texto antes da preparação da versão.
Q10 Recomendação de patch com declaração `none`, mas a versão NÃO é fechada agora: outros itens podem entrar e elevar a minor. Classificação final cabe ao mantenedor na preparação.
Q11 pytest para o parser (Rationale e marcadores), checagens textuais direcionadas para guias, sem congelar prosa; três cenários de avaliação comportamental registrados no piloto wik-01m4vhpp3xyt.
Q12 Um único ticket de implementação, hitl; implementador faz grill curto de confirmação apoiado nestas decisões, retomando grill completo se surgir decisão nova.

**2026-10-29T20:55:57.393730145Z**

Grill fechado: o requisitante confirmou explicitamente o resumo final em 2026-10-29. Ticket de implementação: wik-01m64q57xm81 (hitl, ligado). Cenários comportamentais registrados em wik-01m4vhpp3xyt. Nenhum conteúdo governado editado.

**2026-10-29T20:56:27.272256628Z**

Especificação concluída: grill metodológico fechado em 2026-10-29 definindo o briefing de decisão na revisão pós-atualização e o changelog enriquecido (Rationale, marcadores de natureza, parágrafos de adoção, reescrita retroativa 1.5.0–1.7.0). Implementação em wik-01m64q57xm81; cenários comportamentais em wik-01m4vhpp3xyt.
