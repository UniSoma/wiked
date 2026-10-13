---
id: wik-01m4rt9yj681
title: Introduzir mapa opcional de rotas por intenção no Wiked
status: closed
type: feature
priority: 3
mode: hitl
created: '2026-10-12T19:44:17.985562759Z'
updated: '2026-10-13T19:11:43.979894818Z'
closed: '2026-10-13T19:11:43.979894818Z'
tags:
- metodologia
- wiked
- navegacao
- modelagem
acceptance:
- title: Decisões e fechamento do Methodological grill preservados; detalhes técnicos e compatibilidade documentados, com reabertura explícita para qualquer nova escolha substantiva
  done: true
- title: Contrato e runtime suportam mapa Markdown opcional, apartado, não operacional e integrado ao índice principal, preservando instâncias sem mapa e migrações explicitamente autorizadas
  done: true
- title: Formato comum exige intenção, destinos canônicos e orientação por destino; mapa permite links repetidos/transversais sem relaxar as invariantes dos índices
  done: true
- title: Guia de consulta explicita os dois gatilhos de carregamento seletivo, fallback e fundamentação exclusiva em conteúdo canônico efetivamente consultado
  done: true
- title: Criação/alteração de rotas segue indexação com curadoria e autoridade editorial; oportunidades em consulta são apenas sinalizadas, sem presumir autoridade, escrita ou autorização para iniciar alterações
  done: true
- title: Indexação e manutenção documentam gatilhos de proposta, carregamento na autoria e revisão das rotas diretamente afetadas, sem revisão integral ou expansão silenciosa de escopo
  done: true
- title: Testes sintéticos cobrem opcionalidade, formato/referências, destinos repetidos/transversais no mapa e preservação das restrições dos índices; cenários de consulta sem escrita e sem autoridade são verificados textualmente
  done: true
- title: uv run pytest e verificações textuais aplicáveis têm evidência registrada; instruções/runtime permanecem genéricos em inglês, sem consumidor obrigatório ou dependência de docs/ na instalação
  done: true
links:
- wik-01m17qfp6n6c
---

## Description

### Objetivo
Introduzir uma capacidade opcional e padronizada de navegação por intenção: um documento Markdown apartado, declarado no contrato da instância e vinculado pelo índice principal, que associe necessidades dos leitores a pontos de consulta canônicos sem substituir os índices nem fornecer evidência operacional.

### Problema e motivação
A navegação progressiva atual funciona para quem conhece a taxonomia da wiki, mas uma pergunta como 'onde encontro orientações para encerrar um projeto?' exige conhecimento de domínio para selecionar processos, artefatos e outros destinos. Acrescentar atalhos livremente aos índices pode repetir links ou atravessar troncos, contrariando suas invariantes. Orientação genérica ao agente não basta: as associações concretas intenção→destinos precisam estar registradas na instância e passar por curadoria humana.

O runtime atual exige exatamente um link por destino nos índices. A raiz admite as referências configuradas e índices de tronco; os índices de diretório admitem páginas imediatas e subíndices. A evolução deve preservar essas regras para os índices, acrescentando somente a integração explícita do novo auxiliar opcional na raiz e regras próprias para o mapa.

### Decisões aprovadas e fechamento do Methodological grill
Em 2026-10-12, o solicitante confirmou explicitamente a síntese final do grill metodológico nesta conversa e autorizou criar este ticket detalhado. O objetivo, limites e comportamento abaixo representam o entendimento compartilhado. Este registro não afirma implementação, validação técnica concluída ou autorização para operações em consumidores. Novas escolhas substantivas na execução devem reabrir o grill antes de alterar conteúdo governado.

