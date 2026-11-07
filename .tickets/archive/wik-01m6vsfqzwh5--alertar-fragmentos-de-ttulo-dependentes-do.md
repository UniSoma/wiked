---
id: wik-01m6vsfqzwh5
title: Alertar fragmentos de título dependentes do renderizador e orientar âncoras explícitas
status: closed
type: feature
priority: 2
mode: hitl
created: '2026-11-07T19:59:06.235853752Z'
updated: '2026-11-07T23:53:46.168731320Z'
closed: '2026-11-07T23:53:46.168731320Z'
tags:
- validator
- docsify
- modeling
acceptance:
- title: Methodological grill encerrado com confirmação explícita do escopo e das decisões
  done: true
- title: Sem a nova regra no contrato, a saída do validador é idêntica à da 1.8.0
  done: true
- title: Com a regra ativa, fixtures sintéticas cobrem fragmento resolvido só por slug de título (aviso) e por âncora explícita (sem aviso)
  done: true
- title: Schema, checagem de versão mínima, guias e CHANGELOG atualizados em inglês, sem conhecimento de consumidor
  done: true
- title: uv run pytest passa e evidências registradas no ticket
  done: true
---

## Description

Origem: proposta recebida de uma wiki consumidora («Proposta Wiked: divergência de slug de âncoras», https://claude.ai/artifact/V77t2ySMSsRrjpyfqz6hrM) e revisão metodológica de 2026-11-07.

Problema: o validador (`validate_wiki.py` `heading_data`) aceita fragmentos pelo slug de título ASCII (NFKD, `[a-z0-9 -]`), enquanto Docsify 4.13.1 e GitHub preservam acentos e outros caracteres. Links aprovados abrem a página no topo, sem erro. O slug também é calculado sobre o Markdown inline bruto (ex.: título com link diverge mesmo em inglês). `docsify.md` já trata `<a id>` como alvo portável só para diagramas e declara que links comuns permanecem Markdown comum.

Escopo inicial (a qualificar no Methodological grill):
- Regra opcional de contrato para fragmentos entre páginas resolvidos apenas por slug de título (critério de disparo a decidir: heurística por caracteres vs. qualquer slug de título).
- Schema, checagem de `methodology_version` mínima e diagnóstico.
- Orientação em `modeling.md` para âncoras explícitas ASCII `snake_case`.
- Registro da divergência em `docsify.md`; papel do resolvedor Docsify (exemplo opcional, transitório ou descartado) a decidir.
- Entrada de revisão no CHANGELOG e versão do manifesto.

Fora de escopo: alterar o algoritmo de slug existente; editar qualquer wiki consumidora; fixtures de consumidor real.

Achados da revisão a resolver: contradição entre resolvedor e âncoras explícitas; definição incompleta de slug não portável (`_`, hífens nas pontas, links no título, dígito inicial); critérios de aceitação devem usar fixtures sintéticas.

## Notes

**2026-11-07T23:05:20.831802660Z**

Methodological grill encerrado em 2026-11-07 com confirmação explícita do requerente.
Versão: 1.9.0 única (minor).
Decisões: (1) slug sobre texto renderizado (text/code_inline, inclusive dentro de links/ênfase; softbreak = espaço; imagens e HTML inline excluídos), resto do algoritmo inalterado; (2) regra opcional rules.heading_fragments (severidade $defs/rule, mínimo 1.9.0 via contract.relation), diagnóstico reference.heading_fragment para todo fragmento Markdown resolvido só por slug de título (mesma página, entre páginas, mapa de intenções), nunca para <a id> ou .svg; (3) resolvedor Docsify no template em bloco próprio, mesma regra de slug sobre textContent, só cria id ausente e diferente do id Docsify, origem 1.9.0, testes JS; (4) docsify.md ampliado para Optional Docsify Integration, seção de fragmentos de título, aceitação no navegador ampliada, roteamento em SKILL.md; (5) modeling.md: seção sobre fragmentos de título preferindo <a id> ASCII snake_case; (6) CHANGELOG 1.9.0 - review com Required (fragmentos agora reportados) e Optional adoption (regra; resolvedor para quem já usa Docsify).
Limites: fixtures sintéticas, inglês, sem testes de prosa, nenhuma wiki consumidora editada. Pendências laterais: nenhuma.

**2026-11-07T23:36:46.797484742Z**

Implementação no branch feature/heading-fragments (sem commit).
Evidências:
- uv run pytest: suíte completa passa (1 skip: D2 não instalado).
- WIKED_BROWSER_TESTS=1 uv run pytest tests/test_wiked_docsify.py -k browser: passa com Docsify 4.13.1 real (Chromium headless): link entre entradas para título acentuado e repetido (-1) alcança a seção, recarregamento, diagramas sem regressão, e sem o resolvedor o slug Wiked não tem alvo.
- Paridade resolvedor JS × validador: tests/test_wiked_docsify.py::test_heading_resolver_slugs_are_validator_targets.
- Verificações textuais: âncoras #heading-fragments em modeling.md e docsify.md existem; sem dependência de docs/; exemplo do guia neutro (Résumé).
AC 2 interpretado conforme o grill: sem a regra, a saída só difere pela correção do slug por texto visível (decisão Q4b).
Manifesto: distribution_version 1.9.0 (versão escolhida pelo requerente); fixture de versão futura em test_wiked_validator.py movida para 1.10.0.
Pendência lateral: no Docsify, um fragmento abaixo de um diagrama clicável pode parar antes da seção num render novo, porque a rolagem do Docsify ocorre antes da inserção assíncrona do diagrama; ids nativos do Docsify e âncoras explícitas sofrem o mesmo deslocamento. Pré-existente; registrado como limitação na aceitação do navegador (docsify.md item 8). Candidato a ticket próprio no adaptador de diagramas.

**2026-11-07T23:52:42.683102460Z**

Prova externa (cópia da Reference instance de origem, sem editar o consumidor): validador 1.9.0 sem a regra produz diagnósticos idênticos aos da 1.8.0 (0 erros, 0 avisos, 105 arquivos); nenhum título do consumidor contém link, imagem, HTML ou dígito inicial, então a correção do slug não tem efeito ali. Com rules.heading_fragments (1.9.0) ativa: 42 avisos reference.heading_fragment, batendo com o inventário do consumidor (44 links ancorados menos 2 por âncora explícita). O plugin local do consumidor usa o mesmo hook (afterEach) e o mesmo slug sobre textContent do resolvedor distribuído; diferenças: o distribuído ignora títulos em HTML bruto, converte quebra de linha em espaço e analisa o HTML num <template> inerte.

**2026-11-07T23:53:46.168731320Z**

Wiked 1.9.0: slug de título pelo texto visível; regra opcional rules.heading_fragments (reference.heading_fragment, mínimo 1.9.0); resolvedor de fragmentos de título no template Docsify; guias docsify.md, modeling.md, SKILL.md, contracts/README.md e CHANGELOG atualizados; manifesto em 1.9.0. Validado por uv run pytest, teste de navegador com Docsify 4.13.1 e prova externa na Reference instance de origem. Implementação no branch feature/heading-fragments, sem commit.
