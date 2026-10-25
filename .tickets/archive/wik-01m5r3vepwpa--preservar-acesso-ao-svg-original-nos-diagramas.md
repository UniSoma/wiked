---
id: wik-01m5r3vepwpa
title: Preservar acesso ao SVG original nos diagramas navegáveis do Docsify
status: closed
type: bug
priority: 2
mode: hitl
created: '2026-10-24T23:27:36.156337080Z'
updated: '2026-10-25T00:05:46.680899345Z'
closed: '2026-10-25T00:05:46.680899345Z'
tags:
- metodologia
- wiked
- docsify
- diagramas
acceptance:
- title: Methodological grill encerrado com confirmação explícita do solicitante sobre objetivo, escopo, decisões, exceções e critérios antes de editar conteúdo governado.
  done: true
- title: Cada diagrama aprimorado exibe um link nativo para seu SVG original correto, sem target que force nova guia; o link acompanha a visibilidade original da imagem e não interfere nos links entre nós e descrições.
  done: true
- title: Exemplo distribuído mantém texto genérico em inglês e guia específico exige adaptação ao idioma da instância durante adoção; não há requisito novo de contrato nem duplicação de regras em guias não relacionados.
  done: true
- title: Testes sintéticos verificam destino correto, múltiplos diagramas, imagens originalmente ocultas, ausência de duplicação após reconstrução e preservação do fallback em falhas ou respostas obsoletas.
  done: true
- title: Aceitação em navegador verifica caminhos aninhados, acesso por teclado, abertura independente do SVG, zoom disponível no navegador e preservação da navegação interativa após saída, retorno e recarga; versões, resultados e casos não executados ficam registrados.
  done: true
- title: Executar uv run pytest para alterações de testes ou runtime e verificações textuais pertinentes; registrar evidências e limites no ticket, sem usar testes de prosa como prova de conformidade metodológica nem atualizar automaticamente viewers consumidores.
  done: true
---

## Description

Uma wiki que adotou diagramas navegáveis relatou perder no Chrome a opção habitual de abrir a imagem em outra guia. Os fluxos são grandes e a visualização independente do SVG permite examiná-los com zoom; ampliar a página descritiva não atende à necessidade. No adaptador distribuído, o img original é ocultado após a inserção do SVG interativo em shadow root.

A revisão metodológica recomendou incorporar um link visível para o SVG original como comportamento padrão da integração opcional, preservando a navegação entre nós e descrições. A proposta local cria um a com data-wiked-diagram-open, href apontando para a URL validada do SVG e texto localizado, e inclui esses links na limpeza das renderizações seguintes. A proposta foi avaliada por inspeção, sem teste no navegador.

Este ticket registra implementação futura solicitada pelo usuário, não fechamento do Methodological grill. Antes de alterar conteúdo governado, cumprir o fluxo autoral e obter confirmação explícita do entendimento compartilhado. A integração continua opcional e sua atualização em consumidores exige autorização própria; não sincronizar viewers existentes.

## Design

Escopo inicial: distr/agents/skills/wiked/viewers/index.html, distr/agents/skills/wiked/guides/docsify.md e testes sintéticos pertinentes em tests/js/ e tests/test_wiked_docsify*. Preservar divulgação progressiva, concentrando a regra no guia específico.

Adicionar link HTML nativo junto de cada diagrama aprimorado com sucesso, usando a URL same-origin já validada do SVG e sem forçar outra guia. O texto genérico distribuído deve estar em inglês (sugestão: Open original diagram), com orientação explícita para adaptá-lo ao idioma da instância na adoção (pt-BR: Abrir diagrama original). Ícone de lupa não é necessário. Acompanhar a visibilidade original da imagem, remover links gerados ao reconstruir a integração e preservar o fallback estático em falhas.