1. Rotas podem ter múltiplos destinos, inclusive em diferentes troncos, preservando a organização canônica das páginas.
2. A representação é Markdown compartilhado por pessoas e agentes; a adoção é opcional, mas segue uma convenção comum do Wiked.
3. O conjunto é pequeno e curado, orientado por necessidades recorrentes, importantes ou de localização difícil, sem cobertura exaustiva.
4. Cada rota contém uma intenção, um ou mais links para páginas ou índices canônicos e uma breve orientação por destino. Vocabulário e associações pertencem ao domínio da instância.
5. O mapa é documento apartado, declarado no contrato e identificado/vinculado pelo índice principal. Não reutilizar a referência local de autoria como mapa de domínio.
6. Destinos podem se repetir entre rotas e atravessar troncos exclusivamente no mapa. Não relaxar a unicidade ou os destinos permitidos dos índices existentes.
7. O mapa oferece pontos de consulta, não uma sequência operacional nem garantia de completude. Não reproduz procedimentos, atribui responsabilidades ou acrescenta regras operacionais. Limitações relevantes de cobertura devem ser explicitadas, não compensadas por orientação inventada.
8. O mapa não é evidência operacional. Respostas permanecem fundamentadas nas páginas canônicas efetivamente lidas; a existência de uma rota não prova o conteúdo de uma resposta.
9. Consultas carregam o mapa quando a pergunta expressa tarefa/necessidade sem indicar página ou destino conhecido, ou quando os índices não localizam o assunto/deixam dúvida sobre quais troncos consultar. Consultas com destino conhecido mantêm o percurso atual; o mapa não deve ser carregado indiscriminadamente em toda consulta.
10. Autoria carrega o mapa ao propor rotas ou conferir associações afetadas pelas alterações. Os índices e a busca continuam atendendo intenções não registradas.
11. Registrar ou alterar rotas é processo de indexação com autoridade editorial, curadoria humana e governança existente. O agente pode propor; a autoridade competente valida a pertinência e a sustentação das orientações.
12. Gatilhos para propostas: pedido humano explícito; dificuldade concreta de localização observada em consulta; necessidade relevante sem rota ou rota afetada identificada durante indexação/manutenção. Não criar uma rota por pergunta ou página nova.
13. Durante consulta, o agente apenas sinaliza a oportunidade e explica que registrar a rota para consultas futuras é indexação que exige autoridade editorial. Não presume que o consulente possua essa autoridade, que exista acesso de escrita ou que a consulta autorize iniciar indexação, escrever no mapa ou criar registros de governança.
14. Alterações nas páginas exigem conferir as rotas diretamente afetadas. Renomeações/remoções demandam verificar referências; mudanças de conteúdo demandam avaliar se as orientações continuam corretas. Não exigir revisão integral do mapa a cada alteração.
15. Validação automática confere estrutura e referências. Humanos verificam significado, pertinência e sustentação das orientações; o validador não determina utilidade, completude ou verdade operacional.

### Escopo autoral
- Guias distribuídos de modelagem, consulta, indexação assistida, manutenção e setup; revisar o roteamento e as invariantes do SKILL.md quando afetados.
- Metacontrato e runtime: integração opcional, fronteira não operacional, formato mínimo e referências do mapa.
- Testes sintéticos e documentação das interfaces afetadas.
- Manifesto/compatibilidade da distribuição e contexto autoral apenas quando necessários à mudança coerente.

### Fora de escopo
- Preencher mapas, alterar taxonomia ou operar conteúdo de consumidores reais.
- Relaxar genericamente as regras dos índices ou criar variantes locais da metodologia.
- Implementar projeção semântica, knowledge graph, embeddings, busca semântica completa/determinística ou roteamento exaustivo.
- Criar segunda fonte de verdade, inferir fatos operacionais para completar lacunas ou transformar orientação de navegação em procedimento.
- Instalar ferramentas, substituir skills instaladas, manipular Git ou publicar releases por agente.

### Relação com outra evolução
Relacionado a wik-01m17qfp6n6c, que avalia projeção semântica e roteamento de contexto. Este ticket resolve uma capacidade editorial menor e independente; a relação é contextual, sem dependência de implementação ou adoção da projeção.

