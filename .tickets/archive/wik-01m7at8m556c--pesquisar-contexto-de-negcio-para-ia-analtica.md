---
id: wik-01m7at8m556c
title: Pesquisar contexto de negócio para IA analítica
status: closed
type: chore
priority: 2
mode: afk
created: '2026-11-13T16:01:17.989466462Z'
updated: '2026-11-13T16:04:59.170657607Z'
closed: '2026-11-13T16:04:59.170657607Z'
parent: wik-01m7at81hnsd
tags:
- wayfinder-research
---

## Description

### Question

Que evidências públicas (camadas semânticas, context engineering, text-to-SQL com contexto de negócio, glossários e metadados para agentes) sustentam que contexto de negócio ligado aos dados melhora a qualidade de respostas de IA analítica (UC3)?

## Notes

**2026-11-13T16:04:59.045356123Z**

Benchmarks revisados por pares (BIRD, NeurIPS 2023) mostram ganho consistente quando o modelo recebe conhecimento de negócio ligado aos dados (GPT-4: 34,88% para 54,89% de acurácia de execução); Spider 2.0 e BEAVER mostram que o contexto corporativo real é difícil de encontrar e usar. Estudos de fornecedores (data.world, dbt, AtScale, Snowflake) reportam ganhos grandes com camadas semânticas e ontologias, mas com amostras pequenas e sem controle independente. A evidência mede correção de SQL, não profundidade analítica; os ganhos diminuem com modelos mais novos e o contexto precisa estar correto. Nenhum estudo público testa uma wiki como o Wiked: a mensagem deve posicioná-lo como complemento governado e com proveniência às camadas semânticas.

**2026-11-13T16:04:59.170657607Z**

Evidência pública sustenta, com ressalvas, que contexto de negócio ligado aos dados melhora a acurácia de IA analítica; fraseado defensável documentado.
