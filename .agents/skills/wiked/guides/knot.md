# Knot

Load this guide whenever Wiked work requires reading, creating, updating, or closing tickets.

## Interface

- Use the `knot` CLI from the consumer repository root. Never inspect or edit `.tickets/` or equivalent storage.
- Use `knot show <id> --json` for one ticket, `knot list --json` for filtered inventory, and `knot info` for project metadata.
- Mutate through `knot create`, `knot update`, `knot add-note`, `knot start`, and `knot close`; consult `knot <command> --help` before using an uncertain flag.
- Prefer JSON output for decision logic. Read the returned post-mutation ticket instead of immediately fetching it again.
- Never manipulate ticket files with filesystem tools or Git.

Common forms:

```bash
knot show <id> --json
knot list --json
knot create "<result-oriented title>" --description "<context>" --acceptance "<criterion>" --json
knot start <id> --json
knot update <id> --add-ac "<criterion>" --json
knot update <id> --ac <number> --done --json
knot add-note <id> "<durable decision or evidence>"
knot close <id> --summary "<actual outcome>" --json
```

Repeat acceptance flags as needed. Use CLI fields, not hand-written lifecycle or acceptance sections. If the installed command differs, inspect its help instead of guessing.

## Content Work

- Assisted indexing requires an open ticket with explicit sources, expected pages, and acceptance criteria; operator qualification is governed by `grill.md`.
- Tickets record activity, decisions, and acceptance. They are not source pages and never constitute operational evidence.
- Pending items and change proposals use the titles, tags, ID pattern, statuses, section labels, and frontmatter mapping declared by the instance contract.
- Query mode never reads tickets.
- Put lateral discoveries in separate or linked work rather than silently expanding the current objective.

## Closure

1. Verify acceptance criteria and lifecycle gates.
2. Close with a summary of the actual result.
3. If the ticket has external work-item references, process each only after successful local closure.
4. When authorized and capable, record the Knot outcome externally. Changing external lifecycle state requires specific human authorization.
5. If external update is unavailable or fails, notify the supervising human through an available channel.
6. Add a closed-ticket note for each external reference with the update or handoff result. External failure does not undo local closure.
