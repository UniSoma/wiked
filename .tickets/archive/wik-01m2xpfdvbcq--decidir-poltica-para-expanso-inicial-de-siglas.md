---
id: wik-01m2xpfdvbcq
title: Decidir política para expansão inicial de siglas
status: closed
type: task
priority: 3
mode: hitl
created: '2026-09-19T20:42:11.661702695Z'
updated: '2026-10-24T14:44:20.192382936Z'
closed: '2026-10-24T14:44:20.192382936Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- modelagem
acceptance:
- title: Casos concretos atuais e efeito do relaxamento permanecem registrados
  done: true
- title: Grill decide alcance, autoridade e destino da convenção
  done: true
- title: Solução aprovada evita conhecimento DOI na distribuição e duplicação normativa
  done: true
---

## Description

Decidir se a metodologia deve orientar expansão de siglas na primeira ocorrência e qual é a unidade de leitura (página, seção ou documento completo). Contexto histórico: havia convenção editorial local de expansão de algumas siglas, sem formalizar unidade nem conjunto abrangido; a referência editorial local era opcional e separada da evidência operacional. Exemplos históricos de grafias que motivaram a questão: DGG, MKT, Ginfra, PJP e SGU. São apenas casos de grafia, sem definição ou regra de domínio transportada. Para prova independente, usar casos sintéticos, como ABC e uma sigla de capitalização mista, comparando primeira ocorrência por página e por seção. Conduzir decisão HITL entre orientação genérica, critério editorial local, regra contratual verificável ou abandono justificado. Não presumir exigência universal nem duplicar obrigações entre contexto terminológico e referência de autoria. Este ticket é suficiente para retomar a decisão sem consultar o consumidor ou seus tickets.

## Notes

**2026-10-10T18:40:27.802019884Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-24T14:43:32.374469633Z**

Grill metodológico encerrado em 2026-10-24: o solicitante confirmou explicitamente o resumo final com "de acordo". Objetivo autorizado: esclarecer a expansão inicial de siglas como critério editorial local opcional, não obrigação universal nem validação automática. Primeira ocorrência por página é ponto de partida sujeito à aprovação local. Alcance: páginas da wiki, sem extensão automática a respostas, exportações ou diagramas e sem alterar títulos ou rótulos canônicos. Significados permanecem no contexto terminológico; critérios de apresentação pertencem à referência local de autoria, sem duplicação normativa. Escopo de edição: apenas distr/agents/skills/wiked/guides/authoring-context.md, em inglês; sem arquivo obrigatório novo, mudanças no contrato/runtime ou consumidor. Verificação: checks textuais direcionados e revisão semântica, sem testes que congelem prosa. Nenhuma pendência lateral necessária.

**2026-10-24T14:44:11.231938838Z**

Implementação e evidências: alterado somente distr/agents/skills/wiked/guides/authoring-context.md, com seção Local Acronym Presentation. Critério local opcional, primeira ocorrência por página como proposta sujeita a aprovação humana, separação entre apresentação e significado, adoção/alteração pela manutenção governada, ausência de obrigação de criar referência sem critério adotado e exclusões de formatos/títulos aprovadas. Casos históricos preservados na descrição: DGG, MKT, Ginfra, PJP e SGU; são grafias motivadoras, sem definições ou fatos do consumidor. Estado atual da distribuição: não havia exigência universal; portanto não se removeu regra genérica nem se relaxou automaticamente critério local existente. Uma instância que deixe de exigir expansão reduz repetição, mas pode dificultar leitura isolada; essa alteração local exige sua própria aprovação. Comparação sintética (não operacional): ABC = Archive Batch Controller; MiCo = Mixed Input Coordinator. Página A, seção Prepare: "Archive Batch Controller (ABC) sends work to Mixed Input Coordinator (MiCo)." Seção Recover da mesma página: por página, "Restart ABC, then inspect MiCo"; por seção, repetir as duas formas expandidas. Página B: a convenção por página volta a apresentar ambas; a convenção por documento completo poderia omiti-las e prejudicar consulta independente. A expansão por seção facilita leitura por fragmento, com maior repetição. MiCo mostra que capitalização mista não pode ser presumida irrelevante. Esses exemplos documentam o efeito, não estabelecem política do consumidor. Verificação textual via Node: quatro referências locais a guias resolvidas, ASCII integral e nenhuma dependência de docs/. Revisão semântica comparou modeling.md, maintenance.md, setup.md, query.md, d2.md e manifesto: preservados significados canônicos, governança, referência opcional, roteamento seletivo e títulos/rótulos; arquivo já pertence ao manifesto, sem alterar propriedade ou versão. Não houve edição/inspeção de consumidor, alteração de schema/runtime nem testes de prosa; pytest não se aplica a esta mudança exclusivamente instrucional. Checks estruturais e revisão não demonstram adesão comportamental do agente.

**2026-10-24T14:44:20.192382936Z**

Política decidida por grill confirmado e esclarecida no guia de contexto de autoria: expansão de siglas opcional e local, por página como ponto de partida sujeito a aprovação, sem validação automática ou extensão a outros formatos. Casos históricos, comparação sintética e checks textuais registrados; três critérios concluídos. Nenhuma alteração em consumidor, contrato ou runtime.
