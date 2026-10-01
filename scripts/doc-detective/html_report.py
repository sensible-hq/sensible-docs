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

import envelope_issue

DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

CSS = """
:root {
  --bg: #f7f7f5; --card: #ffffff; --text: #1d1d1b; --muted: #6b6b66; --border: #e3e2dd;
  --code-bg: #f1f0ec; --pass: #1f7a4d; --pass-bg: #e3f3ea; --fail: #b3261e; --fail-bg: #fbe7e5;
  --warn: #8a5a00; --warn-bg: #fdf1d8; --info: #3b4a8a; --info-bg: #e8ebf7;
  --judge: #6a3d9a; --judge-bg: #f1e9fa;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #161615; --card: #1f1f1d; --text: #ecebe6; --muted: #a3a29b; --border: #33332f;
    --code-bg: #262623; --pass: #6fd3a0; --pass-bg: #17322a; --fail: #ff8a80; --fail-bg: #3a1c1a;
    --warn: #f3c46b; --warn-bg: #3a2e14; --info: #a9b6f2; --info-bg: #222a45;
    --judge: #c9a6f0; --judge-bg: #2e2340;
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
.judge { color: var(--judge); background: var(--judge-bg); border: 1px dashed var(--judge); font-weight: 700; letter-spacing: .03em; text-transform: none; }
.envelope { color: var(--info); background: var(--info-bg); border: 1px dashed var(--info); font-weight: 700; letter-spacing: .03em; text-transform: none; }
.disclaimer { border-left: 4px solid var(--judge); background: var(--card); padding: 10px 14px; border-radius: 6px; margin: 0 0 20px; }
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
details.test { margin: 0 0 20px; }
details.test > summary { list-style: none; cursor: pointer; color: var(--text); font-weight: normal; }
details.test > summary::-webkit-details-marker { display: none; }
details.test > summary .row::before { content: "▸"; color: var(--muted); margin-right: 2px; }
details.test[open] > summary .row::before { content: "▾"; }
.toolbar { display: flex; gap: 8px; margin: 0 0 12px; }
.toolbar button { font: inherit; font-size: 13px; padding: 4px 10px; border: 1px solid var(--border); border-radius: 6px; background: var(--card); color: var(--text); cursor: pointer; }
summary { cursor: pointer; color: var(--info); font-weight: 600; }
.muted { color: var(--muted); }
ul { margin: 6px 0 0; padding-left: 20px; }
"""

STATUS_CHIP = {"pass": ("pass", "Passed"), "warn": ("warn", "Passed with warnings"), "fail": ("fail", "Failed")}
VERDICT_CHIP = {"pass": "pass", "warn": "warn", "fail": "fail", "error": "fail"}


def e(value):
    return html.escape(str(value))


def j(value):
    return e(json.dumps(value, ensure_ascii=False))


JUDGE = '<span class="chip judge" title="Probabilistic: decided by an LLM judge">judge</span>'
ENVELOPE = '<span class="chip envelope" title="Compared with a baseline of earlier runs">envelope</span>'
DISCLAIMER = "Every check is deterministic (an exact comparison) unless it's labeled judge. A judge result is probabilistic: an LLM decided it, and the same input can get a different verdict or confidence on another run."


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
                "description": test.get("description", ""),
                "status": "pass" if test.get("result") == "PASS" else "fail",
                "steps": [step_summary(s) for s in steps],
                "failed": len(failed),
                "is_code": any("runShell" in s for s in steps),
            })
    return tests


ACTIONS = {"goTo", "find", "click", "type", "runShell", "runCode", "httpRequest", "checkLink", "screenshot", "wait"}


def step_summary(step):
    """Describe a Doc Detective step: its description, action and target, and result. Never typed text."""
    action = next((k for k in step if k in ACTIONS), "step")
    spec = step.get(action)
    if action == "goTo":
        target = spec.get("url", "") if isinstance(spec, dict) else spec
        what = f"go to {target}"
    elif action == "type":
        what = f"type into {spec.get('selector', 'the focused element')}" if isinstance(spec, dict) else "type"
    elif action in ("find", "click"):
        if isinstance(spec, dict):
            bits = [spec["selector"]] if spec.get("selector") else []
            if spec.get("elementText"):
                bits.append(f'"{spec["elementText"]}"')
            what = f"{action} " + " with text ".join(bits)
        else:
            what = f'{action} "{spec}"'
    elif action == "runShell":
        what = "run the example runner"
    else:
        what = action
    return {
        "description": step.get("description", ""),
        "action": what,
        "result": {"PASS": "pass", "FAIL": "fail"}.get(step.get("result"), "skipped"),
        "message": step.get("resultDescription", ""),
        "seconds": round(step.get("durationMs", 0) / 1000, 1),
    }


