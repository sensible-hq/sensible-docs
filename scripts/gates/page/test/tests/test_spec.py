"""Runs every case in tests.yaml against page_gate.py, as SPEC.md "Testing" describes."""

import base64
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

GATE_DIR = Path(__file__).resolve().parents[2]
GATE = GATE_DIR / "page_gate.py"
CASES = yaml.safe_load((GATE_DIR / "tests.yaml").read_text(encoding="utf-8"))["cases"]
ALPHABETICAL = "scripts/gates/page/alphabetical-folders.yaml"
STRICT_RULES = {
    "json-line-comment", "output-comment", "json5-header-missing",
    "json5-header-repeated", "order-stale", "order-unlisted", "order-unsorted",
}


def page_path(case, slug):
    return case.get("paths", {}).get(slug, f"docs/s/{slug}.md")


def write(root, rel, data):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        p.write_bytes(data)
    else:
        p.write_text(data, encoding="utf-8", newline="\n")


def build(root, case):
    for slug, value in (case.get("pages") or {}).items():
        if isinstance(value, dict):
            title = value.get("title", slug)
            body = value.get("body", "Body.\n")
        else:
            title, body = slug, value
        write(root, page_path(case, slug), f"---\ntitle: {json.dumps(title)}\n---\n{body}")
    for rel, value in (case.get("files") or {}).items():
        if isinstance(value, dict):
            write(root, rel, base64.b64decode(value["base64"]))
        else:
            write(root, rel, value)
    orders = case.get("orders") or {}
    for folder, value in orders.items():
        (root / folder).mkdir(parents=True, exist_ok=True)
        if value is None:
            continue
        text = value if isinstance(value, str) else yaml.safe_dump(value, default_flow_style=False)
        write(root, f"{folder}/_order.yaml", text)
    docs = root / "docs"
    if docs.is_dir():
        for dirpath, dirnames, filenames in os.walk(docs):
            folder = Path(dirpath).relative_to(root).as_posix()
            if folder in orders:
                continue
            listed = sorted(dirnames) + sorted(
                f[:-3] for f in filenames if f.endswith(".md") and f != "index.md")
            write(root, f"{folder}/_order.yaml", yaml.safe_dump(listed, default_flow_style=False))
    if "alphabetical" in case:
        write(root, ALPHABETICAL, yaml.safe_dump(case["alphabetical"], default_flow_style=False))


def run_gate(root, args):
    return subprocess.run([sys.executable, str(GATE), *args], cwd=root,
                          capture_output=True, text=True, encoding="utf-8")


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_case(case, tmp_path):
    build(tmp_path, case)
    args = [str(a) for a in case.get("args", [])]

    if case["exit"] == 2:
        result = run_gate(tmp_path, args)
        assert result.returncode == 2, result.stdout + result.stderr
        return

    if "stdout" in case:
        result = run_gate(tmp_path, args)
        assert result.stdout == case["stdout"], result.stderr
        assert result.returncode == case["exit"]
        return

    result = run_gate(tmp_path, args + ["--json"])
    problems = json.loads(result.stdout)
    strict = "--strict" in args
    got = [(p["path"], p["rule"], p["subject"]) for p in problems]
    want = []
    for line in case["expect"]:
        parts = line.split(" ", 2)
        page, rule = parts[0], parts[1]
        subject = parts[2] if len(parts) > 2 else None
        path = page_path(case, page) if page in (case.get("pages") or {}) else page
        want.append((path, rule, subject))
    key = lambda t: (t[0], t[1], t[2] is not None, t[2] or "")
    assert sorted(got, key=key) == sorted(want, key=key), result.stderr
    for p in problems:
        if p["rule"] == "json5-comment-repeated":
            expected = "warning"
        elif p["rule"] in STRICT_RULES:
            expected = "error" if strict else "warning"
        else:
            expected = "error"
        assert p["severity"] == expected, p
    assert result.returncode == case["exit"], result.stdout + result.stderr
