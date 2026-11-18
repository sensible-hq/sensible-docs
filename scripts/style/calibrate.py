#!/usr/bin/env python3
"""Calibrate the judgment rules: ask Jev each labeled case and measure agreement with the labels.

  python3 scripts/style/calibrate.py [--rules id,...] [--write]

Cases are in style-rules/judgment/labels/<id>.yaml: a text and the choice a reviewer expects. For each
rule it reports:

  precision          of the cases Jev flagged as violations (a verdicts.violation choice at confidence
                     >= 0.70), the share the labels agree are violations
  recall             of the labeled violations, the share Jev flagged
  verdict agreement  Jev and the label agree on whether the case breaks the rule
  choice agreement   Jev picked exactly the labeled choice

and lists every disagreement. --write stores the result in the spec's calibration field, which judge.py
reads: a rule with precision >= 0.90 and recall >= 0.50, over at least 6 cases with at least 3 labeled
violations, can fail a run; otherwise it only advises.
Precision comes first because a judge that flags good text teaches writers to ignore it.

Set JEV_RECORD to save responses, JEV_REPLAY to rerun offline. Exit 3 if Jev is unavailable.
"""
import argparse
import concurrent.futures
import datetime
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jev  # noqa: E402
import judge  # noqa: E402

LABELS = judge.SPECS / "labels"


def violates(spec: dict, choice: str, confidence: float = 1.0) -> bool:
    return choice in (spec["check"].get("verdicts") or {}).get("violation", []) and confidence >= judge.THRESHOLD


def calibrate(rid: str, spec: dict, cases: list[dict]) -> dict:
    criteria = spec["check"]["question"]["criteria"]
    bad = [c["expected"] for c in cases if c["expected"] not in criteria]
    if bad:
        raise ValueError(f"{rid}: labels use choices the spec doesn't have: {sorted(set(bad))}")
    q = {judge.key(rid): jev.choice_question(spec["check"]["question"]["ask"], criteria)}

    def ask(case):
        cand = {"text": case["text"], "context": case.get("context", case["text"]), "mark": case.get("mark")}
        state = judge.state_for({"title": "calibration case"}, "calibration", cand)
        resp = jev.call(state, q)
        return case, (resp.get("answers") or {}).get(judge.key(rid)) or {}, resp

    rows, model, usage = [], None, 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for case, ans, resp in pool.map(ask, cases):
            model = resp.get("model") or model
            usage += (resp.get("usage") or {}).get("input_tokens", 0)
            got, conf = ans.get("choice"), ans.get("confidence", 0)
            rows.append({"text": case["text"], "expected": case["expected"], "got": got, "confidence": conf,
                         "verdict_ok": violates(spec, case["expected"]) == violates(spec, got, conf),
                         "choice_ok": got == case["expected"]})
    n = len(rows)
    flagged = [r for r in rows if violates(spec, r["got"], r["confidence"])]
    real = [r for r in rows if violates(spec, r["expected"])]
    hits = [r for r in flagged if violates(spec, r["expected"])]
    return {"rule": rid, "cases": n, "model": model, "input_tokens": usage,
            "precision": round(len(hits) / len(flagged), 2) if flagged else 0.0,
            "recall": round(len(hits) / len(real), 2) if real else 0.0, "violations": len(real),
            "agreement": round(sum(r["verdict_ok"] for r in rows) / n, 2),
            "choice_agreement": round(sum(r["choice_ok"] for r in rows) / n, 2), "rows": rows}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    specs = judge.load_specs(set(a.rules.split(",")) if a.rules else None)
    total = 0
    for rid, spec in specs.items():
        f = LABELS / f"{rid}.yaml"
        if not f.exists():
            print(f"{rid}: no labels")
            continue
        cases = yaml.safe_load(f.read_text())["cases"]
        try:
            res = calibrate(rid, spec, cases)
        except jev.JevUnavailable as e:
            print(f"calibrate: Jev unavailable: {e}", file=sys.stderr)
            return 3
        total += res["input_tokens"]
        trust = "trusted" if judge.trusted({"calibration": res}) else "advisory"
        print(f"{rid}: precision {res['precision']:.2f}, recall {res['recall']:.2f}, "
              f"verdict agreement {res['agreement']:.2f}, choice agreement {res['choice_agreement']:.2f}, "
              f"{res['cases']} cases, {res['model']} -> {trust}")
        for r in res["rows"]:
            if not r["verdict_ok"] or not r["choice_ok"]:
                kind = "VERDICT" if not r["verdict_ok"] else "choice"
                print(f"    {kind}: expected {r['expected']}, got {r['got']} {r['confidence']:.2f}: {r['text'][:90]!r}")
        if a.write:
            path = judge.SPECS / f"{rid}.yaml"
            text = path.read_text()
            header = "".join(l for l in text.splitlines(keepends=True) if l.startswith("#"))
            data = yaml.safe_load(text)
            data["calibration"] = {"precision": res["precision"], "recall": res["recall"], "violations": res["violations"],
                                   "agreement": res["agreement"], "choice_agreement": res["choice_agreement"],
                                   "cases": res["cases"], "model": res["model"],
                                   "date": datetime.date.today().isoformat(), "labels": f"labels/{rid}.yaml"}
            path.write_text(header + yaml.dump(data, sort_keys=False, allow_unicode=True, width=110))
    print(f"{total} input tokens (${total * jev.INPUT_USD_PER_M / 1e6:.4f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
