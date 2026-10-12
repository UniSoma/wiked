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
contract; implementing it remains executor work.

## Distribution and publication

The distribution source lives in `distr/agents/`, outside automatic agent skill
discovery. Manifest paths are relative to that directory at source and to
the installation directory (by default `.agents/`) in a consumer. The approved
installer will also support a custom destination with the same relative tree;
relocatable skill references and agent discovery instructions remain executor
work. Those files are the copyable
product; source tests, `docs/`, research, and agent-authoring context are not
consumer runtime dependencies. Unlisted consumer files must be preserved.

The official source and release channel are GitHub and GitHub Releases. The
[approved contract](./docs/distribution.md) defines immutable SemVer releases,
MIT licensing, manifested archives, SHA-256 verification, and human-run
installation. This decision does not assert that a release or installer has
already been published. The project metadata version describes the development
environment; the manifest is the authority for the distribution version.

### Installing Wiked

The approved entry path is README instructions, a deterministic installer invoked
by the user, and agent-assisted wiki setup in the consumer repository. Installer
implementation and verified download commands are pending; the publication
executor must add the exact official links and commands before announcing the
first release.

Prepare `uv` and `knot` yourself. Supported targets will be Linux, macOS, and
Windows through WSL. The installer selects the latest stable release, shows its
version and planned changes, and requires approval before overwriting files.
The default destination is `.agents/` from the consumer repository root; a custom
destination preserves the same tree and requires configuring agent discovery.
Other contents of that directory remain consumer-owned. Converters are optional
according to the ingestion capabilities selected during setup.

Updating uses the same installer and checks contract compatibility before
replacement. It may overwrite approved local modifications to Wiked files, but
does not migrate the wiki or its contract. See the contract for collisions,
recovery, and the optional migration-ticket flow.
