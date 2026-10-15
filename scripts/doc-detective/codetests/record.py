"""The record of one code test: what was compared and decided. Every report reads records.

Its shape is schemas/record.schema.json; save() validates against it.
"""

import json
import os

import jsonschema

from . import compare, fields, settings

with open(os.path.join(settings.SCHEMAS_DIR, "record.schema.json"), encoding="utf-8") as f:
    SCHEMA = json.load(f)


def new(test):
    """A record for a code test (a markup.CodeTest), before it runs."""
    record = {
        "test_id": test.test_id,
        "description": test.description,
        "file": os.path.relpath(test.file, settings.REPO_ROOT) if os.path.isabs(test.file) else test.file,
        "document_url": test.document_url,
        "config_fragment": test.fragment,
        "status": "fail",
        "warnings": [],
    }
    if test.document_from:
        record["document_from"] = test.document_from
    return record


def judged_entry(field, path, declared_type, documented, actual, verdict, match, confidence, reasoning, judge_claim="", judge_observed=""):
    return {
        "field": field, "path": path, "type": declared_type, "documented": documented, "actual": actual,
        "verdict": verdict, "match": match, "confidence": confidence, "reasoning": reasoning,
        "judge_claim": judge_claim, "judge_observed": judge_observed,
    }


def summarize(record, expected, actual, index, exact, judged):
    """Fill in what was compared and how: overall, layout, LLM fields, and what wasn't checked."""
    notes = compare.coverage(expected, actual)

    def count(n, word):
        return f"{n} {word}" + ("" if n == 1 else "s")

    details = []
    left_out = []
    if notes["extra_top_level"]:
        left_out.append(count(len(notes["extra_top_level"]), "field"))
    if notes["extra_nested"]:
        left_out.append(count(notes["extra_nested"], "nested key"))
    if left_out:
        details.append("docs leave out " + " and ".join(left_out))
    marked = len(notes["skipped"]) + len(notes["abbreviated"])
    if marked:
        details.append(count(marked, "part") + " marked ... not checked")
    if judged:
        details.append(count(len(judged), "LLM value") + (" differs" if len(judged) == 1 else " differ") + ", decided by the judge")
    if any(j["verdict"] == "error" for j in judged):
        record["overall"] = "undecided: the judge errored"
    elif exact or any(j["verdict"] == "fail" for j in judged):
        record["overall"] = "mismatch"
    elif not details and not compare.diffs(actual, expected):
        record["overall"] = "identical"
    else:
        record["overall"] = "matches, not identical" + (f" ({'; '.join(details)})" if details else "")

    # Each documented leaf belongs to the innermost field that produced it
    llm_fields, layout_fields = {}, set()
    for path in compare.leaf_paths(expected):
        key, kind = index.owner(path)
        if kind in ("llm", "fallback"):
            llm_fields.setdefault(key, {"field": key, "kind": kind, "prompt": index.llm[key], "type": fields.format_type(index.declared_type(key)), "judged": []})
        elif key:
            layout_fields.add(key)
    for j in judged:
        llm_fields[j["field"]]["judged"].append(j)
    record["llm_fields"] = list(llm_fields.values())
    record["layout"] = {"fields": len(layout_fields), "mismatches": [compare.describe(d) for d in exact]}
    record["not_checked"] = [compare.format_path(p) for p in notes["skipped"]] + [
        f"{compare.format_path(p)}: docs show {shown} of {total} items" for p, shown, total in notes["abbreviated"]
    ]
    record["left_out"] = {"fields": notes["extra_top_level"], "nested_keys": notes["extra_nested"]}


def validate(record):
    jsonschema.validate(record, SCHEMA)


def save(record, directory=None):
    validate(record)
    directory = directory or settings.RECORDS_DIR
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, f"{record['test_id']}.json"), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)


def load_all(directory=None):
    directory = directory or settings.RECORDS_DIR
    if not os.path.isdir(directory):
        return []
    records = []
    for name in sorted(os.listdir(directory)):
        if name.endswith(".json"):
            with open(os.path.join(directory, name), encoding="utf-8") as f:
                records.append(json.load(f))
    return records
