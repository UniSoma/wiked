---
id: wik-01m7at8m1h4p-dv7d3
ticket: wik-01m7at8m1h4p
title: Decision/open-question records and external client collaboration
type: other
created: '2026-11-13T16:04:27.012786368Z'
updated: '2026-11-13T16:04:27.012786368Z'
---

# Decision and open-question records, and client collaboration via external platforms

Ticket: wik-01m7at8m1h4p. Research date: 2026-11-13. Research only; not normative guidance.

## Summary answer

Four practice families each control part of the problem. **Decision records** (Nygard ADR, MADR) make settled decisions durable, give them a status lifecycle, and supersede them instead of editing. **Project logs** (RAID, the PMBOK issue and assumption logs, the PRINCE2 issue register and daily log) make open items, assumptions and change requests visible, owned and reviewed. **Business-analysis item tracking** (BABOK "Item Tracking") assigns a responsible person to each stakeholder concern. **Client-facing work platforms** (Basecamp client access, Jira Service Management portals) let clients raise requests and answer questions without touching the engineering repository.

They work when records are small, owned, and carry status and rationale, when an explicit transition (proposed to accepted, open to closed) has a named authority, and when the log is reviewed regularly. They fail when the log is kept apart from the artefact it governs, when nobody owns or reviews it, when entries grow into documents or sales pitches, or when the people who decide cannot reach it. Nygard himself names the last risk: repo-hosted ADRs are less accessible to client stakeholders.

None of these practices makes the log and the artefact check each other. Wiked's ticket-linked pendências, with a validator that checks the link and the ticket status, plus agent-mediated sync to a client platform, combine these strengths and fix that gap.

## Practices

**ADR (Nygard, 2011).** The sections are Title, Context, Decision, Status and Consequences. The statuses are proposed, accepted, deprecated and superseded. Records are numbered sequentially, and numbers are never reused. A reversed decision is kept and marked superseded. Records are stored in the repo (`doc/arch/adr-NNN.md`) as Markdown. The rationale is that small, modular documents "have at least a chance at being updated", and that a team should avoid both "blind acceptance" and "blind reversal" of past decisions. Nygard reports positive developer feedback over roughly ten months of use. He also raises one objection himself: repo-hosted records are less accessible to project managers and client stakeholders. His answer is to share rendered links from the hosting platform. [1]

**Fowler's bliki on ADRs.** Once an ADR is accepted, it "should never be reopened or changed - instead it should be superseded". He stresses brevity, rationale, serious alternatives, consequences and confidence, and the triggers for review. He notes that repos do not suit decisions spanning several code bases, and that some people find git too hard for non-developers. [2]

**MADR 4.0.0 (2024-09-17).** It adds Decision Drivers, Considered Options, Pros and Cons, and Confirmation (how compliance will be checked). Optional front matter covers decision-makers, consulted and informed parties, which is RACI-like. The status values are proposed, rejected, accepted, deprecated and superseded. [3]

**Zimmermann's ADR anti-patterns.** He names "Fairy Tale", "Sales Pitch", "Free Lunch Coupon", "Dummy Alternative", "Sprint", "Tunnel Vision", "Mega-ADR"/"Novel"/"Epic" and "Blueprint or Policy in Disguise". His good practices are to disclose your confidence level and not to defer high-impact decisions. [4]

**RAID log.** It tracks Risks, Assumptions (or Actions), Issues, and Dependencies (or Decisions) in one place. Assumptions are untested beliefs that must be validated. Logging decisions avoids reopening settled questions. Regular review is recommended. Uncertain: these are vendor and practitioner sources, the letters are expanded inconsistently, and none of them is a PMI or AXELOS normative text. [5][6]

**PMBOK issue log.** The PMBOK v5 glossary defines it as "a project document used to document and monitor elements under discussion or in dispute between project stakeholders". This wording is quoted second-hand in a forum and should be checked against the PMBOK 7th/8th editions. The assumption log and issue log are inputs to monitoring and controlling. I found no primary PMI definition of a "decision log". [7]

**PRINCE2 issue register and daily log.** Issue types are request for change, off-specification, and problem or concern. Informal items go in the daily log, and formal items go in the issue register, which gives each an ID and an issue report. In PRINCE2 7 both are reportedly consolidated into a Project Log that provides an audit trail from concern to decision to changed baseline. Uncertain: these come from secondary study guides, because the AXELOS manual is not public. [8][9]

**BABOK v3 Item Tracking (technique 10.26).** Its purpose is "to capture and assign responsibility for issues and stakeholder concerns that pose an impact to the solution". In v2 the technique was Problem Tracking, which was linked to Define Assumptions and Constraints. I found no BABOK category named "open questions" (unconfirmed). [10][11]

**Docs-linked issue tracking (GitHub).** Keywords such as `closes` or `fixes` in a PR or commit link it to an issue, and the issue closes when the PR merges into the default branch. This ties change to tracker status, but only in one direction: nothing checks that a document still referencing an open issue is consistent. [12]

**Client co-editing through external platforms.**
- **Basecamp 3.** Clients are invited into the project, and everything is "private just to your team" by default. Each item is explicitly made client-visible, a reversal of the old visible-by-default model chosen to prevent mistakes. Clients can reply by email without logging in. [13]
- **Basecamp API.** It supports creating, updating and moving card-table cards, so an agent can sync cards programmatically. [14]
- **Jira Service Management.** Portal customers are reportedly free and unlimited and need no agent license. They raise requests by portal or email. This comes from community and FAQ sources, and edge cases with SSO licensing are reported. [15]

