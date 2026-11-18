#!/usr/bin/env python3
"""The weekly Jev cleanup: how the judgment rules, their labels, and the rules' relations hold up this week.

  python3 scripts/style/weekly_cleanup.py run --out DIR [--pages N]
  python3 scripts/style/weekly_cleanup.py summary --results DIR/results.json [--report-url URL] [--run-url URL]
  python3 scripts/style/weekly_cleanup.py issue --results DIR/results.json [--report-url URL] [--run-url URL]

run      Needs TYPESAFE_API_KEY and Vale. Writes DIR/results.json and DIR/report.html:
         - calibration: each judgment rule rerun live on its labels, against the stored numbers
         - corpus: the judge on every docs page, and for each Vale-backed rule the share of its hits Jev clears
         - relations, choice overlap, choice catalog, and fixture cross-fire (rule_hygiene.py)
         - labels still marked labeled_by: claude, and rule-like sentences in the guides with no registry entry
         --pages N judges only the first N pages (for a quick check).
summary  Prints the Markdown run summary ($GITHUB_STEP_SUMMARY).
issue    Prints the Markdown body for the weekly issue.

Exits 3 if Jev is unavailable, 0 otherwise: the report is information, and the issue carries it.
"""
import argparse
import datetime
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calibrate  # noqa: E402
import jev  # noqa: E402
import judge  # noqa: E402
import rule_hygiene as rh  # noqa: E402
import rule_map  # noqa: E402

ROOT = judge.ROOT
DRIFT = 0.15  # a live precision this much below the stored number is drift (one case in six moves it 0.17)


def run_calibration(specs: dict, labels: dict) -> list[dict]:
    out = []
    for rid, spec in specs.items():
        cases = labels.get(rid)
        if not cases:
            continue
        res = calibrate.calibrate(rid, spec, cases)
        stored = spec.get("calibration") or {}
        live_trusted = judge.trusted({"calibration": res})
        out.append({"rule": rid, "cases": res["cases"], "violations": res["violations"],
                    "precision": res["precision"], "recall": res["recall"],
                    "stored_precision": stored.get("precision"), "stored_recall": stored.get("recall"),
                    "stored_trusted": judge.trusted(spec), "trusted": live_trusted, "model": res["model"],
                    # Jev isn't deterministic, so small moves are noise; a loss of precision or a change in trust isn't
                    "drift": (stored.get("precision") is not None and stored["precision"] - res["precision"] >= DRIFT)
                    or live_trusted != judge.trusted(spec),
                    "disagreements": [{"text": r["text"], "expected": r["expected"], "got": r["got"], "p": r["p_violation"]}
                                      for r in res["rows"] if not r["verdict_ok"]],
                    "input_tokens": res["input_tokens"]})
    return out


def run_corpus(specs: dict, pages: int | None) -> dict:
    files = sorted(p for p in (ROOT / "docs").rglob("*.md") if not p.name.startswith("draft-"))
    if pages:
        files = files[:pages]
    out = judge.judge(files, specs)
    by_rule = {}
    for r in out["results"]:
        x = by_rule.setdefault(r["rule"], {"violation": 0, "unsure": 0, "review": 0, "ok": 0})
        x[r["verdict"]] = x.get(r["verdict"], 0) + 1
    flagged = [{k: r[k] for k in ("rule", "path", "line", "text", "choice", "p_violation", "verdict", "trusted")}
               for r in out["results"] if r["verdict"] in ("violation", "unsure")]
    return {"pages": len(files), "calls": out["calls"], "input_tokens": out["usage"]["input_tokens"],
            "by_rule": by_rule, "flagged": flagged}


def unreviewed(labels: dict) -> dict:
    return {rid: {"claude": sum(c.get("labeled_by") == "claude" for c in cases), "total": len(cases)}
            for rid, cases in labels.items()}


