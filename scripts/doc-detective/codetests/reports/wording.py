"""Wording shared by every report, so the text summary, issues, and HTML report say the same thing."""

import re

from .. import envelope

CODE_TESTS_CLI = "python3 scripts/doc-detective/code_tests.py"

JUDGE_DISCLAIMER = (
    "Every check is deterministic (an exact comparison) unless it's labeled {judge}. A judge result is "
    "probabilistic: an LLM decided it, and the same input can get a different verdict or confidence on another run."
)

ENVELOPE_PURPOSE = (
    "What this checks: whether each LLM field's output still looks like it did across the baseline runs (format, "
    "type, unit, value and length ranges, null rate, confidence signal). It's independent of the docs and of the "
    "judge: the judge asks whether the docs are still right; the envelope asks whether the product's behavior "
    "shifted. Within means consistent with earlier runs. Outside means the behavior shifted: if the judge still "
    "passed the field, the docs hold but the feature changed; if the judge failed it, it's likely a regression. "
    "It never changes a test's verdict."
)

TRIAGE = {
    ("fail", "outside"): "Something new: the product now returns output it never did in the baseline. Likely a regression: report it to engineering.",
    ("fail", "within"): "The product returns this within its normal variation, so the docs claim something the feature doesn't reliably deliver. Fix the docs (for example, mark the value `...`).",
    ("error", "outside"): "The judge couldn't decide, and the output shifted from the baseline. Fix the judge problem (see the error) and investigate the output now.",
    ("error", "within"): "The judge couldn't decide, but the output looks like earlier runs, so the product probably didn't change. Fix the judge problem (see the error) and rerun.",
}
NO_BASELINE = f"No usable baseline to compare with, so it's unclear whether this is new. Rebuild the baseline with --build-envelope {envelope.DEFAULT_RUNS}."


def judge_disclaimer(judge_label="judge"):
    return JUDGE_DISCLAIMER.format(judge=judge_label)


def envelope_sentence(records):
    """The envelope part of the disclaimer, naming the baseline size when every baseline agrees."""
    sizes = {r["envelope"]["runs"] for r in records if r.get("envelope", {}).get("runs")}
    baseline = f"an established {sizes.pop()}-result baseline" if len(sizes) == 1 else "an established baseline"
    return f"An envelope result flags an LLM regression against {baseline} of acceptable variance; a result outside the baseline is a warning, not a failure."


def rebuild_command(file, test_id):
    return f'{CODE_TESTS_CLI} --file "{file}" --test {test_id} --build-envelope {envelope.DEFAULT_RUNS}'


def field_of(slot):
    """The LLM field an envelope slot belongs to: "vehicles[*].make" -> "vehicles"."""
    return re.split(r"[.\[#]", slot, 1)[0]


def judge_note(record, field):
    """What the judge made of a field, for an envelope breach on it."""
    for f in record.get("llm_fields", []):
        if f["field"] == field:
            if not f["judged"]:
                return "matched the docs exactly"
            verdicts = {j["verdict"] for j in f["judged"]}
            if "error" in verdicts:
                return "the judge errored: see the doc-detective failure issue"
            if "fail" in verdicts:
                return "judge failed it: see the doc-detective failure issue"
            if "warn" in verdicts:
                return "judge was unsure (warning)"
            return "judge passed it: the feature's behavior likely changed"
    return "not in the documented output"


def field_envelope_state(record, field):
    """"outside", "within", "stale", "missing", or "not checked" for one field."""
    env = record.get("envelope") or {}
    status = env.get("status")
    if status in ("within", "outside"):
        return "outside" if any(field_of(slot) == field for slot in env.get("breaches", {})) else "within"
    return status or "not checked"


def triage_rows(record):
    """(path, verdict, envelope state, suggestion) for each value the judge failed or couldn't decide."""
    rows = []
    for f in record.get("llm_fields", []):
        for j in f["judged"]:
            if j["verdict"] in ("fail", "error"):
                state = field_envelope_state(record, f["field"])
                note = NO_BASELINE if state in ("stale", "missing", "not checked") else TRIAGE.get((j["verdict"], state), "")
                rows.append((j["path"], j["verdict"], state, note))
    return rows


def envelope_status_line(env):
    """One line for a record's envelope result."""
    if env["status"] == "missing":
        return f"no baseline yet: build one with --build-envelope {envelope.DEFAULT_RUNS} and commit envelopes/"
    if env["status"] == "stale":
        return f"baseline is stale (the config changed since {env['built']}): rebuild it"
    if env["status"] == "within":
        return f"within the baseline of {env['runs']} runs ({env['built']})"
    return f"outside the baseline of {env['runs']} runs ({env['built']})"
