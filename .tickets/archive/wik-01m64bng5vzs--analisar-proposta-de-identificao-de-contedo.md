---
id: wik-01m64bng5vzs
title: Analisar proposta de identificação de conteúdo derivado e verificação de links externos
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-29T17:35:02.843597763Z'
updated: '2026-10-29T18:52:16.761215076Z'
closed: '2026-10-29T18:52:16.761215076Z'
tags:
- metodologia
- wiked
- proposta
acceptance:
- title: Grill metodológico decide adoção, escopo e desenho da identificação obrigatória de conteúdo derivado, incluindo unidade de classificação, configuração pela instância e relação com a proveniência
  done: true
- title: Grill metodológico decide adoção, escopo, modo de execução, severidade configurável e taxonomia de causas da verificação de links externos
  done: true
- title: Decisões registradas, com tickets de implementação criados para o que for aprovado ou rejeição justificada
  done: true
links:
- wik-01m64g2kj369
- wik-01m64g2kr5af
- wik-01m64g2kytyz
---

## Description

Analisar uma proposta de usuário com duas capacidades potencialmente independentes e decidir, para cada uma, se o Wiked deve adotá-la, em que escopo e com qual desenho. A análise é metodológica; implementação, se aprovada, deve ser desdobrada em tickets próprios.

Pontos a qualificar na análise:

- Feature 1: unidade de classificação adequada (tipo de página ou outra), como a instância define texto ou critérios da identificação, como expressar e validar presença e posição da identificação e do link para a fonte oficial, e relação com os registros de proveniência já existentes, sem duplicar datas obrigatoriamente.
- Feature 2: escopo (só fonte oficial ou qualquer link externo), modo de execução (validação regular, opcional ou sob demanda; dependência de rede e determinismo), severidade configurável pela instância e taxonomia de causas (endereço malformado, resposta de erro, acesso negado, servidor indisponível, falha de conexão), sem afirmar inexistência quando houver autenticação.
- Limites: o validador não compara conteúdo externo nem determina correção, vigência, completude, autorização de reprodução ou responsabilidade.
- Compatibilidade com os invariantes do repositório: instruções genéricas sem conhecimento de consumidor, carregamento progressivo, Distributed validator e Instance contract como interfaces ativas.

### Proposta original

#### Contexto e caso de uso

Mantemos uma wiki operacional de uma diretoria. Parte do conteúdo será derivada de políticas corporativas cuja **fonte oficial permanece em outro sistema**. A wiki poderá conter um espelho ou apenas um recorte dessas políticas, com foco no que é relevante para a diretoria; não precisa reproduzi-las integralmente.

Queremos que uma pessoa que acesse diretamente uma dessas páginas entenda, antes de ler o conteúdo, que **a página da wiki não é o documento oficial** e consiga acessar a fonte oficial. Também queremos distinguir esse conteúdo das políticas efetivamente governadas pela própria diretoria.

Por exemplo, uma página poderia começar assim:

