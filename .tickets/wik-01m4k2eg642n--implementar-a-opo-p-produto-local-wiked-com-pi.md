---
id: wik-01m4k2eg642n
title: 'Implementar a opção P: produto local Wiked com Pi SDK e núcleo determinístico compartilhado'
status: open
type: epic
priority: 3
mode: hitl
created: '2026-10-10T14:11:08.775081854Z'
updated: '2026-10-24T13:08:04.306400533Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- produto
- pi-sdk
- implementacao-futura
acceptance:
- title: Baseline publicado revalidado, investimento e recorte confirmados pelo responsável, Methodological grill explicitamente fechado e frentes materializadas em tickets com dependências coerentes
  done: false
- title: Núcleo determinístico e CLI sem LLM implementam seleção, plano/diff, autorização humana verificável, aplicação, validação única, archive e reconciliação Knot; interfaces e versões documentadas
  done: false
- title: Host/interface própria e adaptador Pi executam consulta e indexação com contexto e capacidades controlados desde startup, credenciais protegidas e confirmação não fabricável pelo modelo
  done: false
- title: Chat, CLI e skill compartilham operações e autoridade estrutural, com paridade provada e limites de contenção do harness externo explicitamente documentados
  done: false
- title: Journal independente do transcript, bases/recibos, concorrência e recuperação resistem às falhas previstas sem perda, duplicação ou sobrescrita silenciosa, incluindo efeitos incertos e archive com colisão
  done: false
- title: Entrega preserva evidência operacional, qualificação/grill e revisão humana, correlaciona diff e validação e mantém Git/PR/integração humanos com estados e responsabilidades distintos
  done: false
- title: Distribuição versionada no SO aprovado demonstra instalação limpa, compatibilidade, update/rollback humanos, preservação de terceiros, diagnóstico e backup/restore; não há segundo validador normativo
  done: false
- title: Matriz V01–V15 tem resultado e evidência por caso aplicável, não aplicáveis justificados, falhas críticas resolvidas e testes genéricos independentes da DOI; recursos e limites residuais medidos/documentados
  done: false
- title: Validação conceitual e piloto T0–T6 realizados no recorte autorizado, com critérios previamente acordados, denominadores, falhas, suporte, qualidade, recuperação e custos observados registrados
  done: false
- title: Documentação, treinamento, runbooks, responsáveis e política de dados/retenção entregues; mantenedor confirma aceite integrado e registra decisão de adoção separadamente do fechamento da implementação
  done: false
- title: Custódia no repositório autoral independente confirmada, relatório v1.1 preservado com caminho/hash e governança autoral autocontida; execução independe de tickets do consumidor ou notas de pesquisa
  done: false
deps:
- wik-01m4khsrmqya
- wik-01m2tpjtev7w
links:
- wik-01m5q09kvwzm
---

## Description

### Objetivo e resultado esperado

Implementar, quando houver decisão explícita de investimento e após a separação dos repositórios, a opção P descrita em `reports/investigacao-wiked.md`: um aplicativo local Wiked com interface própria, Pi SDK para conversa e sessões, e núcleo determinístico de operações compartilhado pelo chat, por uma CLI sem LLM e pela skill utilizada em outros assistentes. O produto deve orientar consulta e indexação, tornar visíveis fase/decisões/diff/validação, aplicar apenas mudanças autorizadas, recuperar efeitos interrompidos e entregar um pacote revisável. Commit, envio, abertura de PR e integração continuam humanos na versão inicial.

Este ticket registra uma intenção futura de implementação. Não registra aprovação de orçamento, adoção, segurança, preferência de usuários ou encerramento do Methodological grill. Deve permanecer em modo HITL até as decisões humanas pertinentes. O encerramento da investigação não autoriza construir automaticamente o produto.

### Contexto autossuficiente da decisão

