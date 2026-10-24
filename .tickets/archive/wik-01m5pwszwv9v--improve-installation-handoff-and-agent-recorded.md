---
id: wik-01m5pwszwv9v
title: Improve installation handoff and agent-recorded maintenance review
status: closed
type: task
priority: 2
mode: hitl
created: '2026-10-24T12:05:13.679870501Z'
updated: '2026-10-24T12:46:45.650147228Z'
closed: '2026-10-24T12:46:45.650147228Z'
acceptance:
- title: Explicitly close a Methodological grill approving agent-operated acknowledgment after human disposition, its safety model, scope, and acceptance; amend the current human-only publication contract coherently.
  done: true
- title: After a completed review and explicit human confirmation, the maintenance agent can record acknowledgment through a documented installed interface without requiring a separate human installer command; incomplete analysis or missing confirmation leaves review pending.
  done: true
- title: After an effective version change, installer output includes a clearly labeled, self-contained maintenance-agent prompt ready to copy and paste, without command placeholders; first-install setup and pending-review reminders remain appropriately distinct.
  done: true
- title: Acknowledgment preserves version, identity/baseline, pending-range, and transactional-recovery safeguards and changes only review metadata; generic distribution remains portable and consumer-independent.
  done: true
- title: Align README, installation/publication guidance, installed maintenance instructions, and any manifest changes; validate runtime/test changes with uv run pytest and synthetic coverage of approval, failures, and installer handoff.
  done: true
- title: Interactive installer confirmations accept both y and yes case-insensitively, with prompts matching accepted responses and synthetic tests covering both forms; empty or unrecognized input never grants approval and existing authorization boundaries remain intact.
  done: true
links:
- wik-01m4sbvz62vp
- wik-01m4vhpp3xyt
---

## Description

Requester feedback after publishing 1.5.1 and updating a governed consumer wiki: the maintenance agent asked the user to stop agents and run a command containing the placeholder <installer-command>, --destination, and --acknowledge-maintenance-review 1.5.1. This administrative handoff was confusing. The post-installation/update guidance also did not make the exact maintenance-agent prompt obvious enough to copy and paste.

Requested ergonomic changes:
- Let the maintenance agent record completion of the reviewed-version acknowledgment after the human has explicitly accepted the report and decided the disposition of findings. Do not require the user to reconstruct and execute a separate installer command. A dedicated script shipped with the skill is an option, not a predetermined implementation.
- After an effective version update, print an explicit, self-contained, copy-and-paste prompt that asks the agent to use the installed Wiked skill to review the wiki against the new version, report findings and uncertainties, obtain human disposition, and record review completion through the approved interface. Keep first-install setup instructions distinct from update maintenance instructions.

Governance: the current publication contract explicitly reserves acknowledgment to the human with agents stopped and forbids the agent from performing it. The requested agent-operated flow changes that contract; before implementation, complete and explicitly close a Methodological grill covering authority, explicit human confirmation, safe execution while the reviewing agent is active, and acceptance. This ticket records the request; it does not itself authorize code or instruction edits.

Likely source scope: scripts/install-wiked.sh; distributed guides/maintenance.md and related routing; an optional manifested runtime acknowledgment script; distr/agents/wiked-manifest.yaml if inventory changes; README.md; docs/installation.md; docs/distribution.md; applicable source vocabulary/workflow; synthetic installer/runtime tests. Inspect affected interfaces before finalizing scope.

Preserve the meaning of acknowledgment: analysis and human disposition are complete, not certification of wiki conformity or permission for corrections. Corrections may remain pending in consumer-local tickets. Incomplete analysis must leave review pending. Preserve exact installed-version checks, reliable installation identity/baseline checks, transactional recovery, and pending-range integrity. Acknowledgment must not download a release, update the installed skill, modify wiki/contract content, or create correction tickets implicitly. No consumer-specific paths or knowledge may enter generic instructions, runtime messages, tests, or fixtures. No Git operation, publication, tool installation, or live consumer change is in scope.

## Notes

**2026-10-24T12:06:44.966553436Z**

