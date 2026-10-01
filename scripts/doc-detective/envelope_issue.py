#!/usr/bin/env python3
"""Decide what the regression-envelope issue should say after a run.

Reads the code-test records that run_examples.py writes to <output dir>/examples/ and prints
JSON: {"state", "fingerprint", "body"}.

- state "attention": a test is outside its envelope, or its baseline is stale or missing.
  The workflow opens the doc-detective-envelope issue, or comments on it if the fingerprint
  differs from the last one posted (so a repeated breach doesn't re-post every run).
- state "clear": every baseline exists, is current, and the run is within it. The workflow
  closes the issue if one is open.
- state "none": no test has LLM fields, so there's nothing to report.

Usage: envelope_issue.py <output dir> [--run-url URL]
"""

import argparse
import glob
import hashlib
import json
import os
import re
import sys

MARKER = "envelope-fingerprint"


def field_of(slot):
    return re.split(r"[.\[#]", slot, 1)[0]


def judge_note(record, field):
    for f in record.get("llm_fields", []):
        if f["field"] == field:
            if not f["judged"]:
                return "matched the docs exactly"
            verdicts = {j["verdict"] for j in f["judged"]}
            if "fail" in verdicts:
                return "**judge failed it**: see the doc-detective failure issue"
            if "warn" in verdicts:
                return "judge was unsure (warning)"
            return "**judge passed it**: the feature's behavior likely changed"
    return "not in the documented output"


def decide(records, run_url=None):
    problems = []
    for record in records:
        env = record.get("envelope")
        if not env:
            continue
        test_id = record["test_id"]
        if env["status"] == "missing":
            problems.append((test_id, None, "no baseline yet", None))
        elif env["status"] == "stale":
            problems.append((test_id, None, f"baseline is stale: the config changed since {env['built']}", None))
        elif env["status"] == "outside":
            for slot, reasons in sorted(env["breaches"].items()):
                for reason in reasons:
                    problems.append((test_id, slot, reason, judge_note(record, field_of(slot))))
    if not any(r.get("envelope") for r in records):
        return {"state": "none", "fingerprint": "", "body": ""}
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
    for test_id in sorted({p[0] for p in problems}):
        lines.append(f"### `{test_id}`")
        lines.append("")
        for _, slot, reason, note in (p for p in problems if p[0] == test_id):
            lines.append(f"- `{slot}`: {reason} ({note})" if slot else f"- {reason}")
        lines.append("")
        lines.append(
            f"If the new output is acceptable, rebuild the baseline and commit it: "
            f"`python3 scripts/doc-detective/run_examples.py --file \"{next(r['file'] for r in records if r['test_id'] == test_id)}\" "
            f"--test {test_id} --build-envelope 10`. If it isn't, report it to engineering."
        )
        lines.append("")
    lines.append(f"<!-- {MARKER}: {fingerprint} -->")
    return {"state": "attention", "fingerprint": fingerprint, "body": "\n".join(lines)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    parser.add_argument("--run-url")
    args = parser.parse_args()
    records = []
    for path in sorted(glob.glob(os.path.join(args.output_dir, "examples", "*.json"))):
        with open(path, encoding="utf-8") as f:
            records.append(json.load(f))
    print(json.dumps(decide(records, args.run_url)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
