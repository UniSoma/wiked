---
id: wik-01m310mknyjs
title: Precisar a governança da rota de diagramas do Wiked
status: closed
type: task
priority: 3
mode: hitl
created: '2026-09-21T03:37:30.558065496Z'
updated: '2026-10-13T22:44:39.710801210Z'
closed: '2026-10-13T22:44:39.710801210Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- melhoria
- diagrama
acceptance:
- title: Grill metodológico encerrado com decisão explícita sobre criação, ajuste visual, regeneração e exportação temporária
  done: true
- title: Rotas e guias tornam explícitos os pré-requisitos de governança e as exceções aprovadas, sem inferir autorização da ausência de mudança semântica
  done: true
- title: Verificações textuais percorrem os cenários e confirmam coerência, carga seletiva e ausência de dependências de domínio
  done: true
---

## Description

### Constatação
A avaliação metodológica identificou que o roteador encaminha criação, revisão e renderização diretamente ao guia D2. O invariante geral exige grill antes de alterar conteúdo governado, mas o guia explicita o retorno ao grill apenas para correções com escolha semântica. A aplicação da regra a criação, ajustes visuais, regeneração e exportação temporária depende de interpretação.
### Entrega
Conduzir grill metodológico e tornar inequívoco o percurso de cada classe de operação, incluindo qualificação humana, fechamento do grill e eventuais exceções aprovadas. Harmonizar roteador, D2, grill e exportação sem alterar conteúdo de uma instância. A regra global existe; o objetivo é fechar seu encadeamento, não pressupor uma autorização ausente.
### Independência
Melhoria genérica avulsa, não pré-requisito da extração ou publicação. O registro não encerra o grill nem aprova antecipadamente exceções. Executar na origem canônica vigente do Wiked.

## Notes

**2026-10-10T18:40:28.451016281Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-13T22:43:00.962259733Z**

Grill metodológico encerrado: Volnei confirmou explicitamente o resumo final nesta sessão. Escopo autorizado: SKILL.md e guides/d2.md, export.md, grill.md, authoring-context.md. Criação permanente, ajuste visual e regeneração de diagramas exigem qualificação humana e grill fechado, mesmo sem mudança semântica; podem executar sob aprovação já existente apenas no escopo coberto. Preparação contextual comum para autoria permanente. Revisão e comparação temporária dispensam grill sem autorizar escrita permanente. Exportação solicitada pode copiar/converter/criar/ajustar temporariamente com base no Markdown canônico, fora da wiki e sem promover ajustes a assets permanentes; ambiguidade semântica interrompe a parte afetada e exige decisão humana via grill, sem autorização implícita de corrigir a wiki. Nova decisão substantiva ou ampliação de arquivos reabre grill, inclusive em upgrade de renderer. Sem mudanças em consumidores, runtime, schema, política geral de tickets ou publicação. Validação por checks textuais técnicos e revisão metodológica de cenários; não constitui cobertura comportamental.

**2026-10-13T22:44:32.167901051Z**

Implementação concluída nos cinco arquivos aprovados. SKILL.md encaminha operações permanentes aos pré-requisitos específicos; d2.md classifica autoria permanente, revisão somente leitura e exportação, separa comandos mutadores, exige preparação/qualificação/grill e limita upgrade de renderer ao conjunto aprovado. export.md concentra a exceção temporária, distingue fonte D2 técnica de evidência e permite fonte temporária nova baseada no Markdown. grill.md harmoniza conteúdo governado e escolhas semânticas na exportação; authoring-context.md inclui autoria permanente sem impor preparação autoral à consulta. Revisão metodológica percorreu: criação permanente com Markdown completo; ajuste só visual; regeneração de derivado sem mudar fonte; uso de grill existente; upgrade com ampliação de conjunto; revisão/comparação sem escrita permanente; cópia de SVG aceito sem D2; criação/ajuste/conversão temporária sem embedding ou promoção; lacuna semântica interrompendo exportação e exigindo grill sem autorizar correção permanente. Guias query/modeling/maintenance/assisted-indexing e manifesto foram confrontados sem necessidade de alteração. Check técnico não Python via Node confirmou os cinco arquivos no inventário, ausência de dependência docs/ e existência de 37 referências a guias. Revisão manual confirmou inglês genérico, ausência de conhecimento de consumidor e carga seletiva. Duas tentativas de check ASCII estrito falharam por símbolos preexistentes em grill.md; disposição explícita: preservar travessão e símbolos do template canônico, sem normalização fora de escopo. Check final de referências/dependências passou e inventário Unicode foi revisado. Não foram adicionadas assertions de prosa nem executado pytest: alteração somente instrucional. Os cenários foram revisados metodologicamente, não executados como avaliação comportamental. Sem alterações de consumidores, runtime, schema, versão ou publicação.

**2026-10-13T22:44:39.710801210Z**

Governança da rota de diagramas explicitada após grill metodológico confirmado: alterações permanentes exigem preparação, qualificação e fechamento no escopo; revisão temporária e exportação solicitada têm exceções delimitadas, sem autorizar correções permanentes ou inferências semânticas. Cinco arquivos instrucionais harmonizados, três critérios satisfeitos, checks técnicos e revisão de cenários registrados; sem alegação de avaliação comportamental ou publicação.
