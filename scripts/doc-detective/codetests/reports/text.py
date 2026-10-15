"""The plain-text summary code_tests.py prints for each code test (and the failure issue quotes)."""

import json

from . import wording


def summary(record):
    """Lines describing what a code test compared and decided."""
    lines = []
    if "overall" in record:
        lines.append(f"{record['test_id']}: {record['overall']}")
        layout = record["layout"]
        if layout["mismatches"]:
            lines.append(f"  Layout fields: {len(layout['mismatches'])} mismatch(es)")
            lines += [f"    {m}" for m in layout["mismatches"]]
        else:
            lines.append(f"  Layout fields: {layout['fields']}, all exact match" if layout["fields"] else "  Layout fields: none")
        lines += [f"  Not checked (...): {note}" for note in record["not_checked"]]
        for field in record["llm_fields"]:
            if any(j["verdict"] == "error" for j in field["judged"]):
                state = "[judge] undecided: the judge errored"
            else:
                state = "[judge] decided" if field["judged"] else "identical to the docs"
            note = " (fallback chain with a layout field)" if field["kind"] == "fallback" else ""
            lines.append(f"  LLM field {field['field']}{note}: {state}")
        if record.get("judge"):
            lines.append(f"  [judge] {record['judge']['model']}:")
            for field in record["llm_fields"]:
                for j in field["judged"]:
                    lines.append(f"    [judge] {j['verdict'].upper()}  {j['path']}: {json.dumps(j['documented'], ensure_ascii=False)} -> "
                                 f"{json.dumps(j['actual'], ensure_ascii=False)}  ({j['match']}, confidence {j['confidence']:.2f})")
                    lines.append(f"      {j['reasoning']}")
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
