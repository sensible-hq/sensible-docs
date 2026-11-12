"""report.html: a readable report of a page's UI tests and code tests.

Reads the page (for test order and descriptions), Doc Detective's results for UI tests, and the
code-test records. Sections that passed with nothing to review start collapsed.
"""

import os
from .. import envelope, kinds, markup, provenance, settings
from . import wording
from .parts import ENVELOPE, JUDGE, chip, e

CSS = """
:root {
  --bg: #f7f7f5; --card: #ffffff; --text: #1d1d1b; --muted: #6b6b66; --border: #e3e2dd;
  --code-bg: #f1f0ec; --pass: #1f7a4d; --pass-bg: #e3f3ea; --fail: #b3261e; --fail-bg: #fbe7e5;
  --warn: #8a5a00; --warn-bg: #fdf1d8; --info: #3b4a8a; --info-bg: #e8ebf7;
  --judge: #6a3d9a; --judge-bg: #f1e9fa;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #161615; --card: #1f1f1d; --text: #ecebe6; --muted: #a3a29b; --border: #33332f;
    --code-bg: #262623; --pass: #6fd3a0; --pass-bg: #17322a; --fail: #ff8a80; --fail-bg: #3a1c1a;
    --warn: #f3c46b; --warn-bg: #3a2e14; --info: #a9b6f2; --info-bg: #222a45;
    --judge: #c9a6f0; --judge-bg: #2e2340; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #161615; --card: #1f1f1d; --text: #ecebe6; --muted: #a3a29b; --border: #33332f;
  --code-bg: #262623; --pass: #6fd3a0; --pass-bg: #17322a; --fail: #ff8a80; --fail-bg: #3a1c1a;
  --warn: #f3c46b; --warn-bg: #3a2e14; --info: #a9b6f2; --info-bg: #222a45;
  --judge: #c9a6f0; --judge-bg: #2e2340; color-scheme: dark;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--text);
  font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
main { max-width: 960px; margin: 0 auto; padding: 32px 20px 64px; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 18px; margin: 0; }
h3 { font-size: 13px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 22px 0 8px; }
.sub { color: var(--muted); margin: 0 0 24px; }
.card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin: 0 0 20px; overflow-x: auto; }
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
td code { overflow-wrap: anywhere; }
td { overflow-wrap: anywhere; }
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
.toolbar { display: flex; gap: 8px; margin: 0 0 12px; flex-wrap: wrap; }
.toolbar button { font: inherit; font-size: 13px; padding: 4px 10px; border: 1px solid var(--border); border-radius: 6px; background: var(--card); color: var(--text); cursor: pointer; }
summary { cursor: pointer; color: var(--info); font-weight: 600; }
summary:focus-visible, .toolbar button:focus-visible { outline: 2px solid var(--info); outline-offset: 2px; }
.muted { color: var(--muted); }
ul { margin: 6px 0 0; padding-left: 20px; }
"""

def render_ui_test(test, result):
    status = result["status"] if result else "not run"
    steps = result["steps"] if result else []
    if result and len(steps) < test.steps:
        status = "fail"
    out = [f'<details class="card test" id="{e(test.test_id)}"{" open" if status != "pass" else ""}>']
    out.append(f'<summary><div class="row"><h2>{e(test.test_id)}</h2>{chip(status)}<span class="muted">UI test · {len(steps)} steps</span></div></summary>')
    if test.description:
        out.append(f'<p class="muted" style="margin:6px 0 0">{e(test.description)}</p>')
    if not result:
        out.append('<p>Doc Detective didn\'t run this test. Check its <code>&lt;!-- test --&gt;</code> and <code>&lt;!-- step --&gt;</code> comments.</p>')
    else:
        if len(steps) < test.steps:
            out.append(f'<p>{chip("fail", "Steps skipped")} Doc Detective ran {len(steps)} of the {test.steps} steps on the page. '
                       'Check the <code>&lt;!-- step --&gt;</code> comments for an invalid action.</p>')
        out.append('<h3>Steps</h3><table><tr><th>#</th><th>Step</th><th>Action</th><th>Result</th></tr>')
        for i, s in enumerate(steps, 1):
            css = {"pass": "pass", "fail": "fail"}.get(s["result"], "info")
            message = f'<br><span style="color:var(--fail)">{e(s["message"])}</span>' if s["result"] == "fail" else ""
            out.append(
                f'<tr><td class="muted">{i}</td><td>{e(s["description"]) or "<span class=muted>no description</span>"}{message}</td>'
                f'<td><code>{e(s["action"])}</code></td><td><span class="chip {css}">{e(s["result"])}</span> <span class="muted">{s["seconds"]}s</span></td></tr>'
            )
        out.append("</table>")
    out.append("</details>")
    return "\n".join(out)