A investigação comparou alternativas para aproximadamente cinco indexadores e algumas dezenas de leitores esporádicos, com usuários treináveis, computadores modestos e Git humano aceitável. A recomendação inicial foi B1: padronizar ambiente local, versões, credenciais, roteiro e suporte sobre a skill existente. P foi recomendada condicionalmente ao investimento em produto, pela possibilidade de reduzir dificuldades de orientação de fases, revisão e retomada. B3 é um workspace remoto persistente, alternativa para impedimentos de acesso local; não é parte de P por implicação.

Não houve vencedor quantitativo: intervalos de custos e pontuação se sobrepõem. Não houve construção, prova técnica, piloto ou medição de benefício na investigação. P pode ser escolhida diretamente por justificativa estratégica explícita, sem passar obrigatoriamente por B1. Se o problema observado for apenas instalação, credenciais, rede ou Git, confirmar se P realmente resolve a causa antes de financiar seu núcleo.

O produto não é um novo editor genérico nem a TUI padrão do Pi com uma lista reduzida de ferramentas. Pi oferece infraestrutura agêntica; não entrega as regras Wiked, confirmação humana ligada ao plano, integridade multifile ou recuperação de efeitos do domínio.

### Fonte documental e continuidade após a separação

A fonte suficiente para retomar este trabalho é o relatório integrado `reports/investigacao-wiked.md`, versão v1.1 da investigação. O executor futuro não deve precisar desta conversa nem das notas dos 17 filhos de pesquisa. Este ticket preserva os requisitos centrais e aponta os aprofundamentos:

- Seção 4: baseline, capacidades existentes e lacunas do produto.
- Seção 5: responsabilidades, jornada, estados e recuperação.
- Seção 8: custos, premissas e sensibilidade.
- Seção 9: Pi SDK, superfícies indiretas e núcleo compartilhado.
- Seção 10: requisitos P01–P32, ameaças T01–T13 e limites de segurança.
- Seção 11: arquitetura, estado, identidade, compatibilidade e decisões relacionadas.
- Seção 13: provas V01–V15, corpus e ambientes.
- Seção 14: validação conceitual C1–C7 e piloto T0–T6.
- Seção 15: decisão de investimento e gatilhos exploratórios.
- Seção 17.2, âncora `opcao-p`: ficha autônoma da opção P.

No momento da transferência para o repositório autoral Wiked, o mantenedor deve assegurar custódia de uma cópia integral identificável do relatório, registrar caminho definitivo, versão e hash e preservar suas referências. Se houver cópia no repositório consumidor, identificar qual é a referência congelada da decisão e evitar duas autoridades divergentes. Migrar este ticket e suas dependências autorais abertas preservando IDs; todos os pré-requisitos devem ser resolvíveis no tracker autoral independente. Não transferir wiki, raw ou governança operacional indiscriminadamente. Git e transferência/publicação permanecem humanos.

Relatório e ticket são material de pesquisa/governança, nunca evidência de fatos operacionais de uma wiki. As referências externas e APIs precisam ser reconferidas na versão efetivamente escolhida; valores e inventários do relatório são snapshots, não promessas de compatibilidade futura.

### Condição de entrada e autoridade

Antes da execução, o mantenedor deve confirmar custódia no repositório autoral independente e disponibilidade de baseline publicado verificável e instalador/atualizador aprovado. As dependências nativas agora apontam os trabalhos futuros de publicação e instalador deste mesmo tracker. A preparação local da árvore não comprova transferência, release nem instalação real. Um piloto em consumidor real exige autorização e verificação próprias, sem dependência de ticket externo. O novo produto deve ser desenvolvido na origem autoral Wiked.

Antes de alterar código ou conteúdo metodológico governado: ler as instruções vigentes da origem, recuperar o relatório, revalidar o baseline publicado, abrir e fechar explicitamente o Methodological grill com o solicitante responsável. A implementação deve respeitar exatamente o escopo confirmado. Criar este ticket não fecha esse grill. Registrar divergências entre o relatório histórico e a distribuição atual antes de consolidar decisões.

