# Runtime Interface

`validate_wiki.py` is Wiked's distributed validator, a portable PEP 723 script. Invoke it with an explicit consumer repository root:

```text
uv run --script .agents/skills/wiked/scripts/validate_wiki.py --repository-root .
```

Keep `distribution.py`, the shared `wiki_core.py` module, the schema, and `wiked-manifest.yaml` in their manifested
relative layout. The runtime reads its methodology version from that manifest,
independently of cwd and instance contract requirements; there is no second
current-version literal. Missing or invalid distribution identity is a blocking
`runtime.version` diagnostic. Contract format and feature-introduction minimums
are distinct from the current distribution version. Normal validation does not
load the changelog or acknowledge maintenance completion.

The validator derives `wiki/` and `wiki/wiki-structure.yaml` from that root. It never derives the consumer root from the script location and does not require a Python project in the consumer. It validates internal references, configured names, the optional root authoring reference, declared assets, and configured diagram sets; external links and bare URLs are informational outside typed canonical-reference fields and intent-map destination entries unless `rules.external_links` enables the offline check described below. It validates only the authoring reference's structural integration, not its human-review criteria. It does not inspect or require `raw/` or `raw/archive/`; those directories hold ingestion material managed by the setup and assisted-indexing workflows, not contract configuration or operational evidence. Exit codes are `0` for success (warnings allowed), `1` for structural errors, and `2` for contract or runtime failures. Use `--format json` for deterministic structured diagnostics. When the contract passes schema validation, the JSON report also includes `contract.methodology_version`, the methodology version it declares.

Add `--contract-only` to validate only the contract's schema, compatibility, and
relational rules. This mode checks no Markdown pages and never invokes Knot;
it returns `0` for a valid contract and `2` for contract/runtime failures.
Human updates use this mode in the candidate runtime before replacement.
For a custom installation, replace `.agents/skills/wiked/` in the command with
the actual installed skill path; always keep the consumer root explicit.

Reference validation accepts portable `<a id="...">` anchors outside code and
comments, in addition to heading-derived fragments. Duplicate explicit targets
or collisions with heading targets produce `reference.anchor`. Optional SVG
return-link markers described in [the Docsify guide](../guides/docsify.md) are
checked for syntax and an existing description anchor in the current entry;
malformed markers produce `reference.diagram`. Both use `rules.reference`.
These checks neither enable a viewer nor verify rendered node identity or browser
navigation. Unmarked diagrams remain ordinary static assets.

When `navigation.intent_map` is declared, the full validator checks its reserved
root location, existence, exactly one root-index link, common Markdown format,
canonical operational-page/index destinations, exact H1 labels, nonempty guidance,
and within-intent destination uniqueness. Shared and cross-trunk destinations
between intents are allowed only in the map; index invariants remain unchanged.
The map cannot carry frontmatter or acquire an operational role. `intent-map.*`
diagnostics use `rules.navigation`; general reference checks also verify existing
fragments. The validator does not decide usefulness, coverage, or operational
truth. Contract-only mode checks the declaration and minimum methodology 1.5.0,
not the map file or content. Instances without a map retain existing behavior.

When a page type declares `external_authority`, the full validator checks that each page of that type opens with the configured notice in a quotation after the H1 and that the quotation's links are absolute `http(s)` URLs, at least one when required. `external-authority.*` diagnostics use `rules.external_authority`; contract-only mode checks the declaration, rule, and minimum methodology 1.8.0. Instances without the capability retain existing behavior.

When `rules.external_links` is declared, the full validator checks external link and image destinations offline for allowed schemes and syntax, reporting `external-link.scheme` and `external-link.malformed` under that rule; it never accesses the network. Contract-only mode checks the minimum methodology 1.8.0. Instances without the rule retain existing behavior.

## Maintenance review acknowledgment

Load this interface only for the installed-version workflow in
[Maintenance](../guides/maintenance.md#installed-version-review). It is separate
from validation and does not certify content conformity or authorize corrections.

At the start of review, inspect the installation containing this command:

```sh
uv run --no-project --no-python-downloads --offline --script .agents/skills/wiked/scripts/acknowledge_review.py --inspect
```

Retain the returned `version`, `maintenance_since`, and `state_token` for the
review. After completed analysis, reporting, human disposition, and explicit human
confirmation of that version and interval, invoke the same script with
`--version`, `--since`, and `--state-token` set to those returned values and
`--human-confirmed`. That flag is an assertion of received consent, not proof of
it. `--dry-run` validates the request without recording completion. Missing
confirmation, a stale snapshot/version/range, unreliable identity/baseline, or a
pending transaction prevents acknowledgment. If no review is pending, there is
nothing to acknowledge.

Use the actual installed script path for custom locations. Unlike the validator,
this command derives the installation root from its own location, independently
of cwd; keep `acknowledge_review.py` and its shared `installation_state.py` module
in their manifested relative layout. It does not infer or operate on consumer
wiki content. It changes only
`.wiked-install.json`, preserving version, inventory, and baseline hashes, through
the installer's transactional journal. It never downloads releases, modifies
installed skill files, invokes Knot, or performs recovery. Handled failures roll
back; abrupt interruption requires human installer recovery with agents stopped.

The reviewing agent may run this command while active, but no acknowledgment,
installation, update, or recovery may overlap. No general concurrency exclusion
is provided. The offline invocation prohibits dependency and interpreter downloads;
Python, `uv`, and cached dependencies must already be available. If prerequisites
are unavailable, report the blocker and leave review pending rather than allowing
network resolution. Do not hand-edit metadata or replace the installed skill.
