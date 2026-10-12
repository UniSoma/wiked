# Runtime Interface

`validate_wiki.py` is Wiked's portable PEP 723 validator. Invoke it with an explicit consumer repository root:

```text
uv run --script .agents/skills/wiked/scripts/validate_wiki.py --repository-root .
```

The validator derives `wiki/` and `wiki/wiki-structure.yaml` from that root. It never derives the consumer root from the script location and does not require a Python project in the consumer. It validates internal references, configured names, the optional root authoring reference, declared assets, and configured diagram sets; external links and bare URLs are informational. It validates only the authoring reference's structural integration, not its human-review criteria. It does not inspect or require `raw/` or `raw/archive/`; those directories hold ingestion material managed by the setup and assisted-indexing workflows, not contract configuration or operational evidence. Exit codes are `0` for success (warnings allowed), `1` for structural errors, and `2` for contract or runtime failures. Use `--format json` for deterministic structured diagnostics.

Add `--contract-only` to validate only the contract's schema, compatibility, and
relational rules. This mode checks no Markdown pages and never invokes Knot;
it returns `0` for a valid contract and `2` for contract/runtime failures.
Human updates use this mode in the candidate runtime before replacement.
For a custom installation, replace `.agents/skills/wiked/` in the command with
the actual installed skill path; always keep the consumer root explicit.
