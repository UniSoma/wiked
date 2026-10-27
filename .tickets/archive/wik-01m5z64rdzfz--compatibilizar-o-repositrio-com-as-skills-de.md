---
id: wik-01m5z64rdzfz
title: Compatibilizar o repositório com as skills de engenharia e explicitar a fronteira de Git do agente
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-27T17:22:19.199491528Z'
updated: '2026-10-27T18:56:50.738158371Z'
closed: '2026-10-27T18:56:50.738158371Z'
assignee: VolneiSantos
acceptance:
- title: AGENTS.md contém bloco Agent skills e docs/agents/{issue-tracker,domain}.md existem
  done: true
- title: GLOSSARY.md na raiz no formato do domain-modeling; docs/CONTEXT.md e CONTEXT-MAP.md removidos sem referências residuais fora de tests/
  done: true
- title: Regra de Git (develop/main exclusivamente humanos; push/merge/rebase/tag/release humanos) em AGENTS.md e docs/metodologia.md
  done: true
- title: Report e reports/README.md atualizados como pesquisa viva não normativa
  done: true
- title: Targeted textual checks registrados no ticket
  done: true
---

## Description

Methodological grill fechado em 2026-10-27 com confirmação explícita do requerente.

Escopo:
- Bloco `## Agent skills` em AGENTS.md (CLAUDE.md permanece `@AGENTS.md`, desvio deliberado do setup): issue tracker Knot em `docs/agents/issue-tracker.md` (operações básicas via skill/CLI knot, sem wayfinding); domain docs single-context em `docs/agents/domain.md`; sem triage labels (skill `triage` não instalada).
- `docs/CONTEXT.md` → `/GLOSSARY.md` no formato GLOSSARY-FORMAT do domain-modeling (definições de 1–2 frases, sem detalhes de implementação, `_Avoid_` só para sinônimos pouco usados: Source repository, Instance contract, Methodological grill).
- Regras exclusivas do glossário movidas para docs/metodologia.md (Installed skill não modificado por workflows consumidores; coexistência antes do Runtime cutover; limites da Behavioral evaluation); duplicatas descartadas.
- Remover CONTEXT-MAP.md; AGENTS.md lê GLOSSARY.md e docs/metodologia.md e lista no Layout só o que faltava, sem redundância.
- Atualizar referências em README.md e docs/metodologia.md.
- Git: stage/commit em develop e main são exclusivamente humanos; em outras branches o agente pode criar branch, stage e commit; push, merge, rebase, tag e release permanecem humanos. Seção histórica de extração inalterada.
- Report: atualizar L1 e links L2–L8 (`../.agents/` → `../distr/agents/`) em reports/investigacao-wiked.md; reports/README.md deixa de declarar preservação byte-for-byte/SHA-256 e nota de mapeamento; "historical" → "research" em AGENTS.md e README.md, mantendo idioma original e caráter não normativo.

Validação: Targeted textual checks (instrução apenas; sem pytest).
Lateral: alinhar uso de "local contract" e "validator" ao glossário.

## Notes

**2026-10-27T17:23:34.736688492Z**

Implementado e verificado (Targeted textual checks, 2026-10-27):
- Sem referências residuais a CONTEXT-MAP.md, docs/CONTEXT.md, "byte-for-byte", SHA do report ou "manipulate Git" em AGENTS.md/README.md/docs/reports. Restam apenas: tests/ (CONTEXT.md de wikis sintéticas, fora de escopo) e distr/agents/skills/wiked/SKILL.md:49 (regra Git do consumidor, fora de escopo).
- Todos os links Markdown relativos em AGENTS.md, README.md, GLOSSARY.md, docs/metodologia.md, docs/agents/*.md, reports/*.md resolvem.
- Report: além de L1 e L2–L8, a linha L9 também apontava para ../.agents/ e foi corrigida para ../distr/agents/ (mesmo critério aprovado).
- Regras movidas do glossário para docs/metodologia.md: Installed skill não modificado por workflows consumidores; coexistência antes do Runtime cutover; limites da Behavioral evaluation.
- Sem pytest: nenhuma mudança em runtime ou testes.
Pendente: aceitação humana e stage/commit em develop (humano).

**2026-10-27T18:56:50.738158371Z**

Aprovado pelo requerente em 2026-10-27. Repositório compatível com setup-matt-pocock-skills: bloco Agent skills em AGENTS.md, docs/agents/{issue-tracker,domain}.md, GLOSSARY.md na raiz no formato do domain-modeling (CONTEXT-MAP.md e docs/CONTEXT.md removidos), regra de Git (develop/main exclusivamente humanos), report atualizado como pesquisa viva não normativa.
