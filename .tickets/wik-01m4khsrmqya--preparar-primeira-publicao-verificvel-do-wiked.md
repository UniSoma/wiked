---
id: wik-01m4khsrmqya
title: Preparar primeira publicação verificável do Wiked
status: in_progress
type: task
priority: 2
mode: hitl
created: '2026-10-10T18:39:26.693651906Z'
updated: '2026-10-13T02:41:38.605345675Z'
assignee: VolneiSantos
tags:
- metodologia
- wiked
- distribuicao
acceptance:
- title: Repositório autoral independente e custódia confirmados pelo mantenedor
  done: true
- title: Testes genéricos e prova de uso do artefato independentes de qualquer consumidor real
  done: true
- title: Publicação humana identificável registrada e documentação de release coerente
  done: false
- title: Artifact prepared with approved version, exact manifest inventory and compatibility; only distr.tar.gz is uploaded, with no download checksum requirement.
  done: false
- title: README and installation guide document the official main installer, stable-release distribution download, updates/setup, prerequisites and custom destinations without obsolete checksum or installer-asset requirements.
  done: true
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

**2026-10-13T02:28:43.328203975Z**

Human publication follow-up on 2026-10-13: GitHub latest stable release https://github.com/UniSoma/wiked/releases/tag/v1.4.0 was observed with distr.tar.gz attached. The main installer and installer fetched from requester-selected commit fc29ccb both select distr.tar.gz. Requester confirmed the remaining old-name error was cache and explicitly accepted completion of packaging simplification. This records publication-channel evidence and requester acceptance for wik-01m4sbvndyah, not verification of every remaining publication criterion (such as licensing); this publication ticket remains open.

**2026-10-13T02:36:21.236716577Z**

Methodological grill explicitly closed by requester on 2026-10-13. Requester confirmed independent author custody, accepted transfer and authorized v1.4.0 publication as volneids. Approved MIT Copyright (c) 2026 UniSoma, source and distributed license with applicable provenance review; preserve v1.4.0 and prepare v1.4.1 with manifest/runtime agreement. Immutability remains a maintainer commitment, without required platform enforcement. Scope: licensing, manifest/runtime version, README, publication/installation documentation and synthetic package-install-installed-runtime verification with uv run pytest. Git and publication remain human-operated; version centralization and installer redesign excluded. Ticket closure awaits verifiable human publication of corrected release.

**2026-10-13T02:41:38.605345675Z**

Prepared approved 1.4.1 correction: root LICENSE and identical manifested skills/wiked/LICENSE contain MIT Copyright (c) 2026 UniSoma; manifest and runtime agree on 1.4.1. Inventory has 17 regular files. Review found declared external dependencies/tools, not bundled third-party code; historical research and consumer material are not relicensed. README and distribution/installation guides document licensing, observed v1.4.0 publication, maintainer immutability commitment and human 1.4.1 handoff. Synthetic artifact test packages, installs, then runs installed runtime from unrelated cwd against synthetic wiki/tracker: six files checked, no errors/warnings. Installer fixture now derives source version before substituting synthetic release identity; runtime-failure fixture uses coherent synthetic manifest. Initial suite exposed the old mixed-version fixture; corrected final command uv run pytest --basetemp=/tmp/opencode/wiked-publication-1.4.1-tests: 96 passed, 1 skipped (optional external integration not selected). bash scripts/package-wiked.sh --output /tmp/opencode/wiked-publication-1.4.1 produced only /tmp/opencode/wiked-publication-1.4.1/distr.tar.gz; tar inventory inspected. Existing source-root distr.tar.gz is still the old 1.4.0 archive, unchanged (local preservation hash 83f747180dbfbed52bd4618a1a9d358fcc68c55d36aa0a193da8e3424ceb7492); do not upload it for 1.4.1. No new release published, Git operated, tool installed, real consumer edited or active skill replaced. AC 1, 2, 5 checked; AC 3, 4, 6 remain pending verified human publication of v1.4.1 with only the corrected distr.tar.gz and published source/license/main installer.
