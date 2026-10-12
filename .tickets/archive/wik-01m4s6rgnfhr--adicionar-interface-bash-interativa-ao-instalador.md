---
id: wik-01m4s6rgnfhr
title: Adicionar interface Bash interativa ao instalador humano do Wiked
status: closed
type: feature
priority: 2
mode: afk
created: '2026-10-12T23:21:58.187022996Z'
updated: '2026-10-12T23:28:08.603431618Z'
closed: '2026-10-12T23:28:08.603431618Z'
acceptance:
- title: Bash conduz parâmetros ausentes e confirmações no terminal, preserva argumentos explícitos e confirma somente a última estável
  done: true
- title: Python mantém validação, seleção estável fixada, plano e transação; aprovações de plano, colisões e migração permanecem distintas
  done: true
- title: Automação sem terminal usa parâmetros e aprovações explícitos; curl via pipe é coberto com terminal sintético
  done: true
- title: README apresenta execução direta primeiro e opção verificada depois; contrato registra exceção e uv run pytest passa sem alteração de consumidores reais
  done: true
links:
- wik-01m2tpjtev7w
---

## Description

Grill metodológico encerrado explicitamente pelo solicitante em 2026-10-12 (aprovado). Evolução de wik-01m2tpjtev7w: encorpar Bash existente como interface humana; perguntar parâmetros ausentes, validar fornecidos, confirmar somente última estável e destino; apresentar plano Python antes de aprovação; terminal /dev/tty para execução via pipe; automação fornece argumentos e aprovações explícitas sem prompts. Preservar aprovações separadas para colisões e migração, compatibilidade, integridade, ownership e recuperação. README mostra execução curl | bash primeiro e download verificado depois, com exceção explícita para execução do próprio script não verificado. Endereço oficial permanece pendente do executor de publicação. Escopo autorizado: scripts/install-wiked.sh, tests/test_wiked_installer.py, README.md, docs/distribution.md. Não mudar versão/inventário, publicar, instalar ferramentas, manipular Git ou operar consumidores reais.

## Notes

**2026-10-12T23:28:00.174000007Z**

Entrega do escopo aprovado: Bash coleta somente parâmetros ausentes e conduz confirmações por /dev/tty via função exportada; Python mantém em um único processo release fixada, validação, lock, plano e transação, delegando prompts ao Bash. Confirmar última estável não permite escolher versões antigas. Argumentos fornecidos são repassados e continuam validados. Sem terminal, stdin nunca é consentimento; --yes aprova versão/plano, colisões exigem --approve-collision e ticket exige --approve-migration-ticket separado. Dry-run/recovery seguem sem interação obrigatória. README apresenta curl | bash primeiro e download versionado verificado depois; endereço continua explicitamente um template a ser preenchido pela publicação. docs/distribution.md registra exceção de confiança no script de main, preservando hashes dos artefatos e proteções existentes. Evidências: uv run pytest --basetemp=/tmp/opencode/wiked-interactive-final-validation => 76 passed, 1 skipped (integração externa opcional); bash -n scripts/install-wiked.sh => sucesso. Testes incluem pipe curl sintético com PTY e uv real, perguntas ausentes, destino customizado, argumentos explícitos, recusas de versão/plano/colisão/ticket, ausência de terminal, automação e criação de ticket apenas com aprovação separada/localidade comprovada. Alterados somente scripts/install-wiked.sh, tests/test_wiked_installer.py, README.md e docs/distribution.md. Sem alteração da distribuição 1.4.0/inventário, publicação, Git ou consumidor real.

**2026-10-12T23:28:08.603431618Z**

Entregue camada Bash interativa sobre o executor Python existente: parâmetros ausentes e confirmações via terminal, argumentos e aprovações explícitos para automação, execução por pipe testada com PTY e uv real. README mostra entrada direta antes da verificada e contrato registra a exceção de confiança. 76 testes aprovados, 1 integração opcional ignorada; sintaxe Bash válida. Endereço oficial permanece pendente da publicação; distribuição e consumidores reais não alterados.