Decisões de entrada: justificativa do investimento; mantenedor e responsável pelo aceite; público e jornadas prioritárias; primeiro SO/arquitetura e perfil de hardware; formato da interface própria; Pi/Node/Python/uv/Knot suportados; provedor/modelo/endpoints e dados autorizados; armazenamento de segredos; identidade e confirmação humana; localização e ciclo de vida do journal; retenção, backup e restauração; orçamento; suporte/curadoria; opcionais incluídos e critérios de piloto. Não inferir essas decisões da pesquisa.

### Escopo funcional inicial

1. Abrir explicitamente uma instância e conferir raiz, contrato e compatibilidade. Instância errada ou contrato ausente/incompatível interrompem a operação, sem setup ou migração implícitos.
2. Consultar por navegação progressiva de contexto, índices e links, com busca textual subsidiária. Respostas apresentam páginas de suporte e lacunas. Apenas Markdown operacional configurado sustenta fatos: raw/archive, tickets, contratos YAML, instruções e URLs externas não completam evidência. Consultar não inicia escrita.
3. Preparar indexação com ticket, objetivo, critérios, páginas e fontes explicitamente selecionados. Ler o consolidado aplicável antes da fonte. Registrar fingerprints; não varrer raw inteiro por conveniência.
4. Orientar qualificação e grill: explicitar decisões pendentes, separar fatos/propostas/divergências e receber confirmação humana vinculada ao objetivo e ao plano. Login, cargo, assignee ou resposta do modelo não comprovam qualificação. Nova decisão substantiva reabre a qualificação aplicável. Preservar exceções estreitas vigentes de registros durante grill, sem criar permissão genérica nem proibição global incompatível com a metodologia.
5. Preparar e mostrar plano e diff integral, incluindo páginas, índices, proveniência, referências, novos/excluídos, derivados e movimentos. Resumo não substitui diff. Mudança de base ou de plano invalida autorização/revisão correspondente e exige nova avaliação.
6. Aplicar operações tipadas somente dentro do escopo autorizado, com detecção de concorrência e recuperação documentada. O modelo propõe; confirmação e verificação de autoridade pertencem ao host/núcleo, fora do texto do modelo.
7. Executar o validador oficial na revisão efetivamente entregue. Erros bloqueiam; avisos exigem disposição humana registrada. Validação estrutural não atesta verdade ou aprovação semântica. Alterações posteriores invalidam a evidência técnica pertinente.
8. Arquivar apenas as fontes locais selecionadas, após validação, sem colisão e com integridade comprovada; fonte externa permanece externa. A decisão de persistir raw/archive em Git é humana.
9. Reconciliar operações com Knot por sua CLI e preparar entrega com instância/ticket, fontes, decisões, base/diff, versões, validação, avisos, autoria, pendências e próximo responsável.
10. Pausar, cancelar e retomar sem depender do transcript. Cancelar impede novos efeitos, mas não desfaz automaticamente os já realizados. Distinguir alteração de conteúdo, validade estrutural, estado do ticket e publicação; ticket fechado não significa PR integrado.

### Arquitetura-alvo e fronteiras

Fluxo proposto: pessoa ↔ UI/host Wiked ↔ adaptador Pi ↔ provedor autorizado; UI/host, CLI determinística e skill externa usam o mesmo núcleo de operações. O núcleo se integra com arquivos/journal, runtime Python oficial, Knot CLI e opcionais explicitamente habilitados. O pacote de entrega segue para Git/PR humanos e curador.

