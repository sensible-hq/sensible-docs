#!/usr/bin/env python3
"""Claude Code PostToolUse hook: after an edit to a file that states or enforces a style rule, check
that the registry still agrees with it and that the change didn't create a duplicate or a conflict.

Carriers: CLAUDE.md, AGENTS.md, .claude/style-guide/, .claude/preferences/, .claude/skills/,
style-rules/, and .github/styles/. Session files under .claude/sessions/ are skipped.

Runs, in the edited file's own checkout:
  scripts/style/check_registry.py   every problem (the registry is clean on v0, so any problem is new)
  scripts/style/check_overlap.py    deterministic layers only, limited to pairs that include a rule this
                                    file states or enforces, or a rule whose registry entry changed

Exits 2 with the problems on stderr, which Claude Code shows to the model; exits 0 otherwise. It never
blocks an edit: changing a rule takes edits to several files, and the check can only agree after the
last of them.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

CARRIERS = ("CLAUDE.md", "AGENTS.md", ".claude/style-guide/", ".claude/preferences/", ".claude/skills/",
            "style-rules/", ".github/styles/")


def repo_root(path: Path) -> Path | None:
    out = subprocess.run(["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else None


def touched_rules(root: Path, rel: str) -> set[str]:
    """Rules the edited file states, enforces, or tests, plus rules whose registry entry changed."""
    import yaml
    reg_path = root / "style-rules/registry.yaml"
    try:
        rules = yaml.safe_load(reg_path.read_text()) or []
    except (OSError, yaml.YAMLError):
        return set()
    ids = set()
    for r in rules:
        enf = r.get("enforced_by") or {}
        files = [s.get("file") for s in r.get("stated_in") or []] + [r.get("fixture")]
        files += list(enf.get("script") or []) + list(enf.get("judgment") or [])
        files += [f".github/styles/{v.replace('.', '/', 1)}.yml" for v in enf.get("vale") or []]
        if rel in files:
            ids.add(r["id"])
    if rel == "style-rules/registry.yaml":
        old = subprocess.run(["git", "-C", str(root), "show", "HEAD:style-rules/registry.yaml"],
                             capture_output=True, text=True)
        before = {r["id"]: r for r in (yaml.safe_load(old.stdout) or [])} if old.returncode == 0 else {}
        ids |= {r["id"] for r in rules if before.get(r["id"]) != r}
    return ids


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    file = (event.get("tool_input") or {}).get("file_path") or ""
    if not file:
        return 0
    path = Path(file).resolve()
    root = repo_root(path) if path.parent.exists() else None
    if not root or not (root / "scripts/style/check_registry.py").exists():
        return 0
    rel = os.path.relpath(path, root)
    if "/sessions/" in rel or not (rel in CARRIERS or rel.startswith(CARRIERS[2:])):
        return 0

    parts = []
    reg = subprocess.run([sys.executable, "scripts/style/check_registry.py"], cwd=root, capture_output=True, text=True)
    if reg.returncode:
        parts.append("The style rule registry no longer agrees with the files that state or enforce its rules. "
                     "Fix the guide, the check, or style-rules/registry.yaml so they match:\n" + reg.stdout.strip())
    ids = touched_rules(root, rel)
    if ids:
        args = ["--involving", ",".join(sorted(ids))]
        if not (rel.startswith(".github/styles/") or rel.startswith("style-rules/tests/")):
            args.append("--no-fixtures")
        ov = subprocess.run([sys.executable, "scripts/style/check_overlap.py", *args], cwd=root,
                            capture_output=True, text=True)
        if ov.returncode:
            parts.append("This change touches rules that may duplicate or conflict with other rules. Tell the user "
                         "which pairs, and settle each one with them: merge the rules, add `overrides` to the "
                         "winner, or record the pair in style-rules/overlaps.yaml:\n" + ov.stdout.strip())
    if not parts:
        return 0
    print("\n\n".join(parts), file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
