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


def build(root, files):
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, dict):
            path.write_bytes(base64.b64decode(content["base64"]))
        else:
            path.write_bytes(content.encode("utf-8"))


def run(root, args):
    return subprocess.run(
        [sys.executable, str(GATE), "--root", str(root), *args],
        capture_output=True,
    )


def key(problem):
    subject = problem.get("subject")
    return (problem["path"], problem["rule"], subject is not None, subject or "")


def normalize(problem):
    return {
        "path": problem["path"],
        "rule": problem["rule"],
        "severity": problem["severity"],
        "subject": problem.get("subject"),
    }


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_case(case, tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    build(root, case["files"])
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
    want = sorted((normalize(p) for p in case["problems"]), key=key)
    assert got == want
    assert result.returncode == case["exit"]
