from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).parents[1]
DISTRIBUTION = ROOT / "distr/agents"
WIKED = DISTRIBUTION / "skills/wiked"


def test_cutover_leaves_one_self_contained_manifested_distribution() -> None:
    manifest = yaml.safe_load((DISTRIBUTION / "wiked-manifest.yaml").read_text(encoding="utf-8"))
    owned = {
        path
        for paths in manifest["components"].values()
        for path in paths
    }
    distributed = {
        "wiked-manifest.yaml",
        "commands/wiked-setup.md",
        *(str(path.relative_to(DISTRIBUTION)) for path in WIKED.rglob("*") if path.is_file()),
    }

    assert manifest["preserve_unlisted_files"] is True
    assert owned == distributed
    assert all((DISTRIBUTION / path).is_file() for path in owned)
    assert not (ROOT / "scripts/validate_wiki.py").exists()
    assert not (ROOT / "docs/contratos/estrutura-da-wiki.yaml").exists()

    runtime = (WIKED / "scripts/validate_wiki.py").read_text(encoding="utf-8")
    version = re.search(r'^METHODOLOGY_VERSION = "([^"]+)"$', runtime, re.MULTILINE)
    assert version and version.group(1) == str(manifest["distribution_version"])

    text_artifacts = [DISTRIBUTION / path for path in owned if Path(path).suffix in {".md", ".py", ".json", ".yaml"}]
    assert not [path for path in text_artifacts if "docs/" in path.read_text(encoding="utf-8")]


def contract() -> dict[str, object]:
    return {
        "contract_version": "1.0",
        "methodology_version": "1.0.0",
        "language": "en",
        "initial_content": {
            "title": "Knowledge base",
            "purpose": "Document operations.",
            "audience": "Operations team.",
            "scope": "Current operating practices.",
            "context_terms": [{"term": "Operation", "definition": "A recurring practice."}],
        },
        "topology": {
            "trunks": ["handbook", "sources"],
            "required_trunks": ["sources"],
            "sources_trunk": "sources",
            "max_depth": 1,
            "assets_directory": "assets",
        },
        "naming": {"pattern": "^[a-z][a-z0-9-]*$"},
        "navigation": {"root_index": "index.md", "trunk_index": "index.md", "context_file": "CONTEXT.md"},
        "frontmatter": {"marker": "---", "exceptions": ["index.md", "CONTEXT.md"]},
        "page_types": {
            "article": {
                "roles": ["knowledge"],
                "states": ["current", "suggested"],
                "fields": {"required": ["type", "state"], "optional": ["reviewed_on", "change_ticket"], "date": ["reviewed_on"]},
                "sections": {"required": ["Sources"]},
            },
            "source": {
                "roles": ["evidence"],
                "states": ["indexed", "empty"],
                "fields": {"required": ["type", "state", "indexed_on"], "optional": [], "date": ["indexed_on"]},
                "sections": {"required": ["Source record", "Grounded pages"]},
            },
        },
        "states": ["current", "suggested", "indexed", "empty"],
        "sections": {
            "source_record": "Source record",
            "grounded_pages": "Grounded pages",
            "content_sources": "Sources",
            "no_content": "None.",
        },
        "assets": {"allowed_extensions": ["svg", "png"], "forbidden_files": ["index.md"], "allow_subdirectories": False},
        "diagrams": {"required_extensions": ["md", "d2", "svg"], "source_extension": "d2", "visualization_extension": "svg", "applies_to_roles": ["knowledge"]},
        "provenance": {
            "source_role": "evidence",
            "content_roles": ["knowledge"],
            "record_fields": ["Kind", "Origin", "Scope", "Published", "Consulted", "Indexed"],
            "publication_date_field": "Published",
            "publication_unknown": "unknown",
            "date_fields": ["Consulted", "Indexed"],
            "indexed_field": "indexed_on",
            "indexed_record_field": "Indexed",
            "no_content_states": ["empty"],
        },
        "pendency_tracking": {
            "roles": ["knowledge"],
            "section": "Open questions",
            "id_pattern": "^job-[0-9]{4}$",
            "tag": "question",
            "valid_statuses": ["queued", "working"],
            "warning_statuses": ["finished"],
        },
        "proposal_tracking": {
            "roles": ["knowledge"],
            "section": "Suggested changes",
            "id_pattern": "^job-[0-9]{4}$",
            "tag": "change",
            "valid_statuses": ["queued", "working"],
            "warning_statuses": ["finished"],
            "frontmatter_field": "change_ticket",
            "proposal_state": "suggested",
        },
        "rules": {
            name: {"severity": "warning" if name in {"pendency_status", "proposal_status"} else "error"}
            for name in (
                "contract", "topology", "navigation", "frontmatter", "h1", "reference",
                "assets", "diagrams", "provenance", "contextual_citation", "pendency_location", "pendency_association",
                "pendency_status", "pendency_inverse", "proposal_location", "proposal_association",
                "proposal_status", "proposal_inverse",
            )
        },
    }


