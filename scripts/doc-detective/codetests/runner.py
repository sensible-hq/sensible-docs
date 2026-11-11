"""Run code tests: extract, compare, judge, check the envelope, and record it all.

For each code test:
  1. Check syntax, before any network call (markup.check_syntax)
  2. Check the example document link resolves, upload the config as written, and extract
  3. Compare the documented output with parsed_document, plus a top-level "postprocessorOutput" when
     the config has a postprocessor (sensible.actual_output, compare.py). Values that LLM methods
     produced and that differ go to the judge (judge.py); everything else must match exactly
  4. Check the LLM fields against the regression envelope (envelope.py), whatever the outcome above
  5. Record what happened (record.py)

The judge fails closed: if it can't decide, the test fails as JUDGE_ERROR, never passes. The
envelope never changes a verdict; it informs triage.
"""

import json
import os
import shlex
import sys
import traceback

from . import compare, envelope, fields, jsonish, markup, record, settings
from . import judge as judge_module
from .errors import (
    CLASSIFICATION_DRIFT, DOCUMENT_UNREACHABLE, ENVELOPE_INVALID, EXTRACTION_ERROR, FINGERPRINT_DRIFT, RUNNER_ERROR, JUDGE_ERROR, JUDGE_UNAVAILABLE, LLM_DRIFT,
    OUTPUT_DRIFT, SEGMENTS_DRIFT, CodeTestError,
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


def run_code_test(test, client, judge=judge_module.judge, judge_key=None, judge_model=None, fix=False):
    """Run one code test. Returns its record; raises nothing (a failure is recorded in it)."""
    rec = record.new(test)
    try:
        _run(rec, test, client, judge, judge_key, judge_model, fix)
        rec["status"] = "warn" if rec["warnings"] else "pass"
    except CodeTestError as e:
        rec.update(status="fail", category=e.category, message=settings.redact(str(e)))
    except Exception as e:  # noqa: BLE001 -- record it, so the report and issue say what broke
        # Messages can echo request headers, so redact keys before recording or printing
        rec.update(status="fail", category=RUNNER_ERROR,
                   message=settings.redact(f"{RUNNER_ERROR}: {type(e).__name__}: {e}"))
        print(settings.redact(traceback.format_exc()), file=sys.stderr)
    return rec


def _run_segments(rec, test, client):
    """Fingerprint claim: run the fixtures as a portfolio and compare page ranges exactly.
    Fingerprinting uses no LLM, so there's no judge and no envelope."""
    _, expected = markup.check_syntax(test)
    status = client.document_status(test.document_url)
    if status != 200:
        raise CodeTestError(DOCUMENT_UNREACHABLE, f"{test.document_url} returned {status}")
    if test.inline_configs:
        return _run_samples(rec, test, client, expected)
    doc_types, editors = [], []
    for name in test.fixtures:
        refs = markup.fixture_references(name)
        doc_type, config_name, restored = client.ensure_fixture(*markup.fixture_files(name), refs)
        doc_types.append(doc_type)
        editors.append({"fixture": name, "url": markup.editor_url(doc_type, config_name, refs[0]["name"])})
        rec["warnings"] += [{"source": "fixture", "text": f"{name}: {w}"} for w in restored]
    extraction_id, documents = client.extract_portfolio(test.document_url, doc_types, f"ci__{test.test_id}")
    actual = sorted([[d.get("configuration"), d["startPage"] + 1, d["endPage"] + 1] for d in documents], key=lambda d: (d[1], d[2]))
    rec["segments"] = {
        "fixtures": list(test.fixtures),
        **({"table": test.table, "row": test.row} if test.row else {}),
        "document_types": doc_types,
        "editors": editors,
        "extraction_id": extraction_id,
        "expected": expected,
        "actual": actual,
    }
    _compare_segments(expected, actual, extraction_id)


def _compare_segments(expected, actual, extraction_id):
    if actual != sorted(expected, key=lambda d: (d[1], d[2])):
        fmt = lambda docs: "; ".join(f"{c} pages {a}-{b}" for c, a, b in docs) or "no documents"
        raise CodeTestError(SEGMENTS_DRIFT, f"the page claims {fmt(expected)}, but Sensible returned {fmt(actual)} (extraction {extraction_id})")


def _run_samples(rec, test, client, expected):
    """Portfolio claim from the page's own samples: each sample's config in a temporary doc type,
    run together as a portfolio. Sensible validates each config on upload, so a sample with invalid
    syntax fails. The temporary doc types are deleted afterwards."""
    types, created = {}, []
    try:
        for sample in test.inline_configs:
            name = f"{settings.TEMP_DOC_TYPE_PREFIX}{test.test_id}__{sample['doc_type']}"
            if name not in types:
                types[name] = client.create_temp_doc_type(name)
                created.append(types[name])
            client.publish_config(types[name], sample["config"], sample["text"])
        extraction_id, documents = client.extract_portfolio(test.document_url, list(types), f"ci__{test.test_id}",
                                                            environment=settings.ENVIRONMENT)
    finally:
        for type_id in created:
            client.delete_temp_doc_type(type_id)
    actual = sorted([[d.get("configuration"), d["startPage"] + 1, d["endPage"] + 1] for d in documents], key=lambda d: (d[1], d[2]))
    rec["segments"] = {
        "fixtures": [],
        "samples": [{"doc_type": s["doc_type"], "config": s["config"]} for s in test.inline_configs],
        "document_types": list(types),
        "extraction_id": extraction_id,
        "expected": expected,
        "actual": actual,
    }
    _compare_segments(expected, actual, extraction_id)


# Replaces a test to break it on purpose: no document has this line
NO_MATCH = {"type": "includes", "text": "docs-ci: a line no document has"}


def _run_fingerprint(rec, test, client):
    """Standalone fingerprint claim: in strict fingerprint mode, Sensible runs a config only if its
    fingerprint passes, so the extraction completes with the config, or FAILS. Runs the page's config
    as written, then each variant with the listed tests replaced by a match no document has."""
    import copy

    config, expect = markup.check_syntax(test)
    status = client.document_status(test.document_url)
    if status != 200:
        raise CodeTestError(DOCUMENT_UNREACHABLE, f"{test.document_url} returned {status}")
    runs, created = [], []
    try:
        for n, variant in enumerate([{"break": [], "passes": expect["passes"]}] + expect["variants"]):
            text = test.config
            if variant["break"]:
                broken = copy.deepcopy(config)
                for i in variant["break"]:
                    broken["fingerprint"]["tests"][i] = NO_MATCH
                text = json.dumps(broken, indent=2)
            name = f"{settings.TEMP_DOC_TYPE_PREFIX}{test.test_id}" + (f"__v{n}" if n else "")
            type_id = client.create_temp_doc_type(name, {"fingerprint_mode": "strict"})
            created.append(type_id)
            client.publish_config(type_id, test.test_id, text)
            result = client.extract_standalone(test.document_url, name, f"ci__{test.test_id}" + (f"__v{n}" if n else ""))
            if result.get("status") == "FAILED" and result.get("errors"):
                # A failing fingerprint fails with no errors; anything else is a different problem
                raise CodeTestError(EXTRACTION_ERROR, f"extraction {result.get('id')} failed: {json.dumps(result.get('errors'))[:300]}")
            passed = result.get("status") == "COMPLETE" and result.get("configuration") == test.test_id
            runs.append({"break": variant["break"], "expected": variant["passes"], "actual": passed, "extraction_id": result.get("id", "")})
    finally:
        for type_id in created:
            client.delete_temp_doc_type(type_id)
    rec["fingerprint"] = {"config": test.test_id, "runs": runs}
    wrong = [r for r in runs if r["actual"] != r["expected"]]
    if wrong:
        say = lambda r: ("as written" if not r["break"] else f"with tests {', '.join(map(str, r['break']))} broken") + \
            f": the page claims it {'passes' if r['expected'] else 'fails'}, but it {'passed' if r['actual'] else 'failed'} (extraction {r['extraction_id']})"
        raise CodeTestError(FINGERPRINT_DRIFT, "; ".join(say(r) for r in wrong))


def curl_command(path, doc_type, content_type, file):
    """The request a classification run sends, as a curl command to run from the repo root. Every value
    from the page is shell-quoted; the key stays an environment variable, never its value."""
    from urllib.parse import urlencode

    url = f"{settings.api()}{path}?{urlencode({'document_types': doc_type})}"
    return (f"curl -s -w '\\nHTTP %{{http_code}}\\n' -X POST {shlex.quote(url)} "
            f'-H "Authorization: Bearer ${settings.sensible_key_var()}" '
            f"-H {shlex.quote('Content-Type: ' + content_type)} --data-binary {shlex.quote('@' + file)}")


def _run_classification(rec, test, client):
    """Classification claim: send each file to the classify endpoint with its content type, restricted
    to the test's fixture doc type, and check whether Sensible classified it as that doc type. The
    fixture's description is what Sensible classifies by. No extraction, no LLM judge (classification
    is the product's own LLM call; its answer is the claim), no envelope."""
    _, expect = markup.check_syntax(test)
    name = test.fixtures[0]
    refs = markup.fixture_references(name)
    doctype_file, config_file = markup.fixture_files(name)
    doc_type, config_name, restored = client.ensure_fixture(doctype_file, config_file, refs)
    rec["warnings"] += [{"source": "fixture", "text": f"{name}: {w}"} for w in restored]
    with open(doctype_file, encoding="utf-8") as f:
        description = (json.load(f).get("schema") or {}).get("description", "")
    runs = []
    for request in expect["requests"]:
        status, text, got = client.classify(markup.request_path(request["file"]), request["content_type"], doc_type)
        runs.append({
            "file": request["file"], "content_type": request["content_type"], "label": request.get("label", ""),
            "expected": request["classified"], "actual": got == doc_type, "http_status": status,
            "response": settings.redact(" ".join(text.split()))[:300],
            "curl": curl_command("/classify", doc_type, request["content_type"], request["file"]),
        })
    rec["classification"] = {
        "fixture": name, "editor": markup.editor_url(doc_type, config_name, refs[0]["name"]),
        "doc_type_description": description, "runs": runs,
    }
    wrong = [r for r in runs if r["actual"] != r["expected"]]
    if wrong:
        say = lambda r: (f"{r['file']} sent as {r['content_type']}: the page claims Sensible "
                         f"{'classifies' if r['expected'] else 'does not classify'} it, but it "
                         f"{'did' if r['actual'] else 'did not'} (HTTP {r['http_status']}: {r['response'][:120]})")
        raise CodeTestError(CLASSIFICATION_DRIFT, "; ".join(say(r) for r in wrong))


def _run(rec, test, client, judge, judge_key, judge_model, fix):
    if test.compare == "classification":
        return _run_classification(rec, test, client)
    if test.compare == "documents":
        return _run_segments(rec, test, client)
    if test.compare == "fingerprint":
        return _run_fingerprint(rec, test, client)
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


PROBE_DETAIL_MAX = 300


def probeable(test):
    """Whether --probe-blank can rerun a test on a blank page: a test that names its own document and
    compares an inline output. Fixture, portfolio, and fingerprint tests need their document."""
    return not test.blank_document and not test.compare


def probe_blank(test, client):
    """Run a test's config on the blank page instead of its document, and compare the output with
    the page's inline output the way a run does. Returns {"testId", "unchanged", "detail"}.

    "unchanged" true means the blank page gave the documented output, so the example doesn't read
    its document. The comparison is compare.diffs alone: LLM values that differ count as changed,
    without asking the judge, so a probe never calls the judge or its API. A probe that couldn't run
    the test reports unchanged false, and "error" with the failure category."""
    entry = {"testId": test.test_id}
    try:
        _, expected = markup.check_syntax(test)
        client.upload_config(test.test_id, test.config)
        try:
            actual = client.extract(settings.BLANK_DOCUMENT_URL, test.test_id, f"ci__{test.test_id}__blank.pdf")
        finally:
            client.delete_config(test.test_id)
        found = compare.diffs(expected, actual)
        if not found:
            entry.update(unchanged=True, detail="the blank page gives the documented output")
        else:
            entry.update(unchanged=False, detail=f"{len(found)} value(s) differ on the blank page, for example {compare.describe(found[0])}")
    except CodeTestError as e:
        entry.update(unchanged=False, detail=f"couldn't probe: {e}", error=e.category)
    except Exception as e:  # noqa: BLE001 -- report it like a run does: redacted, traceback in the log
        entry.update(unchanged=False, detail=f"couldn't probe: {RUNNER_ERROR}: {type(e).__name__}: {e}", error=RUNNER_ERROR)
        print(settings.redact(traceback.format_exc()), file=sys.stderr)
    # Redact before shortening, so a key cut in half can't get past the redaction
    detail = settings.redact(entry["detail"])
    entry["detail"] = detail if len(detail) <= PROBE_DETAIL_MAX else detail[:PROBE_DETAIL_MAX - 3] + "..."
    return entry


def judge_key():
    return settings.key(*settings.JUDGE_KEY_VARS)
