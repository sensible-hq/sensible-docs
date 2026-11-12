"""Run code tests: check the syntax, run the claim, and record it all.

For each code test, its claim kind (codetests/kinds/) checks the syntax before any network call, then
runs the test against Sensible and fills its section of the record (record.py). A failed claim raises
CodeTestError with a category (errors.py); anything else unexpected is recorded as RUNNER_ERROR.
"""

import sys
import traceback

from . import compare, envelope, fields, kinds, markup, record, settings
from . import judge as judge_module
from .errors import ENVELOPE_INVALID, RUNNER_ERROR, CodeTestError


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


def _run(rec, test, client, judge, judge_key, judge_model, fix):
    kinds.of(test).run(rec, test, client, judge=judge, judge_key=judge_key, judge_model=judge_model, fix=fix)


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
    return kinds.of(test).probeable(test)


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
