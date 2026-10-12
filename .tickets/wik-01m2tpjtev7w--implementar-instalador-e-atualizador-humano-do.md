---
id: wik-01m2tpjtev7w
title: Implementar instalador e atualizador humano do Wiked
status: open
type: feature
priority: 2
mode: afk
created: '2026-09-18T16:46:19.574642249Z'
updated: '2026-10-10T23:29:42.810389980Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- setup
acceptance:
- title: Instalador seleciona e fixa última release estável, valida artefatos e registra versão/inventário/hashes; publicação real não é necessária aos testes
  done: false
- title: Linux/macOS/WSL e requisitos de shell/utilitários documentados; ausência de uv ou knot impede instalação; ferramentas externas e Git/Knot não são instalados/inicializados
  done: false
- title: Destino padrão e personalizado preservam árvore; referência ao manifesto é relocável e instruções explicam descoberta pelo agente
  done: false
- title: Simulação, confirmação, sobrescritas locais aprovadas, colisões explícitas e preservação de terceiros/obsoletos seguem docs/distribution.md
  done: false
- title: Runtime candidato expõe validação somente do contrato; incompatibilidade bloqueia substituição e oferece ticket HITL P1 confirmado apenas no tracker local
  done: false
- title: Concorrência, falhas parciais e interrupções têm backup temporário, restauração e recuperação testados; mesma versão íntegra é no-op e alterações permitem reinstalação aprovada
  done: false
- title: Contrato e conteúdo da wiki permanecem intactos; conclusão orienta setup sem iniciar agente; uv run pytest passa com cobertura sintética sem modificar host
  done: false
deps:
- wik-01m2tphwrc4f
---

## Description

Implementar o contrato aprovado em docs/distribution.md, encerrado explicitamente pelo solicitante no grill de wik-01m2tphwrc4f em 2026-10-10. Entrega anterior à primeira publicação: instalador Bash determinístico testado com releases sintéticas, sem depender de release pública. Linux/macOS e Windows via WSL. Resolver a última release estável oficial uma vez por execução; fixar e registrar versão, validar SHA-256 via HTTPS antes de extrair ou escrever. Não oferecer versões antigas nesta entrega. Exigir uv e knot previamente disponíveis; não instalar ferramentas, inicializar Git/Knot ou exigir todos os conversores. Executar a partir da raiz do consumidor com destino padrão .agents ou destino informado preservando árvore relativa; separar raiz do consumidor do destino, corrigir referência fixa ao manifesto e documentar descoberta manual em destinos alternativos. Expor no runtime validação pública somente do contrato; usar o runtime candidato antes da substituição, sem duplicar regras em Bash, consultar tracker ou validar páginas. Incompatibilidade impede atualização; oferecer ticket HITL P1 somente com confirmação e tracker local, sem fallback ancestral. Planejar adições/substituições/remoções, oferecer simulação e confirmação ou aprovação não interativa explícita. Identificar modificações pela baseline da instalação anterior; sem baseline, alertar genericamente. Alterações locais podem ser sobrescritas com aprovação; colisões sem propriedade anterior exigem aprovação específica. Preservar terceiros e remover obsoletos somente com propriedade e integridade comprovadas. Metadados Wiked registram versão, arquivos e hashes. Preparar antes da escrita, impedir concorrência, backup temporário, restauração em falhas tratáveis e recuperação obrigatória de interrupções. Versão atual íntegra não altera nada; modificada/incompleta oferece reinstalação. Não modificar contrato/wiki; término orienta setup assistido sem iniciar agente. Implementar testes sintéticos e executar uv run pytest; não instalar ferramentas no host, manipular Git ou substituir skill em uso. Preparar interface de empacotamento consumível pelo executor de publicação. O contrato é completo para execução; nova decisão substantiva exige retomar HITL e o workflow autoral.

## Notes

**2026-10-10T18:40:23.994085344Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.