- Núcleo de domínio: seleção/escopo, plano/diff, bases, autorização verificável, efeitos, recibos e reconciliação. Deve esconder a sequência de lock, escrita e recuperação, sem obrigar cada frontend a reinventá-la. Não acoplar o domínio a tipos Pi.
- CLI: operações determinísticas de leitura, planejamento, inspeção, validação, aplicação autorizada e reconciliação funcionam sem modelo ou chave de IA. `wiked` é nome de comando proposto, sujeito à decisão de interface; comandos e envelopes ainda devem ser especificados.
- Adaptador Pi: traduz contexto e ferramentas para as operações de domínio. Síntese e apuração semântica continuam agênticas; o núcleo não se torna árbitro da verdade.
- Host/UI própria: exibe fase, pendências, ações possíveis, diff, diagnósticos e consequências; recebe confirmação humana por canal que o modelo não possa fabricar. Um argumento `approved:true` não é autorização.
- Runtime: reutilizar o validador Python como autoridade estrutural única, preservando seus diagnósticos e códigos de saída; não reimplementar regras em TypeScript por conveniência. No snapshot do relatório, saídas são 0/1/2 e o JSON não tem schema_version: inspecionar o contrato atual antes de definir o adaptador.
- Knot: usar sua CLI/protocolo efetivo; não manipular arquivos internos do tracker. Em resultado incerto, consultar a autoridade antes de repetir.
- Skill: consumir as mesmas operações, sem duplicar regras. Ferramentas gerais de outro harness podem contornar o núcleo; a skill externa não herda a contenção do aplicativo.
- Distribuição: estender os mecanismos publicados na separação, preservando manifesto, ownership, integridade, compatibilidade, atualização humana e rollback. Instalação única encapsula dependências, não elimina Node/Python/uv/Knot.

Especificar interfaces versionadas e resultados distinguindo concluído, pendente, incerto, incompatível, negado e parcial. Registrar separadamente versões de app/protocolo/checkpoint, metodologia/contrato/schema, runtime, Knot, Pi/Node, Python/libs e conversores. Não alterar o contrato da instância para adicionar identidade ou estados sem decisão metodológica própria.

### Persistência, concorrência e recuperação

Manter journal fora da wiki e dos diretórios governados, separado de conversa e segredos, ligado à instância e ao workspace. Não usar somente caminho absoluto como identidade: restauração pode mudar caminho e cópia não pode herdar consentimento. Definir migração de checkpoint e comportamento para versões incompatíveis.

Checkpoint mínimo: raiz/versões/política, ator e qualificação por sessão/objetivo, ticket, fontes/fingerprints, decisões abertas/confirmadas, plano/diff/bases/resultados, operações/recibos, validação/avisos e próximo responsável. Histórico Pi é auxiliar; compaction, fork, import ou retomada não reproduzem aprovação humana. Logs locais não são invioláveis perante o dono do processo.

Sequência de referência a detalhar e provar: candidato/diff e journal durável; conferência de confirmação/base; lock cooperativo; rechecagem imediatamente antes do efeito; staging/substituições controladas; validação dos bytes finais; archive selecionado; reconciliação Knot; entrega. Um escritor por workspace não impede conflito entre cópias distintas. Hashes e múltiplos renames não criam transação distribuída entre páginas, índices, Knot, archive e PR.

Após queda, classificar cada objeto como base, resultado esperado ou terceira versão. Base permite avaliar efeito faltante ainda autorizado; resultado evita repetição; terceira versão exige intervenção ou novo plano. Proibir rollback cego e sobrescrita silenciosa. Tratar disco cheio, travamento, timeout com efeito ocorrido, mudança externa de fonte, destino archive ocupado e perda total de workspace. Backup e restore são distintos de sessão salva e checkpoint.

### Controle de capacidades, dados e limites

A referência histórica do Pi foi 1.1.0, licença MIT; auditar a versão fixada na implementação. Whitelist de tools não é confinamento. Construir loader, catálogo de capacidades, credenciais e UI controlados desde o início do processo: não carregar configuração, pacotes, extensões, hooks ou MCP de origens globais/projeto/ancestrais e só depois tentar filtrá-los. Permitir explicitamente o contexto canônico necessário à rota Wiked, sem autoload arbitrário.

Não expor por padrão built-ins de shell/escrita livre, TUI/RPC integral, !/!!, editor externo, comandos de import/share/reload ou mecanismos indiretos como deferred tools, codemode, tool_search e execução de tools por outras tools. Cada capacidade necessária deve ter justificativa e prova incluindo startup, nova sessão e retomada. Controlar subprocessos e argumentos, paths reais, traversal, symlinks/hardlinks/junctions e rechecagens de uso; testar renderização de conteúdo hostil na interface escolhida.

