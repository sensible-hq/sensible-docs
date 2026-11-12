"""Output claim (the default): the page's documented output is what Sensible extracts.

Uploads the page's config as written, extracts the example document (or a blank page, when the test
names none), and compares the documented output with parsed_document, plus a top-level
"postprocessorOutput" when the config has a postprocessor (sensible.actual_output, compare.py). Values
that LLM methods produced and that differ go to the judge (judge.py); everything else must match
exactly. Then checks the LLM fields against the regression envelope (envelope.py), whatever the outcome.

    {/* code test {"testId": "...", "description": "..."} */}
    {/* inline document */}
    {/* inline config */}
    {/* inline output */}
    {/* code test end */}

The judge fails closed: if it can't decide, the test fails as JUDGE_ERROR, never passes. The envelope
never changes a verdict; it informs triage.
"""

import json
import os
import sys

from .. import compare, envelope, fields, jsonish, markup, record, samples, settings
from .. import judge as judge_module
from ..errors import (
    DOCS_MALFORMED, ENVELOPE_INVALID, JUDGE_ERROR, JUDGE_UNAVAILABLE, LLM_DRIFT, OUTPUT_DRIFT, CodeTestError,
)
from ..reports.parts import JUDGE, VERDICT_CHIP, chip, e, j
from .common import check_document, require_no_portfolio

NAME = "output"
LABEL = "documented output"
RECORD_KEY = None  # fills the record's top-level overall, layout, llm_fields, judge, envelope, and editor
# The test's sample doc type runs whichever config fits best if a fingerprint fails, as the shared one did
DOC_TYPE_SCHEMA = {"fingerprint_mode": "fallback_to_all"}


def parse_expect(options, test_id, where):
    raise CodeTestError(DOCS_MALFORMED, f"{test_id}: an output test has no <!-- expect -->; it compares the <!-- inline output --> ({where})")


def validate(test, seen, where):
    if "document" not in seen and (test.segment_documents_with or test.fixtures or test.inline_configs):
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: missing <!-- inline document --> ({where}). Only a test that compares an "
                            f"inline output can leave it out and run on a blank page")
    require_no_portfolio(test, where)
    missing = {"config", "output"} - seen
    if missing:
        raise CodeTestError(DOCS_MALFORMED, f"{test.test_id}: missing <!-- inline {'/'.join(sorted(missing))} --> ({where})")
    if "document" not in seen:
        # An example that doesn't read its document: run it on a blank page
        test.document_url, test.blank_document = settings.BLANK_DOCUMENT_URL, True


def check(test):
    """(config, documented output). Configs may have comments and trailing commas (Sensible accepts
    them). Output blocks may have comments and `...`, but not trailing commas (Sensible never outputs them)."""
    config = markup.parse_block(test, "config", test.config, test.config_line, test.config_shift, True)
    output = markup.parse_block(test, "output", test.output, test.output_line, 0, False)
    return config, output


def _claim(test_index, expected, actual, diff):
    key, _ = test_index.owner(diff.path)
    field_path = compare.typed_field_path(expected, diff.path)
    actual_field = compare.value_at(actual, field_path)
    return {
        "field": key,
        "path": compare.format_path(diff.path),
        "prompt": test_index.llm[key],
        "type": test_index.type_for(diff.path, expected),
        "documented": diff.expected,
        "actual": None if diff.actual is compare.MISSING else diff.actual,
        "documented_field": compare.value_at(expected, field_path),
        "actual_field": None if actual_field is compare.MISSING else actual_field,
    }


def check_envelope(rec, test, actual, index):
    """Compare this run's LLM fields with the saved baseline, and record the result."""
    if not index.llm:
        return
    try:
        baseline = envelope.load(test.test_id)
    except envelope.EnvelopeInvalid as e:
        raise CodeTestError(ENVELOPE_INVALID, f"{os.path.relpath(envelope.path(test.test_id))} isn't a valid envelope: {e}. Rebuild it with --build-envelope")
    if baseline is None:
        rec["envelope"] = {"status": "missing"}
        return
    info = {"runs": baseline["runs"], "built": baseline["built"] + (f", extended {baseline['updated']}" if baseline.get("updated") else "")}
    if baseline["config_sha256"] != envelope.config_hash(test.config):
        rec["envelope"] = {"status": "stale", **info}
        return
    breaches = envelope.check(baseline, envelope.observe_output(actual, index.llm))
    rec["envelope"] = {"status": "outside" if breaches else "within", **info, "breaches": breaches, "slots": baseline["slots"]}
    rec["warnings"] += [{"source": "envelope", "text": f"{slot}: {reason}"} for slot, reasons in breaches.items() for reason in reasons]


