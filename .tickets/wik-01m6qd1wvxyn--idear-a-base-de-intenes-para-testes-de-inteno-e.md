---
id: wik-01m6qd1wvxyn
title: Idear a base de intenções para testes de intenção e evals da metodologia
status: open
type: task
priority: 2
mode: hitl
created: '2026-11-06T03:04:51.836771250Z'
updated: '2026-11-06T03:25:30.205136921Z'
tags:
- metodologia
- evals
- ideation
acceptance:
- title: Conduzir fase de ideation produzindo opções e eixos de tradeoff para formato do registro de intenções, tipos de saída dos predicados e política da cascata de avaliadores
  done: false
- title: Decidir em Methodological grill próprio o recorte a implementar, sem tratar esta ideation como autorização de implementação
  done: false
- title: Registrar lacunas aceitas, incluindo intenções sem eval e limites estatísticos dos evals sob orçamento
  done: false
links:
- wik-01m4vhpp3xyt
---

## Description

Resultado de debate dialético somente leitura (2026-11-06; trajetória `exploration`, restrição `challenge_premise`) sobre testes automatizados das instruções agênticas do Wiked. Próxima fase: `ideation` (opções + eixos de tradeoff). Este ticket não autoriza implementação nem edição de conteúdo governado; implementação exige Methodological grill próprio.

### Espinha dorsal: base de intenções

Cada intenção consolidada e gerida registra:

- **Enunciado** da intenção.
- **Linhagem**: decisão de origem (grill, ticket ou ADR). Mudar uma intenção é decisão governada, nunca ajuste de teste.
- **Portadores**: trechos que a descrevem.
- **Rotas**: objetivos do `SKILL.md` que devem carregar esses trechos (alcançabilidade, por causa da divulgação progressiva).
- **Contraexemplos conhecidos** (opcional): fixtures de calibração e mutação. Contradições não são enumeradas; o avaliador as procura no corpus.
- **Evals associados**: relação muitos-para-muitos e parcial; intenção sem eval é lacuna registrada, não cobertura.

### Três tipos de drift

| Drift | Camada | Detecção | Bloqueio |
|---|---|---|---|
| Textual: ausente, inalcançável ou contradita | Meio (testes de intenção) | rodada aplicada ao diff, Jev ou cascata | só contradição |
| Comportamental | Fim (evals) | evals pareados contra versão anterior, modelo/harness fixados | regressão grande ou violação de governança |
| Do avaliador | ambas | versão fixada por release e concordância com humanos | invalida a rodada |

### Testes de intenção (meio)

Predicados distintos: implicada, não contradita, alcançável na rota. Alcançabilidade é parcialmente verificável por código no grafo de links e rotas. Executar sobre o diff como apoio à revisão, nunca como reprovação global do corpus (seria congelamento de prosa por outro meio). Verificam a especificação, não o agente.

### Evals (fim)

Alarme de regressão grande e de violação de governança, não medida fina: com amostra pequena só regressões grandes são detectáveis. Lacunas: comparação pareada com modelo e harness fixados; rotina que transforme falhas reais de consumidores em fixtures sintéticas; cenários reservados contra sobreajuste; métrica de eficiência (guias e tokens carregados por tarefa); usuário simulado em cenários multi-turno como fonte de variância e custo. A maior parte da avaliação deve ser feita por código sobre ações e estado final. Ver cenários S1–S6 em wik-01m4vhpp3xyt.

### Avaliador Jev

Saída tipada com probabilidade calibrada corresponde ao resultado em três estados (atende, viola, inconclusivo); "inconclusivo" por limiar de confiança. Evidência como ponteiro tipado (enum de IDs de trechos, até 255). Adequado para implicação, contradição entre pares de trechos (inviável com LLM, trivial a ~US$ 0,042/M tokens) e sonda de ambiguidade de rota (indício, não prova). Inadequado como agente sob teste, usuário simulado ou juiz de raciocínio longo multi-turno; não reduz o custo dominante dos evals (execução do agente). Riscos: early access, calibração medida contra modelos de fronteira e não no domínio do Wiked, deriva de versão. Mitigações: avaliador como interface (Jev, LLM, humano intercambiáveis), cascata por confiança com limiares medidos contra rótulos humanos, versão fixada por release.

### Testes dos testes

Mutação (apagar ou negar trecho portador deve reprovar a rodada) e concordância com humanos por critério são pré-requisitos para tratar resultado verde como evidência.

### Questões para ideation

Formato e localização do registro de intenções; granularidade das intenções; tipos de saída de cada predicado; política e limiares da cascata; acionamento (grandes mudanças, PRs, pré-release); orçamento; relação com o piloto de wik-01m4vhpp3xyt.

## Notes

**2026-11-06T03:21:33.921614189Z**

**Síntese da ideation (2026-11-06; dialectic, trajetória `ideation`, restrição `semente_mínima, crescimento_composicional`).** Opções e tendências para o grill decidir; não autoriza implementação.