Segredos ficam fora de prompt, argv, logs, diff, journal e pacote. Não executar comandos embutidos em auth/models/MCP para obter chaves. Provedor/modelo/destinos de rede são explícitos, sem fallback silencioso. Ler um arquivo local não autoriza enviá-lo ao provedor. Definir minimização, quotas de custo/tokens/tempo, cancelamento, telemetria e retenção por classe; incluir chamadas automáticas e não apenas prompts manuais. Logout não equivale a revogação no provedor.

A variante inicial é local com processo/dependências confiáveis e limites residuais declarados. Restringir o modelo não isola código comprometido nem o proprietário local. Hospedagem remota/multiusuário fica fora do recorte inicial; incluí-la exige novo escopo com sandbox, isolamento, rede, identidade, quotas e provas próprias. Não atribuir garantias de isolamento por marca de SDK ou contêiner.

### Plano de execução futuro e decomposição

As frentes abaixo são uma decomposição proposta, não filhos já criados nem APIs aprovadas. Ao ativar o trabalho, materializar tickets com critérios e dependências após o grill. Como dependência do pai não deve ser presumida como herdada, a primeira frente executável deve depender explicitamente da publicação e do instalador autorais; frentes seguintes devem depender dos marcos que realmente consomem. O épico é portão de aceite integrado, não bloqueador circular dos filhos.

1. Rebaseline e decisão de produto: custódia do relatório, versões publicadas, validação conceitual, investimento, recorte e grill fechado. Saída: decisões, exclusões, responsáveis e critérios mensuráveis aprovados.
2. Contratos e desenho do núcleo: modelo de tarefa, identidades, autorização, envelopes, planos/bases, journal, falhas e matriz de compatibilidade. Saída: interfaces e fixtures de referência revisadas, sem segunda autoridade estrutural.
3. Núcleo, adaptadores e CLI: leitura/seleção/plano/diff, aplicação, runtime, Knot, archive, recibos e recuperação. Saída: percurso determinístico sem LLM e falhas injetadas cobertas.
4. Host Pi controlado: loader, sessões, credenciais, contexto mínimo, tools tipadas e interface de confirmação. Saída: provas de descoberta/callable/dados antes de alegar restrição de capacidades.
5. Experiência integrada e skill: consulta, indexação, fases, revisão, avisos, retomada, entrega e paridade entre entradas. Saída: mesma autoridade para operações equivalentes e limites do harness externo documentados.
6. Distribuição e operação: empacotamento no primeiro SO, instalação/update/rollback humanos, versões fixas, opcionais, diagnóstico, retenção, backup/restore e runbooks. Saída: instalação limpa reproduzível e recuperação operacional comprovada.
7. Qualificação técnica: executar matriz V01–V15 aplicável, corrigir falhas e produzir evidências versionadas. Saída: candidata funcional apta ao piloto, sem contar casos ausentes como aprovados.
8. Piloto e aceite integrado: treinamento, tarefas T0–T6, métricas, limitações, custo observado e decisão humana sobre uso limitado/ajuste/suspensão/expansão. Saída: entrega aceita e decisão de adoção explicitamente distinta do fechamento documental.

Podem existir trabalhos paralelos após os contratos comuns, mas a prova integrada precisa usar a mesma candidata/revisão. Não delegar decisões de domínio ou aprovação de investimento ao agente por conveniência de paralelismo.

### Estratégia de prova e evidência

Usar instâncias sintéticas independentes da DOI, Alfa/Beta, com manifestos verificáveis; corpus de 100/1.000/10.000 páginas conforme recorte aprovado; nomes Unicode/espaços, fontes contraditórias/hostis/externas, fontes alteradas, archive ocupado e segredos-canário fora de escopo. Simulador de respostas serve à integração determinística, não comprova qualidade de consulta com modelo real. Registrar versões, SO/hardware, dados, configuração, comandos, resultado esperado/observado, falhas e artefatos reproduzíveis.

Cobertura exigida, detalhada na seção 13 do relatório:

- V01: raiz, subpastas, contrato e compatibilidade; zero efeito indevido.
- V02: consulta direta, multipágina e sem resposta/contraditória; citações e lacunas corretas (referência: 30 perguntas distribuídas em três grupos de dez).
- V03: fonte hostil, confirmação forjada/antiga e plano alterado; autorização humana válida e diff integral.
- V04: paridade de bytes/diagnósticos e recusas em CLI/chat/skill; operação determinística sem chave.
- V05: escapes de caminho, links, troca de pai e dois escritores; base obsoleta bloqueada sem sobrescrita silenciosa.
- V06–V08: sentinelas de descoberta desde startup, capacidades indiretas/UI e canários de credenciais/contexto/rede; ausência de execução, segredo ou destino inesperados.
- V09: queda antes/depois dos efeitos, disco cheio, volumes distintos e timeout; parcial detectado e reconciliação sem perda/duplicação silenciosa.
- V10: perda de rede/processo, retomada/compaction/import e restauração sem transcript; RPO/RTO efetivamente medidos.
- V11: isolamento remoto somente se essa variante for formalmente incluída; para o produto local, registrar não aplicável com justificativa, nunca aprovado sem execução.
- V12: limites de harness externo explicitamente demonstrados, sem prometer contenção herdada.
- V13: handoff com operadores/curador de ensaio, conflito, rejeição e correção; Git humano, revisão correta e atribuição identificada.
- V14: recursos, latência, tokens, falhas, suporte e treinamento em máquina modesta; referência de cinco rodadas frias e vinte quentes, medianas/faixas sem p95 fictício.
- V15: instalação limpa, uso determinístico offline com pacote pronto, update/rollback, proxy e opcionais ausentes; sem download inesperado, migração implícita ou perda de arquivos de terceiros.

Priorizar autoridade/fronteiras, depois integridade, depois jornada/distribuição e por fim benefício. Falha crítica impede considerar a configuração apta. Não substituir prova de efeito por mock que apenas repete a implementação. Testes genéricos devem rodar sem o repositório DOI; integração consumidora é adicional. Seguir os comandos de validação da origem vigente; Python via `uv run`.

### Validação conceitual, piloto e adoção

Antes da construção, retomar C1–C7 com o solicitante e Lucas, caso continue sendo o participante adequado: pressupostos e autoridade; evidência/lacunas; seleção/grill; diff/estrutura versus sentido; recuperação; entrega/publicação; preferência justificada. A investigação não colheu respostas nem demonstrou qualificação, máquina ou preferência de Lucas. Registrar respostas reais separadas de interpretação e replanejar se o perfil mudou.

Piloto ocorre após candidata versionada e provas pertinentes, com suporte e curador designados. T0 acesso/credencial/instância; T1 consulta/lacuna; T2 seleção/grill; T3 diff/erro/aviso; T4 interrupção/base concorrente/retomada; T5 Git humano/handoff; T6 correção/revalidação. Iniciar com corpus sintético; dados reais exigem autorização própria. Prever segunda sessão para observar retenção do aprendizado; o relatório sugere 7–14 dias, sem tornar isso requisito já aprovado.

Medir tarefas válidas sobre atribuídas, autonomia sem ajuda corretiva, eventos e pessoa-minutos de suporte, recuperação correta e perda/duplicação, qualidade de citações/lacunas/revisão, aceite de pacotes, preparo/treino/tempo ativo/espera/curadoria/retrabalho, tokens e custo. Incluir falha/desistência e denominadores; registrar ajuda e tomada de teclado. Revisão normal do curador não é falha técnica. Alvo de autonomia de 80% e outros limiares do relatório são exploratórios, a confirmar antes do ensaio; não os apresentar como resultados ou SLA. Violação crítica não é compensada por velocidade ou preferência.

### Custos e incertezas a reestimar

