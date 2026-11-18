#!/usr/bin/env python3
"""Check the style rules against each other: the Jev specs' choices, how they overlap, how the rules'
statements relate, and whether one rule's correct text breaks another.

  python3 scripts/style/rule_hygiene.py catalog
  python3 scripts/style/rule_hygiene.py overlap
  python3 scripts/style/rule_hygiene.py relations [--rules id,...]
  python3 scripts/style/rule_hygiene.py crossfire
  python3 scripts/style/rule_hygiene.py all [--html PATH]

catalog    Every choice name across the judgment specs. A problem: one name defined differently in two
           specs. A warning: a labeled case copied from its spec's criteria or examples, which tests the
           wording it was copied from rather than the rule.
overlap    From the recorded calibration answers (JEV_REPLAY), how often two choices of one spec both get
           probability >= 0.25 on the same case. Two choices on the same side of the verdict (both break
           the rule, or neither does) that split a third of the cases or more are near-duplicates. A split
           between a violating and a passing choice is Jev being unsure, and is reported, not a problem.
relations  For each rule, Jev reads its statement and answers, for every other rule, whether the two are
           the same requirement, overlap, conflict, or are independent. A same-requirement or conflicting
           pair is a problem unless the registry resolves it (relations: [{rule, relation, reason}]).
           Needs TYPESAFE_API_KEY, or JEV_REPLAY with recordings (scripts/style/test/fixtures/jev-relations).
crossfire  Lints each Vale fixture with every gating rule (registry gate block or warn). A pass line that
           another rule flags is a contradiction: following one rule breaks the other. A fail line that
           another rule also flags is an overlap (reported, not a problem).

Exits 1 if any command finds a problem, 3 if Jev is unavailable.
"""
import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev  # noqa: E402
import judge  # noqa: E402

ROOT = judge.ROOT
SPECS = judge.SPECS
LABELS = SPECS / "labels"
REGISTRY = ROOT / "style-rules/registry.yaml"
TESTS = ROOT / "style-rules/tests"
RELATIONS_FIXTURES = Path(__file__).resolve().parent / "test/fixtures/jev-relations"
SPLIT = 0.25          # a choice with at least this probability is "in play"
SPLIT_SHARE = 1 / 3   # a pair in play together on this share of cases is a near-duplicate
RELATION_P = 0.5      # a relation answer counts when its probability is at least this
RELATION_CRITERIA = {
    "same-requirement": "both rules ask for the same change to the same text: every violation of one is a violation of the other",
    "overlapping": "some text breaks both rules for the same reason, but each rule also catches text the other doesn't",
    "conflicting": "following one rule can force a writer to break the other",
    "independent": "the rules ask for unrelated things, even where both apply to the same sentence",
}
BLOCKING = ("same-requirement", "conflicting")


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", str(s)).strip().lower()


def load_registry() -> list[dict]:
    return yaml.safe_load(REGISTRY.read_text()) or []


def load_labels() -> dict:
    return {p.stem: (yaml.safe_load(p.read_text()) or {}).get("cases") or [] for p in sorted(LABELS.glob("*.yaml"))}


# ------------------------------------------------------------------ catalog

def catalog(specs: dict, labels: dict) -> dict:
    """{choices: {name: [(spec, criterion)]}, problems: [...], copied: [(spec, text)]}"""
    choices = collections.defaultdict(list)
    for rid, spec in specs.items():
        for name, crit in ((spec.get("check") or {}).get("question") or {}).get("criteria", {}).items():
            choices[name].append((rid, str(crit)))
    problems = []
    for name, uses in sorted(choices.items()):
        meanings = {norm(c) for _, c in uses}
        if len(meanings) > 1:
            detail = "; ".join(f"{rid}: {c[:80]}" for rid, c in uses if norm(c) != norm(uses[0][1]) or rid == uses[0][0])
            problems.append(f"choice {name!r} means different things in {len(uses)} specs: {detail}")
    copied = []
    for rid, cases in labels.items():
        spec = specs.get(rid) or {}
        source = norm(json.dumps([((spec.get("check") or {}).get("question") or {}).get("criteria"), spec.get("examples")]))
        for c in cases:
            if len(norm(c["text"])) > 12 and norm(c["text"]) in source:
                copied.append((rid, c["text"]))
    return {"choices": dict(choices), "problems": problems, "copied": copied}