def test_contract_only_cli_never_reads_pages_or_tracker(tmp_path: Path) -> None:
    script = copy_runtime(tmp_path)
    repository = tmp_path / "consumer"
    (repository / "wiki").mkdir(parents=True)
    path = repository / "wiki/wiki-structure.yaml"
    path.write_text(yaml.safe_dump(contract()))
    (repository / "wiki/unreadable.md").write_bytes(b"\xff")
    tools = tmp_path / "bin"
    tools.mkdir()
    knot = tools / "knot"
    knot.write_text(f"#!/bin/sh\ntouch '{tmp_path / 'tracker-called'}'\nexit 99\n")
    knot.chmod(0o755)

    def invoke():
        return subprocess.run(
            ["uv", "run", "--script", str(script), "--repository-root", str(repository), "--contract-only", "--format", "json"],
            env={**os.environ, "PATH": str(tools) + os.pathsep + os.environ["PATH"]},
            capture_output=True, text=True,
        )

    result = invoke()
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["summary"]["files_checked"] == 0
    incompatible = contract()
    incompatible["methodology_version"] = "2.0.0"
    path.write_text(yaml.safe_dump(incompatible))
    assert invoke().returncode == 2
    path.unlink()
    assert invoke().returncode == 2
    assert not (tmp_path / "tracker-called").exists()


def test_namespaced_setup_command_routes_to_the_distributed_guide() -> None:
    manifest = yaml.safe_load((DISTRIBUTION / "wiked-manifest.yaml").read_text(encoding="utf-8"))
    command = (DISTRIBUTION / "commands/wiked-setup.md").read_text(encoding="utf-8")

    assert "commands/wiked-setup.md" in manifest["components"]["commands"]
    assert "guides/setup.md" in command
    assert "distributed schema and validator" in command


def test_human_qualification_and_ingestion_stay_outside_the_contract() -> None:
    skill = (WIKED / "SKILL.md").read_text(encoding="utf-8")
    setup = (WIKED / "guides/setup.md").read_text(encoding="utf-8")
    indexing = (WIKED / "guides/assisted-indexing.md").read_text(encoding="utf-8")
    grill = (WIKED / "guides/grill.md").read_text(encoding="utf-8")
    contract_readme = (WIKED / "contracts/README.md").read_text(encoding="utf-8")
    runtime_readme = (WIKED / "scripts/README.md").read_text(encoding="utf-8")
    schema = json.loads((WIKED / "contracts/wiki-structure.schema.json").read_text(encoding="utf-8"))

    assert "session- and objective-specific" in skill
    assert "qualified to govern the current objective" in grill
    assert "raw/` and `raw/archive/" in setup
    assert "raw/archive/YYYY-MM-DD_<ticket-id>/" in indexing
    assert "stop rather than overwrite" in indexing
    assert "persisted in Git" in contract_readme
    assert "does not inspect or require `raw/` or `raw/archive/`" in runtime_readme
    assert "human_authority" not in schema["properties"]
    assert "ingestion" not in schema["properties"]


