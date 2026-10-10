# Democratização do Wiked: investigação, comparação e caminho recomendado

**Relatório de pesquisa v1.1 — 10 de outubro de 2026.** Épico: `wik-01m2xs9pmqtw`; consolidação: `wik-01m2xsck8cjb`. Público: solicitante, Lucas e responsáveis futuros por produto, suporte e curadoria. Idioma: pt-BR. Revisão 1.1: descrições autônomas das opções recomendadas e atalhos de leitura.

**Síntese da recomendação:** começar por **B1, ambiente local padronizado sobre o fluxo existente, com inferência remota e Git humano**. Considerar **P, Wiked + Pi SDK com interface própria e núcleo determinístico compartilhado**, como investimento condicional em produto. Manter **B3, workspace remoto individual persistente e isolado**, como alternativa quando acesso local for inviável ou infraestrutura corporativa existente o favorecer. A comparação não demonstrou um vencedor quantitativo: essa preferência é uma decisão analítica por reuso, reversibilidade e escala inicial, não uma medição de superioridade.

Este documento consolida integralmente o percurso dos 16 estudos anteriores. É pesquisa no contexto autor do Wiked, **não nova instrução metodológica, especificação aprovada, evidência operacional da DOI ou autorização de implantação**. Os estudos fizeram análise documental/estática; não construíram o produto nem realizaram entrevista, validação conceitual ou piloto com Lucas. A aprovação integrada pertence ao solicitante e permanece posterior.

