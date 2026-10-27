---
id: wik-01m5z64vwzy0
title: Alinhar uso de 'local contract' e 'validator' ao glossário
status: closed
type: task
priority: 3
mode: hitl
created: '2026-10-27T17:22:22.750856523Z'
updated: '2026-10-27T18:56:52.511837335Z'
closed: '2026-10-27T18:56:52.511837335Z'
links:
- wik-01m5zb67c010
---

## Description

Lateral de wik-01m5z64rdzfz: 'local contract' e 'validator' são sinônimos amplamente usados de Instance contract e Distributed runtime em AGENTS.md, docs/ e distr/. Decidir se viram _Avoid_ no GLOSSARY.md e realinhar o uso.

## Notes

**2026-10-27T18:50:06.767068018Z**

Methodological grill fechado em 2026-10-27. Escopo: GLOSSARY.md, AGENTS.md, docs/metodologia.md (exceto seção histórica), docs/distribution.md. Distributed runtime → Distributed validator (_Avoid_: distributed runtime, portable validator); Instance contract _Avoid_: consumer contract, local contract; Runtime cutover mantém nome; validator/runtime genéricos livres. README.md, docs/installation.md, scripts/install-wiked.sh, distr/ e reports/ seguem vocabulário do consumidor e ficam fora. Lateral: vocabulário da instalação em distr/ e mensagem do instalador.

**2026-10-27T18:50:35.019852511Z**

Implementado e verificado (Targeted textual checks, 2026-10-27): GLOSSARY.md (Distributed validator; _Avoid_ em Instance contract e Distributed validator; Contract version e Runtime cutover atualizados), AGENTS.md:51,66, docs/metodologia.md:13,15,17,60,62, docs/distribution.md:218,242. Nenhuma ocorrência residual de 'distributed runtime', 'portable validator', 'local contract' ou 'consumer contract' nos arquivos do escopo, exceto linhas _Avoid_ e a seção histórica metodologia.md:114 (exceção aprovada). 'runtime interface' em distribution.md:314 é uso genérico. Nenhum link alterado; sem pytest (sem mudança de runtime/testes). Lateral: wik-01m5zb67c010. Pendente: aceitação humana e commit.

**2026-10-27T18:56:52.511837335Z**

Aprovado pelo requerente em 2026-10-27. Documentos de autor alinhados ao GLOSSARY.md: Distributed validator (antes Distributed runtime) e Instance contract com _Avoid_ para local/consumer contract e distributed runtime/portable validator. Vocabulário voltado ao consumidor segue no lateral wik-01m5zb67c010.
