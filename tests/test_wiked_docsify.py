from __future__ import annotations

import os
import base64
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]


def test_docsify_adapter_control_flow_with_dependency_free_node():
    node = shutil.which("node")
    if not node:
        pytest.skip("Node is not installed; adapter control-flow checks were not run")
    result = subprocess.run(
        [node, "--test", str(ROOT / "tests/js/docsify-diagrams.test.cjs")],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_adapter_metadata_and_resource_checks_with_installed_d2(tmp_path):
    d2 = shutil.which("d2")
    node = shutil.which("node")
    if not d2 or not node:
        pytest.skip("D2 and Node must already be installed for renderer compatibility checks")
    source = tmp_path / "process.d2"
    rendered = tmp_path / "process.svg"
    source.write_text("direction: down\nreceive: Receive request\nteam: {\n  receive_again: Receive request\n}\nreceive -> team.receive_again\n", encoding="utf-8")
    result = subprocess.run([d2, "--bundle=true", "--theme=4", "--layout=elk", str(source), str(rendered)],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    svg = ET.fromstring(rendered.read_text(encoding="utf-8"))
    classes = {value for element in svg.iter() for value in element.get("class", "").split()}
    for identifier in ("receive", "team.receive_again"):
        encoded = base64.b64encode(identifier.encode("ascii")).decode("ascii")
        assert encoded in classes or encoded.rstrip("=") in classes
    resources = [attribute for element in svg.iter() for attribute in element.attrib.values()]
    resources += [element.text or "" for element in svg.iter() if element.tag.endswith("}style")]
    adapter = ROOT / "tests/js/docsify-example.cjs"
    script = "const api=require(process.argv[1]);let s='';process.stdin.on('data',c=>s+=c);process.stdin.on('end',()=>{if(!JSON.parse(s).every(api.safeCSS))process.exit(1)});"
    checked = subprocess.run([node, "-e", script, str(adapter)], input=json.dumps(resources),
                             capture_output=True, text=True, timeout=30)
    assert checked.returncode == 0, checked.stderr


def test_docsify_browser_integration(tmp_path):
    """Real Docsify/browser test; explicit opt-in avoids downloads in default tests."""
    if os.environ.get("WIKED_BROWSER_TESTS") != "1":
        pytest.skip("Set WIKED_BROWSER_TESTS=1 with playwright-cli and a browser already installed")
    cli = shutil.which("playwright-cli")
    assert cli, "playwright-cli must be human-installed; tests never install tools"
    # Import only for this explicitly selected browser verification.
    import functools
    import http.server
    import threading

    from test_wiked_docsify_fixture import write_browser_fixture

    write_browser_fixture(tmp_path)
    config = tmp_path / "browser-config.json"
    config.write_text(json.dumps({"browser": {"browserName": "chromium", "launchOptions": {
        "headless": True, "chromiumSandbox": False,
    }}}), encoding="utf-8")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp_path))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    session = f"wiked-docsify-{os.getpid()}"

    def invoke(*args):
        return subprocess.run([cli, "-s=" + session, *args], cwd=tmp_path,
                              text=True, capture_output=True, timeout=120)

    try:
        opened = invoke("open", f"http://127.0.0.1:{server.server_port}/viewer/index.html#/handbook/process",
                        "--config=" + os.environ.get("WIKED_PLAYWRIGHT_CONFIG", str(config)))
        assert opened.returncode == 0, opened.stdout + opened.stderr
        code = (ROOT / "tests/js/docsify-browser-check.js").read_text(encoding="utf-8")
        result = invoke("run-code", code)
        assert result.returncode == 0 and "WIKED_BROWSER_PASS" in result.stdout, result.stdout + result.stderr
        print(result.stdout.split("### Ran Playwright code", 1)[0])
    finally:
        invoke("close")
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
