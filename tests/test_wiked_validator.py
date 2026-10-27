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
    assert "METHODOLOGY_VERSION" not in runtime
    assert "from distribution import distribution_version" in runtime

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
    assert json.loads(result.stdout)["contract"] == {"methodology_version": "1.0.0"}
    incompatible = contract()
    incompatible["methodology_version"] = "2.0.0"
    path.write_text(yaml.safe_dump(incompatible))
    assert invoke().returncode == 2
    path.unlink()
    result = invoke()
    assert result.returncode == 2
    assert "contract" not in json.loads(result.stdout)
    assert not (tmp_path / "tracker-called").exists()


def test_namespaced_setup_command_routes_to_the_distributed_guide() -> None:
    manifest = yaml.safe_load((DISTRIBUTION / "wiked-manifest.yaml").read_text(encoding="utf-8"))
    command = (DISTRIBUTION / "commands/wiked-setup.md").read_text(encoding="utf-8")

    assert "commands/wiked-setup.md" in manifest["components"]["commands"]
    assert "guides/setup.md" in command


def test_human_qualification_and_ingestion_stay_outside_the_contract() -> None:
    schema = json.loads((WIKED / "contracts/wiki-structure.schema.json").read_text(encoding="utf-8"))

    assert "human_authority" not in schema["properties"]
    assert "ingestion" not in schema["properties"]


def test_indexing_documents_the_archive_path_template() -> None:
    indexing = (WIKED / "guides/assisted-indexing.md").read_text(encoding="utf-8")
    assert "raw/archive/YYYY-MM-DD_<ticket-id>/" in indexing


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
    distribution = root / "portable" / "skills" / "wiked"
    shutil.copytree(WIKED / "scripts", distribution / "scripts")
    shutil.copytree(WIKED / "contracts", distribution / "contracts")
    shutil.copyfile(DISTRIBUTION / "wiked-manifest.yaml", root / "portable" / "wiked-manifest.yaml")
    return distribution / "scripts" / "validate_wiki.py"


def test_runtime_uses_only_its_distribution_manifest_for_version(tmp_path: Path) -> None:
    script = copy_runtime(tmp_path)
    repository = tmp_path / "consumer"
    (repository / "wiki").mkdir(parents=True)
    value = contract()
    value["methodology_version"] = "1.9.0"
    (repository / "wiki/wiki-structure.yaml").write_text(yaml.safe_dump(value))
    # A consumer-local manifest is not the runtime's authority.
    (repository / "wiked-manifest.yaml").write_text("namespace: wiked\ndistribution_version: 9.0.0\n")
    manifest = tmp_path / "portable/wiked-manifest.yaml"

    def invoke():
        return subprocess.run(
            ["uv", "run", "--script", str(script), "--repository-root", str(repository),
             "--contract-only", "--format", "json"], cwd=repository,
            capture_output=True, text=True,
        )

    assert invoke().returncode == 2
    manifest.write_text("namespace: wiked\ndistribution_version: 1.9.0\n")
    assert invoke().returncode == 0
    for content in ("namespace: wiked\ndistribution_version: invalid\n", "[]\n"):
        manifest.write_text(content)
        result = invoke()
        assert result.returncode == 2
        assert "runtime.version" in result.stdout
    manifest.unlink()
    result = invoke()
    assert result.returncode == 2 and "runtime.version" in result.stdout


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


def write_intent_map(repository: Path, content: str | None = None) -> Path:
    wiki = repository / "wiki"
    config_path = wiki / "wiki-structure.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["methodology_version"] = "1.5.0"
    config["navigation"]["intent_map"] = "routes.md"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    index = wiki / "index.md"
    index.write_text(index.read_text(encoding="utf-8") + "\n## Transversal references\n\n- [Intent routes](routes.md)\n", encoding="utf-8")
    path = wiki / "routes.md"
    path.write_text(content if content is not None else (
        "# Intent routes\n\nSelected consultation points, not exhaustive coverage.\n\n"
        "## Understand the practice\n\n"
        "- [Operations](handbook/operations.md#operations) - Read the canonical description.\n"
        "- [Sources](sources/index.md) - Locate provenance records.\n\n"
        "## Locate the practice\n\n"
        "- [Operations](handbook/operations.md) - Consult the same canonical practice.\n"
        "- [Handbook](handbook/index.md) - Locate related knowledge.\n"
    ), encoding="utf-8")
    return path


