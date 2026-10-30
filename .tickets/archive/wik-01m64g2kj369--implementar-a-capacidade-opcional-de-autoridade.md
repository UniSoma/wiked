---
id: wik-01m64g2kj369
title: Implementar a capacidade opcional de autoridade externa por tipo de página
status: closed
type: feature
priority: 2
mode: hitl
created: '2026-10-29T18:52:06.586236773Z'
updated: '2026-10-30T14:36:35.207469783Z'
closed: '2026-10-30T14:36:35.207469783Z'
tags:
- metodologia
- wiked
- validador
acceptance:
- title: Metacontrato aceita external_authority no tipo de página, exige rules.external_authority só quando declarada e exige a methodology_version mínima
  done: true
- title: Validador diagnostica aviso ausente, fora da posição, com texto divergente e link exigido ausente ou não http(s) absoluto
  done: true
- title: Contratos sem a capacidade mantêm o resultado de validação
  done: true
- title: Documentação em contracts/README.md e guides/modeling.md, com targeted textual checks
  done: true
- title: uv run pytest passa com fixtures sintéticas e sem asserções sobre prosa
  done: true
links:
- wik-01m64bng5vzs
---

## Description

Implementar a Feature 1 decidida no grill metodológico de wik-01m64bng5vzs (consultar as notas desse ticket para o contexto completo).

- Contrato: `page_types.<tipo>.external_authority` opcional, com `notice` (texto literal no idioma da instância) e `link: required | optional`. `rules.external_authority` passa a ser obrigatória só quando algum tipo declara a capacidade. Declarar a capacidade exige a próxima `methodology_version` minor; `contract_version` permanece 1.0.
- Validação: o primeiro bloco depois do H1 é uma citação cujo primeiro parágrafo contém literalmente o aviso configurado, ignorando formatação inline. Com `link: required`, ou quando um link estiver presente, ele é um link `http(s)` absoluto dentro da citação. O link não depende da proveniência e não há regra de igualdade com o registro da fonte.
- Documentação: `contracts/README.md` (formato e regra) e `guides/modeling.md` (parágrafo curto sobre o aviso; a coerência entre aviso, link e fonte cabe ao humano). Preservar o carregamento progressivo.
- Fora de escopo: comparar conteúdo externo ou decidir correção, vigência, completude, autorização ou responsabilidade.

## Notes

**2026-10-30T14:27:38.255797118Z**

Grill metodológico de implementação, rodada 1 (todas as recomendações aceitas): Q1 mínimo methodology_version 1.8.0 no validador, sem subir manifesto nem CHANGELOG (preparação de release humana); testes com manifesto sintético 1.8.0 no runtime copiado. Q2 códigos external-authority.missing|position|notice|link sob rules.external_authority. Q3 aviso em texto puro, comparado por substring sensível a maiúsculas com o texto renderizado do primeiro parágrafo da citação (text, code_inline, rótulos de link), espaços e quebras colapsados. Q4 todo link (inclusive autolink) da citação deve ser http/https com host; required exige ao menos um; imagens ignoradas. Q5 usa o primeiro H1; sem H1 não verifica posição (h1.count cobre). Q6 schema {notice: nonEmptyString, link: required|optional}, ambos obrigatórios, additionalProperties false; exigência de rules.external_authority e methodology_version >= 1.8.0 por contract.relation; regra sem tipo permanece aceita. Q7 documentação em contracts/README.md, guides/modeling.md e uma frase em scripts/README.md e SKILL.md (ampliação aprovada).

**2026-10-30T14:27:52.741379912Z**

Entendimento compartilhado confirmado explicitamente pelo requerente validador em 2026-10-30; grill metodológico de implementação encerrado.

**2026-10-30T14:32:47.478888496Z**

Implementação na branch wik-01m64g2kj369-autoridade-externa (sem commit). Evidência: uv run pytest — suíte completa aprovada (2 skips de integração externa), incluindo 21 casos novos em tests/test_wiked_validator.py com fixtures sintéticas, manifesto sintético 1.8.0 e asserções apenas sobre códigos, severidades e exit codes. Targeted textual checks: sem dependência de docs/ nos arquivos distribuídos alterados, texto genérico em inglês, sem conhecimento de consumidor, âncoras referenciadas (modeling.md#intent-map, scripts/README.md#maintenance-review-acknowledgment) preservadas, nenhum arquivo novo fora do manifesto. Manifesto e CHANGELOG permanecem em 1.7.0 por decisão Q1: contratos que declaram a capacidade são rejeitados até a preparação humana da 1.8.0.

**2026-10-30T14:36:35.207469783Z**

Capacidade opcional page_types.<tipo>.external_authority implementada (schema, relações de contrato com mínimo 1.8.0 e rules.external_authority, diagnósticos external-authority.missing|position|notice|link, documentação e testes sintéticos); aceita pelo requerente validador em 2026-10-30. Manifesto e CHANGELOG 1.8.0 ficam para a preparação humana da release.
