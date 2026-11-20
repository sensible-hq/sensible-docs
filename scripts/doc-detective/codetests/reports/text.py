"""The plain-text summary code_tests.py prints for each code test (and the failure issue quotes)."""

from .. import kinds
from . import wording


def summary(record):
    """Lines describing what a code test compared and decided."""
    lines = []
    if record.get("blank_document"):
        lines.append(f"{record['test_id']}: names no document, so it ran on a blank page")
    lines += kinds.of_record(record).text(record)
    env = record.get("envelope")
    if env:
        prefix = "[envelope] WARNING: " if env["status"] == "outside" else "[envelope] "
        lines.append(f"  {prefix}{wording.envelope_status_line(env)}" + (":" if env["status"] == "outside" else ""))
        for slot, reasons in env.get("breaches", {}).items():
            lines += [f"    {slot}: {reason}" for reason in reasons]
    lines.append(result_line(record))
    return lines


def result_line(record):
    if record["status"] == "fail":
        return f"FAIL {record['test_id']}  {record['message']}"
    counts = {}
    for w in record["warnings"]:
        counts[w["source"]] = counts.get(w["source"], 0) + 1
    sources = ", ".join(f"{n} [{source}]" for source, n in sorted(counts.items()))
    return f"PASS {record['test_id']}" + (f" with warnings: {sources}" if sources else "")
