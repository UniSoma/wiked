# Example: consulting mapping

> **Illustrative, not normative.** This example shows how Wiked can be configured for the Consulting mapping use case. It is not a recommended configuration or an official template. The client and its content are invented. Wiked's rules live in the Wiked distribution and its contract schema.

This example accompanies the [Wiked value proposition](../proposta_de_valor_wiked.md). It maps the order intake of a fictional client: processes, business rules, data sources, analytical tools, stakeholders, and gaps. The complete synthetic wiki passed the Distributed validator of Wiked 1.9.0 with no errors or warnings.

## The Instance contract (excerpt)

The contract below uses a strict setting. Besides page types and states, it declares **structured sections**: record formats with named fields, permitted value types, and cardinalities that the validator enforces.

```yaml
contract_version: "1.0"
methodology_version: "1.9.0"
language: en

topology:
  trunks: [processes, rules, data, tools, stakeholders, gaps, sources]
  sources_trunk: sources

page_types:
  process:
    roles: [knowledge, flow]
    states: [current, proposed]
  gap:
    roles: [knowledge]
    states: [open, addressed, accepted, proposed]
  # business_rule, data_source, analytical_tool and role follow the same pattern.

structured_sections:
  - section: Activities
    page_types: [process]
    min_records: 1
    max_records: null
    fields:
      - {name: Accountable, value_types: [page], min_items: 1, max_items: 1}
      - {name: Responsible, value_types: [page], min_items: 1, max_items: null}
      - {name: Consulted, value_types: [page], min_items: 0, max_items: null, empty_value: Nobody.}
      - {name: Data sources, value_types: [page], min_items: 0, max_items: null, empty_value: None.}
      - {name: Rules, value_types: [page], min_items: 0, max_items: null, empty_value: None.}
  - section: Profile
    page_types: [data_source]
    min_records: 1
    max_records: 1
    fields:
      - {name: Owner, value_types: [page], min_items: 1, max_items: 1}
      - {name: Steward, value_types: [page], min_items: 0, max_items: null, empty_value: Not assigned.}
  # SIPOC (process), Rule (business_rule), Profile (analytical_tool) and Gap (gap) are declared the same way.
```

The full contract also declares navigation, naming, provenance, diagrams, the remaining fields of each record (such as `Informed` and `Tools`), ticket tracking for open questions and proposed changes, and the severity of each rule.

## A process page (current operation)

`wiki/processes/order-intake.md` records how orders are handled today. Each activity names exactly one accountable role; empty responsibilities are stated, not omitted. Activities link to the data sources, rules, and tools they use.

```markdown
---
type: process
state: current
---
# Order intake

How customer orders are received and released today.

![Order intake flow](./order-intake.svg)

## SIPOC

### Order intake scope

- **Suppliers:** Customers
- **Inputs:** Purchase order
- **Outputs:** Released order
- **Customers:** [Finance manager](../stakeholders/finance-manager.md)

## Activities

### Register the order

- **Accountable:** [Sales desk](../stakeholders/sales-desk.md)
- **Responsible:** [Sales desk](../stakeholders/sales-desk.md)
- **Consulted:** Nobody.
- **Informed:** Nobody.
- **Data sources:** [Customer master](../data/customer-master.md)
- **Rules:** None.
- **Tools:** None.

### Check credit

- **Accountable:** [Finance manager](../stakeholders/finance-manager.md)
- **Responsible:** [Credit analyst](../stakeholders/credit-analyst.md)
- **Consulted:** [Sales desk](../stakeholders/sales-desk.md)
- **Informed:** Nobody.
- **Data sources:** [Customer master](../data/customer-master.md)
- **Rules:** [Credit limit check](../rules/credit-limit-check.md)
- **Tools:** [Sales dashboard](../tools/sales-dashboard.md)

## Open questions

- [cli-01m7bev8w073] Confirm who approves credit exceptions

## Proposed changes

- [cli-01m7bev8zkwh] Automate credit analysis at order intake

## Sources

- [Interview with the sales desk](../sources/interview-sales-desk.md)
```

The proposed future state has its own page, `order-intake-proposed.md`, with `state: proposed` and the same change ticket in its frontmatter. Each process page has a diagram next to it, not shown here.

## A gap page

`wiki/gaps/missing-credit-history.md` records a data gap relative to the use that needs the data, with an owner who answers for it.

```markdown
---
type: gap
state: open
---
# Missing credit history

## Gap

### Missing credit history

- **Kind:** Completeness
- **Affects:** [Customer master](../data/customer-master.md)
- **Impacts:**
  - [Credit limit check](../rules/credit-limit-check.md)
  - [Sales dashboard](../tools/sales-dashboard.md)
- **Cause:** Payment history is kept in spreadsheets outside the ERP.
- **Owner:** [Finance manager](../stakeholders/finance-manager.md)

## Sources

- [Interview with the sales desk](../sources/interview-sales-desk.md)
```

## What this configuration guarantees

- An activity with two accountable roles, or with none, is reported as an error.
- An omitted field is an error; an empty one must say so explicitly (`Nobody.`, `None.`, `Not assigned.`).
- Every data source has exactly one owner, and every gap has an owner, a cause, and what it affects and impacts.
- Every open question and proposed change points to an open ticket with the right tag; a closed one produces a warning.
- Every statement is grounded in a source page, and every source page lists the pages it supports.

## What it does not guarantee yet

These checks are tracked as improvements to Wiked (*Evolving* in the value proposition):

- that a `Rules` field links to a business rule rather than, say, a stakeholder page;
- that links are reciprocal, for example that a rule's `Applies to` process also cites the rule;
- that every current process has a proposed version or an explicit "no change" decision, and that the two can be compared side by side.

The contract guarantees the form of the map. Whether the map is true is decided by the people interviewed and confirmed in each decision interview.
