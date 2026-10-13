---
id: wik-01m310mm3e55
title: Explicitar o carregamento do contexto canônico nas rotas de autoria
status: closed
type: task
priority: 3
mode: hitl
created: '2026-09-21T03:37:30.990835725Z'
updated: '2026-10-13T18:08:44.250977402Z'
closed: '2026-10-13T18:08:44.250977402Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
- contexto
acceptance:
- title: Grill metodológico define o ponto e a autoridade do carregamento do contexto para autoria e suas exceções de inicialização
  done: true
- title: Indexação, criação e revisão possuem um percurso explícito até o contexto canônico antes de decisões de autoria, conforme o escopo aprovado
  done: true
- title: Verificações textuais confirmam ausência de carga integral, duplicação normativa e dependência circular no setup
  done: true
- title: Preparação contextual em guia próprio manifestado permite carregamento lazy sem exigir modeling apenas para preparar contexto
  done: true
- title: AGENTS.md registra progressive disclosure como princípio da skill do Wiked obrigatório em quaisquer evoluções metodológicas
  done: true
- title: Verificações textuais confirmam inventário exato em 1.5.0, chamadas lazy e preservação das autoridades e exceções anteriores
  done: true
---

## Description

### Constatação
A consulta exige explicitamente a leitura do contexto configurado. Na indexação, a entrada lista referência de autoria, índices e páginas afetadas; a leitura do vocabulário fica dependente da orientação ampla do grill sobre contexto aplicável. A modelagem exige preservar termos, mas o pré-requisito de leitura poderia ser mais determinístico.
### Entrega
Conduzir grill metodológico para definir uma autoridade canônica de carregamento do contexto antes de criar ou revisar conteúdo. Tornar explícitas as dependências das rotas pertinentes, preservando navegação progressiva e leitura somente do necessário. Tratar a configuração inicial, quando o contexto ainda será criado, sem introduzir um pré-requisito circular.
### Independência
Melhoria genérica avulsa, não condiciona publicação ou corte da DOI. Não transformar contexto terminológico em evidência operacional nem impor leitura integral da wiki. Executar na origem canônica vigente do Wiked.

## Notes

**2026-10-10T18:40:29.763863521Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-13T17:45:53.224451574Z**

Grill metodológico encerrado em 2026-10-13 por confirmação explícita do solicitante ("confirmado") ao resumo final. Objetivo: carregar contexto canônico antes de análise ou propostas de autoria, com autoridade única em modeling.md e chamadas em assisted-indexing.md, maintenance.md, grill.md e setup.md. Contrato resolve navigation.context_file; contexto governa vocabulário, referência local governa autoria, nenhum é evidência operacional. Navegação progressiva somente por índices e páginas pertinentes; revisão somente leitura continua sem grill obrigatório. Inicialização explicitamente solicitada qualifica termos na conversa/Knot e materializa apenas após fechamento. Contexto ausente em instância existente bloqueia autoria normal e exige recuperação autorizada. Migração explícita lê estado existente sem liberar autoria normal sob contrato incompatível. Escopo apenas instrucional e em inglês, validado por verificações textuais; consulta, diagramas, adaptador, testes Python, schema, runtime, manifest, versão, publicação e instalação não mudam. Pendências laterais: diagramas e relação entre contexto e initial_content, sem ampliação deste ticket.

**2026-10-13T17:48:40.732259089Z**

