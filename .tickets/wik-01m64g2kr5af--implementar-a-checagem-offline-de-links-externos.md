---
id: wik-01m64g2kr5af
title: Implementar a checagem offline de links externos no validador
status: open
type: feature
priority: 2
mode: hitl
created: '2026-10-29T18:52:06.779244016Z'
updated: '2026-10-29T18:52:06.779244016Z'
tags:
- metodologia
- wiked
- validador
acceptance:
- title: Validador diagnostica URLs externas malformadas e esquemas não permitidos quando rules.external_links está declarada
  done: false
- title: Contratos sem rules.external_links mantêm o resultado de validação
  done: false
- title: Módulo compartilhado de extração de links e leitura do contrato pronto para reuso
  done: false
- title: Documentação atualizada, com targeted textual checks
  done: false
- title: uv run pytest passa com fixtures sintéticas e sem asserções sobre prosa
  done: false
links:
- wik-01m64bng5vzs
---

## Description

Implementar a camada offline da Feature 2 decidida no grill metodológico de wik-01m64bng5vzs (consultar as notas desse ticket para o contexto completo).

- Escopo: todos os links explícitos e autolinks externos em Markdown da wiki. URLs soltas no texto continuam informativas.
- Esquemas aceitos: `http`, `https` e `mailto`. URLs malformadas e outros esquemas (por exemplo `file:` ou `javascript:`) geram diagnóstico.
- Regra: `rules.external_links`, opcional e de adoção explícita, que exige a próxima `methodology_version` minor. Sem a regra, a checagem não roda; `contract_version` permanece 1.0.
- Extrair para um módulo compartilhado a extração de links externos e a leitura do contrato que o script online (ticket dependente) vai reutilizar, sem wrapper e sem regra duplicada.
- Documentação: uma linha em `scripts/README.md` e o formato da regra em `contracts/README.md`.