def run(out_dir: Path, pages: int | None) -> dict:
    specs, labels, registry = judge.load_specs(), rh.load_labels(), rh.load_registry()
    vale_rules = {r["id"]: (r.get("enforced_by") or {}).get("vale") or [] for r in registry}
    cal = run_calibration(specs, labels)
    corpus = run_corpus(specs, pages)
    rel = rh.relations(registry)
    ovl = rh.overlap(specs, labels)
    cat = rh.catalog(specs, labels)
    cf = rh.crossfire(registry)
    results = {
        "date": datetime.date.today().isoformat(), "model": next((c["model"] for c in cal if c.get("model")), None),
        "calibration": cal, "corpus": corpus,
        "vale_clear_rate": {rid: {"checks": vale_rules[rid], "hits": sum(v.values()), "cleared": v.get("ok", 0) + v.get("review", 0)}
                            for rid, v in corpus["by_rule"].items() if vale_rules.get(rid)},
        "relations": {"problems": rel["problems"],
                      "pairs": {f"{a}|{b}": both for (a, b), both in rel["pairs"].items()}},
        "overlap": {"problems": ovl["problems"], "rows": ovl["rows"]},
        "catalog": {"problems": cat["problems"], "copied": cat["copied"]},
        "crossfire": cf, "unreviewed": unreviewed(labels),
        "coverage": [{"file": f, "line": n, "text": t} for f, n, t in rule_map.coverage()],
    }
    tokens = sum(c["input_tokens"] for c in cal) + corpus["input_tokens"]
    results["input_tokens_approx"] = tokens
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(results, indent=1, default=list))
    (out_dir / "report.html").write_text(render_html(results, registry))
    return results


def problems(results: dict) -> list[str]:
    out = [f"calibration drift: {c['rule']} precision {c['stored_precision']} → {c['precision']}, recall {c['stored_recall']} → {c['recall']}"
           + (f", {'now trusted' if c['trusted'] else 'no longer trusted'}" if c["trusted"] != c["stored_trusted"] else "")
           for c in results["calibration"] if c["drift"]]
    out += results["relations"]["problems"] + results["overlap"]["problems"] + results["catalog"]["problems"] + results["crossfire"]["problems"]
    return out


def render_html(results: dict, registry: list[dict]) -> str:
    import report_html as h
    probs = problems(results)
    sections = []
    cal_rows = [[f"<code>{h.e(c['rule'])}</code>", f"{c['cases']} ({c['violations']})",
                 f"{c['stored_precision']} → <b>{c['precision']}</b>", f"{c['stored_recall']} → <b>{c['recall']}</b>",
                 h.chip("pass" if c["trusted"] else "info", "trusted" if c["trusted"] else "advisory"),
                 h.chip("fail", "drift") if c["drift"] else ""] for c in results["calibration"]]
    dis = "".join(f"<li><code>{h.e(c['rule'])}</code>: expected <b>{h.e(d['expected'])}</b>, Jev said {h.e(d['got'])} "
                  f"(p violation {d['p']:.2f}): {h.e(d['text'][:160])}</li>" for c in results["calibration"] for d in c["disagreements"])
    sections.append(h.card("Calibration", h.table(["Rule", "Cases (violations)", "Precision", "Recall", "Trust", ""], cal_rows)
                           + (f"<h3>Where Jev and the labels disagree</h3><ul>{dis}</ul>" if dis else ""),
                           "Each judgment rule rerun live on its labels. Stored numbers → this week's. Drift is a precision drop of 0.15 or more, or a change in trust; Jev isn't deterministic, so recall moves a little from week to week.",
                           open_=True, badge=h.JUDGE))
    corpus = results["corpus"]
    clear = [[f"<code>{h.e(rid)}</code>", h.e(", ".join(v["checks"])), str(v["hits"]), str(v["cleared"]),
              h.chip("warn" if v["hits"] and v["cleared"] / v["hits"] >= 0.8 else "pass", f"{v['cleared'] / v['hits']:.0%}" if v["hits"] else "n/a")]
             for rid, v in sorted(results["vale_clear_rate"].items())]
    by = [[f"<code>{h.e(rid)}</code>", str(v.get("violation", 0)), str(v.get("unsure", 0)), str(v.get("review", 0)), str(v.get("ok", 0))]
          for rid, v in sorted(corpus["by_rule"].items())]
    flagged = [[h.e(f"{r['path']}:{r['line']}"), f"<code>{h.e(r['rule'])}</code>", h.chip("fail" if r["verdict"] == "violation" else "warn", r["verdict"])
                + ("" if r["trusted"] else ' <span class="muted">advisory</span>'), f"{r['p_violation']:.2f}", h.e(r["text"][:180])]
               for r in sorted(corpus["flagged"], key=lambda r: (-r["p_violation"], r["path"]))]
    sections.append(h.card("Docs corpus",
                           "<h3>How often Jev clears each Vale-backed rule's hits</h3>"
                           + h.table(["Rule", "Vale checks", "Hits", "Cleared by Jev", "Share"], clear)
                           + '<p class="muted">A rule whose hits Jev clears 80% of the time or more is a candidate to narrow or drop.</p>'
                           + "<h3>Verdicts by rule</h3>" + h.table(["Rule", "Violation", "Unsure", "Review", "OK"], by)
                           + f"<h3>Flagged text ({len(flagged)})</h3>" + (h.table(["Where", "Rule", "Verdict", "p", "Text"], flagged) if flagged else "<p>None.</p>"),
                           f"The judge on {corpus['pages']} docs pages, {corpus['calls']} Jev calls.", open_=True, badge=h.JUDGE))
    sections += rh.html_sections(
        cat={"choices": rh.catalog(judge.load_specs(), rh.load_labels())["choices"], **results["catalog"]},
        ovl={"rows": [tuple(r) for r in results["overlap"]["rows"]], "problems": results["overlap"]["problems"]},
        rel={"problems": results["relations"]["problems"],
             "pairs": {tuple(k.split("|")): v for k, v in results["relations"]["pairs"].items()}},
        cf=results["crossfire"], registry=registry)
    un = [[f"<code>{h.e(rid)}</code>", f"{v['claude']} of {v['total']}"] for rid, v in sorted(results["unreviewed"].items()) if v["claude"]]
    sections.append(h.card(f"Labels to review ({sum(v['claude'] for v in results['unreviewed'].values())})",
                           h.table(["Rule", "Labeled by Claude, not reviewed"], un) if un else "<p>Every label is reviewed.</p>",
                           "Change <code>labeled_by: claude</code> to <code>frances</code> as you review each case in "
                           "<code>style-rules/judgment/labels/</code>.", open_=False))
    cov = results["coverage"]
    sections.append(h.card(f"Unregistered rule-like sentences ({len(cov)})",
                           h.table(["File", "Line", "Text"], [[h.e(c["file"]), str(c["line"]), h.e(c["text"][:200])] for c in cov]),
                           "Sentences in the style guides that read like a rule, with no rule marker in their section.", open_=False))
    status = ("fail", f"{len(probs)} problems") if probs else ("pass", "No problems")
    return h.page("Weekly style rule cleanup", f"{results['date']} · {results.get('model') or 'Jev'} · about "
                  f"${results['input_tokens_approx'] * jev.INPUT_USD_PER_M / 1e6:.3f} of Jev", sections, status)


