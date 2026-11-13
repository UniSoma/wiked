---
id: wik-01m7at8m1h4p
title: Pesquisar registros de decisões e indefinições e colaboração via plataformas externas
status: closed
type: chore
priority: 2
mode: afk
created: '2026-11-13T16:01:17.872994783Z'
updated: '2026-11-13T16:04:27.274688324Z'
closed: '2026-11-13T16:04:27.274688324Z'
parent: wik-01m7at81hnsd
tags:
- wayfinder-research
---

## Description

### Question

Que práticas (ADR, RAID log, decision log, issue tracking ligado a documentação, pedidos de cliente em plataformas como Basecamp) sustentam o controle explícito de indefinições e a coedição sem acesso ao repositório?

## Notes

**2026-11-13T16:04:27.141411511Z**

ADR/MADR, RAID, issue log do PMBOK, issue register do PRINCE2 e Item Tracking do BABOK funcionam quando os registros são pequenos, têm dono, status, racional e revisão periódica. Falham quando o log se descola do artefato, quando quem decide não consegue acessá-lo (o próprio Nygard aponta a barreira do repositório para clientes) ou quando o registro vira documento ou peça de venda. Plataformas como Basecamp (privado por padrão, resposta por e-mail) e o portal do JSM dão acesso ao cliente sem Git. As pendências do Wiked ligadas a tickets e validadas fecham a lacuna de drift. Faltam relação explícita de supersessão, decisores registrados, visibilidade por item na sincronização e cadência de revisão.

**2026-11-13T16:04:27.274688324Z**

Pesquisa concluída: registros de decisões e pendências e colaboração via plataformas externas, com comparação ao Wiked e lacunas
