---
id: wik-01m6pr00hwgd
title: Especificar a proposta de indexação por informantes e sua importação manual na indexação assistida
status: open
type: feature
priority: 2
mode: hitl
created: '2026-11-05T20:56:49.963885039Z'
updated: '2026-11-05T20:56:49.963885039Z'
tags:
- metodologia
- wiked
- indexacao
- proposta
acceptance:
- title: Methodological grill explicitamente fechado cobrindo exceção de acesso à fonte, ponto de entrada no chatbot, identificação de snapshot, categorias de ratificação, versão do formato e rotas
  done: false
- title: guides/proposal.md conduz o pré-grill somente leitura sem etapas locais, sem qualificação ou ticket e sem suspender invariantes, emitindo exatamente uma proposta sem patches nem prévias
  done: false
- title: Formato versionado da proposta documentado na distribuição, com linhagem, origem por decisão e trecho literal obrigatório para origem na fonte
  done: false
- title: 'assisted-indexing.md ganha a entrada de importação de proposta: reabertura de desatualizadas, perguntas individuais conforme decidido, fechamento integral pelo grill.md e critério de derivabilidade'
  done: false
- title: A distribuição documenta quais arquivos publicar numa skill de chatbot para consulta e proposta, os limites conhecidos desses ambientes e que publicar o snapshot é decisão humana do consumidor
  done: false
- title: Manifesto, CHANGELOG e versão atualizados; Targeted textual checks registrados no ticket
  done: false
links:
- wik-01m4vhpp3xyt
---

## Description

### Problema

Hoje só incorpora conhecimento a uma wiki Wiked quem tem um agente local, o repositório da instância clonado e familiaridade com Git e Knot. Boa parte de quem detém o conhecimento operacional (quem participou da reunião, escreveu a ata ou executa o processo) só tem acesso a chatbots de nuvem: Gemini Gems, ChatGPT Custom GPTs/Projects e Claude Projects. Nesses ambientes não há repositório, Knot, validador, gravação de arquivos nem Git. Por isso o conhecimento chega ao operador de modo informal, e o grill inteiro recai sobre ele, que muitas vezes não é quem conhece melhor o assunto.

Houve uma tentativa de montar, num chatbot de nuvem, um assistente com a wiki e os guias embarcados que conduzia o grill e emitia um "blueprint" de edição. A demanda é real, mas a tentativa tinha três defeitos metodológicos:
1. Desligava a confirmação de qualificação e a exigência de ticket, em vez de reinterpretá-las.
2. Misturava decisões (vigência, responsabilidade, terminologia, divergência, escopo) com patches exatos de Markdown, D2 e glossário, gerados sobre um snapshot sem identificação. Os patches perdem a validade assim que a wiki muda; as decisões em geral continuam válidas.
3. Não tinha linhagem: não registrava a revisão de base nem a versão da metodologia, nem distinguia o que veio da fonte, o que o colaborador declarou e o que o agente inferiu. Diante de patches prontos, o operador só podia aceitar sem verificar ou refazer o grill.

O `guides/grill.md` já separa o interrogatório (reunir decisões) do fechamento (o operador qualificado confirma o entendimento mútuo). O interrogatório pode ser respondido em grande parte por outra pessoa, desde que o fechamento continue com o operador qualificado e cada decisão seja verificável.

### Princípios da proposta original

- A governança se desloca, não se suspende: nenhum conteúdo governado é criado sem ticket aberto e sem fechamento por operador qualificado.
- O informante propõe, o operador decide: as respostas do informante são recomendações, nunca decisões fechadas.
- Decisões, não patches: o texto final é sempre derivado pelo agente do operador sobre a revisão vigente.
- Linhagem explícita: revisão de base, versão da metodologia e origem de cada decisão.
- Neutralidade de ambiente e de canal: o artefato é produzível por qualquer chatbot e entregue por qualquer canal (e-mail, chat, anexo).
- Mudança mínima: um guia novo e uma entrada nova no `assisted-indexing`, sem ramificar o `grill.md`.

### Vocabulário proposto (os termos em inglês nos guias ficam a decidir)

- Informante: conhece a fonte ou a operação e responde ao pré-grill. Não governa o conteúdo nem declara qualificação.
- Operador qualificado: papel já existente, que declara qualificação, conduz a importação e fecha o grill.
- Pré-grill: interrogatório somente leitura com o informante. Produz decisões propostas e nunca fecha um grill.
- Proposta de indexação (indexing proposal): artefato único com decisões propostas, evidências, plano de destino e linhagem. Não é conteúdo governado nem evidência operacional.

