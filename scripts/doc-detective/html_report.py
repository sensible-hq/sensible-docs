#!/usr/bin/env python3
"""Render a readable HTML report of a Doc Detective run.

Reads Doc Detective's newest testResults-*.json and the code-test records that run_examples.py
writes to output/examples/, and writes output/report.html.

Usage: html_report.py [output dir]   (default: scripts/doc-detective/output)
"""

import glob
import html
import json
import os
import sys
from datetime import datetime

DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

CSS = """
:root {
  --bg: #f7f7f5; --card: #ffffff; --text: #1d1d1b; --muted: #6b6b66; --border: #e3e2dd;
  --code-bg: #f1f0ec; --pass: #1f7a4d; --pass-bg: #e3f3ea; --fail: #b3261e; --fail-bg: #fbe7e5;
  --warn: #8a5a00; --warn-bg: #fdf1d8; --info: #3b4a8a; --info-bg: #e8ebf7;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #161615; --card: #1f1f1d; --text: #ecebe6; --muted: #a3a29b; --border: #33332f;
    --code-bg: #262623; --pass: #6fd3a0; --pass-bg: #17322a; --fail: #ff8a80; --fail-bg: #3a1c1a;
    --warn: #f3c46b; --warn-bg: #3a2e14; --info: #a9b6f2; --info-bg: #222a45;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text);
  font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
main { max-width: 960px; margin: 0 auto; padding: 32px 20px 64px; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 18px; margin: 0; }
h3 { font-size: 13px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 22px 0 8px; }
.sub { color: var(--muted); margin: 0 0 24px; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin: 0 0 20px; }
.row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.chip { display: inline-block; font-size: 12px; font-weight: 600; padding: 2px 9px; border-radius: 999px; white-space: nowrap; }
.pass { color: var(--pass); background: var(--pass-bg); }
.fail { color: var(--fail); background: var(--fail-bg); }
.warn { color: var(--warn); background: var(--warn-bg); }
.info { color: var(--info); background: var(--info-bg); }
table { width: 100%; border-collapse: collapse; }
td, th { text-align: left; padding: 8px 6px; border-bottom: 1px solid var(--border); vertical-align: top; }
th { font-size: 12px; color: var(--muted); font-weight: 600; }
code, pre { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; }
code { background: var(--code-bg); padding: 1px 5px; border-radius: 4px; }
pre { background: var(--code-bg); padding: 12px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; margin: 6px 0 0; }
.verdict { border: 1px solid var(--border); border-radius: 8px; padding: 14px; margin: 0 0 12px; }
.compare { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0; }
@media (max-width: 600px) { .compare { grid-template-columns: 1fr; } }
.compare div { background: var(--code-bg); border-radius: 6px; padding: 8px 10px; }
.label { display: block; font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin-bottom: 2px; }
.reasoning { margin: 8px 0 0; }
.meter { display: inline-block; width: 70px; height: 6px; background: var(--border); border-radius: 3px; vertical-align: middle; overflow: hidden; }
.meter span { display: block; height: 100%; background: var(--pass); }
details { margin: 10px 0 0; }
summary { cursor: pointer; color: var(--info); font-weight: 600; }
.muted { color: var(--muted); }
ul { margin: 6px 0 0; padding-left: 20px; }
"""

STATUS_CHIP = {"pass": ("pass", "Passed"), "warn": ("warn", "Passed with warnings"), "fail": ("fail", "Failed")}
VERDICT_CHIP = {"pass": "pass", "warn": "warn", "fail": "fail"}


def e(value):
    return html.escape(str(value))


def j(value):
    return e(json.dumps(value, ensure_ascii=False))


def chip(status, text=None):
    css, default = STATUS_CHIP.get(status, ("info", status))
    return f'<span class="chip {css}">{e(text or default)}</span>'


def load_doc_detective(output_dir):
    files = sorted(glob.glob(os.path.join(output_dir, "testResults-*.json")))
    if not files:
        return []
    data = json.load(open(files[-1], encoding="utf-8"))
    tests = []
    for spec in data.get("specs", []):
        for test in spec.get("tests", []):
            steps = [s for c in test.get("contexts", []) for s in c.get("steps", [])]
            failed = [s for s in steps if s.get("result") == "FAIL"]
            tests.append({
                "test_id": test["testId"],
                "status": "pass" if test.get("result") == "PASS" else "fail",
                "steps": len(steps),
                "failed": [s.get("description") or next((k for k in s if k in ACTIONS), "step") for s in failed],
                "failed_reason": [s.get("resultDescription", "") for s in failed],
                "is_code": any("runShell" in s for s in steps),
            })
    return tests


ACTIONS = {"goTo", "find", "click", "type", "runShell", "runCode", "httpRequest", "checkLink", "screenshot", "wait"}