def render_ui_test(test):
    out = [f'<details class="card test" id="{e(test["test_id"])}"{" open" if test["status"] != "pass" else ""}>']
    out.append(f'<summary><div class="row"><h2>{e(test["test_id"])}</h2>{chip(test["status"])}<span class="muted">App UI · {len(test["steps"])} steps</span></div></summary>')
    if test["description"]:
        out.append(f'<p class="muted" style="margin:6px 0 0">{e(test["description"])}</p>')
    out.append('<h3>Steps</h3><table><tr><th>#</th><th>Step</th><th>Action</th><th>Result</th></tr>')
    for i, s in enumerate(test["steps"], 1):
        css = {"pass": "pass", "fail": "fail"}.get(s["result"], "info")
        message = f'<br><span style="color:var(--fail)">{e(s["message"])}</span>' if s["result"] == "fail" else ""
        out.append(
            f'<tr><td class="muted">{i}</td><td>{e(s["description"]) or "<span class=muted>no description</span>"}{message}</td>'
            f'<td><code>{e(s["action"])}</code></td><td><span class="chip {css}">{e(s["result"])}</span> <span class="muted">{s["seconds"]}s</span></td></tr>'
        )
    out.append("</table></details>")
    return "\n".join(out)


def render_envelope(env, record=None):
    if not env:
        return ""
    out = [
        f"<h3>Regression envelope {ENVELOPE}</h3>",
        '<p class="muted" style="margin:0 0 8px">What this checks: whether each LLM field\'s output still looks like it did across the '
        'baseline runs (format, type, unit, value and length ranges, null rate, confidence signal). It\'s independent of the docs and of '
        'the judge: the judge asks whether the docs are still right; the envelope asks whether the product\'s behavior shifted. '
        '<b>Within</b> means consistent with earlier runs. <b>Outside</b> means the behavior shifted: if the judge still passed the field, '
        'the docs hold but the feature changed; if the judge failed it, it\'s likely a regression. It never changes a test\'s verdict.</p>',
    ]
    if env["status"] == "missing":
        out.append('<p class="muted">No baseline yet. Build one with <code>run_examples.py --build-envelope 10</code> and commit <code>scripts/doc-detective/envelopes/</code>.</p>')
        return "\n".join(out)
    if env["status"] == "stale":
        out.append(f'<p>{chip("warn", "Stale")} The config changed since the baseline was built ({e(env["built"])}). Rebuild it with <code>--build-envelope</code>.</p>')
        return "\n".join(out)
    if env["status"] == "within":
        out.append(f'<p>{chip("pass", "Within the envelope")} Every LLM field measurement is inside the baseline of {env["runs"]} runs, built {e(env["built"])}.</p>')
    else:
        count = sum(len(r) for r in env["breaches"].values())
        out.append(f'<p>{chip("warn", "Outside the envelope")} {count} measurement(s) fall outside the baseline of {env["runs"]} runs, built {e(env["built"])}.</p><ul>')
        for slot, reasons in env["breaches"].items():
            note = envelope_issue.judge_note(record or {}, envelope_issue.field_of(slot)).replace("**", "")
            out += [f"<li><code>{e(slot)}</code>: {e(reason)} <span class=\"muted\">({e(note)})</span></li>" for reason in reasons]
        out.append("</ul><p class=\"muted\">If the new output is acceptable, rebuild the baseline with <code>--build-envelope 10</code> and commit it. If it isn't, report it to engineering.</p>")
    rows = []
    for slot, s in env.get("slots", {}).items():
        if "count_min" in s:
            measured = f'{s["count_min"]}-{s["count_max"]} items'
        else:
            bits = [f'null {round(s["null_rate"] * 100)}%']
            if s["types"]:
                bits.append("type " + ", ".join(s["types"]))
            if isinstance(s.get("shapes"), list):
                bits.append("formats " + ", ".join(repr(x) for x in s["shapes"]))
            elif s.get("shapes"):
                bits.append("free text")
            if isinstance(s.get("source_shapes"), list):
                bits.append("source formats " + ", ".join(repr(x) for x in s["source_shapes"]))
            if "length_min" in s:
                bits.append(f'length {s["length_min"]}-{s["length_max"]}')
            if "number_min" in s:
                bits.append(f'value {s["number_min"]}-{s["number_max"]}')
            if s["units"]:
                bits.append("unit " + ", ".join(s["units"]))
            if s["confidence_signals"]:
                bits.append("confidence " + ", ".join(s["confidence_signals"]))
            measured = "; ".join(bits)
        rows.append(f"<tr><td><code>{e(slot)}</code></td><td>{e(measured)}</td></tr>")
    if rows:
        out.append('<details><summary>Baseline</summary><table><tr><th>Measurement</th><th>Seen in the baseline runs</th></tr>' + "".join(rows) + "</table></details>")
    return "\n".join(out)


