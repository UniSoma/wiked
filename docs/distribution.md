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
[v1.4.1](https://github.com/UniSoma/wiked/releases/tag/v1.4.1) was published by
`volneids` on 2026-10-13 at 02:45:45 UTC with only `distr.tar.gz` (28,211 bytes).
The downloaded archive contains exactly 17 manifested regular files, each matching
the tested source distribution and published tag, including the MIT license.
The main installer and root license were also verified available. Release
preparation must verify the documented download paths before announcing them;
never infer repository authority from schema IDs.
The maintainer explicitly approved `wik-01m4s821zj1m` to make `UniSoma/wiked` the
installer's only release origin. Do not expose a remote origin argument or ask users
to choose a repository. Synthetic tests intercept transport for the official
URLs rather than introduce a configurable alternative origin.
The maintainer approved `wik-01m66t0dc77b` as the only exception: `--source`
installs from a local Wiked clone, never a URL, to test unpublished releases or
branches on real wikis. The clone's own `scripts/package-wiked.sh` builds the
candidate archive, which then follows the official candidate path unchanged.
Its user owns that choice: installation metadata does not record the source,
uncommitted changes are not checked, and older versions are still rejected.
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
  Its matching release tag is `v1.4.1`; human publication is verified above.
  The runtime reads its version from the authoritative manifest. The development
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
- `scripts/package-wiked.sh` reads the version from the manifest and validates
  source inventory and release declarations, then creates only
  `distr.tar.gz`. Default output is a fresh temporary
  directory; `--output` selects a directory. Existing archives must not be
  overwritten. The script does not run the test suite, install, publish, operate
  Git, or increment versions. Packaging uses the source matching the intended tag.

## Version authority and increments

`distr/agents/wiked-manifest.yaml` is the sole current distribution-version
authority. The installed runtime reads the same relative manifest through
`scripts/distribution.py`; no runtime or packaging version literal is maintained.
Contract format versions, feature-introduction minimums, historical changelog
entries, and the development project's version have distinct meanings and do not
increment mechanically with the distribution.

The maintainer approves every increment, applying SemVer to the methodological
contract, not merely to code or documentation file types:

- Major: incompatible behavior or a mandatory change requiring existing wikis
  to migrate.
- Minor: compatible methodological evolution or optional capability; review may
  be needed, but migration is not imposed.
- Patch: fixes, clarifications, and infrastructure refinements that preserve the
  methodological obligations of existing wikis. A change to those obligations is
  not a patch just because its implementation edits instructions.

For release preparation, the human chooses the version, edits only the manifest's
current version, and adds its declaration to the distributed
`skills/wiked/CHANGELOG.md`. That changelog records only impacts that may demand
review of existing wiki texts, not every internal optimization. Each release has
one `## X.Y.Z - review` or `## X.Y.Z - none` declaration, newest first, with a
nonempty explanation. Impactful entries include `### Review`, `### Rationale`,
and `### Action` sections. Review describes affected content. Rationale states
why each impact was made and the pains it resolves, in up to three lines per
impact; it need not describe earlier behavior, and a motivation absent from the
historical record is declared unrecorded rather than inferred. Action contains
only list items, each starting with `Required:`, `Optional adoption:`, or
`Informational:`. Every `Optional adoption:` item links to an installed guide
section containing a short paragraph on what adoption offers and requires; the
changelog states why, the guide states the consequences. The installed-version
review uses these fields to brief the human before asking for disposition.
Write an impact index, not a second manual: keep each impact to a few lines stating
what to review, when it applies, and where to find the canonical rules. Link to
installed guides instead of repeating methodology, governance, or procedures.
Use one sentence for `none` and `baseline` entries; omit internal-change narratives.
Packaging and installation check only the presence of these sections and markers.
The oldest `baseline` entry starts coverage at 1.4.1; prior history is out of
scope. The changelog must extend through the current manifest version. Structural
checks cannot certify the maintainer's semantic classification or historical
completeness.

Run `uv run pytest`, then `bash scripts/package-wiked.sh`. Packaging reads the
version only from the manifest and prints the matching publication tag; it does
not require the human to repeat the version as an argument. The installer rejects
tag/manifest disagreement and invalid release declarations. Neither script
selects an increment, operates Git, or publishes.
Humans create the matching release tag and publish the immutable archive. The
1.5.1 preparation preserves existing wiki obligations, records 1.5.0's optional
intent-map impact from the 1.4.1 baseline, and is not evidence of publication.

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
Display and confirm only the selected latest stable version, or the version
packaged from an explicit local `--source`; do not introduce older-version selection. Keep that selection, candidate, and plan in one
operation through final approval. The operation-level approval follows Python's
displayed plan, not merely the initial parameter questions.

Automation supplies parameters and explicit approval options through the same
interface. `--yes` approves the selected stable version and operation plan, not
collisions or migration tickets. Without a controlling terminal, installation
requires explicit approvals; stdin text is never consent. Dry runs and explicit
recovery remain available without a terminal or installation approval. Defaults
may be accepted through explicit noninteractive invocation. Preserve all
ownership, compatibility, and recovery checks in both usages.

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

Download and validate the candidate before changing installed files. The user must
run installation, update, and recovery one operation at a time; concurrent
operations are unsupported and are not prevented by the installer.
Keep temporary backups of affected files and restore the
previous state on handled failures. Record pending operations so that an abrupt
interruption requires recovery before another installation proceeds. Backups may
be removed after successful completion; permanent backups are not required.

If the latest version is already installed and its files are intact, make no
changes. If its files are modified or missing, offer an approved reinstall.
Do not update automatically while an agent is using the methodology.

## Compatibility and agent-assisted setup

Use a public contract-only validation mode in the candidate Distributed validator
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

After first installation without an Instance contract, provide the instruction
to begin `wiked-setup` with the installed skill to create it. When a compatible
Instance contract already exists, the candidate Distributed validator reports its
declared methodology version. If that version equals the installed one, route the
operator to the installed skill and reserve `wiked-setup` for an authorized
contract migration. If it is older, record the pending review from the declared
version and print the maintenance-agent prompt for that interval instead of the
setup instruction. Keep this output distinct from update and repair output. Do
not launch an agent or create domain content.
After every effective version change from a recorded installation, print a
clearly labeled maintenance-agent prompt ready to copy and paste. Place the title
`WIKED MAINTENANCE AGENT PROMPT:` outside the copyable region, delimit that region
with two `-----` lines, and separate the prompt from the delimiters and surrounding
logs with blank lines. Tell the operator to copy only the text between the
separators. Include the installed version and pending interval, but no repository,
installation, or skill paths and no embedded commands. Route the agent to the
Wiked skill's installed-version maintenance workflow and consumer-owned Instance
contract, explicitly distinguishing review from setup. The installed guide owns
the review and acknowledgment procedure; do not duplicate it in the prompt.
Require review to assess content against the new methodology. Contract-only preflight is not
content validation. The notice does not authorize corrections, contract migration,
or automatic adoption of optional capabilities; those need their own governance.
First installation without an older Instance contract, same-version repair,
intact no-op, and dry run do not trigger this version-change prompt. The delegated workflow requires impacts, findings,
validation, uncertainties, human disposition and explicit completion confirmation,
followed by recording through the installed acknowledgment interface; the prompt
grants no correction authority. Same-version pending-review reminders remain
distinct and concise, reporting only the pending interval.

Preserve `maintenance_since` in installation metadata across successive updates:
oldest unreviewed version exclusive, installed version inclusive. Initial
installation records null. Legacy metadata uses the previous recorded version
when starting a new range; it cannot prove earlier review completion. Invalid
pending ranges block the operation. Same-version repair and no-op retain and may
display an existing pending range. The installed maintenance guide lazily loads
the distributed changelog for that interval, including skipped releases; `none`
does not waive ordinary review. Missing history requires explicit uncertainty
and human disposition, not an inferred absence of impact.

The agent reports impacts, findings, validation, and uncertainties. Human
disposition assigns explicit follow-ups, including consumer-local correction
tickets when appropriate. Review may finish before corrections do, but not when
analysis itself was prevented. After the completed report and disposition, the
human must explicitly confirm review completion for the exact installed version
and interval. Only then may the reviewing agent record acknowledgment through a
dedicated installed command. Inspection captures a token bound to metadata and
manifest before the review; the command requires that snapshot, exact version and
pending start, and an explicit assertion of received human confirmation. A flag
cannot prove consent or complete analysis: the installed workflow enforces those
human gates. A changed installation requires reassessment and renewed confirmation,
not simply obtaining a new token to bypass a stale review.

The reviewing agent may remain active only for this metadata operation. No
acknowledgment may overlap installation, update, recovery, or another acknowledgment;
general concurrency exclusion is not introduced. Human installation, update, and
recovery still require agents stopped. The command runs offline, never downloads
a release or resolves dependencies over the network, and changes only metadata
using transactional recovery. Preserve version/inventory/hashes and the metadata
format; add no audit-log schema. It neither modifies skill/wiki/contract nor
creates tickets. Stale snapshots, version/range disagreement, invalid manifest
identity, unreliable baseline, and pending transactions block acknowledgment.
Recheck the reviewed state before mutation, without requiring current installed
files to match every baseline hash. Dry runs do not acknowledge. Missing offline
prerequisites block rather than authorize downloads. Handled failures roll back;
abrupt interruptions require human recovery through the installer. The existing
human installer option remains compatible and separately approved, with agents
stopped; agents use the installed interface, not the downloaded installer.

`installation_state.py` is the canonical shared state/transaction implementation.
The self-contained installer embeds it; `scripts/sync-installer-core.py` generates
that block and offers a non-mutating synchronization check. Tests must verify
synchronization and recovery compatibility between entrypoints. Both short `y`
and full `yes` interactive approvals are accepted case-insensitively, with prompts
listing accepted responses; empty/unrecognized input never grants approval.
Neither form broadens `--yes` authorization to collisions or migration tickets.

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
Centralizing version authority and defining increments was deferred to
`wik-01m4sbvz62vp`, not silently included in packaging. Its Methodological grill
was explicitly closed on 2026-10-13 for the authority/increment policy above,
1.5.1 preparation, impact changelog from the 1.4.1 baseline, persistent pending
review and human acknowledgment, README maintenance prompt, and synthetic tests.
No consumer installation, Git operation, or publication is authorized by that
source delivery.

The requester explicitly closed the Methodological grill for
`wik-01m5pwszwv9v` on 2026-10-24, approving the installed agent-operated
acknowledgment exception, shared embedded core, stale-state safeguards, distinct
copy-ready maintenance handoff, and short/full interactive confirmations above.
Prepare 1.6.0 as a compatible evolution, with `none` impact on existing wiki
texts. This approval authorizes source preparation and synthetic testing only,
not publication, installation, Git operations, or consumer changes.

The requester explicitly closed the Methodological grill for
`wik-01m64g9wck6z` on 2026-10-29 and confirmed its implementation scope for
`wik-01m64q57xm81` on 2026-10-30, approving the changelog Rationale and action
markers above, the decision briefing in the installed-version review, adoption
paragraphs in the guides, and the retroactive rewrite of the 1.5.0 through 1.7.0
entries without changing their meaning. Prepare 1.8.0 as a compatible evolution
with `review` impact, covering this change and the optional external-authority
and offline external-link capabilities. This approval authorizes source
preparation and synthetic testing only, not publication, installation, Git
operations, or consumer changes.

This contract's consolidation changes only source documentation and executor
tickets. Implementing these interfaces, changing the distributed inventory or
version, publishing, and installing remain executor work. Future independent
signing, native Windows support, and older-version selection are outside this
delivery. Historical research remains non-normative and unmodified.
