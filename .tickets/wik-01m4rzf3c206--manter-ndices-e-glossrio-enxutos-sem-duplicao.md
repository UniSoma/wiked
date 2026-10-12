---
id: wik-01m4rzf3c206
title: Manter índices e glossário enxutos, sem duplicação operacional
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-12T21:14:29.633802968Z'
updated: '2026-10-12T21:14:29.633802968Z'
tags:
- metodologia
- wiked
- modelagem
- navegacao
- contexto
acceptance:
- title: Methodological grill fechado com confirmação explícita do solicitante, escopo mínimo de arquivos e exceções definidos antes de alterar conteúdo governado.
  done: false
- title: Instrução central concisa distingue glossário, índices e páginas canônicas; preserva definições essenciais e conteúdo institucional exigido no índice raiz, sem duplicação normativa entre guias.
  done: false
- title: Procedimentos afetados aplicam verificação de destino e cobertura antes de reduzir conteúdo, preservando condições, exceções, estado, proveniência e decisão humana sobre lacunas/divergências, sem limpeza incidental.
  done: false
- title: Verificação textual com exemplos sintéticos distingue definição legítima, descrição de navegação e detalhe operacional; confirma que a redução não deixa informação exclusivamente na camada de navegação nem trata links como substitutos da cobertura.
  done: false
- title: Comparação antes/depois registra tamanho das instruções e carregamentos por rota afetada; não há novos carregamentos obrigatórios nem leitura integral adicional, e qualquer crescimento textual necessário é mínimo e justificado ao solicitante.
  done: false
- title: Verificações textuais confirmam coerência com query, setup e papéis do contrato, links válidos, instruções genéricas em inglês e ausência de dependência de docs/ ou de conteúdo de consumidor na distribuição; evidências registradas no ticket.
  done: false
---

## Description

### Objetivo
Melhorar os procedimentos de autoria, indexação assistida e manutenção para evitar que índices e o contexto/glossário acumulem descrições operacionais que pertencem às páginas canônicas. Preservar navegação progressiva, vocabulário canônico e cobertura informacional, sem inchar a skill nem aumentar desnecessariamente o contexto carregado pelos agentes.

### Motivação e diagnóstico
Uma observação externa relatou um contexto de 273 linhas, carregado em toda consulta, com verbetes que também desenvolvem responsabilidades, condições e regras presentes em páginas canônicas. Esse relato é motivação, não evidência verificada nem requisito de domínio. Na distribuição atual, query.md separa vocabulário de evidência operacional e modeling.md exige navegação progressiva, mas faltam critérios positivos e concisos sobre o conteúdo apropriado a índices e glossário e sua revisão durante a consolidação.

### Direção proposta, sujeita ao grill
Distinguir definição terminológica, orientação de navegação e descrição operacional. O glossário deve conservar definição, distinções essenciais, sinônimos/termos a evitar e links pertinentes; uma responsabilidade mínima pode ser necessária para definir um papel. Índices devem orientar a escolha de destinos com agrupamentos e descrições breves, sem substituir páginas canônicas. Preservar título, propósito, público e escopo exigidos no índice raiz.
Usar um teste editorial simples: o trecho esclarece um termo/seleciona um destino ou descreve como a operação funciona? Na segunda hipótese, verificar o destino canônico. Antes de remover detalhes, conferir cobertura, condições, exceções, estado e proveniência; lacunas e divergências exigem decisão humana. Não criar páginas ou ampliar uma limpeza incidentalmente.

### Restrição expressa do solicitante
Não inchar os arquivos da skill nem carregar excessivamente o contexto dos agentes nas wikis. Preferir substituir ou ajustar instruções existentes, uma regra central breve e remissões mínimas apenas onde necessárias. Não replicar a regra em cada guia, criar guia adicional por padrão ou adicionar leitura integral/obrigatória. Comparar o tamanho das instruções e o percurso de carregamento antes/depois; justificar qualquer aumento necessário. Não impor limites arbitrários de linhas nem divisão automática de arquivos como substituto da revisão semântica.

### Superfície inicial de avaliação
Regra principal em distr/agents/skills/wiked/guides/modeling.md; avaliar somente os ajustes necessários em maintenance.md, assisted-indexing.md, query.md e setup.md. Não presumir alteração em todos esses arquivos. Verificar coerência com papéis configurados no contrato antes de qualquer regra geral sobre índices e evidência.

### Governança e exclusões
A criação deste ticket registra trabalho futuro, não fecha o Methodological grill nem autoriza alteração de instruções. Antes da implementação, confirmar escopo e aceite com o solicitante e fechar explicitamente o grill conforme docs/metodologia.md. Não operar ou limpar consumidor, alterar contrato/runtime, implementar heurísticas semânticas automáticas, manipular Git, publicar ou instalar ferramentas como parte deste ticket. Nenhum consumidor real deve virar fixture ou requisito genérico.
