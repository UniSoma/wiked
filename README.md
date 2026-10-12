# Wiked

Wiked maintains operational knowledge in progressively navigated Markdown,
using an instance contract, human-governed authoring, and a portable validator.
This is the methodology's source tree, not an operational wiki or a consumer.
Consumer repositories install the
distribution and own their wiki, contract, ingestion material, and governance.

## Start here

- [AGENTS.md](./AGENTS.md) and [context map](./CONTEXT-MAP.md): source authority.
- [Source vocabulary](./docs/CONTEXT.md) and [development workflow](./docs/metodologia.md).
- [Distribution manifest](./distr/agents/wiked-manifest.yaml): Wiked 1.4.0 and its 16 owned files.
- [Publication and distribution contract](./docs/distribution.md): approved release and installer requirements.
- [Historical research](./reports/README.md): preserved research, not an approved product specification.

## Development

Use Python 3.11 or newer through `uv`. Project dependencies and the test runner
are declared in `pyproject.toml` and locked in `uv.lock`. The distributed runtime
declares its own script dependencies. First execution may require network access.

```sh
uv run pytest
```

The default suite uses synthetic consumer fixtures and a Knot test double. It
needs no operational wiki, real tracker, domain data, credentials, or parent
repository. One optional real-consumer integration test is skipped by default.
To opt in, supply an absolute consumer root (with its contract and Knot CLI):

```sh
WIKED_CONSUMER_ROOT=/absolute/path/to/consumer uv run pytest -m integration
```

Read-only methodological review requires no ticket. Do not load or require the
environment-provided `grilling` skill unless the requester asks to qualify the
objective; that exception requires a Methodological grill. Otherwise, an
unavailable skill does not block review.

Methodology changes, including changes arising from review, require an approved
open ticket and explicit Methodological grill closure before editing. Follow the
[source development workflow](./docs/metodologia.md). Governed authoring requires
the environment-provided `grilling` skill; ticket operations require the `knot`
skill and CLI. These skills are not vendored into the distribution. Initialize
and migrate source governance manually into this repository before further
governed development.

The requester-provided `.aishell/Dockerfile` is retained as a sandbox environment.
It is not part of the distribution manifest or a normative dependency inventory.
Product prerequisite handling is defined in the publication and distribution
contract; the human installer checks its own prerequisites before installation.

## Distribution and publication

The distribution source lives in `distr/agents/`, outside automatic agent skill
discovery. Manifest paths are relative to that directory at source and to
the installation directory (by default `.agents/`) in a consumer. The approved
installer supports a custom destination with the same relative tree and
relocatable skill references. Those files are the copyable
product; source tests, `docs/`, research, and agent-authoring context are not
consumer runtime dependencies. Unlisted consumer files must be preserved.