# ------------------------------------------------------------------ overlap

def answers_for(rid: str, spec: dict, cases: list[dict]) -> list[tuple[dict, dict]]:
    """(case, answer) for each labeled case, from Jev (or JEV_REPLAY): the same requests calibrate.py sends."""
    q = {judge.key(rid): jev.choice_question(spec["check"]["question"]["ask"], spec["check"]["question"]["criteria"])}
    out = []
    for case in cases:
        cand = {"text": case["text"], "context": case.get("context", case["text"]), "mark": case.get("mark")}
        state = judge.state_for({"title": "calibration case"}, "calibration", cand)
        out.append((case, (jev.call(state, q).get("answers") or {}).get(judge.key(rid)) or {}))
    return out


def overlap(specs: dict, labels: dict) -> dict:
    """{rows: [(spec, a, b, together, cases, same_side)], problems: [...]}"""
    rows, problems = [], []
    for rid, cases in labels.items():
        spec = specs.get(rid)
        if not spec or not cases:
            continue
        together = collections.Counter()
        for _, ans in answers_for(rid, spec, cases):
            live = sorted(c for c, p in (ans.get("probabilities") or {}).items() if p >= SPLIT)
            for i, a in enumerate(live):
                for b in live[i + 1:]:
                    together[(a, b)] += 1
        bad = set((spec["check"].get("verdicts") or {}).get("violation") or [])
        for (a, b), n in sorted(together.items()):
            same_side = (a in bad) == (b in bad)
            rows.append((rid, a, b, n, len(cases), same_side))
            if same_side and n / len(cases) >= SPLIT_SHARE:
                problems.append(f"{rid}: choices {a!r} and {b!r} split the probability on {n} of {len(cases)} cases")
    return {"rows": rows, "problems": problems}


# ------------------------------------------------------------------ relations

def relation_question(other: dict) -> dict:
    ask = (f"How does the rule in `rule` relate to this other house style rule, {other['id']}: "
           f"\"{other['statement']}\"" + (f" (applies to {other['applies_to']})" if other.get("applies_to") else "") + "?")
    return jev.choice_question(ask, RELATION_CRITERIA)


def relation_state(rule: dict) -> dict:
    return {"rule": {"id": rule["id"], "statement": rule["statement"], "scope": rule.get("scope"),
                     "applies_to": rule.get("applies_to") or "every docs page"},
            "context": "House style rules for Sensible's developer documentation."}


def call_state(state: dict, questions: dict) -> dict:
    """jev.call with a structured state (Jev accepts an object)."""
    return jev.call(state, questions)


def relations(registry: list[dict], only: set | None = None) -> dict:
    """{pairs: {(a, b): {a->b answer, b->a answer}}, problems: [...]}"""
    by_id = {r["id"]: r for r in registry}
    targets = [r for r in registry if not only or r["id"] in only]
    answers = {}
    for rule in targets:
        others = [o for o in registry if o["id"] != rule["id"]]
        qs = {judge.key(o["id"]): relation_question(o) for o in others}
        resp = call_state(relation_state(rule), qs)
        for o in others:
            answers[(rule["id"], o["id"])] = (resp.get("answers") or {}).get(judge.key(o["id"])) or {}
    pairs, problems = {}, []
    for (a, b), ans in answers.items():
        key = tuple(sorted((a, b)))
        pairs.setdefault(key, {})[f"{a}->{b}"] = ans
    resolved = {(r["id"], x["rule"]) for r in registry for x in r.get("relations") or []}
    for (a, b), both in sorted(pairs.items()):
        for rel in BLOCKING:
            ps = [x.get("probabilities", {}).get(rel, 0) for x in both.values()]
            if max(ps) >= RELATION_P and (a, b) not in resolved and (b, a) not in resolved:
                problems.append(f"{a} and {b}: {rel} (p {max(ps):.2f}): \"{by_id[a]['statement'][:70]}\" / "
                                f"\"{by_id[b]['statement'][:70]}\"")
    return {"pairs": pairs, "problems": problems}