def links(report_url: str | None, run_url: str | None) -> list[str]:
    if report_url:
        return [f"**[Open the full HTML report]({report_url})** (opens in the browser; you need to be signed in to GitHub)"]
    if run_url:
        return [f"Report: the artifacts at the bottom of [this run]({run_url})"]
    return []


def summary(results: dict, report_url: str | None, run_url: str | None) -> str:
    probs = problems(results)
    corpus = results["corpus"]
    trusted = sum(c["trusted"] for c in results["calibration"])
    lines = [f"## Weekly style rule cleanup: {'⚠️ ' + str(len(probs)) + ' problems' if probs else '✅ no problems'}", ""]
    lines += [*links(report_url, run_url), ""] if links(report_url, run_url) else []
    lines += [
             f"- Calibration: {len(results['calibration'])} judgment rules, {trusted} trusted, "
             f"{sum(c['drift'] for c in results['calibration'])} drifted",
             f"- Docs corpus: {corpus['pages']} pages, {sum(v.get('violation', 0) for v in corpus['by_rule'].values())} violations, "
             f"{sum(v.get('unsure', 0) for v in corpus['by_rule'].values())} unsure",
             f"- Labels not yet reviewed: {sum(v['claude'] for v in results['unreviewed'].values())}",
             f"- Unregistered rule-like sentences: {len(results['coverage'])}"]
    if probs:
        lines += ["", "### Problems", ""] + [f"- {p}" for p in probs]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["run", "summary", "issue"])
    ap.add_argument("--out", default="weekly-output")
    ap.add_argument("--results")
    ap.add_argument("--pages", type=int)
    ap.add_argument("--report-url")
    ap.add_argument("--run-url")
    a = ap.parse_args(argv)
    if a.command == "run":
        try:
            results = run(Path(a.out), a.pages)
        except jev.JevUnavailable as e:
            print(f"weekly_cleanup: Jev unavailable: {e}", file=sys.stderr)
            return 3
        for p in problems(results):
            print(p)
        print(f"wrote {Path(a.out) / 'report.html'}")
        return 0
    results = json.loads(Path(a.results).read_text())
    text = summary(results, a.report_url, a.run_url)
    if a.command == "issue":  # one comment per week on the standing issue
        text = text.replace("## Weekly style rule cleanup:", f"## Week of {results['date']}:", 1)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