## Success factors

1. **Small, atomic records with an ID, status and rationale** (ADR, MADR, issue register). [1][2][3]
2. **Supersede, don't edit:** history is preserved and the current state stays unambiguous. [1][2]
3. **Named ownership and decision authority:** MADR's decision-makers, consulted and informed fields, BABOK's assignment of responsibility, and PRINCE2's formal register. [3][10][8]
4. **Two tiers of formality**, so trivial items do not clog the formal record: PRINCE2's daily log versus its issue register. [8]
5. **A regular review cadence** and validation of assumptions. [5][6]
6. **Low-friction client access:** email replies, a portal, and explicit per-item visibility. [13][15]

## Failure modes

1. **Inaccessible to deciders:** repo and git barriers for non-developers. [1][2]
2. **Log drift:** the register is kept apart from the artefact it governs, so nothing detects stale or contradictory entries. No source found describes automated cross-checking. This is an inference.
3. **Entries become documents or advocacy:** "Mega-ADR", "Sales Pitch", "Fairy Tale". [4]
4. **Late start or no review:** assumptions are discovered false only after the fact. Practitioner claim, uncertain. [6]
5. **Accidental exposure** when platforms default to client visibility. [13]
6. **Split-brain** between an internal tracker and a client platform when sync is manual or ad hoc. This is an inference; no primary source was found.

## Comparison with Wiked's ticket-linked pendências

| Concern | Classic practice | Wiked |
|---|---|---|
| Open question visible in context | A separate RAID log or issue log | A pendência section on the wiki page itself |
| Decision durability | ADR, supersede | Grill-closed decision with provenance; ticket closed with a summary |
| Who decides meaning | Decision-makers field, RACI | A mandatory human grill; agents never decide meaning |
| Log–artefact consistency | Manual review | The validator checks the link and the ticket status |
| Formality tiers | Daily log vs. register | Ticket vs. note; whether this is a real equivalence is unclear |
| Client participation without the repo | Basecamp, JSM portal | External reference on the ticket; an agent syncs on curator request |
| Overview | A RAID dashboard | A curation dashboard per page or trunk |

Gaps to consider:
- An explicit supersede relation for changed decisions, as in ADR and MADR.
- Recording decision-makers and consulted parties on the record (MADR).
- Explicit per-item client visibility when syncing to a platform, private by default as in Basecamp.
- An explicit review cadence for open pendências.
- Assumptions as a first-class category, distinct from open questions.

## Implications for a business-facing value proposition

- Position Wiked as **"a RAID and decision log that cannot drift from the documentation"**. Every open question lives on the page it affects, links to a tracked ticket, and is machine-checked. Wiked keeps the ADR virtues of brevity, status, history and rationale while removing the repo-access barrier through the client's existing platform.
- Clients keep working where they already are, such as Basecamp cards or email replies, and never touch Git. The consultancy keeps an auditable trail from question to human decision to changed wiki text, comparable in function to the PRINCE2 audit trail from concern to decision to baseline.
- Do not overclaim. Value depends on review discipline and on the curator triggering the sync. Sync is on request, not real-time. Visibility rules on the external platform must be designed deliberately.

## Sources

1. Nygard, "Documenting Architecture Decisions", 2011. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
2. Fowler, "Architecture Decision Record" (bliki). https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
3. MADR. https://adr.github.io/madr/
4. Zimmermann, "How to create ADRs — and how not to", 2023. https://ozimmer.ch/practices/2023/04/03/ADRCreation.html
5. Atlassian, RAID log. https://www.atlassian.com/agile/project-management/raid-log
6. Asana, RAID log (vendor). https://asana.com/pt/resources/raid-log
7. PMBOK issue log definition, quoted second-hand. https://www.projectmanagement.com/discussion-topic/52843/-Issues--and--Issue-Log---a-decisive-component-of-Risk-Mgmt---Comm--Plan--Conflict-Mgmt---or-PMBOK-s-entirety-
8. PRINCE2 change theme (secondary). https://prince2.wiki/theme/change
9. PRINCE2 7 issues practice (secondary). https://open-exam-prep.com/study-guides/prince2-practitioner/practices-issues/issues-change-control
10. BABOK v3 Item Tracking (Packt excerpt). https://subscription.packtpub.com/book/data/9781838825263/14/ch14lvl1sec33/item-tracking
11. BABOK v2 technique mapping (EBG). https://www.ebgconsulting.com/Navigator/BABOK%20Navigator-BABOK%20Tech%20ref%20by%20Task.pdf
12. GitHub Docs, linking a PR to an issue. https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue
13. Basecamp, "Launch: A brand new way to work with clients in Basecamp 3". https://signalvnoise.com/svn3/launch-a-brand-new-way-to-work-with-clients-in-basecamp-3/
14. Basecamp API, card table cards. https://github.com/basecamp/bc3-api/blob/master/sections/card_table_cards.md
15. Atlassian, JSM FAQ. https://confluence.atlassian.com/display/SERVICEDESK/Jira+Service+Management+FAQ
