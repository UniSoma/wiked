---
id: wik-01m4s9naqts0
title: Make the README a welcoming entrypoint for new Wiked users
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-13T00:12:39.546650727Z'
updated: '2026-10-13T02:51:15.809601489Z'
closed: '2026-10-13T02:51:15.809601489Z'
acceptance:
- title: README explains agent-managed wiki value, human oversight, and brief illustrative use cases in accessible English.
  done: true
- title: README keeps basic installation and agent-assisted setup guidance with accurate prerequisites, discovery, and download availability.
  done: true
- title: Detailed installation guidance is preserved in docs/installation.md; README links deeper architecture, governance, and development material.
  done: true
- title: Explicit methodological grill closure and targeted textual validation evidence are recorded; changes stay within the approved two-file scope.
  done: true
---

## Description

Requester approved a dedicated ticket for a concise English README aimed at technical newcomers. Present Wiked as an agent-managed, human-governed Markdown wiki inspired by LLM Wiki; explain value and short illustrative use cases before installation. Keep the basic curl command and an agent-assisted setup request in README. Move detailed installation guidance into docs/installation.md and link architecture/governance as further reading. Scope: README.md and docs/installation.md only; no runtime, installer, publication, Git, or tool installation changes. Methodological grill remains open pending final shared-understanding confirmation. Requester considers Wiked ready for use and asks to remove unfinished-product language. Read-only HTTP checks found the public installer returns 200 but the latest stable release API returns 404; resolve how to present download availability accurately before closure.

## Notes

**2026-10-13T00:14:25.415968664Z**

Methodological grill explicitly closed by the validating requester ('sim') after the final shared-understanding summary. Approved scope: README.md and new docs/installation.md only. English newcomer-first README: value, LLM Wiki inspiration, agent-managed wiki with human oversight, illustrative use cases, basic curl installation, agent-assisted setup, further-reading links. Preserve installation details in the guide and link existing architecture/governance guidance. Requester explicitly directs documentation to assume the stable release will be published immediately after README completion: no unfinished-product or pending-publication notices in these two files. This is a publication-target assumption, not evidence of publication; public installer HTTP 200 and latest-release API HTTP 404 were observed before editing. Publishing, release verification, runtime/installer changes, tool installation, and Git operations remain outside scope. Validate through targeted textual checks; no Python/runtime/test changes.

**2026-10-13T00:16:18.614012447Z**

Implementation delivered for requester review: README.md reduced from 224 to 94 lines (571 words), reorganized around value, LLM Wiki-inspired agent management, three illustrative use cases, prepare/install/setup, a first indexing request, and further reading. New docs/installation.md preserves prerequisites, discovery, script trust and checksum verification, interactive flow, setup governance/local contract, updates, migration-ticket approvals, ownership/collisions, automation/custom destinations, transaction recovery, and release format. Targeted Node textual checks passed: 14 local links and anchors resolve; Markdown code fences balanced; both files ASCII English; no unfinished-product wording; expected section order, exact curl command and setup prompt present; all six documented advanced flags exist in installer source; distributed Markdown skill has no relative docs/ link dependencies. Manual review confirms source-versus-consumer identity, consumer-owned content boundaries, installed-skill/local-contract routing, and human meaning versus structural validation. No runtime/test files changed, so pytest was not run. No installer execution, tool installation, Git operation, consumer edits, or publication performed. Publication remains an explicitly approved documentation assumption, not a verified release result. Ticket remains open for requester editorial acceptance.

**2026-10-13T00:22:56.485650527Z**

Methodological grill amendment closed by requester ('de acordo, pode aplicar') after the explicit proposed sequence and caveats. Same two-file scope: explain Knot briefly, show optional Knot install from official install.sh using sh, local knot init only when not already configured, then Wiked install; preserve Python/uv prerequisites, add ~/.local/bin PATH troubleshooting, and keep advanced integration/verification in the guide. This authorizes documenting human-run commands only, not executing installers or initializing any tracker. The official Knot README was checked read-only; Context7 returned only unrelated DNS products, so upstream documentation supplied the CLI facts.

**2026-10-13T00:23:32.102726770Z**

Approved onboarding amendment applied in README.md and docs/installation.md. README now explains Knot and shows optional official Knot install (curl | sh), conditional local knot init, then Wiked install (curl | bash). Added ~/.local/bin PATH warning, retained explicit Python/uv prerequisites, removed redundant tracker-preparation instruction from setup, and broadened script-trust warning to both downloads. Guide includes local-only initialization, existing-tracker caveat, upstream advanced integration and manual-verification links. Targeted Node textual checks passed for both files: exact command order, optional initialization, PATH/prerequisite/setup guidance, ASCII English, balanced fences, and all 14 local links/anchors. No installers executed, tracker initialized, runtime/test changes, Git operations, tool installation, or publication. Acceptance checks remain satisfied; ticket remains open for editorial review.

**2026-10-13T00:26:48.632356691Z**

Requester-directed copy refinement within the confirmed newcomer README objective and existing file scope: expanded the Markdown ownership paragraph to explain the open, human-readable format, freedom from a particular tool, browsing in a favorite Markdown app such as Obsidian, and reading files as plain text. This describes reading, not manual governed wiki edits or a new integration guarantee. Only README.md changed. Targeted Node checks passed for required wording, ASCII, balanced fences, local links and anchors. No runtime/test changes; no pytest required.

**2026-10-13T02:51:15.809601489Z**

Requester explicitly approved the final README. Delivered newcomer-first English introduction, LLM Wiki-inspired agent-managed/human-governed framing, use cases, open human-readable Markdown with Obsidian/plain-text reading, optional Knot installation and local initialization followed by Wiked installation and agent-assisted setup. Preserved advanced installation guidance in docs/installation.md. Targeted textual checks passed; no runtime changes or publication performed.