Additional requester feedback: during installation the user repeatedly entered 'y', but the confirmation accepted only 'yes'. Extend this UX ticket to accept both 'y' and 'yes', case-insensitively, across interactive installer confirmations. Make prompt wording consistent with accepted answers. Preserve explicit consent: empty or unrecognized input must not approve an operation, and this must not broaden --yes authorization to collisions or migration-ticket creation. Include synthetic interactive tests for short and full affirmative answers and existing refusal/no-terminal safeguards. No implementation is authorized by this note; incorporate the addition into the ticket's Methodological grill.

**2026-10-24T12:27:16.742323585Z**

Methodological grill explicitly closed by the validating requester on 2026-10-24 after confirmation of the consolidated summary. Approved: installed metadata-only acknowledgment after complete analysis, report, human disposition and explicit confirmation of exact version/range; narrow live-reviewer exception, no concurrent install/update/recovery; canonical shared state/transaction core embedded in the self-contained installer with synchronization generation/check; stale-state refusal, preserved identity/baseline/range/recovery safeguards, no network dependency resolution in installed acknowledgment; unchanged metadata format; copy-ready post-update agent prompt distinct from setup/reminders; case-insensitive y/yes without broader --yes authority; prepare 1.6.0 with none impact. Scope includes installer, installed helper/shared core, embedding tooling, related distribution instructions, manifest/changelog, README, installation/publication docs, synthetic tests. Validate with uv run pytest and targeted textual/semantic review. No Git, publication, tool installation, consumer operation, general concurrency coordination, or audit-log mechanism. Behavioral agent compliance is not proven by structural tests.

**2026-10-24T12:45:41.119097645Z**

Delivered approved source preparation for 1.6.0. Added installed acknowledge_review.py (--inspect; exact --version/--since/--state-token plus --human-confirmed; --dry-run), canonical installation_state.py, and sync-installer-core.py generation/check for the self-contained installer embedding. Snapshot token binds installation root and metadata/manifest bytes; pre-replacement changes are refused without overwriting newer state. Preserved metadata-only transactions and installer recovery, baseline/inventory identity and pending-range checks, with no installed-file conformity prerequisite. Normalized alternate script paths only after symlink checks so interrupted acknowledgment journals remain discoverable by human recovery. Offline invocation uses already available Python/uv/cached PyYAML; missing prerequisites leave pending. Installer accepts case-insensitive y/yes without broadening --yes, prints a delimited copy-ready prompt on effective version changes, and separates setup/reminders. Aligned installed maintenance/runtime/routing guidance, README, source vocabulary/workflow, installation/publication contract, manifest and none-impact changelog. Validation: final uv run pytest => 205 passed, 1 skipped (optional external integration), 133.07s; no external consumer selected. Prior 120s attempt timed out without a reported failure; later complete runs passed. Synthetic coverage includes missing confirmation, dry run, exact-version/range/token refusal, root-bound portability, manifest/baseline failures, no-network prerequisite failure, metadata-only success, last-moment metadata/manifest races, handled and abrupt failures, installer-compatible recovery, dot-dot paths and symlink refusal, generated-core synchronization, quoted custom-path handoff, and short/full/invalid terminal approvals. Removed two old output phrase assertions from the handoff test in favor of technical prompt/path/argument checks; no methodological-prose freeze tests added. These checks do not establish agent behavioral compliance, actual human consent, semantic review completeness, or operational wiki conformity. Local links in 9 affected documentation files and Bash syntax verified. Packaging succeeded: /tmp/opencode/wiked-release-rg56ensw/distr.tar.gz, intended tag v1.6.0; no publication, installation, Git operation, or consumer change performed.

**2026-10-24T12:46:45.650147228Z**

Prepared Wiked 1.6.0 with installed, human-confirmed metadata-only review acknowledgment, canonical embedded transaction safeguards, copy-ready maintenance handoff, y/yes confirmations, aligned governance/docs, and synthetic regression coverage. Final uv run pytest: 205 passed, 1 optional external integration skipped. Packaged /tmp/opencode/wiked-release-rg56ensw/distr.tar.gz; no publication, installation, Git, or consumer operations. Future behavioral evaluation scenario amendment recorded in linked wik-01m4vhpp3xyt; it is not implemented coverage.