Restrição: a semente deve ser a menor configuração funcional com primitivas existentes; o crescimento deve ter custo marginal baixo por compromisso no fechamento de cada grill, sem redesenho ao escalar.

| Decisão | Opções | Tendência da semente | Quando mudar |
|---|---|---|---|
| Nome | *Methodological commitment* · *Design invariant* · *Consolidated intent* | *Methodological commitment* (evita colisão com o *intent map* do consumidor) | — |
| Formato | YAML único com JSON Schema · Markdown por compromisso · tickets Knot · seção no `metodologia.md` | YAML único com esquema, só no autor e fora do manifesto | dividir se o tamanho atrapalhar a revisão |
| Ponteiro | arquivo + parágrafo localizado na hora · citação com prefixo/sufixo · âncoras na distribuição | arquivo como portador; avaliador devolve IDs de parágrafo | citações quando um arquivo concentrar muitos compromissos; âncoras descartadas (vazam conceito autoral para o consumidor) |
| Gatilho | interseção diff × portadores + varredura de contradição · corpus inteiro | diff para `implied`; varredura completa para `not_contradicted`, só gerando avisos | — |
| Cascata | modo sombra · triagem calibrada · avaliador decide | modo sombra: disposição humana sempre (`metodologia.md`: avisos nunca autorizam decisão semântica automática) | triagem por predicado após N disposições com concordância acima de limiar (N e limiar no grill) |
| Crescimento | campo no resumo de fechamento do grill · revisão periódica | resumo de fechamento lista compromissos novos, alterados e aposentados, ou "nenhum" | — |
| Execução | marcador `pytest` opcional · CLI própria | marcador opcional fora da suíte padrão, como `integration` | — |

Registro mínimo: `id`, `version`, `statement` (inglês, especificação independente da prosa), `lineage`, `carriers`, `routes` (ausente = global), `predicates`, `evals` (vazio = lacuna explícita), `status` (`active` | `retired`). Resultados de rodadas ficam fora do registro (relatório de execução ou nota de ticket).

Predicados no avaliador: `implied` → `{implied, partial, absent}` + p + IDs de parágrafo; `not_contradicted` → por parágrafo `{consistent, contradicts, unrelated}` + p; `infra_error` distinto de falha. Avaliador como contrato `(commitment, passages) → typed verdict`, versão registrada por execução. Custo estimado de uma varredura completa com Jev (~400 parágrafos × 30 compromissos): ~US$ 0,10.

Granularidade: é compromisso aquilo cuja violação um revisor rejeitaria como regressão, independentemente da redação.

Caminho errado descartado: base como instância Wiked do próprio repositório (viola `AGENTS.md` e mistura evidência autoral e consumidora); sobrevive apenas o padrão esquema + validador.

**Adendo: colheita e triagem.**

- A semente vem da colheita dos 40 tickets arquivados, via Knot CLI, começando por `wik-01m4vhmcwene` (lista de comportamentos críticos sem avaliação). A linhagem vem do próprio ticket. A colheita fica adiada para a execução do ticket correspondente; não foi realizada nesta ideation.
- Triagem de cada intenção colhida: determinística → teste unitário `pytest` (sem teste existente = lacuna da suíte); contrato técnico → checagem literal permitida; semântica → base de compromissos. Só a última classe entra na base.
- `reachable` deixa de ser predicado da cascata e vira teste unitário sobre a tabela *Route* do `SKILL.md` e o grafo de links. A cascata fica restrita a `implied` e `not_contradicted`.
- Limite: intenções nunca discutidas em ticket ficam fora da semente até um grill futuro.
- O fixture de avaliação é pré-requisito para o campo `evals` deixar de ficar vazio; a decisão pertence a wik-01m4vhpp3xyt.

Para o grill: nome e entrada no glossário, lista da semente após a colheita, N e limiar do modo sombra, mudança no fluxo de fechamento do grill, caminho do registro, relação com wik-01m4vhpp3xyt.

**2026-11-06T03:25:30.205136921Z**

**Organização e precedência (2026-11-06).**

- Épico não criado: com dois tickets no tema e os links existentes, ele não acrescentaria contexto nem qualidade. Reavaliar quando o grill gerar os tickets de implementação.
- Precedência: wik-01m4vhpp3xyt depende deste ticket. Os dois compartilham o contrato do avaliador, a cascata e o fixture com iscas derivado da colheita; fechar o grill do piloto antes duplicaria o desenho do avaliador. Prioridades mantidas em P2.
- Trabalhos antecipados, não criados para não antecipar o recorte do grill: semente da base (colheita, glossário, mudança no fechamento do grill); testes unitários para lacunas determinísticas e `reachable`; executor da rodada com Jev em modo sombra; fixture de avaliação (no escopo de wik-01m4vhpp3xyt).
- Fora do tema: wik-01m5q082jdqm (critérios de avaliação da recuperação) permanece no épico de recuperação.
- A ideation não está encerrada. O primeiro critério de aceitação fica aberto para o grill refletir e eventualmente complementar as opções registradas.
