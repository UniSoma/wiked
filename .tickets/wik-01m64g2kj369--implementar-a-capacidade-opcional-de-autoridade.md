---
id: wik-01m64g2kj369
title: Implementar a capacidade opcional de autoridade externa por tipo de página
status: open
type: feature
priority: 2
mode: hitl
created: '2026-10-29T18:52:06.586236773Z'
updated: '2026-10-29T18:52:06.586236773Z'
tags:
- metodologia
- wiked
- validador
acceptance:
- title: Metacontrato aceita external_authority no tipo de página, exige rules.external_authority só quando declarada e exige a methodology_version mínima
  done: false
- title: Validador diagnostica aviso ausente, fora da posição, com texto divergente e link exigido ausente ou não http(s) absoluto
  done: false
- title: Contratos sem a capacidade mantêm o resultado de validação
  done: false
- title: Documentação em contracts/README.md e guides/modeling.md, com targeted textual checks
  done: false
- title: uv run pytest passa com fixtures sintéticas e sem asserções sobre prosa
  done: false
links:
- wik-01m64bng5vzs
---

## Description

Implementar a Feature 1 decidida no grill metodológico de wik-01m64bng5vzs (consultar as notas desse ticket para o contexto completo).

- Contrato: `page_types.<tipo>.external_authority` opcional, com `notice` (texto literal no idioma da instância) e `link: required | optional`. `rules.external_authority` passa a ser obrigatória só quando algum tipo declara a capacidade. Declarar a capacidade exige a próxima `methodology_version` minor; `contract_version` permanece 1.0.
- Validação: o primeiro bloco depois do H1 é uma citação cujo primeiro parágrafo contém literalmente o aviso configurado, ignorando formatação inline. Com `link: required`, ou quando um link estiver presente, ele é um link `http(s)` absoluto dentro da citação. O link não depende da proveniência e não há regra de igualdade com o registro da fonte.
- Documentação: `contracts/README.md` (formato e regra) e `guides/modeling.md` (parágrafo curto sobre o aviso; a coerência entre aviso, link e fonte cabe ao humano). Preservar o carregamento progressivo.
- Fora de escopo: comparar conteúdo externo ou decidir correção, vigência, completude, autorização ou responsabilidade.
