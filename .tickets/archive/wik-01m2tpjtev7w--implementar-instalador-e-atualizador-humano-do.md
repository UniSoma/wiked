---
id: wik-01m2tpjtev7w
title: Implementar instalador e atualizador humano do Wiked
status: closed
type: feature
priority: 2
mode: afk
created: '2026-09-18T16:46:19.574642249Z'
updated: '2026-10-12T23:21:58.187022996Z'
closed: '2026-10-12T23:00:47.607223790Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- setup
acceptance:
- title: Instalador seleciona e fixa última release estável, valida artefatos e registra versão/inventário/hashes; publicação real não é necessária aos testes
  done: true
- title: Linux/macOS/WSL e requisitos de shell/utilitários documentados; ausência de uv ou knot impede instalação; ferramentas externas e Git/Knot não são instalados/inicializados
  done: true
- title: Destino padrão e personalizado preservam árvore; referência ao manifesto é relocável e instruções explicam descoberta pelo agente
  done: true
- title: Simulação, confirmação, sobrescritas locais aprovadas, colisões explícitas e preservação de terceiros/obsoletos seguem docs/distribution.md
  done: true
- title: Runtime candidato expõe validação somente do contrato; incompatibilidade bloqueia substituição e oferece ticket HITL P1 confirmado apenas no tracker local
  done: true
- title: Concorrência, falhas parciais e interrupções têm backup temporário, restauração e recuperação testados; mesma versão íntegra é no-op e alterações permitem reinstalação aprovada
  done: true
- title: Contrato e conteúdo da wiki permanecem intactos; conclusão orienta setup sem iniciar agente; uv run pytest passa com cobertura sintética sem modificar host
  done: true
deps:
- wik-01m2tphwrc4f
links:
- wik-01m4s6rgnfhr
---

## Description

Implementar o contrato aprovado em docs/distribution.md, encerrado explicitamente pelo solicitante no grill de wik-01m2tphwrc4f em 2026-10-10. Entrega anterior à primeira publicação: instalador Bash determinístico testado com releases sintéticas, sem depender de release pública. Linux/macOS e Windows via WSL. Resolver a última release estável oficial uma vez por execução; fixar e registrar versão, validar SHA-256 via HTTPS antes de extrair ou escrever. Não oferecer versões antigas nesta entrega. Exigir uv e knot previamente disponíveis; não instalar ferramentas, inicializar Git/Knot ou exigir todos os conversores. Executar a partir da raiz do consumidor com destino padrão .agents ou destino informado preservando árvore relativa; separar raiz do consumidor do destino, corrigir referência fixa ao manifesto e documentar descoberta manual em destinos alternativos. Expor no runtime validação pública somente do contrato; usar o runtime candidato antes da substituição, sem duplicar regras em Bash, consultar tracker ou validar páginas. Incompatibilidade impede atualização; oferecer ticket HITL P1 somente com confirmação e tracker local, sem fallback ancestral. Planejar adições/substituições/remoções, oferecer simulação e confirmação ou aprovação não interativa explícita. Identificar modificações pela baseline da instalação anterior; sem baseline, alertar genericamente. Alterações locais podem ser sobrescritas com aprovação; colisões sem propriedade anterior exigem aprovação específica. Preservar terceiros e remover obsoletos somente com propriedade e integridade comprovadas. Metadados Wiked registram versão, arquivos e hashes. Preparar antes da escrita, impedir concorrência, backup temporário, restauração em falhas tratáveis e recuperação obrigatória de interrupções. Versão atual íntegra não altera nada; modificada/incompleta oferece reinstalação. Não modificar contrato/wiki; término orienta setup assistido sem iniciar agente. Implementar testes sintéticos e executar uv run pytest; não instalar ferramentas no host, manipular Git ou substituir skill em uso. Preparar interface de empacotamento consumível pelo executor de publicação. O contrato é completo para execução; nova decisão substantiva exige retomar HITL e o workflow autoral.

## Notes

**2026-10-10T18:40:23.994085344Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-12T22:48:03.015865597Z**

Grill metodológico encerrado explicitamente pelo solicitante em 2026-10-12: confirmou e autorizou instalador/atualizador Bash, validação pública somente do contrato, referência relocável, documentação e testes sintéticos. Escopo: scripts/install-wiked.sh, tests/test_wiked_installer.py, runtime/README e SKILL.md distribuídos, tests/test_wiked_validator.py e README.md. Sem publicação, ferramentas novas no host, Git, instalação em consumidor ou alteração de versão/inventário. Endereço oficial e versão final permanecem na preparação da publicação.

**2026-10-12T23:00:38.548386889Z**

Implementação concluída no escopo autorizado: scripts/install-wiked.sh autocontido, seleção estável fixada por execução, HTTPS/SHA-256 antes da extração, manifesto exato e metadados de baseline, planos/dry-run/aprovações explícitas, destinos relocáveis, preservação de terceiros e obsoletos modificados, validação --contract-only pelo candidato, ticket P1 HITL com confirmação separada e prova de tracker local via knot info, lock POSIX, backups/journal e recuperação obrigatória. README documenta ferramentas, integridade do instalador, interface de empacotamento e descoberta manual. Versão 1.4.0 e inventário de 16 arquivos preservados. Evidências: uv run pytest --basetemp=/tmp/opencode/wiked-installer-validation => 67 passed, 1 skipped (integração externa opcional); bash -n scripts/install-wiked.sh => sucesso. Cobertura sintética inclui uv real, projeto consumidor inválido não alterado, no-op, reinstalação, colisões, downgrade bloqueado, tar inseguro/checksum, wiki intacta, ausência de ferramentas, falhas parciais e após metadados, SIGKILL/recuperação, backups corrompidos, concorrência e redirecionamento externo do tracker. Nenhuma publicação, instalação em consumidor real, manipulação de Git ou substituição de skill em uso. Endereço oficial, licença, artefatos e aprovação final de release pertencem a wik-01m4khsrmqya.

**2026-10-12T23:00:47.607223790Z**

Entregues instalador/atualizador humano autocontido, validação pública somente do contrato, referências relocáveis, documentação e interface de release. Sete critérios atendidos com 67 testes aprovados e uma integração externa opcional ignorada; sintaxe Bash validada. Publicação e endereço oficial permanecem no executor separado; nenhum consumidor real ou Git foi alterado.