### Escopo deste ticket (só instruções e formato; nenhum script)

1. Novo guia `guides/proposal.md`, carregado em ambiente somente leitura sem repositório, Knot, validador, Git ou gravação:
   - declara explicitamente que as etapas locais não se aplicam, para que as instruções do ambiente não precisem contorná-lo;
   - não exige qualificação nem ticket, porque não cria conteúdo governado;
   - registra que o participante atua como informante;
   - faz preparação equivalente à do `authoring-context.md` sobre o snapshot embarcado (contexto, referência de autoria, índice raiz, navegação seletiva);
   - exige o confronto (afirmação da fonte, operação atual, mudança proposta, divergência não resolvida, sem valor operacional);
   - usa a mecânica do `grill.md` (árvore, fronteira, rodadas) por referência, sem duplicá-la; "não sei" e "não cabe a mim" levam a decisão para "Questões em aberto";
   - no fechamento do pré-grill, o informante confirma que o resumo reflete o que declarou, e essa confirmação não equivale ao fechamento do grill;
   - a saída é exatamente uma proposta. Patches de texto, D2 ou glossário e prévias do texto final são proibidos.
2. Formato da proposta: um único Markdown com frontmatter YAML, escolhido por ser o formato que todo chatbot emite com confiança (ZIP, hash e branch não são portáveis). Esboço original:
   - frontmatter: `proposal_version`, `snapshot_id`, `methodology_version`, `objective`, `sources[]` (name, kind, origin, date ou "unavailable") e `informant.relation`;
   - seções: Objetivo e escopo; Confronto; Decisões propostas; Plano de destino; Termos propostos; Pendências e propostas de mudança; Questões em aberto;
   - cada Dn traz categoria (vigência | responsabilidade | terminologia | divergência | escopo | estrutura | rota), decisão proposta, origem (fonte, com trecho literal e localização | informante | inferência do agente aceita pelo informante), páginas afetadas e alternativas descartadas;
   - o Plano de destino indica página, seção e afirmações a consolidar, sem texto final;
   - regras: decisão com origem na fonte exige trecho e localização; `snapshot_id` é obrigatório; a proposta não traz hashes.
3. Nova entrada "importar proposta" no `guides/assisted-indexing.md`. Os passos atuais de entrada continuam valendo (ticket, `grill.md`, preparação contextual), e a importação acrescenta:
   - o ticket registra a proposta como material do objetivo (governança, não evidência);
   - decisões cujas páginas afetadas mudaram desde o snapshot são reabertas;
   - as decisões propostas formam a fronteira inicial, cada uma apresentada como recomendação;
   - decisões desatualizadas, inferidas ou em aberto exigem pergunta individual;
   - as demais admitem ratificação em bloco, sempre com a opção "reabrir Dn";
   - o fechamento segue integralmente o `grill.md`;
   - critério de derivabilidade: se a consolidação exigir uma decisão que a proposta não cobre, o trabalho para e o grill é retomado.

   O ganho vem da fronteira já calculada e das evidências já ancoradas, não de pular decisões.
4. Documentação de publicação manual numa skill de chatbot (ver "Questão de publicação" abaixo), já que neste ticket não há gerador de pacote.

Fica fora de escopo, por ter ido para o ticket de automação: o script de importação, o gerador de pacote portátil com manifesto, os perfis de adaptador por ambiente e a avaliação ponta a ponta. Também fica fora: patches produzidos fora do ambiente do operador, qualificação do informante, serviços com credenciais Git, criação automática de branch ou PR e canais de submissão específicos.

### Achados da revisão metodológica (2026-11-05) a resolver no grill