Não alterar Markdown, D2, SVG, contrato da instância ou layout do diagrama. Não implementar zoom embutido, instalar ferramentas, publicar versões ou editar uma wiki consumidora. O acesso direto ao arquivo não deve ser descrito como navegação interativa nem como garantia universal de zoom do navegador. Preservar as restrições de confiança dos SVGs locais revisados e não enfraquecer verificações existentes.

## Notes

**2026-10-24T23:57:39.911105326Z**

Methodological grill encerrado: solicitante confirmou explicitamente o resumo nesta sessão. Objetivo: acesso nativo ao SVG original após enhancement bem-sucedido, URL validada, sem target forçando nova guia, visibilidade original, cleanup e fallback preservados. Escopo: exemplo HTML e guia Docsify distribuídos e testes sintéticos pertinentes. Texto genérico em inglês, adaptação ao idioma na adoção. Validar suíte uv run pytest e navegador sintético, registrando versões e limitações. Excluídos consumidores, contrato, Markdown/D2/SVG, zoom embutido, instalação de ferramentas, publicação e Git. Sem pendências laterais necessárias.

**2026-10-25T00:03:43.999968669Z**

Implementação: link HTML nativo data-wiked-diagram-open dentro do shadow root de cada host, href igual à URL same-origin já validada e sem fragmento, sem target/listeners próprios. Compartilha ocultação e cleanup do host. Guia específico exige localização na adoção e esclarece SVG estático, zoom variável e confiança no recurso bruto requisitado novamente. Nenhum consumidor, contrato, SVG/D2 ou guia não relacionado alterado. Validação: node --test tests/js/docsify-diagrams.test.cjs: 16/16 passaram (URLs aninhadas/query, múltiplos diagramas, hidden, reconstrução, falhas, respostas obsoletas e imagens sem opt-in). WIKED_BROWSER_TESTS=1 uv run pytest -s tests/test_wiked_docsify.py::test_docsify_browser_integration --basetemp=/tmp/opencode/wik-svg-browser-5: 1 passou, Chromium 153.0.8010.12, Docsify 4.13.1, playwright-cli 0.1.19; compatibilidade D2 instalada v0.7.1. Navegador verificou Tab/Enter, abertura na mesma guia, abertura em guia independente por botão do meio, URLs distintas/aninhadas, ocultação original, navegação e retorno, recarga sem duplicação, fallback inseguro e respostas atrasadas, e ausência de dependência da skill. Zoom no SVG independente verificado por visualViewport.scale=2 via CDP Emulation.setPageScaleFactor; menus/atalhos de zoom da interface do navegador, outros engines e deployments consumidores NÃO executados, sem alegar cobertura desses casos. Ajustes no harness durante execução: URL calculada no contexto do navegador, evento de nova página no BrowserContext para botão do meio e src absoluto no fixture HTML oculto. Verificação textual de links reais do guia passou após excluir blocos ilustrativos; revisão semântica preservou inglês genérico, divulgação progressiva, propriedade manifestada e autoridade local. Primeira suíte completa atingiu timeout externo de 120s sem falha reportada; reexecução com limite 600s em andamento. Sem instalação, publicação ou manipulação de Git.

**2026-10-25T00:05:39.747731727Z**

Validação completa concluída: uv run pytest --basetemp=/tmp/opencode/wik-svg-pytest: 221 passed, 2 skipped em 294.10s. Os testes opcionais omitidos na suíte padrão não substituem o browser opt-in executado separadamente e aprovado, conforme evidência anterior. Sem falhas; critérios técnicos e limites de aceitação registrados.

**2026-10-25T00:05:46.680899345Z**

Preservado acesso ao SVG original por link nativo no exemplo Docsify, sem forçar nova guia e com visibilidade, limpeza, fallback e navegação preservados. Guia de adoção e testes atualizados. Suíte: 221 passaram, 2 omitidos; 16 testes JS e aceitação Chromium aprovados. Zoom via viewport validado; menus/atalhos e outros navegadores não testados. Nenhum consumidor atualizado.
