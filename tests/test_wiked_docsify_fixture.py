"""Synthetic viewer fixture; no consumer content or implicit dependency installs."""
from __future__ import annotations

import base64
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).parents[1]


def svg(*nodes: str) -> str:
    groups = []
    for index, name in enumerate(nodes):
        identity = base64.b64encode(name.encode("ascii")).decode("ascii")
        y = 20 + index * 100
        groups.append(f'<g class="{identity}"><rect x="20" y="{y}" width="200" height="60" '
                      f'fill="#E5F3FF"/><text x="30" y="{y + 30}">Receive request</text></g>')
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 260 340">' + ''.join(groups) + '</svg>'


def write_browser_fixture(root: Path) -> None:
    viewer = root / "viewer"
    content = root / "wiki/handbook"
    viewer.mkdir()
    content.mkdir(parents=True)
    example = ROOT / "distr/agents/skills/wiked/viewers/index.html"
    html = example.read_text(encoding="utf-8")
    docsify = os.environ.get("WIKED_DOCSIFY_JS")
    if docsify:
        shutil.copyfile(docsify, viewer / "docsify.min.js")
        html = html.replace("https://cdn.jsdelivr.net/npm/docsify@4.13.1/lib/docsify.min.js", "docsify.min.js")
    (viewer / "index.html").write_text(html, encoding="utf-8")
    (root / "wiki/index.md").write_text('# Wiki\n\n[Process](handbook/process.md)\n', encoding="utf-8")
    (root / "wiki/other.md").write_text('# Other entry\n\n[Process](handbook/process.md)\n', encoding="utf-8")
    (content / "process.svg").write_text(svg("receive", "receive_again"), encoding="utf-8")
    (content / "other.svg").write_text(svg("receive"), encoding="utf-8")
    (content / "process.md").write_text(
        '# Process\n\n![Flow](process.svg "wiked-diagram=process")\n\n'
        '![Other flow](other.svg "wiked-diagram=other")\n\n'
        '<a id="step_receive"></a>\n\n## Receive request\n\nRegister the request.\n\n'
        '[Back to step in diagram: Receive request - initial](process.svg#wiked-node=receive&section=step_receive)\n\n'
        '[Back to step in diagram: Receive request - retry](process.svg#wiked-node=receive_again&section=step_receive)\n\n'
        '<a id="step_other"></a>\n\n## Receive request\n\nAnother flow.\n\n'
        '[Back to step in diagram: Receive request - other flow](other.svg#wiked-node=receive&section=step_other)\n\n'
        '[Other entry](../other.md)\n', encoding="utf-8",
    )
