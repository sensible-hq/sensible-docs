"""Runs every case in tests.yaml against frontmatter_gate.py, as SPEC.md "Testing" describes."""

import base64
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

GATE_DIR = Path(__file__).resolve().parents[2]
GATE = GATE_DIR / "frontmatter_gate.py"
CASES = yaml.safe_load((GATE_DIR / "tests.yaml").read_text(encoding="utf-8"))["cases"]


def page_text(docops):
    """The file for one `pages` entry: frontmatter with a title and, unless null, a docops line."""
    lines = ["---", "title: T"]
    if docops is not None:
        if isinstance(docops, dict) and "page_type" not in docops:
            docops = {"page_type": "reference", **docops}
        lines.append("docops: " + json.dumps(docops))
    return "\n".join(lines) + "\n---\n\nBody.\n"


def build(root, case):
    """Writes the case's pages and files; returns {page key or files path: repo-relative path}."""
    paths = case.get("paths") or {}
    contents = {}
    for slug, docops in (case.get("pages") or {}).items():
        contents[paths.get(slug, f"docs/s/{slug}.md")] = (slug, page_text(docops))
    for rel, content in (case.get("files") or {}).items():
        contents[rel] = (rel, content)

    names = {}
    for rel, (name, content) in contents.items():
        names[name] = rel
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, dict):
            path.write_bytes(base64.b64decode(content["base64"]))
        else:
            path.write_bytes(content.encode("utf-8"))
    return names


def expected(case, names):
    """Turns each "<page> <rule> [<subject>]" line into a problem."""
    require = "--require" in (case.get("args") or [])
    problems = []
    for line in case["expect"]:
        page, rule, *rest = line.split(" ", 2)
        warning = rule == "missing-docops" and not require
        problems.append({
            "path": names[page],
            "rule": rule,
            "severity": "warning" if warning else "error",
            "subject": rest[0] if rest else None,
        })
    return problems


def run(root, args):
    return subprocess.run(
        [sys.executable, str(GATE), "--root", str(root), *args],
        capture_output=True,
    )


def key(problem):
    subject = problem.get("subject")
    return (problem["path"], problem["rule"], subject is not None, subject or "")


def normalize(problem):
    return {k: problem.get(k) for k in ("path", "rule", "severity", "subject")}


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_case(case, tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    names = build(root, case)
    args = list(case.get("args") or [])

    if case["exit"] == 2:
        result = run(root, args)
        assert result.returncode == 2, result.stderr.decode("utf-8", "replace")
        return

    if "stdout" in case:
        result = run(root, args)
        assert result.stdout.decode("utf-8") == case["stdout"]
        assert result.returncode == case["exit"]
        return

    if "--json" not in args:
        args.append("--json")
    result = run(root, args)
    assert result.returncode in (0, 1), result.stderr.decode("utf-8", "replace")
    got = sorted((normalize(p) for p in json.loads(result.stdout)), key=key)
    want = sorted(expected(case, names), key=key)
    assert got == want
    assert result.returncode == case["exit"]
