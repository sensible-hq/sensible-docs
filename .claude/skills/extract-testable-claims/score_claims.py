#!/usr/bin/env python3
"""Score claims against criteria.md with Jev: one noul (yes/no) per claim.

  python3 score_claims.py <claims.json> [--out scored.json]
  python3 score_claims.py --calibrate

claims.json is a list of {"claim", "page", "line", "sentence", "kind"}. "claim" is one behavior, split out
of "sentence", the docs sentence it came from. Only this docs text goes to Jev; never send engine code.
A claim with "kind": "output" (an example's Output block) is always worth testing, so it isn't sent to
Jev; Jev scored these inconsistently in calibration.

Each claim gets "p", Jev's probability that it meets the criteria. At or above 0.70 it's worth testing,
at or below 0.30 it isn't, and in between it's unsure. Output is sorted by p, highest first.

--calibrate asks Jev about the labeled claims in cases.yaml and reports how often it agrees.
Exit 3 if Jev is unavailable.
"""
import argparse
import concurrent.futures
import json
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts/style"))
import jev  # noqa: E402

YES, NO = 0.70, 0.30


def question() -> dict:
    """The noul question: the blockquote that ends criteria.md."""
    text = (HERE / "criteria.md").read_text()
    quote = re.findall(r"^> ?(.*)$", text, re.M)
    return {"type": "noul", "instructions": " ".join(q.strip() for q in quote if q.strip())}


def verdict(p: float) -> str:
    return "test" if p >= YES else "skip" if p <= NO else "unsure"


def score(claims: list[dict]) -> list[dict]:
    q = {"worth_testing": question()}

    def ask(c):
        parts = [f"Page: {c.get('page', 'docs page')}"]
        if c.get("sentence") and c["sentence"] != c["claim"]:
            parts.append(f"Context:\n{c['sentence']}")
        parts.append(f"Marked text:\n{c['claim']}")
        resp = jev.call("\n\n".join(parts), q)
        p = ((resp.get("answers") or {}).get("worth_testing") or {}).get("noul")
        return {**c, "p": p, "verdict": verdict(p) if p is not None else "no answer"}

    fixed = [{**c, "p": 1.0, "verdict": "test"} for c in claims if c.get("kind") == "output"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        out = list(pool.map(ask, [c for c in claims if c.get("kind") != "output"]))
    return sorted(fixed + out, key=lambda c: -(c["p"] or 0))


def calibrate() -> int:
    cases = yaml.safe_load((HERE / "cases.yaml").read_text())["cases"]
    rows = score([{"claim": c["claim"], "expected": c["expected"]} for c in cases])
    flagged = [r for r in rows if r["verdict"] == "test"]
    real = [r for r in rows if r["expected"] == "yes"]
    hits = [r for r in flagged if r["expected"] == "yes"]
    print(f"precision {len(hits) / len(flagged) if flagged else 0:.2f}, recall {len(hits) / len(real) if real else 0:.2f}, "
          f"{len(rows)} cases")
    for r in rows:
        ok = (r["verdict"] == "test") == (r["expected"] == "yes") and r["verdict"] != "unsure"
        print(f"  {'  ' if ok else '✗ '}{r['p']:.2f} {r['verdict']:6} expected {r['expected']:3}  {r['claim'][:90]}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("claims", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--calibrate", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.calibrate:
            return calibrate()
        if not a.claims:
            ap.error("give a claims.json file, or --calibrate")
        rows = score(json.loads(Path(a.claims).read_text()))
    except jev.JevUnavailable as e:
        print(f"score_claims: Jev unavailable: {e}", file=sys.stderr)
        return 3
    if a.out:
        Path(a.out).write_text(json.dumps(rows, indent=2) + "\n")
    for r in rows:
        print(f"{r['p']:.2f} {r['verdict']:6} {r.get('page', '')}:{r.get('line', '')}  {r['claim']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
