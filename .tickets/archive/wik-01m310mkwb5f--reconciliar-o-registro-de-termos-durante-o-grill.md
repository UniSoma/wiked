---
id: wik-01m310mkwb5f
title: Reconciliar o registro de termos durante o grill com o fechamento obrigatório
status: closed
type: task
priority: 3
mode: hitl
created: '2026-09-21T03:37:30.762947404Z'
updated: '2026-10-12T23:52:46.509427181Z'
closed: '2026-10-12T23:52:46.509427181Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
- governanca
acceptance:
- title: Grill metodológico decide explicitamente quando e sob qual autorização um termo resolvido pode ser registrado
  done: true
- title: Invariante e guias expressam uma única regra coerente, incluindo o limite de qualquer exceção
  done: true
- title: Verificações textuais distinguem termo resolvido, decisão ainda aberta e consolidação final, sem permitir alterações incidentais de outros conteúdos
  done: true
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

**2026-10-12T23:51:49.333397026Z**

Grill metodológico encerrado: o solicitante confirmou explicitamente o resumo e autorizou a implementação. Termos resolvidos permanecem na conversa ou em registros Knot antes do fechamento; gravar o contexto exige confirmação explícita do resumo final com termos e definições. Decisões abertas não são aprovação, e nova decisão substantiva retoma o grill. Setup prepara initial_content antes e grava contrato/contexto depois. Escopo: SKILL.md e guias de grill, indexação e setup, preservando o invariante geral correto e alterando somente o necessário. Sem exceção para outras edições; runtime, schema, testes Python, consumidor, instalação e publicação fora do escopo. Validação por checks textuais direcionados.

**2026-10-12T23:52:39.053289664Z**

Implementação concluída nos guias distribuídos grill.md, assisted-indexing.md e setup.md. SKILL.md preservado: seu invariante geral já exige fechamento antes de qualquer edição governada. Removida a exceção de termos durante entrevista; resumo final inclui termos e definições acordados e distingue decisões abertas; indexação grava contexto apenas na consolidação dentro do escopo confirmado; setup prepara initial_content na conversa/Knot e grava após confirmação. Checks textuais aprovados para regra geral, registro pré-fechamento, decisões abertas, confirmação humana, retomada do grill, ausência de edições incidentais, sequência da indexação/setup, preservação de contrato compatível, alinhamento com modelagem/manutenção, identidade autor/consumidor, contrato local, referências existentes, ownership no manifesto e ausência de docs/ e permissões antigas. Verificação inicial de ASCII integral rejeitou emojis/travessões preexistentes do grill; corrigido o check para os trechos alterados, todos em inglês/ASCII, preservando formatação histórica. Sem alterações de runtime/schema/testes Python, portanto pytest não aplicável à rota instruction-only. Nenhuma operação Git, instalação ou publicação.

**2026-10-12T23:52:46.509427181Z**

Grill metodológico confirmado e regra reconciliada: termos só são gravados no contexto após confirmação final; indexação e setup harmonizados, sem exceções para edições incidentais. Três critérios atendidos e checks textuais aprovados, com evidência registrada. Invariante geral preservado; runtime, schema e testes Python não alterados.