def propose_fix(test, fixed_output):
    """Rewrite the test's output block in its page with `fixed_output`. Returns whether it did."""
    if "/*" in test.output or "//" in test.output or jsonish.MARK in test.output or jsonish.has_bare_ellipsis(test.output):
        print("  Not proposing a fix: the output block has comments or is abridged ([...] or ...)", file=sys.stderr)
        return False
    with open(test.file, encoding="utf-8") as f:
        text = f.read()
    start, end = test.output_span
    if text[start:end] != test.output:
        print("  Not proposing a fix: the page changed during the run", file=sys.stderr)
        return False
    with open(test.file, "w", encoding="utf-8") as f:
        f.write(text[:start] + json.dumps(fixed_output, indent=2, ensure_ascii=False) + text[end:])
    return True


def prepare(client, test):
    """Recreate the test's sample doc type with the page's config as written, as configuration <testId>.
    Sensible validates the config on upload, so invalid syntax fails here. Returns (doc type name, the
    SenseML editor opened on the config and the example document)."""
    name = sample_doc_types(test)[0]
    _, reference = samples.create(client, name, test.test_id, test.config, test.document_url, DOC_TYPE_SCHEMA)
    return name, markup.editor_url(name, test.test_id, reference)


def run(rec, test, client, judge=judge_module.judge, judge_key=None, judge_model=None, fix=False):
    config, expected = check(test)
    check_document(client, test.document_url)
    doc_type, rec["editor"] = prepare(client, test)
    actual = client.extract(test.document_url, doc_type, test.test_id, f"ci__{test.test_id}.pdf")

    index = fields.FieldIndex(config)
    found = compare.diffs(expected, actual)
    exact = [d for d in found if not index.is_llm(d.path)]
    to_judge = [d for d in found if index.is_llm(d.path)]
    failures = [compare.describe(d) for d in exact]
    fixable = list(exact)
    judged = []
    judge_error = None

    if to_judge:
        if not judge_key:
            raise CodeTestError(JUDGE_UNAVAILABLE, "LLM fields differ but ANTHROPIC_API_KEY isn't set:\n  " + "\n  ".join(compare.describe(d) for d in found))
        claims = [_claim(index, expected, actual, d) for d in to_judge]
        try:
            exchange = judge(judge_key, claims, judge_model)
            results = exchange["results"]
        except judge_module.JudgeError as e:
            # Fail closed, but record what was sent and still run the envelope, as context for triage
            judge_error, exchange = e, e.exchange
            results = [{"match": "error", "confidence": 0.0, "reasoning": f"The judge errored: {e}", "claim": "", "observed": ""}] * len(claims)
        rec["judge"] = {k: exchange[k] for k in ("model", "system_prompt", "user_prompt", "raw_output")}
        for diff, claim, result in zip(to_judge, claims, results):
            verdict = "error" if judge_error else judge_module.classify(result)
            judged.append(record.judged_entry(
                claim["field"], claim["path"], fields.format_type(claim["type"]), claim["documented"], claim["actual"],
                verdict, result["match"], result["confidence"], result["reasoning"], result.get("claim", ""), result.get("observed", ""),
            ))
            line = f"{compare.describe(diff)}\n    judge ({exchange['model']}): {result['match']}, confidence {result['confidence']:.2f}. {result['reasoning']}"
            if verdict == "fail":
                failures.append(line)
                fixable.append(diff)
            elif verdict == "warn":
                rec["warnings"].append({"source": "judge", "text": line})

    record.summarize(rec, expected, actual, index, exact, judged)
    check_envelope(rec, test, actual, index)
    if judge_error:
        status = rec.get("envelope", {}).get("status")
        context = {"within": "output is within the envelope", "outside": "output is outside the envelope"}.get(status, f"envelope {status or 'not checked'}")
        raise CodeTestError(JUDGE_ERROR, f"{judge_error} ({context})")
    if failures:
        message = "docs output doesn't match the extraction:\n  " + "\n  ".join(failures)
        if fix and propose_fix(test, compare.apply_fixes(expected, fixable)):
            message += f"\n  Proposed fix written to {test.file}"
        raise CodeTestError(OUTPUT_DRIFT if exact else LLM_DRIFT, message)


def sample_doc_types(test):
    """One, named for the page and test, with the test's config as its only config."""
    return [f"{samples.prefix(test.file)}{test.test_id}"]


def probeable(test):
    return not test.blank_document


def shows_document(rec):
    return True


def text(rec):
    if "overall" not in rec:
        return []
    lines = [f"{rec['test_id']}: {rec['overall']}"]
    if rec.get("editor"):
        lines.append(f"  Editor: {rec['editor']}")
    layout = rec["layout"]
    if layout["mismatches"]:
        lines.append(f"  Layout fields: {len(layout['mismatches'])} mismatch(es)")
        lines += [f"    {m}" for m in layout["mismatches"]]
    else:
        lines.append(f"  Layout fields: {layout['fields']}, all exact match" if layout["fields"] else "  Layout fields: none")
    lines += [f"  Not checked (...): {note}" for note in rec["not_checked"]]
    for field in rec["llm_fields"]:
        if any(x["verdict"] == "error" for x in field["judged"]):
            state = "[judge] undecided: the judge errored"
        else:
            state = "[judge] decided" if field["judged"] else "identical to the docs"
        note = " (fallback chain with a layout field)" if field["kind"] == "fallback" else ""
        lines.append(f"  LLM field {field['field']}{note}: {state}")
    if rec.get("judge"):
        lines.append(f"  [judge] {rec['judge']['model']}:")
        for field in rec["llm_fields"]:
            for x in field["judged"]:
                lines.append(f"    [judge] {x['verdict'].upper()}  {x['path']}: {json.dumps(x['documented'], ensure_ascii=False)} -> "
                             f"{json.dumps(x['actual'], ensure_ascii=False)}  ({x['match']}, confidence {x['confidence']:.2f})")
                lines.append(f"      {x['reasoning']}")
    return lines


