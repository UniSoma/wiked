# Publication and distribution contract

This source-development contract was approved through the Methodological grill
for `wik-01m2tphwrc4f` on 2026-10-10, with the interactive-entry amendment explicitly
approved for `wik-01m4s6rgnfhr` on 2026-10-12 and the packaging simplification
explicitly approved for `wik-01m4sbvndyah` on 2026-10-13. The latter supersedes
versioned archive names, separate installer assets, and download checksums.
It governs release and installer work;
installer verification uses synthetic releases and does not establish publication. It is not an
installed skill dependency or authority to operate a consumer wiki.

## Audience, authority, and delivery

Initial consumers are a controlled audience. The repository README must also
enable an independent user to discover Wiked, install its distribution, and then
start agent-assisted wiki setup in their own repository.

The maintainer, Volnei Santos, decides methodology versions and approves releases.
The canonical source is [UniSoma/wiked](https://github.com/UniSoma/wiked), confirmed
by the maintainer through the Methodological grill for `wik-01m4s7m8f01s` on
2026-10-12. The public repository's default branch is `main`; versioned downloads
belong to its [GitHub Releases](https://github.com/UniSoma/wiked/releases).
The first human publication, [v1.4.0](https://github.com/UniSoma/wiked/releases/tag/v1.4.0),
was published by `volneids` on 2026-10-13 at 01:02:42 UTC with only `distr.tar.gz`.
The official main installer and archive were observed available; the maintainer
confirmed authorized publication and independent author custody in the
Methodological grill for `wik-01m4khsrmqya`. That archive omitted the MIT license.
The approved correction is 1.4.1, without replacing the published 1.4.0 artifact.
Preparation of 1.4.1 is not evidence of its publication. Release
preparation must verify the documented download paths before announcing them;
never infer repository authority from schema IDs.
The maintainer explicitly approved `wik-01m4s821zj1m` to make `UniSoma/wiked` the
installer's only release origin. Do not expose an origin argument or ask users
to choose a repository. Synthetic tests intercept transport for the official
URLs rather than introduce a configurable alternative origin.
Humans operate Git and publish releases. Agents prepare and verify release material
without installing tools on the host or replacing their running skill.

Wiked's own code and instructions use the [MIT License](../LICENSE),
Copyright (c) 2026 UniSoma. The identical distributed license is explicitly owned
as `skills/wiked/LICENSE`. External runtime dependencies and optional tools are
resolved separately, not vendored in the archive, and retain their own licenses.
The inventory review found no bundled third-party code requiring a separate notice.
This grant does not assert rights over historical source material, third-party
works, or consumer content; historical research remains unmodified.

Delivery order is this approved contract, implementation and synthetic testing of
the installer, then preparation and human publication of the first release.
Installer tests must not require an already published release or a real consumer.

## Artifact, version, and validation

- Each release provides only `distr.tar.gz`, containing exactly the files owned by
  `distr/agents/wiked-manifest.yaml`. The installer is downloaded directly from
  `main/scripts/install-wiked.sh`; no installer asset or download checksum is required.
- The archive preserves the manifest-relative tree. Source tests, research, and
  development documentation are not installed runtime dependencies.
- Wiked owns the namespaced manifest and the paths it lists, not the whole
  installation directory. Unlisted consumer and third-party files are preserved.
- Distribution versions use SemVer. Published versions and their artifacts are
  immutable; corrections require a new version. Prereleases may use `-rc.1` and
  are excluded from automatic stable-release selection.
- Immutability is the maintainer's commitment not to replace published artifacts;
  GitHub platform enforcement is not required for this delivery.
- The maintainer approved source distribution 1.4.1 to deliver the missing license.
  Its matching release tag is `v1.4.1`; human publication remains pending.
  The manifest and runtime version must agree. The development
  environment's project version is not the distribution version.
- An invocation resolves the latest stable official release once, displays its
  version, and pins that selection through the entire operation. It records the
  installed version. Selecting older releases or offering downgrade is outside
  the initial installer interface.
- Downloads use HTTPS without download checksum verification. The README presents
  direct `curl ... | bash` execution first, followed by an option to download and
  inspect the main installer before execution. Users must trust the repository
  and download channel. Inventory and version checks do not independently
  authenticate the package or protect against a compromised running script.
  Version pinning, release immutability, and local installation baseline hashes
  remain required; independent signing is deferred.
- `scripts/package-wiked.sh` validates source inventory and manifest/runtime version
  agreement, then creates only `distr.tar.gz`. Default output is a fresh temporary
  directory; `--output` selects a directory. Existing archives must not be
  overwritten. The script does not run the test suite, install, publish, operate
  Git, or increment versions. Packaging uses the source matching the intended tag.

## Installation interface and prerequisites

The deterministic Bash installer is invoked by a human following the README.
Initial supported environments are Linux, macOS, and Windows through WSL; native
Windows is outside the first delivery. Installation requires network access to
the official release channel; an offline bundle is not part of this delivery.

The existing script provides two usages, not a separate bootstrap: Bash owns
human questions and confirmations; Python owns release selection, validation,
planning, and transactional execution. Ask for a missing destination
through the controlling terminal, never stdin, which may contain
the piped script. Supplied values bypass questions, not authoritative validation.
Display and confirm only the selected latest stable version; do not introduce
older-version selection. Keep that selection, candidate, and plan in one
operation through final approval. The operation-level approval follows Python's
displayed plan, not merely the initial parameter questions.

Automation supplies parameters and explicit approval options through the same
interface. `--yes` approves the selected stable version and operation plan, not
collisions or migration tickets. Without a controlling terminal, installation
requires explicit approvals; stdin text is never consent. Dry runs and explicit
recovery remain available without a terminal or installation approval. Defaults
may be accepted through explicit noninteractive invocation. Preserve all
ownership, compatibility, concurrency, and recovery checks in both usages.

Both `uv` and `knot` must already be available before any distribution artifacts
are installed. The installer checks prerequisites and explains missing tools; it
does not install external tools or initialize Git or Knot. Runtime prerequisites
follow the candidate runtime metadata, currently Python >=3.11. Converters are
optional and required only for the ingestion capabilities selected during setup.
The implementation must document and test the shell and utility requirements
used on the supported platforms.

The usual invocation runs from the consumer repository root and installs into
`.agents/` there. A user may specify another installation directory, which
replaces `.agents/` as the manifest-relative root, not merely the skill directory.
Keep `skills/wiked/`, `commands/`, and the manifest in their relative positions.
Keep the consumer repository root distinct from the installation directory.

Internal references must resolve from the installation rather than assume
`.agents/`. For custom destinations, the installer reports installed paths and
the README explains that the user must configure their agent's discovery of the
skill and adapter. Copying to an arbitrary directory does not establish discovery.

Provide a dry run and display the selected version, destination, additions,
replacements, and removals before asking for one operation-level confirmation.
An explicit noninteractive approval option authorizes the same displayed plan
and checks; it must not weaken ownership or compatibility rules.

## Existing files, updates, and recovery

Record the installed release, owned paths, and baseline hashes in Wiked-specific
installation metadata without claiming ownership of unrelated files. Comparing
current files with that previous baseline identifies local modifications even
when the candidate is a different version. When no reliable baseline exists,
display a generic warning that local modifications may be overwritten.

Local modifications to Wiked files may be overwritten with user approval. A
first-install collision at a manifested path without a prior ownership record
requires explicit approval to take over that path. Approval covers that path,
not its parent directory or adjacent third-party content. A noninteractive
invocation must explicitly authorize such a collision rather than assume it.

Remove obsolete paths only when prior installation metadata proves Wiked
ownership and the old file's integrity. Do not automatically delete modified
obsolete files. Files outside Wiked ownership remain untouched. Contract,
operational wiki, ingestion material, and governance remain consumer-owned.

Download and validate the candidate before changing installed files. Prevent
concurrent operations. Keep temporary backups of affected files and restore the
previous state on handled failures. Record pending operations so that an abrupt
interruption requires recovery before another installation proceeds. Backups may
be removed after successful completion; permanent backups are not required.

If the latest version is already installed and its files are intact, make no
changes. If its files are modified or missing, offer an approved reinstall.
Do not update automatically while an agent is using the methodology.

## Compatibility and agent-assisted setup

Use a public contract-only validation mode in the candidate Distributed runtime
before replacing an existing installation with a configured Instance contract.
It must not require a full wiki check or access the tracker. Expose the existing
contract validation boundary rather than duplicate its rules in Bash. Missing
tools needed for this check prevent the update.

This contract does not change the existing compatibility policy: contract format
1.0, methodology major matching the runtime, and required methodology version no
newer than the runtime. An incompatible contract blocks replacement and produces
migration guidance. A first installation without a contract proceeds to setup.
Technical installation never migrates the contract or operational content.

On incompatibility, offer to create a priority-1 HITL migration ticket with current
and requested versions, the incompatibility, and the migration objective. Obtain
confirmation and use only an existing tracker in the consumer repository. Never
initialize one or fall back to an ancestor tracker. Without a local tracker,
provide the migration instructions instead. This is the only approved consumer
governance write performed by the installer and does not authorize migration.
Interactive approval is separate from the operation approval; automation may
use a separate explicit `--approve-migration-ticket` option. `--yes` never grants
this permission, and dry runs never create tickets. Verify tracker locality
before any create command, including configured ticket/archive paths.

After success, provide the instruction to begin `wiked-setup` using the installed
skill and consumer contract. Do not launch an agent or create domain content.

## Execution and verification

`wik-01m2tpjtev7w` implements the installer, relocatable references, contract-only
runtime interface, and synthetic failure/recovery coverage. It establishes the
artifact format without requiring a live release. Runtime or test changes require
`uv run pytest` under the source-development workflow.

`wik-01m4s6rgnfhr` evolves the existing Bash interaction and README entry order
under the amendment above. Test a piped script with a synthetic controlling
terminal, missing and explicit arguments, declined approvals, and unattended
execution. The distribution version and manifested inventory are unchanged.

`wik-01m4khsrmqya` follows the tested installer: prepare the manifested artifact,
MIT licensing, exact official download links, and the complete README
installation/update path. Verify the packaged artifact independently of any real
consumer. Record human publication as evidence, not merely local preparation.

The requester explicitly closed this ticket's Methodological grill on 2026-10-13:
prepare 1.4.1 with MIT licensing, preserve 1.4.0, align manifest/runtime versions,
and verify package -> install -> installed-runtime use with synthetic evidence.
Run `uv run pytest`, prepare only the exact manifested `distr.tar.gz`, and record
the human-published corrected release before closing the ticket. Git and
publication remain human-operated; installer redesign and version centralization
are excluded.

`wik-01m4sbvndyah` implements the approved fixed-name archive, human-operated
packaging script, checksum-free downloads, and corresponding tests and guidance.
The requester explicitly confirmed the Methodological grill summary, including
amending the publication ticket, before source changes. Local baseline hashes,
inventory checks, compatibility and transactional recovery are preserved.
Centralizing version authority and defining increments is deferred to
`wik-01m4sbvz62vp`, not silently included in packaging.

This contract's consolidation changes only source documentation and executor
tickets. Implementing these interfaces, changing the distributed inventory or
version, publishing, and installing remain executor work. Future independent
signing, native Windows support, and older-version selection are outside this
delivery. Historical research remains non-normative and unmodified.
