#!/usr/bin/env python3
"""CI wrapper for the two skill checks: restated or contradicted rules (skill_rules.py) in the skill,
template, and preference files a change touched, and skill routing (skill_overlap.py).

  python3 scripts/style/skill_checks.py --base REF [--html PATH] [--summary] [--report-url URL]

Jev answers replay from the committed routing recordings first; anything not recorded (a changed
section, description, or request) goes live with TYPESAFE_API_KEY. Without a key, a missing recording
fails the check. Only the sections that contain a changed line are judged. Exits 1 on a problem, 3 if Jev is unavailable.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev  # noqa: E402
import skill_overlap  # noqa: E402
import skill_rules  # noqa: E402

ROOT = skill_rules.ROOT
STATE = Path(tempfile.gettempdir()) / "skill-checks.json"


def changed(base: str) -> dict:
    """{file: changed line numbers} for skill, template, and preference files changed since base."""
    import re
    scope = {str(p.relative_to(ROOT)) for p in skill_rules.files()}
    out = {}
    for f in subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", base, "--"], capture_output=True, text=True).stdout.split():
        if f not in scope:
            continue
        diff = subprocess.run(["git", "-C", str(ROOT), "diff", "-U0", base, "--", f], capture_output=True, text=True).stdout
        lines = set()
        for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.M):
            start, count = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
            lines.update(range(start, start + max(count, 1)))
        out[f] = lines
    return out


def run(base: str) -> dict:
    if os.environ.get("TYPESAFE_API_KEY") and not os.environ.get("JEV_RECORD"):
        os.environ["JEV_RECORD"] = tempfile.mkdtemp(prefix="jev-skills-")
    os.environ.setdefault("JEV_REPLAY", str(skill_overlap.FIXTURES))
    registry = yaml.safe_load(skill_rules.REGISTRY.read_text()) or []
    files = changed(base)
    rules = (skill_rules.scan([ROOT / f for f in files], registry, lines=files) if files
             else {"findings": [], "problems": [], "sections": 0})
    try:
        routing = skill_overlap.check(yaml.safe_load(skill_overlap.REQUESTS.read_text()), skill_overlap.skills())
    except ValueError as e:
        routing = {"rows": [], "pairs": [], "skills": 0, "problems": [str(e)]}
    return {"base": base, "files": sorted(files), "rules": rules, "routing": routing}


def summary(res: dict, report_url: str | None) -> str:
    probs = res["rules"]["problems"] + res["routing"]["problems"]
    lines = [f"## Skill checks: {'❌ ' + str(len(probs)) + ' problems' if probs else '✅ passed'}", ""]
    if report_url:
        lines += [f"**[Open the full HTML report]({report_url})** (opens in the browser; you need to be signed in to GitHub)", ""]
    lines += [f"- Rules restated or contradicted: {len(res['files'])} changed files, {res['rules']['sections']} sections, "
              f"{len(res['rules']['problems'])} problems",
              f"- Skill routing: {len(res['routing']['rows'])} requests, {len(res['routing']['problems'])} problems"]
    if probs:
        lines += ["", *[f"- {p}" for p in probs]]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="origin/v0")
    ap.add_argument("--html")
    ap.add_argument("--summary", action="store_true", help="print the summary of the last run (needs a prior run)")
    ap.add_argument("--report-url")
    a = ap.parse_args(argv)
    if a.summary:
        print(summary(json.loads(STATE.read_text()), a.report_url))
        return 0
    try:
        res = run(a.base)
    except jev.JevUnavailable as e:
        print(f"skill_checks: Jev unavailable: {e}", file=sys.stderr)
        return 3
    STATE.write_text(json.dumps(res, default=list))
    probs = res["rules"]["problems"] + res["routing"]["problems"]
    for p in probs:
        print(p)
    if a.html:
        import report_html as h
        h.write(Path(a.html), h.page("Skill checks", f"Skill, template, and preference changes since {a.base}",
                                     [skill_rules.html_section(res["rules"]), skill_overlap.html_section(res["routing"])],
                                     ("fail", f"{len(probs)} problems") if probs else ("pass", "No problems")))
    print(f"{len(res['files'])} changed files, {len(probs)} problems")
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main())
