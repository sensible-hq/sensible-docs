"""Runs every case in tests.yaml as described in SPEC.md "Testing"."""

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


def page_text(value):
    lines = ["---", "title: T"]
    if value is not None:
        if isinstance(value, dict) and "page_type" not in value:
            value = {"page_type": "reference", **value}
        lines.append("docops: " + json.dumps(value))
    lines += ["---", "", "Body.", ""]
    return "\n".join(lines)


def page_path(case, key):
    return case.get("paths", {}).get(key, f"docs/s/{key}.md")


def build(case, root):
    for key, value in (case.get("pages") or {}).items():
        path = root / page_path(case, key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page_text(value), encoding="utf-8")
    for rel, content in (case.get("files") or {}).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, dict):
            path.write_bytes(base64.b64decode(content["base64"]))
        else:
            path.write_bytes(content.encode("utf-8"))


def run(args, cwd):
    return subprocess.run(
        [sys.executable, str(GATE), *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def subject_text(subject):
    if subject is None or isinstance(subject, str):
        return subject
    return json.dumps(subject)


def sort_key(problem):
    path, rule, severity, subject = problem
    return (path, rule, subject or "", severity)


def expected_problems(case, args):
    pages = case.get("pages") or {}
    problems = []
    for line in case["expect"]:
        parts = line.split(" ", 2)
        page, rule = parts[0], parts[1]
        subject = parts[2] if len(parts) == 3 else None
        path = page_path(case, page) if page in pages else page
        if rule == "missing-docops" and "--require" not in args:
            severity = "warning"
        else:
            severity = "error"
        problems.append((path, rule, severity, subject))
    return sorted(problems, key=sort_key)


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_case(case, tmp_path):
    build(case, tmp_path)
    args = list(case.get("args") or [])

    if case["exit"] == 2:
        result = run(args, tmp_path)
        assert result.returncode == 2, result.stderr
        return

    if "stdout" in case:
        result = run(args, tmp_path)
        assert result.stdout == case["stdout"], result.stderr
        assert result.returncode == case["exit"], result.stderr
        return

    result = run(args + ["--json"], tmp_path)
    actual = sorted(
        (
            (p["path"], p["rule"], p["severity"], subject_text(p["subject"]))
            for p in json.loads(result.stdout)
        ),
        key=sort_key,
    )
    assert actual == expected_problems(case, args), result.stderr
    assert result.returncode == case["exit"], result.stderr
