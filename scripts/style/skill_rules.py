#!/usr/bin/env python3
"""Do the repo's skills, templates, and preferences restate or contradict a registered style rule?

  python3 scripts/style/skill_rules.py [--files PATH,...] [--html PATH] [--json PATH]

Each section (the text under one heading, code blocks removed) of each file in SCAN is sent to Jev
once, with one choice question per registered rule:

  restates     it tells the writer to do what the rule says, in its own words
  contradicts  it tells the writer to do something the rule forbids, or allows what the rule bans
  unrelated    it gives no instruction about what the rule covers, or only points to the guide

Code decides:
  - contradicts with probability >= 0.70 is a problem; from 0.50 it's listed for review.
  - restates with probability >= 0.70 is a problem unless the section carries the rule's marker
    (<!-- rule: id -->, which check_registry.py then requires a stated_in entry for).
  - An entry in style-rules/skill-exceptions.yaml (file, heading, rule, reason) clears either.

A restatement should usually become a pointer to the guide ("follow writing-rules.md"); a skill that
needs its own wording keeps it and gets the marker, so the registry knows it's another carrier.

Needs TYPESAFE_API_KEY (about $0.0007 a section). Recordings aren't committed: any change to a rule
statement changes every request (decisions RO-025). JEV_REPLAY plus JEV_RECORD reuses a local cache.
Exits 1 on a problem, 3 if Jev is unavailable.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev  # noqa: E402
import judge  # noqa: E402

ROOT = judge.ROOT
REGISTRY = ROOT / "style-rules/registry.yaml"
EXCEPTIONS = ROOT / "style-rules/skill-exceptions.yaml"
SCAN = [".claude/skills/*/*.md", ".claude/skills/*/references/*.md", ".claude/style-guide/*template*.md",
        ".claude/preferences/*.md"]
RESTATES, CONTRADICTS, REVIEW = 0.70, 0.70, 0.50
MAX_SECTION = 3000
FENCE = re.compile(r"(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$")
MARKER = re.compile(r"<!--\s*rule:\s*([a-z0-9-]+)\s*-->")
CRITERIA = {
    "restates": "it tells the agent to write docs the way the rule says, in its own words (a pointer to a guide without the rule's content doesn't count)",
    "contradicts": "it tells the agent to write docs in a way the rule forbids, or allows in docs what the rule bans",
    "unrelated": "it gives no instruction about what the rule covers, only points to the guide, or the rule doesn't apply to what it asks the agent to write",
}


def files(only: list[str] | None = None) -> list[Path]:
    if only:
        return [ROOT / f for f in only]
    return sorted({p for g in SCAN for p in ROOT.glob(g)})


def sections(path: Path) -> list[dict]:
    """(heading, line, text) for each heading's section, code blocks removed, long ones split."""
    # Blank out code blocks line by line, so line numbers still match the file
    text = FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), path.read_text())
    out, heading, start, buf = [], "(top)", 1, []
    lines = text.splitlines()

    def flush(end):
        body = "\n".join(buf).strip()
        if len(re.sub(r"\W", "", body)) > 40:
            for k in range(0, len(body), MAX_SECTION):
                out.append({"heading": heading, "line": start, "end": end, "text": body[k:k + MAX_SECTION],
                            "markers": set(MARKER.findall(body))})

    for n, line in enumerate(lines, 1):
        m = re.match(r"^#{1,6}\s+(.*)", line)
        if m:
            flush(n - 1)
            heading, start, buf = m.group(1).strip(), n, []
        else:
            buf.append(line)
    flush(len(lines))
    return out


def rule_question(rule: dict) -> dict:
    ask = (f"How do the instructions in `section` treat the house style rule {rule['id']}: \"{rule['statement']}\""
           + (f" (applies to {rule['applies_to']})" if rule.get("applies_to") else "")
           + "? Judge what the section tells the agent to write, not how the section itself is written.")
    return jev.choice_question(ask, CRITERIA)


def load_exceptions() -> list[dict]:
    return (yaml.safe_load(EXCEPTIONS.read_text()) or []) if EXCEPTIONS.is_file() else []


