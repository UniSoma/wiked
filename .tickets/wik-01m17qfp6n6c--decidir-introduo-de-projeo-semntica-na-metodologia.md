---
id: wik-01m17qfp6n6c
title: Decidir introdução de projeção semântica na metodologia
status: open
type: task
priority: 3
mode: hitl
created: '2026-08-29T21:40:49.491848512Z'
updated: '2026-10-10T18:40:22.489098946Z'
assignee: VolneiSantos
tags:
- metodologia
- knowledge-graph
- arquitetura
acceptance:
- title: Conduzir e encerrar Sessão de grill metodológica com a autoridade solicitante
  done: false
- title: Decidir autoridade, limites e fallback da projeção semântica
  done: false
- title: Definir modelo mínimo de nós, relações, ocorrências e identidade para um piloto
  done: false
- title: Definir integração da projeção nos fluxos de consulta, indexação, grill e consistência
  done: false
- title: Definir contrato da CLI e do manifesto explicável de contexto
  done: false
- title: Definir piloto, perguntas de competência, métricas e critério de adoção
  done: false
- title: Registrar decisão final e abrir trabalhos de implementação separados se aprovados
  done: false
---

## Description

## Objetivo

Avaliar e decidir se a metodologia da wiki deve incorporar uma projeção semântica pequena, determinística e derivada da `Wiki operacional`, possivelmente acompanhada por uma CLI, para melhorar roteamento de contexto, consultas relacionais, análise de impacto e escalabilidade sem criar uma segunda fonte de verdade.

## Motivação

A wiki já funciona como um grafo documental tipado: páginas representam entidades, links representam conexões, o frontmatter declara tipos e estados, o Contrato estrutural da wiki valida invariantes e as Páginas de fonte mantêm proveniência bidirecional. Entretanto, a maior parte das relações operacionais permanece em prosa ou em campos Markdown cujo significado não é projetado como predicado consultável.

A navegação atual começa obrigatoriamente no Índice principal, segue Troncos e Subíndices e só então abre páginas. Essa estratégia evita varredura integral, mas tende a perder eficiência quando a wiki cresce, quando uma pergunta atravessa vários Troncos ou quando a relevância depende de relações como responsabilidade, participação, uso de artefato e proveniência. Uma projeção pode desacoplar parcialmente o tamanho total da wiki do contexto necessário para cada atividade.

## Resultado esperado

Uma decisão metodológica explícita, tomada em Sessão de grill metodológica, sobre adoção, limites de autoridade, modelo mínimo, integração nos fluxos, piloto e critérios de sucesso. Se adotada, a decisão deve produzir trabalho posterior separado para contrato semântico, CLI, validação, testes e alterações nos guias; este ticket não autoriza por si só a implementação nem mudanças no conteúdo governado.

## Escopo

- Projeção operacional derivada exclusivamente de Markdown sob `wiki/`.
- Entidades, relações tipadas, referências genéricas e ocorrências rastreáveis.
- Roteamento de contexto para consulta, indexação assistida e consistência.
- Papel do glossário, Índice principal, Troncos e busca textual como bootstrap ou fallback.
- CLI determinística e manifesto explicável de páginas e seções.
- Estratégia de sincronização, validação, cobertura e falha segura.
- Piloto e métricas de qualidade, contexto e manutenção.

## Fora de escopo inicial

- Substituir Markdown por banco de grafos.
- Usar o KG como evidência operacional autônoma.
- Extrair fatos diretamente de fontes brutas para o grafo.
- Inferir relações operacionais de prosa por LLM.
- Introduzir ontologia completa, OWL, embeddings, GraphRAG ou banco de grafos antes de demonstrar necessidade.
- Automatizar decisões humanas sobre significado, responsabilidade, vigência, divergência ou Proposta de mudança.

## Design

## Síntese das descobertas

