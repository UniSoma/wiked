---
id: wik-01m4s821zj1m
title: Fixar origem oficial e simplificar argumentos do instalador Wiked
status: closed
type: task
priority: 2
mode: afk
created: '2026-10-12T23:44:39.410288123Z'
updated: '2026-10-12T23:46:57.672641872Z'
closed: '2026-10-12T23:46:57.672641872Z'
acceptance:
- title: Instalador fixa UniSoma/wiked, remove --repository e não pergunta origem; origem não pode ser sobrescrita por argumentos
  done: true
- title: README e contrato documentam comando simples e interface restante sem parâmetro ou pergunta de origem
  done: true
- title: Testes de pipe interativo, automação, validação e preservação das proteções usam transporte sintético da origem oficial; uv run pytest passa
  done: true
---

## Description

Grill metodológico encerrado explicitamente pelo solicitante: fixar UniSoma/wiked como única origem de instalação, sem outro repositório possível; remover --repository e pergunta de origem. Comando README curl -fsSL https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh | bash. Preservar somente opções úteis de destino, simulação, recuperação e aprovações explícitas. Escopo autorizado: scripts/install-wiked.sh, tests/test_wiked_installer.py, README.md, docs/distribution.md. Sem publicar, alterar versão/inventário, Git ou consumidores reais. Testes sintéticos devem interceptar transporte da origem oficial, nunca oferecer override de origem ao usuário.

## Notes

**2026-10-12T23:46:50.146418057Z**

Implementação concluída: OFFICIAL_REPOSITORY=UniSoma/wiked fixo no núcleo; --repository e pergunta de origem removidos do Bash/Python. Argumento antigo é rejeitado antes de download; assets de outras origens também são rejeitados. README mostra comando direto curl -fsSL https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh | bash e automação padrão apenas --yes; destino customizado, dry-run, recovery e aprovações específicas preservados. Contrato registra exclusividade da origem e transporte sintético dos URLs oficiais nos testes. Evidências: uv run pytest --basetemp=/tmp/opencode/wiked-fixed-origin-validation => 78 passed, 1 skipped; bash -n scripts/install-wiked.sh => sucesso. Testes de pipe usam exatamente bash sem argumentos no fluxo padrão, com PTY e uv real; nenhuma rede real é necessária. Checagens textuais: README sem --repository; instalador só mantém --repository-root na chamada interna do runtime, interface distinta do consumidor. Sem publicação, Git, mudança de versão/inventário ou consumidor real.

**2026-10-12T23:46:57.672641872Z**

Origem UniSoma/wiked fixada, removidos parâmetro --repository e pergunta de origem. README simplificado para curl | bash e automação padrão --yes; opções necessárias e proteções preservadas. Testes rejeitam override e assets externos usando transporte sintético da origem oficial. Validação: 78 testes passaram, 1 integração opcional ignorada; sintaxe Bash válida. Sem publicação ou alteração de consumidores reais.
