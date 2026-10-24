---
id: wik-01m5qx0wbcbd
title: Distribuir exemplo Docsify independente da skill com adaptador inline
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-24T21:28:13.932227879Z'
updated: '2026-10-24T21:51:26.148070573Z'
closed: '2026-10-24T21:51:26.148070573Z'
acceptance:
- title: Exemplo index.html manifestado contém configuração Docsify e adaptador inline canônico; JS distribuído separado removido
  done: true
- title: Guia, manutenção e changelog orientam adoção consumer-owned independente da skill e atualizações autorizadas
  done: true
- title: Testes exercitam implementação extraída do exemplo e visualizador copiado sem skill; suíte e checks técnicos registrados
  done: true
---

## Description

Aprovado pelo solicitante: substituir o adaptador JS separado por exemplo completo de index.html com implementação inline única. A adoção copia/adapta o HTML ao repositório consumidor sem sobrescrever visualizador existente; não pode depender de .agents ou da skill instalada. Atualizações futuras explícitas e autorizadas. Grill metodológico encerrado por confirmação de Q1 e Q2/Q3; escopo guia, manutenção, changelog 1.6.0, manifesto, exemplo e testes. Sem consumidores reais, Git, instalação ou publicação.

## Notes

**2026-10-24T21:30:04.542802913Z**

Implementado no escopo confirmado: exemplo canônico viewers/index.html com configuração, CSS/Docsify 4.13.1 fixados e adaptador inline; removido JS distribuído separado e ajustado manifesto. Guia distingue exemplo Wiked de viewer consumer-owned, proíbe skill como entrada de build/serviço (incluindo links/symlinks), preserva visualizador existente, exige atualizações propostas/autorizadas e independência após remoção/atualização da skill. Manutenção/changelog 1.6.0 alinhados. Testes Node/D2 extraem única implementação HTML; fixture de navegador copia/adapta HTML real para raiz sintética sem .agents; cenário sem adaptador remove bloco inline. WIKED_BROWSER_TESTS=1 uv run pytest tests/test_wiked_docsify.py::test_docsify_browser_integration: 1 passed em 13.51s. Checks Node de manifesto/versão, links/fragmentos, ASCII, whitespace e ordem/sintaxe de scripts passaram. Primeira suíte --maxfail=1: 20 passed e falha de pré-requisito ambiental no teste offline por PyYAML ausente do cache uv; nenhuma alteração no teste offline. Suíte completa sem parada antecipada em execução. Não houve instalação de ferramentas, Git, publicação ou alteração de consumidores reais.

**2026-10-24T21:33:35.510791533Z**

Suíte completa final concluída: uv run pytest => 220 passed, 2 skipped, 1 failed (213.48s). Única falha: test_documented_offline_invocation_ignores_consumer_python_project, resolução --offline sem PyYAML no cache uv. Não é evidência de suíte verde; erro bloqueia aceitação final. Teste de navegador específico já passou com HTML inline adotado sem skill (1 passed). Não alterado teste offline ou instalado tooling para contornar ambiente. Solicitante está fazendo checagem manual da fixture /tmp/pytest-of-developer/pytest-1/test_docsify_browser_integrati0; preservar esse diretório durante a revisão, evitando novas execuções pytest que possam limpá-lo.

**2026-10-24T21:47:26.484640222Z**

Solicitante autorizou explicitamente a execução dos comandos necessários à evolução do Wiked, esclarecendo que considera legada a restrição discutida sobre instalação. Aplicação concreta neste escopo: uv run --no-project --no-python-downloads --with 'PyYAML>=6,<7' python -c 'import yaml; print(yaml.__version__)' executado com sucesso (6.0.3). Nenhuma mudança de AGENTS.md ou autorização presumida para Git/publicação. Suíte reiniciada com --basetemp em diretório exclusivo criado sob /tmp/opencode/wiked-validation-XXXXXX, preservando fixture anterior da revisão manual. Solicitante informou que o teste manual funcionou e observou os links.

**2026-10-24T21:51:17.786516302Z**

Validação final concluída após disponibilizar PyYAML no cache: uv run pytest --basetemp <diretório exclusivo sob /tmp/opencode> => 221 passed, 2 skipped em 230.55s, sem falhas. Mantido teste offline inalterado. Teste real Docsify/Chromium do HTML copiado já passou (1 passed); solicitante também confirmou funcionamento manual e links. Checks técnicos de manifesto/versão 1.6.0, links, ASCII, whitespace e scripts passaram. Fixture manual anterior preservada. Sem publicação, Git ou alterações de consumidor real.

**2026-10-24T21:51:26.148070573Z**

Exemplo index.html com adaptador inline substitui JS separado; adoção e atualizações consumer-owned independentes da skill orientadas no guia, manutenção e changelog 1.6.0. Suíte final: 221 passed, 2 skipped, sem falhas; navegador real e checagem manual confirmados. Sem publicação ou alterações em consumidores reais.