**Para entender primeiro as recomendações:** leia as fichas autônomas de [B1 — ambiente local padronizado](#opcao-b1), [P — produto Wiked com Pi SDK](#opcao-p) e [B3 — workspace remoto](#opcao-b3). Cada ficha reúne funcionamento, jornada, esforço, limites e condições de escolha; a leitura das demais seções é opcional para esse primeiro entendimento.

## 1. Objetivo, escopo e autoridade

O objetivo é investigar como tornar consulta fundamentada e indexação assistida acessíveis a colaboradores não necessariamente técnicos, preservando Markdown canônico, qualificação/grill, autoridade humana, Knot, validação determinística e rastreabilidade. A experiência considerada vai da abertura da instância até consulta, seleção de fontes, decisões, diff, validação, retomada e entrega ao curador.

O acordo registrado no épico em 2026-10-10 autorizou investigação AFK, escolha analítica de critérios e recomendações sem entrevistas intermediárias. Autorizou este relatório como artefato de pesquisa. Não autorizou construção, adoção, mudança metodológica, operação Git, instalação, credenciais reais ou publicação automática. O fechamento dos filhos significa entrega documental, não aceite humano do resultado integrado.

### Premissas autorizadas

- Aproximadamente cinco indexadores, algumas dezenas de leitores esporádicos e baixa concorrência. Não são censo nem telemetria.
- Usuário treinável para terminal e comandos simples; reduzir configuração continua desejável. Terminal não é motivo automático de descarte.
- Git inicialmente operado por humanos: branch, commit, envio e PR, com revisão/aprovação/merge humano pelo curador. Para o cenário DOI do épico, considerar Bitbucket; isso não se torna regra universal do Wiked.
- Operador rastreável como Author; plataforma poderá ser Committer em evolução própria. Credencial de IA não identifica o autor no Bitbucket.
- Computadores podem ser modestos. Aplicação local com modelo remoto deve ser distinguida de inferência local de LLM.
- Pesquisa documental de alta confiança pode concluir viabilidade conceitual sem experimento, desde que limites sejam explícitos.
- Execução remota exige sandbox e análise da política corporativa. A hipótese local sem sandbox exige examinar capacidades do modelo **e** direitos do processo/dependências.
- Solicitante avaliará o relatório; Lucas participará de validação conceitual posterior; piloto real ocorrerá após construção/preparo autorizado.

### Premissas analíticas, ainda revisáveis

Inferência remota; um escritor cooperativo por workspace; um objetivo/seleção de fontes por tarefa; primeiro SO suportado explicitamente; instalação assistida; responsável identificável por manutenção e recuperação. Para contas, usar 30 leitores no cenário de referência, não como número conhecido. Leitores podem ter canal separado, mas leitura estática não substitui consulta conversacional sem uma decisão explícita de escopo.

Setup, migração, manutenção estrutural e evolução metodológica ficam com mantenedores. Diagramas e exportações permanecem compatíveis, podendo continuar em fluxo especializado. Índice semântico, automação Git, novos serviços e decomposição de skills não são pré-requisitos artificiais desta investigação.

## 2. Método, evidência e rastreabilidade

### 2.1 Como a investigação foi conduzida

Os estudos identificaram autoridades e baseline; levantaram jornadas, rubrica, ambientes, Git, harnesses, AIShell e Pi; derivaram aplicações e requisitos; compararam configurações; aprofundaram finalistas; prepararam avaliação com Lucas; recomendaram entrada/evolução; propuseram comportamento e arquitetura. A consolidação leu o pai, este filho e **todas as notas dos 16 irmãos pelo Knot, inclusive arquivados, correções e encerramentos**. Todas as dependências estavam fechadas antes do claim da consolidação.

Fontes técnicas externas foram consultadas nos estudos de origem por Context7 e HTTP somente leitura, privilegiando documentação/código oficiais e tags quando disponíveis. Este relatório sintetiza essas pesquisas; não reivindica nova auditoria independente de cada URL, versão binária ou dependência transitiva. Fontes locais de desenvolvimento sustentam afirmações sobre software e governança, nunca fatos da operação DOI. Não foi consultado conteúdo operacional para completar esta análise.

Na consolidação foram conferidos cobertura dos filhos, links locais, coerência de categorias, pesos, intervalos e aritmética. Não foram executados testes de software: o único artefato criado é este relatório, além dos registros de governança via Knot.

### 2.2 Categorias usadas

| Categoria | Significado neste relatório | Exemplo |
|---|---|---|
| **D — documentado** | Afirmação sustentada por texto/código identificado; pode ser evidência herdada do estudo | Runtime atual valida, mas não edita páginas |
| **O — observado** | Algo efetivamente feito/recebido durante pesquisa | Leitura de documento, resposta Knot, cálculo; não desempenho do produto |
| **I — inferência** | Conclusão arquitetural/lógica derivada de premissas | Modelo remoto dispensa carregar pesos de LLM no cliente |
| **E — estimativa/cenário** | Número de planejamento com unidade, método e limites | 360–720 pessoa-horas para P |
| **R — recomendação/proposta** | Escolha analítica ou desenho ainda sujeito à decisão | B1 inicial; loader próprio; journal futuro |
| **U — desconhecido** | Evidência insuficiente | Economia real, RAM pico e preferência de Lucas |

Confiança alta documental não significa alta segurança implantada. Confiança média caracteriza boa parte das composições propostas; baixa caracteriza horas e ganhos estimados. Não há intervalo estatístico nem probabilidade de sucesso nas notas comparativas. O desconhecido não recebe automaticamente nota zero; uma intenção de produto não conta como funcionalidade atual.

### 2.3 Referências locais legíveis

Estas referências são fontes de software/governança. Os links são relativos a este relatório.

| Código | Referência | Uso e fotografia |
|---|---|---|
| L1 | [AGENTS.md](../AGENTS.md), [mapa de contexto](../CONTEXT-MAP.md), [contexto autor](../docs/CONTEXT.md), [evolução metodológica](../docs/metodologia.md) | Autor/consumidor, pesquisa versus alteração governada, Git humano; snapshot de 2026-10-10 |
| L2 | [Manifesto da distribuição](../.agents/wiked-manifest.yaml) | Wiked 1.4.0, propriedade de 16 arquivos e preservação de terceiros |
| L3 | [Skill Wiked](../.agents/skills/wiked/SKILL.md) | Roteamento e autoridades vigentes |
| L4 | [Consulta](../.agents/skills/wiked/guides/query.md), [indexação assistida](../.agents/skills/wiked/guides/assisted-indexing.md), [grill](../.agents/skills/wiked/guides/grill.md), [Knot](../.agents/skills/wiked/guides/knot.md) | Evidência, fonte, qualificação, confirmação, arquivo e governança |
| L5 | [Contrato: documentação](../.agents/skills/wiked/contracts/README.md), [schema](../.agents/skills/wiked/contracts/wiki-structure.schema.json) | Contrato 1.0 e JSON Schema draft 2020-12 |
| L6 | [Runtime: documentação](../.agents/skills/wiked/scripts/README.md), [validador Python](../.agents/skills/wiked/scripts/validate_wiki.py) | Runtime 1.4.0; CLI, dependências e diagnósticos |
| L7 | [Testes do validador](../tests/test_wiked_validator.py), [projeto fonte](../pyproject.toml) | 32 definições de testes observadas pelo inventário; projeto fonte 0.1.0 é versão distinta |
| L8 | [Diagramas](../.agents/skills/wiked/guides/d2.md), [exportação](../.agents/skills/wiked/guides/export.md), [manutenção](../.agents/skills/wiked/guides/maintenance.md), [setup](../.agents/skills/wiked/guides/setup.md), [modelagem](../.agents/skills/wiked/guides/modeling.md) | Capacidades especializadas a preservar |
| L9 | [Adaptador de setup](../.agents/commands/wiked-setup.md), [README do repositório](../README.md) | Adaptador fino e identificação contextual de UniSoma/aishell |

Hashes registrados pelo inventário, não identificadores de release assinada: manifesto `a302ceee142edc0fe45d3e7034839064bd494683776b952a40306c4c3e5d9040`; runtime `2017e27978a09b651942ee0b6d8d069b4d84aa9ef405af1b1d135d93ba35e8d9`; schema `f89d24a7223c27796d288f8794db3f03391a1e600c0340f5db0ffd9b7a842775`; testes `66bd0a7c1c1c0e3d4a431f794709ba76be2e4f060a24d5702cd599e545332853`. Não houve consulta Git para fixar SHA local.

### 2.4 Fontes externas diretas e versões

**Data de consulta dos estudos: 2026-10-10.** URLs contínuas podem mudar; os fatos decisivos estão preservados no texto deste relatório. Uma tag consultada não equivale a verificar criptograficamente o pacote instalado. Preços são fotografias documentais, não propostas comerciais. Referências abaixo permitem entender as conclusões sem depender exclusivamente dos IDs Knot.

| Código | Fontes oficiais diretas | Recorte e informação decisiva |
|---|---|---|
| E1 | [Pi SDK 1.1.0](https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/docs/sdk.md), [SDK 1.0.0](https://github.com/earendil-works/pi/blob/v1.0.0/packages/coding-agent/docs/sdk.md), [pacote npm](https://registry.npmjs.org/@earendil-works/pi-coding-agent/latest) | Base aprofundada 1.0.0; confronto dirigido 1.1.0, latest observado; Node >=22.19.0; sessões, tools e loader |
| E2 | [Segurança Pi 1.1.0](https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/docs/security.md), [loader](https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/src/core/resource-loader.ts), [agent-session](https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/src/core/agent-session.ts) | Cwd/trust não são sandbox; descoberta e callable excedem tools visíveis |
| E3 | [Licença Pi](https://github.com/earendil-works/pi/blob/v1.1.0/LICENSE), [providers](https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/docs/providers.md), [CLI integration](https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/docs/cli-integration.md), [changelog](https://github.com/earendil-works/pi/blob/v1.1.0/packages/coding-agent/CHANGELOG.md) | MIT; credenciais e UI têm caminhos adicionais; versão 1.1.0 em 2026-10-07 |
| E4 | [UniSoma/aishell no SHA examinado](https://github.com/UniSoma/aishell/tree/e4edfc2c788def40d3a2bcbd4f1ea9e26a014dc2), [run.clj](https://github.com/UniSoma/aishell/blob/e4edfc2c788def40d3a2bcbd4f1ea9e26a014dc2/src/aishell/docker/run.clj), [ADR 0006](https://github.com/UniSoma/aishell/blob/e4edfc2c788def40d3a2bcbd4f1ea9e26a014dc2/docs/adr/0006-harden-on-docker-with-an-egress-proxy.md), [release v4.4.1](https://github.com/UniSoma/aishell/releases/tag/v4.4.1) | Main de 2026-09-28, separado da release de 2026-09-24; intenção de hardening não demonstrada no código |
| E5 | [Docker security](https://docs.docker.com/engine/security/), [recursos](https://docs.docker.com/engine/containers/resource_constraints/), [rootless](https://docs.docker.com/engine/security/rootless/), [gVisor security](https://gvisor.dev/docs/architecture_guide/security/) | Documentação contínua; namespaces, quotas, daemon e contenção têm fronteiras distintas |
| E6 | [Codespaces arquitetura](https://docs.github.com/en/codespaces/about-codespaces/deep-dive), [billing](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces) | SaaS contínuo; VM/workspace, persistência em /workspaces; US$0,18/0,36 por hora e US$0,07/GB-mês |
| E7 | [WorkSpaces preços](https://aws.amazon.com/workspaces-family/workspaces/pricing/), [rede](https://docs.aws.amazon.com/workspaces/latest/adminguide/workspaces-network-requirements.html), [Windows 365 Business](https://www.microsoft.com/en-us/windows-365/business/compare-plans-pricing), [rede Windows 365](https://learn.microsoft.com/en-us/windows-365/enterprise/requirements-network) | SKUs/regiões/edições distintos; não transportar preço Business para regra Enterprise |
| E8 | [Kasm requisitos](https://docs.kasm.com/docs/explanations/system-requirements), [perfis persistentes](https://docs.kasm.com/docs/how-to/data-storage/persistent-profiles), [VS Code requisitos](https://code.visualstudio.com/docs/supporting/requirements), [Remote SSH](https://code.visualstudio.com/docs/remote/ssh.md) | Kasm 1.19.0: host mais sessões; suporte VS Code varia por topologia |
| E9 | [uv instalação](https://docs.astral.sh/uv/getting-started/installation/), [Python pelo uv](https://docs.astral.sh/uv/guides/install-python/), [Pandoc](https://pandoc.org/installing.html), [D2 exportações](https://d2lang.com/tour/exports) | Encapsular provisionamento não elimina runtimes, conversores, fontes ou browser |
| E10 | [Git commit 2.51.0](https://git-scm.com/docs/git-commit/2.51.0), [Bitbucket identidade](https://support.atlassian.com/bitbucket-cloud/docs/configure-your-dvcs-username-for-commits/), [branch permissions](https://support.atlassian.com/bitbucket-cloud/docs/use-branch-permissions/), [merge checks](https://support.atlassian.com/bitbucket-cloud/docs/suggest-or-require-checks-before-a-merge/) | Metadados versus autenticação; checks bloqueantes Cloud dependem de Premium/configuração |
| E11 | [Cloud PR REST 2.0](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/), [source API](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-source/), [API tokens](https://support.atlassian.com/bitbucket-cloud/docs/api-tokens/), [OAuth](https://developer.atlassian.com/cloud/bitbucket/oauth-2/) | Autor do PR é principal autenticado; scopes não são todos equivalentes |
| E12 | [DC HTTP tokens](https://confluence.atlassian.com/bitbucketserver/http-access-tokens-939515499.html), [DC merge checks](https://confluence.atlassian.com/bitbucketserver/checks-for-merging-pull-requests-776640039.html), [REST DC v1002](https://developer.atlassian.com/server/bitbucket/rest/v1002/api-group-pull-requests/) | Páginas DC 10.5 e API 10.0.2 são fotografias distintas; ambiguidade de tokens exige prova na configuração escolhida |
| E13 | [OpenCode V2](https://opencode.ai/v2/docs/), [web](https://opencode.ai/v2/docs/cli/web/), [permissões](https://opencode.ai/v2/docs/permissions), [cliente](https://opencode.ai/v2/docs/build/client), [SDK](https://opencode.ai/v2/docs/build/sdk), [Console](https://opencode.ai/v2/docs/console/), [licença](https://raw.githubusercontent.com/anomalyco/opencode/dev/LICENSE) | Download anunciado 2.0.6, sem conferir binário; docs contínuos; MIT na fonte dev; servidor/SDK/gateway de inferência não são o mesmo produto |
| E14 | [Codex cloud](https://developers.openai.com/codex/cloud/), [ambientes atuais](https://developers.openai.com/codex/environments/cloud-environments.md), [preços](https://developers.openai.com/codex/pricing.md) | Cloud atual separado de Legacy; VM por tarefa, GitHub e recuperação temporal limitada |
| E15 | [Claude Code web](https://code.claude.com/docs/en/claude-code-on-the-web), [dados](https://code.claude.com/docs/en/data-usage), [preços](https://claude.com/pricing) | Cloud versus Remote Control; bundle Bitbucket não dá push de retorno; condições de plano/retenção |
| E16 | [Copilot agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent), [riscos](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations), [billing](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/billing), [assentos](https://docs.github.com/en/copilot/concepts/billing-and-usage/organizations-and-enterprises/seats-and-billing-cycles) | GitHub-only, Author agente, sessão limitada; créditos atuais não equivalem a premium requests antigos |
| E17 | [Devin Bitbucket](https://docs.devin.ai/integrations/bitbucket), [skills](https://docs.devin.ai/product-guides/skills.md), [security profiles](https://docs.devin.ai/product-guides/security-profiles.md), [segurança](https://docs.devin.ai/admin/security.md), [billing](https://docs.devin.ai/admin/billing/self-serve.md), [ambiente](https://docs.devin.ai/onboard-devin/environment.md) | Bitbucket nativo, uma skill ativa; perfis, retenção e preços dependem de plano/configuração |
| E18 | [n8n Wait](https://raw.githubusercontent.com/n8n-io/n8n-docs/main/docs/integrations/builtin/core-nodes/n8n-nodes-base.wait.md), [licença n8n](https://raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md), [Human Input Dify](https://raw.githubusercontent.com/langgenius/dify-docs/main/en/api-reference/guides/human-input-flow.mdx), [licença Dify](https://raw.githubusercontent.com/langgenius/dify/main/LICENSE), [compose Dify](https://raw.githubusercontent.com/langgenius/dify/main/docker/docker-compose.yaml) | Main móvel: n8n sem release fixada; compose Dify anuncia 1.17.1 sem fixar docs; pausa humana não implementa domínio Wiked |

## 3. Percurso completo: os 16 estudos e suas contribuições

Todos os estudos abaixo foram concluídos em **2026-10-10**, com notas integrais e AC satisfeitos. São recuperáveis por `knot show <id>`, mesmo arquivados. As fontes L/E são definidas acima; os horários identificam encerramentos UTC, não duração produtiva. A leitura das notas inclui correções posteriores. Nenhum estudo reporta benchmark, piloto ou aceite humano de adoção.

### 3.1 Jornadas e papéis — `wik-01m2xsbstm3e` — 13:05:20Z

**Objetivo/passos:** transformar o escopo em preparação, consulta, indexação, diff/validação, entrega e retomada; confrontar guias Wiked 1.4.0 e documentação conceitual Pi com papéis e falhas. **Fontes:** L1–L4/L6/L8; E1 em main na coleta inicial, sem fixação suficiente de sintaxe. **Premissas:** usuário treinável, fonte/ticket explícitos e baixa concorrência.

**Resultado:** separar leitor, colaborador, humano qualificado, curador, suporte e mantenedor; função não prova qualificação. J0 prepara o ambiente; consulta mantém lacuna; indexação exige grill; revisão vê diff integral; entrega distingue conclusão local de publicação; retomada reconcilia arquivos, decisões e ticket. **I/R:** separar preparo excepcional de uso recorrente e mostrar sempre fase/próximo responsável. **Confiança/limites:** alta nas regras documentadas, média na experiência proposta, U em facilidade real. Não havia resultado Pi final naquele momento; o estudo dedicado posterior prevalece para versões e controles.

### 3.2 Rubrica — `wik-01m2xsbsv23a` — 13:06:31Z

**Objetivo/passos:** derivar restrições não compensáveis, escalas, pesos, TCO e sensibilidade do acordo, sem favorecer tecnologia. **Fontes:** épico e L1; rubrica v1.0, sem afirmar capacidades de produtos. **Premissas:** configurações equivalentes e mesma jornada; pesos do agente, não preferência medida.

**Resultado:** cinco gates, oito critérios de 0–4, pesos 25/15/15/10/8/10/10/7; desconhecido [0,4], sem central automática; TCO por papel; cenários 3/12/36 meses e clientes 4/8 GiB. **R:** decidir primeiro viabilidade/autoridade, depois trade-offs. **Confiança/limites:** alta na lógica de não compensar violação por custo; média nos cortes e pesos, não calibrados empiricamente. Não produziu ranking por si só.

### 3.3 Ambientes — `wik-01m2xsbsw0xk` — 13:07:29Z

**Objetivo/passos:** comparar skill local, pacote, app Pi, terminal remoto, Codespaces, DaaS e Kasm; pesquisar requisitos/preços oficiais e separar cliente, inferência, servidor e suporte. **Fontes:** E6–E9, Kasm 1.19.0; serviços contínuos. **Premissas:** inferência remota, equipamento existente, cinco indexadores; horas de uso e 30 leitores somente para cenários.

**Resultado D/I:** cliente local não precisa GPU/pesos de LLM; ainda usa runtimes, corpus e conversores. Remoto desloca dependências e acrescenta rede, persistência e operação. **E:** Codespaces cinco usuários US$21,50–147,50/mês em configurações/horas diferentes; operação local padronizada 2–6 h/mês, excluída manutenção de produto. **R:** local padronizado e remoto persistente como alternativas; não contratar desktop escritor por leitor eventual sem necessidade. **Confiança/limites:** alta em mecanismos/preços documentados, baixa em envelopes de recursos/suporte; Kasm comercial não cotado e nenhum consumo medido.

### 3.4 Aplicações e composição — `wik-01m2xsbswsza` — 13:13:55Z

**Objetivo/passos:** consumir Pi e estudos básicos, separar chat de domínio, comparar web fina, workflow web e Dify/n8n; consultar APIs/licenças. **Fontes:** L2–L8, E1–E3/E13/E18; Pi 1.1.0, OpenCode V2, Dify main/compose 1.17.1, n8n main. **Premissas:** núcleo independente do harness e Git humano suficiente inicialmente.

**Resultado:** SDK/harness reutiliza conversa/modelos/sessões, não plano autorizado, efeitos recuperáveis, arquivo e reconciliação. Dify/n8n têm pausa humana real, mas timeout não é consentimento; integração aumenta estados e manutenção. **E:** Pi 9–18 pessoa-semanas; web fina 12–24; workflow 16–30; composição 12–26. **R:** baseline e Pi de domínio; web/low-code condicionados a benefício ou plataforma já operada. **Confiança/limites:** média na composição, baixa no esforço; licenças não são parecer jurídico nem custo zero.

### 3.5 Git e Bitbucket — `wik-01m2xsbsy098` — 13:06:30Z

**Objetivo/passos:** desenhar branch/PR/curadoria humanos, pesquisar identidade e automação opcional; confrontar Cloud/DC e recuperação. **Fontes:** E10–E12; Git 2.51.0, Cloud REST 2.0, páginas DC 10.5/REST v1002. **Premissas:** contas individuais, curador, edição/licença real desconhecidas.

**Resultado D:** Author, Committer, ator do push, autor do PR e integrador são distintos. Cloud cria PR como usuário autenticado; metadado Author não autentica. Checks bloqueantes Cloud exigem Premium/configuração; DC tem outro contrato. **R:** Git humano inicial com diff/staging criteriosos, recuperação assistida e revalidação após conflito. Publicador futuro separado, sem merge pelo agente. **E:** 2–4 h iniciais de treino mais primeiras 2–3 entregas acompanhadas. **Confiança/limites:** alta nos mecanismos, média na adequação; configuração real, identidade após squash/rebase e ambiguidades DC precisam prova.

### 3.6 Harnesses hospedados — `wik-01m2xsbszt87` — 13:06:23Z

**Objetivo/passos:** comparar OpenCode, Codex, Claude, Copilot e Devin por identidade, ferramentas, sessão, isolamento, Bitbucket e custo; diferenciar SaaS, servidor e controle remoto. **Fontes:** E13–E17; OpenCode V2/download 2.0.6 anunciado, demais SaaS contínuos. **Premissas:** shell remoto isolado, preservação de todas as jornadas.

**Resultado:** OpenCode é hospedeiro controlável, mas operação multiusuário não vem pronta; Console não demonstra VM gerenciada. Devin tem Bitbucket nativo, porém uma skill ativa gera risco na composição Wiked/Knot/grill. Codex/Claude favorecem GitHub; Copilot é GitHub-only e atribui Author ao agente. **R:** OpenCode/Devin reservas condicionais desta família, não vencedor global. **Confiança/limites:** alta em diferenças documentadas; média em preços/entitlements; sem implantação, auditoria contratual ou composição Wiked comprovada.

### 3.7 AIShell e segurança server-side — `wik-01m2xsbt175b` — 13:06:45Z

**Objetivo/passos:** identificar o AIShell correto, confrontar documentação/ADR com parser, launcher e entrypoint; modelar rede, segredos, recursos e operação. **Fontes:** L9, E4/E5; SHA `e4edfc2c788def40d3a2bcbd4f1ea9e26a014dc2`, separado de v4.4.1. **Premissas:** inferência remota e sandbox remoto obrigatório.

**Resultado D:** bind mounts graváveis, flags livres, avisos consultivos, sudo no contêiner, credenciais acessíveis e ausência de quotas injetadas por padrão; ADR strict/proxy não demonstrado implementado e exclui multi-tenant. **R:** launcher/política externos, segregação, egress, quotas e auditoria; AIShell pode ser componente, não serviço pronto. **E:** hosts 8/16/32 GiB como ensaios para 2/5 escritores e exportações. **Confiança/limites:** alta no código examinado, média no desenho, baixa no dimensionamento; conformidade corporativa U. PowerShell/AIShell é homônimo descartado.

### 3.8 Baseline — `wik-01m2xsbt1bk6` — 13:06:27Z

**Objetivo/passos:** inspecionar toda distribuição, schema, runtime e testes; mapear efeitos e lacunas sem executar suíte. **Fontes:** L1–L9; Wiked 1.4.0/contrato 1.0, hashes acima. **Premissas:** preservar Markdown, governança, opcionais e interfaces atuais.

**Resultado D:** 16 arquivos distribuídos após correção explícita de uma contagem inicial 17; 32 definições de testes, não execuções aprovadas. Núcleo executável atual é validador portátil, não editor/servidor/checkpoint/publicador. Edição, arquivo e retomada são instruções executadas por agente/harness. **R:** reutilizar Python; núcleo de efeitos é construção futura. **Confiança/limites:** alta documental/estática; média no encapsulamento; custos, tempos e taxas de falha não medidos. Datas de tickets não foram usadas como duração de trabalho.

### 3.9 Requisitos e ameaças — `wik-01m2xscjr6rn` — 13:14:47Z

**Objetivo/passos:** derivar catálogo verificável das jornadas, baseline, AIShell e Pi; separar restrições, propostas e metas exploratórias. **Fontes:** L1–L8, E2/E4/E5; Pi security 1.1.0 reconferido. **Premissas:** fonte potencialmente hostil, workspace individual e processo local confiável apenas como hipótese.

**Resultado:** oito restrições, 32 requisitos propostos, 13 ameaças, retenção por classe, sete cenários e seis grupos de provas. Cobrem identidade, confirmação, paths, segredos, contexto, isolamento, integridade, recuperação, orçamento e suporte. **R:** custo de jornada íntegra antes de aparência do chat. **Confiança/limites:** alta nos limites documentados, média no catálogo; números de RAM, retenção, RPO/RTO/SLO são E, não compromissos. Nenhum controle proposto foi atestado implementado.

### 3.10 Comparação e shortlist — `wik-01m2xsck3q0r` — 13:20:21Z

**Objetivo/passos:** ler dez pré-requisitos, aplicar rubrica v1.0 a oito configurações, calcular intervalos, cinco vetores e 16 perturbações, TCO e limiares. **Fontes:** estudos 3.1–3.9 e 3.16; versões herdadas, sem nova auditoria de produtos. **Premissas:** S2, um SO, mesma jornada, sem ganho de UX medido.

**Resultado:** B1/P/B3 finalistas; B0 controle; B4 pode compor B3. Intervalos amplos sobrepostos, sem centrais; cobertura documental estrita de pontuação 0%, apesar de evidência forte de componentes. **R:** reuso inicial, produto Pi condicional e remoto para acesso. **Confiança/limites:** média na shortlist, baixa nas estimativas; nenhum vencedor numérico. Cálculos são O aritmético, não evidência de desempenho.

### 3.11 Viabilidade e provas futuras — `wik-01m2xscjvtef` — 13:24:24Z

**Objetivo/passos:** percorrer verticalmente B1/P/B3; confrontar SDK/security Pi 1.1.0 e persistência Codespaces; preparar corpus/ambientes/V01–V15. **Fontes:** E1/E2/E6 e estudos anteriores. **Premissas:** mesma tarefa e nenhuma prototipação nesta etapa.

**Resultado:** B1/B3 continuam com recuperação assistida; Pi exige plano, host e núcleo próprios. Sessão persistida não é transação; rename individual não torna multifile atômico. Pontas favoráveis de custo/qualidade são correlacionadas, não combináveis livremente. **R:** provar primeiro autoridade/fronteiras, depois integridade e benefício. **Confiança/limites:** alta nos mecanismos, média na integração; zero provas futuras executadas e nenhum estreitamento de estimativas sem dados.

### 3.12 Recomendação — `wik-01m2xsck6fnt` — 13:29:43Z

**Objetivo/passos:** sintetizar comparação, viabilidade e roteiro Lucas para escolher entrada e condições de mudança. **Fontes:** estudos 3.10/3.11/3.15/3.16 e baseline. **Premissas:** treinamento/Git humano admissíveis, pequena escala e valor de reversibilidade.

**Resultado R:** B1 é escolha inicial contextual; Pi é preferencial se houver investimento em produto; B3 remove impedimento de acesso. Não é empate decisório nem vitória quantitativa. **E/R:** gatilhos de revisão por autonomia, suporte, acesso e benefício líquido, descritos adiante. **Confiança/limites:** média na preferência; baixa em horas/economia; usabilidade U. Pode-se ir diretamente a P com justificativa/autoridade próprias; B1 não é pedágio obrigatório.

### 3.13 Comportamento — `wik-01m2xsckbw27` — 13:32:49Z

**Objetivo/passos:** derivar estados, permissões, jornadas, falhas e handoffs; separar regras vigentes, roteiro B1 e controles futuros P. **Fontes:** jornadas, recomendação, baseline, Pi, requisitos e viabilidade. **Premissas:** revisão identificável, fonte selecionada, um escritor e suporte.

**Resultado R:** quatro eixos independentes — conteúdo/tarefa, validade técnica, ciclo Knot e publicação. Mostrar instância, modo, fase comprovada, revisão, decisão pendente e próximo responsável. Fechado não é publicado; validado não é semanticamente aprovado. **Confiança/limites:** média no modelo de experiência; não há novas strings/comandos/status implementados nem ganho de suporte medido. Comando `wiked` permanece proposto.

### 3.14 Arquitetura — `wik-01m2xsck4v3k` — 13:36:34Z

**Objetivo/passos:** confrontar recomendação/comportamento com módulos, interfaces, armazenamento, compatibilidade e seis decisões relacionadas; consultar loader Pi. **Fontes:** L1–L9, E1–E3 e estudos anteriores; Pi 1.0.0 versionado no trecho adicional, 1.1.0 herdado do parecer dedicado. **Premissas:** domínio independente de tipos Pi e uma autoridade de validação.

**Resultado R:** B1 reutiliza; P compartilha efeitos entre CLI/skill/chat; B3 muda localização, acrescentando isolamento/operação. Journal separado de conversa; adapters para runtime/Knot/arquivos; confirmação humana fora do modelo; recuperação por base/resultado/terceira versão. Publicação/opcionais/projeção/governança têm escopos próprios. **Confiança/limites:** média na arquitetura, baixa em custo herdado; não define APIs disponíveis. Falha transitória Knot foi preservada no estudo e retomada autorizada; não foi tratada como evidência de produto.

### 3.15 Lucas: conceito e piloto — `wik-01m2xsckbz92` — 13:27:07Z

**Objetivo/passos:** usar o caso sentinela de papéis do time técnico para preparar conversa C1–C7 e piloto T0–T6, com métricas e suporte. **Fontes:** acordo, jornadas, rubrica e viabilidade; sem dados operacionais do time. **Premissas:** Lucas é caso de aprofundamento, não amostra representativa ou pessoa já qualificada por inferência.

**Resultado R:** validar entendimento após relatório; observar desempenho somente após construção e provas. Separar ajuda, tempo ativo, espera, curadoria e retrabalho; registrar denominadores e falhas. **E:** conversa 60–90 min; duas sessões de treino de 45–60 min como reserva, não suficiência comprovada. **Confiança/limites:** média no roteiro, baixa nas durações/metas; não houve participação, preferência, resposta ou aceite de Lucas.

### 3.16 Pi SDK — `wik-01m4jx0e5n6g` — 13:07:03Z, conferência 13:07:17Z

**Objetivo/passos:** fixar versão/licença/APIs; examinar descoberta, TUI, credenciais, callable e ciclo de sessão; mapear núcleo compartilhado, dependências, ameaça e esforço. **Fontes:** E1–E3, L2/L6; base 1.0.0 confrontada com 1.1.0, tags prevalecendo sobre snippets main. **Premissas:** processo local confiável e inferência autorizável; sem transferir garantias a harness externo.

**Resultado D/I:** SDK permite host próprio; chamada mínima herda recursos. Tools ativas não esgotam capacidades indiretas. Loader/UI/credenciais próprios são necessários à variante restrita; Pi não oferece sandbox nativo. **E:** 9–18 pessoa-semanas. **R:** incluir produto de domínio condicionalmente, descartar “Pi padrão + whitelist = confinado”. **Confiança/limites:** alta documental, média na arquitetura, baixa em esforço; sem auditoria exaustiva de transitivos, execução ou garantia de segurança.

## 4. Baseline: o que já existe e o que ainda precisa ser construído

Wiked 1.4.0 oferece uma distribuição copiável, roteamento por skill, contrato 1.0/schema, nove guias, adaptador fino e validador Python portátil. A contagem correta é **16 arquivos: 1 manifesto + 10 instruções + 1 comando + 2 contratos + 2 runtime**. Os 17 do épico são filhos de pesquisa, outra contagem.

| Capacidade | Hoje, documentado no baseline | Trabalho adicional para produto P |
|---|---|---|
| Abrir instância | Skill resolve raiz/contrato; runtime recebe raiz explícita; incompatibilidade interrompe | Host/CLI, diagnóstico uniforme e versões suportadas |
| Consultar | Navegação progressiva por contexto/índices/links; busca textual subsidiária; resposta cita páginas/limites | Tools de leitura por papel e manifesto de evidência; síntese continua agêntica |
| Selecionar fonte/ticket | Knot via CLI; fontes/objetivo/páginas/AC antes de indexar | Vínculo executável de seleção, fingerprint e escopo |
| Qualificar/grill | Declaração humana por sessão/objetivo; decisões e síntese confirmadas | Estado/confirmador do host, sem fabricar competência humana |
| Editar | Agente/harness aplica páginas, índices, proveniência e referências | Plano/diff/base, operações tipadas e aplicação recuperável |
| Validar | Runtime determinístico lê contrato/wiki e consulta Knot | Adaptador do mesmo runtime ligado à revisão; não segundo validador |
| Arquivar fonte | Guia move só seleção local após validação; colisão interrompe | Operação com recibo, integridade e reconciliação |
| Retomar/entregar | Conversa, notas, arquivos e ferramentas do harness; Git humano | Journal de tarefa independente e pacote correlacionado |
| Diagramas/exportações | Guias e ferramentas externas; inspeção visual/semântica humana | Capacidades opcionais controladas, não reescrita dos motores |
| Distribuir/atualizar | Manifesto de ownership; cópia não é instalador publicado | Canal, artefatos, integridade, locks, rollback e suporte |

Interface do runtime atual, citada como referência e não executada nesta pesquisa:

```text
uv run --script <skill>/scripts/validate_wiki.py --repository-root <instância> --format json
```

JSON atual: `ok`, `summary`, `diagnostics` com código/severidade/path/linha/mensagem; **não tem `schema_version` atual**. Saída 0: sem erros, possivelmente avisos; 1: erro estrutural; 2: falha de contrato/runtime. Valida schema/relações, navegação/links, frontmatter, proveniência/citações, assets/registros/tracking. Não atesta verdade, atualidade semântica, aprovação humana ou renderização correta. Não escreve conteúdo/índices/raw/tickets.

Dependências declaradas: Python >=3.11, uv, jsonschema >=4.23,<5, markdown-it-py >=3,<4, PyYAML >=6,<7 e Knot. Knot foi observado pelos estudos como 0.14.0; skill instalada dizia 0.13.0, prevalecendo CLI. Faixas PEP 723 não são lock reprodutível/offline. D2/Pandoc/WeasyPrint/rsvg-convert e outros componentes dependem do formato. D2 PNG/PDF pode envolver Playwright/browser; PDF por Pandoc requer motor, não necessariamente uma instalação LaTeX completa específica.

O inventário encontrou 32 definições `test_*`, com fixtures de contrato, portabilidade, tracking, navegação e fronteiras textuais. **Não houve execução nessa pesquisa.** Não se identificou nessa suíte prova de edição transacional, replay, archive com falha/colisão, isolamento hostil, diffs até PR ou conversores reais. Ausência nessa suíte não prova ausência em sistemas externos. Nenhum percentual de cobertura, duração de validação, tokens ou custo operacional foi medido.

## 5. Jornada e comportamento recomendados

### 5.1 Responsabilidades

Suporte prepara versões, acesso, credencial, proxy e recuperação; mantenedor trata setup/migração/estrutura; leitor consulta; colaborador seleciona fonte/ticket e confere mudanças; humano qualificado decide semântica e confirma grill; agente apura fatos e propõe/consolida o escopo confirmado; curador revisa e publica humanamente. Papéis podem coincidir, mas login, cargo ou assignee não comprovam qualificação.

### 5.2 Percurso recorrente

1. **Abrir:** confirmar raiz, instância e compatibilidade. B1 usa o comando do harness fornecido pelo suporte. `wiked` é comando proposto de P, não produto já disponível. Contrato ausente/incompatível não autoriza setup/migração automática.
2. **Consultar:** navegar contexto/índices/links, retornar resposta com páginas e lacunas. Só Markdown operacional configurado sustenta fatos; raw/archive, tickets, YAML, instruções e URLs externas não completam evidência. Consulta não inicia escrita implicitamente.
3. **Preparar indexação:** humano organiza workspace/branch e seleciona ticket/fontes/objetivo/páginas/AC. Preparação e leitura do consolidado precedem fonte. Não varrer raw inteiro por conveniência.
4. **Qualificar e grill:** declaração explícita; agente separa fato, proposta e divergência; humano resolve questões e confirma síntese. Nova decisão substantiva reabre grill. Exceções vigentes estreitas de registros durante grill não viram permissão genérica.
5. **Consolidar e revisar:** mostrar diff integral com novos/alterados/excluídos, índices, proveniência, citações, derivados e movimentos. Resumo não substitui diff. P ligaria plano a bases/hash; B1 depende de procedimento e ferramentas do harness.
6. **Validar:** usar runtime único na revisão efetivamente entregue; erros bloqueiam, avisos exigem disposição humana. Validação não aprova sentido. Alteração posterior invalida evidência técnica correspondente.
7. **Arquivar/reconciliar:** somente fonte local selecionada, após validação, destino sem colisão e conteúdo preservado. Fonte externa permanece externa. Humano decide persistência em Git. Conferir AC e concluir localmente segundo o fluxo vigente.
8. **Entregar:** pacote com instância/ticket, fontes, decisões, base/diff, versões/resultado, avisos, pendências, autoria e próximo responsável. Humano seleciona arquivos, faz commit/envio/PR; curador revisa/integra. Correção ou conflito exige nova revisão/validação aplicável.
9. **Retomar:** reconstruir estado comprovado por arquivos, Knot e decisões; renovar qualificação conforme sessão/objetivo; não reproduzir consentimento por resumo de conversa. Resultado incerto é pendência a reconciliar, não autorização de repetir.

### 5.3 Estados sem ambiguidade

Indicadores propostos: preparação pendente → pronto → escopo/qualificação pendentes → grill → confirmação pendente → consolidação → revisão/validação → conclusão local → entrega/curadoria → integração/publicado. Correção, pausa, cancelamento e resultado incerto atravessam fases. São indicadores de experiência, **não novos status Knot**.

Quatro eixos permanecem separados: bytes/conteúdo, validade estrutural, ciclo do ticket e publicação. Ticket fechado não comprova merge; PR aprovado não comprova integração; conversa salva não comprova efeito recuperável; saída 0 não comprova verdade. Cancelar interrompe novas ações, não desfaz automaticamente efeitos já realizados.

### 5.4 Recuperação e falhas

| Falha | Resposta proposta e responsável |
|---|---|
| Instância/contrato errado | Parar antes de escrever; suporte/mantenedor resolve destino/compatibilidade |
| Credencial/rede/modelo | Preservar estado; suporte restaura acesso; sem fallback silencioso de endpoint |
| Fonte mudou/fora do escopo | Revalidar seleção; humano decide novo escopo/grill quando necessário |
| Confirmação ausente/forjada | Manter pendente; texto do modelo/fonte não vale como consentimento |
| Diff/base obsoletos | Preservar versões, preparar novo diff; não sobrescrever concorrência |
| Parcial multifile/disco cheio | Classificar base/resultado/terceira versão; suporte intervém no terceiro caso |
| Knot timeout | Consultar autoridade antes de repetir; conteúdo aplicado pode ter registro pendente |
| Archive ocupado/interrompido | Conferir origem/destino/fingerprint; nunca sobrescrever ou alegar sucesso incerto |
| PR falhou/correção solicitada | Manter entrega pendente; humano corrige e revalida revisão |
| Perda de máquina/workspace | Restaurar backup separado e reconciliar; persistência de sessão não é backup |

B1 pode recuperar com ajuda explícita e mensurada. Se recuperação automática passar a ser obrigatória, B1 muda de escopo/custo; não lhe atribuir gratuitamente o núcleo proposto para P.

## 6. Famílias comparadas e finalistas

### 6.1 Configurações, não marcas abstratas

| Código/família | Configuração prospectiva | Reuso e custo/lacuna principal | Destino |
|---|---|---|---|
| B0 status quo | Skill Wiked 1.4.0 em harness local existente, modelo remoto, Python/uv/Knot, Git humano | Menor mudança; heterogeneidade e retomada dependem de disciplina/suporte | Controle |
| B1 local simplificado | B0 com versões conhecidas, instalação assistida, roteiro e suporte para primeiro SO | Padroniza sem construir editor/journal; não pressupõe instalador já lançado | Entrada recomendada condicional |
| B2/P aplicação local leve | Wiked + Pi SDK 1.1.0 fixado, UI/loader/credenciais próprios, núcleo futuro | Reutiliza modelo/sessão; construir domínio, distribuição e recuperação | Produto condicional; uma só candidata |
| B3 desktop/VDI/workspace | Workspace individual persistente, ferramentas preprovisionadas, acesso remoto, Git humano | Centraliza instalação; isolamento, backup, identidade e operação adicionais | Finalista de acesso |
| B4 harness hospedado | OpenCode V2 por operador/workspace com executor isolado e terminal humano | Reusa web/chat; operação e reconciliação banco+arquivos permanecem | Reserva/componente de B3 |
| B5 web fina | UI própria sobre OpenCode HTTP, núcleo/estado e sandbox | Poupa parte do agente, não workflow; reconexão e identidade novas | Não priorizar sem ganho claro sobre web existente |
| B6 workflow web | UI de fases/diff, backend de domínio, adapter agêntico e sandbox | Maior orientação/acesso, maior construção e serviço contínuo | Evolução condicional |
| B7 composição | Dify Human Input **ou** n8n Wait, UI, executor/núcleo/Knot | Pausa e integrações reais; múltiplos estados, licença e manutenção | Priorizar só com reuso organizacional justificado |

Pi pertence também à família workflow, mas não recebe voto duplicado. B3 com P/núcleo seria outra configuração, com novo custo, não a linha B3 original. Leitura canônica web + escrita local é composição transversal promissora; chat read-only ainda exige inferência, política e operação.

### 6.2 Ambientes concretos

- **Local:** sem servidor permanente incremental quando equipamento já existe, mas harness/modelo/suporte podem custar. Não exige Docker/WSL nem modelo local na hipótese leve. Interseção de SOs suportados por Node/Python/Knot/conversores ainda precisa confirmação.
- **Codespaces:** VM Linux dedicada por workspace; `/workspaces` persiste stop/start/rebuild. Outras áreas geralmente não sobrevivem rebuild; lifecycle commands podem rodar novamente. Fechar aba não para imediatamente, timeout padrão documentado de 30 min e saída contínua pode manter atividade. Exclusão não é recuperada pela simples persistência. GitHub não autentica Bitbucket automaticamente.
- **WorkSpaces Personal/Windows 365:** desktop persistente reduz provisionamento do cliente, mas mantém software, atualização e curadoria. WorkSpaces Pools estava fechado a novos clientes desde 2026-07-31 segundo a página consultada; não entra como nova opção. Bundle/protocolo e suporte browser importam.
- **Kasm 1.19.0:** mínimo do servidor 2 cores/4 GB/75 GB SSD **mais sessões**; padrão de sessão 2 cores/2768 MB. Cinco sessões reservam 10 cores/13840 MB, além do host; não é benchmark. Perfis persistentes precisam configuração. Licença/preço comercial não confirmado.
- **VS Code:** requisito do editor isolado de 1 GB RAM não é envelope de SO+Wiked+extensões. Documentação não assegura suporte do desktop completo em todo contêiner/VDI compartilhado. Remote SSH não sincroniza automaticamente cópia local.

### 6.3 Harnesses: diferenças que impedem tratá-los como equivalentes

| Candidato | Capacidade documental relevante | Lacuna para esta investigação |
|---|---|---|
| OpenCode V2 | TUI/desktop/web, skills, HTTP/client e SDK embutido; fonte MIT consultada | Senha/pairing não são RBAC multiusuário de filesystem; shell tem direitos do host. Eventos client são live-only, sem replay/reconexão automáticos. Console é inferência/políticas, não workspace hospedado comprovado |
| Codex Cloud atual | VM/workspace por tarefa, skills do repo, rede/secrets por mecanismos documentados; recuperação da VM por até 7 dias após atividade na configuração descrita | GitHub nativo; API key não habilita Cloud; não confundir Legacy. Prazo da VM não é retenção global/backup; browser/computer use não suportados no produto atual examinado |
| Claude Code cloud | VM gerenciada ou opção self-host, proxy de Git, histórico e diffs | GitHub nativo; bundle Bitbucket tem limites (<100 MB, untracked excluídos) e não dá push de retorno. Reabrir histórico não restaura necessariamente processos/arquivos; Remote Control continua executando na máquina original |
| Copilot cloud agent | Ambiente efêmero, branch/PR e revisão humana; firewall/credencial limitados | GitHub-only, sessão até 59 min; Author Copilot e humano coautor não equivalem ao Author humano exigido; fora da shortlist DOI nessa configuração |
| Devin | Bitbucket Cloud/DC nativos, VM por sessão, perfis de rede/MCP/Git | Uma skill ativa: outra substitui a anterior. Wiked→Knot/grill precisa prova; conta técnica não garante Author humano. Mudanças de perfil aplicam no boot/wake, não necessariamente imediatamente |

Hospedagem reduz processamento no cliente, mas nenhuma dessas opções foi comprovada como Wiked hospedado pronto. Memória, busca de código, DeepWiki ou RAG do fornecedor não substituem a autoridade da wiki configurada. Compromissos comerciais de retenção/treinamento, suporte e identidade variam por plano. Codex/Claude/Copilot ganham atratividade em instâncias GitHub; espelhar Bitbucket adiciona custódia/sincronização, não é integração gratuita. Devin é reserva real por Bitbucket, não solução integral já compatível.

Dify/n8n merecem distinção adicional: Dify pausa com formulário/token/run/user; n8n Wait pode persistir execução e retomar por webhook. Nenhum mecanismo prova qualificação Wiked ou vínculo ao diff. Timeout deve seguir pendente/expirado/rejeitado, nunca aprovação implícita. n8n usa SUL 1.0; Dify usa Apache modificada, com condições de multitenancy/branding. Cinco usuários do mesmo workspace não são necessariamente cinco tenants. Uso interno, distribuição e produto comercial precisam análise específica; não presumir licença irrestrita nem proibição universal.

## 7. Rubrica aplicada, notas e sensibilidade reproduzível

### 7.1 Gates antes de pontuar

G1 canonicalidade/compatibilidade; G2 autoridade/qualificação; G3 rastreabilidade; G4 execução/dados; G5 jornada íntegra. Estados: PD = passa documentalmente no conceito; C = condicional a adaptação identificada; U = desconhecido; F = falha comprovada. Não há passe por observação de implantação.

| Configuração | G1 | G2 | G3 | G4 | G5 |
|---|---|---|---|---|---|
| B0 | PD | PD | C | U | C |
| B1 | PD | PD | C | U | C |
| P | C | C | C | C | C |
| B3 | PD | PD | C | C | C |
| B4 | PD | PD | C | C | C |
| B5 | C | C | C | C | C |
| B6 | C | C | C | C | C |
| B7 | C | C | C | C | C |

B0/B1 não receberam segurança presumida: harness concreto/política não foram auditados. G4 condicional em P/remoto significa caminho de solução identificado, não aprovação corporativa. Nenhuma soma compensa falha de gate. Falham as **alegações/configurações** “Pi padrão + whitelist = confinado” e “ADR strict/AIShell padrão já entrega serviço multiusuário”. Corrigi-las cria configuração nova, com trabalho/custo próprios.

### 7.2 Critérios e escalas

| Critério | Peso base | Como pontuar de 0 a 4, maior é melhor |
|---|---:|---|
| C1 TCO prospectivo | 25 | Razão de custo completo contra baseline no mesmo horizonte |
| C2 esforço/prazo útil | 15 | Menor nota entre razões de pessoa-horas e dias decorridos |
| C3 facilidade das jornadas | 15 | Média de consulta, fonte/grill, diff/validação, retomada e entrega |
| C4 treino/reciclagem | 10 | Razão ponderada por perfis, incluindo retorno após inatividade |
| C5 instalação/update | 8 | Pior etapa obrigatória: de inviável a acesso já disponível e update com dono |
| C6 manutenção/operação/suporte | 10 | Mínimo entre atualizar, diagnosticar, retomar, restaurar e resolver conflito |
| C7 cliente modesto | 10 | Pior razão RAM/CPU/disco necessários versus folga pós-SO; SO/rede compatíveis |
| C8 reversibilidade/evolução | 7 | Portabilidade de conteúdo, decisões, identidade e evidência, não só Markdown |

C1+C2+C6 = 50: construir e sustentar têm metade do peso; C3+C4+C5 = 33 para adoção; C7 = 10; C8 = 7. Há sobreposição intencional entre dinheiro, prazo e atrito, examinada em cenário sem dupla valorização.

Razões C1/C2/C4: `r<=0,5 → 4`; `0,5<r<=0,8 → 3`; `0,8<r<=1,2 → 2`; `1,2<r<=2 → 1`; `r>2 → 0`. Baseline positivo consigo mesmo tem 2; zero exige referência alternativa explícita, não divisão por zero.

Escala operacional C3/C6: 0 inviável; 1 depende de especialista recorrente/improviso; 2 múltiplas ferramentas e ajuda em exceções; 3 checklist/recuperação documentados e ajuda ocasional; 4 roteiro curto estável sem assistência técnica recorrente. Revisão normal do curador não é penalizada como ajuda técnica.

C5: 0 inviável; 1 intervenção técnica recorrente/privilégio elevado; 2 passos documentados para usuário treinado; 3 pacote gerenciado com update/rollback; 4 canal já disponível com atualização atribuída. C7: razão máxima de uso/folga <=0,25 dá 4; <=0,5 dá 3; <=0,8 dá 2; <=1 dá 1; >1/incompatibilidade comprovada dá 0. Sem consumo/folga conhecidos, [0,4]. C8: 0 saída inviável; 1 onerosa/não especificada; 2 conteúdo preservado com reconstrução parcial; 3 conversão delimitada; 4 exportação documentada de todos os artefatos necessários e troca de provedor.

### 7.3 Matriz conservadora S2

Notas são **intervalos I/E de configuração prospectiva**, não capacidades medidas. S2: 5 indexadores, 30 leitores, 20 indexações e 60 consultas/mês, 12 meses, concorrência 2. Não há centrais justificadas. TCO, reciclagem e recursos permanecem abertos; a identidade matemática do baseline não o transforma em medição.

| Configuração | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Pontos base/100 | Cobertura informacional |
|---|---|---|---|---|---|---|---|---|---|---:|
| B0 | 2 | 2 | 1–2 | 2 | 1–2 | 1–2 | 0–4 | 2–3 | 36,8–56,8 | 90% |
| B1 | 0–4 | 0–4 | 1–3 | 0–4 | 1–3 | 1–2 | 0–4 | 2–3 | 11,8–87,5 | 40% |
| P | 0–4 | 0 | 1–3 | 0–4 | 1–3 | 1–3 | 0–4 | 2–4 | 11,8–76,8 | 55% |
| B3 | 0–4 | 0–3 | 1–2 | 0–4 | 2–4 | 1–2 | 0–4 | 2–3 | 13,8–82,0 | 55% |
| B4 | 0–4 | 0–2 | 1–2 | 0–4 | 2–4 | 1–2 | 0–4 | 1–3 | 12,0–78,3 | 55% |
| B5 | 0–4 | 0 | 1–3 | 0–4 | 2–4 | 1–2 | 0–4 | 2–3 | 13,8–74,5 | 55% |
| B6 | 0–4 | 0 | 1–3 | 0–4 | 2–4 | 1–2 | 0–4 | 2–4 | 13,8–76,3 | 55% |
| B7 | 0–4 | 0 | 1–3 | 0–4 | 2–4 | 1–2 | 0–4 | 1–3 | 12,0–74,5 | 55% |

Justificativas: C2 usa as faixas de preparo da seção 8. P mínimo 360/120=3 já dá 0; B3 mínimo 80/120=0,667 admite 3; B4 mínimo 120/120=1 admite 2; máximos de razão levam a 0. C3 [1,3] em B1/P/web representa potencial de roteiro/UI, **não UX presente comprovada**. C5 teto 3 local exige pacote/rollback ainda a construir; teto 4 web não torna backend gratuito. C6 teto 3 de P depende de journal/recuperação futuros; demais são limitados pela restauração/conflito. C8 tetos maiores P/B6 pressupõem registros portáveis; B4/B7 acrescentam estado externo.

Fórmula: `S_min = Σ(w_i × s_min_i)/4`; `S_max` análogo. Para P: mínimo `(15×1+8×1+10×1+7×2)/4=11,75`; máximo `(25×4+15×0+15×3+10×4+8×3+10×3+10×4+7×4)/4=76,75`. Arredondar só na apresentação, a uma casa decimal.

Cobertura informacional é a soma dos pesos com intervalo mais estreito que [0,4], inclusive estimativas. **Cobertura documental estrita de pontuação é 0% em todas as configurações**: nenhum critério tem D/O suficiente para todas as subvariáveis da configuração final. Isso não significa ausência de documentação forte; significa que documentação de componente não mede jornada, TCO ou consumo completos. Os 90% de B0 não são 90% de desempenho comprovado.

### 7.4 Sensibilidade numérica

Vetores C1..C8, todos somando 100:

- Base: 25,15,15,10,8,10,10,7.
- Tempo até valor: 20,30,15,8,7,8,7,5.
- Adoção/cliente: 15,10,22,15,10,8,15,5.
- Operação: 25,10,10,8,5,22,10,10.
- Sem dupla valorização monetizada: 40,10,20,0,8,0,15,7. C2 usa só prazo; B3 passa a [0,4], B4 a [0,3].

| Configuração | Base | Tempo | Adoção/cliente | Operação | Sem dupla |
|---|---|---|---|---|---|
| B0 | 36,8–56,8 | 39,0–54,8 | 32,5–58,8 | 35,8–57,5 | 35,5–59,3 |
| B1 | 11,8–87,5 | 10,0–89,3 | 12,5–86,8 | 14,3–82,8 | 10,5–91,3 |
| P | 11,8–76,8 | 10,0–62,5 | 12,5–80,0 | 14,3–80,8 | 10,5–83,0 |
| B3 | 13,8–82,0 | 11,8–79,8 | 15,0–81,3 | 15,5–79,0 | 12,5–88,3 |
| B4 | 12,0–78,3 | 10,5–72,3 | 13,8–78,8 | 13,0–76,5 | 10,8–85,8 |
| B5 | 13,8–74,5 | 11,8–61,0 | 15,0–79,3 | 15,5–74,0 | 12,5–83,3 |
| B6 | 13,8–76,3 | 11,8–62,3 | 15,0–80,5 | 15,5–76,5 | 12,5–85,0 |
| B7 | 12,0–74,5 | 10,5–61,0 | 13,8–79,3 | 13,0–74,0 | 10,8–83,3 |

Variação individual de cada peso em ±25%, redistribuindo os demais proporcionalmente, produz 16 execuções. Envelopes: B0 35,6–58,0; B1 10,8–88,5; P 10,8–80,1; B3 12,6–83,5; B4 11,0–80,1; B5 12,6–77,8; B6 12,6–79,6; B7 11,0–77,8. São mínimos/máximos entre execuções diferentes, não um novo cenário único.

Retirar as vantagens hipotéticas de P em recuperação (C6 máximo 3→2) e portabilidade (C8 máximo 4→3) reduz teto base em `(10+7)/4=4,25`, de 76,75 para **72,5**. C1 desconhecido ocupa 25 pontos, C4 e C7 mais 10 cada: reduzir essas incertezas vale mais que discutir décimos de peso.

**Conclusão numérica:** intervalos se sobrepõem em todos os vetores; nenhum mínimo domina os máximos dos concorrentes. Maior teto não é vitória; média de extremos não é score central nem probabilidade. As pontas não são independentes: menor esforço pode ser incompatível com máxima recuperação/UX. B1 é preferência contextual, não resultado de uma ordenação robusta.

### 7.5 Receita para reprodução

As matrizes acima são entradas completas. Pseudocódigo de cálculo, não implementação de produto:

```javascript
const score = (linha, pesos) => [0, 1].map(k =>
  linha.reduce((s, v, i) => s + v[k] * pesos[i] / 4, 0));
// Representar nota n por [n,n]. Não calcular central pela média.
const perturbacoes = base => base.flatMap((_, i) =>
  [0.75, 1.25].map(m => base.map((v, j) => j === i ? v*m :
    v*(100-base[i]*m)/(100-base[i]))));
const horas = (F, R, H, fatorF=1, fatorR=1) =>
  [0,1].map(k => fatorF*F[k] + H*fatorR*R[k]);
const prazo = F => [F[0]/4, F[1]/4+10];
const cobertura = (linha, pesos) => linha.reduce((s,v,i) =>
  s + (v[0] === 0 && v[1] === 4 ? 0 : pesos[i]), 0);
// No vetor sem dupla, alterar C2 de B3/B4 conforme descrito acima.
```

S1: 3 meses, 5 indexações+20 consultas/mês, 75 tarefas atribuídas, concorrência 1. S2: 12 meses, 20+60/mês, 960 tarefas, concorrência 2. S3: 36 meses, 40+200/mês, 8640 tarefas, concorrência 5. Tarefa não é chamada de modelo nem sucesso observado. Não se publica custo por sucesso sem número de jornadas aceitas.

Perfis M4/M8: 2 núcleos/4 GiB e 4 núcleos/8 GiB, sem GPU; N1 rede estável e N2 interrupção analítica de 10 min. C7 permanece [0,4] em ambos: não há folga/picos medidos. S1/S3 não recebem rankings artificiais; se volume comprometer recuperação/suporte, ampliar C3/C6 até evidência. A tabela de pesos é S2, não ensaio de carga.

## 8. Custos, recursos, treinamento e suporte

### 8.1 TCO completo, não só preço da VM

Para horizonte H e papéis p:

```text
TCO(H) = Σp cp × [Fp + formação_p + Σm Rp,m
                  + Σm trabalho_jornadas_p,m + saída_p]
         + Σm [licenças + infraestrutura + inferência + rede/armazenamento]
         + desembolsos únicos + cenário de incidente − residual justificado
```

`cp` é custo-hora carregado de cada papel; `F` preparo/construção prospectivos; `R` manutenção/operação/suporte técnico sem duplicações. Trabalho de jornadas inclui colaborador, Git humano, curadoria, retrabalho, conflito e retomada. Treinamento inicial entra uma vez; reciclagem é recorrente. Custo histórico afundado do baseline não entra. Saída e residual sem dados ficam parâmetros, não zeros implícitos.

Inferência = soma por modelo de tokens de entrada/saída/cache × tarifas correspondentes, mais cobranças específicas, retries/compaction/chamadas auxiliares. Não equiparar assinatura de chat a direito de API. Sem modelo/volume escolhido, não há total honesto em BRL nem tarifa por tarefa. Incidente sem probabilidade fundamentada é cenário separado, não valor esperado factual.

Publicar desembolso e TCO econômico separadamente; equipamento já disponível não é nova compra. Somar USD e BRL requer câmbio/data/impostos explícitos. Não repetir storage/compute já embutidos no plano. Horas de aluno e instrutor são pessoas diferentes; suporte não pode aparecer duas vezes como a mesma atividade em manutenção e operação.

Para custos lineares comparáveis `TCO_A=F_A+H×f_A+Q×v_A` e B análogo, o ponto de equilíbrio é `Q*=(F_A−F_B+H×(f_A−f_B))/(v_B−v_A)`, se denominador não nulo e hipóteses válidas. Degraus de assentos/capacidade exigem cálculo por trecho. Custo por jornada aceita seria TCO dividido por jornadas efetivamente aceitas; os volumes analíticos S1–S3 não fornecem esse denominador observado.

### 8.2 Esforço técnico comparável

**E, confiança baixa.** Uma pessoa-semana=40 h; dia técnico=8 h; cenário de calendário com 20 h/semana reservadas (4 h/dia útil), trabalho sequencial e 0–10 dias úteis de espera externa. Um SO inicial, escopo pequeno. Multiplataforma, HA, homologação, OCR/conversores complexos podem exceder faixas.

| Configuração | F inicial h | Prazo de cenário, dias úteis | R h/mês | F+3R h | F+12R h | F+36R h |
|---|---:|---:|---:|---:|---:|---:|
| B0 | 40–120 | 10–40 | 8–18 | 64–174 | 136–336 | 328–768 |
| B1 | 40–120 | 10–40 | 6–14 | 58–162 | 112–288 | 256–624 |
| P | 360–720 | 90–190 | 10–30 | 390–810 | 480–1080 | 720–1800 |
| B3 | 80–240 | 20–70 | 10–26 | 110–318 | 200–552 | 440–1176 |
| B4 | 120–320 | 30–90 | 12–32 | 156–416 | 264–704 | 552–1472 |
| B5 | 480–960 | 120–250 | 22–48 | 546–1104 | 744–1536 | 1272–2688 |
| B6 | 640–1200 | 160–310 | 22–56 | 706–1368 | 904–1872 | 1432–3216 |
| B7 | 480–1040 | 120–270 | 22–56 | 546–1208 | 744–1712 | 1272–3056 |

Origem: B0/B1 1–3 pessoa-semanas de preparo no estudo de aplicações; P 9–18 no estudo Pi; B5/B6/B7 no estudo aplicações. B3 2–6 e B4 3–8 são estimativas adicionais da comparação para imagem, dependências, identidade, isolamento, backup e runbook. Não são cotações nem custo histórico.

R foi decomposto na comparação, por hipótese de atividades disjuntas: B0 manutenção 4–8 + operação 4–10; B1 4–8 + 2–6; P 8–24 + 2–6; B3 8–16 + 2–10; B4 8–16 + 4–16; B5 16–32 + 6–16; B6/B7 16–40 + 6–16 h/mês. **Não inclui trabalho do colaborador/curador, formação nem evolução de escopo.** Se houver sobreposição, retirar antes de orçar. Incidentes podem exceder limites. Manter R de S2 ao variar H isola horizonte; não dimensiona S3 automaticamente.

Se B0 já estiver integralmente provisionado, F=0 prospectivo; C2 próprio é 4 e candidatas positivas precisam referência alternativa, por exemplo 80 h/20 dias explicitamente analíticos. Não dividir por zero nem atribuir custo fictício ao baseline para favorecer produto novo.

### 8.3 Preços condicionais e exclusões

USD, fotografia documental de 2026-10-10. Nenhum contrato/região brasileira confirmado. Os exemplos de cinco usuários não estimam tarefas atendidas, consumo de modelo ou TCO.

| Oferta/configuração | Conta documental/ilustrativa | Condições e exclusões principais |
|---|---|---|
| Codespaces | 2 cores US$0,18/h; 4 cores US$0,36/h; disco US$0,07/GB-mês. 20×0,18+10×0,07=US$4,30; 80×0,36+10×0,07=US$29,50 por pessoa. Cinco: US$21,50–147,50/mês | Pontas mudam SKU e horas. Sem quota gratuita corporativa presumida; storage efetivamente cobrado, ociosidade, prebuild/Actions e extras importam |
| WorkSpaces Personal | Exemplo Oregon Ubuntu Power: 7,25+20×0,66=US$20,45; 80 h dá US$60,05. Cinco US$102,25–300,25. Outro SKU Windows Standard AlwaysOn: US$44, cinco US$220 | Bundles/volumes/SOs diferentes; não calcular ponto de equilíbrio cruzando SKUs. IPv4/diretório/serviços adicionais podem cobrar |
| Windows 365 Business | Planos EUA examinados US$36 (2 vCPU/8 GB/128 GB) e US$56 (4 vCPU/16 GB/128 GB). Cinco US$180–280/mês | Assinatura mensal renovável; preço/termos regionais e software adicionais. Cancelamento tem implicações de dados |
| Host próprio/Kasm | Envelope E de host pequeno US$30–150/mês; Kasm US$50–200 de infraestrutura | Baixa confiança, sem cotação/SLA ou garantia de cinco sessões pesadas. Licença Kasm não confirmada; acrescentar operação/backup/licenças |
| OpenCode Console | Go US$10, Go Plus US$40/mês documentados | Inferência, não VM/workspace; self-host soma sandbox, disco, backup, operação e provedor |
| Codex Business | US$20/usuário-mês equivalente anual (2+), US$25 mensal; cinco US$100/125 + extras | Créditos/limites/uso compartilhado; Enterprise por cotação. API key não substitui entitlement Cloud |
| Claude individual | Pro US$20 mensal ou US$200 anual; Max desde US$100. Cinco Pro mensais US$100 | Não equivale a Team/Enterprise; cotas compartilhadas e política consumer diferente de comercial; preço corporativo não suficientemente apurado |
| Copilot | Business US$19 e 1900 créditos; Enterprise US$39 e 3900; extra US$0,01/crédito. Cinco US$95/195 + extras | Planos/contrato GitHub e pool; extra habilitado por padrão na documentação consultada; sem adequação Bitbucket nesta configuração |
| Devin | Guia self-serve: full US$40/assento, Teams mínimo US$80; cinco full US$200 + uso; flex sem fixo por assento sob mínimo | Confiança média: página comercial retornou 404, guia oficial usado; mínimo em créditos não garante volume; retenção/treino variam por plano |

Excluídos dessas faixas diretas: impostos/câmbio, internet/equipamento/energia já disponíveis, inferência quando não incluída, assinaturas adicionais, identidade/diretório, storage/egress/backup extras, desenvolvimento, testes/hardening, integração Bitbucket, treinamento, suporte interno, revisão e retrabalho. Uma parcela já existente pode ter custo marginal baixo; não presumir zero nem duplicá-la.

O estudo de ambientes propôs reserva **E** de API US$10–50/indexador-mês, cinco US$50–250, apenas para sensibilidade. Não é tarifa, teto ou previsão: contextos longos/loops podem exceder muito. Este relatório mantém o modelo parametrizado como base, não essa reserva como orçamento.

Trinta leitores em Cloud PCs US$36–56 acrescentariam US$1080–1680/mês. Codespaces 30 leitores, 1 h/2 cores e 10 GB cada: `30×(0,18+0,70)=US$26,40/mês`, mas com onboarding/identidade/workspace por leitor. Diferença de preço não resolve experiência, entitlement ou necessidade de consulta conversacional.

### 8.4 Recursos e suporte residual

Local com inferência remota não carrega pesos de LLM e não exige GPU. Ainda executa UI, busca/parsing, Node/Python/Knot, validação e conversores. Perfil exploratório local: 2 núcleos, 4–8 GB totais; 4 GB pode ser apertado com SO/browser/editor. Reserva estimada de 2–5 GB de disco livre para ferramentas/caches exclui corpus e opcionais. Perfil browser estimado: 0,5–2 GB RAM/cache; não é mínimo oficial nem pico medido. C7 ficou aberto por isso.

Envelopes remotos do estudo AIShell, **não dimensionamento aprovado**: 2 escritores×2 GiB+2 GiB de controle=6 GiB, host 8 GiB de ensaio; 5×2+2=12, host 16; 5 exportações×4+2=22, host 32 ou serialização. CPU, disco, runtime/gVisor/VM e leitores agênticos acrescentam carga. Storage = imagens/cache + cópias + checkpoints + logs + backups, não apenas tamanho da wiki.

Rede remota sustenta UI além da inferência. Referências de fornecedor não são requisitos Wiked: WorkSpaces documentou 1 Mbps para vídeo 480p e RTT DCV recomendado <250 ms; Windows 365 traz exemplos de aproximadamente 100–150 Kbps em Word até 6–6,5 Mbps em navegação gráfica. É necessário medir a jornada/dispositivo real. Offline local pode permitir Markdown/diagnóstico/validação já provisionados, não chat com modelo remoto.

Suporte mantém SO/PATH/versões, credenciais/proxy, rede, conflitos, backups e restauração. Curadoria decide semântica e publicação. Local distribui instalações; remoto centraliza e concentra indisponibilidade. Não há responsável, SLA ou operação 24×7 demonstrados.

### 8.5 Formação e economia: reconciliação das estimativas

Ambientes/Git reservaram 2–4 h/indexador para fundamentos/jornada/Git, 15–30 min/leitor e 0,5–1,5 h/indexador para acesso padronizado (heterogêneo 1–3 h). Para 5+30 pessoas: base `5×(2–4)+30×(0,25–0,5)=17,5–35 h`; com acesso padronizado, **20–42,5 h de alunos/acesso**; heterogêneo, 22,5–50 h. Instrutor, preparo, primeiras entregas e reciclagem ficam à parte. As duas sessões de 45–60 min propostas no estudo Lucas podem compor a formação; não são garantia de suficiência nem pacote adicional a somar cegamente.

Sensibilidade técnica H=12:

| Configuração | F 0,5×, R base | Base | F 2×, R base | F base, R 0,5× | F base, R 2× |
|---|---:|---:|---:|---:|---:|
| B1 | 92–228 h | 112–288 h | 152–408 h | 76–204 h | 184–456 h |
| P | 300–720 h | 480–1080 h | 840–1800 h | 420–900 h | 600–1440 h |

Mudar a estimativa de construção também muda C2: com F_P reduzido à metade, razão mínima 180/120=1,5 permite nota 1, enquanto a ponta maior segue 0. O teto base de P poderia aumentar 3,75 pontos por esse critério. Não manter a nota original rígida depois de trocar sua premissa; tampouco interpretar multiplicador de estresse como probabilidade.

Investimento incremental P−B1 = **240–680 h**. Se g é economia mensal líquida em horas equivalentes, já descontados manutenção/desembolsos adicionais e normalizados custos-hora, retorno simples = ΔF/g. Com g=10: 24–68 meses; g=30: 8–22,7; g<=0: nenhum retorno simples. Para H=3/12/36, g precisa de 80–226,7 / 20–56,7 / 6,7–18,9 h/mês. São limiares, não ganhos previstos.

O estudo de aplicações calculou 36–72 meses com 10 h/mês usando **todo F_P=360–720 h**, não incremento contra B1; ambos os cálculos são válidos para perguntas diferentes. Não escolher a cifra mais favorável sem informar denominador/base. Em S2, ganho hipotético de 15 min em 80 jornadas gera 20 h/mês **brutas**, antes de manutenção. Consultas/indexações não têm duração igual demonstrada.

B3 contra B1, exemplo fixo: ΔF=80 h, ΔR=4 h/mês, despesas extras US$100/mês; em 12 meses requer economia >`80/12+4+100/c` horas equivalentes/mês. Com c=US$30/h didáticos, **14 h/mês**. Não é taxa corporativa. Infraestrutura já operada pode inverter sinal; acesso inviável pode justificar remoto mesmo sem economia.

## 9. Pi: viabilidade real, superfície e limites

### 9.1 O que o SDK oferece

Referência aprofundada 1.0.0, confronto dirigido com 1.1.0; candidata futura fixada em 1.1.0 com dependências fixadas, não `latest` flutuante. Pacotes atuais `@earendil-works/pi-coding-agent`, pi-agent-core, pi-ai e pi-tui; exemplos antigos `@mariozechner` exigem revisão. Node >=22.19.0. MIT permite modificação/redistribuição com avisos, não concede automaticamente marca nem resolve transitivos/termos de provedores.

APIs documentadas incluem `createAgentSession`, `ModelRuntime`, `ResourceLoader`, `SettingsManager.inMemory`, `SessionManager`, `tools/noTools/excludeTools/customTools`, prompt/subscribe/dispose. Nomes/padrões vão em tools; definições em customTools. Chamada mínima herda descoberta, configurações, credenciais e persistência. SDK não carrega automaticamente codemode/tool_search/MCP built-ins da CLI, mas DefaultResourceLoader continua sendo descoberta, não modo seguro vazio.

SessionManager recompõe contexto em árvore JSONL; compaction não é ata de aprovação. Troca/fork/import recria serviços e exige religar subscriptions. `agent_end` não implica fim de toda recuperação/fila; `agent_settled` não significa que efeito Wiked foi validado. Estado do domínio precisa existir fora da conversa.

### 9.2 Por que whitelist e TUI padrão não bastam

| Caminho | Evidência/risco documentado | Recomendação para P, ainda por construir |
|---|---|---|
| Built-ins read/bash/edit/write e demais ferramentas | Cwd é diretório, não fronteira de filesystem | Operações Wiked tipadas, sem shell/path livre |
| Configuração global/projeto/ancestrais | agentDir, .pi, .agents, AGENTS/CLAUDE/SYSTEM podem alterar contexto/recursos | Loader próprio com origens explícitas; contexto canônico por rota permanece permitido |
| Extensões/pacotes/hooks | Código TS/JS roda com direitos do processo; resolução pode instalar/carregar antes de filtros posteriores | Código empacotado/revisado; não confiar em filtrar resultado depois de executar loader |
| DefaultResourceLoader | Resolve packageManager antes de noExtensions; paths explícitos permanecem; override pode ocorrer após loadFinalExtensionSet | Não usar override tardio como prova de ausência de execução |
| MCP/codemode/deferred/tool_search/ctx.executeTool | Registrado, ativo e callable são conjuntos distintos | Não registrar/conectar mecanismos indiretos por padrão; auditar callable, startup e retomada |
| TUI/RPC | !/!!, editor externo, export/share/import/bug/reload/settings/model/login/trust e comandos adicionais | UI pequena própria; não expor TUI/RPC integral. !! só exclui saída do contexto, não impede shell |
| Credenciais | auth/models/MCP admitem !comando; ambiente pode carregar credenciais cloud; logout não revoga provedor | Adaptador próprio, segredo fora de prompt/argv/log/instância, endpoint/modelo explícitos |
| Sessões/import/cwd | Retomada pode reconstruir serviços/recursos; sessionDir lido antes de trust | Reaplicar política/raiz/identidade; transcript não herda consentimento |

Diferença versionada decisiva: em 1.0.0, custom/ext tools não recebiam o mesmo filtro de built-ins; em 1.1.0 passam por `_isAllowedTool`, **mas MCP pode permanecer fora de uma allowlist comum**, salvo filtro/exclusão específicos ou desativação total. Modificadores `+/-` não equivalem a allowlist. Logo “só listar tools Wiked” não demonstra ausência de carga/conexão MCP.

Na base 1.0.0, InteractiveMode recebe AgentSessionRuntime, não AgentSession nua: exemplos simplificados com assinatura diferente são pseudocódigo. Branding documentado para fork não é botão de renomear SDK. Preferência R: host/UI próprios, eventualmente componentes pi-tui, sem fork grande antes de demonstrar necessidade.

`auth.json` não é cofre cifrado demonstrado. Comandos de chave em auth podem cachear stdout; apiKey/headers de models podem executar por request; MCP também pode executar comandos. Pi 1.1.0 corrigiu autoload `.env` no standalone, lembrando que embalagem altera superfície. A aplicação precisa controlar catálogo/update/cache warming/telemetria, não supor que somente prompt manual gera rede/custo.

### 9.3 Núcleo/CLI/skill/chat e dependências

CLI determinística futura deve ler, planejar, validar, aplicar autorizado e reconciliar sem LLM/chave. Chat Pi usa essas operações; skill em outros harnesses também pode usá-las. O validador Python permanece inicialmente único; não reescrever schema/regras em TypeScript por conveniência do SDK. Instalação única pode empacotar Node+Python/uv+Knot e opcionais, mas não os elimina.

P requer núcleo de plano/diff, bases, seleção de fontes, autorização humana, efeitos e journal; não apenas wrapper do validador. Decomposição E original: núcleo/estado 3–6 pessoa-semanas; SDK/UI 2–4; distribuição/endurecimento/provas 3–6; documentação/treino 1–2, total indicativo 9–18. Possível sobreposição não é promessa de prazo de produção. Múltiplos SOs/conversores podem exceder.

**Condição local sem sandbox:** host/processo/dependências confiáveis e risco residual avaliado posteriormente. Tools restritas reduzem ações do modelo, mas não contêm extensão/parser comprometido, malware, dono local ou acesso do processo à rede/segredos. Ler localmente não autoriza enviar ao provedor. **A skill externa não herda contenção do chat:** outras ferramentas do harness podem escrever/rodar shell por fora. Remoto continua exigindo sandbox.

## 10. Requisitos, ameaças, privacidade e execução remota

### 10.1 Catálogo proposto, não controles entregues

O estudo de requisitos distinguiu C01–C08 (restrições do acordo) de P01–P32 (propostas). O quadro preserva os 32 itens em grupos verificáveis; nenhum deles é declarado implementado por existir neste relatório.

| IDs | Requisito proposto | Prova futura essencial |
|---|---|---|
| P01–P04 | Raiz/compatibilidade, papéis ler/propor/aplicar, confirmação humana ligada ao objetivo/plano, paths/pais reais | Instância errada, confirmação forjada e traversal/symlink não produzem efeito |
| P05–P06 | Loader/settings/credenciais Pi próprios; mesma política nas operações do núcleo; limite explícito do harness externo | Sentinelas de descoberta e paridade de recusa CLI/chat/skill |
| P07–P08 | Segredos fora de contexto/log/argv; minimização e endpoint/modelo autorizados | Canários e captura de requests sintéticos; revogação efetiva |
| P09–P10 | Sandbox remoto, launcher externo, segregação, egress deny-by-default | Tentativas entre usuários/host/metadata/rede falham |
| P11–P13 | Subprocessos aprovados, identidade por papel/objeto, renderização/entrada sem conteúdo ativo | Parser travado/argumento malicioso/XSS/ANSI/CSRF tratados conforme interface |
| P14–P16 | Runtime único, plano/base/journal, escritor por workspace e detecção de concorrência | Mesmos diagnósticos, queda multifile detectável e base obsoleta bloqueada |
| P17–P19 | Checkpoint fora da conversa, idempotência/reconciliação, archive selecionado sem colisão | Retomada sem transcript e sem repetir efeito incerto |
| P20–P22 | Degradação offline, backup/restore, estados locais versus publicação | Perda de rede/volume e PR falho preservam diagnóstico/realidade |
| P23–P25 | Cliente sem GPU obrigatória, quotas/fila/cancelamento, orçamento por tarefa | Medir recursos e loops; limites preservam estado e vizinhos |
| P26–P28 | Auditoria mínima, métricas úteis, versões/integridade/rollback | Reconstruir entrega sem transcript; update não migra instância implicitamente |
| P29–P32 | Treino/acessibilidade, responsáveis/runbooks, retenção por classe, evolução sem duplicar autoridades | Onboarding/restore/incidente/expiração e saída portável comprováveis |

### 10.2 Modelo de ameaças

Ativos: conteúdo/contrato, fontes, decisões/tickets, identidades/segredos, host/rede, sessões/journal, orçamento e publicação. Atores: usuário legítimo sujeito a erro, fonte hostil, modelo induzido, pacote/parser comprometido, outro usuário remoto, atacante de conta/rede e administrador privilegiado. Fronteiras: fonte→modelo; modelo→núcleo/confirmador; processo→SO; usuário/instância→outros; cliente→provedor; arquivos→Knot/archive/PR; projeto→launcher; rascunho→publicação.

| Ameaça do catálogo | Controle proposto | Limite residual |
|---|---|---|
| T01 injection/autoridade | Fonte é dado; tool tipada; confirmação fora do modelo | Conteúdo semanticamente errado dentro do escopo ainda exige curadoria |
| T02 escape de path | Pais reais, traversal/links/TOCTOU, rechecagem no uso | Checagem de string não contém processo comprometido |
| T03 código indireto/supply chain | Loader explícito, binários fixos, sem autoload/instalação | Transitivos vulneráveis conservam privilégios do processo |
| T04 exfiltração | Contexto mínimo, segredos separados, política de provedor | Allowlist não impede envio indevido ao destino permitido |
| T05 SSRF/lateral | Rede externa ao guest, validar DNS/redirect/IPv4/IPv6 | Endpoint permitido comprometido continua risco |
| T06 cruzamento de sessão/tenant | Workspace/segredos segregados, autorização por objeto | Administrador/host é domínio privilegiado |
| T07 identidade/consentimento/replay | Vínculo humano a plano/base/revisão, auditoria | Dono local pode adulterar registros no próprio SO |
| T08 corrupção/conflito | Journal, comparação de base, recibos, recuperação | Não há transação mágica entre sistemas; terceiro estado exige humano |
| T09 DoS/custo | CPU/RAM/PIDs/disco/tempo/tokens, fila e cancelamento | Chamada enviada pode já cobrar; quota pode interromper tarefa |
| T10 política remota adulterada | Launcher/configuração fora do projeto, sem socket Docker | Bugs de runtime/kernel permanecem possíveis |
| T11 persistência indevida | Retenção por classe, minimização, revogação | Provedor, exports humanos e backup têm ciclos próprios |
| T12 publicação equivocada | Revisão identificada, diff integral, curador | Validador não prova verdade; humano também pode errar |
| T13 conteúdo ativo em UI/export | Renderização segura, limites de upload/link/ANSI | Biblioteca/conversor vulnerável requer contenção adicional |

### 10.3 AIShell correto e desenho remoto

O produto pertinente é **UniSoma/aishell**, identificado no README local, não PowerShell/AIShell. O snapshot examinado lança Docker efêmero e aceita uso SSH/script; isso torna execução server-side plausível, mas não oferece serviço multiusuário pronto.

Achados de código E4: projeto gravável por bind mount; diretório Git comum de worktree pode ser montado; flags/mounts perigosos recebem avisos consultivos; entrypoint configura sudo sem senha e depois troca usuário; chaves entram como ambiente; estado de harness persiste; `/tools` pode ficar gravável com pacotes Pi; não são injetadas quotas padrão. Projeto pode influenciar herança/flags de lançamento. Efemeridade não desfaz dano em volume persistente. Identidade Git lida do host é metadado, não autenticação do operador.

ADR 0006 propõe strict, proxy de saída e hardening, mas parser/launcher do SHA não demonstram esses controles implementados. O ADR exclui multi-tenant do modelo. Não contabilizar intenção como funcionalidade. Root no contêiner não é automaticamente root no host; Docker também não é contenção universal, especialmente com daemon/mounts/configuração amplos.

Desenho remoto R: cliente autenticado → gateway/autorização → fila/gerenciador confiável → sandbox por domínio de confiança/execução → workspace privado; rede controlada externamente; resultado como pacote revisável ao humano. Sem socket Docker, home comum, imagem/flags escolhidas pelo modelo ou credenciais de merge. Imagem por digest, usuário não privilegiado, limites, seccomp/capabilities compatíveis; rootless/gVisor/VM devem ser avaliados, não aprovados pelo nome. `cap-drop ALL` pode exigir adaptação do entrypoint; não supor compatibilidade.

Bloquear egress direto, LAN/link-local/metadata, DNS arbitrário e bypass de proxy; revisar redirects/resolução. Preferir broker de modelo sem token principal no guest quando compatível; segredo necessário dentro do processo continua exposto. Auditoria remota fora do workspace, sem transcript bruto por padrão. Backup e restore independentes de stop/start/rebuild. Responsáveis por versões, incidentes, quotas, revogação e retenção precisam existir.

### 10.4 Retenção e metas exploratórias

Propostas E do catálogo, **não política autorizada**: conversa apenas durante sessão ou 7–30 dias após atividade; journal/diff até reconciliação e janela adicional 7–30 dias; metadados diagnósticos 30–90 dias; temporários limpos em sucesso/falha, órfãos até 24 h; backup diário com janela 7–30 dias. Conteúdo canônico, decisões/proveniência e raw/archive seguem política própria, não TTL de chat. Credencial deve ser revogada no provedor; logout/apagar pasta não apaga todas as cópias.

Também exploratórios: RSS do app até 512 MiB/1 GiB para ensaio, não conjunto do SO; resposta de interface/cancelamento ~1 s e navegação pequena 1–3 s; RPO de desastre até 24 h com backup diário versus checkpoints 5–15 min; RTO 4–8 horas úteis versus um dia útil; SLO remoto 99%/99,5% de janela ainda a definir. Nenhum valor foi atingido, contratado ou medido. Crash de processo e perda total de dispositivo são falhas diferentes.

Lacunas corporativas: classificação de dados, provedor/modelo/endpoints, DPA/treinamento/residência, SSO/MFA/RBAC, SO/hardware/rede, retenção/legal hold, licença, suporte, curadoria, RPO/RTO/SLA e orçamento. Essas lacunas não impedem concluir pesquisa, mas impedem chamá-la de aprovação de dados reais/implantação.

## 11. Arquitetura proposta, identidade e compatibilidade

### 11.1 Separar o que cada camada decide

```text
B1: pessoa -> harness + skill -> Markdown/contrato + runtime Python + Knot
              roteiro/checkpoint assistidos -> Git/PR humanos -> curador

P:  pessoa <-> UI/host Wiked <-> adaptador Pi <-> provedor autorizado
                  | confirmação humana
    CLI sem LLM --+--> núcleo de operações --> arquivos/journal
    skill externa-+          |                runtime Python único
                             +--------------> Knot CLI / opcionais
    pacote revisável -----------------------> Git/PR humanos -> curador

B3: cliente -> identidade/gateway -> executor isolado + workspace persistente
                                      B1, ou futuramente P
                                      backup/quotas/auditoria externos
```

Módulos propostos: host/UI apresenta fase/revisão/pendência e recebe humano; adapter Pi traduz tools/contexto sem tipos Pi no domínio; núcleo concentra plano/escopo/bases/efeitos/reconciliação; adapter runtime preserva autoridade estrutural; adapter arquivos controla staging/movimento; adapter Knot usa CLI; journal guarda recibos e estado; opcionais invocam motores aprovados; entrega compõe pacote sem operar Git.

A interface de domínio deve esconder uma sequência complexa de lock, escrita e recuperação, não obrigar cada frontend a reinventá-la. Famílias conceituais: contexto/leitura; preparar plano; executar autorizado; inspecionar/reconciliar; validar/entregar. Não são comandos já existentes. Envelope futuro inclui versão, instância/raiz, ator/papel, ticket/objetivo, operação/base e argumentos limitados; resultado distingue concluído, pendente, incerto, incompatível, negado e parcial. Não aceitar `approved:true` fornecido pelo modelo como atalho CLI.

### 11.2 Estado, concorrência e recuperação

Journal fora de wiki/diretórios governados, vinculado a instância/workspace, separado de conversa/segredos. Não definir identidade apenas pelo caminho absoluto: restauração pode mudar caminho, cópia não pode herdar consentimento. Identificadores de instância/workspace/sessão/tarefa/operação são proposta; não adicionar UUID ao contrato vigente sem decisão própria.

Checkpoint: raiz/versões/política, ator/qualificação por sessão/objetivo, ticket, fontes/fingerprints, decisões abertas/confirmadas, plano/diff/bases/resultados, operações/recibos, validação/avisos e próximo responsável. Conversa Pi é auxiliar; logs locais não são invioláveis sob o mesmo usuário.

Aplicação recuperável proposta: preparar candidato/diff e journal durável; conferir confirmação e base; lock cooperativo; revalidar imediatamente ao efeito; staging/substituições controladas; validar bytes finais; arquivar seleção; reconciliar Knot; entregar. Hash/CAS lógico não é primitiva atômica universal contra editor hostil. Vários renames não tornam página+índice+Knot+archive+PR uma transação distribuída.

Na queda, cada arquivo é base, resultado esperado ou terceira versão. Base permite efeito faltante ainda autorizado; resultado impede repetição; terceira versão requer intervenção/novo plano. Nada de rollback cego. Timeout Knot exige consultar antes de repetir; marcador em nota não cria exactly-once. Lock de uma cópia não impede conflito entre dois workspaces nem conflito semântico em merge textual limpo.

### 11.3 Git humano e identidade Bitbucket

Fluxo inicial: suporte configura conta individual/nome/e-mail por repo; humano confirma branch/base/trabalho pendente, sincroniza e cria branch por tarefa; acompanha grill/edição; revisa diff geral e staged, novos/deletados; seleciona só arquivos autorizados; valida; confere Author/Committer; envia branch e abre PR; curador revisa revisão final e integra. Não incluir raw, sessão, segredo ou trabalho alheio por staging indiscriminado. Persistência raw/archive continua humana.

Cinco identidades: **Author** do conteúdo; **Committer** que materializa commit; **ator autenticado** do push/API; **autor do PR**; **revisor/integrador**. Alias de e-mail melhora mapeamento visual, não prova autoria. Assinatura/sign-off/coautor não substituem qualificação ou revisão. Author humano com Committer técnico é representável, mas API que aceita author não prova controle independente de Committer. No Cloud, PR pertence ao principal autenticado; token técnico não se torna pessoa por alterar metadado.

Cloud: branch permissions e merge checks são controles distintos; regras sobrepostas podem ampliar acesso. Sem Premium, checks podem avisar sem bloquear; processo manual é possível, mas não enforcement automático. OAuth `pullrequest:write` inclui operações além de criar PR e implica escrita: não é permissão exclusiva de submissão. API tokens têm scopes próprios, são pessoais e não devem ser compartilhados; app passwords depreciados não são escolha nova.

Data Center: não aplicar nomenclatura Premium Cloud. Docs 10.5/REST v1002 diferem; página de tokens tem ambiguidade entre Bearer e Basic com x-token-auth e condições de merge/identidade. Validar categoria/versão efetiva. Não usar bypass de Verify Committer como solução. Preferência inicial por estratégia que preserve commits originais; squash/rebase exigem prova de atribuição e política próprias.

Recuperação humana: preservar trabalho antes de sincronizar; abort pode não reconstruir alterações soltas; push rejeitado exige entender avanço, não force-push rotineiro; erro publicado pede correção/revert revisado; reflog é local/expirável, não backup nem garantia para arquivo nunca commitado. Perda de VDI pode perder rascunho/raw/conversa não enviados.

Publicador futuro é módulo separado com consentimento humano ligado a revisão/hash, identidade verificada, mínimo privilégio, idempotência e recibos; merge continua com curador. API upload que cria commit também publica: não contorna proibição vigente de Git pelo agente. Essa evolução requer ticket/grill e decisão próprios, não faz parte da autorização atual.

### 11.4 Versões e decisões relacionadas

Registrar separadamente app/protocolo/checkpoint, Wiked/metodologia/contrato/schema, runtime/hash, Knot/JSON, Pi/Node, Python/libs e conversores. Reutilizar Python primeiro; eventual migração exige benefício demonstrado, fixtures diferenciais e cutover que retire autoridade antiga. Não manter dois validadores normativos divergentes. Lock/artefato íntegro e rollback devem impedir download/update inesperado no meio da tarefa; pacote global não determina raiz da instância.

O estudo arquitetural confrontou seis decisões abertas, recuperáveis via Knot:

| Decisão | Relação com proposta | Fronteira |
|---|---|---|
| `wik-01m2tphwrc4f`, publicação/versionamento | Custódia, canais, integridade, instalação/update | Decisão correspondente necessária para distribuir P oficialmente; não bloqueia pesquisa/B1 provisionado |
| `wik-01m2tpkz9x55`, capacidades opcionais | Namespaces/lazy/dependências explícitas | Evolução independente; não assumir skill já decomposta nem autoload arbitrário |
| `wik-01m17qfp6n6c`, projeção semântica | Índice derivado reconstruível com retorno ao Markdown | Não aprovado nem obrigatório; navegação vigente permanece |
| `wik-01m310mknyjs`, diagramas | Autorização por criar/ajustar/regenerar/exportar | Resolver antes de automatizar permissões ambíguas; fluxo especializado preservado |
| `wik-01m310mkwb5f`, termos durante grill | Exceção estreita de registro versus confirmação final | Não substituir guias por regra genérica nova de zero escrita; representar exceção ou reservar operação especializada |
| `wik-01m310mm3e55`, contexto canônico | Carregamento por rota, inclusive bootstrap | Contexto terminológico não vira evidência; loader futuro precisa decisão correspondente |

Esses IDs são governança futura, não novas dependências bloqueantes deste relatório. Qualquer criação/alteração metodológica posterior deve seguir a autoridade e o grill próprios definidos em L1.

## 12. Divergências reconciliadas e incertezas preservadas

| Divergência entre estudos/fontes | Reconciliação adotada | Incerteza restante |
|---|---|---|
| Baseline inicialmente 17 arquivos | Correção posterior explícita: 16; 17 é quantidade de filhos | Inventário é snapshot local, não release assinada |
| Jornadas numeram entrega/retomada em ordens distintas | Mesmas atividades; rubrica usa J4 retomada/J5 entrega; percurso deste relatório usa nomes | Não criar ordem normativa por numeração |
| Pi em jornadas/main versus estudo versionado | Parecer 1.0.0→1.1.0 e confronto direto prevalecem; snippets main não fixam tag | Auditoria transitiva e artefato final ausentes |
| Pi “candidata preferencial” versus “sem vencedor” | Preferência de produto/estratégia, não ranking comprovado. B1 entrada por reuso | TCO/UX podem inverter escolha |
| C6/C8 favorecem teto de Pi futuro | Benefícios são condicionais; retirar ambos reduz teto 4,25 pontos | Nenhum journal/portabilidade de produto foi construído |
| Suporte local 2–6 h/mês versus P 10–30 | Primeiro só operação de ambiente estabilizado; segundo soma manutenção software 8–24 | Remover sobreposição real antes de orçamento; não somar novamente |
| Treino 2–4 h versus duas sessões 45–60 min | Reserva do caso Lucas pode compor formação; não é pacote adicional nem suficiência | Tempo/reciclagem reais U |
| Payback Pi 36–72 versus 24–68 meses a 10 h/mês | Primeiro usa F total; segundo investimento incremental contra B1 | Ganho líquido não foi observado |
| Kasm índice dizia 2 GB/sessão | Página direta 1.19.0 com 2768 MB prevaleceu | Imagem/carga e licença comercial precisam confirmação |
| AIShell ADR strict/proxy versus código | Não contar intenção como controle entregue no SHA | Nova release exigirá nova inspeção/prova |
| Scores amplos versus números precisos de preço | Preço de SKU é D; TCO/jornada incluem muitas parcelas U/E | Pontas de preço mudam tamanho/uso, não intervalos estatísticos |
| “Só navegador” versus cliente modesto | Desloca computação, não elimina memória/rede/custo total | Picos/folga e responsividade não medidos |
| Pausa Dify/n8n versus ausência de domínio | Reconhecer pausa humana real; não equivaler a grill/autorização por diff | Integração/retomada/versão/licença concretas pendentes |
| “Sessão persiste” versus recuperação | Conversa, workspace, journal e backup são objetos diferentes | Restore e falhas parciais precisam prova |
| Git manual possível versus controles Bitbucket | Percurso pode ser humano; enforcement depende de edição/plano/configuração | Instalação real Cloud/DC não identificada |

Não foram escondidas lacunas sob médias. Gate desconhecido vem antes de pontuação; configuração incompatível deve mudar ou sair, não receber ajuste cosmético de peso. Todos os números de engenharia podem ser excedidos. Não existe orçamento/SLA corporativo aprovado nem preferência real de Lucas neste material.

## 13. Provas futuras: o que resolver antes de alegar produto pronto

Plano documental do estudo de viabilidade, **nenhuma prova executada nesta investigação**. Requer autorização própria, versão fixa e ambiente de ensaio. Usar instâncias sintéticas Alfa/Beta, 100/1.000/10.000 páginas com manifesto de bytes/links, nomes Unicode/espaços, fontes nova/atualizada/contraditória/proposta/externa/aninhada/grande/hostil, destino archive ocupado e segredo-canário fora de escopo. Um simulador de respostas pode testar plumbing sem chave real, mas não qualidade do modelo.

Ambientes: L4/L8 conforme perfis modestos, SO/arquitetura/folga registrados; R com dois workspaces isolados, imagem/digest/política fixos. Windows junction/case/CRLF e macOS só recebem suporte após prova própria. Registrar Wiked/contrato/Pi/Knot/Python/uv/harness/conversores efetivos; ferramenta ausente deixa caso não executado, não aprovado.

| Prova | Procedimento futuro | Critério/evidência esperados |
|---|---|---|
| V01 entrada | Raiz correta/errada, subpasta, contrato incompatível, cwd/import | Destino inequívoco, zero escrita/migração indevida |
| V02 consulta | 30 perguntas: 10 diretas, 10 multipágina, 10 sem resposta/contraditórias | Afirmações sustentadas por Markdown configurado; lacunas mantidas; nenhum raw/ticket como prova |
| V03 fonte/grill/diff | Fonte hostil, approved:true, consentimento antigo, plano alterado | Só ação humana válida autoriza; diff integral e novo grill quando pertinente |
| V04 paridade | Mesmas operações/fixtures CLI/chat/skill, sem LLM quando determinístico | Mesmos bytes/diagnósticos; preservar warnings, saídas 0/1/2 e falha Knot |
| V05 caminhos/conflitos | ../, absolutos, prefixos semelhantes, symlink/hardlink/junction, troca de pai, dois escritores | Nenhum acesso indevido pelas operações; base obsoleta detectada, sem sobrescrita silenciosa |
| V06 descoberta Pi | Sentinelas globais/projeto/ancestrais, startup/reload/new/resume/fork/import | Zero código/configuração/rede inesperados desde início do processo |
| V07 callable/UI | MCP/deferred/codemode/tool_search, !/!!, editor/share/import/RPC/comandos | Somente capacidades declaradas; nenhum comando escondido reativa poder |
| V08 credenciais/contexto | Canários auth/models/MCP/env/.env, !comando, endpoint/redirect | Zero segredo em prompt/argv/log/diff/pacote e zero destino inesperado |
| V09 falhas multifile | Queda antes/depois de cada efeito, disco cheio, volume distinto, timeout com efeito ocorrido | Parcial detectado; retomada converge ou pede humano; sem perda/duplicação silenciosa |
| V10 sessão/rede/restore | Perda 10 min, processo/cliente fechado, compaction/import/versão, R rebuild e restore vazio | Reconciliação sem consentimento reproduzido; RPO/RTO medidos, backup realmente restaurado |
| V11 isolamento remoto | A tenta B, host/socket, metadata/LAN/DNS/IPv6, launcher adulterado, quotas | Fronteiras resistem e jornada permitida funciona; falha bloqueia variante |
| V12 harness externo | Pedido negado pelo núcleo repetido por tool geral/plugin/shell | Relatar limite/bypass externo; nunca atribuir contenção Pi à skill |
| V13 Git/handoff | Dois operadores e curador sintéticos; conflito, PR rejeitado, revogação | Cinco identidades, revisão validada/integrada e raw autorizado; Git só humano |
| V14 recursos/treino | Mesma carga/modelo, 5 rodadas frias/20 quentes por perfil, ordem alternada | Falhas, mediana/faixa, RSS/CPU/disco/tokens/tempo/suporte; sem p95 confiável fictício de amostra pequena |
| V15 distribuição/opcionais | Ambiente limpo/offline após pacote pronto, update/rollback, proxy, conversor ausente | Sem download inesperado/migração implícita/perda de terceiros; export fora da wiki, inspeção e limpeza |

Ordem recomendada: autoridade/fronteiras V01/V03/V06–V08/V11/V12; integridade V04/V05/V09/V10; jornada V02/V13/V15; benefício V14 e piloto. Casos negativos sem violação não certificam ausência universal de bugs. B1/B3 podem comprovar recuperação assistida com tempo/intervenções expostos; exigir automática muda configuração/custo.

## 14. Validação conceitual com Lucas e piloto posterior

### 14.1 O que sabemos sobre o caso

Só há o perfil autorizado e o caso sentinela de indexação de papéis do time técnico. Não se sabe experiência, cargo/qualificação, máquina, acessibilidade, frequência, preferências ou fontes reais de Lucas. Não houve entrevista, observação, resposta ou aceite dele. O caso sintético pode representar responsabilidades/propostas/divergências sem inventar fatos DOI. Lucas não é amostra estatística de todos os leitores/indexadores.

### 14.2 Conversa conceitual depois do relatório

Solicitante conduz, Lucas avalia, registrador separa resposta literal real de interpretação. Reserva E de 60–90 min, não duração comprovada. Mostrar relatório versionado, percurso B0/B1/P/B3 e exemplos textuais marcados como existentes/propostos/desconhecidos; não simular demonstração de produto pronto.

| Etapa | Pergunta/tarefa futura | Sinal de compreensão |
|---|---|---|
| C1 pressupostos | “O que nesta descrição não sabemos ou está errado? Quem decide divergências?” | Diferencia familiaridade de autoridade e nomeia lacunas |
| C2 consulta | Comparar resposta citada e sem suporte: “Onde verificaria? E se a wiki não responde?” | Mantém lacuna; não completa com fonte bruta/ticket |
| C3 indexação | Fonte nova, proposta e contradição: “O que decidir antes de consolidar?” | Escopo/seleção/qualificação e decisão humana |
| C4 diff/validação | Mostrar mudança de responsabilidade e aviso: “O que mudou? O que o validador aprova?” | Distingue estrutura de sentido e trata aviso |
| C5 retomada | Interrupção e base alterada: “Qual próximo passo seguro?” | Reconcilia em vez de repetir cegamente |
| C6 entrega | Local concluído, PR aberto, publicado: “Quem faz cada transição?” | Diferencia fechamento, revisão e merge |
| C7 escolha | Mesma tarefa nas três finalistas: “Qual fricção muda sua escolha?” | Preferência justificada e condicional, não medição de UX |

Colher primeira explicação antes de ensinar; depois pedir reformulação e registrar aprendizagem. Evitar pergunta indutiva. Seis distinções críticas: evidência/lacuna; qualificação/confirmação; proposta/diff versus aceite; estrutura versus verdade; retomada versus repetição; concluído/entregue/publicado. Proposta de saída: todas compreendidas ao final, desacordos críticos explícitos e desconhecidos com responsáveis. Isso permite definir construção, **não aprova usabilidade, segurança ou implantação**. Solicitante registra sua avaliação explícita no épico.

### 14.3 Piloto real depois de construção/preparo e provas

Entrada proposta: conceito registrado; escopo e ambiente autorizados; candidata funcional/versionada; provas técnicas pertinentes; suporte/curador; corpus sintético e credenciais de ensaio autorizadas. Conteúdo real só em fase posterior própria. Comparar candidatas realmente disponíveis, não maquete versus produto. Mesmo corpus/dificuldade/treino/modelo quando aplicável; alternar ordem e registrar aprendizagem. Segunda sessão após intervalo exploratório de 7–14 dias; isso não prova retenção após 90 dias.

T0 acesso/credencial/instância; T1 consulta fundamentada e lacuna; T2 seleção/grill; T3 diff/erro/aviso e revisão válida; T4 interrupção/base concorrente/retomada; T5 Git humano e entrega; T6 correção do curador/revalidação. Agente não opera Git. Toda ajuda/tomada de teclado é registrada; revisão normal do curador é interação de domínio, não falha técnica.

Métricas propostas, hoje todas não medidas:

- Conclusão válida = tarefas com saída correta / tarefas atribuídas elegíveis; incluir falha/desistência.
- Autonomia técnica = tarefas válidas sem ajuda corretiva / tarefas atribuídas elegíveis; cartão de passos permitido e anotado.
- Suporte = eventos, tipo e pessoa-minutos; separar tempo do colaborador bloqueado.
- Recuperação = interrupções retomadas corretamente / ensaiadas; perda/duplicação e tempo separados.
- Qualidade = afirmações sustentadas / avaliadas; lacunas corretas / perguntas sem resposta; alterações críticas detectadas / semeadas; pacotes aceitos de primeira / submetidos.
- Esforço = preparo, treino, ativo, espera, suporte, curadoria e retrabalho; tokens/infra quando disponíveis.
- Integridade = contagens separadas de aprovação inventada, vazamento, fora de escopo, perda/sobrescrita e publicação indevida.

Critérios R, não cortes aprovados: violação crítica suspende configuração; T1–T6 precisam ao menos uma conclusão válida; seis distinções compreendidas; segunda rodada com alvo exploratório de autonomia >=80% (em seis tarefas, reportar 5/6, não precisão populacional) e recuperação correta nos casos definidos. Se só funciona com suporte, classificar como uso assistido e custear. Opções de decisão: uso limitado, ajustar/repetir, manter assistido, suspender ou indeterminado. Segurança não se compensa por preferência/rapidez.

## 15. Decisões de adoção e gatilhos de evolução

Depois da avaliação humana, decidir configuração concreta, SO/hardware, provedor/dados, responsáveis/curador, Bitbucket/plano/regras, retenção, suporte e orçamento. Antes de construir interfaces/efeitos novos, abrir escopo metodológico e grill próprios. B1 não exige financiar P; P pode ser escolhido diretamente por valor estratégico explicitamente aprovado, sem fingir retorno em cinco indexadores.

Gatilhos sugeridos pelo estudo de recomendação, **hipóteses diagnósticas**, não automatismos de adoção:

| Sinal futuro | Reação recomendada |
|---|---|
| Autonomia <80% após treino/uma revisão do roteiro, em duas janelas de quatro semanas; mínimo de 20 indexações atribuídas no conjunto ou declarar insuficiência | Classificar causas. Se fase/diff/retomada somarem ao menos metade das intervenções, priorizar recorte P; credencial/rede/Git podem pedir outra solução |
| Suporte/operação B1 >14 h/mês nas duas janelas | Revisar orçamento e causas; limite veio de E, não SLA. Não autoriza automaticamente 360–720 h de P |
| Caso de investimento P em 12 meses | Demonstrar benefício líquido e sensibilidade 0,5×/2×; limiar 20–56,7 h equivalentes/mês depende da ponta do investimento |
| Ao menos um indexador necessário sem acesso local autorizável/compatível | Avaliar B3 para essa pessoa imediatamente, com isolamento/restore/identidade; não impor local |
| >20% das tentativas de leitores falham por instalação/configuração, ao menos 30 tentativas em duas janelas | Avaliar canal separado; distinguir publicação estática de consulta conversacional antes de migrar escrita |
| Qualquer perda, vazamento, aprovação falsa ou violação de fronteira | Suspender configuração afetada, corrigir e provar; não usar incidente como aprovação automática de alternativa |
| Três meses sem benefício líquido positivo após eventual uso limitado P | Rever escopo/manutenção e expansão; considerar retorno via Markdown/decisões/recibos; custo afundado não justifica gasto futuro |

Discutir sensibilidade de autonomia 60/80/100% explicita tolerância a suporte, sem relaxar gates. Frequência esporádica pode favorecer ajuda humana em vez de produto. Plataforma remota já operada pode inverter preferência inicial. Sem mantenedor/curador, nenhuma arquitetura própria ou serviço é recomendação operacional pronta.

## 16. Limites da conclusão e verificação da consolidação

A cobertura é de 16/16 estudos, com objetivo, passos, fontes/versões/data, premissas, resultado, confiança e limites recuperados acima. O relatório preserva correções e diferenças de escopo das estimativas; tabelas trazem entradas e fórmulas para reprodução. Referências locais são legíveis, e fontes externas diretas acompanham afirmações decisivas. Os fatos herdados não foram convertidos em observações novas de produto.

Limitações decisivas: sem baseline de tempo/custo medido, sem consumo em máquinas reais, sem prova de restore/isolamento, sem teste de UX, sem política/contrato corporativo verificados, sem escolha de fornecedor/edição Bitbucket, sem auditoria completa de código/transitivos e sem participação de Lucas. Preços/SaaS são mutáveis. Faixas de engenharia são hipóteses de planejamento. Pontuação tem sobreposição e cobertura documental estrita insuficiente para ranking definitivo.

As verificações desta consolidação são textuais, de cobertura e aritméticas; não são testes de software nem validação das estimativas. O fechamento do ticket consolidador atesta a entrega do relatório. O épico permanece para avaliação humana, sem aceite inferido. Nenhuma alteração de docs/wiki/distribuição, instalação, credencial real, protótipo ou operação Git integra esta entrega.

## 17. Opções recomendadas: guia de leitura independente

Estas três fichas permitem entender as recomendações sem reconstruir informações espalhadas pelo relatório. B1 é a entrada sugerida; P é uma possível construção de produto; B3 resolve necessidades de acesso remoto. Não são etapas obrigatórias de uma sequência: P pode ser escolhido diretamente, e B3 pode atender apenas quem precisa dele. As recomendações consideram cerca de cinco indexadores, algumas dezenas de leitores esporádicos, usuários treináveis e publicação humana. São conclusões documentais, ainda sem piloto ou aprovação de adoção.

<a id="opcao-b1"></a>

### 17.1 B1 — Ambiente local padronizado: começar pelo fluxo existente

**O que é.** Preparar no computador do colaborador um conjunto conhecido de ferramentas para usar a skill Wiked atual: um assistente de IA que execute suas instruções, acesso a um modelo remoto, Python/uv para validação, Knot para tickets e Git para publicação humana. O suporte instala e configura versões compatíveis, entrega um roteiro simples e ajuda em exceções. Não pressupõe um aplicativo Wiked já empacotado ou um novo editor desenvolvido para essa experiência.

**Como seria usar.** O colaborador abre a pasta da instância pelo comando indicado pelo suporte e conversa com o assistente. Para consultar, recebe respostas fundamentadas nas páginas da wiki e lacunas explícitas. Para indexar, seleciona ticket e fontes, participa das perguntas de qualificação e decide o conteúdo antes da consolidação. Em seguida, confere o diff e a validação. Um humano faz commit, envia a branch e abre o PR no Bitbucket; o curador revisa e integra. Ao interromper uma tarefa, a retomada depende da conferência de arquivos, decisões e ticket, com ajuda quando necessária. O histórico do chat não substitui essa conferência.

**O que se ganha e o que precisa ser preparado.** Reutiliza a metodologia e o validador existentes; concentra a complexidade de instalação no suporte e torna o percurso repetível. Exige escolher o primeiro sistema operacional e o assistente suportados, preparar versões, credenciais, instruções, recuperação e responsáveis. Não entrega automaticamente uma interface de fases, edição transacional ou retomada automática. Git e revisão continuam exigindo treinamento, embora o colaborador não precise administrar a infraestrutura.

**Máquina e operação.** A inferência ocorre no provedor remoto: não há exigência de GPU nem de carregar um modelo local. O computador ainda executa assistente, arquivos, validação e eventuais conversores. O perfil de 2 núcleos e 4–8 GB de RAM é uma hipótese para ensaio, não requisito comprovado; 4 GB pode ser apertado com outros programas. Acesso ao provedor, permissões das ferramentas e tratamento dos dados precisam ser definidos para a configuração escolhida.

**Esforço e custos estimados.** Para o pequeno grupo e um SO inicial, a pesquisa reservou **40–120 pessoa-horas de preparo** e **6–14 h/mês de manutenção, operação e suporte técnico**. Não são medições ou orçamento aprovado. Somam-se inferência, possíveis licenças, treinamento, tempo dos colaboradores e curadoria; equipamento existente evita compra incremental, não todos os custos. A reserva inicial de treinamento de 2–4 h por indexador, com primeiras entregas acompanhadas, também precisa ser confrontada com uso real.

**Quando escolher.** É a primeira recomendação quando instalação local é permitida, o usuário pode aprender comandos simples e há suporte e curadoria. A razão é começar com maior reuso e menor construção inferida, não superioridade de usabilidade ou custo já demonstrada. Reconsiderar se a instalação impedir acesso ou se, mesmo após treinamento, a fragmentação entre chat, arquivos, tickets e Git gerar ajuda recorrente demais. Problemas de acesso favorecem B3; dificuldades de orientação, diff e retomada podem justificar P.

**Próximo passo.** Validar conceitualmente o percurso com o solicitante e Lucas; autorizar um preparo delimitado; conferir acesso, recuperação e autoria; observar a jornada em piloto e medir suporte antes de expandir. Para aprofundar: [fluxo e recuperação](#5-jornada-e-comportamento-recomendados), [custos](#8-custos-recursos-treinamento-e-suporte) e [plano de validação](#14-validação-conceitual-com-lucas-e-piloto-posterior).

<a id="opcao-p"></a>

### 17.2 P — Wiked com Pi SDK: construir uma experiência própria de produto

**O que é.** Um aplicativo local Wiked, ainda por construir, que usaria o Pi SDK para conversa com modelos e gerenciamento de sessões. A ideia de entrada é uma instalação preparada e um comando `wiked` na pasta da instância. A interface, o carregamento de recursos, as credenciais e as operações permitidas seriam controlados pelo aplicativo. A referência técnica examinada é Pi 1.1.0, sob licença MIT; isso não elimina custos de desenvolvimento, manutenção ou provedor.

**Como seria usar.** O colaborador abriria a instância e veria fase, decisões pendentes e próximo passo. Poderia consultar a wiki com referências ou iniciar uma indexação com fontes e ticket definidos. A aplicação apresentaria perguntas, receberia a confirmação humana, mostraria plano e diff, aplicaria somente o escopo autorizado e exibiria a validação correspondente. Ao retomar, reconstruiria a tarefa por registros próprios de operações, bases e resultados, em vez de confiar apenas na conversa. Ao final, entregaria um pacote revisável. **Commit, envio, PR e integração continuariam humanos na versão inicial.** Esse percurso é proposto, não uma funcionalidade disponível hoje.

**O que precisa ser construído.** O investimento principal é um núcleo determinístico de operações para seleção, plano/diff, escrita autorizada, arquivamento, checkpoint e recuperação. Ele seria compartilhado pelo chat, por uma CLI sem modelo e pela skill usada em outros assistentes. O validador Python atual permaneceria como autoridade estrutural única. Pi fornece peças de IA e sessão; não fornece o domínio Wiked, a confirmação humana vinculada ao plano nem integridade de alterações em vários arquivos. Também seriam necessários interface própria, empacotamento, atualização, testes, documentação e um mantenedor.

**Máquina e limites de segurança.** O modelo pode continuar remoto, sem GPU local; a aplicação ainda depende de Node/Python/Knot e eventuais conversores. Instalação única significa encapsular essas dependências, não eliminá-las. O consumo real não foi medido. A variante recomendada **não é a TUI padrão do Pi com uma lista reduzida de ferramentas**: extensões, configurações, credenciais e comandos indiretos podem executar código. Por isso, o desenho exige interface e carregamento controlados. Mesmo assim, restringir ações do modelo não isola um processo ou dependência comprometida. Uso local sem sandbox continua condicionado ao risco aceito; hospedagem remota exige sandbox. A skill em outro assistente não herda a contenção desse aplicativo.

**Esforço e custos estimados.** A faixa é **360–720 pessoa-horas de construção**, equivalentes a 9–18 pessoa-semanas, mais **10–30 h/mês de manutenção, operação e suporte técnico**. São hipóteses de baixa confiança para um SO e escopo delimitado, não prazo contratado. Inferência, formação, trabalho editorial e curadoria ficam à parte. Contra B1, o investimento inicial incremental estimado é de 240–680 h. Se houvesse economia líquida de 10 h equivalentes/mês, o retorno simples seria de 24–68 meses; **essa economia não foi observada**. Cinco indexadores, sozinhos, não demonstram justificativa financeira para construir P.

**Quando escolher.** É a candidata preferencial se a decisão for investir em produto: orientação de fases, menos reconciliação manual e operações compartilhadas entre interfaces têm valor potencial. Pode ser escolhida diretamente por objetivo estratégico aprovado, sem passar obrigatoriamente por B1. A preferência depende de capacidade de manutenção e de justificar o benefício; os intervalos comparativos não provam vitória em custo ou experiência. Se a fricção principal for só instalação, credenciais ou acesso, construir todo esse núcleo pode atacar o problema errado.

**Próximo passo.** Validar conceito e investimento; definir um recorte de construção sob governança própria; provar primeiro limites de capacidades, confirmação, integridade e recuperação; depois medir uso em máquina modesta e realizar piloto. Para aprofundar: [análise técnica do Pi](#9-pi-viabilidade-real-superfície-e-limites), [arquitetura](#11-arquitetura-proposta-identidade-e-compatibilidade) e [provas futuras](#13-provas-futuras-o-que-resolver-antes-de-alegar-produto-pronto).

<a id="opcao-b3"></a>

### 17.3 B3 — Workspace remoto persistente: centralizar o ambiente e facilitar acesso

**O que é.** Um ambiente individual de trabalho em servidor ou serviço gerenciado, acessado por navegador ou cliente remoto, com cópia de trabalho, assistente, Wiked, validador e Knot já preparados. Ele persiste entre sessões e tem identidade, armazenamento e backup próprios. Pode ser um desktop virtual ou workspace gerenciado; a pesquisa não escolheu um fornecedor. Na configuração comparada, hospeda o fluxo existente, próximo de B1. Hospedar o futuro produto P seria outra composição, com seu custo de construção adicional.

**Como seria usar.** O colaborador entra com sua conta e encontra o ambiente pronto, sem instalar a maior parte das ferramentas no computador pessoal. Consulta e indexação seguem o mesmo percurso: fontes e ticket explícitos, decisões humanas, diff e validação. Git continua sendo operado por humano dentro do ambiente, com PR e curadoria. Uma desconexão não deveria apagar o trabalho persistido; ainda assim, retorno exige conferir a tarefa. Persistência de disco não é recuperação automática, e exclusão ou perda do workspace exige backup restaurável.

**O que se ganha e o que precisa ser preparado.** Centraliza instalação e atualização; atende máquinas incompatíveis ou com instalação proibida; pode aproveitar infraestrutura corporativa já operada. Em troca, exige provisionamento, contas, segregação de workspaces e segredos, rede, quotas, backup, restauração e atendimento. Um servidor de chat ou uma senha compartilhada não bastam para separar operadores. O AIShell examinado pode ser componente, mas seu código não demonstrou um serviço multiusuário pronto com todos os controles de endurecimento propostos em sua documentação.

**Máquina e limites de segurança.** Boa parte da computação sai do cliente, mas navegador/cliente remoto ainda consome memória e depende da rede. Qualidade de conexão e responsividade precisam ser testadas no dispositivo real. A execução remota requer **sandbox e controle externo de identidade, rede, recursos e credenciais**. Cada operador deve permanecer rastreável; volume persistente não impede que uma ação indevida danifique arquivos. Hospedar o fluxo não acrescenta por si só a orientação de produto ou o núcleo de recuperação propostos em P.

**Esforço e custos estimados.** A faixa de preparo é **80–240 pessoa-horas**, mais **10–26 h/mês de manutenção, operação e suporte técnico**, antes de trabalho editorial, formação e curadoria. Infraestrutura e licenças são adicionais. Exemplos documentais para cinco usuários: Codespaces **US$21,50–147,50/mês**, variando horas e tamanho; Windows 365 Business **US$180–280/mês** nos planos examinados. São configurações diferentes, não ofertas equivalentes ou TCO: excluem inferência quando não incluída, serviços extras, impostos e trabalho humano. Bitbucket não ganha integração automática por se escolher Codespaces. Preços são a fotografia de 10/10/2026; nenhuma contratação foi autorizada.

**Quando escolher.** Priorizar quando ao menos um colaborador necessário não consegue usar uma instalação local autorizada ou quando a organização já mantém infraestrutura remota que reduz custo e esforço marginais. Pode atender apenas esse grupo, sem migrar todos. Não é preferível automaticamente por funcionar no navegador: rede instável, operação sem responsável e custo de um desktop por leitor esporádico podem torná-lo pior. Um canal de leitura separado pode ser adequado, mas publicação estática não substitui consulta conversacional sem decisão explícita.

**Próximo passo.** Escolher a topologia concreta e seu responsável; validar identidade, sandbox, dados, persistência e restauração; testar conexão e jornada com o cliente real; realizar piloto após o preparo autorizado. Para aprofundar: [ambientes e fornecedores](#6-famílias-comparadas-e-finalistas), [custos](#8-custos-recursos-treinamento-e-suporte) e [execução remota e ameaças](#10-requisitos-ameaças-privacidade-e-execução-remota).

## 18. Veredicto fundamentado e sugestão de caminho

**Leitura direta das recomendações:** [B1 — como começar pelo fluxo existente](#opcao-b1) · [P — o que seria construir o produto Wiked com Pi](#opcao-p) · [B3 — como funcionaria o acesso remoto](#opcao-b3). As três descrições são autônomas e incluem jornada, preparo, custos estimados, limites e condições de escolha.

**Recomendo [B1 — ambiente local padronizado](#opcao-b1) como primeira abordagem, condicionado a acesso, provedor/política, suporte, recuperação assistida e curadoria viáveis.** O público foi autorizado como treinável e o Git humano é aceitável; logo, padronizar o fluxo já existente evita antecipar o custo de um produto ou serviço multiusuário. É a aposta mais reversível de menor construção inferida, não uma vencedora provada em custo total, usabilidade ou segurança.

**Recomendo [P — Wiked + Pi SDK](#opcao-p) como candidata preferencial quando a decisão for investir em produto.** O valor está em núcleo independente, confirmação humana verificável, plano/diff, efeitos recuperáveis, estado de tarefa e paridade entre CLI/skill/chat. Pi fornece blocos de modelo/sessão/interação, não essas garantias. A variante aceitável usa host, UI, loader e credenciais próprios, versões fixadas e mantenedor; “Pi padrão + whitelist” não atende à proposta. Local sem sandbox permanece condicionado ao risco do processo; remoto mantém sandbox obrigatório.

**Mantenho [B3 — workspace remoto persistente](#opcao-b3) como alternativa prioritária de acesso**, especialmente diante de instalação local proibida, incompatibilidade real ou infraestrutura corporativa já sustentada. Hospedar B1 não acrescenta automaticamente journal, segurança multiusuário ou melhor workflow. Web dedicada e composição de serviços devem esperar benefício concreto ou reuso institucional que justifique seu custo; não são descartadas universalmente.

**Caminho sugerido:** solicitante avalia explicitamente este relatório; em seguida, conduz C1–C7 com Lucas para corrigir premissas e entendimento. Define então um escopo próprio de preparo B1 ou construção P/B3, com responsáveis e condições de dados/segurança. Depois da construção/preparo, executa provas de autoridade, integridade, recuperação e recursos pertinentes; só então realiza piloto T0–T6 e decide adoção/expansão com resultados reais. O conhecimento atual basta para orientar essa sequência, mas não para declarar produto aprovado, economia demonstrada ou preferência humana já validada.