def html(rec, links):
    out = []
    layout = rec.get("layout")
    if layout:
        out.append("<h3>Layout fields</h3>")
        if layout["mismatches"]:
            out.append(f'<p>{chip("fail", str(len(layout["mismatches"])) + " mismatch(es)")} compared exactly:</p><ul>')
            out += [f"<li><code>{e(m)}</code></li>" for m in layout["mismatches"]]
            out.append("</ul>")
        else:
            out.append(f'<p>{layout["fields"]} field(s), all an exact match.</p>' if layout["fields"] else '<p class="muted">None in the documented output.</p>')

    notes = rec.get("not_checked", [])
    left = rec.get("left_out", {})
    if notes or left.get("fields") or left.get("nested_keys"):
        out.append("<h3>Not compared</h3><ul>")
        out += [f"<li>Marked <code>...</code> in the docs: <code>{e(n)}</code></li>" for n in notes]
        if left.get("fields"):
            out.append(f'<li>In <code>parsed_document</code> but not in the docs: {", ".join(f"<code>{e(k)}</code>" for k in left["fields"])}</li>')
        if left.get("nested_keys"):
            out.append(f'<li>{left["nested_keys"]} nested key(s) in <code>parsed_document</code> that the docs leave out</li>')
        out.append("</ul>")

    llm = rec.get("llm_fields", [])
    if "overall" in rec:
        out.append("<h3>LLM fields</h3>")
        if llm:
            out.append('<table><tr><th>Field</th><th>Type</th><th>Extraction prompt</th><th>Result</th></tr>')
            for f in llm:
                if f["judged"]:
                    verdicts = {x["verdict"] for x in f["judged"]}
                    worst = next(v for v in ("error", "fail", "warn", "pass") if v in verdicts)
                    result = f'{JUDGE} <span class="chip {VERDICT_CHIP[worst]}">{e(worst)}</span>'
                else:
                    result = '<span class="chip info">Identical to the docs</span>'
                note = ' <span class="muted">(fallback chain with a layout field)</span>' if f["kind"] == "fallback" else ""
                out.append(f'<tr><td><code>{e(f["field"])}</code>{note}</td><td><code>{e(f["type"])}</code></td><td>{e(f["prompt"]) or "<span class=muted>none</span>"}</td><td>{result}</td></tr>')
            out.append("</table>")
        else:
            out.append('<p class="muted">None in the documented output.</p>')

    judge = rec.get("judge")
    if llm and not judge and rec.get("overall"):
        out.append('<p class="muted" style="margin:10px 0 0">The judge wasn\'t called: every LLM field matched the docs exactly.</p>')
    if judge:
        out.append(f'<h3>Judge reasoning {JUDGE} <span class="muted" style="text-transform:none;letter-spacing:0">({e(judge["model"])})</span></h3>')
        for f in llm:
            for v in f["judged"]:
                pct = max(0, min(100, round(v["confidence"] * 100)))
                out.append(
                    f'<div class="verdict"><div class="row">{JUDGE}<code>{e(v["path"])}</code>'
                    f'<span class="muted">type <code>{e(v["type"])}</code></span>'
                    f'<span class="chip {VERDICT_CHIP[v["verdict"]]}">{e(v["verdict"].upper())}</span>'
                    f'<span class="muted">match: {e(v["match"])}, confidence {v["confidence"]:.2f}</span>'
                    f'<span class="meter"><span style="width:{pct}%"></span></span></div>'
                    f'<div class="compare"><div><span class="label">Docs show</span><code>{j(v["documented"])}</code></div>'
                    f'<div><span class="label">Sensible returned</span><code>{j(v["actual"])}</code></div></div>'
                    f'<p class="reasoning">{e(v["reasoning"])}</p></div>'
                )
        raw = judge["raw_output"]
        try:
            raw = json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
        except ValueError:
            pass
        out.append(
            f'<details><summary>Full prompt the judge received</summary>'
            f'<span class="label" style="margin-top:10px">System</span><pre>{e(judge["system_prompt"])}</pre>'
            f'<span class="label" style="margin-top:10px">User</span><pre>{e(judge["user_prompt"])}</pre></details>'
            f'<details><summary>Full judge output (JSON)</summary><pre>{e(raw)}</pre></details>'
        )
    return out


def details(test, rec):
    return f"{test.test_id}: output comparison"


def checked(test, rec):
    return f"documented output vs Sensible: {rec['overall']}" if rec.get("overall") else ""
