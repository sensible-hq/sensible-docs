#!/usr/bin/env python3
"""Lint only the lines an agent added, with the agent-only Vale rules.

The agent-only rules are listed under `agent_only_rules:` in registry.yaml and
turned off in .vale.ini, so normal Vale runs never flag them. This script runs
them on the lines added or changed since --base. The spec is in README.md
("Agent-only rules"); test/tests/test_agent_lines.py is its acceptance test.

Usage: agent_lines.py --base REF [--root DIR] [--vale PATH] [FILE ...]
Exit code: 0 no alerts, 1 alerts, 2 couldn't run.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

STYLES_REL = ".github/styles"
REGISTRY_REL = "scripts/style_sync/registry.yaml"
DOC_DIRS = ("docs/", "reference/")
EXTENSIONS = (".md", ".mdx")
HUNK_RE = re.compile(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@")


class RunError(Exception):
    pass


def git(root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise RunError("git not found") from exc
    if proc.returncode != 0:
        raise RunError(f"git {' '.join(args)} failed: {proc.stderr.strip()[:300]}")
    return proc.stdout


def find_root(start: Path) -> Path:
    try:
        return Path(git(start, "rev-parse", "--show-toplevel").strip()).resolve()
    except RunError as exc:
        raise RunError(f"not in a git repository: {start}") from exc


def find_vale(given: str | None) -> str:
    candidates = [given] if given else [shutil.which("vale"), str(Path.home() / ".local/bin/vale")]
    for c in candidates:
        if c and Path(c).is_file() and os.access(c, os.X_OK):
            return c
    raise RunError(f"Vale isn't installed{' at ' + given if given else ' or on PATH'}")


def agent_only_rules(root: Path) -> list[str]:
    path = root / REGISTRY_REL
    try:
        reg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise RunError(f"cannot read {REGISTRY_REL}: {exc}") from exc
    rules = reg.get("agent_only_rules") if isinstance(reg, dict) else None
    if not isinstance(rules, list) or not all(isinstance(r, str) for r in rules):
        raise RunError(f"{REGISTRY_REL}: agent_only_rules must be a list of rule names")
    return rules


def added_lines(root: Path, base: str, rel: str) -> set[int] | None:
    """Line numbers in the working-tree file that are added or changed since base.
    None means every line (the file doesn't exist at base)."""
    exists = subprocess.run(["git", "cat-file", "-e", f"{base}:{rel}"], cwd=root,
                            capture_output=True).returncode == 0
    if not exists:
        return None
    diff = git(root, "diff", "--no-color", "--no-ext-diff", "--unified=0", base, "--", rel)
    lines: set[int] = set()
    for ln in diff.splitlines():
        m = HUNK_RE.match(ln)
        if m:
            start, count = int(m.group(1)), int(m.group(2) or 1)
            lines.update(range(start, start + count))
    return lines


def changed_docs(root: Path, base: str) -> list[str]:
    changed = git(root, "diff", "--name-only", "--no-renames", base, "--").splitlines()
    untracked = git(root, "ls-files", "--others", "--exclude-standard").splitlines()
    return sorted({p for p in changed + untracked
                   if p.startswith(DOC_DIRS) and p.endswith(EXTENSIONS) and (root / p).is_file()})


def run_vale(vale: str, root: Path, rules: list[str], files: list[Path]) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        ini = Path(tmp) / "vale.ini"
        lines = [f"StylesPath = {(root / STYLES_REL).as_posix()}", "MinAlertLevel = suggestion", "",
                 "[*.{md,mdx}]", "BasedOnStyles ="]
        lines += [f"{r} = YES" for r in rules]
        ini.write_text("\n".join(lines) + "\n", encoding="utf-8")
        cmd = [vale, "--no-global", "--no-exit", f"--config={ini}", "--output=JSON", *map(str, files)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=root, timeout=300)
        except OSError as exc:
            raise RunError(f"cannot run Vale: {exc}") from exc
    try:
        data = json.loads(proc.stdout or "{}")
    except json.JSONDecodeError as exc:
        raise RunError(f"Vale failed (exit {proc.returncode}): {(proc.stderr or proc.stdout).strip()[:300]}") from exc
    if not isinstance(data, dict):
        raise RunError(f"Vale failed: {str(data)[:300]}")
    return {str(Path(p) if Path(p).is_absolute() else (root / p).resolve()): a for p, a in data.items()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--base", required=True, help="git revision; lines added or changed since it are checked")
    ap.add_argument("--root", type=Path, help="repository root (default: git top level of the current directory)")
    ap.add_argument("--vale", help="path to the vale binary (default: vale on PATH, then ~/.local/bin/vale)")
    ap.add_argument("files", nargs="*", help="files to check (default: changed docs/ and reference/ pages)")
    args = ap.parse_args(argv)

    try:
        root = find_root(args.root or Path.cwd())
        vale = find_vale(args.vale)
        rules = agent_only_rules(root)
        git(root, "rev-parse", "--verify", "--quiet", f"{args.base}^{{commit}}")

        # (label printed, absolute path, repo-relative path)
        targets = []
        if args.files:
            for given in args.files:
                p = Path(given)
                p = (p if p.is_absolute() else Path.cwd() / p).resolve()
                if not p.is_file() or not p.name.endswith(EXTENSIONS) or not p.is_relative_to(root):
                    continue
                targets.append((given, p, p.relative_to(root).as_posix()))
        else:
            targets = [(rel, (root / rel).resolve(), rel) for rel in changed_docs(root, args.base)]

        wanted = {}
        for label, path, rel in targets:
            lines = added_lines(root, args.base, rel)
            if lines is None or lines:
                wanted[str(path)] = (label, lines)
        if not wanted or not rules:
            return 0
        results = run_vale(vale, root, rules, [Path(p) for p in wanted])
    except RunError as exc:
        print(f"agent_lines: {exc}", file=sys.stderr)
        return 2

    alerts = []
    for path, (label, lines) in wanted.items():
        for a in results.get(path, []):
            line = a.get("Line")
            if lines is None or line in lines:
                col = (a.get("Span") or [1])[0]
                alerts.append((label, line, col, a.get("Check", ""), a.get("Message", "")))
    for label, line, col, check, msg in sorted(alerts):
        print(f"{label}:{line}:{col}:{check}:{msg}")
    return 1 if alerts else 0


if __name__ == "__main__":
    sys.exit(main())
