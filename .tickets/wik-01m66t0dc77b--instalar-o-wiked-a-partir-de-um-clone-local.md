---
id: wik-01m66t0dc77b
title: Instalar o Wiked a partir de um clone local
status: in_progress
type: task
priority: 2
mode: hitl
created: '2026-10-30T16:24:09.350876381Z'
updated: '2026-10-30T17:14:19.696890807Z'
acceptance:
- title: Instalador aceita --source <diretório local> com scripts/package-wiked.sh, recusa URLs e diretórios sem empacotador; sem o argumento o comportamento oficial não muda
  done: true
- title: O pacote gerado pelo empacotador do clone segue o caminho oficial do candidato; falha de empacotamento aborta sem alterações
  done: true
- title: 'Com --source: versão maior atualiza normalmente, mesma versão com conteúdo divergente oferece substituição confirmada sem nova revisão, versão menor é recusada'
  done: true
- title: docs/installation.md documenta o fluxo e o realinhamento; docs/distribution.md registra a revisão da decisão de origem; README, runtime distribuído, manifesto e versão inalterados
  done: true
- title: Testes sintéticos cobrem os casos decididos e uv run pytest passa
  done: true
---

## Description

Permitir que o instalador receba a raiz de um clone local do Wiked (`--source <raiz-do-clone>`) em vez de buscar a última release do GitHub, para testar uma release ainda não publicada numa wiki real e para que contribuidores testem uma branch. Reverte parcialmente a decisão de wik-01m4s821zj1m (origem única UniSoma/wiked, sem argumento de origem); continua sem origem remota alternativa.

Proposta inicial (sujeita ao Methodological grill): o instalador empacota o clone com o `scripts/package-wiked.sh` do próprio clone numa pasta temporária e conduz o `distr.tar.gz` resultante pelo mesmo caminho do candidato oficial (validação, contrato, plano, confirmações, transação, metadados); `.wiked-install.json` registra origem local, commit e árvore suja.

Escopo inicial: scripts/install-wiked.sh, tests/test_wiked_installer.py, README.md, docs/distribution.md e, se necessário, o núcleo gerado do estado de instalação.

Methodological grill aberto; nenhuma edição de conteúdo governado antes do fechamento explícito.

## Notes

**2026-10-30T17:06:55.882426980Z**

Methodological grill encerrado com confirmação explícita do solicitante (2026-10-30).

Objetivo: permitir instalar o Wiked a partir de um clone local para testar releases não publicadas e branches em wikis reais. Revê wik-01m4s821zj1m apenas nisso; continua sem origem remota alternativa.

Decisões:
- Interface: `--source <diretório local>`; URLs rejeitadas; sem o argumento nada muda; sem `--archive`. O diretório precisa conter `scripts/package-wiked.sh`; Git não é exigido.
- Candidato: o `package-wiked.sh` do clone gera `distr.tar.gz` em pasta temporária, que segue o caminho oficial (validação do candidato, contrato, plano, confirmações, transação, metadados). Falha de empacotamento aborta sem alterar nada.
- Responsabilidade delegada: sem controle de árvore suja, sem registro de origem nos metadados, sem comparação de conteúdo no instalador oficial.
- Versões: maior segue o fluxo normal, incluindo revisão pós-atualização confirmável normalmente; mesma versão com conteúdo diferente oferece substituição com confirmação, sem nova revisão, só com `--source`; menor é rejeitada.
- Realinhamento: para release de mesma versão, `--source` apontando para clone no tag correspondente; release oficial de versão maior realinha pelo instalador tradicional.
- Escopo: scripts/install-wiked.sh, tests/test_wiked_installer.py, docs/installation.md (README inalterado), docs/distribution.md. Runtime distribuído, manifesto e versão da distribuição inalterados.
- Validação: testes sintéticos (clone, URL recusada, diretório sem empacotador recusado, mesma versão divergente com oferta de substituição só via --source, versão menor recusada, falha do empacotador sem alterações); uv run pytest.

**2026-10-30T17:07:21.674789152Z**

Correção de fato após o grill: o instalador já compara candidato e arquivos instalados na mesma versão (plano sobre observed x hashes) e oferece reinstalação confirmada quando divergem, em qualquer origem. A Q4 não exige código novo, e o instalador oficial também realinha uma instalação local de mesma versão, ao contrário do que foi afirmado no grill. Escopo reduzido, sem nova decisão.

**2026-10-30T17:14:15.949313033Z**

Implementado: --source no instalador (Bash e Python, fora do núcleo gerado), testes sintéticos (clone com empacotador stub, clone real com o package-wiked.sh, URL/diretório sem empacotador/falha de empacotamento sem alterações, versão maior/mesma divergente/menor, fluxo interativo, --help), docs/installation.md (seção Install from a local clone) e docs/distribution.md (exceção à origem única). README, runtime distribuído, manifesto e versão inalterados. Evidências: uv run pytest => 274 passed, 2 skipped, exit 0; dry-run real em ../wikidoi com --source /home/volneids/wiked selecionou 1.8.0 sem alterar arquivos.