def needs_attention(record):
    """Open a code test's section unless it simply passed: identical, nothing judged, within its envelope."""
    judged = any(f["judged"] for f in record.get("llm_fields", []))
    envelope_ok = record.get("envelope", {}).get("status", "within") == "within"
    return record.get("status") != "pass" or judged or not envelope_ok


def render_code_test(record):
    judged = any(f["judged"] for f in record.get("llm_fields", []))
    env_status = record.get("envelope", {}).get("status")
    badges = (JUDGE if judged else "") + (f' {ENVELOPE} <span class="chip warn">{e(env_status)}</span>' if env_status and env_status != "within" else "")
    out = [f'<details class="card test" id="{e(record["test_id"])}"{" open" if needs_attention(record) else ""}>']
    out.append(f'<summary><div class="row"><h2>{e(record["test_id"])}</h2>{chip(record.get("status", "fail"))}{badges}<span class="muted">Code sample</span></div></summary>')
    if record.get("overall"):
        out.append(f'<p class="muted" style="margin:6px 0 0">Docs output vs <code>parsed_document</code>: {e(record["overall"])}</p>')
    source = f' (the link in <a href="#{e(record["document_from"])}"><code>{e(record["document_from"])}</code></a>)' if record.get("document_from") else ""
    out.append(f'<p class="muted" style="margin:4px 0 0">Example document: <a href="{e(record["document_url"])}">{e(os.path.basename(record["document_url"]))}</a>{source}</p>')
    if record.get("config_fragment"):
        out.append('<p class="muted" style="margin:4px 0 0">Config: an excerpt of one field, run wrapped in <code>{"fields": [ ... ]}</code></p>')
    if record.get("status") == "fail" and record.get("message"):
        out.append(f'<h3>Failure</h3><pre>{e(record["message"])}</pre>')
        rows = envelope_issue.triage_rows(record)
        if rows:
            out.append('<table><tr><th>Field</th><th>Judge</th><th>Envelope</th><th>What it suggests</th></tr>')
            out += [f'<tr><td><code>{e(p)}</code></td><td>{JUDGE} <span class="chip fail">{e(v)}</span></td><td>{ENVELOPE} {e(s)}</td><td>{e(n)}</td></tr>' for p, v, s, n in rows]
            out.append("</table>")

    layout = record.get("layout")
    if layout:
        out.append("<h3>Layout fields</h3>")
        if layout["mismatches"]:
            out.append(f'<p>{chip("fail", str(len(layout["mismatches"])) + " mismatch(es)")} compared exactly:</p><ul>')
            out += [f"<li><code>{e(m)}</code></li>" for m in layout["mismatches"]]
            out.append("</ul>")
        else:
            out.append(f'<p>{layout["fields"]} field(s), all an exact match.</p>' if layout["fields"] else '<p class="muted">None in the documented output.</p>')

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

    fields = record.get("llm_fields", [])
    out.append("<h3>LLM fields</h3>")
    if fields:
        out.append('<table><tr><th>Field</th><th>Type</th><th>Extraction prompt</th><th>Result</th></tr>')
        for f in fields:
            if f["judged"]:
                verdicts = {x["verdict"] for x in f["judged"]}
                worst = next(v for v in ("error", "fail", "warn", "pass") if v in verdicts)
                result = f'{JUDGE} <span class="chip {VERDICT_CHIP[worst]}">{e(worst)}</span>'
            else:
                result = '<span class="chip info">Identical to the docs</span>'
            note = ' <span class="muted">(fallback chain with a layout field)</span>' if f["kind"] == "fallback" else ""
            out.append(f'<tr><td><code>{e(f["field"])}</code>{note}</td><td><code>{e(f.get("type", "string"))}</code></td><td>{e(f["prompt"]) or "<span class=muted>none</span>"}</td><td>{result}</td></tr>')
        out.append("</table>")
    else:
        out.append('<p class="muted">None in the documented output.</p>')

    judge = record.get("judge")
    if fields and not judge and record.get("overall"):
        out.append('<p class="muted" style="margin:10px 0 0">The judge wasn\'t called: every LLM field matched the docs exactly.</p>')
    if judge:
        out.append(f'<h3>Judge reasoning {JUDGE} <span class="muted" style="text-transform:none;letter-spacing:0">({e(judge["model"])})</span></h3>')
        for f in fields:
            for v in f["judged"]:
                pct = max(0, min(100, round(v["confidence"] * 100)))
                out.append(
                    f'<div class="verdict"><div class="row">{JUDGE}<code>{e(v["path"])}</code>'
                    f'<span class="muted">type <code>{e(v.get("type", "string"))}</code></span>'
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
    out.append(render_envelope(record.get("envelope"), record))
    out.append("</details>")
    return "\n".join(out)


def envelope_sentence(records):
    """The envelope part of the disclaimer, naming the baseline size when every baseline agrees."""
    sizes = {r["envelope"]["runs"] for r in records if r.get("envelope", {}).get("runs")}
    baseline = f"an established {sizes.pop()}-result baseline" if len(sizes) == 1 else "an established baseline"
    return f"An envelope result flags an LLM regression against {baseline} of acceptable variance; a result outside the baseline is a warning, not a failure."


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
        f'<p class="disclaimer">{e(DISCLAIMER).replace("labeled judge", "labeled " + JUDGE)} '
        f'{ENVELOPE} {e(envelope_sentence(records.values()))}</p>',
        '<section class="card"><h2>Tests</h2><table><tr><th>Test</th><th>Type</th><th>Description</th><th>Result</th><th>Details</th></tr>',
    ]
    for t in dd_tests:
        record = records.get(t["test_id"])
        status = record.get("status", t["status"]) if record else t["status"]
        if t["is_code"]:
            judged = record and any(f["judged"] for f in record.get("llm_fields", []))
            details = (f'<a href="#{e(t["test_id"])}">Comparison' + (" and judge reasoning</a> " + JUDGE if judged else "</a>")) if record else "No record"
            kind = "Code sample"
        else:
            failed = f', {t["failed"]} failed' if t["failed"] else ""
            details = f'<a href="#{e(t["test_id"])}">{len(t["steps"])} steps{failed}</a>'
            kind = "App UI"
        out.append(f'<tr><td><code>{e(t["test_id"])}</code></td><td>{kind}</td><td>{e(t["description"])}</td><td>{chip(status)}</td><td>{details}</td></tr>')
    for test_id, record in records.items():
        if not any(t["test_id"] == test_id for t in dd_tests):
            out.append(f'<tr><td><code>{e(test_id)}</code></td><td>Code sample</td><td></td><td>{chip(record.get("status", "fail"))}</td><td><a href="#{e(test_id)}">Comparison and judge reasoning</a></td></tr>')
    out.append("</table></section>")
    out.append('<div class="toolbar"><button onclick="document.querySelectorAll(\'details.test\').forEach(d => d.open = true)">Expand all</button>'
               '<button onclick="document.querySelectorAll(\'details.test\').forEach(d => d.open = false)">Collapse all</button>'
               '<span class="muted" style="align-self:center">Sections that passed with nothing to review start collapsed.</span></div>')
    out += [render_ui_test(t) for t in dd_tests if not t["is_code"]]
    out += [render_code_test(r) for r in records.values()]
    # Following a link to a test opens its section
    out.append("<script>function openTarget(){var d=document.getElementById(location.hash.slice(1));if(d&&d.tagName==='DETAILS')d.open=true;}"
               "window.addEventListener('hashchange',openTarget);openTarget();</script>")
    out.append("</main></body></html>")
    path = os.path.join(output_dir, "report.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return path


if __name__ == "__main__":
    print(f"Wrote {render(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT)}")
