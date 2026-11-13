# Example: a knowledge base for an area

> **Illustrative, not normative.** This example shows how Wiked can be configured for the Knowledge base use case. It is not a recommended configuration or an official template. The organisation and its content are invented. Wiked's rules live in the Wiked distribution and its contract schema.

This example accompanies the [Wiked value proposition](../proposta_de_valor_wiked.md). It describes a synthetic wiki for the delivery department of a services company. Its shape follows the reference instance in which Wiked was created; none of its content does. The complete synthetic wiki passed the Distributed validator of Wiked 1.9.0 with no errors or warnings.

## The Instance contract (excerpt)

The contract below uses a light setting. Content pages need only a type, a state, and a `Sources` section. Process pages also need a diagram, and policy mirrors must state that they are not the official version.

```yaml
contract_version: "1.0"
methodology_version: "1.9.0"
language: en

initial_content:
  title: Delivery operations knowledge base
  purpose: "How the delivery department runs its projects: processes, roles, policies and tools."
  audience: Delivery staff, new hires and agents.
  scope: Delivery operations.

topology:
  trunks: [areas, processes, roles, policies, tools, sources]
  required_trunks: [areas, processes, roles, sources]
  sources_trunk: sources

navigation:
  root_index: index.md
  trunk_index: index.md
  context_file: CONTEXT.md
  intent_map: intents.md

page_types:
  process:
    roles: [knowledge, flow]          # "flow" pages require a diagram
    states: [current, proposed]
    fields: {required: [type, state], optional: [change_ticket], date: []}
    sections: {required: [Sources]}
  external_document:
    roles: [knowledge]
    states: [current, proposed]
    fields: {required: [type, state], optional: [change_ticket], date: []}
    sections: {required: [Sources]}
    external_authority:
      notice: "This page mirrors an external document; it is not the official version."
      link: required
  # area, role and tool follow the same pattern; source pages are shown below.

pendency_tracking:
  roles: [knowledge]
  section: Open questions
  tag: pendency
  valid_statuses: [open, in_progress]
  warning_statuses: [closed]

proposal_tracking:
  roles: [knowledge]
  section: Proposed changes
  tag: proposal
  frontmatter_field: change_ticket
  proposal_state: proposed
```

The full contract also declares naming, frontmatter, provenance record fields, assets, diagrams, ticket identifier patterns, and the severity of each rule.

## A process page (excerpt)

`wiki/processes/project-closure.md` describes how the department works today. Steps name who is responsible. The open question and the proposed change are tickets; the validator checks that each ticket exists, carries the right tag, and is still open.

```markdown
---
type: process
state: current
---
# Project closure

## Purpose

Hand the delivered solution over to the client, run the warranty period, and close
the project in the [Project tracker](../tools/project-tracker.md).

## Trigger

The client accepts the final delivery.

## Flow overview

The diagram complements the steps below, which are the canonical description of the process.

![Project closure flow](./project-closure.svg)

## Steps

### Confirm the support arrangement

The [Project manager](../roles/project-manager.md) checks whether the client has a
support contract. If not, the Project manager asks [Finance](../areas/finance.md) to
offer one before the warranty ends.

- **Responsible:** [Project manager](../roles/project-manager.md)
- **Involved:** client, [Finance](../areas/finance.md).

### Close the project

When the warranty ends, the Project manager records lessons learned and closes the
project in the Project tracker.

- **Responsible:** [Project manager](../roles/project-manager.md)

## Open questions

- [kb-01m7bewf6m5q] Confirm who signs off the end of the warranty period

## Proposed changes

- [kb-01m7bewfa30m] Run a lessons-learned session with the client before closure

## Sources

- [Project closure checklist](../sources/project-closure-checklist.md)
- [Interview with project managers](../sources/interview-project-managers.md)
```

The process diagram (`project-closure.d2` and its rendered `project-closure.svg`) sits next to the page and is not shown here.

## A source page (excerpt)

`wiki/sources/interview-project-managers.md` records where knowledge came from. It lists every page it supports, and the validator checks that each of those pages cites it back.

```markdown
---
type: source
state: indexed
indexed_on: 2026-11-10
---
# Interview with project managers

## Source record

- **Kind:** interview notes.
- **Origin:** interview with two project managers.
- **Scope:** closure, roles and tools.
- **Published:** unknown.
- **Consulted:** 2026-11-10.
- **Indexed:** 2026-11-10.

## Grounded pages

- [Information security policy](../policies/information-security-policy.md)
- [Project closure](../processes/project-closure.md)
- [Project manager](../roles/project-manager.md)
- ...
```

## What this configuration guarantees

- Every content page has a type, a valid state, and sources, and every source page links back to the pages it supports.
- Every open question and proposed change points to an open ticket with the right tag, and every such ticket is cited by a page.
- Process pages have a diagram; policy mirrors carry the authority notice and a link to the official version.
- The intent map (`intents.md`) leads common questions, such as "how do we close a project?", to the pages that answer them.

It does not prescribe how steps or responsibilities are structured inside a page. That is a deliberate light setting. The [consulting-mapping example](./consulting-mapping.md) shows a stricter one.