Os tipos, estados, campos e exemplos abaixo são uma proposta histórica ilustrativa e autocontida, não o contrato universal do Wiked. Revalidar o desenho contra a distribuição vigente. Nenhuma página de uma instância real é necessária para retomar este ticket.

### Paralelo com knowledge graphs

A metodologia já contém vários elementos de um knowledge graph em sentido amplo:

- páginas tipadas como `macroprocesso`, `area`, `artefato`, `fonte`, colegiados e `operacional`;
- estados como `operacao-atual`, `proposta-de-mudanca`, `indexada` e `sem-conteudo-operacional`;
- links internos e topologia de navegação;
- proveniência bidirecional entre página operacional e Página de fonte;
- Citações contextuais;
- validação estrutural por contrato legível por máquina;
- evolução incremental e curadoria humana.

A base é hoje melhor descrita como grafo documental tipado, ou knowledge graph fraco. Ela é amplamente `machine-checkable`, mas apenas parcialmente `machine-queryable`.

### Limitações observadas

- Links Markdown normalmente não declaram se significam `participaDe`, `responsavelPor`, `usa`, `produz`, `governa`, `precede` ou apenas referência textual.
- `Etapa` costuma ser um heading H3 e não um nó com identidade estável.
- Ordem, paralelismo, condição, exceção e caminhos alternativos ficam em prosa.
- `type: operacional` agrupa políticas, papéis, ferramentas, orçamentos e playbooks.
- A proveniência é principalmente por página, não por afirmação.
- Não há IDs conceituais independentes de caminhos, títulos ou fragments.
- Não há consulta relacional ou análise de impacto sistemática.
- Atualidade, prevalência de fontes e divergências continuam decisões humanas.

### Princípio recomendado

A projeção deve compilar declarações editoriais controladas, nunca interpretar silenciosamente a prosa:

> O predicado é determinado por uma seção ou campo normatizado; o objeto é determinado por link explícito; prosa livre não gera relação operacional tipada.

Exemplos determinísticos:

- página `type: macroprocesso` -> nó `Macroprocesso`;
- H3 dentro de `## Etapas` -> nó `Etapa`;
- contenção -> `Macroprocesso temEtapa Etapa`;
- `Responsável pela etapa` -> `responsavelPelaEtapa`;
- `Envolvido na etapa` -> `envolvidoNaEtapa`;
- `Artefatos` -> inicialmente `relacionaArtefato`;
- `## Fontes` -> `fundamentadaPor`;
- `Páginas fundamentadas` -> relação inversa `fundamenta`.

O campo genérico `Artefatos` não permite distinguir deterministicamente `usa`, `produz` e `atualiza`. Essa distinção só deve ser projetada depois que o Markdown declarar campos diferentes, como `Artefatos de entrada`, `Artefatos produzidos` e `Artefatos atualizados`.

### Relação genérica de referência

Todo link Markdown interno para um nó conhecido pode gerar uma ocorrência documental genérica. Recomenda-se o predicado `referencia`, e não `cita`, para evitar conflito terminológico com `Citação contextual`.

Semântica deliberadamente fraca:

> A página contém um link explícito para o nó, sem afirmar a natureza operacional da relação.

Relações tipadas podem ser tratadas como especializações conceituais de `referencia`. Links de índices devem ser classificados separadamente como `indexa` ou `navegaPara`, para não poluir consultas de conteúdo. Links para fontes fora de `## Fontes` podem ser classificados como `citaContextualmente`, conforme a regra metodológica existente.

Cada ocorrência deve preservar:

- página de origem;
- nó de destino;
- relação ou classificação;
- seção e heading;
- linha ou posição no AST;
- contexto como prosa, campo estruturado, proveniência ou navegação.

Assim, uma aresta agregada `Página referencia Nó` pode ser derivada sem perder múltiplas ocorrências e seus contextos.

### Identidade