Entrega implementada nos cinco guias aprovados: distr/agents/skills/wiked/guides/modeling.md, assisted-indexing.md, maintenance.md, grill.md e setup.md. Preparação contextual única resolve navigation.context_file a partir de wiki/, lê referência local quando declarada e limita navegação ao objetivo antes de análise/proposta. Chamadas explícitas preservam a barreira anterior à inspeção da fonte e revisão sem grill obrigatório. Setup explicita inicialização sem pré-requisito circular, leitura do estado anterior em migração e recuperação autorizada de contexto ausente. Mantida preparação genérica dos demais objetivos, sem ampliar diagramas. Validação: 49 verificações textuais Bash/grep passaram, cobrindo roteamento, autoridade única, momento da leitura, evidência, ausência de carga integral e dependência docs/, links/âncora, referências aos guias, limites de setup e instruções em inglês. As tentativas preliminares de checks foram ajustadas para não confundir Unicode histórico do protocolo do grill com conteúdo novo nem nomes ilustrativos routes.md com links de guias; nenhuma alteração adicional foi necessária. Revisão textual confirma ausência de decisões pendentes no escopo. Sem mudanças em testes/runtime/schema/manifest/versão; pytest não executado por ser entrega apenas instrucional, conforme rota aprovada.

**2026-10-13T17:48:53.279672951Z**

Preparação contextual centralizada em modeling.md e explicitamente chamada por indexação, manutenção, grill e setup antes de análise/propostas. Exceções de inicialização e migração delimitadas sem circularidade; contexto ausente bloqueia autoria normal. Três critérios de aceitação atendidos; 49 verificações textuais passaram. Entrega restrita aos cinco guias aprovados, sem alterar runtime, testes ou versão.

**2026-10-13T18:06:21.775484794Z**

Grill metodológico retomado e encerrado em 2026-10-13. Solicitante aprovou Q1 e resumo final ("de acordo com o plano"), ajustando Q2: progressive disclosure é princípio da skill do Wiked, que quaisquer evoluções metodológicas precisam seguir; a diretriz será registrada no AGENTS.md autoral, não como instrução operacional adicional da skill. Escopo revisado: extrair authoring-context.md; ajustar modeling, assisted-indexing, maintenance, grill e setup; incluir novo guia no manifest; registrar princípio em AGENTS.md. Modeling permanece exigido por regras substantivas, nunca apenas por preparação contextual. Preservar autoridades, revisão sem grill e exceções de inicialização/migração já aprovadas. A migração para 1.5.0 inclui este incremento do inventário; manifest já declara 1.5.0 e não haverá outro incremento de versão. Validação apenas textual; não alterar testes, runtime, schema, adaptador ou consulta. Três critérios adicionais registram aceitação do escopo lazy. Diagramas e relação entre contexto e initial_content permanecem pendências laterais.

**2026-10-13T18:08:35.783128520Z**

Revisão lazy implementada. Novo distr/agents/skills/wiked/guides/authoring-context.md concentra a preparação contextual e não exige modeling, intent map nem setup na preparação normal. Modeling, assisted-indexing, maintenance, grill e setup apontam para o guia completo, sem depender de leitura parcial por âncora. Indexação carrega modeling ao analisar/propor mudanças em páginas, glossário, índices ou rotas; setup o carrega antes de decisões estruturais/representacionais; manutenção mantém uso por estrutura. Autoridades e exceções anteriores preservadas. AGENTS.md registra progressive disclosure como princípio de projeto da skill do Wiked obrigatório em todas as evoluções metodológicas, sem copiar regra operacional para o consumidor. Novo guia incluído no inventário manifesto; distribution_version e METHODOLOGY_VERSION continuam 1.5.0. Validação: 72 checks textuais Bash/grep/find/diff passaram, incluindo inventário exato e arquivos possuídos, links/referências, ausência da antiga âncora e de dependência docs/, autoridade única, lazy sem carregamento indireto de modeling, inglês, governança, revisão somente leitura e setup sem circularidade. Nenhuma alteração em testes, runtime, schema, adaptador ou consulta. Pytest não executado por se tratar de mudança instrucional com inventário, conforme rota aprovada. Seis critérios de aceitação atendidos no escopo revisado.

**2026-10-13T18:08:44.250977402Z**

Preparação contextual extraída para authoring-context.md com chamadas lazy e inventário manifesto em 1.5.0. AGENTS.md exige preservar progressive disclosure como princípio da skill em todas as evoluções metodológicas. Regras substantivas de modeling e exceções anteriores mantidas. Seis critérios atendidos; 72 verificações textuais passaram.
