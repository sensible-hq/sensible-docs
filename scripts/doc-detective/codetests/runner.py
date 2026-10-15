"""Run code tests: extract, compare, judge, check the envelope, and record it all.

For each code test:
  1. Check syntax, before any network call (markup.check_syntax)
  2. Check the example document link resolves, upload the config as written, and extract
  3. Compare the documented output with parsed_document (compare.py). Values that LLM methods
     produced and that differ go to the judge (judge.py); everything else must match exactly
  4. Check the LLM fields against the regression envelope (envelope.py), whatever the outcome above
  5. Record what happened (record.py)

The judge fails closed: if it can't decide, the test fails as JUDGE_ERROR, never passes. The
envelope never changes a verdict; it informs triage.
"""

import json
import os
import sys

from . import compare, envelope, fields, jsonish, markup, record, settings
from . import judge as judge_module
from .errors import (
    DOCUMENT_UNREACHABLE, ENVELOPE_INVALID, JUDGE_ERROR, JUDGE_UNAVAILABLE, LLM_DRIFT, OUTPUT_DRIFT, CodeTestError,
)


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
    if "/*" in test.output or "//" in test.output or jsonish.has_bare_ellipsis(test.output):
        print("  Not proposing a fix: the output block has comments or a bare ...", file=sys.stderr)
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


def run_code_test(test, client, judge=judge_module.judge, judge_key=None, judge_model=None, fix=False):
    """Run one code test. Returns its record; raises nothing (a failure is recorded in it)."""
    rec = record.new(test)
    try:
        _run(rec, test, client, judge, judge_key, judge_model, fix)
        rec["status"] = "warn" if rec["warnings"] else "pass"
    except CodeTestError as e:
        rec.update(status="fail", category=e.category, message=str(e))
    return rec


def _run(rec, test, client, judge, judge_key, judge_model, fix):
    config, expected = markup.check_syntax(test)
    status = client.document_status(test.document_url)
    if status != 200:
        raise CodeTestError(DOCUMENT_UNREACHABLE, f"{test.document_url} returned {status}")
    client.upload_config(test.test_id, test.config)
    try:
        actual = client.extract(test.document_url, test.test_id, f"ci__{test.test_id}.pdf")
    finally:
        # One config in the document type at a time: Sensible can pick any config in it
        client.delete_config(test.test_id)

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


def build_envelope(test, client, runs, extend=False, progress=print):
    """Extract a code test `runs` times and save its LLM fields' baseline, or add the runs to the saved one.
    Returns the saved envelope, or None if the test has no LLM fields."""
    config, _ = markup.check_syntax(test)
    index = fields.FieldIndex(config)
    if not index.llm:
        return None
    existing = None
    if extend:
        try:
            existing = envelope.load(test.test_id)
        except envelope.EnvelopeInvalid as e:
            raise CodeTestError(ENVELOPE_INVALID, f"{test.test_id}: the saved baseline is invalid ({e}); rebuild it with --build-envelope")
        if existing is None:
            raise CodeTestError(ENVELOPE_INVALID, f"{test.test_id}: no baseline to extend; build one with --build-envelope")
        if existing["config_sha256"] != envelope.config_hash(test.config):
            raise CodeTestError(ENVELOPE_INVALID, f"{test.test_id}: the baseline is stale (the config changed); rebuild it with --build-envelope")
    client.upload_config(test.test_id, test.config)
    observations = []
    try:
        for i in range(runs):
            parsed = client.extract(test.document_url, test.test_id, f"ci__{test.test_id}__envelope_{i + 1}.pdf")
            observations.append(envelope.observe_output(parsed, index.llm))
            progress(f"  run {i + 1}/{runs} done")
    finally:
        client.delete_config(test.test_id)
    built = envelope.build(observations, test.config, test.test_id)
    if existing:
        built = envelope.merge(existing, built)
    envelope.save(built)
    return built


def judge_key():
    return settings.key(*settings.JUDGE_KEY_VARS)
