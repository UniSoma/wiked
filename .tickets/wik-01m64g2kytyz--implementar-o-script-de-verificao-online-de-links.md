---
id: wik-01m64g2kytyz
title: Implementar o script de verificação online de links externos
status: open
type: feature
priority: 2
mode: hitl
created: '2026-10-29T18:52:06.983580402Z'
updated: '2026-10-29T18:52:06.983580402Z'
tags:
- metodologia
- wiked
- manutencao
acceptance:
- title: Script apartado com --timeout e --workers, limite por host e saída text/json
  done: false
- title: Diagnósticos distintos por causa, sem afirmar inexistência do documento
  done: false
- title: Ausência de rules.external_reachability encerra com código 2
  done: false
- title: Testes com servidor HTTP local cobrem 200, 401/403, 404, 5xx, timeout, redirecionamento e rejeição de HEAD, sem rede externa
  done: false
- title: Manifesto, scripts/README.md, guides/maintenance.md e SKILL.md atualizados, preservando o carregamento progressivo
  done: false
deps:
- wik-01m64g2kr5af
links:
- wik-01m64bng5vzs
---

## Description

Implementar a camada online da Feature 2 decidida no grill metodológico de wik-01m64bng5vzs (consultar as notas desse ticket para o contexto completo).

- Script apartado `scripts/check_external_links.py`, listado no manifesto e acionado pelo guia de manutenção só quando o mantenedor pede. Fica fora da rota de validação exigida pelos fluxos governados.
- Reutiliza o módulo compartilhado do ticket da camada offline e ignora links malformados, que o validador já reporta.
- Rede: cada URL distinta é acessada uma vez, com `HEAD` e recuo para `GET`. Redirecionamentos são seguidos com limite, nenhuma credencial ou cookie é enviado e fragmentos não são verificados. `--timeout` tem padrão de 10 s, `--workers` tem padrão de 8, e há limite fixo de 2 conexões por host. `mailto` não é acessado.
- Severidade: `rules.external_reachability` (error|warning). Sem a regra declarada, o script sai com código 2 e orienta a declarar a regra. Saída `text`/`json` e códigos de saída como os do validador.
- Diagnósticos distintos para: DNS ou conexão, tempo esgotado, TLS, 401/403, 404/410, 5xx e outras respostas. As mensagens descrevem o observado e nunca afirmam que o documento não existe. Redirecionamento para login conta como sucesso.
- Documentação: seção própria em `scripts/README.md`, procedimento opcional curto em `guides/maintenance.md` (inclui a ressalva sobre links autenticados) e rota "Check external link reachability" em `SKILL.md`.