- Conflito com o `assisted-indexing.md` (Entry: "Before these conditions hold, do not access a source or change the wiki") e com o `query.md` (proíbe inspecionar material de ingestão). O pré-grill lê a fonte antes de haver ticket. Recomendação: uma exceção limitada e explícita no `proposal.md`, nos moldes da "Bounded Grill Exception" do `export.md`, restrita à fonte entregue pelo informante, sem escrita e com saída que não é evidência.
- O Start do `SKILL.md` exige a raiz do repositório, `wiki/wiki-structure.yaml` e `../../wiked-manifest.yaml`, e não roda num chatbot. Não se pode criar um segundo ponto de entrada que reescreva regras (o `AGENTS.md` proíbe wrappers e regras duplicadas). Recomendação: um adaptador fino, como o `wiked-setup`, que só troca a resolução de contrato e versões e delega aos guias inalterados.
- `snapshot_id` como commit esbarra em "Never manipulate Git" e exige que o importador obtenha o estado daquele commit. Sem script, decidir o que identifica o snapshot e como o operador detecta desatualização manualmente. Recomendação: um identificador registrado por quem publica o snapshot e guardado fora de `wiki/`; o commit entra só como informação preenchida por um humano.
- A ratificação em bloco não precisa alterar a mecânica do `grill.md` (que o `assisted-indexing` declara autoridade única): cada Dn entra na primeira rodada como pergunta numerada com a recomendação do informante, e o operador pode responder "aceito Q3 a Q9". Recomendação: vigência, responsabilidade e divergência sempre com pergunta individual; terminologia, estrutura e escopo podem ser ratificados em bloco.
- A desatualização baseada só em "páginas afetadas" depende de uma lista montada pelo chatbot, que pode estar incompleta, e não percebe mudanças no context file, nos índices ou em páginas novas que cubram o assunto. Uma importação "válida" não prova que a proposta está atual.
- O operador pode conferir se cada trecho literal citado existe na fonte, nos formatos textuais. Isso mede a fidelidade do chatbot.
- Destino da proposta: sugerido `raw/<slug>/` junto com as fontes, arquivado com elas e registrado no ticket. A proposta não gera página de fonte (Consolidate, passo 1).
- Publicar o snapshot da wiki num serviço de terceiros é decisão humana do consumidor (confidencialidade), sem padrão implícito.
- Chatbots de nuvem costumam carregar todos os arquivos de conhecimento de uma vez, o que limita o carregamento progressivo. A documentação deve declarar isso.
- Versionamento: recomenda-se `proposal_version` independente, como o `contract_version`, aceito pela distribuição, com a proposta carregando também a `methodology_version`.
- Rotas de intenção: recomenda-se incluí-las na v1 como categoria `rota`, por serem só recomendações. A dificuldade de localização observada numa consulta pelo chatbot é um gatilho que o `assisted-indexing` já admite.

### Questão de publicação (decidir no grill)

Com só este ticket implementado, o consumidor precisa de documentação, dentro da distribuição (a skill deve funcionar sem `docs/`), que diga quais arquivos publicar numa skill de chatbot para os modos consulta e proposta. Há duas alternativas: publicar toda a skill `wiked` ou um subconjunto dos guias.

Ponto de partida para o grill: um subconjunto.
- Necessários:
  - `query.md`, `proposal.md` e `authoring-context.md`;
  - o `grill.md`, se o `proposal.md` referenciar sua mecânica;
  - o `modeling.md`, se o plano de destino depender das fronteiras de página;
  - o formato da proposta;
  - o adaptador fino que substitui o Start do `SKILL.md`;
  - a instância: `wiki/` (incluindo `wiki-structure.yaml`, context file e índices) e uma identificação do snapshot e da versão.
- Excluídos (exigem ambiente local ou governança, ou não servem aos dois modos):
  - `assisted-indexing.md`, `maintenance.md`, `setup.md`, `knot.md`, `d2.md`, `docsify.md` e `export.md`;
  - `scripts/` e `viewers/`;
  - `raw/` e `.tickets/`.

Riscos a pesar:
- Publicar a skill inteira expõe instruções que o chatbot não consegue cumprir.
- O `grill.md` traz a exigência de qualificação, que o `proposal.md` precisa neutralizar explicitamente para o pré-grill.
- Um subconjunto cria uma lista que precisa ser mantida em sincronia com a evolução dos guias. Avaliar se ela fica no `proposal.md` ou num documento próprio, e como se relaciona ao manifesto.

### Critérios de aceite da proposta original (adaptados a este ticket)

- O `proposal.md` conduz o pré-grill sem ferramentas e sem etapas locais, sem que uma instrução externa precise suspender invariantes.
- Uma proposta válida importada pelo `assisted-indexing` chega ao fechamento com perguntas individuais apenas para decisões desatualizadas, inferidas, em aberto e das categorias que o grill decidir.

Validação: Targeted textual checks (o ticket é só de instruções). A avaliação comportamental ponta a ponta exige escopo próprio (ver wik-01m4vhpp3xyt) e não substitui o grill.
