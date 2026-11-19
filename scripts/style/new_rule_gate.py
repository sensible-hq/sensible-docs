#!/usr/bin/env python3
"""Gate for new style rules: a rule added since the base branch must be registered, tested, labeled,
and checked against every other rule.

  python3 scripts/style/new_rule_gate.py [--base origin/v0] [--html PATH] [--summary]

A rule is new when its registry id isn't in the base branch's registry, or when it gained a Vale rule
or a judgment spec the base branch doesn't have. Each new rule must have:

  every rule      a clean registry entry (check_registry.py) with a scope, and a recorded relations
                  check against every other rule with no unresolved same-requirement or conflicting pair
                  (rule_hygiene.py relations; record with JEV_RECORD=scripts/style/test/fixtures/jev-relations)
  Vale            a fixture with at least one fail and one pass line, whose pass lines no other gating
                  rule flags (rule_hygiene.py crossfire)
  judgment        a label file with at least 6 cases and 3 violations, none copied from the spec; no
                  choice name another spec defines differently; no near-duplicate choices; a stored
                  calibration (calibrate.py --write)
  prose           at least one stated_in place with its marker
  and             no skill, template, or preference that restates it without its marker, or contradicts it
                  (skill_rules.py, one Jev request per section)

Jev answers come from recordings (JEV_REPLAY defaults to the committed fixtures), so CI needs no key.
Exits 1 if a new rule fails, 0 otherwise (including when there are no new rules).
"""
import argparse
import json
import os
import tempfile
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_registry  # noqa: E402
import jev  # noqa: E402
import judge  # noqa: E402
import rule_hygiene as rh  # noqa: E402

ROOT = judge.ROOT
MIN_CASES, MIN_VIOLATIONS = judge.MIN_CASES, judge.MIN_VIOLATIONS
HERE = Path(__file__).resolve().parent