def scan(paths: list[Path], registry: list[dict], only: set | None = None, lines: dict | None = None) -> dict:
    """{findings: [...], problems: [...], sections: n}. only: judge just these rules (the new-rule gate).
    lines: {relative path: changed line numbers}; judge only the sections that contain one."""
    rules = [r for r in registry if r.get("statement") and (not only or r["id"] in only)]
    questions = {judge.key(r["id"]): rule_question(r) for r in rules}
    exceptions = {(x["file"], x["heading"], x["rule"]) for x in load_exceptions()}
    findings, problems, n = [], [], 0
    for path in paths:
        rel = str(path.relative_to(ROOT))
        for sec in sections(path):
            if lines is not None and not any(sec["line"] <= k <= sec["end"] for k in lines.get(rel, ())):
                continue
            n += 1
            state = {"file": rel, "heading": sec["heading"], "section": sec["text"],
                     "context": "A section of a skill, template, or preference file: instructions for an agent that writes Sensible's docs pages, blog posts, changelogs, or API specs. The style rules apply to docs pages unless they name another page type."}
            resp = jev.call(state, questions)
            marked = sec["markers"]  # a marker anywhere in the section covers each part of a long one
            for r in rules:
                ans = (resp.get("answers") or {}).get(judge.key(r["id"])) or {}
                p = ans.get("probabilities") or {}
                kind = ("contradicts" if p.get("contradicts", 0) >= REVIEW else
                        "restates" if p.get("restates", 0) >= RESTATES else None)
                if not kind:
                    continue
                excepted = (rel, sec["heading"], r["id"]) in exceptions
                review = kind == "contradicts" and p.get("contradicts", 0) < CONTRADICTS
                ok = excepted or review or (kind == "restates" and r["id"] in marked)
                f = {"file": rel, "line": sec["line"], "heading": sec["heading"], "rule": r["id"], "kind": kind,
                     "p": p.get(kind, 0), "marked": r["id"] in marked, "excepted": excepted, "review": review, "ok": ok}
                findings.append(f)
                if not ok:
                    fix = ("change the section or the rule, or record why in style-rules/skill-exceptions.yaml" if kind == "contradicts"
                           else f"point to the guide instead, or add <!-- rule: {r['id']} --> and a stated_in entry")
                    problems.append(f"{rel}:{sec['line']} ({sec['heading']}): {kind} {r['id']} (p {p.get(kind, 0):.2f}); {fix}")
    return {"findings": findings, "problems": problems, "sections": n}


def html_section(res: dict) -> str:
    import report_html as h
    rows = [[h.e(f"{f['file']}:{f['line']}"), h.e(f["heading"]), f"<code>{h.e(f['rule'])}</code>",
             h.chip("fail" if f["kind"] == "contradicts" and not f["ok"] else ("warn" if not f["ok"] else "pass"), f["kind"]),
             f"{f['p']:.2f}", "marker" if f["marked"] else ("exception" if f["excepted"] else ("below 0.70: review" if f.get("review") else ""))]
            for f in sorted(res["findings"], key=lambda f: (f["ok"], f["kind"] != "contradicts", f["file"], f["line"]))]
    body = (h.table(["Problem"], [[h.e(p)] for p in res["problems"]]) if res["problems"]
            else "<p>No skill restates a rule without its marker, and none contradicts one.</p>")
    body += f"<h3>Every section Jev tied to a rule ({len(rows)})</h3>" + (
        h.table(["Where", "Section", "Rule", "Kind", "p", "Cleared by"], rows) if rows else "<p>None.</p>")
    return h.card("Skills and registered rules", body,
                  f"{res['sections']} sections of skills, templates, and preferences, each judged against every registered rule.",
                  open_=bool(res["problems"]), badge=h.JUDGE)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--files")
    ap.add_argument("--rules", help="judge only these rules")
    ap.add_argument("--changed-since", help="scan only the files that changed since this git ref")
    ap.add_argument("--html")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    registry = yaml.safe_load(REGISTRY.read_text()) or []
    try:
        only = a.files.split(",") if a.files else None
        if a.changed_since:
            import subprocess
            changed = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", a.changed_since, "--"],
                                     capture_output=True, text=True).stdout.split()
            scope = {str(p.relative_to(ROOT)) for p in files()}
            only = [f for f in changed if f in scope]
            if not only:
                print(f"no skill, template, or preference file changed since {a.changed_since}")
                return 0
        res = scan(files(only), registry, set(a.rules.split(",")) if a.rules else None)
    except jev.JevUnavailable as e:
        print(f"skill_rules: Jev unavailable: {e}", file=sys.stderr)
        return 3
    for p in res["problems"]:
        print(p)
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=1))
    if a.html:
        import report_html as h
        h.write(Path(a.html), h.page("Skills and style rules", "Skills, templates, and preferences against the registered rules",
                                     [html_section(res)], ("fail", f"{len(res['problems'])} problems") if res["problems"] else ("pass", "No problems")))
    print(f"{res['sections']} sections, {len(res['findings'])} tied to a rule, {len(res['problems'])} problems")
    return 1 if res["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