Links devem identificar os objetos das relações. Valores apenas textuais podem gerar warning, mas não devem ser ligados por similaridade. Conceitos canônicos sem página própria podem ser referenciados por anchors do `wiki/CONTEXT.md` ou, futuramente, por IDs explícitos.

Etapas podem usar inicialmente `caminho-da-pagina#fragmento` como identidade. Se passarem a receber relações externas ou forem renomeadas com frequência, devem ganhar ID estável explícito.

## Arquitetura recomendada

```text
Fontes primárias
       |
       v
Indexação assistida + validação humana
       |
       v
Wiki Markdown canônica
       |
       +--> Validação documental
       |
       +--> Extração determinística
                    |
                    v
            Projeção semântica
                    |
                    +--> roteamento de contexto
                    +--> consultas relacionais
                    +--> análise de impacto
                    +--> consistência
```

Invariantes propostas:

- `wiki/` permanece a única fonte de evidência operacional.
- A projeção é índice derivado, descartável e regenerável.
- Toda relação aponta para sua ocorrência canônica no Markdown.
- Respostas nunca são fundamentadas apenas na saída da projeção.
- Consulta não escreve de volta na wiki.
- Fontes brutas não alimentam diretamente o grafo operacional.
- Tickets pertencem à governança e não se tornam evidência.
- Ausência de aresta significa ausência de declaração projetada, não falsidade operacional.
- Inferências automáticas devem ser mínimas, declaradas, auditáveis e desativáveis.

## Mudança de navegação recomendada

Substituir, quando a projeção estiver válida, `índice primeiro` por `roteamento semântico primeiro`, sem tornar o grafo exclusivo:

```text
Protocolo e glossário
  -> resolução de entidades
  -> projeção semântica
  -> manifesto de páginas e seções
  -> leitura do Markdown canônico
  -> expansão pelo grafo
  -> índices e busca textual como fallback
```

O glossário precede o grafo para preservar identidade e terminologia. Índice principal, Troncos e Subíndices continuam necessários para perguntas sem entidade inicial clara, descoberta ampla, navegação humana, conferência editorial e fallback quando a cobertura do grafo for insuficiente.

## Integração por fluxo

### Consulta

1. Carregar protocolo, `CONTEXT-MAP.md`, `wiki/CONTEXT.md` e guia aplicável.
2. Verificar validade e cobertura da projeção.
3. Resolver termos da pergunta em nós canônicos.
4. Selecionar um perfil de relações e orçamento de expansão.
5. Gerar manifesto explicável com `must_read`, `may_read` e `fallback`.
6. Ler páginas e seções canônicas indicadas.
7. Expandir se a evidência for insuficiente.
8. Responder somente com evidência efetivamente lida e listar as Páginas consultadas.

Relações tipadas devem ter prioridade maior que `referencia`; `indexa` e `navegaPara` normalmente ficam fora da expansão operacional.

### Indexação assistida

1. Confirmar ticket, fontes, escopo e participação do `Mantenedor de conteúdo` antes de acessar fontes.
2. Resolver o escopo pelo glossário.
3. Explorar relações diretas, inversas, proveniência e referências genéricas para localizar páginas potencialmente afetadas.
4. Ler essas páginas antes de comparar a Fonte primária.
5. Conduzir e fechar o grill operacional.
6. Consolidar primeiro no Markdown.
7. Validar e reconstruir a projeção.
8. Revisar diff semântico de nós e relações e reavaliar páginas afetadas.

O grafo não recebe fatos da Fonte primária antes da consolidação humana.

### Grill

Usar o subgrafo para preparar páginas afetadas, relações existentes, possíveis conflitos, termos sem identidade e perguntas de decisão. O grafo não decide prevalência de fonte, responsabilidade, vigência, escopo nem natureza organizacional das relações.

### Consistência e manutenção estrutural

Usar o grafo como objeto de análise para encontrar:

