"""What the doc-detective-envelope issue should say after a run.

decide() returns {"state", "fingerprint", "body"}:
- "attention": a test is outside its envelope, or its baseline is stale or missing. The workflow
  opens the issue, or comments on it if the fingerprint differs from the last one posted (so a
  repeated breach doesn't re-post every run).
- "clear": every baseline exists, is current, and the run is within it. The workflow closes the issue.
- "none": no test has LLM fields, so there's nothing to report.
"""

import hashlib
import json

from . import wording

MARKER = "envelope-fingerprint"


def decide(records, run_url=None):
    if not any(r.get("envelope") for r in records):
        return {"state": "none", "fingerprint": "", "body": ""}
    problems = []  # (test ID, slot or None, reason, judge note or None)
    for record in records:
        env = record.get("envelope")
        if not env:
            continue
        if env["status"] == "missing":
            problems.append((record["test_id"], None, "no baseline yet", None))
        elif env["status"] == "stale":
            problems.append((record["test_id"], None, f"baseline is stale: the config changed since {env['built']}", None))
        elif env["status"] == "outside":
            for slot, reasons in sorted(env["breaches"].items()):
                problems += [(record["test_id"], slot, reason, wording.judge_note(record, wording.field_of(slot))) for reason in reasons]
    if not problems:
        return {"state": "clear", "fingerprint": "", "body": "Back within the regression envelope" + (f" in {run_url}" if run_url else "") + "."}

    fingerprint = hashlib.sha256(json.dumps(sorted(p[:3] for p in problems)).encode()).hexdigest()[:16]
    lines = [
        "Doc Detective's regression envelope flagged LLM fields whose output shifted from their baseline. "
        "Tests still pass: an envelope result is a warning, not a failure.",
        "",
    ]
    if run_url:
        lines += [f"Workflow run: {run_url}", ""]
    files = {r["test_id"]: r["file"] for r in records}
    for test_id in sorted({p[0] for p in problems}):
        lines += [f"### `{test_id}`", ""]
        for _, slot, reason, note in (p for p in problems if p[0] == test_id):
            lines.append(f"- `{slot}`: {reason} ({note})" if slot else f"- {reason}")
        lines += ["", f"If the new output is acceptable, rebuild the baseline and commit it: `{wording.rebuild_command(files[test_id], test_id)}`. "
                      "If it isn't, report it to engineering.", ""]
    lines.append(f"<!-- {MARKER}: {fingerprint} -->")
    return {"state": "attention", "fingerprint": fingerprint, "body": "\n".join(lines)}
