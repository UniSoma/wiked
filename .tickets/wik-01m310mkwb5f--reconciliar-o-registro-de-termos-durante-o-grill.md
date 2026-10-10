---
id: wik-01m310mkwb5f
title: Reconciliar o registro de termos durante o grill com o fechamento obrigatório
status: open
type: task
priority: 3
mode: hitl
created: '2026-09-21T03:37:30.762947404Z'
updated: '2026-10-10T18:40:29.089880615Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
- governanca
acceptance:
- title: Grill metodológico decide explicitamente quando e sob qual autorização um termo resolvido pode ser registrado
  done: false
- title: Invariante e guias expressam uma única regra coerente, incluindo o limite de qualquer exceção
  done: false
- title: Verificações textuais distinguem termo resolvido, decisão ainda aberta e consolidação final, sem permitir alterações incidentais de outros conteúdos
  done: false
---

## Description

### Constatação
O invariante geral da skill exige encerramento do grill antes de criar ou alterar conteúdo governado, enquanto o guia de grill permite registrar no contexto um termo de domínio resolvido durante a entrevista. A indexação também referencia essa permissão. A exceção não está reconciliada explicitamente com o enunciado geral.
### Entrega
Conduzir grill metodológico para decidir entre manter uma exceção estreita, com limites explícitos, ou adiar o registro para depois da confirmação final. Harmonizar skill, grill e indexação segundo a decisão, preservando a autoridade humana e sem expandir a permissão para outras edições.
### Independência
Melhoria genérica avulsa, não bloqueia a separação dos repositórios. A abertura do ticket registra a questão; a política final depende do grill. Executar na origem canônica vigente do Wiked.

## Notes

**2026-10-10T18:40:29.089880615Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.