The official source is [UniSoma/wiked](https://github.com/UniSoma/wiked), with
versioned downloads through its [GitHub Releases](https://github.com/UniSoma/wiked/releases). The
[approved contract](./docs/distribution.md) defines immutable SemVer releases,
MIT licensing, manifested archives, SHA-256 verification, and human-run
installation. This decision does not assert that a release or installer has
already been published. The project metadata version describes the development
environment; the manifest is the authority for the distribution version.

### Installing Wiked

The human entrypoint is [`scripts/install-wiked.sh`](./scripts/install-wiked.sh).
It is implemented and tested against synthetic releases. The maintainer confirmed
the public repository `UniSoma/wiked`, whose default branch is `main`.
**Publication is pending:** the installer path and release artifacts are not yet
publicly available. The commands below are for use after development is finalized
and published; the publication executor must verify their availability and supply
versioned artifact download/verification commands before announcing the release.

Supported environments are Linux, macOS, and Windows through WSL (not native
Windows). Prepare Bash >=3.2, `curl` with HTTPS support, `uv`, `knot`, and Python
>=3.11 yourself. Bash's `command` and standard shell facilities are sufficient;
archive handling, JSON, SHA-256, file locking, and recovery use Python's standard
library. `uv` resolves PyYAML for the embedded installer and the candidate's
PEP 723 dependencies in its cache, not the consumer's Python project. Missing
Python is an error: automatic Python downloads are disabled. No external tool
is installed, and neither Git nor Knot is initialized. Converters remain optional
according to the ingestion capabilities selected during setup. Network access is
required; this is not an offline installer.

#### Option 1: direct, interactive installation

After the installer and stable release are published, stop agents using Wiked,
then run from the **consumer repository root**:

```sh
curl -fsSL https://raw.githubusercontent.com/UniSoma/wiked/main/scripts/install-wiked.sh | bash
```

This simplest entry executes the script from mutable `main` **without verifying
the script itself first**. Use it only if you trust that repository and channel.
The distribution archive is still verified before extraction and installation;
those checks cannot protect you against a compromised script already running.

The Bash layer checks prerequisites and asks for missing values using the
controlling terminal (`/dev/tty`), never the pipe containing the script. Accept
the default `.agents/` destination or enter another directory. The origin is
always `UniSoma/wiked`; there is no origin argument or repository question.
Python selects and validates the latest stable release once, and Bash
asks whether to continue with that version. There is no older-version selection.
After validation, inspect the displayed file plan and answer `yes` to approve it.
Providing a value skips its question, not its validation or the plan approval.

#### Option 2: verify the downloaded installer first

Download the installer and `SHA256SUMS` from the same verified **versioned** HTTPS
release. Compute the installer's SHA-256 using `sha256sum install-wiked.sh`
(Linux/WSL) or `shasum -a 256 install-wiked.sh` (macOS), and compare the entire
digest to its exact entry in `SHA256SUMS` before execution. These checks provide
integrity, not an independent publisher signature. Exact download links remain
the publication executor's responsibility.

```sh
bash /path/to/verified/install-wiked.sh --dry-run
bash /path/to/verified/install-wiked.sh
```

The installer resolves GitHub's latest stable release once per invocation, pins
it, validates the archive hash before extraction, and displays additions,
replacements, removals, local edits, and unowned collisions. Answer `yes` to
approve the operation. `--yes` is an explicit noninteractive operation approval,
but does not approve collisions or migration-ticket creation. Taking over an
unowned file requires a separate interactive confirmation or repeatable
`--approve-collision <manifest-relative-path>` options. Approval never claims the
parent directory or adjacent third-party files.

#### Automation

The same entrypoint accepts explicit parameters and approvals without a terminal:

```sh
bash /path/to/verified/install-wiked.sh --yes
```

`--yes` approves continuing with the selected latest stable version and the
displayed operation plan; it never approves unowned collisions or migration
tickets. Omitted destination defaults to `.agents/` with `--yes`, `--dry-run`, or
`--recover`. Without `--yes`, installation requires a controlling terminal;
stdin text such as piped `yes` is never interpreted as consent. `--dry-run`
does not ask for approval or change installed files/tickets.

The default manifest-relative destination is `.agents/`; automation needs no
destination argument to accept that default. Use
`--destination /path/to/installation` to preserve the same manifest,
`skills/wiked/`, and `commands/` tree elsewhere; its parent must already exist.
The consumer root remains the invocation directory, not the installation path.
For custom destinations, configure your agent's skill discovery to include
`<destination>/skills/wiked/` and its command discovery to include
`<destination>/commands/wiked-setup.md`; the installer reports both paths but
does not configure or launch the agent. Arbitrary copying does not establish
discovery. Symlink/hard-link targets and consumer wiki, ingestion, tracker, or
Git destinations are rejected.

Updating uses the same command. Candidate contract-only validation blocks
incompatible replacements without reading wiki pages or querying Knot. A
confirmed P1 HITL migration ticket is offered only if both `.knot.edn` and
`.tickets/` already exist locally (not through symlinks); `--yes` never approves
that ticket. A human can approve it separately at the terminal; automation can
explicitly pass `--approve-migration-ticket`. This only authorizes a ticket on
incompatibility, never installation or migration, and has no effect in a dry run.
After approval, `knot info --json` must prove that the config,
tracker root, ticket directory, and archive resolve within the consumer; redirects
outside it are rejected. Knot must support this JSON paths interface and the
`create --priority --mode --description` options (verified with Knot 0.14.0).
Without a local tracker, follow the displayed migration guidance
manually. Runtime/prerequisite failures block the update without offering a
migration ticket. The installer never migrates or changes the contract or wiki.

`.wiked-install.json` records the installed version, owned inventory, and baseline
hashes. Modified Wiked files may be replaced after approval; intact owned obsolete
files may be removed, but modified obsolete and all unlisted files are preserved.
An intact installation of the selected version is a no-op; damaged or edited
files produce a reinstall plan. Missing metadata produces a warning and separate
collision approvals rather than assumed ownership. Invalid metadata likewise
proves no ownership and cannot authorize obsolete-file deletion.

A sibling `.<destination-name>.wiked-lock` provides concurrency exclusion. It
remains as a reusable lock file and must not be unlinked during operations.
Temporary backups and a durable journal live in the sibling
`.<destination-name>.wiked-transaction/`. Handled failures restore affected files,
permissions, metadata, and newly created empty directories. After an abrupt
interruption, another install is blocked until explicit recovery:

```sh
bash /path/to/verified/install-wiked.sh --recover
# Include the same --destination value if it was customized.
```

Recovery requires no release download and restores the previous installation,
or cleans an already committed transaction. Corrupted backups block recovery
and remain available for human investigation; do not delete the transaction to
bypass this protection. Backups are temporary, not permanent version history.
Dry runs leave installed files and tickets untouched; the reusable sibling lock
may be created to exclude concurrency.

After success, begin agent-assisted `wiked-setup` with the installed skill and
consumer contract. Installation itself creates no domain content or agent session.

### Release packaging interface

The publication executor supplies a stable SemVer GitHub Release tagged `vX.Y.Z`
(or `X.Y.Z`), `wiked-X.Y.Z.tar.gz`, the separately downloadable
`install-wiked.sh`, and `SHA256SUMS`. Checksums use ordinary SHA-256 utility
output (`<64 hex digits>  <filename>`). Asset URLs must be immutable versioned
`https://github.com/UniSoma/wiked/releases/download/<tag>/<filename>`
URLs, never mutable latest-download aliases.

The archive contains **only unique regular files**, exactly the manifest's
inventory, with names relative to its root (no directory entries, `./` prefix,
links, or enclosing directory). The manifest's namespace, version, entrypoint,
preservation policy, and runtime version are checked before installation. Tests
demonstrate this interface without publication or consumer-specific fixtures.
