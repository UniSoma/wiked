---
id: wik-01m4s7m8f01s
title: Consolidar endereço público oficial do Wiked
status: closed
type: task
priority: 2
mode: afk
created: '2026-10-12T23:37:07.296486757Z'
updated: '2026-10-12T23:40:50.766883437Z'
closed: '2026-10-12T23:40:50.766883437Z'
acceptance:
- title: README usa UniSoma/wiked nos comandos e no endereço oficial, sem placeholders de repositório
  done: true
- title: Contrato registra endereço confirmado e branch main; documentação mantém disponibilidade do instalador/releases pendente e não afirma publicação
  done: true
- title: Checagens textuais verificam comandos, links e ausência de placeholders obsoletos sem executar instalador ou alterar runtime
  done: true
---

## Description

Grill metodológico encerrado explicitamente pelo solicitante em 2026-10-12: autorizou substituir placeholders de endereço em README.md e registrar https://github.com/UniSoma/wiked em docs/distribution.md, mantendo publicação pendente explícita. Solicitante confirmou que scripts/install-wiked.sh estará disponível após finalização e publicação. Verificação HTTP somente leitura: repositório público, branch main; raw main/scripts/install-wiked.sh retorna 404; nenhuma release pública listada. Escopo estrito de documentação: endereço oficial e comandos derivados, sem afirmar disponibilidade atual do instalador ou dos artefatos. Sem publicar, Git, alterações de runtime, versão/inventário ou consumidores.

## Notes

**2026-10-12T23:40:02.886890141Z**

Solicitante também autorizou explicitamente a atualização pontual da asserção em tests/test_wiked_installer.py que exigia o placeholder anterior, para verificar a URL e --repository UniSoma/wiked. Escopo ampliado somente para essa asserção; instalador e runtime permanecem inalterados. README e contrato agora registram o endereço oficial e mantêm publicação/artefatos pendentes explícitos.

**2026-10-12T23:40:50.766883437Z**

Consolidado https://github.com/UniSoma/wiked e branch main no README e contrato de distribuição; comandos diretos, verificados e de automação usam UniSoma/wiked. Mantido aviso de instalador/releases ainda pendentes da finalização e publicação. Ajustada somente a asserção autorizada da URL oficial. Checagens textuais confirmam ausência de placeholders e preservação do aviso; uv run pytest --basetemp=/tmp/opencode/wiked-official-address-validation => 76 passed, 1 skipped. Sem alteração do instalador/runtime, Git, publicação ou consumidor real.