def git(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def base_state(base: str) -> dict:
    """The base branch's registry ids, Sensible Vale rules, and judgment specs."""
    reg = git("show", f"{base}:style-rules/registry.yaml")
    if reg.returncode:
        raise SystemExit(f"new_rule_gate: can't read the registry at {base}: {reg.stderr.strip()}")
    files = git("ls-tree", "-r", "--name-only", base, "--", ".github/styles/Sensible", "style-rules/judgment").stdout.split()
    return {"ids": {r["id"] for r in yaml.safe_load(reg.stdout) or []},
            "vale": {f"Sensible.{Path(f).stem}" for f in files if f.startswith(".github/styles/Sensible/")},
            "specs": {f for f in files if f.startswith("style-rules/judgment/") and f.count("/") == 2}}


def new_rules(registry: list[dict], base: dict) -> list[dict]:
    out = []
    for r in registry:
        enf = r.get("enforced_by") or {}
        if (r["id"] not in base["ids"] or any(v.startswith("Sensible.") and v not in base["vale"] for v in enf.get("vale") or [])
                or any(s not in base["specs"] for s in enf.get("judgment") or [])):
            out.append(r)
    return out


def fixture_lines(path: Path) -> tuple[int, int]:
    import test_rules
    kinds = [m.group(1) or m.group(2) for m in (test_rules.MARK.search(l) for l in path.read_text().splitlines()) if m]
    return kinds.count("fail"), kinds.count("pass")


def check_rule(r: dict, registry: list[dict], specs: dict, labels: dict, registry_problems: list[str]) -> list[str]:
    rid, kind = r["id"], r.get("kind")
    enf = r.get("enforced_by") or {}
    problems = [p for p in registry_problems if p.startswith(f"{rid}:")]

    # Duplicates and contradictions, judged from the statements
    try:
        rel = rh.relations(registry, {rid})
        problems += [f"{rid}: {p}" for p in rel["problems"]]
    except jev.JevUnavailable as e:
        problems.append(f"{rid}: no recorded relations check ({e}); run TYPESAFE_API_KEY=… JEV_RECORD={rh.RELATIONS_FIXTURES.relative_to(ROOT)} "
                        f"python3 scripts/style/rule_hygiene.py relations --rules {rid}")

    if enf.get("vale"):
        fx = r.get("fixture")
        if not fx or not (ROOT / fx).is_file():
            problems.append(f"{rid}: a Vale rule needs a fixture in style-rules/tests/")
        else:
            fails, passes = fixture_lines(ROOT / fx)
            if not fails or not passes:
                problems.append(f"{rid}: fixture {fx} needs at least one fail line and one pass line ({fails} fail, {passes} pass)")
            problems += [f"{rid}: {p}" for p in rh.crossfire(registry, [ROOT / fx])["problems"]]

    if kind == "judgment":
        spec = specs.get(rid)
        cases = labels.get(rid) or []
        if spec and ((spec.get("check") or {}).get("find") or {}).get("kind") != "manual":
            bad = set((spec["check"].get("verdicts") or {}).get("violation") or [])
            n_bad = sum(c.get("expected") in bad for c in cases)
            if len(cases) < MIN_CASES or n_bad < MIN_VIOLATIONS:
                problems.append(f"{rid}: needs a label file with at least {MIN_CASES} cases and {MIN_VIOLATIONS} violations "
                                f"(style-rules/judgment/labels/{rid}.yaml has {len(cases)} cases, {n_bad} violations)")
            cat = rh.catalog(specs, labels)
            problems += [f"{rid}: labeled case copied from the spec, so it tests the spec's wording: {t[:80]!r}" for x, t in cat["copied"] if x == rid]
            mine = set(((spec.get("check") or {}).get("question") or {}).get("criteria") or {})
            problems += [f"{rid}: {p}" for p in cat["problems"] if any(f"choice {c!r}" in p for c in mine)]
            if cases:
                try:
                    problems += [p for p in rh.overlap({rid: spec}, {rid: cases})["problems"]]
                except jev.JevUnavailable as e:
                    problems.append(f"{rid}: no recorded calibration ({e}); run calibrate.py --rules {rid} --write with JEV_RECORD")
            if not spec.get("calibration"):
                problems.append(f"{rid}: no stored calibration; run python3 scripts/style/calibrate.py --rules {rid} --write")

    if kind == "prose" and not r.get("stated_in"):
        problems.append(f"{rid}: a prose rule needs at least one stated_in place with its marker")
    return problems


def report_html(results: dict, base: str) -> str:
    import report_html as h
    failed = sum(1 for p in results.values() if p)
    rows = [[f"<code>{h.e(rid)}</code>", h.chip("fail" if p else "pass", "Blocked" if p else "Passes"),
             "<br>".join(h.e(x) for x in p) or "All checks pass"] for rid, p in results.items()]
    body = h.table(["Rule", "Result", "Problems"], rows) if rows else "<p>No new rules since the base branch.</p>"
    return h.page("New style rule gate", f"Rules added since {base}: registered, tested, labeled, and checked against every other rule",
                  [h.card(f"New rules ({len(results)})", body)],
                  ("fail", f"{failed} blocked") if failed else ("pass", "No new rule blocked"))


def summary_md(results: dict, base: str, report_url: str | None) -> str:
    lines = [f"## New style rule gate: {'❌ ' + str(sum(1 for p in results.values() if p)) + ' blocked' if any(results.values()) else '✅ passed'}", ""]
    if report_url:
        lines += [f"**[Open the full HTML report]({report_url})** (opens in the browser; you need to be signed in to GitHub)", ""]
    if not results:
        return "\n".join(lines + [f"No new rules since `{base}`."])
    lines += ["| Rule | Result | Problems |", "| --- | --- | --- |"]
    for rid, p in results.items():
        cell = "<br>".join(x.replace("|", "\\|") for x in p)
        lines.append(f"| `{rid}` | {'❌ Blocked' if p else '✅ Passes'} | {cell} |")
    return "\n".join(lines)


def run(base: str) -> dict:
    """{rule id: problems} for each new rule. Jev answers replay from the committed recordings unless
    JEV_RECORD is set (then they're live and recorded)."""
    if not os.environ.get("JEV_RECORD"):
        os.environ.setdefault("JEV_REPLAY", os.pathsep.join([str(HERE / "test/fixtures/jev"), str(rh.RELATIONS_FIXTURES)]))
        if os.environ.get("TYPESAFE_API_KEY"):
            # The skill scan for new rules isn't recorded: fetch what's missing live, into a scratch directory
            os.environ["JEV_RECORD"] = tempfile.mkdtemp(prefix="jev-gate-")
    registry = rh.load_registry()
    new = new_rules(registry, base_state(base))
    if not new:
        return {}
    specs, labels = judge.load_specs(), rh.load_labels()
    reg_problems = check_registry.check(registry)
    out = {r["id"]: check_rule(r, registry, specs, labels, reg_problems) for r in new}
    for rid, problems in skill_problems(registry, {r["id"] for r in new}).items():
        out[rid] += problems
    return out


def skill_problems(registry: list[dict], ids: set) -> dict:
    """Skills, templates, and preferences that restate a new rule without its marker, or contradict it.
    One Jev request per section, with a question for each new rule."""
    import skill_rules
    try:
        res = skill_rules.scan(skill_rules.files(), registry, ids)
    except jev.JevUnavailable as e:
        return {rid: [f"{rid}: no recorded skill check ({e}); run TYPESAFE_API_KEY=… python3 scripts/style/new_rule_gate.py, "
                      "or let CI run it with the repo's key"] for rid in ids}
    out = {rid: [] for rid in ids}
    for f in res["findings"]:
        if not f["ok"]:
            out[f["rule"]].append(f"{f['rule']}: {f['file']}:{f['line']} ({f['heading']}) {f['kind']} it (p {f['p']:.2f}); "
                                  "point to the guide, add the rule's marker and a stated_in entry, or record an exception")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="origin/v0")
    ap.add_argument("--html")
    ap.add_argument("--summary", action="store_true", help="print the run summary (Markdown) of the last run, instead of the plain report")
    ap.add_argument("--report-url")
    a = ap.parse_args(argv)
    state = Path(tempfile.gettempdir()) / "new-rule-gate.json"
    if a.summary and state.is_file():  # the run summary after the upload step: don't judge again
        results = json.loads(state.read_text())
    else:
        results = run(a.base)
        state.write_text(json.dumps(results))
    if a.html:
        import report_html as h
        h.write(Path(a.html), report_html(results, a.base))
    if a.summary:
        print(summary_md(results, a.base, a.report_url))
    else:
        for rid, problems in results.items():
            print(f"{rid}: {'blocked' if problems else 'passes'}")
            for p in problems:
                print(f"    {p}")
        print(f"{len(results)} new rules since {a.base}, {sum(1 for p in results.values() if p)} blocked")
    return 1 if any(results.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
