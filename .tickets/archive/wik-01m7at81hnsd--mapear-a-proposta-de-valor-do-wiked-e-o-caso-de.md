---
id: wik-01m7at81hnsd
title: Mapear a proposta de valor do Wiked e o caso de uso de mapeamento consultivo
status: closed
type: epic
priority: 2
mode: hitl
created: '2026-11-13T16:00:58.933728582Z'
updated: '2026-11-13T22:04:33.705500691Z'
closed: '2026-11-13T22:04:33.705500691Z'
tags:
- wayfinder-map
---

## Description

### Destination

`docs/proposta_de_valor_wiked.md` escrito (em inglês, UniSoma como mantenedora formal) para público externo de negócios, apresentando o núcleo do Wiked, suas funcionalidades e casos de uso; `docs/metodologia.md` (Objective) e `GLOSSARY.md` reconhecendo formalmente os casos de uso; lacunas para o caso de mapeamento consultivo registradas como tickets próprios.

### Notes

- Exceção ao "só planejar": o mapa executa a escrita final no ticket "Escrever a proposta e ajustar o objetivo e o glossário", condicionada a ticket aprovado e fechamento explícito do Methodological grill (AGENTS.md, docs/metodologia.md).
- Resultados de pesquisa e protótipos ficam como documentos Knot anexados ao ticket (`knot document add`); nada de push nem branches `research/*`.
- Convenção de wayfinding da instância de referência: épico `wayfinder-map`, filhos `chore` com tag `wayfinder-<tipo>`, bloqueio via `knot dep`.
- Skills: grilling + domain-modeling em tickets HITL; research em tickets de pesquisa; consultar GLOSSARY.md e docs/metodologia.md.
- Casos de uso: UC1 base de conhecimento (área, projeto, produto) e UC2 mapeamento consultivo (processos as-is/to-be, data sources e lacunas, regras de negócio, ferramentas, stakeholders) são principais; UC3 contexto de negócio navegável por agentes (diferencial: IA analítica ligando contexto aos dados) e UC4 derivação de artefatos são consequências naturais, citadas explicitamente.
- Núcleo em cinco pilares: conhecimento governado; rastreabilidade; indefinição explícita (pendências/propostas em tickets); consistência estrutural (Instance contract + Distributed validator); formato aberto, progressivo e navegável por agentes. Em torno: visões derivadas (Panorama, Curadoria — inclusive mapa visual por tronco para foco do curador) e artefatos derivados.
- Três níveis de maturidade explícitos: disponível hoje / em evolução / visão. Completude = seções obrigatórias e cardinalidades + pendências explícitas; checagem de cobertura é evolução. As-is/to-be: mecanismo atual (operação atual × propostas de mudança) + comparação lado a lado em evolução.
- Distinguir *data source* (objeto de domínio da instância) de *Source* (proveniência do Wiked).
- Acompanhamento pelo cliente: vista de leitura publicada a cada incremento validado; coedição via pedidos de correção/indexação em plataforma externa (ex.: Basecamp), ligados por external-ref aos tickets e sincronizados pelo agente a pedido do curador; cliente não toca no Git.
- Documento anônimo quanto a consumidores; a instância de referência aparece apenas como tal.
- Rigor configurável: o Instance contract torna o protocolo da wiki tão fraco ou forte quanto os requisitos ativados (cardinalidades, tipos de vínculo, rastreamento), atendendo casos de uso distintos; o custo de curadoria acompanha o rigor (muitas regras de relacionamento demandam grills mais rígidos). Mensagem a explicitar na proposta.

### Decisions so far

