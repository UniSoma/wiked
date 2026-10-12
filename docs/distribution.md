# Publication and distribution contract

This source-development contract was approved through the Methodological grill
for `wik-01m2tphwrc4f` on 2026-10-10. It specifies the release and installer work;
it does not claim those capabilities are already implemented. It is not an
installed skill dependency or authority to operate a consumer wiki.

## Audience, authority, and delivery

Initial consumers are a controlled audience. The repository README must also
enable an independent user to discover Wiked, install its distribution, and then
start agent-assisted wiki setup in their own repository.

The maintainer, Volnei Santos, decides methodology versions and approves releases.
The canonical source is the official Wiked GitHub repository; versioned downloads
are published through its GitHub Releases. Release preparation must verify and
document that repository's exact address rather than infer it from schema IDs.
Humans operate Git and publish releases. Agents prepare and verify release material
without installing tools on the host or replacing their running skill.

The author-owned distribution is to be licensed under MIT, retaining applicable
third-party notices and licenses. The publication executor supplies the license
text and attribution; this contract alone is not a license file.

Delivery order is this approved contract, implementation and synthetic testing of
the installer, then preparation and human publication of the first release.
Installer tests must not require an already published release or a real consumer.

## Artifact, version, and integrity

- Each release provides a `.tar.gz` containing exactly the files owned by
  `distr/agents/wiked-manifest.yaml`, plus a separately downloadable installer and
  SHA-256 checksums for the downloadable artifacts.
- The archive preserves the manifest-relative tree. Source tests, research, and
  development documentation are not installed runtime dependencies.
- Wiked owns the namespaced manifest and the paths it lists, not the whole
  installation directory. Unlisted consumer and third-party files are preserved.
- Distribution versions use SemVer. Published versions and their artifacts are
  immutable; corrections require a new version. Prereleases may use `-rc.1` and
  are excluded from automatic stable-release selection.
- The current source distribution is 1.4.0. It may be the first published version
  only if the delivered changes fit that version; the maintainer approves the
  final version. The manifest and runtime version must agree. The development
  environment's project version is not the distribution version.
- An invocation resolves the latest stable official release once, displays its
  version, and pins that selection through the entire operation. It records the
  installed version. Selecting older releases or offering downgrade is outside
  the initial installer interface.
- Downloads use HTTPS. Check SHA-256 before extracting the distribution or
  changing the installation. README instructions must also explain verification
  of the downloaded installer before execution. Checksums provide integrity, not
  an independent publisher signature; independent signing is deferred.

## Installation interface and prerequisites

The deterministic Bash installer is invoked by a human following the README.
Initial supported environments are Linux, macOS, and Windows through WSL; native
Windows is outside the first delivery. Installation requires network access to
the official release channel; an offline bundle is not part of this delivery.

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

After success, provide the instruction to begin `wiked-setup` using the installed
skill and consumer contract. Do not launch an agent or create domain content.

## Execution and verification

`wik-01m2tpjtev7w` implements the installer, relocatable references, contract-only
runtime interface, and synthetic failure/recovery coverage. It establishes the
artifact format without requiring a live release. Runtime or test changes require
`uv run pytest` under the source-development workflow.

`wik-01m4khsrmqya` follows the tested installer: prepare the manifested artifact,
MIT licensing, checksums, exact official download links, and the complete README
installation/update path. Verify the packaged artifact independently of any real
consumer. Record human publication as evidence, not merely local preparation.

This contract's consolidation changes only source documentation and executor
tickets. Implementing these interfaces, changing the distributed inventory or
version, publishing, and installing remain executor work. Future independent
signing, native Windows support, and older-version selection are outside this
delivery. Historical research remains non-normative and unmodified.