def test_intent_map_is_optional_and_accepts_shared_cross_trunk_destinations(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    write_intent_map(repository)
    result = run_portable(tmp_path, repository)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["summary"] == {"files_checked": 7, "errors": 0, "warnings": 0}
    assert json.loads(result.stdout)["contract"] == {"methodology_version": "1.5.0"}


@pytest.mark.parametrize("name", ["index.md", "CONTEXT.md", "authoring.md", "nested/routes.md", "../routes.md", "routes.yaml"])
def test_intent_map_rejects_collisions_and_invalid_configuration(tmp_path: Path, name: str) -> None:
    repository = write_instance(tmp_path)
    write_intent_map(repository)
    config_path = repository / "wiki/wiki-structure.yaml"
    config = yaml.safe_load(config_path.read_text())
    config["navigation"]["authoring_file"] = "authoring.md"
    config["navigation"]["intent_map"] = name
    config_path.write_text(yaml.safe_dump(config))
    result = run_portable(tmp_path, repository)
    assert result.returncode == 2, result.stdout + result.stderr
    assert json.loads(result.stdout)["summary"]["files_checked"] == 0


def test_intent_map_contract_only_checks_minimum_version_not_content(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    path = write_intent_map(repository)
    path.write_bytes(b"\xff")
    script = copy_runtime(tmp_path)
    command = ["uv", "run", "--script", str(script), "--repository-root", str(repository), "--contract-only", "--format", "json"]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["summary"]["files_checked"] == 0
    path.unlink()
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    config_path = repository / "wiki/wiki-structure.yaml"
    config = yaml.safe_load(config_path.read_text())
    config["methodology_version"] = "1.4.1"
    config_path.write_text(yaml.safe_dump(config))
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 2
    assert "1.5.0 or newer" in result.stdout


@pytest.mark.parametrize("change,code", [("missing", "topology.required-file"), ("unlinked", "navigation.root-count"), ("duplicate", "navigation.root-count")])
def test_declared_map_must_exist_and_be_linked_once(tmp_path: Path, change: str, code: str) -> None:
    repository = write_instance(tmp_path)
    path = write_intent_map(repository)
    index = repository / "wiki/index.md"
    if change == "missing":
        path.unlink()
    elif change == "unlinked":
        index.write_text(index.read_text().replace("- [Intent routes](routes.md)", ""))
    else:
        index.write_text(index.read_text() + "\n## Another section\n\n- [Routes](routes.md#intent-routes)\n")
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1
    assert code in {item["code"] for item in json.loads(result.stdout)["diagnostics"]}


@pytest.mark.parametrize("content,code", [
    ("# Routes\n", "intent-map.intent"),
    ("# Routes\n\n## Intent\n", "intent-map.destinations"),
    ("# Routes\n\n## Intent\n\n- [Operations](handbook/operations.md)\n", "intent-map.entry"),
    ("# Routes\n\n## Intent\n\n- [Operations](handbook/operations.md) - \n", "intent-map.entry"),
    ("# Routes\n\n##\n\n- [Operations](handbook/operations.md) - Consult here.\n", "intent-map.intent"),
    ("## Intent\n\n- [Operations](handbook/operations.md) - Consult here.\n", "intent-map.title"),
    ("# Routes\n\n```markdown\n## Fake intent\n- [Operations](handbook/operations.md) - Consult here.\n```\n", "intent-map.intent"),
    ("# Routes\n\n> ## Fake intent\n> - [Operations](handbook/operations.md) - Consult here.\n", "intent-map.intent"),
    ("# Routes\n\n## Intent\n\n- Group\n  - [Operations](handbook/operations.md) - Consult here.\n", "intent-map.entry"),
    ("# Routes\n\n## Intent\n\n### Subheading\n\n- [Operations](handbook/operations.md) - Consult here.\n", "intent-map.structure"),
    ("# Routes\n\n## Intent\n\n1. [Operations](handbook/operations.md) - Consult here.\n", "intent-map.structure"),
    ("# Routes\n\n## Intent\n\n- [Operations](handbook/operations.md) - Consult [elsewhere](sources/index.md).\n", "intent-map.entry"),
    ("---\ntype: article\nstate: current\n---\n# Routes\n\n## Intent\n\n- [Operations](handbook/operations.md) - Consult here.\n", "intent-map.frontmatter"),
])
def test_intent_map_requires_real_intents_destinations_and_guidance(tmp_path: Path, content: str, code: str) -> None:
    repository = write_instance(tmp_path)
    write_intent_map(repository, content)
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1, result.stdout + result.stderr
    diagnostics = json.loads(result.stdout)["diagnostics"]
    assert code in {item["code"] for item in diagnostics}
    assert not any(item["code"].startswith(("provenance.", "diagrams.", "pendency.", "proposal.")) for item in diagnostics)


@pytest.mark.parametrize("target,label,code", [
    ("sources/manual.md", "Manual", "intent-map.destination"),
    ("CONTEXT.md", "Context", "intent-map.destination"),
    ("routes.md", "Intent routes", "intent-map.destination"),
    ("wiki-structure.yaml", "Contract", "intent-map.destination"),
    ("handbook/missing.md", "Missing", "reference.missing"),
    ("../raw/source.md", "Raw", "reference.boundary"),
    ("../.tickets/task.md", "Task", "reference.boundary"),
    ("../.agents/instructions.md", "Instructions", "reference.boundary"),
    ("https://example.test/page.md", "External", "intent-map.destination"),
    ("handbook/operations.md?query=1", "Operations", "intent-map.destination"),
    ("handbook/operations.md", "Alias", "intent-map.label"),
    ("handbook/operations.md#missing", "Operations", "reference.fragment"),
])
def test_intent_map_references_only_canonical_operational_pages_or_indexes(tmp_path: Path, target: str, label: str, code: str) -> None:
    repository = write_instance(tmp_path)
    write_intent_map(repository, f"# Intent routes\n\n## Intent\n\n- [{label}]({target}) - Consult here.\n")
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1, result.stdout + result.stderr
    assert code in {item["code"] for item in json.loads(result.stdout)["diagnostics"]}


def test_map_does_not_relax_index_duplicates_or_cross_trunk_shortcuts(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    path = write_intent_map(repository)
    path.write_text(path.read_text() + "\n- [Handbook](handbook/index.md#handbook) - A repeated destination.\n")
    index = repository / "wiki/handbook/index.md"
    index.write_text(index.read_text() + "\n## Another grouping\n\n- [Operations](operations.md#operations)\n- [Sources](../sources/index.md)\n")
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1
    codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}
    assert {"intent-map.duplicate", "navigation.trunk-count", "navigation.trunk-target"} <= codes


def test_intent_map_accepts_instance_language_and_configured_filename(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    path = write_intent_map(repository, "# Rotas por inten\u00e7\u00e3o\n\n## Consultar uma pr\u00e1tica\n\n- [Operations](handbook/operations.md) - Consulte a descri\u00e7\u00e3o can\u00f4nica.\n")
    renamed = path.with_name("rotas.md")
    path.rename(renamed)
    config_path = repository / "wiki/wiki-structure.yaml"
    config = yaml.safe_load(config_path.read_text())
    config["language"] = "pt-BR"
    config["navigation"]["intent_map"] = renamed.name
    config_path.write_text(yaml.safe_dump(config))
    index = repository / "wiki/index.md"
    index.write_text(index.read_text().replace("routes.md", "rotas.md"))
    result = run_portable(tmp_path, repository)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("kind", ["absolute", "symlink", "authoring", "duplicate-fragments"])
def test_intent_map_cannot_bypass_destination_boundaries(tmp_path: Path, kind: str) -> None:
    repository = write_instance(tmp_path)
    wiki = repository / "wiki"
    label = "Operations"
    target = "handbook/operations.md"
    if kind == "absolute":
        target = str(wiki / target)
    elif kind == "symlink":
        outside = tmp_path / "outside.md"
        outside.write_text("# Operations\n")
        (wiki / "handbook/linked.md").symlink_to(outside)
        target = "handbook/linked.md"
    elif kind == "authoring":
        config_path = wiki / "wiki-structure.yaml"
        config = yaml.safe_load(config_path.read_text())
        config["navigation"]["authoring_file"] = "authoring.md"
        config_path.write_text(yaml.safe_dump(config))
        (wiki / "authoring.md").write_text("# Authoring\n")
        index = wiki / "index.md"
        index.write_text(index.read_text() + "\n- [Authoring](authoring.md)\n")
        label, target = "Authoring", "authoring.md"
    content = f"# Intent routes\n\n## Intent\n\n- [{label}]({target}) - Consult here.\n"
    if kind == "duplicate-fragments":
        content += "- [Operations](handbook/operations.md#sources) - Consult provenance here.\n"
    write_intent_map(repository, content)
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1, result.stdout + result.stderr
    codes = {item["code"] for item in json.loads(result.stdout)["diagnostics"]}
    assert ("intent-map.duplicate" if kind == "duplicate-fragments" else "intent-map.destination") in codes


def test_intent_map_diagnostics_reuse_navigation_severity(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    write_intent_map(repository, "# Intent routes\n\n## Intent\n")
    config_path = repository / "wiki/wiki-structure.yaml"
    config = yaml.safe_load(config_path.read_text())
    config["rules"]["navigation"]["severity"] = "warning"
    config_path.write_text(yaml.safe_dump(config))
    result = run_portable(tmp_path, repository)
    assert result.returncode == 0, result.stdout + result.stderr
    diagnostics = json.loads(result.stdout)["diagnostics"]
    assert diagnostics and all(item["severity"] == "warning" for item in diagnostics)


def test_map_frontmatter_never_enters_operational_record_validation(tmp_path: Path) -> None:
    repository = write_instance(tmp_path)
    write_intent_map(repository, "---\ntype: article\nstate: suggested\nchange_ticket: job-9999\n---\n# Intent routes\n")
    config_path = repository / "wiki/wiki-structure.yaml"
    config = yaml.safe_load(config_path.read_text())
    config["structured_sections"] = [{
        "section": "Records", "page_types": ["article"], "min_records": 1, "max_records": None,
        "fields": [{"name": "Description", "value_types": ["text"], "min_items": 1, "max_items": 1}],
    }]
    config["rules"]["structured_sections"] = {"severity": "error"}
    config_path.write_text(yaml.safe_dump(config))
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1, result.stdout + result.stderr
    map_diagnostics = [item for item in json.loads(result.stdout)["diagnostics"] if item["path"] == "routes.md"]
    assert {item["code"] for item in map_diagnostics} == {"intent-map.frontmatter"}


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
    manifest = yaml.safe_load((DISTRIBUTION / "wiked-manifest.yaml").read_text(encoding="utf-8"))
    major, minor, patch = map(int, manifest["distribution_version"].split("."))
    data["methodology_version"] = f"{major}.{minor}.{patch + 1}"
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