def render_envelope(env, record):
    if not env:
        return ""
    out = [f"<h3>Regression envelope {ENVELOPE}</h3>", f'<p class="muted" style="margin:0 0 8px">{e(wording.ENVELOPE_PURPOSE)}</p>']
    if env["status"] == "missing":
        out.append(f'<p class="muted">No baseline yet. Build one with <code>--build-envelope {envelope.DEFAULT_RUNS}</code> and commit <code>scripts/doc-detective/envelopes/</code>.</p>')
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
            note = wording.judge_note(record, wording.field_of(slot))
            out += [f'<li><code>{e(slot)}</code>: {e(reason)} <span class="muted">({e(note)})</span></li>' for reason in reasons]
        out.append(f'</ul><p class="muted">If the new output is acceptable, rebuild the baseline with <code>--build-envelope {envelope.DEFAULT_RUNS}</code> and commit it. If it isn\'t, report it to engineering.</p>')
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


def judged(record):
    return any(f["judged"] for f in record.get("llm_fields", []))


def needs_attention(record):
    """Open a code test's section unless it simply passed: identical, nothing judged, within its envelope."""
    return record.get("status") != "pass" or judged(record) or record.get("envelope", {}).get("status", "within") != "within"


class Links:
    """Links from a report to files in the repo, relative to where the report is written, so they open
    from a local checkout. run.sh writes the report in output/ and saves a copy in reports/, a folder at
    the same depth, so the links work from either."""

    def __init__(self, out_path=None):
        self.base = os.path.dirname(os.path.abspath(out_path)) if out_path else settings.OUTPUT_DIR

    def repo(self, path):
        """A repo-relative path, as a link from the report."""
        return os.path.relpath(os.path.join(settings.REPO_ROOT, path), self.base).replace(os.sep, "/")


def render_code_test(record, links=None):
    kind = kinds.of_record(record)
    links = links or Links()
    env_status = record.get("envelope", {}).get("status")
    badges = (JUDGE if judged(record) else "") + (f' {ENVELOPE} <span class="chip warn">{e(env_status)}</span>' if env_status and env_status != "within" else "")
    out = [f'<details class="card test" id="{e(record["test_id"])}"{" open" if needs_attention(record) else ""}>']
    out.append(f'<summary><div class="row"><h2>{e(record["test_id"])}</h2>{chip(record["status"])}{badges}<span class="muted">Code test</span></div></summary>')
    if record.get("overall"):
        out.append(f'<p class="muted" style="margin:6px 0 0">Docs output vs <code>parsed_document</code>: {e(record["overall"])}</p>')
    source = f' (the link in <a href="#{e(record["document_from"])}"><code>{e(record["document_from"])}</code></a>)' if record.get("document_from") else ""
    if record.get("blank_document"):
        out.append(f'<p class="muted" style="margin:4px 0 0">Example document: none, so it ran on <a href="{e(record["document_url"])}">a blank page</a></p>')
    elif kind.shows_document(record):
        out.append(f'<p class="muted" style="margin:4px 0 0">Example document: <a href="{e(record["document_url"])}">{e(os.path.basename(record["document_url"]))}</a>{source}</p>')
    if record.get("config_fragment"):
        out.append('<p class="muted" style="margin:4px 0 0">Config: an excerpt of one field, run wrapped in <code>{"fields": [ ... ]}</code></p>')
    if record["status"] == "fail":
        out.append(f'<h3>Failure</h3><pre>{e(record["message"])}</pre>')
        rows = wording.triage_rows(record)
        if rows:
            out.append('<table><tr><th>Field</th><th>Judge</th><th>Envelope</th><th>What it suggests</th></tr>')
            out += [f'<tr><td><code>{e(p)}</code></td><td>{JUDGE} <span class="chip fail">{e(v)}</span></td><td>{ENVELOPE} {e(s)}</td><td>{e(n)}</td></tr>' for p, v, s, n in rows]
            out.append("</table>")
    out += kind.html(record, links)
    out.append(render_envelope(record.get("envelope"), record))
    out.append("</details>")
    return "\n".join(out)


def details_label(test, rec):
    """Link text for a test's details, unique to the test: what it checked, not a generic word."""
    return kinds.of_record(rec).details(test, rec)


def render_usage(usage):
    """The test account's Sensible usage: this run, and the month to date (from Sensible, after the run)."""
    if not usage:
        return ""
    parts = []
    run = usage.get("run")
    if run:
        calls = sorted((run.get("by_call") or {}).items(), key=lambda kv: -kv[1])
        breakdown = ('<details style="margin:2px 0 0"><summary style="font-weight:normal">Requests by call</summary><ul>'
                     + "".join(f"<li><code>{e(c)}</code>: {n}</li>" for c, n in calls) + "</ul></details>") if calls else ""
        parts.append(f'<div>This run: {run["extractions"]} extraction(s), at least {run["requests"]} API request(s).{breakdown}</div>')
    month, budget = usage.get("month"), usage.get("budget")
    if month:
        line = (f'<div>Test account since {e(month["since"])}: {month["extractions"]} extraction(s), {month["charged"]} charged '
                f'({month["test_runs"]} from test runs, named <code>ci__…</code>; {month["other"]} other). '
                '<span title="Sensible charges a single-document extraction once, and a portfolio extraction once per document it returns (at least once), so charged can exceed extractions.">Why charged ≥ extractions?</span>')
        if budget:
            state = "fail" if month["charged"] >= budget else "warn" if month["charged"] >= 0.8 * budget else "pass"
            line += f' {chip(state, f"{month["charged"]} of {budget} monthly extraction budget")}'
        parts.append(line + "</div>")
    elif usage.get("error"):
        parts.append(f'<div>Test account usage this month: unavailable ({e(usage["error"])}).</div>')
    if not parts:
        return ""
    return '<div class="muted" style="margin:-16px 0 20px;display:grid;gap:4px">' + "".join(parts) + "</div>"