def render_code_test(record):
    out = [f'<section class="card" id="{e(record["test_id"])}">']
    out.append(f'<div class="row"><h2>{e(record["test_id"])}</h2>{chip(record.get("status", "fail"))}</div>')
    if record.get("overall"):
        out.append(f'<p class="muted" style="margin:6px 0 0">Docs output vs <code>parsed_document</code>: {e(record["overall"])}</p>')
    out.append(f'<p class="muted" style="margin:4px 0 0">Example document: <a href="{e(record["document_url"])}">{e(os.path.basename(record["document_url"]))}</a></p>')
    if record.get("status") == "fail" and record.get("message"):
        out.append(f'<h3>Failure</h3><pre>{e(record["message"])}</pre>')

    fields = record.get("llm_fields", [])
    out.append("<h3>LLM fields</h3>")
    if fields:
        out.append('<table><tr><th>Field</th><th>Extraction prompt</th><th>Result</th></tr>')
        for f in fields:
            if f["judged"]:
                worst = "fail" if any(x["verdict"] == "fail" for x in f["judged"]) else "warn" if any(x["verdict"] == "warn" for x in f["judged"]) else "pass"
                result = f'<span class="chip {VERDICT_CHIP[worst]}">Judged: {e(worst)}</span>'
            else:
                result = '<span class="chip info">Identical to the docs</span>'
            note = ' <span class="muted">(fallback chain with a layout field)</span>' if f["kind"] == "fallback" else ""
            out.append(f'<tr><td><code>{e(f["field"])}</code>{note}</td><td>{e(f["prompt"]) or "<span class=muted>none</span>"}</td><td>{result}</td></tr>')
        out.append("</table>")
    else:
        out.append('<p class="muted">None in the documented output.</p>')

    layout = record.get("layout")
    if layout:
        out.append("<h3>Layout fields</h3>")
        if layout["mismatches"]:
            out.append(f'<p>{chip("fail", str(len(layout["mismatches"])) + " mismatch(es)")} compared exactly:</p><ul>')
            out += [f"<li><code>{e(m)}</code></li>" for m in layout["mismatches"]]
            out.append("</ul>")
        else:
            out.append(f'<p>{layout["fields"]} field(s), all an exact match.</p>')

    notes = record.get("not_checked", [])
    left = record.get("left_out", {})
    if notes or left.get("fields") or left.get("nested_keys"):
        out.append("<h3>Not compared</h3><ul>")
        out += [f"<li>Marked <code>...</code> in the docs: <code>{e(n)}</code></li>" for n in notes]
        if left.get("fields"):
            out.append(f'<li>In <code>parsed_document</code> but not in the docs: {", ".join(f"<code>{e(k)}</code>" for k in left["fields"])}</li>')
        if left.get("nested_keys"):
            out.append(f'<li>{left["nested_keys"]} nested key(s) in <code>parsed_document</code> that the docs leave out</li>')
        out.append("</ul>")

    judge = record.get("judge")
    if judge:
        out.append(f'<h3>Judge reasoning <span class="muted" style="text-transform:none;letter-spacing:0">({e(judge["model"])})</span></h3>')
        for f in fields:
            for v in f["judged"]:
                pct = max(0, min(100, round(v["confidence"] * 100)))
                out.append(
                    f'<div class="verdict"><div class="row"><code>{e(v["path"])}</code>'
                    f'<span class="chip {VERDICT_CHIP[v["verdict"]]}">{e(v["verdict"].upper())}</span>'
                    f'<span class="muted">match: {e(v["match"])}, confidence {v["confidence"]:.2f}</span>'
                    f'<span class="meter"><span style="width:{pct}%"></span></span></div>'
                    f'<div class="compare"><div><span class="label">Docs show</span><code>{j(v["documented"])}</code></div>'
                    f'<div><span class="label">Sensible returned</span><code>{j(v["actual"])}</code></div></div>'
                    f'<p class="reasoning">{e(v["reasoning"])}</p></div>'
                )
        raw = judge.get("raw_output", "")
        try:
            raw = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            pass
        out.append(
            f'<details><summary>Full prompt the judge received</summary>'
            f'<span class="label" style="margin-top:10px">System</span><pre>{e(judge["system_prompt"])}</pre>'
            f'<span class="label" style="margin-top:10px">User</span><pre>{e(judge["user_prompt"])}</pre></details>'
            f'<details><summary>Full judge output (JSON)</summary><pre>{e(raw)}</pre></details>'
        )
    out.append("</section>")
    return "\n".join(out)


def render(output_dir):
    dd_tests = load_doc_detective(output_dir)
    records = {}
    for path in sorted(glob.glob(os.path.join(output_dir, "examples", "*.json"))):
        record = json.load(open(path, encoding="utf-8"))
        records[record["test_id"]] = record

    statuses = [t["status"] for t in dd_tests] + [r.get("status", "fail") for r in records.values()]
    overall = "fail" if "fail" in statuses else "warn" if "warn" in statuses else "pass"
    source = next((r["file"] for r in records.values()), "")

    out = [
        "<!doctype html><html lang=en><head><meta charset=utf-8>",
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>Doc Detective report</title><style>{CSS}</style></head><body><main>",
        f'<div class="row"><h1>Doc Detective report</h1>{chip(overall, "All tests passed" if overall == "pass" else None)}</div>',
        f'<p class="sub">{e(source)} · {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>',
        '<section class="card"><h2>Tests</h2><table><tr><th>Test</th><th>Type</th><th>Result</th><th>Details</th></tr>',
    ]
    for t in dd_tests:
        record = records.get(t["test_id"])
        status = record.get("status", t["status"]) if record else t["status"]
        if t["is_code"]:
            details = f'<a href="#{e(t["test_id"])}">Comparison and judge reasoning</a>' if record else "No record"
            kind = "Code sample"
        else:
            details = f'{t["steps"]} steps' + ("".join(f'<br>Failed: {e(n)} — {e(r)}' for n, r in zip(t["failed"], t["failed_reason"])))
            kind = "App UI"
        out.append(f'<tr><td><code>{e(t["test_id"])}</code></td><td>{kind}</td><td>{chip(status)}</td><td>{details}</td></tr>')
    for test_id, record in records.items():
        if not any(t["test_id"] == test_id for t in dd_tests):
            out.append(f'<tr><td><code>{e(test_id)}</code></td><td>Code sample</td><td>{chip(record.get("status", "fail"))}</td><td><a href="#{e(test_id)}">Comparison and judge reasoning</a></td></tr>')
    out.append("</table></section>")
    out += [render_code_test(r) for r in records.values()]
    out.append("</main></body></html>")
    path = os.path.join(output_dir, "report.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return path


if __name__ == "__main__":
    print(f"Wrote {render(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT)}")
