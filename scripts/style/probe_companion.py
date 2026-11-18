#!/usr/bin/env python3
"""One-off probe: does a companion yes-or-no question work better than each spec's `other` option?

  python3 scripts/style/probe_companion.py [--rules id,...]

TypeSafe's guidance (Jev 1.14): a Choice always picks an option, and a Noul asked alongside it ("does
anything fit?") usually tells code when nothing fits better than a "none of the above" option. For each
labeled case this sends one request with three questions over the same state:

  current    the spec's question as it is, with `other`
  no_other   the same question without `other`
  fits       a Noul: does any of the spec's choices describe the marked text?

and reports, per rule, verdict agreement with the labels for current and no_other, how much probability
`other` takes, and the Noul's mean. Responses are recorded under test/fixtures/jev-companion, so the
numbers can be reproduced with JEV_REPLAY. Results: .claude/sessions/rule-observability/decisions.md.
"""
import argparse
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev  # noqa: E402
import judge  # noqa: E402
import rule_hygiene  # noqa: E402


def questions(spec: dict) -> dict:
    q = spec["check"]["question"]
    crit = q["criteria"]
    without = {k: v for k, v in crit.items() if k != "other"}
    listed = "; ".join(f"{k}: {v}" for k, v in without.items())
    return {"current": jev.choice_question(q["ask"], crit),
            "no_other": jev.choice_question(q["ask"], without),
            "fits": {"type": "noul", "instructions": f"Does one of these descriptions fit the marked text? {listed}"}}


def probe(rid: str, spec: dict, cases: list[dict]) -> dict:
    qs = questions(spec)
    bad = set((spec["check"].get("verdicts") or {}).get("violation") or [])
    rows = []
    for case in cases:
        cand = {"text": case["text"], "context": case.get("context", case["text"]), "mark": case.get("mark")}
        resp = jev.call(judge.state_for({"title": "calibration case"}, "calibration", cand), qs)
        a = resp.get("answers") or {}
        expect = case["expected"] in bad
        rows.append({"current_ok": (judge.verdict(spec, a.get("current") or {}) == "violation") == expect,
                     "no_other_ok": (judge.verdict(spec, a.get("no_other") or {}) == "violation") == expect,
                     "other_p": ((a.get("current") or {}).get("probabilities") or {}).get("other", 0),
                     "fits": (a.get("fits") or {}).get("noul"),
                     "tokens": (resp.get("usage") or {}).get("input_tokens", 0)})
    n = len(rows)
    return {"rule": rid, "cases": n, "current": sum(r["current_ok"] for r in rows) / n,
            "no_other": sum(r["no_other_ok"] for r in rows) / n,
            "other_p": statistics.mean(r["other_p"] for r in rows),
            "fits": statistics.mean(r["fits"] for r in rows if r["fits"] is not None) if any(r["fits"] is not None for r in rows) else None,
            "tokens": sum(r["tokens"] for r in rows)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rules")
    a = ap.parse_args(argv)
    specs, labels = judge.load_specs(set(a.rules.split(",")) if a.rules else None), rule_hygiene.load_labels()
    out, tokens = [], 0
    try:
        for rid, spec in specs.items():
            if labels.get(rid) and "other" in spec["check"]["question"]["criteria"]:
                out.append(probe(rid, spec, labels[rid]))
    except jev.JevUnavailable as e:
        print(f"probe: Jev unavailable: {e}", file=sys.stderr)
        return 3
    print("| rule | cases | agreement with other | agreement without | mean p(other) | mean fits |")
    print("| ---- | ----: | -------------------: | ----------------: | ------------: | --------: |")
    for r in out:
        tokens += r["tokens"]
        fits = f"{r['fits']:.2f}" if r["fits"] is not None else "n/a"
        print(f"| {r['rule']} | {r['cases']} | {r['current']:.2f} | {r['no_other']:.2f} | {r['other_p']:.2f} | {fits} |")
    n = sum(r["cases"] for r in out)
    print(f"\nall: with other {sum(r['current'] * r['cases'] for r in out) / n:.3f}, "
          f"without {sum(r['no_other'] * r['cases'] for r in out) / n:.3f}, {n} cases, "
          f"{tokens} input tokens (${tokens * jev.INPUT_USD_PER_M / 1e6:.4f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