> **Esta página é um espelho ou recorte de uma política externa; não é o documento oficial.**
>
> [Consultar a política oficial](https://exemplo.org/politicas/politica-de-seguranca)

A wiki já mantém registros de proveniência relacionados às páginas, com informações como origem, data de publicação ou última modificação e data de consulta. Não vemos necessidade de duplicar essas datas obrigatoriamente na página derivada.

#### Feature 1 — Identificação obrigatória de conteúdo derivado

Gostaríamos que o Wiked permitisse configurar, para determinados tipos de página ou outra unidade de classificação que considere adequada:

- uma **identificação visível no início da página** de que o conteúdo é derivado e não é o documento oficial;
- um **link direto obrigatório para o documento oficial**, também em posição facilmente visível;
- validação da presença desses elementos e de sua posição.

A instância deveria poder definir o texto ou os critérios dessa identificação. Não dependemos de um formato específico de contrato ou de Markdown: o importante é que a distinção apareça para quem consulta a página e seja verificável automaticamente.

No nosso caso, usaríamos essa capacidade para diferenciar páginas derivadas de políticas corporativas de políticas governadas pela diretoria. Ela também poderia servir a outros tipos de documento cuja autoridade esteja fora da wiki.

#### Feature 2 — Verificação de links externos com severidade configurável

Como recurso potencialmente independente, seria útil que o Wiked pudesse verificar links externos e permitisse à instância configurar a severidade dos diagnósticos.

No nosso caso, gostaríamos de receber um **aviso** quando não fosse possível acessar o documento oficial, para que uma pessoa confira o link. A causa deve ser diferenciada quando possível: endereço malformado, resposta de erro, acesso negado, servidor indisponível ou falha de conexão não significam necessariamente a mesma coisa.

Em especial, alguns sistemas exigem autenticação. Nesses casos, o validador pode não conseguir acessar um link que funciona para usuários autorizados; o diagnóstico não deveria afirmar categoricamente que o documento não existe.

A definição de escopo, modo de execução e configuração dessa verificação fica a critério do mantenedor. Ela poderia ser útil também para outras fontes e referências externas da wiki.

#### Limites esperados

Não esperamos que o validador compare o conteúdo da wiki com documentos externos não estruturados nem determine correção, vigência, completude, autorização de reprodução ou responsabilidade pela política. Essas decisões e verificações cabem ao operador qualificado durante a indexação e a manutenção.

O objetivo da automação é mais restrito: **exigir a identificação do caráter derivado, garantir que haja um caminho explícito para o documento oficial e sinalizar problemas verificáveis nos links**.

## Notes

**2026-10-29T17:39:33.301912384Z**

Grill metodológico, rodada 1 (decisões do requerente validador): Q1 analisar as duas features no mesmo grill, com decisões e tickets de implementação independentes. Q2 adotar a Feature 1 como capacidade genérica e opcional do contrato para tipos de página com autoridade externa (nova methodology_version, contract_version 1.0 mantida). Q3 adotar a Feature 2 em duas camadas: checagem offline e determinística de links externos na validação padrão; verificação de acessibilidade online apenas como modo explícito e opcional, fora da validação padrão exigida pelos fluxos. Grill ainda aberto.

**2026-10-29T18:19:37.995706966Z**

Grill metodológico, rodada 2: Q4 unidade = tipo de página, por coleção opcional de nível superior no contrato. Q5 aviso no corpo da página com link externo absoluto direto, independente da proveniência e sem regra de igualdade com o registro da fonte; ajuste do requerente: a instância pode optar por apresentar só o aviso configurado, sem link. Q6 checagem offline de todo link externo em Markdown da wiki, com família de regras própria. Q7 em revisão: o requerente prefere um script apartado para a verificação online, por ser procedimento eventual de manutenção. Q8 regra própria de severidade (error|warning) para acessibilidade online. Q9 taxonomia de causas distintas (malformado, DNS/conexão, tempo esgotado, TLS, 401/403, 404/410, 5xx, outras); mensagens descrevem o observado e nunca afirmam inexistência do documento.

**2026-10-29T18:46:13.117466218Z**

Grill metodológico, rodada 3: Q10 verificação online em script apartado acionado pela manutenção, sob demanda, com extração de links e leitura do contrato compartilhadas com o validador; checagem offline permanece no validador; ajuste do requerente: timeout padrão sobrescrevível por argumento e paralelismo na checagem. Q11 o primeiro bloco após o H1 é uma citação cujo primeiro parágrafo contém literalmente o aviso configurado (formatação inline ignorada). Q12 link oficial required/optional, externo absoluto http(s) na citação; em revisão: o requerente propõe declarar external_authority dentro da definição do tipo de página. Q13 apenas links explícitos e autolinks. Q14 esquemas http/https/mailto offline; online: uma requisição por URL distinta, HEAD com recuo para GET, redirecionamentos limitados, sem credenciais, sem verificar fragmentos.

**2026-10-29T18:49:12.194625960Z**

Grill metodológico, rodada 4 (todas as recomendações aceitas): Q15 external_authority {notice, link: required|optional} declarado dentro do tipo de página, revogando a coleção de nível superior de Q4; rules.external_authority obrigatória só quando algum tipo a declara. Q16 script com --timeout (padrão 10 s) e --workers (padrão 8), limite fixo de 2 conexões por host. Q17 regras novas opcionais e de adoção explícita, com methodology_version mínima na próxima minor e contract_version 1.0; sem rules.external_links não há checagem offline; sem rules.external_reachability o script sai com código 2. Q18 documentação em contracts/README, modeling, scripts/README (seção própria do script), maintenance e uma rota em SKILL.md. Q19 fixtures sintéticas e servidor HTTP local nos testes, sem rede externa nem asserções sobre prosa. Q20 três tickets de implementação: F1, F2 offline e F2 online (dependente da offline). Aguardando confirmação de entendimento compartilhado.

**2026-10-29T18:52:10.288897571Z**

Entendimento compartilhado confirmado explicitamente pelo requerente validador em 2026-10-29; grill metodológico encerrado. Tickets de implementação: wik-01m64g2kj369 (F1 autoridade externa), wik-01m64g2kr5af (F2 offline), wik-01m64g2kytyz (F2 online, depende da offline).

**2026-10-29T18:52:16.761215076Z**

Análise concluída: as duas features foram adotadas com o desenho registrado nas notas e desdobradas em três tickets de implementação.
