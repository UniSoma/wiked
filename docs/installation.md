# Installing and updating Wiked

[Back to the README](../README.md)

Install Wiked in the repository where you want to maintain your wiki. This guide
covers the human-run installer; wiki setup happens afterwards with your agent.
The official source is [UniSoma/wiked](https://github.com/UniSoma/wiked), and
versioned downloads are available through
[GitHub Releases](https://github.com/UniSoma/wiked/releases).

## Before you start

Supported environments are Linux, macOS, and Windows through WSL, not native
Windows. Have these tools installed and available in your terminal:

| Tool | Requirement | Used for |
| --- | --- | --- |
| Bash | 3.2 or newer | Running the installer and asking for approval |
| `curl` | HTTPS support | Downloading the installer |
| Python | 3.11 or newer | Installation and validation |
| `uv` | Available on `PATH` | Running Python with the required dependencies |
| `knot` | Available on `PATH` | Tracking setup and governed wiki changes |

The installer checks prerequisites and reports missing tools; it does not install
them. Python must already be present: automatic Python downloads are disabled.
Network access is required; this is not an offline installer.

Archive handling, JSON, SHA-256, file locking, and recovery use Python's standard
library. `uv` resolves PyYAML for the embedded installer and the release's script
dependencies in its cache, not your repository's Python project. Optional
tools are needed only for the diagram, ingestion, or export capabilities you
select during setup or request later.

The Wiked installer does not initialize Git or Knot. For other tool provisioning,
follow each tool's installation instructions; Wiked does not provision your
environment.

### Optional diagram and export tools

[D2](https://d2lang.com/) (`d2` on `PATH`) is optional: install it to create,
validate, or regenerate process diagrams. Reading canonical Markdown or copying
an already accepted SVG does not require D2. Follow D2's installation
instructions; the Wiked installer does not install it.

Export tools depend on the requested format: `pandoc` for DOCX, `pandoc` and
`weasyprint` for PDF, and `rsvg-convert` for SVG-to-PNG conversion or diagram
compatibility where needed. See the
[export guide](../distr/agents/skills/wiked/guides/export.md#dependencies)
for the capability-specific requirements. None is a basic installation prerequisite.

### Agent sandbox

Wiked can run inside an agent sandbox instead of directly on your host. Prepare
the prerequisites above inside the environment where the installer and agent
commands run; tools installed only on the host may not be available there.
Include D2 or export tools only for the capabilities you need.

Mount your intended wiki repository read-write or use a persistent workspace,
and run installation and setup from its root inside the sandbox. Preserve the
whole repository, including the wiki, local Knot tracker, `.agents/` installation,
and `.wiked-install.json`, across sandbox restarts. Follow the
[Knot initialization](#install-and-initialize-knot) and
[agent discovery](#agent-discovery) steps in that same environment; mounting
files does not by itself configure skill discovery.

The source repository's [`.sandbox/Dockerfile`](../.sandbox/Dockerfile) is an
example of provisioning tools for this approach, not a generic Wiked image.
It extends `aishell:foundation` and relies on that base for tools such as `uv`
and Babashka/`bbin`; it adds a version-selected D2 renderer, Knot, document
converters, and the optional Basecamp CLI. Basecamp is not a Wiked prerequisite.
The Dockerfile does not install Wiked or initialize a repository's tracker.
Adapt its provisioning to your sandbox and verify all prerequisites, including
Python 3.11+, rather than assuming another base image supplies them.

A Dockerfile alone does not establish isolation guarantees. Access to files,
network, credentials, and host resources depends on your sandbox's execution
configuration, which remains your responsibility.

### Install and initialize Knot

[Knot](https://github.com/UniSoma/knot) tracks the work your agent does on the wiki.
If you don't already have it, install it in Linux, macOS, or your WSL environment:

```sh
curl -fsSL https://raw.githubusercontent.com/UniSoma/knot/main/install.sh | sh
```

The Knot installer puts its executable in `~/.local/bin/knot` and warns if that
directory is not on `PATH`. If `knot` is not found, follow that warning to add
`~/.local/bin` to your shell's `PATH` before continuing. This installs Knot only,
not Python or `uv`.

From the root of your intended wiki repository, initialize a local tracker if
that repository does not already use Knot:

```sh
knot init
```

This creates the local tracker configuration and ticket directory needed for
agent-assisted setup. Do not rely on a tracker in a parent repository. For
advanced agent integration, see Knot's
[AI-agent integration guide](https://github.com/UniSoma/knot#ai-agent-integration).

### Agent discovery

Use an agent that can load local Markdown skills. The default installation puts
the skill at `.agents/skills/wiked/` and the thin setup adapter at
`.agents/commands/wiked-setup.md`. Ensure your agent discovers both through its
own configuration; installing files does not configure or launch the agent.

For a custom destination, configure skill discovery to include
`<destination>/skills/wiked/` and command discovery to include
`<destination>/commands/wiked-setup.md`. The installer reports both paths.
Arbitrary copying does not establish discovery.

## Interactive installation

Stop agents using Wiked, then run from the **root of your wiki repository**:

```sh
curl -fsSL https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh | bash
```

This option executes the script from mutable `main` **without a download checksum**.
Use it only if you trust that repository and channel. The distribution archive
also has no download checksum. Its inventory and version are validated before
installation, but those checks do not independently authenticate downloaded
content or protect against a compromised script. To inspect before execution,
use the next section.

The installer checks prerequisites and asks for missing values through the
controlling terminal (`/dev/tty`), never the pipe containing the script. Accept
the default `.agents/` destination or enter another directory. The origin is
always `UniSoma/wiked`; there is no origin argument or repository question.

It selects and validates the latest stable release once, then asks whether to
continue with that version. There is no older-version selection. Inspect the
displayed file plan and answer `yes` to approve it. Providing a value skips its
question, not its validation or the plan approval.

## Inspect the installer first

Instead of executing the piped Wiked script immediately, download
`main/scripts/install-wiked.sh` into a new local directory and inspect its contents.
This is inspection, not checksum verification or independent authentication.
The release does not provide a separate installer asset.

For example, download into a fresh temporary directory:

```sh
installer_dir=$(mktemp -d)
curl -fsSL https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh \
  -o "$installer_dir/install-wiked.sh"
less "$installer_dir/install-wiked.sh"
```

After inspection, from your wiki repository root, preview the installation and
then run the downloaded script:

```sh
bash "$installer_dir/install-wiked.sh" --dry-run
bash "$installer_dir/install-wiked.sh"
```

Each invocation pins the latest stable release, validates the archive inventory
and version, and displays additions, replacements, removals, local edits, and
unowned collisions. Answer `yes` to approve the operation.

## Set up your wiki

After installation, open your agent in the same repository and ask:

> Use the installed Wiked skill to run wiked-setup in this repository. Help me
> define the wiki's purpose, language, and structure before creating it.

Setup uses a local open Knot ticket and asks you to confirm that you are qualified
to govern the wiki's objective. The agent helps you decide its purpose, audience,
language, terminology, structure, and provenance rules. It summarizes those
decisions and waits for your explicit confirmation before writing.

It then creates and validates the agreed wiki structure and its local
`wiki/wiki-structure.yaml` configuration. It does not invent domain pages or
populate the wiki with fictional knowledge. Choose real source material for a
subsequent assisted-indexing request.

Installation itself creates no domain content or agent session. Operate your wiki
through its installed skill and local configuration, not this source repository's
development documents.

## Updates and existing files

Updating uses the same installation command. Stop agents using Wiked first.
An intact installation of the selected version is a no-op; damaged or edited
files produce a reinstall plan.

Before replacing an existing installation, the candidate validates your local
wiki configuration without reading wiki pages or querying Knot. An incompatible
configuration blocks the update; the installer never migrates or changes your
configuration or wiki.

After every successful change of installed version, run a maintenance agent using
the installed Wiked skill and your local contract to review content against the
new methodology. The installer displays this required next step but never starts
an agent. Its contract-only preflight does not establish content conformity.
Corrections or contract migration require separately authorized scope and a closed
grill; an update does not authorize them. First installation retains the setup
instruction; same-version repair and intact no-op do not trigger this review.
In 1.5.0, the intent map remains optional: maintenance does not imply adopting it.
The [README maintenance prompt](../README.md#update-and-review-an-existing-wiki)
starts this review without authorizing edits. The installed changelog covers the
1.4.1 baseline onward and distinguishes methodological impacts from internal
changes; no-impact releases still receive the ordinary maintenance review.

A priority-1, human-in-the-loop migration ticket is offered only if both
`.knot.edn` and `.tickets/` already exist locally, not through symlinks. Ticket
creation requires separate approval; `--yes` never approves it. Without a local
tracker, follow the displayed migration guidance manually. Runtime or prerequisite
failures block the update without offering a migration ticket.

After approval, `knot info --json` must prove that the config, tracker root, ticket
directory, and archive resolve within your repository; external redirects are
rejected. Knot must support this JSON paths interface and the
`create --priority --mode --description` options (verified with Knot 0.14.0).

`.wiked-install.json` records the installed version, owned inventory, baseline
hashes, and `maintenance_since`: the oldest version still awaiting review,
exclusive, through the installed version, inclusive. A first install sets it to
null; a version change starts or extends the range. Legacy metadata without this
field uses the recorded version as the new range's start, but cannot prove that
earlier reviews happened. Same-version repair and no-op preserve pending review.
Invalid pending-range metadata blocks updates rather than silently clearing it.
Modified Wiked files may be replaced after approval; intact owned obsolete
files may be removed. Modified obsolete files and all unlisted files are preserved.
Your wiki, configuration, ingestion material, governance, and unrelated agent
files remain yours.

Missing metadata produces a warning and separate collision approvals rather than
assumed ownership. Invalid metadata likewise proves no ownership and cannot
authorize obsolete-file deletion. Taking over an unowned file requires a separate
interactive confirmation or repeatable `--approve-collision <manifest-relative-path>`
options. Approval never claims the parent directory or adjacent third-party files.

### Acknowledge a maintenance review

After the agent completes the review, decide the disposition of findings and
record follow-ups, including consumer-local Knot correction tickets where
appropriate. Corrections may remain pending; acknowledgment means the analysis
and human disposition are complete, not that the wiki is conformant. An analysis
failure leaves the review pending.

Stop agents and run the downloaded installer with the exact reviewed installed
version (replace `X.Y.Z` below):

```sh
bash /path/to/downloaded/install-wiked.sh --acknowledge-maintenance-review X.Y.Z
# Include --destination /path/to/installation if customized.
```

This separate human-confirmed operation downloads nothing and changes only
installation metadata through the same recovery journal, not wiki, contract,
skill, or tickets. `--yes` explicitly confirms this acknowledgment without a
terminal; `--dry-run` leaves it pending. A stale version, manifest/metadata
disagreement, unreliable baseline, or interrupted transaction blocks it. No-op
and repair may remind you of an existing pending range, but never acknowledge it.
Report records and correction tickets remain consumer governance, not operational
evidence or installer-owned content.

## Automation and custom destinations

The same entrypoint supports explicit approval without a terminal:

```sh
bash /path/to/downloaded/install-wiked.sh --yes
```

`--yes` approves the selected latest stable version and the displayed operation
plan, not unowned collisions or migration tickets. Without `--yes`, installation
requires a controlling terminal; piped `yes` is never interpreted as consent.
`--dry-run` does not ask for approval or change installed files or tickets.

The destination defaults to `.agents/` with `--yes`, `--dry-run`, or `--recover`.
Use `--destination /path/to/installation` to preserve the same manifest,
`skills/wiked/`, and `commands/` tree elsewhere; its parent must already exist.
The wiki repository root remains the invocation directory, not the installation
path. Configure [agent discovery](#agent-discovery) for a custom destination.
Symlink/hard-link targets and wiki, ingestion, tracker, or Git destinations are
rejected.

Automation can explicitly pass `--approve-migration-ticket` to authorize a ticket
on incompatibility. This never approves installation or migration and has no
effect in a dry run. Collision approval remains separate as described above.

## Interrupted installation and recovery

The user must run installation, update, and recovery one operation at a time.
Concurrent operations are unsupported and are not prevented by the installer.
Run `--recover` only after the previous operation has stopped.
Temporary backups and a durable journal live in the sibling
`.<destination-name>.wiked-transaction/`.

Handled failures restore affected files, permissions, metadata, and newly created
empty directories. After an abrupt interruption, another install is blocked until
explicit recovery:

```sh
bash /path/to/downloaded/install-wiked.sh --recover
# Include the same --destination value if it was customized.
```

Recovery requires no release download and restores the previous installation,
or cleans an already committed transaction. Corrupted backups block recovery
and remain available for human investigation; do not delete the transaction to
bypass this protection. Backups are temporary, not permanent version history.
Dry runs leave installed files and tickets untouched.

## Distribution and release format

The copyable product lives in `distr/agents/` in the Wiked source repository,
outside automatic skill discovery. The
[distribution manifest](../distr/agents/wiked-manifest.yaml) declares its version
and exact ownership. Manifest paths are relative to that source directory and to
the installation directory in your repository. Source tests, `docs/`, research,
and agent-authoring context are not consumer runtime dependencies.

The release interface uses a stable SemVer tag `vX.Y.Z` (or `X.Y.Z`) and a single
asset, `distr.tar.gz`. The installer comes directly from `main/scripts/install-wiked.sh`,
not a release asset. No download checksum is required. Asset URLs are immutable versioned
`https://github.com/UniSoma/wiked/releases/download/<tag>/<filename>` URLs,
not mutable latest-download aliases.

The archive contains only unique regular files, exactly the manifest's inventory,
with names relative to its root: no directory entries, `./` prefix, links, or
enclosing directory. The installer checks the manifest's namespace, version,
entrypoint, preservation policy, and release declarations. The runtime reads its
version from the manifest through the bundled distribution module. The manifest is the
distribution-version authority; the Python project's version describes the
source development environment.

Starting with the published 1.4.1 distribution, the archive includes
`skills/wiked/LICENSE`: MIT, Copyright (c) 2026 UniSoma. External dependencies and
tools are not bundled and retain their own licenses. Consumer content is not
licensed by Wiked. The previously published 1.4.0 omitted the license file;
the maintainer published the correction as a new version, not a replacement asset.

### Prepare the release package

From the Wiked source tree corresponding to the intended release tag, run:

```sh
uv run pytest
bash scripts/package-wiked.sh
```

The packaging command reads the version from the sole manifest authority and
validates the inventory and changelog declarations, then
creates only `distr.tar.gz` in a new temporary directory and prints its path. It
does not run tests, install Wiked, change versions, operate Git, or publish a release.
It can be called from another directory using an absolute script path.
For a chosen output directory, use:

```sh
bash scripts/package-wiked.sh --output /path/to/release-output
```

Existing output archives are never overwritten. Upload only `distr.tar.gz` as an
asset of the matching stable GitHub release; GitHub's automatic source archives
are not installation packages. Keep published artifacts immutable and use a new
version for corrections. Version management remains separate from packaging.
The command prints the matching publication tag without requiring a version
argument. It cannot inspect or create a Git tag; humans publish only the matching
tag and immutable artifact.
For the increment and changelog policy, see the distribution contract's
[version authority](./distribution.md#version-authority-and-increments).

[The 1.4.1 correction](https://github.com/UniSoma/wiked/releases/tag/v1.4.1) was
published by `volneids` on 2026-10-13 at 02:45:45 UTC. Its only attached asset is
`distr.tar.gz`, with 17 manifested regular files verified against the tested source
and published tag. The official main installer and MIT license are available.
Future releases follow the same human publication boundary. Do not reuse an older archive.
Record the release URL, publisher, publication time, tag, and attached inventory
as publication evidence. Local packaging or tests do not establish publication.
Immutability is a maintainer commitment; platform-enforced immutability is not
required for this delivery.

See the [publication and distribution contract](./distribution.md) for the
source-development requirements behind this interface.
