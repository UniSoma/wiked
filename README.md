# Wiked

Wiked maintains operational knowledge in progressively navigated Markdown,
using an instance contract, human-governed authoring, and a portable validator.
This is the methodology's source tree. Consumer repositories install the
distribution and own their wiki, contract, ingestion material, and governance.

## Start here

- [AGENTS.md](./AGENTS.md) and [context map](./CONTEXT-MAP.md): source authority.
- [Source vocabulary](./docs/CONTEXT.md) and [development workflow](./docs/metodologia.md).
- [Distribution manifest](./.agents/wiked-manifest.yaml): Wiked 1.4.0 and its 16 owned files.
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
Defining product dependency provisioning remains separate future work.

## Distribution and publication

The manifest paths are relative to `.agents/`. Those files are the copyable
product; source tests, `docs/`, research, and agent-authoring context are not
consumer runtime dependencies. Unlisted consumer files must be preserved.

This tree is prepared for a human's first source-repository commit. It does not
assert that a remote repository, release, installer, or update channel exists.
Publication, immutable artifacts, integrity, supported platforms, licensing, and
human installation/update behavior remain separately governed work. The project
metadata version describes the development environment; the manifest is the
authority for the distribution version.