def write_instance(root: Path) -> Path:
    repository = root / "consumer"
    wiki = repository / "wiki"
    (wiki / "handbook").mkdir(parents=True)
    (wiki / "sources").mkdir()
    (wiki / "assets").mkdir()
    (wiki / "wiki-structure.yaml").write_text(yaml.safe_dump(contract(), sort_keys=False), encoding="utf-8")
    (wiki / "CONTEXT.md").write_text("# Context\n\n## Operation\n\nA recurring practice.\n", encoding="utf-8")
    (wiki / "index.md").write_text("# Knowledge base\n\nDocument operations.\n\nOperations team.\n\nCurrent operating practices.\n\n- [Context](./CONTEXT.md)\n- [Handbook](./handbook/index.md)\n- [Sources](./sources/index.md)\n", encoding="utf-8")
    (wiki / "handbook" / "index.md").write_text("# Handbook\n\n- [Operations](./operations.md)\n", encoding="utf-8")
    (wiki / "handbook" / "operations.md").write_text("---\ntype: article\nstate: current\n---\n# Operations\n\nSee the [source](../sources/manual.md).\n\n![Diagram](./operations.svg)\n\n## Sources\n\n- [Manual](../sources/manual.md)\n", encoding="utf-8")
    (wiki / "handbook" / "operations.d2").write_text("diagram\n", encoding="utf-8")
    (wiki / "handbook" / "operations.svg").write_text("svg\n", encoding="utf-8")
    (wiki / "sources" / "index.md").write_text("# Sources\n\n- [Manual](./manual.md)\n", encoding="utf-8")
    (wiki / "sources" / "manual.md").write_text(
        "---\ntype: source\nstate: indexed\nindexed_on: 2026-09-18\n---\n# Manual\n\n"
        "## Source record\n\n- **Kind:** guide.\n- **Origin:** [Manual](https://example.test/manual).\n"
        "- **Scope:** operations.\n- **Published:** unknown.\n- **Consulted:** 2026-09-18.\n"
        "- **Indexed:** 2026-09-18.\n\n## Grounded pages\n\n- [Operations](../handbook/operations.md)\n",
        encoding="utf-8",
    )
    return repository


