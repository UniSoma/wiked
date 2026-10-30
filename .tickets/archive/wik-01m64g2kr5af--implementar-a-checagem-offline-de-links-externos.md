---
id: wik-01m64g2kr5af
title: Implementar a checagem offline de links externos no validador
status: closed
type: feature
priority: 2
mode: hitl
created: '2026-10-29T18:52:06.779244016Z'
updated: '2026-10-30T14:58:47.034415009Z'
closed: '2026-10-30T14:58:47.034415009Z'
tags:
- metodologia
- wiked
- validador
acceptance:
- title: Validador diagnostica URLs externas malformadas e esquemas não permitidos quando rules.external_links está declarada
  done: true
- title: Contratos sem rules.external_links mantêm o resultado de validação
  done: true
- title: Módulo compartilhado de extração de links e leitura do contrato pronto para reuso
  done: true
- title: Documentação atualizada, com targeted textual checks
  done: true
- title: uv run pytest passa com fixtures sintéticas e sem asserções sobre prosa
  done: true
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

## Notes

**2026-10-30T14:44:37.447936684Z**

Grill metodológico de implementação, rodadas 1-2: Q1 mínimo methodology_version 1.8.0 por contract.relation (inclusive --contract-only), sem subir manifesto nem CHANGELOG; testes com manifesto sintético 1.8.0. Q2 códigos external-link.malformed e external-link.scheme sob uma severidade rules.external_links; um diagnóstico por ocorrência. Q3 todo *.md sob wiki/, só o corpo (frontmatter fora); externo = destino com esquema ou netloc; links inline, por referência e autolinks; HTML bruto, URLs soltas e código fora. Q4 extrator com validateLink permissivo para expor javascript:/file: etc.; esquema sem distinção de caixa; //host sem esquema recebe external-link.scheme. Q5 malformado sintático: http(s) com urlsplit válido, hostname, porta válida e host IP literal ou rótulos DNS válidos (IDN via IDNA); mailto com endereços local@domínio; sem rede. Q6 módulo compartilhado único scripts/wiki_core.py (Diagnostic, issue, issue_key, load_data, validate_contract, severity, split_page, markdown_links, extração e classificação offline), manifestado em runtime; validate_wiki.py importa dele. Q7 contracts/README.md e scripts/README.md (formato, regra e ajuste da frase sobre links externos informativos), passo 4 do SKILL.md e entrada no manifesto; guides intocados. Q8 permanecer na branch wik-01m64g2kj369-autoridade-externa (família de tickets). Q9 imagens externas incluídas, esquemas aceitos http/https; mailto em imagem gera external-link.scheme; ajuste do requerente: data: não é link para fora e permanece permitido e fora da regra, em links e imagens.

**2026-10-30T14:46:45.815426542Z**

Entendimento compartilhado confirmado explicitamente pelo requerente validador em 2026-10-30; grill metodológico de implementação encerrado.

**2026-10-30T14:53:36.657362426Z**

Implementação na branch wik-01m64g2kj369-autoridade-externa (sem commit). Novo módulo manifestado scripts/wiki_core.py com leitura/validação do contrato, diagnósticos, split_page, markdown_links, external_links (parser com validateLink permissivo, data: excluído) e external_link_problem (classificação offline); validate_wiki.py importa dele sem mudar comportamento. rules.external_links no schema, contract.relation com mínimo 1.8.0, diagnósticos external-link.scheme|malformed. Documentação em contracts/README.md, scripts/README.md e passo 4 do SKILL.md. Evidência: uv run pytest — suíte completa sem falhas (2 skips de integração externa), com casos novos em tests/test_wiked_validator.py usando fixtures sintéticas e manifesto sintético 1.8.0, asserções só sobre códigos, severidades, caminhos e exit codes; o teste de corte passa a exigir a importação de distribution via wiki_core. Targeted textual checks: sem dependência de docs/, texto genérico em inglês, sem conhecimento de consumidor, arquivo novo presente no manifesto e nenhum resíduo fora dele. Manifesto e CHANGELOG permanecem em 1.7.0.

**2026-10-30T14:58:47.034415009Z**

Checagem offline opcional de links externos (rules.external_links, mínimo 1.8.0, external-link.scheme|malformed, data: fora da regra) e módulo compartilhado scripts/wiki_core.py; aceita pelo requerente validador em 2026-10-30. Manifesto e CHANGELOG 1.8.0 ficam para a preparação humana da release.
