"""Runs every case in tests.yaml as described in SPEC.md "Testing"."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

GATE_DIR = Path(__file__).resolve().parents[2]
GATE = GATE_DIR / "public_diff_paths.py"
CASES = yaml.safe_load((GATE_DIR / "tests.yaml").read_text(encoding="utf-8"))["cases"]
GIT_ENV = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, env=GIT_ENV, check=True, capture_output=True)


def write(repo, files):
    for rel, text in (files or {}).items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))


def build(case, tmp):
    repo = tmp / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "base")
    write(repo, case.get("base") or {"README.md": "readme\n"})
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    git(repo, "checkout", "-q", "-b", "head")
    write(repo, case.get("head"))
    for rel in case.get("delete") or []:
        (repo / rel).unlink()
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", "head")
    if "base_after" in case:
        git(repo, "checkout", "-q", "base")
        write(repo, case["base_after"])
        git(repo, "add", "-A")
        git(repo, "commit", "-q", "-m", "base after")
    (tmp / "denylist.txt").write_text(case.get("denylist", ""), encoding="utf-8")
    return repo


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_case(case, tmp_path):
    repo = build(case, tmp_path)
    default = ["--base", "base", "--head", "head", "--denylist", "$TMP/denylist.txt"]
    args = [str(a).replace("$TMP", str(tmp_path)) for a in case.get("args", default)]
    res = subprocess.run([sys.executable, str(GATE), *args], cwd=repo, capture_output=True,
                         text=True, encoding="utf-8")
    detail = f"\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
    assert res.returncode == case["exit"], detail
    if res.returncode == 2:
        assert res.stdout == "", detail
        lines = res.stderr.splitlines()
        assert len(lines) == 1 and lines[0].startswith("public_diff_paths.py: "), detail
    if "stdout" in case:
        assert res.stdout == case["stdout"], detail
    if "expect" in case:
        prefix = ": error: forbidden-path: "
        got = [line.replace(prefix, " -> ", 1) for line in res.stdout.splitlines()[:-1]]
        assert got == case["expect"], detail
