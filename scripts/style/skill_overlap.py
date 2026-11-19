#!/usr/bin/env python3
"""Do the repo's skill descriptions route requests to the right skill, one at a time?

  python3 scripts/style/skill_overlap.py [--html PATH] [--json PATH]

For each request in style-rules/skill-requests.yaml, Jev reads the request and answers one Noul per
repo skill (.claude/skills/*/SKILL.md): would this skill's description make an assistant pick it for
this request? One request to Jev per user request, with every skill's question bundled.

Code decides:
  collision  the runner-up skill also scores >= 0.50, within 0.20 of the top one (a near match further
             behind is listed as close, not a problem)
  miss       the expected skill isn't the top score, or scores < 0.50
  stray      a request that expects no skill gets a skill >= 0.50

Every collision, miss, and stray is a problem. Responses are recorded (scripts/style/test/fixtures/
jev-skill-overlap), so CI replays them; a changed description or request needs TYPESAFE_API_KEY (CI
has it) to fetch only what changed. Exits 1 on a problem, 3 if Jev is unavailable.
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
REQUESTS = ROOT / "style-rules/skill-requests.yaml"
FIXTURES = Path(__file__).resolve().parent / "test/fixtures/jev-skill-overlap"
HIGH = 0.50
GAP = 0.20  # a runner-up within this of the top skill, and itself a match, is a collision


def skills() -> dict:
    """name -> description, from each repo skill's frontmatter. A frontmatter that doesn't parse is an error."""
    out = {}
    for p in sorted(ROOT.glob(".claude/skills/*/SKILL.md")):
        m = re.match(r"---\n(.*?)\n---", p.read_text(), re.S)
        if not m:
            raise ValueError(f"{p.relative_to(ROOT)}: no frontmatter")
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"{p.relative_to(ROOT)}: frontmatter isn't valid YAML ({str(e).splitlines()[0]})") from None
        out[meta.get("name") or p.parent.name] = str(meta.get("description") or "")
    return out


def question(name: str, description: str) -> dict:
    return {"type": "noul", "instructions": f"Would an assistant that reads this skill description pick the skill "
                                            f"\"{name}\" to handle `request`? Description: {description}"}


def check(requests: list[dict], descs: dict) -> dict:
    qs = {judge.key(n): question(n, d) for n, d in descs.items()}
    rows, problems = [], []
    for r in requests:
        resp = jev.call({"request": r["request"], "context": "A request typed to a coding assistant working in the sensible-docs repo."}, qs)
        scores = {n: ((resp.get("answers") or {}).get(judge.key(n)) or {}).get("noul", 0) for n in descs}
        ranked = sorted(scores.items(), key=lambda x: -x[1])
        high = [n for n, s in ranked if s >= HIGH]
        expect = r.get("expect")
        kinds = []
        if len(ranked) > 1 and ranked[1][1] >= HIGH and ranked[0][1] - ranked[1][1] < GAP:
            kinds.append("collision")
        elif len(high) >= 2:
            kinds.append("close")
        if expect and expect != "none" and (ranked[0][0] != expect or scores.get(expect, 0) < HIGH):
            kinds.append("miss")
        if expect == "none" and high:
            kinds.append("stray")
        rows.append({"request": r["request"], "expect": expect, "top": ranked[:3], "high": high, "kinds": kinds})
        for k in kinds:
            if k == "close":
                continue
            problems.append(f"{k}: {r['request']!r} expects {expect}; " + ", ".join(f"{n} {s:.2f}" for n, s in ranked[:3]))
    pairs = {}
    for row in rows:
        for i, a in enumerate(row["high"]):
            for b in row["high"][i + 1:]:
                pairs[tuple(sorted((a, b)))] = pairs.get(tuple(sorted((a, b))), 0) + 1
    return {"rows": rows, "problems": problems, "pairs": sorted(pairs.items(), key=lambda x: -x[1]), "skills": len(descs)}


def html_section(res: dict) -> str:
    import report_html as h
    rows = [[h.e(r["request"]), f"<code>{h.e(r['expect'])}</code>",
             "<br>".join(f"<code>{h.e(n)}</code> {s:.2f}" for n, s in r["top"]),
             " ".join(h.chip("warn" if k == "close" else "fail", k) for k in r["kinds"]) or h.chip("pass", "ok")]
            for r in sorted(res["rows"], key=lambda r: (not [k for k in r["kinds"] if k != "close"], not r["kinds"], r["expect"] or ""))]
    pairs = h.table(["Skills", "Requests both score high on"], [[f"<code>{h.e(a)}</code> / <code>{h.e(b)}</code>", str(n)] for (a, b), n in res["pairs"]]) \
        if res["pairs"] else "<p>No two skills score high on the same request.</p>"
    return h.card("Skill routing", f"<h3>Colliding skills</h3>{pairs}<h3>Requests ({len(rows)})</h3>"
                  + h.table(["Request", "Expected", "Top scores", "Result"], rows),
                  f"{res['skills']} repo skills, each scored on every request in style-rules/skill-requests.yaml. A score of {HIGH} or more is a match.",
                  open_=True, badge=h.JUDGE)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    try:
        res = check(yaml.safe_load(REQUESTS.read_text()), skills())
    except ValueError as e:
        print(f"skill_overlap: {e}")
        return 1
    except jev.JevUnavailable as e:
        print(f"skill_overlap: Jev unavailable: {e}", file=sys.stderr)
        return 3
    for p in res["problems"]:
        print(p)
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=1))
    if a.html:
        import report_html as h
        h.write(Path(a.html), h.page("Skill routing", "Which repo skill each realistic request reaches",
                                     [html_section(res)], ("fail", f"{len(res['problems'])} problems") if res["problems"] else ("pass", "No problems")))
    print(f"{len(res['rows'])} requests, {res['skills']} skills, {len(res['problems'])} problems")
    return 1 if res["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
