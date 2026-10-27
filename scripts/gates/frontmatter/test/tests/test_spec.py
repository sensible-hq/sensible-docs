"""Runs every case in tests.yaml against frontmatter_gate.py, as SPEC.md "Testing" describes."""
import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

GATE_DIR = Path(__file__).resolve().parents[2]
GATE = GATE_DIR / "frontmatter_gate.py"
CASES = yaml.safe_load((GATE_DIR / "tests.yaml").read_text(encoding="utf-8"))["cases"]


def _key(problem):
    return (problem["path"], problem["rule"], problem["severity"], problem.get("subject"))


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_case(case, tmp_path):
    for rel, content in case["files"].items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    text_mode = "stdout" in case
    args = [sys.executable, str(GATE), "--root", str(tmp_path), *case.get("args", [])]
    if not text_mode:
        args.append("--json")
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")

    assert result.returncode == case["exit"], result.stdout + result.stderr
    if case["exit"] == 2:
        return

    if text_mode:
        assert result.stdout == case["stdout"]
    else:
        actual = json.loads(result.stdout)
        actual_set = {_key(p) for p in actual}
        assert len(actual_set) == len(actual), f"duplicate problems: {actual}"
        assert actual_set == {_key(p) for p in case["problems"]}