def render(page_path, ui_results, records, out_path, usage=None):
    """Write report.html for one page."""
    page = markup.parse_page(page_path)
    by_id = {r["test_id"]: r for r in records}
    statuses = ["fail" if t.test_id not in ui_results or len(ui_results[t.test_id]["steps"]) < t.steps else ui_results[t.test_id]["status"] for t in page.ui_tests]
    statuses += [by_id[t]["status"] if t in by_id else "fail" for t in page.code_tests]
    overall = "fail" if "fail" in statuses else "warn" if "warn" in statuses else "pass"
    shown_path = os.path.relpath(page_path) if os.path.isabs(page_path) else page_path
    links = Links(out_path)

    out = [
        "<!doctype html><html lang=en><head><meta charset=utf-8>",
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>Docs tests: {e(os.path.basename(page_path))}</title><style>{CSS}</style></head><body><main>",
        f'<div class="row"><h1>Docs tests: {e(os.path.basename(page_path))}</h1>{chip(overall, "All tests passed" if overall == "pass" else None)}</div>',
        f'<p class="sub">{e(shown_path)} · {e(provenance.describe(provenance.for_run(os.path.dirname(out_path), page_path)))}</p>',
        render_usage(usage),
        f'<p class="disclaimer">{e(wording.judge_disclaimer()).replace("labeled judge", "labeled " + JUDGE)} '
        f'{ENVELOPE} {e(wording.envelope_sentence(records))}</p>',
        '<section class="card"><h2>Tests</h2><table><tr><th>Test</th><th>Type</th><th>Description</th><th>Result</th><th>Details</th></tr>',
    ]
    rows = [(t.line, "ui", t) for t in page.ui_tests] + [(t.line, "code", t) for t in page.code_tests.values()]
    for _, kind, test in sorted(rows, key=lambda r: r[0]):
        if kind == "ui":
            result = ui_results.get(test.test_id)
            status = result["status"] if result else "not run"
            if result and len(result["steps"]) < test.steps:
                status = "fail"
            failed = f', {result["failed"]} failed' if result and result["failed"] else ""
            details = f'<a href="#{e(test.test_id)}">{e(test.test_id)}: {len(result["steps"]) if result else 0} steps{failed}</a>'
            label = "UI test"
        else:
            rec = by_id.get(test.test_id)
            status = rec["status"] if rec else "not run"
            details = (f'<a href="#{e(test.test_id)}">{e(details_label(test, rec))}' + (" and judge reasoning</a> " + JUDGE if judged(rec) else "</a>")) if rec else "Not run"
            label = "Code test"
        out.append(f'<tr><td><code>{e(test.test_id)}</code></td><td>{label}</td><td>{e(test.description)}</td><td>{chip(status)}</td><td>{details}</td></tr>')
    out.append("</table></section>")
    out.append('<div class="toolbar"><button type="button" data-open="1">Expand all</button><button type="button" data-open="0">Collapse all</button>'
               '<span class="muted" style="align-self:center">Sections that passed with nothing to review start collapsed.</span></div>')
    for _, kind, test in sorted(rows, key=lambda r: r[0]):
        if kind == "ui":
            out.append(render_ui_test(test, ui_results.get(test.test_id)))
        elif test.test_id in by_id:
            out.append(render_code_test(by_id[test.test_id], links))
    out.append("<script>"
               "document.querySelectorAll('.toolbar button').forEach(function(b){b.addEventListener('click',function(){"
               "document.querySelectorAll('details.test').forEach(function(d){d.open=b.dataset.open==='1';});});});"
               # Following a details link opens only that section, so the eye can follow where the link went
               "function openTarget(){var d=document.getElementById(location.hash.slice(1));if(!d||d.tagName!=='DETAILS')return;"
               "document.querySelectorAll('details.test').forEach(function(x){x.open=(x===d);});d.scrollIntoView({block:'start'});}"
               "document.querySelectorAll('a[href^=\"#\"]').forEach(function(a){a.addEventListener('click',function(){setTimeout(openTarget,0);});});"
               "window.addEventListener('hashchange',openTarget);openTarget();</script>")
    out.append("</main></body></html>")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    return out_path