def write_minimal_setup_instance(root: Path) -> Path:
    repository = root / "consumer"
    wiki = repository / "wiki"
    (wiki / "sources").mkdir(parents=True)
    (wiki / "assets").mkdir()
    data = contract()
    data["topology"] = {
        "trunks": ["sources"],
        "required_trunks": ["sources"],
        "sources_trunk": "sources",
        "max_depth": 1,
        "assets_directory": "assets",
    }
    (wiki / "wiki-structure.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    (wiki / "CONTEXT.md").write_text("# Context\n\n## Operation\n\nA recurring practice.\n", encoding="utf-8")
    (wiki / "index.md").write_text(
        "# Knowledge base\n\nDocument operations.\n\nOperations team.\n\nCurrent operating practices.\n\n"
        "- [Context](./CONTEXT.md)\n- [Sources](./sources/index.md)\n",
        encoding="utf-8",
    )
    (wiki / "sources" / "index.md").write_text("# Sources\n", encoding="utf-8")
    return repository


def copy_runtime(root: Path) -> Path:
    distribution = root / "portable" / "wiked"
    shutil.copytree(WIKED / "scripts", distribution / "scripts")
    shutil.copytree(WIKED / "contracts", distribution / "contracts")
    return distribution / "scripts" / "validate_wiki.py"


def knot_environment(tmp_path: Path, repository: Path, responses: dict[str, object] | None = None) -> dict[str, str]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    executable = bin_dir / "knot"
    executable.write_text(
        "#!/usr/bin/env -S uv run --script\n"
        "import json, os, sys\n"
        "if os.getcwd() != os.environ['EXPECTED_KNOT_CWD']:\n"
        "    print(json.dumps({'ok': False, 'error': {'code': 'cwd', 'message': os.getcwd()}})); sys.exit(1)\n"
        "responses = json.loads(os.environ.get('KNOT_RESPONSES', '{}'))\n"
        "command = sys.argv[1]\n"
        "if command in {'list', 'closed'}:\n"
        "    tag = sys.argv[sys.argv.index('--tag') + 1]\n"
        "    key = '_' + command + ':' + tag\n"
        "    response = responses.get(key, responses.get('_' + command, {'ok': True, 'data': []}))\n"
        "else:\n"
        "    response = responses.get(sys.argv[2], {'ok': False, 'error': {'code': 'not_found', 'message': 'missing'}})\n"
        "print(json.dumps(response)); sys.exit(int(response.get('_exit', 0)))\n",
        encoding="utf-8",
    )
    executable.chmod(0o755)
    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
    env["EXPECTED_KNOT_CWD"] = str(repository.resolve())
    env["KNOT_RESPONSES"] = json.dumps(responses or {})
    return env


def run_portable(tmp_path: Path, repository: Path, output_format: str = "json", responses: dict[str, object] | None = None) -> subprocess.CompletedProcess[str]:
    script = copy_runtime(tmp_path)
    cwd = tmp_path / "unrelated-cwd"
    cwd.mkdir()
    return subprocess.run(
        ["uv", "run", "--script", str(script), "--repository-root", str(repository), "--format", output_format],
        cwd=cwd,
        env=knot_environment(tmp_path, repository, responses),
        text=True,
        capture_output=True,
    )


def test_portable_validator_runs_outside_source_layout(tmp_path: Path) -> None:
    result = run_portable(tmp_path, write_instance(tmp_path), "text")

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Files checked: 6" in result.stdout
    assert "Errors: 0" in result.stdout
    assert "Warnings: 0" in result.stdout
    assert "Arquivos" not in result.stdout


@pytest.mark.integration
def test_explicit_consumer_validates_with_distributed_runtime() -> None:
    configured_root = os.environ.get("WIKED_CONSUMER_ROOT")
    if not configured_root:
        pytest.skip("Set WIKED_CONSUMER_ROOT to opt into real-consumer integration")
    repository = Path(configured_root)
    assert repository.is_absolute(), "WIKED_CONSUMER_ROOT must be absolute"
    assert (repository / "wiki/wiki-structure.yaml").is_file(), "Consumer contract not found"
    result = subprocess.run(
        [
            "uv",
            "run",
            "--script",
            str(WIKED / "scripts" / "validate_wiki.py"),
            "--repository-root",
            str(repository),
            "--format",
            "json",
        ],
        cwd=repository,
        text=True,
        capture_output=True,
    )
    payload = json.loads(result.stdout)

    assert result.returncode == 0, result.stdout + result.stderr
    assert payload["summary"]["errors"] == 0
    assert payload["summary"]["warnings"] == 0
    assert payload["summary"]["files_checked"] > 0


def test_setup_creation_is_minimal_and_declares_the_approved_language(tmp_path: Path) -> None:
    repository = write_minimal_setup_instance(tmp_path)

    result = run_portable(tmp_path, repository)
    saved = yaml.safe_load((repository / "wiki/wiki-structure.yaml").read_text(encoding="utf-8"))

    assert result.returncode == 0, result.stdout + result.stderr
    assert saved["language"] == "en"
    assert not (repository / "wiki/sources/manual.md").exists()
    assert list((repository / "wiki/assets").iterdir()) == []


def test_schema_rejects_invalid_contract_before_pages(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["contract_version"] = "2.0"
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    (repository / "wiki/handbook/operations.md").write_bytes(b"\xff")

    result = run_portable(tmp_path, repository)
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert payload["summary"]["files_checked"] == 0
    assert payload["diagnostics"][0]["code"] == "contract.schema"
    assert "2.0" in payload["diagnostics"][0]["message"]


def test_contract_relations_are_checked_after_schema(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["topology"]["required_trunks"] = ["missing"]
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    result = run_portable(tmp_path, repository)
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert payload["summary"]["files_checked"] == 0
    assert {item["code"] for item in payload["diagnostics"]} == {"contract.relation"}


def test_provenance_indexed_field_must_be_an_allowed_date_on_source_types(tmp_path: Path) -> None:
    for fields in (
        {"required": ["type", "state"], "optional": [], "date": []},
        {"required": ["type", "state", "indexed_on"], "optional": [], "date": []},
    ):
        sandbox = tmp_path / str(len(fields["required"]))
        sandbox.mkdir()
        repository = write_instance(sandbox)
        contract_path = repository / "wiki/wiki-structure.yaml"
        data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        data["page_types"]["source"]["fields"] = fields
        contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

        result = run_portable(sandbox, repository)
        payload = json.loads(result.stdout)

        assert result.returncode == 2
        assert {item["code"] for item in payload["diagnostics"]} == {"contract.relation"}


def test_schema_requires_the_configured_provenance_indexed_field(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    del data["provenance"]["indexed_field"]
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    result = run_portable(tmp_path, repository)
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert {item["code"] for item in payload["diagnostics"]} == {"contract.schema"}


def test_provenance_no_content_states_must_be_allowed_by_source_types(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["provenance"]["no_content_states"] = ["current"]
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    result = run_portable(tmp_path, repository)
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert {item["code"] for item in payload["diagnostics"]} == {"contract.relation"}


def test_proposal_state_must_be_allowed_by_tracked_page_types(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["proposal_tracking"]["proposal_state"] = "indexed"
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    result = run_portable(tmp_path, repository)
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert {item["code"] for item in payload["diagnostics"]} == {"contract.relation"}


def test_schema_requires_semantic_lists_but_accepts_empty_optional_lists(tmp_path: Path) -> None:
    required_lists = (
        ("provenance", "no_content_states"),
        ("pendency_tracking", "roles"),
        ("pendency_tracking", "valid_statuses"),
        ("page_types", "source", "states"),
        ("page_types", "source", "fields", "required"),
    )
    for index, path in enumerate(required_lists):
        sandbox = tmp_path / str(index)
        sandbox.mkdir()
        repository = write_instance(sandbox)
        contract_path = repository / "wiki/wiki-structure.yaml"
        data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        target = data
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = []
        contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

        result = run_portable(sandbox, repository)
        payload = json.loads(result.stdout)

        assert result.returncode == 2
        assert {item["code"] for item in payload["diagnostics"]} == {"contract.schema"}

    sandbox = tmp_path / "optional"
    sandbox.mkdir()
    repository = write_instance(sandbox)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["assets"]["forbidden_files"] = []
    data["pendency_tracking"]["warning_statuses"] = []
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    result = run_portable(sandbox, repository)

    assert result.returncode == 0, result.stdout + result.stderr


def test_required_sources_and_progressive_navigation_are_enforced(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    shutil.rmtree(repository / "wiki/sources")
    (repository / "wiki/index.md").write_text("# Knowledge base\n\n- [Page](./handbook/operations.md)\n", encoding="utf-8")

    result = run_portable(tmp_path, repository)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    codes = {item["code"] for item in payload["diagnostics"]}
    assert "topology.required-trunk" in codes
    assert "navigation.root-target" in codes
    assert "navigation.root-count" in codes


def test_configured_depth_uses_progressive_child_indexes(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["topology"]["max_depth"] = 2
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    runbooks = repository / "wiki/handbook/runbooks"
    runbooks.mkdir()
    (runbooks / "index.md").write_text("# Runbooks\n\n- [Recovery](./recovery.md)\n", encoding="utf-8")
    (runbooks / "recovery.md").write_text("---\ntype: article\nstate: current\n---\n# Recovery\n\n![Diagram](./recovery.svg)\n\n## Sources\n", encoding="utf-8")
    (runbooks / "recovery.d2").write_text("diagram\n", encoding="utf-8")
    (runbooks / "recovery.svg").write_text("svg\n", encoding="utf-8")
    (repository / "wiki/handbook/index.md").write_text("# Handbook\n\n- [Operations](./operations.md)\n- [Runbooks](./runbooks/index.md)\n", encoding="utf-8")

    result = run_portable(tmp_path, repository)

    assert result.returncode == 0, result.stdout + result.stderr


def test_frontmatter_and_reference_diagnostics_are_deterministic(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    page = repository / "wiki/handbook/operations.md"
    page.with_suffix(".d2").unlink()
    page.with_suffix(".svg").unlink()
    page.write_text("---\ntype: article\nstate: draft\nextra: true\n---\n## Operations\n\n[Missing](./missing.md)\n", encoding="utf-8")

    first = run_portable(tmp_path, repository)
    second_root = tmp_path / "second"
    second_root.mkdir()
    second = run_portable(second_root, repository)

    assert first.returncode == second.returncode == 1
    assert json.loads(first.stdout) == json.loads(second.stdout)
    payload = json.loads(first.stdout)
    assert [item["code"] for item in payload["diagnostics"] if item["path"] == "handbook/operations.md"] == [
        "frontmatter.state",
        "frontmatter.unknown",
        "reference.missing",
        "frontmatter.section",
        "h1.count",
    ]


def test_generic_provenance_checks_both_directions_and_contextual_citations(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    operations = repository / "wiki/handbook/operations.md"
    operations.write_text(
        operations.read_text(encoding="utf-8").replace(
            "## Sources\n\n- [Manual](../sources/manual.md)",
            "## Sources\n\nNone.",
        ),
        encoding="utf-8",
    )

    result = run_portable(tmp_path, repository)
    payload = json.loads(result.stdout)

    assert result.returncode == 1
    codes = {item["code"] for item in payload["diagnostics"]}
    assert "provenance.backlinks" in codes
    assert "contextual-citation.missing" in codes
    assert all("fonte" not in item["message"].lower() for item in payload["diagnostics"])


def test_configured_tracking_uses_non_doi_ids_labels_tags_and_states(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    operations = repository / "wiki/handbook/operations.md"
    operations.write_text(
        operations.read_text(encoding="utf-8").replace(
            "state: current",
            "state: suggested\nchange_ticket: job-1002",
        ).replace(
            "## Sources",
            "## Open questions\n\n- [job-1001] Confirm owner\n\n"
            "## Suggested changes\n\n- [job-1002] Replace workflow\n\n## Sources",
        ),
        encoding="utf-8",
    )
    responses = {
        "job-1001": {"ok": True, "data": {"status": "queued", "tags": ["question"]}},
        "job-1002": {"ok": True, "data": {"status": "working", "tags": ["change"]}},
        "_list:question": {"ok": True, "data": [{"id": "job-1001"}]},
        "_list:change": {"ok": True, "data": [{"id": "job-1002"}]},
    }

    result = run_portable(tmp_path, repository, responses=responses)

    assert result.returncode == 0, result.stdout + result.stderr
    assert not [item for item in json.loads(result.stdout)["diagnostics"] if item["code"].startswith(("pendency.", "proposal."))]


def test_proposal_field_is_exclusive_and_inverse_associations_are_required(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    operations = repository / "wiki/handbook/operations.md"
    operations.write_text(
        operations.read_text(encoding="utf-8").replace("state: current", "state: current\nchange_ticket: job-2001"),
        encoding="utf-8",
    )
    responses = {
        "job-2001": {"ok": True, "data": {"status": "queued", "tags": ["change"]}},
        "job-2002": {"ok": True, "data": {"status": "queued", "tags": ["question"]}},
        "_list:question": {"ok": True, "data": [{"id": "job-2002"}]},
    }

    result = run_portable(tmp_path, repository, responses=responses)
    codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}

    assert result.returncode == 1
    assert "proposal.location" in codes
    assert "pendency.inverse" in codes


def test_terminal_tracking_tickets_are_historical_warnings(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    operations = repository / "wiki/handbook/operations.md"
    operations.write_text(
        operations.read_text(encoding="utf-8").replace(
            "## Sources",
            "## Open questions\n\n- [job-3001] Historical question\n\n## Sources",
        ),
        encoding="utf-8",
    )
    responses = {
        "job-3001": {"ok": True, "data": {"status": "finished", "tags": ["question"]}},
        "_closed:question": {"ok": True, "data": [{"id": "job-3001"}]},
    }

    result = run_portable(tmp_path, repository, responses=responses)
    diagnostics = json.loads(result.stdout)["diagnostics"]

    assert result.returncode == 0
    assert [item for item in diagnostics if item["code"] == "pendency.status"]
    assert all(item["severity"] == "warning" for item in diagnostics)


def test_external_links_and_bare_urls_are_informational(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    page = repository / "wiki/handbook/operations.md"
    page.write_text(
        page.read_text(encoding="utf-8") + "\n[External](ftp://example.test) https://example.test/plain\n",
        encoding="utf-8",
    )

    result = run_portable(tmp_path, repository)

    assert result.returncode == 0, result.stdout + result.stderr
    assert not [item for item in json.loads(result.stdout)["diagnostics"] if item["code"].startswith("reference.external")]


def test_names_unknown_files_assets_and_diagram_sets_are_contract_driven(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    wiki = repository / "wiki"
    (wiki / "handbook" / "Bad Name.txt").write_text("invalid\n", encoding="utf-8")
    (wiki / "assets" / "orphan.gif").write_bytes(b"gif")
    (wiki / "handbook" / "operations.svg").unlink()
    (wiki / "handbook" / "operations.d2").write_text("diagram\n", encoding="utf-8")

    result = run_portable(tmp_path, repository)
    codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}

    assert result.returncode == 1
    assert {"topology.unknown-file", "topology.name", "assets.extension", "assets.orphan", "diagrams.incomplete"} <= codes


def test_applicable_markdown_without_diagram_files_reports_every_missing_extension(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    wiki = repository / "wiki"
    (wiki / "handbook" / "operations.d2").unlink()
    (wiki / "handbook" / "operations.svg").unlink()

    result = run_portable(tmp_path, repository)
    diagnostics = json.loads(result.stdout)["diagnostics"]
    incomplete = [item for item in diagnostics if item["code"] == "diagrams.incomplete"]

    assert result.returncode == 1
    assert incomplete == [{
        "code": "diagrams.incomplete",
        "severity": "error",
        "path": "handbook/operations",
        "line": None,
        "message": "Diagram set is incomplete; missing: .d2, .svg.",
    }]


def test_complete_diagram_embeds_visualization_and_assets_must_be_referenced(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    wiki = repository / "wiki"
    page = wiki / "handbook" / "operations.md"
    page.write_text(page.read_text(encoding="utf-8") + "\n![Logo](../assets/logo.png)\n", encoding="utf-8")
    (wiki / "assets" / "logo.png").write_bytes(b"png")

    result = run_portable(tmp_path, repository)

    assert result.returncode == 0, result.stdout + result.stderr


def test_methodology_version_accepts_only_supported_semver(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["methodology_version"] = "1.5.0"
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    before = contract_path.read_bytes()

    result = run_portable(tmp_path, repository)

    assert result.returncode == 2
    assert {item["code"] for item in json.loads(result.stdout)["diagnostics"]} == {"contract.relation"}
    assert contract_path.read_bytes() == before


def test_optional_authoring_reference_is_root_navigation_without_frontmatter(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    wiki = repository / "wiki"
    contract_path = wiki / "wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["methodology_version"] = "1.1.0"
    data["navigation"]["authoring_file"] = "AUTHORING.md"
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    (wiki / "AUTHORING.md").write_text("# Local authoring criteria\n\n## Required criteria\n\nReview meaning.\n", encoding="utf-8")
    index = wiki / "index.md"
    index.write_text(index.read_text(encoding="utf-8") + "- [Authoring](./AUTHORING.md)\n", encoding="utf-8")

    result = run_portable(tmp_path, repository)

    assert result.returncode == 0, result.stdout + result.stderr


def test_declared_authoring_reference_must_exist_and_be_linked_once(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["navigation"]["authoring_file"] = "AUTHORING.md"
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    result = run_portable(tmp_path, repository)
    diagnostics = json.loads(result.stdout)["diagnostics"]

    assert result.returncode == 1
    assert any(item["code"] == "topology.required-file" and item["path"] == "AUTHORING.md" for item in diagnostics)
    assert any(item["code"] == "navigation.root-count" and "AUTHORING.md" in item["message"] for item in diagnostics)


def test_authoring_reference_must_be_distinct_from_reserved_navigation_files(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    data["navigation"]["authoring_file"] = "CONTEXT.md"
    contract_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    result = run_portable(tmp_path, repository)

    assert result.returncode == 2
    assert {item["code"] for item in json.loads(result.stdout)["diagnostics"]} == {"contract.relation"}


def test_compatible_contract_is_preserved_during_setup_validation(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    contract_path = repository / "wiki/wiki-structure.yaml"
    before = contract_path.read_bytes()

    result = run_portable(tmp_path, repository)

    assert result.returncode == 0, result.stdout + result.stderr
    assert contract_path.read_bytes() == before


def test_terminal_tracking_warning_is_deduplicated_by_ticket_association(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    page = repository / "wiki/handbook/operations.md"
    page.write_text(
        page.read_text(encoding="utf-8").replace(
            "## Sources",
            "## Open questions\n\n- [job-3001] Historical question\n- [job-3001] Repeated historical question\n\n## Sources",
        ),
        encoding="utf-8",
    )
    responses = {
        "job-3001": {"ok": True, "data": {"status": "finished", "tags": ["question"]}},
        "_closed:question": {"ok": True, "data": [{"id": "job-3001"}]},
    }

    result = run_portable(tmp_path, repository, responses=responses)
    diagnostics = json.loads(result.stdout)["diagnostics"]

    assert result.returncode == 0
    assert len([item for item in diagnostics if item["code"] == "pendency.status"]) == 1


def test_knot_cli_failure_is_a_structured_runtime_error(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    responses = {
        "_list:question": {"ok": False, "error": {"code": "internal", "message": "tracker unavailable"}, "_exit": 1},
    }

    result = run_portable(tmp_path, repository, responses=responses)
    payload = json.loads(result.stdout)

    assert result.returncode == 2
    assert any(item["code"] == "runtime.knot" and "tracker unavailable" in item["message"] for item in payload["diagnostics"])


def test_structured_sections_validate_generic_records_values_and_disjunction(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    wiki = repository / "wiki"
    data = yaml.safe_load((wiki / "wiki-structure.yaml").read_text(encoding="utf-8"))
    data["structured_sections"] = [{
        "section": "Steps",
        "page_types": ["article"],
        "min_records": 1,
        "max_records": None,
        "fields": [
            {"name": "Owner", "value_types": ["page"], "min_items": 1, "max_items": None, "disjoint_with": ["Participants"]},
            {"name": "Participants", "value_types": ["text", "page"], "min_items": 0, "max_items": None, "empty_value": "Nobody else."},
        ],
    }]
    data["rules"]["structured_sections"] = {"severity": "error"}
    (wiki / "wiki-structure.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    page = wiki / "handbook" / "operations.md"
    page.write_text(
        "---\ntype: article\nstate: current\n---\n# Operations\n\n![Diagram](./operations.svg)\n\n## Steps\n\n### Plan\n\n"
        "- **Owner:** [Manual](../sources/manual.md)\n- **Participants:**\n  - Analyst\n  - [Operations](./operations.md)\n\n"
        "## Sources\n\n- [Manual](../sources/manual.md)\n",
        encoding="utf-8",
    )

    result = run_portable(tmp_path, repository)

    assert result.returncode == 0, result.stdout + result.stderr

    page.write_text(page.read_text(encoding="utf-8").replace("- **Participants:**\n  - Analyst\n  - [Operations](./operations.md)", "- **Participants:** Nobody else."), encoding="utf-8")
    sentinel_run = tmp_path / "sentinel"
    sentinel_run.mkdir()
    result = run_portable(sentinel_run, repository)
    assert result.returncode == 0, result.stdout + result.stderr

    page.write_text(page.read_text(encoding="utf-8").replace("Nobody else.", "[Manual](../sources/manual.md)"), encoding="utf-8")
    disjoint_run = tmp_path / "disjoint"
    disjoint_run.mkdir()
    result = run_portable(disjoint_run, repository)
    codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}
    assert result.returncode == 1
    assert "structured.disjoint" in codes

    data = yaml.safe_load((wiki / "wiki-structure.yaml").read_text(encoding="utf-8"))
    data["rules"]["structured_sections"] = {"severity": "warning"}
    (wiki / "wiki-structure.yaml").write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    warning_run = tmp_path / "warning"
    warning_run.mkdir()
    result = run_portable(warning_run, repository)
    payload = json.loads(result.stdout)
    assert result.returncode == 0, result.stdout + result.stderr
    assert payload["summary"]["warnings"] > 0
    assert "structured.disjoint" in {item["code"] for item in payload["diagnostics"]}
