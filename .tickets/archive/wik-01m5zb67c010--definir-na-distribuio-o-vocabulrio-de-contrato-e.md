---
id: wik-01m5zb67c010
title: Definir na distribuição o vocabulário de contrato e validador necessário à instalação
status: closed
type: task
priority: 3
mode: hitl
created: '2026-10-27T18:50:30.142672260Z'
updated: '2026-10-27T19:18:45.979580977Z'
closed: '2026-10-27T19:16:34.223357974Z'
links:
- wik-01m5z64vwzy0
- wik-01m5zcsy6ky7
---

## Description

Lateral de wik-01m5z64vwzy0. O que uma instalação precisa saber deve estar definido em distr/agents; o agente consumidor só enxerga a skill. Hoje distr/ usa "local contract" (guides/docsify.md, maintenance.md, setup.md), "the contract" e "distributed validator" sem defini-los explicitamente; scripts/README.md:11 usa "consumer contract", e scripts/install-wiked.sh:635 imprime "consumer contract" ao consumidor. Verificar se a distribuição define esses termos e uniformizá-los, incluindo a mensagem do instalador. Mudança em distr/ exige decisão de versão e declaração no CHANGELOG distribuído (docs/distribution.md). README.md e docs/installation.md seguem o vocabulário voltado ao consumidor.

## Notes

**2026-10-27T19:01:15.297543577Z**

Methodological grill fechado em 2026-10-27: 'instance contract' definido em SKILL.md:13 e 'distributed validator' em SKILL.md:54 (formas curtas 'the contract'/'the validator'); substituir local/consumer contract e versioned/portable validator em distr/; alinhar instalador (linha 635 e prompt de manutenção), README.md:106 e docs/installation.md:204,209; manifesto e CHANGELOG intocados (recomendação: patch, none). Validação: textual + uv run pytest.

**2026-10-27T19:16:32.322044518Z**

Implementado e verificado (2026-10-27): SKILL.md:13 define 'the instance contract' e SKILL.md:54 'the distributed validator'; substituições em guides/maintenance.md, docsify.md, setup.md:18 (ocorrência adicional encontrada na checagem), assisted-indexing.md, scripts/README.md:3,11; instalador (prompt de manutenção e mensagem de primeira instalação), README.md:105 e docs/installation.md:204,209. Nenhum resíduo de 'local contract', 'consumer contract', 'versioned validator' ou 'portable PEP 723 validator' em distr/, scripts/, README.md e docs/installation.md. uv run pytest: todos passaram (2 skipped). Uma execução anterior teve falha transitória em test_documented_offline_invocation_ignores_consumer_python_project por cache offline do uv, sem relação com a mudança; não reproduziu. Manifesto e CHANGELOG intocados; recomendação para o release: patch com declaração 'none'. Observação: a mensagem de primeira instalação diz 'with the installed skill and instance contract', embora o contrato normalmente ainda não exista nesse momento (já era assim com 'consumer contract').

**2026-10-27T19:16:34.223357974Z**

Aprovado pelo requerente em 2026-10-27. Distribuição define 'instance contract' e 'distributed validator' no SKILL.md; distr/, instalador, README.md e docs/installation.md alinhados. Pendente para o release humano: versão (recomendação patch) e declaração 'none' no CHANGELOG.
