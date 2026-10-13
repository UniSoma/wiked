---
id: wik-01m4vhmcwene
title: Revisar verificações textuais das instruções metodológicas
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-13T21:10:26.446331377Z'
updated: '2026-10-13T21:32:06.261769758Z'
closed: '2026-10-13T21:32:06.261769758Z'
tags:
- metodologia
- tests
acceptance:
- title: Revisar os três arquivos, remover asserções de prosa e registrar justificativas, preservando contratos técnicos e testes de execução
  done: true
- title: Harmonizar vocabulário e validação; AGENTS.md proíbe novos testes que congelam prosa metodológica
  done: true
- title: Criar ticket vinculado de evals com cenários prioritários especificados e controle de custo explícito
  done: true
- title: Executar uv run pytest e registrar o resultado sem declarar cobertura comportamental substituída
  done: true
links:
- wik-01m4vhpp3xyt
---

## Description

Objetivo aprovado: preservar verificações estruturais e contratos técnicos, removendo asserções que congelam redação da prosa e aparentam comprovar comportamento metodológico.

Escopo: tests/test_wiked_validator.py, tests/test_wiked_packaging.py, tests/test_wiked_installer.py; harmonização mínima de docs/metodologia.md e docs/CONTEXT.md; instrução explícita em AGENTS.md para impedir recorrência. Diagnósticos produzidos durante execução, runtime, distribuição e documentos de instalação permanecem fora do escopo de alteração.

O solicitante confirmou e aprovou o resumo final do Methodological grill e explicitou a orientação preventiva em AGENTS.md. Decisões: literais apenas para contratos técnicos; remoções não exigem eval substituta implementada, mas exigem justificativa e identificação de cenários críticos futuros; implementação das evals em ticket separado vinculado; custo de tokens controlado, sem repetições automáticas obrigatórias neste trabalho. Os cenários especificam contexto, solicitação, comportamento esperado, violações observáveis, evidências e forma de avaliação.

Registro de remoções e validação ficará neste ticket. Nenhuma remoção constitui cobertura comportamental já substituída. Alterações de testes requerem uv run pytest. Não manipular Git nem instalar ferramentas.

## Notes

**2026-10-13T21:31:58.224818623Z**

Revisão implementada após confirmação explícita do grill e autorização adicional de instrução preventiva em AGENTS.md.

Justificativas e lacunas por bloco:
- tests/test_wiked_validator.py: removida a frase sobre schema/validator do adaptador; preservados manifesto e destino guides/setup.md. Retiradas frases sobre qualificação, Git, raw e ausência de inspeção: sua presença não prova gates ou comportamento. Preservadas exclusões human_authority/ingestion do schema e extraída a verificação do template técnico raw/archive/YYYY-MM-DD_<ticket-id>/. Comportamentos futuros: S2 e S3.
- tests/test_wiked_validator.py: removido o teste de frases sobre intent routes, consulta somente leitura, fallback, curadoria, escopo localizado, idioma e limites semânticos. Reformulações equivalentes quebravam o teste e contradições podiam passar. Comportamentos futuros: S1, S4 e S6; revisão de versão: S5. Testes reais do mapa/validador preservados.
- tests/test_wiked_packaging.py: mantidas declarações executadas de versão e dependências documentadas do changelog, com destino ../CHANGELOG.md sem congelar rótulo do link. Removidas frases sobre releases pulados, correction tickets, reconhecimento pelo humano e prompt do README (inclusive quebras de linha). O teste foi renomeado para refletir o que realmente verifica. Comportamentos futuros: S5 e S6.
- tests/test_wiked_installer.py: removidas frases sobre confiança, checksum e stdin; preservados comando oficial, flags, artefato e identificador obsoleto SHA256SUMS. Retirada exigência de newline no comando. Nome do teste agora descreve interfaces documentadas, não ordem ou confiança. Coerência da prosa continua sujeita à revisão documental, não a um cenário artificial de agente; testes reais de instalação/terminal/segurança permanecem.

Orientações harmonizadas em docs/CONTEXT.md e docs/metodologia.md: distinção entre contratos técnicos, revisão semântica e Behavioral evaluation; remoções justificadas e lacunas explícitas; evals não são requisito em toda alteração. AGENTS.md proíbe congelar prosa metodológica por substring, regex ou snapshot e remete aos limites de validação canônicos.

Ticket futuro vinculado wik-01m4vhpp3xyt contém seis cenários com contexto, solicitação, esperado, violações, evidências e avaliação. Implementação, modelo, orçamento, acionamento, repetições e thresholds exigem grill próprio. Nenhuma eval foi implementada ou executada; a especificação não substitui cobertura comportamental.

Validação: a primeira tentativa foi interrompida sem resultado; retomada solicitada pelo usuário. uv run pytest completou: 157 passed, 1 skipped in 92.59s. Nenhuma alteração de runtime, distribuição ou diagnósticos de execução; nenhuma operação Git.

**2026-10-13T21:32:06.261769758Z**

Revisadas as verificações de documentação nos três arquivos de testes; removido congelamento de prosa e preservados contratos técnicos e testes de execução. AGENTS.md contém orientação preventiva, com vocabulário e validação harmonizados. Seis cenários e controle de custo especificados no ticket futuro wik-01m4vhpp3xyt, sem implementação de evals. Validação: uv run pytest — 157 passed, 1 skipped.
