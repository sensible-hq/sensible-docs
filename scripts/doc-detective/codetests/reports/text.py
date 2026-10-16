"""The plain-text summary code_tests.py prints for each code test (and the failure issue quotes)."""

import json

from . import wording


def summary(record):
    """Lines describing what a code test compared and decided."""
    lines = []
    seg = record.get("segments")
    if seg:
        fmt = lambda docs: "; ".join(f"{c} pages {s}-{e}" for c, s, e in docs) or "no documents"
        lines.append(f"{record['test_id']}: portfolio segments (fingerprints, compared exactly)" + (f", table {seg.get('table')} row {seg['row']}" if seg.get("row") else ""))
        if seg.get("samples"):
            lines.append(f"  Samples: {', '.join(x['config'] for x in seg['samples'])}  (extraction {seg['extraction_id']})")
        else:
            lines.append(f"  Fixtures: {', '.join(seg['fixtures'])}  (extraction {seg['extraction_id']})")
        lines += [f"  Editor: {x['url']}" for x in seg.get("editors", [])]
        lines.append(f"  Page claims: {fmt(seg['expected'])}")
        lines.append(f"  Sensible:    {fmt(seg['actual'])}")
        lines += [f"  [fixture] WARNING: {w['text']}" for w in record["warnings"] if w["source"] == "fixture"]
    fp = record.get("fingerprint")
    if fp:
        lines.append(f"{record['test_id']}: fingerprint in strict mode (compared exactly)")
        for run in fp["runs"]:
            which = "as written" if not run["break"] else f"tests {', '.join(map(str, run['break']))} broken"
            lines.append(f"  {which}: page claims {'passes' if run['expected'] else 'fails'}; Sensible {'passed' if run['actual'] else 'failed'}  (extraction {run['extraction_id']})")
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
