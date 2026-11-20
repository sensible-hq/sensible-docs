#!/usr/bin/env python3
"""Run Vale on each rule fixture and check that every line marked fail or pass behaves as marked.

  python3 scripts/style/test_rules.py [fixture ...]

A fixture is a Markdown file in style-rules/tests/. Its first comment names the rules under test:

  <!-- rules: Sensible.EmDash -->

Then each line to check ends with a marker (in YAML frontmatter, use a trailing `# fail` or `# pass`):

  Configure portfolio mode — Sensible segments the file. <!-- fail -->
  Configure portfolio mode. Sensible segments the file. <!-- pass -->

A fail line must get at least one alert from a rule under test; a pass line must get none. Alerts from
other rules are ignored. Exits 1 if any fixture fails.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "style-rules/tests"
RULES = re.compile(r"<!--\s*rules:\s*(.*?)\s*-->")
MARK = re.compile(r"(?:<!--\s*(fail|pass)\s*-->|\s#\s*(fail|pass))\s*$")


def vale():
    for cand in ("vale", str(Path.home() / ".local/bin/vale")):
        if subprocess.run(["which", cand], capture_output=True).returncode == 0 or Path(cand).is_file():
            return cand
    sys.exit("test_rules: Vale isn't installed")


def check(path: Path, exe: str) -> list[str]:
    """Problems found in one fixture, as messages."""
    text = path.read_text()
    m = RULES.search(text)
    if not m:
        return [f"{path.name}: no <!-- rules: ... --> comment"]
    rules = {r.strip() for r in m.group(1).split(",") if r.strip()}
    out = subprocess.run([exe, "--config", str(ROOT / ".vale.ini"), "--output=JSON",
                          "--minAlertLevel=suggestion", str(path.relative_to(ROOT))],
                         cwd=ROOT, capture_output=True, text=True)
    if out.stderr.strip():
        return [f"{path.name}: Vale error: {out.stderr.strip()[:300]}"]
    try:
        results = json.loads(out.stdout or "{}")
    except json.JSONDecodeError:
        return [f"{path.name}: Vale failed: {(out.stderr or out.stdout).strip()[:300]}"]
    hits = {}
    for alerts in results.values():
        for a in alerts:
            if a["Check"] in rules:
                hits.setdefault(a["Line"], []).append(a["Check"])
    problems, marked = [], 0
    for n, line in enumerate(text.splitlines(), 1):
        mark = MARK.search(line)
        if not mark:
            continue
        marked += 1
        got = hits.get(n, [])
        kind = mark.group(1) or mark.group(2)
        if kind == "fail" and not got:
            problems.append(f"{path.name}:{n}: expected an alert, got none: {line.strip()[:90]}")
        if kind == "pass" and got:
            problems.append(f"{path.name}:{n}: expected no alert, got {', '.join(got)}: {line.strip()[:90]}")
    if not marked:
        problems.append(f"{path.name}: no lines marked fail or pass")
    return problems


def main(argv):
    exe = vale()
    files = [Path(a).resolve() for a in argv] or sorted(TESTS.glob("*.md"))
    problems = [p for f in files for p in check(f, exe)]
    for p in problems:
        print(p)
    print(f"{len(files)} fixtures, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
