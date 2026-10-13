# Wiked

**A Markdown wiki maintained by AI agents, guided by you.**

Turn scattered documents and decisions into connected knowledge that you and
your AI agent can consult and keep up to date.

Inspired by the **LLM Wiki** idea, Wiked puts agents in charge of maintaining the
wiki, not just answering questions about it. You decide what the knowledge means
and approve changes; the agent organizes pages, maintains links and indexes, and
checks structure so updates are not left as isolated edits.

Your knowledge stays in Markdown files in your own repository: an open,
human-readable format, not locked inside a particular tool. Browse it with your
favorite Markdown app, such as Obsidian, or simply open the files and read them
as plain text.

## What could you use it for?

- **Team knowledge:** connect decisions, terminology, and onboarding material.
- **Processes and playbooks:** document how work happens and keep related pages
  aligned when a process changes.
- **Project knowledge:** consolidate selected documents into a wiki you can ask
  questions about, with links to the pages supporting each answer.

For example, ask your agent to incorporate a procedure, review how it relates to
existing pages, and then answer: "Who is responsible for this step, and why?"
When the wiki lacks evidence, the agent reports the gap rather than inventing
an answer.

## Try it in your repository

### 1. Prepare

You need:

- Linux, macOS, or Windows through WSL.
- Bash 3.2+, `curl`, Python 3.11+, and `uv`, plus internet access.
- `knot`, installed below if you don't already have it.
- An AI agent that can use local Markdown skills. Make sure it can discover
  `.agents/skills/wiked/` and the setup command in `.agents/commands/`.

Missing a tool or unsure about agent discovery? See the
[installation guide](./docs/installation.md#before-you-start).

### 2. Install

In a terminal, open the root of the repository where you want your wiki.
Stop any agents currently using Wiked there. [Knot](https://github.com/UniSoma/knot)
tracks the work your agent does on the wiki. Run these commands in order:

```sh
# Install Knot if you don't already have it
curl -fsSL https://raw.githubusercontent.com/UniSoma/knot/main/install.sh | sh

# Initialize tracking if this repository doesn't already use Knot
knot init

# Install Wiked
curl -fsSL https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh | bash
```

If `knot` is not found after installation, follow the installer's instructions
to add `~/.local/bin` to your `PATH` before continuing. Python and `uv` must
already be available; these commands do not install them.

Accept the default `.agents/` location, review the selected release and file plan,
and confirm the installation.

The `curl` commands download and run scripts from `main`; use them only if you
trust their sources. Prefer to inspect and verify them first? See the
[verified-download option](./docs/installation.md#verify-the-installer-first).

### 3. Ask your agent to set up the wiki

Open your agent in the same repository and ask:

> Use the installed Wiked skill to run wiked-setup in this repository. Help me
> define the wiki's purpose, language, and structure before creating it.

The agent uses a setup ticket, asks you to resolve the wiki's design decisions,
and waits for your confirmation before creating and validating its structure.

You now have a wiki structure, not a populated knowledge base. To start adding
knowledge, choose a real source and ask:

> Use Wiked to help me incorporate this document into the wiki.

Wiki changes go through the agent's governed workflow, rather than direct manual
edits. You approve meaning and scope; agents handle the related page updates and
deterministic checks. Validation checks structure, not the truth of your content.

## Learn more

- [Installation guide](./docs/installation.md): prerequisites, agent discovery,
  updates, automation, and recovery.
- [How Wiked works](./distr/agents/skills/wiked/SKILL.md): the agent's workflows
  and operating rules.
- [Architecture and vocabulary](./docs/CONTEXT.md): the distribution, runtime,
  and per-wiki configuration.
- [Governance and development](./docs/metodologia.md): how changes to Wiked itself
  are proposed and validated.
- [Releases](https://github.com/UniSoma/wiked/releases) and
  [distribution contract](./docs/distribution.md): versioning and packaging.
- [Historical research](./reports/README.md): background, not operating instructions.

This repository develops and distributes Wiked; it is not a live wiki. Install
Wiked in your own repository to use it. Contributors should start with
[AGENTS.md](./AGENTS.md) and the [context map](./CONTEXT-MAP.md).
