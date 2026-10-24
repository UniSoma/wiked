---
id: wik-01m5q09kwfw9
title: Decidir o papel da recuperação vetorial e híbrida na consulta
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-24T13:06:11.459713397Z'
updated: '2026-10-24T13:30:24.920932761Z'
parent: wik-01m5q079q8jz
tags:
- metodologia
- wiked
- projecoes
- embeddings
- recuperacao
- wayfinder:grilling
acceptance:
- title: Solicitante confirma decisão sobre inclusão, exclusão ou revisão da alternativa vetorial/híbrida, com classes de consulta atendidas e limites explicitados.
  done: false
- title: Evidências são comparadas aos critérios prévios; custo, manutenção e incertezas ficam registrados, sem exigir PoC desnecessária ou apresentar teste não executado como resultado.
  done: false
- title: PoCs ou pesquisas necessárias têm escopo autorizado e ativos vinculados; resultados exploratórios não são confundidos com entrega produtiva ou consistência medida.
  done: false
- title: Resolução alimenta a especificação comum sem CLI concorrente, preservando leitura canônica, rastreabilidade e limites de dados; detalhes ainda indecidíveis viram névoa ou novas perguntas precisas.
  done: false
deps:
- wik-01m5q082jdqm
---

## Question

Recuperação por similaridade vetorial, isolada ou combinada à textual, oferece ganho suficiente sobre o baseline para entrar na especificação de consulta do Wiked; em quais situações e sob quais limites?

Usar contrato e critérios definidos na decisão anterior. Comparar capacidade de encontrar Markdown com vocabulário diferente, termos exatos, ambiguidade, exceções e lacunas. Investigar recuperação, contexto, latência, custo de construção/consulta/atualização, dependências e manutenção. O menor acoplamento editorial esperado em relação ao KG é hipótese a testar, não fato já estabelecido.

A resposta deve ser adotar no desenho, ajustar e investigar mais, ou rejeitar, com justificativa e confiança compatível com a evidência. Se escolhida, especificar o necessário sobre segmentação, contexto, atualização/exclusão, cobertura e integração ao resultado comum; deixar decisões novas em tickets próprios se não couberem nesta sessão. Escolher para a especificação não significa capacidade implementada ou adoção operacional.

## Notes

Ticket wayfinder:grilling, HITL, P2; preferencialmente antes da decisão relacional P3, sem dependência técnica entre elas. Antes de trabalhar, obter claim por assignee e invocar grilling e domain-modeling. Não exigir piloto executável por princípio: executar PoC apenas se necessária para uma decisão e autorizada em recorte próprio.

Se a evidência exigir experimento, especificar ticket wayfinder:prototype com pergunta, fidelidade, orçamento, dados autorizados, ambiente, critério de parada e ativo ligado ao ticket; a resolução deste ticket aguarda a evidência relevante. Pesquisa externa precisa de ticket wayfinder:research e skill compatível antes de delegar. Não instalar ferramentas nem manipular Git. Envio de conteúdo a provedor externo não é autorizado por leitura local.

Projeção localiza; Markdown canônico sustenta a resposta. Similaridade não consolida identidade nem relações operacionais. Fixtures sintéticas são a base; consumidor real exige autorização separada. PoC não vira implementação oficial nem altera skill instalada por implicação.

Registrar resposta por nota de resolução e fechamento com resumo; indexar somente ponteiro pelo nome e síntese no mapa. No máximo uma decisão não-research resolvida por sessão.