---
id: wik-01m5zcsy6ky7
title: Corrigir a mensagem de primeira instalação que pressupõe um instance contract existente
status: closed
type: bug
priority: 3
mode: hitl
created: '2026-10-27T19:18:44.690408083Z'
updated: '2026-10-27T21:12:57.061837942Z'
closed: '2026-10-27T21:12:57.061837942Z'
assignee: VolneiSantos
links:
- wik-01m5zb67c010
---

## Description

Lateral de wik-01m5zb67c010. scripts/install-wiked.sh imprime na primeira instalação 'start wiked-setup with the installed skill and instance contract.', mas normalmente o contrato ainda não existe nesse momento: o setup o cria. docs/distribution.md:242 especifica a mesma instrução.

## Notes

**2026-10-27T19:31:11.479789982Z**

Methodological grill fechado em 2026-10-27: validador expõe contract.methodology_version no JSON; instalador ramifica a primeira instalação (sem contrato → setup; mesma versão → operar via skill; versão anterior → maintenance_since=methodology_version e prompt de manutenção); spec em distribution.md/installation.md (inclui correção 'local contract' em distribution.md:251-252); testes novos; manifesto/CHANGELOG intocados (recomendação patch ou minor, 'none').

**2026-10-27T19:48:20.541469931Z**

Implementado e verificado (2026-10-27): validate_wiki.py inclui contract.methodology_version no relatório JSON quando o contrato passa no schema (modos completo e --contract-only), documentado em scripts/README.md; install-wiked.sh: compatibility() retorna a versão declarada (bloqueia se o candidato não a reportar), primeira instalação sem contrato → wiked-setup para criar o contrato; com contrato de mesma versão → operar via skill; com versão anterior → maintenance_since=versão declarada e prompt de manutenção; dry run não registra nem imprime prompt. Spec atualizada em docs/distribution.md (inclui 'local contract' → 'Instance contract' em 251-252) e docs/installation.md. Testes novos: test_first_installation_routes_by_existing_contract_methodology, test_first_installation_over_older_contract_requires_maintenance_review, asserções do campo contract em test_wiked_validator. uv run pytest completo: todos passaram (2 skipped). Manifesto e CHANGELOG intocados; recomendação para release: patch ou minor (campo JSON aditivo), declaração 'none'.

**2026-10-27T21:12:57.061837942Z**

Aprovado pelo requerente em 2026-10-27. Primeira instalação ramifica pelo instance contract: sem contrato → wiked-setup; mesma versão → operar via skill; versão anterior → revisão pendente desde a versão declarada e prompt de manutenção. Validador expõe contract.methodology_version no JSON. Pendente para o release humano: versão (patch ou minor) e declaração 'none' no CHANGELOG.
