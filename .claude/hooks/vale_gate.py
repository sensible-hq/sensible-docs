#!/usr/bin/env python3
"""Write-time style hook for docs pages: Vale and the code-block check, on the lines an edit changes.

Wired in .claude/settings.json for two events on Edit, Write, and MultiEdit. Check it with
scripts/vale-doctor.sh.

  PreToolUse   Rebuilds the page as it would be after the edit, lints it, and denies the edit when a
               changed line breaks a rule whose registry gate is "block" (style-rules/registry.yaml).
               The reason names each rule and its fix, so Claude rewrites before anything is written.
               After 3 denials for the same file in a session, the edit goes through and the alerts
               are passed on as context instead, so a false positive can't stall the work.
  PostToolUse  Reports warnings and errors on the lines changed since the last commit (all lines for a
               new file) and hands them back to Claude with exit 2. Alerts on lines nobody touched
               are left out, so Claude doesn't rewrite text outside its change.

Scope: Markdown under docs/ at the root of the file's checkout. reference/**/*.md is generated from the
OpenAPI specs and is skipped. If Vale isn't installed, the hook exits 1 (shown to you, not Claude).
"""
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD_LIMIT = 3


def repo_root(path: Path) -> Path | None:
    out = subprocess.run(["git", "-C", str(path.parent), "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True)
    return Path(out.stdout.strip()) if out.returncode == 0 else None


def vale_exe() -> str | None:
    for cand in ("vale", str(Path.home() / ".local/bin/vale")):
        found = subprocess.run(["sh", "-c", f'command -v "{cand}"'], capture_output=True, text=True).stdout.strip()
        if found:
            return found
        if Path(cand).is_file():
            return cand
    return None


def gates(root: Path) -> tuple[dict, dict]:
    """Vale check name → gate, and rule id → gate, from the registry."""
    import yaml
    by_check, by_id = {}, {}
    reg = root / "style-rules/registry.yaml"
    for r in (yaml.safe_load(reg.read_text()) if reg.is_file() else None) or []:
        gate = r.get("gate", "report")
        by_id[r.get("id")] = gate
        for name in (r.get("enforced_by") or {}).get("vale") or []:
            by_check[name] = gate
    return by_check, by_id


def lint(root: Path, text: str, name: str, level: str) -> list[dict]:
    """Vale alerts and code-block problems for text that would live at docs/.../name."""
    exe = vale_exe()
    if not exe:
        print(f"vale_gate: Vale isn't installed or on PATH; skipping lint of {name}", file=sys.stderr)
        sys.exit(1)
    alerts = []
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / name
        page.write_text(text)
        out = subprocess.run([exe, "--config", str(root / ".vale.ini"), "--output=JSON",
                              f"--minAlertLevel={level}", str(page)], capture_output=True, text=True)
        try:
            for items in json.loads(out.stdout or "{}").values():
                alerts += [{"line": a["Line"], "check": a["Check"], "level": a["Severity"],
                            "message": a["Message"]} for a in items]
        except json.JSONDecodeError:
            pass
        sys.path.insert(0, str(root / "scripts/style"))
        try:
            import check_code_blocks
            for p in check_code_blocks.check(page):
                m = re.match(r".*?:(\d+): (.*)", p)
                if m:
                    alerts.append({"line": int(m.group(1)), "check": "sensible-code-fences",
                                   "level": "error", "message": m.group(2)})
        except ImportError:
            pass
    return alerts


def changed_lines(old: str, new: str) -> set[int]:
    """1-based line numbers in new that an edit from old inserted or replaced."""
    lines = set()
    sm = difflib.SequenceMatcher(None, old.splitlines(), new.splitlines(), autojunk=False)
    for tag, _, _, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "insert"):
            lines.update(range(j1 + 1, j2 + 1))
    return lines


def apply_edit(tool: str, inp: dict, current: str) -> str | None:
    """The file as it would be after the tool call, or None if the edit wouldn't apply."""
    if tool == "Write":
        return inp.get("content", "")
    edits = inp.get("edits") if tool == "MultiEdit" else [inp]
    text = current
    for e in edits or []:
        old, new = e.get("old_string", ""), e.get("new_string", "")
        if old not in text:
            return None
        text = text.replace(old, new) if e.get("replace_all") else text.replace(old, new, 1)
    return text


def guard(session: str, path: Path, reset: bool = False) -> int:
    """Denials so far for this file in this session; increments unless reset."""
    state = Path(tempfile.gettempdir()) / f"vale-gate-{re.sub(r'[^A-Za-z0-9-]', '', session) or 'nosession'}.json"
    try:
        data = json.loads(state.read_text())
    except (OSError, json.JSONDecodeError):
        data = {}
    key = str(path)
    data[key] = 0 if reset else data.get(key, 0) + 1
    state.write_text(json.dumps(data))
    return data[key]


def describe(alerts: list[dict]) -> str:
    return "\n".join(f"  line {a['line']}: {a['check']}: {a['message']}" for a in sorted(alerts, key=lambda a: a["line"]))


def pre(event: dict, root: Path, path: Path) -> int:
    current = path.read_text() if path.is_file() else ""
    new = apply_edit(event.get("tool_name", ""), event.get("tool_input") or {}, current)
    if new is None:
        return 0  # the edit won't apply; let the tool report that
    touched = changed_lines(current, new)
    by_check, by_id = gates(root)
    blocking = [a for a in lint(root, new, path.name, "warning")
                if a["line"] in touched and (by_check.get(a["check"]) or by_id.get(a["check"])) == "block"]
    session = event.get("session_id", "")
    if not blocking:
        guard(session, path, reset=True)
        return 0
    if guard(session, path) > GUARD_LIMIT:
        guard(session, path, reset=True)
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext":
               f"vale_gate let this edit through after {GUARD_LIMIT} denials. These blocking alerts remain; "
               f"fix them, or say why each is a false positive:\n{describe(blocking)}"}}
    else:
        out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
               "permissionDecisionReason":
               f"The edit adds text that breaks a house style rule. Rewrite these lines and try again, "
               f"keeping the meaning:\n{describe(blocking)}\nRules and fixes: style-rules/registry.yaml."}}
    print(json.dumps(out))
    return 0


def post(root: Path, path: Path) -> int:
    if not path.is_file():
        return 0
    text = path.read_text()
    rel = str(path.relative_to(root))
    tracked = subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"HEAD:{rel}"], capture_output=True).returncode == 0
    base = subprocess.run(["git", "-C", str(root), "show", f"HEAD:{rel}"], capture_output=True,
                          text=True).stdout if tracked else ""
    touched = changed_lines(base, text)
    alerts = [a for a in lint(root, text, path.name, "warning") if a["line"] in touched]
    if not alerts:
        return 0
    print(f"Vale flagged {len(alerts)} warnings or errors on lines you changed in {path}. Fix them, keeping "
          f"the meaning.\nIf one is a false positive, such as a product term, code, or a quote, leave the "
          f"text and say why.\n\n{describe(alerts)}", file=sys.stderr)
    return 2


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    file = (event.get("tool_input") or {}).get("file_path") or ""
    if not file.endswith((".md", ".mdx")):
        return 0
    path = Path(file).resolve()
    root = repo_root(path) if path.parent.exists() else None
    if not root:
        return 0
    rel = os.path.relpath(path, root)
    if not rel.startswith("docs" + os.sep):
        return 0  # reference/**/*.md is generated from the OpenAPI JSON specs
    if event.get("hook_event_name") == "PreToolUse":
        return pre(event, root, path)
    return post(root, path)


if __name__ == "__main__":
    sys.exit(main())
