from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from test_wiked_anchors import append
from test_wiked_validator import copy_runtime, run_portable, run_script, write_instance, write_intent_map


def enable_rule(tmp_path: Path, repository: Path, rule: str | None = "warning", version: str = "1.9.0") -> Path:
    """Configure the optional rule and a runtime at the minimum version."""
    config_path = repository / "wiki/wiki-structure.yaml"
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    data["methodology_version"] = version
    if rule:
        data["rules"]["heading_fragments"] = {"severity": rule}
    config_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    script = copy_runtime(tmp_path)
    (tmp_path / "portable/wiked-manifest.yaml").write_text("namespace: wiked\ndistribution_version: 1.9.0\n", encoding="utf-8")
    return script


def link_index(repository: Path, fragment: str) -> None:
    index = repository / "wiki/handbook/index.md"
    index.write_text(index.read_text(encoding="utf-8").replace("./operations.md)", f"./operations.md#{fragment})"), encoding="utf-8")


def diagnostics(result) -> list[tuple[str, str, str]]:
    return [(item["code"], item["severity"], item["path"]) for item in json.loads(result.stdout)["diagnostics"]]


@pytest.mark.parametrize("heading,fragment", [
    ("## See [Manual](../sources/manual.md) now", "see-manual-now"),
    ("## Run `make check` first", "run-make-check-first"),
    ("## ![Icon](https://example.test/icon.png) Review", "review"),
    ("## *Ação* <em>rápida</em>", "acao-rapida"),
])
def test_heading_slugs_use_reader_visible_text(tmp_path, heading, fragment):
    repository = write_instance(tmp_path)
    append(repository / "wiki/handbook/operations.md", f"{heading}\n\n[Here](#{fragment})\n")
    result = run_portable(tmp_path, repository)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("heading,fragment", [
    ("## See [Manual](../sources/manual.md) now", "see-manualsourcesmanualmd-now"),
    ("## ![Icon](https://example.test/icon.png) Review", "iconhttpsexampletesticonpng-review"),
])
def test_markdown_source_slugs_are_no_longer_targets(tmp_path, heading, fragment):
    repository = write_instance(tmp_path)
    append(repository / "wiki/handbook/operations.md", f"{heading}\n\n[Here](#{fragment})\n")
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1
    assert ("reference.fragment", "error", "handbook/operations.md") in diagnostics(result)


def test_rule_warns_on_heading_fragments_in_pages_and_intent_map(tmp_path):
    repository = write_instance(tmp_path)
    write_intent_map(repository)
    append(repository / "wiki/handbook/operations.md", "## Pendências\n\n[Local](#pendencias)\n")
    link_index(repository, "pendencias")
    script = enable_rule(tmp_path, repository)
    result = run_script(tmp_path, script, repository)
    assert result.returncode == 0, result.stdout + result.stderr
    assert sorted(diagnostics(result)) == [
        ("reference.heading_fragment", "warning", "handbook/index.md"),
        ("reference.heading_fragment", "warning", "handbook/operations.md"),
        ("reference.heading_fragment", "warning", "routes.md"),
    ]


def test_rule_accepts_explicit_anchors_and_diagram_targets(tmp_path):
    repository = write_instance(tmp_path)
    page = repository / "wiki/handbook/operations.md"
    page.write_text(page.read_text(encoding="utf-8").replace(
        "![Diagram](./operations.svg)", '![Diagram](operations.svg "wiked-diagram=process")'), encoding="utf-8")
    append(page, '<a id="pending_items"></a>\n\n## Pendências\n\n[Local](#pending_items)\n\n'
                 "[Return](operations.svg#wiked-node=review&section=pending_items)\n")
    link_index(repository, "pending_items")
    script = enable_rule(tmp_path, repository, rule="error")
    result = run_script(tmp_path, script, repository)
    assert result.returncode == 0, result.stdout + result.stderr
    assert diagnostics(result) == []


def test_rule_severity_is_configurable(tmp_path):
    repository = write_instance(tmp_path)
    link_index(repository, "operations")
    script = enable_rule(tmp_path, repository, rule="error")
    result = run_script(tmp_path, script, repository)
    assert result.returncode == 1
    assert diagnostics(result) == [("reference.heading_fragment", "error", "handbook/index.md")]


def test_rule_requires_minimum_version(tmp_path):
    repository = write_instance(tmp_path)
    script = enable_rule(tmp_path, repository, version="1.8.0")
    result = run_script(tmp_path, script, repository, "--contract-only")
    assert result.returncode == 2
    assert {item["code"] for item in json.loads(result.stdout)["diagnostics"]} == {"contract.relation"}


def test_contracts_without_the_rule_accept_heading_fragments(tmp_path):
    repository = write_instance(tmp_path)
    write_intent_map(repository)
    append(repository / "wiki/handbook/operations.md", "## Pendências\n\n[Local](#pendencias)\n")
    script = enable_rule(tmp_path, repository, rule=None)
    result = run_script(tmp_path, script, repository)
    assert result.returncode == 0, result.stdout + result.stderr
    assert diagnostics(result) == []