## Design

### Interfaces e restrições verificadas
- distr/agents/skills/wiked/scripts/validate_wiki.py: validate_navigation e internal_markdown_targets. A contagem atual considera o arquivo de destino, mesmo em links para fragmentos distintos, e aplica as regras ao índice inteiro, sem exceção por seção.
- distr/agents/skills/wiked/contracts/wiki-structure.schema.json: navigation atualmente aceita root_index, trunk_index, context_file e authoring_file, com additionalProperties desativado. Um auxiliar configurado novo exige evolução explícita; exceção de frontmatter não autoriza, sozinha, um arquivo reservado na raiz.
- distr/agents/skills/wiked/guides/query.md: contexto e raiz → índices relevantes → páginas/referências → busca textual quando a navegação não localiza. Não usar a referência de autoria para consulta.
- distr/agents/skills/wiked/guides/modeling.md: contrato é autoridade estrutural; critérios locais de autoria não redefinem significado de domínio; Markdown operacional permanece canônico.
- distr/agents/skills/wiked/guides/assisted-indexing.md e maintenance.md: autoria governada e atualização de páginas/índices após fechamento do grill; incorporar a revisão das rotas afetadas sem ampliar silenciosamente o escopo.
- distr/agents/skills/wiked/guides/setup.md: materialização e migração explicitamente autorizadas; preservar instâncias sem mapa e evitar criação de conteúdo fictício.
- tests/test_wiked_validator.py: estender cobertura existente de navegação, autoria e contratos com fixtures genéricas, sem domínio de consumidor real.

### Preparação da execução
Definir nome/caminho configurável, chave opcional de contrato, sintaxe Markdown mínima e estratégia de versão/compatibilidade coerentes com as decisões aprovadas. Não converter detalhes técnicos em escolhas semânticas silenciosas: se uma alternativa alterar carga seletiva, autoridade, papel de evidência, regras dos índices ou transição dos consumidores, reabrir o Methodological grill e obter confirmação explícita.

Preservar o comportamento de instâncias que não adotam o mapa. Não materializar mapa vazio/fictício automaticamente nem migrar contratos existentes sem autorização. A fronteira de navegação deve ser explícita nos guias e no runtime, evitando atribuir papel operacional ao auxiliar.

### Cenários de verificação
- Instância sem mapa preserva validação e navegação existentes.
- Instância com mapa declarado integra o auxiliar na raiz e valida estrutura/referências; destinos repetidos entre rotas e links transversais são aceitos no mapa.
- Links repetidos e atalhos fora dos destinos permitidos continuam diagnosticados nos índices; incluir regressão com duplicação entre seções e links para fragmentos distintos do mesmo destino.
- Mapa ausente quando declarado, configuração inválida, rota sem intenção/destino/orientação exigida e referência inexistente têm diagnóstico coerente. Destinos de ingestão, governança, configuração e instruções não se tornam pontos de consulta canônicos por simples link.
- Consulta com destino conhecido não exige mapa; consulta por tarefa ou navegação inconclusiva o carrega seletivamente; ausência de rota retorna ao percurso existente sem inventar cobertura.
- Consulta pode funcionar sem escrita e com consulente sem autoridade editorial; sinalizar uma proposta não altera arquivos nem inicia indexação.
- Indexação/manutenção conferem rotas diretamente afetadas e exigem curadoria para associações novas ou alteradas.
- Exemplos e mensagens genéricos em inglês, sem conhecimento específico de consumidor e sem dependência de docs/ na distribuição instalada.

### Validação e aceite
Executar uv run pytest para alterações de runtime/testes. Realizar verificações textuais direcionadas de coerência entre guias, links, identidade autor/consumidor, carga seletiva, idioma e limites de propriedade; registrar evidências e disposição de warnings no ticket. Testes automáticos não substituem revisão humana da semântica. Integração externa é opcional e requer consumidor explicitamente selecionado e autorizado. Publicação e integração Git permanecem humanas.

