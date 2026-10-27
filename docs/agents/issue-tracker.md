# Issue tracker: Knot

Issues and specs for this repo live in the local Knot tracker configured by
`.knot.edn`. Use the `knot` skill and CLI for every operation; never read or
edit `.tickets/` directly. Run `knot help <command>` for flags and examples.

## Conventions

- **Create an issue**: `knot create "<title>" -d "..."`, with `--acceptance`
  (repeatable) for acceptance criteria. Use a quoted heredoc for multi-line text.
- **Read an issue**: `knot show <id>`.
- **List issues**: `knot list`, `knot ready`, or `knot blocked`, with filters such
  as `--type`, `--tag`, or `--assignee`; add `--json` for machine-readable output.
- **Comment on an issue**: `knot add-note <id> "..."`.
- **Close**: `knot close <id> --summary "..."`.

Source changes also require the governance in `AGENTS.md`: an approved open
ticket and a closed Methodological grill before governed content is edited.

## When a skill says "publish to the issue tracker"

Create a Knot ticket with `knot create`.

## When a skill says "fetch the relevant ticket"

Run `knot show <id>`.
