---
id: wik-01m5q5abxefd
title: Fornecer integração opcional Docsify para diagramas interativos na 1.6.0
status: closed
type: feature
priority: 2
mode: hitl
created: '2026-10-24T14:33:58.957835196Z'
updated: '2026-10-24T15:08:42.941098568Z'
closed: '2026-10-24T15:08:42.941098568Z'
tags:
- metodologia
- docsify
- diagramas
acceptance:
- title: Núcleo e manutenção distinguem correspondência obrigatória de interatividade opcional; changelog 1.6.0 orienta agente pós-instalação sem ativação implícita
  done: true
- title: Guia lazy e adaptador manifestado fornecem padrão reproduzível de imagem, identificadores, links, configuração e falhas seguras com leitura estática
  done: true
- title: Validador e testes cobrem âncoras estáveis e compatibilidade com imagens Markdown e links existentes
  done: true
- title: Testes sintéticos do adaptador cobrem ida/volta, múltiplas ocorrências e diagramas, navegação/reabertura e rejeição de conteúdo inseguro; execução de navegador ou impedimento documentado explicitamente
  done: true
- title: uv run pytest e verificações técnicas executadas; fronteiras de propriedade preservadas sem instalação, consumidor real ou publicação
  done: true
---

## Description

Methodological grill explicitamente fechado pelo solicitante habilitado nesta sessão; escopo confirmado antes das edições. Núcleo Wiked exige correspondência, títulos e identidade estável, mas não caixas clicáveis. Entregar guia opcional e lazy específico de diagramas no Docsify, adaptador reutilizável versionado, compatibilidade de âncoras no validador, testes sintéticos estruturais e de navegador. Preservar imagem Markdown, desenho aceito e leitura estática. Manutenção pós-instalação segue changelog 1.6.0, identifica Docsify e propõe ativação sob autorização; sem autoativação. Wiked mantém adaptador, consumidor mantém configuração. Release 1.6.0 ainda não publicada; sem incremento de manifesto ou publicação. Não editar consumidores nem instalar ferramentas. Redação do changelog será revista pelo solicitante. Navegador/CLI ausente neste ambiente na verificação inicial: não instalar, registrar eventual impedimento de execução sem alegar cobertura.

## Notes

**2026-10-24T15:04:09.616093445Z**

Implementação preparada: protocolo genérico aceita diagramas estáticos, guia opcional guides/docsify.md e adaptador viewers/docsify-diagrams.js manifestado na 1.6.0, manutenção pós-instalação propõe ativação autorizada. Padrão concreto usa título Markdown wiked-diagram=<id>, âncoras <a id=...>, retornos SVG #wiked-node=<source-key>&section=<anchor>; o retorno declara a associação uma vez e o adaptador torna o grupo existente clicável via classe base64 do identificador D2. Não requer D2 link nem ícones e não altera SVG em disco. Teste real revelou que Docsify 4.13.1 descarta filename de imagens relativas com fragmento; substituído o marcador de fragmento por metadado no título, com orientação explícita. Validador reconhece âncoras fora de código/comentários, colisões e sintaxe/destino descritivo dos retornos opcionais. Teste de navegador executado com playwright-cli e Chromium fornecidos pelo humano após reinício: passou com Docsify 4.13.1 real, múltiplos diagramas/ocorrências, ida/volta, teclado, navegação/reload, rejeição de SVG ativo, heading renomeado com identidade estável, resposta atrasada e fallback sem adaptador. WIKED_BROWSER_TESTS=1 uv run pytest tests/test_wiked_docsify.py::test_docsify_browser_integration: 1 passed. Verificações textuais finais passaram (manifesto, links/fragmentos de instruções, ASCII, whitespace, versão inalterada). Testes antigos de empacotamento corrigidos para obter a declaração técnica atual em vez de presumir none. Suíte completa final em execução; nenhuma publicação ou edição de consumidor.

**2026-10-24T15:08:29.904453184Z**

Validação final após reinício: uv run pytest --maxfail=1 concluiu com 220 passed, 3 skipped (177.14s). WIKED_BROWSER_TESTS=1 uv run pytest tests/test_wiked_docsify.py concluiu com 2 passed, 1 skipped (7.26s), incluindo teste real de navegador com Docsify 4.13.1/Chromium via playwright-cli 0.1.19. O skip desse arquivo é a verificação opcional com D2, ausente no ambiente reiniciado; antes do reinício, a verificação de metadados e recursos com D2 0.7.1 passou na execução específica. Outros skips padrão correspondem à opção explícita de navegador e integração externa não selecionada. A primeira tentativa de suíte completa foi interrompida por timeout; outra pelo reinício; não são evidência de sucesso. A execução final acima concluiu sem falhas. Testes Node usam um modelo DOM pequeno para fluxo de controle, distinguido explicitamente do teste de navegador real. Browser acceptance não é prova semântica nem evidência operacional de consumidor. Changelog 1.6.0 permanece disponível para revisão final do solicitante. Sem alteração de versão, instalação de ferramentas, consumidor real, Git ou publicação.

**2026-10-24T15:08:42.941098568Z**

Integração opcional Docsify entregue para 1.6.0: guia lazy, adaptador reutilizável, âncoras no validador, núcleo sem obrigatoriedade de cliques e orientação de manutenção/changelog. Suíte final: 220 passaram, 3 skips; verificação específica com navegador real: 2 passaram, 1 skip D2 indisponível após reinício. Sem publicação ou edição de consumidores; revisão final do changelog permanece com o solicitante.