- [Inventariar capacidades do Wiked e dos painéis da instância de referência por maturidade](wik-01m7at8kkdae): distribuição cobre governança, proveniência, pendências/propostas em tickets e validação estrutural; Panorama e Curadoria em evolução; lacunas do UC2 listadas no anexo.
- [Pesquisar práticas de wikis mantidas por LLM e de docs-as-code](wik-01m7at8kpzkx): Wiked é a versão governada do padrão LLM wiki; diferencia-se por significado decidido por humanos, proveniência, indefinição explícita e validador determinístico; complementa RAG.
- [Pesquisar governança e catálogo de dados para mapeamento de data sources](wik-01m7at8ky3xw): DMBOK + DCAT/DQV + OpenLineage; lacuna de dados como página explícita relativa ao uso; wiki complementa, não substitui, catálogo de dados.
- [Pesquisar registros de decisões e indefinições e colaboração via plataformas externas](wik-01m7at8m1h4p): registros falham ao se descolar da documentação; pendências ligadas a tickets e validadas fecham essa lacuna; pedidos via plataforma externa confirmados.
- [Pesquisar práticas de mapeamento de processos e requisitos](wik-01m7at8ktmre): cobrir SIPOC/RACI, as-is/to-be com lacunas, regras separadas do fluxo, requisitos rastreados, evidência de entrevistas; Wiked é fonte governada para BPMN/DMN, não os gera.
- [Pesquisar panorama de ferramentas adjacentes ao Wiked](wik-01m7at8m8p16): nenhuma categoria cobre o Wiked; cada uma é melhor numa parte; posicionar como complemento; fraquezas: sem UI hospedada/conectores, dependência de Git, ritmo de entrevistas.
- [Pesquisar contexto de negócio para IA analítica](wik-01m7at8m556c): BIRD (NeurIPS 2023) mostra ganho com conhecimento de negócio; estudos de fornecedores são fracos; nenhum estudo testa wiki tipo Wiked; posicionar como complemento governado de camadas semânticas, sem prometer números.
- [Prototipar Instance contract de referência para mapeamento consultivo](wik-01m7at8mcfp3): contrato ilustrativo UC2 (processo SIPOC/RACI, regra, data source, ferramenta, papel, lacuna) valida hoje; registro as-is/to-be disponível, comparação e cobertura em evolução; lacunas com caminhos opcionais compatíveis encaminhadas à consolidação.
- [Prototipar sumário e mensagens-chave da proposta de valor](wik-01m7at8mfwtv): pitch + cinco mensagens-chave, núcleo, rigor configurável, UC2 mais longo e UC1 como caso fundador; vantagem sobre RAG cru e agentes de plataformas de dados; sem modelo comercial.
- [Consolidar lacunas do caso consultivo em tickets de melhoria](wik-01m7at8mpxn6): oito tickets de melhoria avulsos (tipo de destino em campos page, vínculo inverso e cobertura, par as-is/to-be, estado de proposta, supersessão e decisores, visibilidade ao cliente, requisitos com estados, entrevistas e divergência).
- [Definir termos do glossário e redação do objetivo da metodologia](wik-01m7at8mk9db): glossário ganha casos de uso (Use case + Knowledge base, Consulting mapping, Agent-navigable business context, Derived artifact production), Derived view, Derived artifact e Source page; Objective ganha parágrafo curto com principais × consequências e rigor via Instance contract.
- [Escrever a proposta e ajustar o objetivo e o glossário](wik-01m7at8mtgq0): proposta, exemplos de base de conhecimento e de mapeamento consultivo, Objective, glossário e link no README escritos e validados; UC4 com modelos de exportação como visão e Panorama em evolução sem caminho prometido.

### Not yet specified

- Nada: as duas dúvidas restantes foram resolvidas no grill do ticket de escrita.

### Out of scope

- Material para cliente em pt-BR (derivado depois pelo requisitante).
- Implementação dos painéis, template oficial de contrato distribuído, benchmark próprio de IA, checagem de cobertura no validador.
- Recepção da especificação do Painel de Curadoria e documentação das operações de wayfinding no issue-tracker (tickets avulsos).
- Formato de engajamento comercial: a proposta não descreve modelo comercial, só convida a conversa (decidido em "Prototipar sumário e mensagens-chave da proposta de valor").

## Notes

**2026-11-13T22:04:33.705500691Z**

Mapa concluído: proposta de valor, exemplos UC1/UC2, Objective e glossário escritos; lacunas do UC2 em oito tickets de melhoria.
