---
id: wik-01m4khsrmqya
title: Preparar primeira publicação verificável do Wiked
status: open
type: task
priority: 2
mode: hitl
created: '2026-10-10T18:39:26.693651906Z'
updated: '2026-10-13T00:55:22.692788900Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- distribuicao
acceptance:
- title: Repositório autoral independente e custódia confirmados pelo mantenedor
  done: false
- title: Testes genéricos e prova de uso do artefato independentes de qualquer consumidor real
  done: false
- title: Publicação humana identificável registrada e documentação de release coerente
  done: false
- title: Artifact prepared with approved version, exact manifest inventory and compatibility; only distr.tar.gz is uploaded, with no download checksum requirement.
  done: false
- title: README and installation guide document the official main installer, stable-release distribution download, updates/setup, prerequisites and custom destinations without obsolete checksum or installer-asset requirements.
  done: false
- title: MIT license and applicable notices are present; the release contains distr.tar.gz with an immutable version approved by the maintainer; installer source is tested and available on main.
  done: false
deps:
- wik-01m2tphwrc4f
- wik-01m2tpjtev7w
---

## Description

Prepare and verify the first publication under docs/distribution.md, amended by the requester-confirmed Methodological grill for wik-01m4sbvndyah on 2026-10-13. The maintainer approves versions and releases; Git and publication remain human-operated. Prepare MIT licensing and applicable notices, and only distr.tar.gz as a release asset, containing exactly the manifest inventory. Installer is obtained from main/scripts/install-wiked.sh; no separately attached installer or SHA256SUMS is required. Stable SemVer tags and immutable published artifacts remain required; manifest/runtime/tag versions must agree. Document official origin, trusted-source download, prerequisites, supported platforms, default/custom destinations, discovery and installation/update/setup. Synthetic tests verify artifact and installer without real consumers or existing releases. Record identifiable human publication evidence, not only local preparation. Version centralization/increments are future work wik-01m4sbvz62vp. Preserve ownership boundaries, local installation baseline hashes, compatibility and transaction safeguards. No tool installation or replacement of the running agent skill.

## Notes

**2026-10-10T18:40:31.740875930Z**

Preparação de migração autorizada em 2026-10-10: este ticket aberto pertence à metodologia e será transferido manualmente com seu ID para o tracker autoral independente. Relações com registros que permanecem no consumidor foram retiradas; o contexto necessário está autocontido. Publicação e instalação permanecem trabalhos futuros. Esta nota não registra transferência física nem encerra o grill próprio deste trabalho.

**2026-10-13T00:55:22.692788900Z**

2026-10-13 requester-confirmed Methodological grill for wik-01m4sbvndyah supersedes the original versioned-archive, installer-asset and release-checksum requirements. Description and conflicting acceptance criteria now require only distr.tar.gz, installer obtained from main, and no download checksum. Local baseline hashes and all inventory/compatibility/recovery safeguards remain. This update is not evidence of human release publication.