Estimativa histórica de baixa confiança: 360–720 pessoa-horas (9–18 pessoa-semanas) para um SO e escopo delimitado; 10–30 h/mês de manutenção/operação/suporte técnico. Decomposição indicativa: núcleo/estado 3–6 semanas; SDK/UI 2–4; distribuição/endurecimento/provas 3–6; documentação/treino 1–2. Não é prazo contratado, orçamento aprovado ou capacidade medida; pode haver sobreposição com entregas da separação e deve ser retirada na reestimativa.

Inferência, licenças aplicáveis, treinamento dos usuários, trabalho editorial, curadoria e expansão de escopo são parcelas próprias. Incremento estimado contra B1: 240–680 horas; com economia hipotética líquida de dez horas equivalentes/mês, retorno simples de 24–68 meses, economia nunca observada. Cinco indexadores não justificam automaticamente o investimento. Reestimar após decisões e comparar custos observados no piloto, sem alegar retorno com valores brutos ou custos duplicados.

### Exclusões e decisões laterais

Ficam fora da versão inicial: Git/PR/merge automáticos; serviço remoto multiusuário; novo mecanismo de busca semântica/RAG obrigatório; reescrita do validador; editor genérico; suporte universal a SOs; reorganização automática da wiki; inferência de qualificação humana; substituição das regras Wiked pelo chat. Diagramas/exportações são opcionais cujo recorte e dependências devem ser aprovados; não reconstruir motores existentes.

Antes de implementar o comportamento afetado, verificar na distribuição vigente como ficaram as decisões relacionadas do relatório: capacidades opcionais (`wik-01m2tpkz9x55`), projeção semântica (`wik-01m17qfp6n6c`), autorização de diagramas (`wik-01m310mknyjs`), registros de termos durante grill (`wik-01m310mkwb5f`) e contexto canônico por rota (`wik-01m310mm3e55`). Esses IDs são pistas históricas, não pré-requisitos adicionais implícitos nem fontes necessárias para compreender este ticket. Se não estiverem disponíveis, comparar o comportamento publicado e levar qualquer ambiguidade ao grill; não inventar resolução. As dependências bloqueantes são a primeira publicação e o instalador autorais, conforme os campos nativos; decisões laterais não se tornam dependências implícitas.

### Entrega final e aceite humano

Entregar código/testes genéricos, artefato versionado e verificável na origem Wiked, integração com a distribuição, guia de usuário, treinamento, documentação de interfaces/compatibilidade, runbooks de instalação/update/rollback/recuperação/incidente, matriz de provas, resultados do piloto e limitações residuais. Manter instruções/código genéricos livres de conhecimento DOI e no idioma exigido pela origem; artefatos dirigidos ao solicitante em pt-BR.

O mantenedor revisa o conjunto e registra aceite explícito. Encerrar filhos ou passar testes não aprova adoção automaticamente. Registrar separadamente entrega do produto e decisão de uso/expansão. Se o investimento for abandonado, encerrar como cancelamento conforme o tracker, com motivo explícito, sem marcar requisitos não realizados como satisfeitos.

### Custódia preparada em 2026-10-10

Relatório integral no caminho autoral `reports/investigacao-wiked.md`, v1.1; SHA-256 `272b49fdd54426533aeecef9bcb0a9f814e08476a07f947f73f78d7b119e418d`. A árvore local preparada contém essa cópia; a transferência humana ao repositório independente ainda deve ser confirmada. `reports/README.md` documenta os limites das referências históricas.

## Notes

**2026-10-10T18:40:31.148539898Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-24T13:07:59.337282337Z**

Reorganização autorizada do backlog em 2026-10-24: o épico wik-01m5q079q8jz e a CLI/protocolo de recuperação wik-01m5q09kvwzm são trabalhos independentes deste produto. Ao especificar seleção e consulta do núcleo, avaliar reutilização da API/CLI de recuperação aprovada, evitando segunda lógica de navegação. A nova frente não implementa operações de escrita, autorização, journal ou host Pi deste produto, não exige investimento no aplicativo e não torna RAG obrigatório. Relação informativa, sem nova dependência bloqueante ou alteração de prioridade/aceite deste épico.
