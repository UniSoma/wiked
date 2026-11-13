---
id: wik-01m7at8kkdae-dd5k4
ticket: wik-01m7at8kkdae
title: Inventário de capacidades por maturidade
type: other
created: '2026-11-13T16:01:50.349318489Z'
updated: '2026-11-13T16:01:50.349318489Z'
---

# Inventário de capacidades por maturidade

Fontes: distribuição em `distr/agents/skills/wiked/` (v1.9.0; S/ abaixo), README.md, docs/, reports/investigacao-wiked.md; painéis da instância de referência (panorama.html, curadoria.html e tickets de especificação/aceite daquela instância). Fato, não decisão.

## Disponível hoje (distribuição)

- Setup/migração da instância via grill (S/guides/setup.md, distr/agents/commands/wiked-setup.md).
- Indexação assistida de fontes brutas: ticket + grill fechado; página por fonte com proveniência; consolidação em páginas operacionais, glossário e índices; arquivamento em raw/archive/AAAA-MM-DD_<ticket>/ (S/guides/assisted-indexing.md).
- Operational grill: humano qualificado decide; confirmação explícita antes de escrita (S/guides/grill.md).
- Preparação de contexto e modelagem: tipos de página, seções estruturadas com campos text/page e cardinalidade, autoridade externa, mapa de intenções, âncoras estáveis; separação operação atual × propostas × pendências (S/guides/authoring-context.md, modeling.md).
- Consulta só leitura com páginas consultadas e limitações (S/guides/query.md); exportação PDF/DOCX/SVG/PNG (export.md); diagramas D2 com raias por papel (d2.md).
- Pendências e propostas ligadas a tickets Knot (`pendency_tracking`, `proposal_tracking`), validadas em localização, status e vínculo (S/guides/knot.md, schema). Tickets aceitam `--external-ref` (ex.: card de plataforma externa).
- Distributed validator determinístico (S/scripts/validate_wiki.py): schema, topologia, navegação, frontmatter, referências, assets, diagramas, proveniência, citações, pendências/propostas, seções estruturadas, links externos offline, fragmentos de título. Estrutural, não semântico.
- Manutenção e revisão pós-atualização com reconhecimento registrado (S/guides/maintenance.md).
- Leitura via Docsify opcional (S/guides/docsify.md, S/viewers/index.html).
- Instance contract (wiki/wiki-structure.yaml) configura idioma, propósito, público, escopo, termos, topologia, nomes, navegação, page_types, estados, seções estruturadas, políticas de diagrama/proveniência, rastreamento e severidades.

## Em evolução (demonstrado na instância de referência, ainda não na distribuição)

- Panorama: viewer de navegação gerado em runtime no browser a partir do Markdown (árvore radial/sunburst por tronco, tamanho por palavras ou links recebidos, vizinhança, portal, busca, filtro por termos do glossário, estado na URL, integração com a nav do Docsify). Sem sinais de pendência por decisão de design.
- Painel de Curadoria: implementado e aceito; lê o Instance contract (não o Knot). Sinais: ponto de curadoria (id em Pendências/Propostas/proposal_ticket), carga (ids distintos por página, sem pesos), natureza (página em proposta, com pendências, com propostas), links recebidos (informativo). Visões: lista por tronco ordenada por carga, mapa por tronco (foco do curador), lista de itens deduplicados; contadores-filtro, busca, copiar id, abrir seção. Trata contrato ausente/versão divergente. Encaminhamento decidido pela instância: propor só a especificação ao Wiked após uso real (ticket lateral "Receber a especificação do Painel de Curadoria no Wiked").
- Genérico/reaproveitável: lógica de curadoria derivada do contrato; extração em runtime; slug compatível com Docsify; padrão de viewer derivado. Local: formato de links e deploy, troncos, tema, intenções.

## Visão / pesquisa

- Colaboração de não técnicos e ambiente padronizado (reports/investigacao-wiked.md; opções B1/P/B3); produto local (épico da opção P).
- Projeções e recuperação unificada para consulta (épico em aberto).

## Lacunas para o mapeamento consultivo (UC2)

- As-is/to-be: há operação atual × proposta e estado de proposta, mas não comparação lado a lado nem cenários versionados.
- *Source* no Wiked = proveniência documental; *data source* do negócio não tem modelo — precisaria de page_types/seções estruturadas da instância.
- Sem modelo de referência para processo, regra de negócio, sistema/dado, ferramenta, stakeholder/papel, lacuna; sem RACI.
- Sem visões agregadas na distribuição (lacuna coberta pelos painéis em evolução).
- Sem orientação específica para entrevistas/workshops e divergência entre entrevistados.
- Sem checagem de cobertura (ex.: etapa sem responsável), salvo via cardinalidade de seções estruturadas.
- Coedição pelo cliente: viável hoje por pedidos em plataforma externa ligados por external-ref e sincronizados pelo agente a pedido do curador.