## Notes

**2026-10-13T17:12:26.805818690Z**

Methodological grill fechado em 2026-10-13: solicitante confirmou explicitamente a síntese e autorizou implementação. Preservadas decisões originais. Aprovados navigation.intent_map como nome Markdown configurável na raiz de wiki/ e um link no índice; idioma da instância; H1, introdução opcional, H2 por intenção, lista com destino e orientação obrigatória, sem frontmatter ou mapa vazio; páginas operacionais e índices, títulos H1, links relativos com fragmentos existentes, repetição entre rotas mas não na mesma. Distribuição 1.5.0, contrato 1.0, adoção exige metodologia >=1.5.0, sem migração automática. Escopo adicional aprovado: aviso do instalador após mudança efetiva de versão orientando agente de manutenção, documentação e testes; revisão requerida não autoriza correções. Escopo fonte: schema/runtime/guias/interfaces/manifesto/testes. Sem consumidor real, Git, instalação ou publicação; novas decisões substantivas reabrem grill.

**2026-10-13T17:23:53.698102580Z**

Implementação fonte concluída para 1.5.0. Schema aceita navigation.intent_map opcional como arquivo Markdown distinto na raiz de wiki/; relações exigem metodologia >=1.5.0 sem mudar contract_version 1.0. Runtime reserva/exige mapa declarado, integra exatamente um link na raiz, valida H1/H2/listas/orientação, destinos operacionais/índices canônicos, labels H1, referências/fragmentos e unicidade por intenção. Auxiliar não recebe papel operacional mesmo com frontmatter inválido; índices preservam restrições. Guias SKILL/query/modeling/assisted-indexing/maintenance/setup e READMEs de interfaces documentam idioma local, carga seletiva, fallback, evidência apenas canônica consultada, consulta sem escrita/autoridade, curadoria e revisão diretamente afetada. Instalador avisa manutenção após mudança efetiva de versão; sem aviso em instalação inicial/reparo/no-op/dry-run, sem iniciar agentes ou migrar conteúdo. Documentação de atualização sincronizada. Evidência: execução final uv run pytest: 144 passed, 1 skipped em 132.48s; integração externa opcional ignorada por não haver consumidor selecionado. Primeira execução: 137 passed, 1 failed, 1 skipped; única falha era teste legado que tratava 1.5.0 como versão futura, corrigido para derivar versão incompatível acima da distribuição atual. Verificações textuais finais passaram: guias/interfaces referenciados existem, sem dependência docs/ na distribuição, instruções/diagnósticos genéricos afetados ASCII/inglês; identidade fonte/consumidor e rota ao contrato local conferidas. bash -n scripts/install-wiked.sh passou. Nenhum warning pendente. Testes sintéticos incluem opcionalidade, configuração/versão mínima/contract-only, formato, referências, idioma/nome configurável, repetições/transversalidade, regressões de índices, fronteiras/symlink, exclusão de papel operacional e atualização sem escrita do consumidor. Sem operação em consumidor real, Git, instalação de skill ativa ou publicação. Pronto para aceite humano final; publicação 1.5.0 permanece com o solicitante.

**2026-10-13T19:11:43.979894818Z**

Aceite final explícito do solicitante: mudança validada na migração de uma wiki e aprovada. Entregues mapa opcional de rotas por intenção, contrato/runtime e guias com carga seletiva e governança editorial, preservação das restrições dos índices e aviso de manutenção após mudança de versão. Distribuição fonte preparada para 1.5.0; validação fonte: 144 testes passaram, 1 integração opcional ignorada, verificações textuais e sintaxe do instalador passaram. Validação na migração foi reportada pelo solicitante, não executada pelo agente. Publicação permanece humana.
