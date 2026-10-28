"""Runs every case in tests.yaml, as described in SPEC.md "Testing"."""

import base64
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

GATE_DIR = Path(__file__).resolve().parents[2]
SCRIPT = GATE_DIR / "example_coverage.py"
CASES = yaml.safe_load((GATE_DIR / "tests.yaml").read_text(encoding="utf-8"))["cases"]


def page_path(page):
    return page if "/" in page else f"docs/s/{page}.md"


def write_tree(root, mapping):
    root.mkdir()
    for key, value in (mapping or {}).items():
        target = root / page_path(key)
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, dict):
            target.write_bytes(base64.b64decode(value["base64"]))
        else:
            target.write_bytes(value.encode("utf-8"))


def run(tmp, args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--base", str(tmp / "base"), "--head", str(tmp / "head"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def parse_expect(line):
    parts = line.split(" ", 2)
    return (page_path(parts[0]), parts[1], parts[2] if len(parts) > 2 else None)


def problem_key(p):
    return (p[0], p[1], p[2] or "")


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_case(case, tmp_path):
    write_tree(tmp_path / "base", case.get("base"))
    write_tree(tmp_path / "head", case.get("head"))
    args = [str(a) for a in case.get("args", [])]

    if case["exit"] == 2:
        assert run(tmp_path, args).returncode == 2
        return

    if "stdout" in case:
        result = run(tmp_path, args)
        assert result.stdout == case["stdout"], result.stderr
        assert result.returncode == case["exit"], result.stderr
        return

    result = run(tmp_path, args + ["--json"])
    assert result.returncode != 2, result.stderr
    problems = json.loads(result.stdout)
    actual = sorted(((p["path"], p["rule"], p["subject"]) for p in problems), key=problem_key)
    expected = sorted((parse_expect(e) for e in case.get("expect") or []), key=problem_key)
    assert actual == expected
    for p in problems:
        assert p["severity"] == ("warning" if p["rule"] == "exempt" else "error"), p
    assert result.returncode == case["exit"]

    result = run(tmp_path, args + ["--json", "--print-tests"])
    listed = sorted(((t["path"], t["testId"]) for t in json.loads(result.stdout)))
    want = []
    for line in case.get("tests") or []:
        page, test_id = line.split(" ", 1)
        want.append((page_path(page), test_id))
    assert listed == sorted(want)
    assert result.returncode == case["exit"]