- etapas sem responsável;
- destinos com tipo incompatível;
- valores textuais sem links;
- relações sem ocorrência de origem;
- proveniência sem reciprocidade;
- nós isolados;
- fragments inexistentes;
- relações inversas inconsistentes;
- diferenças entre índices e entidades projetadas;
- nós excessivamente centrais por abuso de `referencia`.

Achados semânticos permanecem candidatos a decisão humana e não autorizam correção automática.

### Evolução metodológica

Manter separados o grafo operacional derivado de `wiki/` e a governança definida por `AGENTS.md` e `docs/`. A projeção pode mostrar impactos e exemplos na wiki, mas não deve transformar os documentos metodológicos em evidência operacional.

## CLI mínima recomendada

A CLI inicial deve oferecer primitivas determinísticas, não uma interpretação opaca de perguntas abertas:

```text
kg status
kg search "Plano de Projeto"
kg show artefatos/plano-de-projeto
kg references artefatos/plano-de-projeto
kg neighbors artefatos/plano-de-projeto
kg context --profile consulta --seed artefatos/plano-de-projeto
kg impact --seed artefatos/plano-de-projeto
kg validate
```

Capacidades:

- `status`: integridade, versão do esquema e sincronização;
- `search`: labels, aliases e IDs;
- `show`: tipo, relações e ocorrências;
- `references`: referências genéricas e seus contextos;
- `neighbors`: travessia explicitamente parametrizada;
- `context`: manifesto com orçamento e explicação;
- `impact`: relações inversas e páginas candidatas;
- `validate`: contrato semântico, cardinalidades e cobertura.

Parâmetros esperados: `--relation`, `--direction`, `--max-hops`, `--max-pages`, `--include-generic-references`, `--state`, `--explain` e `--format json|markdown`.

### Manifesto de contexto

A CLI deve retornar, para cada página ou seção:

- motivo da seleção;
- caminho relacional;
- distância do nó inicial;
- relação responsável;
- prioridade de leitura;
- warnings de cobertura;
- fallback recomendado.

A saída não é resposta operacional; é plano auditável de leitura.

### Persistência inicial

Recomendação inicial: construir a projeção em memória a partir do Markdown atual a cada comando composto, sem gravar arquivos. Isso evita cache obsoleto, segunda fonte de verdade, serviço externo e conflito com consulta somente leitura. Persistência em SQLite ou outro formato deve ser considerada apenas depois de medir custo real e exigir fingerprint/verificação de sincronização.

## Escalabilidade esperada

A projeção pode fazer com que o contexto médio dependa da vizinhança relevante, e não do número total de páginas:

```text
sem roteamento: contexto ~ páginas potencialmente relacionadas
com roteamento: contexto ~ subgrafo relevante e limitado
```

Controles necessários:

- máximo de saltos;
- máximo de páginas;
- fan-out por relação;
- preferência por `operacao-atual`;
- prioridade de relações tipadas;
- penalização de nós muito centrais;
- exclusão padrão de navegação;
- seleção por seção;
- expansão progressiva.

O KG melhora principalmente escalabilidade de consulta, análise de impacto e consistência. Ele não reduz por si só o custo humano de Indexação assistida, grill, resolução de divergências e manutenção do vocabulário.

Perguntas globais podem exigir agregações ou resumos de comunidades. GraphRAG é uma referência possível para esse caso, mas não deve ser ponto de partida; qualquer resumo derivado serve para roteamento e deve levar de volta ao Markdown canônico.

## Riscos

- Criar uma segunda fonte de verdade ou cache silenciosamente obsoleto.
- Formalizar cedo demais uma ontologia ampla e cara de manter.
- Inferir de modo incorreto vinculação, responsabilidade, precedência ou vigência.
- Confundir ausência de relação com negação.
- Sobrecarregar o contexto com nós centrais e referências genéricas.
- Reduzir recall ao confiar em cobertura semântica ainda parcial.
- Duplicar informação entre corpo Markdown e metadados laterais.
- Permitir que extração por LLM consolide interpretação não validada.

