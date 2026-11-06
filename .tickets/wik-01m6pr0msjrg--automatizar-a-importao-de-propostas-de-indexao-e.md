---
id: wik-01m6pr0msjrg
title: Automatizar a importação de propostas de indexação e a geração de pacotes portáteis
status: open
type: feature
priority: 4
mode: hitl
created: '2026-11-05T20:57:10.636157085Z'
updated: '2026-11-05T20:57:10.636157085Z'
tags:
- metodologia
- wiked
- indexacao
- proposta
- implementacao-futura
acceptance:
- title: Methodological grill fechado e decomposição em etapas decidida, com dependências coerentes
  done: false
- title: Importador determinístico sem Git rejeita proposta sem snapshot_id, com fontes ausentes ou excedentes ou com formato inválido, marca decisões desatualizadas, verifica trechos literais e posiciona fontes sem sobrescrever
  done: false
- title: Gerador de pacote determinístico byte a byte, sem saída parcial nem datas, com manifesto de identificação e hashes por arquivo e subconjunto de guias decidido
  done: false
- title: Localização dos perfis de adaptador decidida e ao menos um ambiente avaliado ponta a ponta em escopo de Behavioral evaluation aprovado
  done: false
- title: uv run pytest verde com fixtures sintéticas; manifesto, CHANGELOG e documentação atualizados
  done: false
deps:
- wik-01m6pr00hwgd
links:
- wik-01m2tpkz9x55
- wik-01m4vhpp3xyt
---

## Description

### Contexto

O ticket wik-01m6pr00hwgd especifica a proposta de indexação: um artefato Markdown com frontmatter YAML, produzido num chatbot de nuvem (Gemini Gem, ChatGPT, Claude Project) por um informante não qualificado, durante um pré-grill somente leitura. O guia `guides/proposal.md` e a entrada de importação manual no `guides/assisted-indexing.md` também ficam naquele ticket. Lá, a proposta traz decisões propostas (com categoria, origem e páginas afetadas), um plano de destino sem texto final, a linhagem (`snapshot_id`, `methodology_version`, `proposal_version`) e a lista de fontes entregues junto. O operador qualificado importa a proposta com ticket aberto e fecha o grill normalmente.

Este ticket agrega a automação que lá ficou fora de escopo. A divisão em etapas fica para quando o trabalho for executado.

### Escopo agregado (da proposta original)

1. `scripts/import_proposal.py`: determinístico, sem Git e sem modelo. Recebe a proposta e as fontes por qualquer canal e:
   - valida o formato e os campos obrigatórios;
   - confere que cada fonte listada foi recebida e que não sobra fonte recebida fora da lista;
   - calcula os hashes das fontes no recebimento;
   - compara as páginas afetadas da instância atual com os hashes do manifesto do snapshot;
   - posiciona as fontes em `raw/<slug>/` sem sobrescrever destinos existentes;
   - emite um relatório (`valid`, `stale in Dn…` ou `invalid: reasons`) para o agente do operador abrir o ticket e iniciar a importação.
2. `scripts/build_portable.py`: gera, a partir de uma instância e de uma revisão, um pacote neutro quanto ao ambiente, com:
   - snapshot de `wiki/`;
   - manifesto (identificação, hashes por arquivo, `methodology_version`, `contract_version`);
   - os guias aplicáveis aos modos consulta e proposta, conforme o subconjunto decidido em wik-01m6pr00hwgd;
   - o formato da proposta e instruções neutras.

   Garantias: determinismo byte a byte, falha sem saída parcial e nenhuma data gravada. O manifesto é a peça de linhagem compartilhada; outros consumidores, como bots de consulta com snapshot embarcado, podem adotá-lo.
3. Perfis de adaptador por ambiente (limites de anexos e tamanho, agrupamento de arquivos, texto de instruções). Recomendação da revisão: o Wiked mantém o pacote neutro e um esquema de declaração de limites; os perfis concretos ficam fora da distribuição manifestada, porque mudam conforme o fornecedor. Relaciona-se com a arquitetura de skills opcionais (wik-01m2tpkz9x55).
4. Avaliação ponta a ponta em ao menos um ambiente (Gemini Gem): consulta, pré-grill, proposta, importação e fechamento. É uma Behavioral evaluation dependente de modelo e harness, com escopo, cenários e limites de custo próprios (ver wik-01m4vhpp3xyt), não uma prova determinística.

### Achados da revisão metodológica (2026-11-05) a resolver no grill

- "Never manipulate Git": o `snapshot_id` não deve exigir leitura do Git pelos scripts. Recomendação: digest do manifesto de conteúdo; o operador guarda fora de `wiki/` os manifestos dos pacotes que emitiu, e o commit entra só como informação.
- O importador precisa obter o manifesto correspondente ao `snapshot_id` que a proposta cita. Definir onde ele fica guardado e o que acontece quando não for encontrado.
- A desatualização baseada só em páginas afetadas (lista feita pelo chatbot) é insuficiente. O relatório deve listar todos os arquivos alterados desde o snapshot, incluindo context file e índices, e deixar claro que "valid" não prova que a proposta está atual.
- Verificação determinística recomendada: conferir se cada trecho literal com origem "fonte" existe na fonte (formatos textuais), para medir a fidelidade do chatbot. Os hashes no recebimento só ligam o que o operador recebeu ao que será arquivado.
- Posicionar arquivos em `raw/` antes do ticket deve ser compatível com o Entry do `assisted-indexing` ("do not access a source or change the wiki" antes de ticket e grill). A proposta é arquivada com as fontes e não gera página de fonte.
- A saída do pacote fica fora de `wiki/`. Publicar o pacote num serviço de terceiros é decisão humana do consumidor.
- Scripts novos entram no manifesto (componente runtime) ou num componente opcional, conforme a decisão de wik-01m2tpkz9x55. Mudanças de runtime exigem `uv run pytest` com fixtures sintéticas.
- Possível sobreposição com o núcleo determinístico do épico wik-01m4k2eg642n (seleção, plano, diff). Verificar antes de implementar.