# ------------------------------------------------------------------ crossfire

def gating_checks(registry: list[dict]) -> dict:
    """Vale check name -> rule id, for rules whose gate is block or warn."""
    return {v: r["id"] for r in registry if r.get("gate") in ("block", "warn")
            for v in (r.get("enforced_by") or {}).get("vale") or []}


def crossfire(registry: list[dict], fixtures: list[Path] | None = None) -> dict:
    """{contradictions: [(fixture, line, text, check)], overlaps: [...], problems: [...]}"""
    import test_rules
    exe = test_rules.vale()
    gating = gating_checks(registry)
    contradictions, overlaps = [], []
    for path in fixtures or sorted(TESTS.glob("*.md")):
        text = path.read_text()
        m = test_rules.RULES.search(text)
        own = {r.strip() for r in m.group(1).split(",")} if m else set()
        out = subprocess.run([exe, "--config", str(ROOT / ".vale.ini"), "--output=JSON", "--minAlertLevel=suggestion",
                              str(path.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True)
        try:
            hits = [a for v in json.loads(out.stdout or "{}").values() for a in v]
        except json.JSONDecodeError:
            hits = []
        lines = text.splitlines()
        for a in hits:
            if a["Check"] in own or a["Check"] not in gating:
                continue
            line = lines[a["Line"] - 1]
            mark = test_rules.MARK.search(line)
            kind = mark and (mark.group(1) or mark.group(2))
            row = (path.name, a["Line"], line.strip()[:100], a["Check"])
            if kind == "pass":
                contradictions.append(row)
            elif kind == "fail":
                overlaps.append(row)
    problems = [f"{f}:{n}: a pass line for this fixture breaks {c}: {t}" for f, n, t, c in contradictions]
    return {"contradictions": contradictions, "overlaps": overlaps, "problems": problems}


# ------------------------------------------------------------------ report

def html_sections(cat=None, ovl=None, rel=None, cf=None, registry=None) -> list[str]:
    import report_html as h
    out = []
    if cat is not None:
        rows = [[f"<code>{h.e(n)}</code>", "<br>".join(f"<b>{h.e(r)}</b>: {h.e(c)}" for r, c in uses)]
                for n, uses in sorted(cat["choices"].items()) if len(uses) > 1 or n != "other"]
        body = (h.table(["Problem"], [[h.e(p)] for p in cat["problems"]]) if cat["problems"] else "<p>No choice name means two things.</p>")
        body += "<h3>Labeled cases copied from their spec</h3>" + (
            h.table(["Rule", "Case"], [[f"<code>{h.e(r)}</code>", h.e(t)] for r, t in cat["copied"]]) if cat["copied"] else "<p>None.</p>")
        body += "<h3>Every choice</h3>" + h.table(["Choice", "Criteria by spec"], rows)
        out.append(h.card("Choice catalog", body, "One name, one meaning. A copied case tests the wording it was copied from.",
                          open_=bool(cat["problems"] or cat["copied"])))
    if ovl is not None:
        body = h.table(["Rule", "Choices", "Kind", "Cases split", "Share"], [
            [f"<code>{h.e(r)}</code>", f"{h.e(a)} / {h.e(b)}", "same side: near-duplicate?" if same else "opposite sides: Jev unsure",
             f"{n} of {t}", h.chip("fail" if same and n / t >= SPLIT_SHARE else ("warn" if n / t >= SPLIT_SHARE else "pass"), f"{n / t:.0%}")]
            for r, a, b, n, t, same in ovl["rows"]]) if ovl["rows"] else "<p>No two choices split a case.</p>"
        out.append(h.card("Choice overlap", body, f"Cases where two choices of one spec both get probability {SPLIT} or more.", open_=bool(ovl["problems"])))
    if rel is not None:
        by_id = {r["id"]: r for r in registry or []}
        flagged = []
        for (a, b), both in sorted(rel["pairs"].items()):
            best = {}
            for ans in both.values():
                for k, p in (ans.get("probabilities") or {}).items():
                    best[k] = max(best.get(k, 0), p)
            top = max(best, key=best.get) if best else ""
            if top in ("same-requirement", "conflicting", "overlapping"):
                flagged.append((best.get(top, 0), a, b, top))
        rows = [[f"<code>{h.e(a)}</code><br>{h.e(by_id.get(a, {}).get('statement', ''))}",
                 f"<code>{h.e(b)}</code><br>{h.e(by_id.get(b, {}).get('statement', ''))}",
                 h.chip("fail" if top in BLOCKING else "info", top), f"{p:.2f}"] for p, a, b, top in sorted(flagged, reverse=True)]
        body = (h.table(["Problem"], [[h.e(p)] for p in rel["problems"]]) if rel["problems"] else "<p>No unresolved same-requirement or conflicting pair.</p>")
        body += "<h3>Pairs Jev relates</h3>" + (h.table(["Rule", "Other rule", "Relation", "p"], rows) if rows else "<p>None.</p>")
        out.append(h.card(f"Rule relations {h.JUDGE}".replace(h.e(h.JUDGE), h.JUDGE), body,
                          f"{len(rel['pairs'])} pairs judged from the rules' statements, in both directions. Code decides what blocks.",
                          open_=bool(rel["problems"])))
    if cf is not None:
        body = (h.table(["Fixture", "Line", "Text", "Broken rule"], [[h.e(f), str(n), h.e(t), f"<code>{h.e(c)}</code>"] for f, n, t, c in cf["contradictions"]])
                if cf["contradictions"] else "<p>No fixture's correct text breaks another gating rule.</p>")
        if cf["overlaps"]:
            body += "<h3>Fail lines another rule also flags</h3>" + h.table(["Fixture", "Line", "Text", "Also flagged by"], [
                [h.e(f), str(n), h.e(t), f"<code>{h.e(c)}</code>"] for f, n, t, c in cf["overlaps"]])
        out.append(h.card("Fixture cross-fire", body, "Each Vale fixture linted with every rule whose gate is block or warn.",
                          open_=bool(cf["contradictions"])))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["catalog", "overlap", "relations", "crossfire", "all"])
    ap.add_argument("--rules")
    ap.add_argument("--html")
    a = ap.parse_args(argv)
    specs, labels, registry = judge.load_specs(), load_labels(), load_registry()
    results, problems = {}, []
    try:
        if a.command in ("catalog", "all"):
            results["cat"] = catalog(specs, labels)
            for rid, t in results["cat"]["copied"]:
                print(f"warning: {rid}: labeled case copied from the spec: {t[:90]!r}")
        if a.command in ("overlap", "all"):
            results["ovl"] = overlap(specs, labels)
        if a.command in ("relations", "all"):
            results["rel"] = relations(registry, set(a.rules.split(",")) if a.rules else None)
        if a.command in ("crossfire", "all"):
            results["cf"] = crossfire(registry)
            for f, n, t, c in results["cf"]["overlaps"]:
                print(f"overlap: {f}:{n}: also flagged by {c}: {t[:80]!r}")
    except jev.JevUnavailable as e:
        print(f"rule_hygiene: Jev unavailable: {e}", file=sys.stderr)
        return 3
    for r in results.values():
        problems += r["problems"]
    for p in problems:
        print(p)
    if a.html:
        import report_html
        report_html.write(Path(a.html), report_html.page("Style rule hygiene", "How the rules agree with each other",
                                                          html_sections(**results, registry=registry),
                                                          ("fail", f"{len(problems)} problems") if problems else ("pass", "No problems")))
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
