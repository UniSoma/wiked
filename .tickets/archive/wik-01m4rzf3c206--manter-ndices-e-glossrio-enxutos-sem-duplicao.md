---
id: wik-01m4rzf3c206
title: Manter índices e glossário enxutos, sem duplicação operacional
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-12T21:14:29.633802968Z'
updated: '2026-10-13T16:40:39.688296490Z'
closed: '2026-10-13T16:40:39.688296490Z'
tags:
- metodologia
- wiked
- modelagem
- navegacao
- contexto
acceptance:
- title: Methodological grill fechado com confirmação explícita do solicitante, escopo mínimo de arquivos e exceções definidos antes de alterar conteúdo governado.
  done: true
- title: Instrução central concisa distingue glossário, índices e páginas canônicas; preserva definições essenciais e conteúdo institucional exigido no índice raiz, sem duplicação normativa entre guias.
  done: true
- title: Procedimentos afetados aplicam verificação de destino e cobertura antes de reduzir conteúdo, preservando condições, exceções, estado, proveniência e decisão humana sobre lacunas/divergências, sem limpeza incidental.
  done: true
- title: Verificação textual com exemplos sintéticos distingue definição legítima, descrição de navegação e detalhe operacional; confirma que a redução não deixa informação exclusivamente na camada de navegação nem trata links como substitutos da cobertura.
  done: true
- title: Comparação antes/depois registra tamanho das instruções e carregamentos por rota afetada; não há novos carregamentos obrigatórios nem leitura integral adicional, e qualquer crescimento textual necessário é mínimo e justificado ao solicitante.
  done: true
- title: Verificações textuais confirmam coerência com query, setup e papéis do contrato, links válidos, instruções genéricas em inglês e ausência de dependência de docs/ ou de conteúdo de consumidor na distribuição; evidências registradas no ticket.
  done: true
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

## Notes

**2026-10-13T16:36:58.275881054Z**

Methodological grill fechado: solicitante confirmou explicitamente o resumo final e autorizou implementação. Escopo instrucional: modeling.md (regra central de glossário/índices, cobertura segura e ordem alfabética dentro de agrupamentos úteis com exceções semânticas), assisted-indexing.md (aplicação na consolidação), maintenance.md (revisão/correção governada que pode abranger outras ou novas páginas e ficar para ticket posterior), setup.md (atualização pertinente pode motivar conferência via manutenção, sem autorizar correção/migração). Preservar definições essenciais, conteúdo institucional da raiz, topologia/papéis do contrato, condições, exceções, estado e proveniência. Sem consumidor, runtime/schema, novo guia, carregamento obrigatório adicional, limites arbitrários ou limpeza incidental. Validar por checks textuais/exemplos sintéticos e comparação de tamanho/carregamentos. Pendência lateral excluída: encaminhamento do instalador após atualização.

**2026-10-13T16:40:27.580755708Z**

Implementação concluída no escopo aprovado, somente instruções:
- guides/modeling.md: substituída orientação mínima de termos por critérios centrais de glossário, índice, página canônica, preservação institucional, ordem alfabética dentro de grupos com exceção semântica aprovada e cobertura antes de redução (condições, exceções, estado, proveniência). Link não comprova cobertura; lacunas/divergências humanas; preservar informação sem destino e não ampliar limpeza.
- guides/assisted-indexing.md: consolidação explícita de páginas operacionais antes do contexto/índices, aplicando regra central.
- guides/maintenance.md: aplicação da regra na revisão e correção governada que pode criar/revisar páginas no escopo confirmado ou ficar para ticket posterior.
- guides/setup.md: atualização humana pertinente pode motivar conferência via manutenção, sem autorizar correção/migração.
Query e SKILL inalterados; manifesto, schema/runtime e consumidores não alterados. Pendência lateral de encaminhamento do instalador permanece excluída.

Verificação textual (Node, sem Python/runtime): 45 checks passaram. Cobriram presença das regras, remissões válidas aos guias, arquivos manifestados, ASCII/inglês genérico, ausência de docs/, identidade autor/consumidor preservada no SKILL inalterado, papéis de evidência do contrato e de query, campos institucionais coerentes com schema initial_content, bootstrap preservado e diretivas explícitas de carregamento inalteradas. Revisão editorial independente confirmou ausência de bloqueios, sem algoritmo semântico.

Exemplos sintéticos revisados manualmente:
1. Reviewer definido pela responsabilidade mínima, distinto de requester, com sinônimo e link: conservar no glossário.
2. Prazo de dois dias, urgência com dois reviewers, exceção em outage e estado proposto; destino apenas 'Review requests': conservar informação e resolver cobertura, não remover.
3. Entrada 'Requests — submission and review workflow' com link: descrição legítima de navegação.
4. Procedimento no índice e destino com cobertura integral de condições/exceções/estado/proveniência: redução possível após governança, não automática.
5. Link isolado: não comprova cobertura nem autoriza retirar informação do contexto.
6. Título/propósito/público/escopo na raiz: conservar.
7. Divergência índice/página: resolver com humano antes de apagar.
8. Intake/Review agrupados, entradas alfabéticas dentro de cada grupo: válido; Collect->Assess->Decide aprovado pode prevalecer.
9. Atualização Wiked: revisão opcional, sem correção/migração automática.
10. Destino inexistente: preservar informação; correção pode criar página no escopo confirmado ou ficar para ticket posterior.

Comparação antes/depois (linhas / palavras / bytes; wc):
SKILL: 50/554/4079 -> igual.
query: 28/258/1718 -> igual.
modeling: 46/442/3145 -> 49/569/4127.
maintenance: 20/189/1377 -> 22/230/1668.
assisted-indexing: 42/465/3314 -> 42/469/3364.
setup: 22/400/2910 -> 24/426/3123.
Total dos seis: 208/2308/16543 -> 215/2506/18079 (+7 linhas, +198 palavras, +1536 bytes). Crescimento mínimo justificado: +127 palavras para critérios/segurança centrais, +41 para aplicação e tratativa posterior na manutenção, +4 na consolidação da indexação, +26 para gatilho opcional no setup; sem regra duplicada em cada guia.

Carregamentos por rota (apenas instruções, não conteúdo da wiki; incluindo SKILL e guias existentes):
Consulta [SKILL,query]: 78/812/5797 -> igual.
Indexação [SKILL,assisted-indexing,knot,modeling,grill]: 225/2376/16661 -> 228/2507/17693.
Revisão estrutural [SKILL,maintenance,modeling]: 116/1185/8601 -> 121/1353/9874.
Correção [anteriores,grill]: 160/1742/12272 -> 165/1910/13545.
Setup [SKILL,setup,grill,knot]: 159/1869/13112 -> 161/1895/13325.
Nenhum novo guia obrigatório, preload ou leitura integral adicional. A inspeção direcionada do destino afetado é necessária à cobertura; revisão pós-atualização é opcional e usa rota existente. Não executado pytest: alteração exclusivamente instrucional, validada pela rota textual definida em docs/metodologia.md.

**2026-10-13T16:40:39.688296490Z**

Protocolos de glossário e índices enxutos implementados nos quatro guias aprovados, com cobertura segura, ordenação alfabética dentro de agrupamentos e conferência opcional após atualização. Seis critérios atendidos; 45 checks textuais e 10 exemplos sintéticos revisados, sem novos carregamentos obrigatórios ou operação em consumidor. Evidências e comparação de tamanho/carregamentos registradas.
