---
id: wik-01m7at8mcfp3
title: Prototipar Instance contract de referência para mapeamento consultivo
status: closed
type: chore
priority: 2
mode: hitl
created: '2026-11-13T16:01:18.223315490Z'
updated: '2026-11-13T16:59:38.323525380Z'
closed: '2026-11-13T16:59:38.323525380Z'
parent: wik-01m7at81hnsd
tags:
- wayfinder-prototype
deps:
- wik-01m7at8kkdae
- wik-01m7at8ktmre
- wik-01m7at8ky3xw
assignee: VolneiSantos
---

## Description

### Question

Como seria um Instance contract de exemplo para o UC2 (processos as-is/to-be, regras de negócio, data sources, ferramentas, stakeholders/papéis, lacunas), e o mecanismo atual de operação atual × propostas basta para o caso? Rascunho anexado, apenas ilustrativo.

## Notes

**2026-11-13T16:59:38.180978802Z**

Resolução (protótipo validado com o requisitante):
- Q1: modelo aceito como referência ilustrativa do UC2: tipos process (SIPOC + Activities/RACI, papel flow com diagrama), business_rule, data_source, analytical_tool, role, gap; entrevista como source; requisitos rastreados ficam como evolução.
- Resposta: mecanismo atual basta para registrar as-is/to-be com governança (disponível hoje); comparação lado a lado e garantias de cobertura são evolução. Validado com 0 erros no validador v1.9.0.
- Q2: lacunas confirmadas, com caminhos compatíveis com legado sugeridos pelo requisitante: (1) tipo/tronco de destino opcional em campos page de seções estruturadas, além de flag nullable; (2) flag opcional de link-back: exigir que a página destino cite a origem (qualquer citação); (3) to-be via seção estruturada opcional no processo exigindo link para outro processo, restrito por tipo (vide 1). Lacuna 4 (estado de proposta exigido em todos os tipos do papel) registrada sem caminho definido.
- Q3: a proposta exibe trecho curto de contrato e página de exemplo, anônimo, em inglês, marcado como ilustrativo, sem template oficial.
Protótipo: documento anexo "Protótipo: Instance contract de referência para mapeamento consultivo".

**2026-11-13T16:59:38.323525380Z**

Contrato de referência UC2 validado; registro as-is/to-be disponível hoje, comparação e cobertura em evolução; lacunas com caminhos compatíveis encaminhadas.