Mitigações: projeção derivada, ocorrências rastreáveis, falha explícita, fallback obrigatório, cobertura declarada, orçamento de travessia e autoridade exclusiva do Markdown.

## Piloto sugerido

Começar apenas com:

Entidades:

- `Macroprocesso`;
- `Etapa`;
- `Área`;
- papel;
- `Artefato`;
- ferramenta;
- `Página de fonte`.

Relações:

- `temEtapa`;
- `responsavelPelaEtapa`;
- `envolvidoNaEtapa`;
- `relacionaArtefato`;
- `fundamentadaPor`;
- `referencia` com classificação de ocorrência.

Perguntas de competência:

1. Quais etapas são responsabilidade de determinada Área ou papel?
2. Quais processos usam ou se relacionam com determinado artefato?
3. Quais páginas seriam candidatas a impacto por mudança em ferramenta ou artefato?
4. Quais páginas e afirmações sensíveis ao tempo são fundamentadas por determinada fonte?
5. Quais etapas não têm responsável ou artefatos formalizados?
6. Quais páginas referenciam um nó e em que contexto?

Métricas:

- páginas candidatas e efetivamente carregadas;
- tokens de contexto por resposta correta;
- precisão e recall das páginas selecionadas;
- relações relevantes omitidas;
- páginas irrelevantes incluídas;
- rastreabilidade das respostas;
- tempo de consulta;
- custo editorial adicional;
- divergência entre Markdown e projeção;
- cobertura de relações tipadas versus referências genéricas.

A adoção só deve avançar se reduzir contexto sem perda relevante de recall e sem criar manutenção desproporcional.

## Decisões que exigem HITL

- Nome canônico da projeção e de seus conceitos metodológicos.
- Se o grafo será primeiro passo obrigatório ou preferencial quando válido.
- Quais tipos de nós e predicados entram no piloto.
- Como identificar conceitos do glossário sem página própria.
- Quando uma Etapa precisa de ID estável.
- Se relações tipadas são também materializadas como `referencia` ou tratadas por hierarquia de predicados.
- Política de cobertura, exaustividade e fallback.
- Critérios de erro versus warning.
- Forma do manifesto de contexto e orçamento padrão por fluxo.
- Estratégia de persistência após o piloto.
- Como integrar geração e validação sem contrariar a natureza somente leitura do validador atual.

## Arquivos metodológicos potencialmente afetados após decisão

- `AGENTS.md`;
- `docs/metodologia.md`;
- `docs/CONTEXT.md`;
- `.agents/skills/wiked/guides/query.md`;
- `.agents/skills/wiked/guides/assisted-indexing.md`;
- `.agents/skills/wiked/guides/modeling.md`;
- `.agents/skills/wiked/contracts/wiki-structure.schema.json`;
- validador e testes, se houver implementação.

## Referências para retomada

Origem autoral: `docs/CONTEXT.md`, `docs/metodologia.md`, distribuição em `.agents/skills/wiked/` e testes sintéticos. Os exemplos de processo, etapa, papel e artefato descritos neste ticket bastam como casos ilustrativos; qualquer piloto real exige seleção e autorização próprias. Pesquisa complementar não normativa: `reports/investigacao-wiked.md` v1.1.

Referências externas consultadas durante a análise:

- Hogan et al., Knowledge Graphs: https://arxiv.org/abs/2003.02320
- W3C RDF Concepts: https://www.w3.org/TR/rdf12-concepts/
- W3C SHACL: https://www.w3.org/TR/shacl/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- W3C SPARQL: https://www.w3.org/TR/sparql11-query/
- Wikidata Data Model: https://www.wikidata.org/wiki/Wikidata:Data_model
- Edge et al., GraphRAG: https://arxiv.org/abs/2404.16130

## Notes

**2026-10-10T18:40:22.489098946Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.
