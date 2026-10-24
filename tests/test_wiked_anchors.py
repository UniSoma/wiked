from __future__ import annotations

import json
from pathlib import Path

import pytest

from test_wiked_validator import run_portable, write_instance


def append(path: Path, body: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + "\n" + body, encoding="utf-8")


def test_portable_explicit_anchors_survive_heading_renames_and_decode_links(tmp_path):
    repository = write_instance(tmp_path)
    page = repository / "wiki/handbook/operations.md"
    page.write_text(page.read_text(encoding="utf-8").replace(
        '![Diagram](./operations.svg)', '![Diagram](operations.svg "wiked-diagram=process")'), encoding="utf-8")
    append(page, '<a id="step_receive"></a>\n\n## Renamed request handling\n\n'
                 '[Step](#%73tep_receive)\n\n'
                 '[Return](operations.svg#wiked-node=review.receive&section=step_receive)\n')
    index = repository / "wiki/handbook/index.md"
    index.write_text(index.read_text(encoding="utf-8").replace("./operations.md)", "./operations.md#step_receive)"), encoding="utf-8")
    result = run_portable(tmp_path, repository)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("body", [
    '```html\n<a id="hidden"></a>\n```\n',
    '`<a id="hidden"></a>`\n',
    '<!-- <a id="hidden"></a> -->\n',
    '&lt;a id="hidden"&gt;&lt;/a&gt;\n',
])
def test_anchor_examples_and_comments_are_not_targets(tmp_path, body):
    repository = write_instance(tmp_path)
    append(repository / "wiki/handbook/operations.md", body + '\n[Missing](#hidden)\n')
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1
    assert any(item["code"] == "reference.fragment" for item in json.loads(result.stdout)["diagnostics"])


@pytest.mark.parametrize("body", [
    '<a id="step_receive"></a>\n\n<a id="step_receive"></a>\n',
    '<a id="operations"></a>\n',
])
def test_explicit_anchor_duplicates_and_heading_collisions_are_reported(tmp_path, body):
    repository = write_instance(tmp_path)
    append(repository / "wiki/handbook/operations.md", body)
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1
    diagnostics = json.loads(result.stdout)["diagnostics"]
    assert any(item["code"] == "reference.anchor" and item["line"] for item in diagnostics)


@pytest.mark.parametrize("fragment,code", [
    ("wiked-node=receive&section=missing", "reference.fragment"),
    ("section=missing&wiked-node=receive", "reference.fragment"),
    ("wiked-node=receive", "reference.diagram"),
    ("wiked-node=receive&section=step_receive&section=other", "reference.diagram"),
    ("wiked-node=Receive&section=step_receive", "reference.diagram"),
    ("wiked-node=receive&section=step_receive&extra=x", "reference.diagram"),
])
def test_optional_diagram_return_links_validate_identity_and_description(tmp_path, fragment, code):
    repository = write_instance(tmp_path)
    append(repository / "wiki/handbook/operations.md",
           '<a id="step_receive"></a>\n\n## Receive request\n\n'
           f'[Return](operations.svg#{fragment})\n')
    result = run_portable(tmp_path, repository)
    assert result.returncode == 1
    assert any(item["code"] == code for item in json.loads(result.stdout)["diagnostics"])


def test_unmarked_static_diagram_and_existing_heading_links_remain_valid(tmp_path):
    repository = write_instance(tmp_path)
    append(repository / "wiki/handbook/operations.md", '[Heading](#operations)\n')
    result = run_portable(tmp_path, repository)
    assert result.returncode == 0, result.stdout + result.stderr
