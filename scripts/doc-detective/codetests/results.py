"""One result per test, whatever ran it: the shape report.html, the CI summary, the failure issue, the
saved results, and TEST-MATRIX.md read. Its shape is schemas/result.schema.json.

Three sources:
  - UI tests: Doc Detective's results (reports/doc_detective.py), one per <!-- test --> on the page
  - code tests: their records (record.py), one per code test on the page
  - other runners: output/results/<runner>.json, a list of results. A runner that checks the page
    some other way (for example the parameter-table checks, or the API contract tests) writes its
    results there during a run, and every report and the matrix include them. Its tests aren't in
    the page's markup, so each result names its own test ID, kind, and claim, and links its evidence.

A test the page marks up but that has no result is "not run", which fails the page like "fail".
"""

import glob
import json
import os

import jsonschema

from . import kinds, settings

STATUSES = ("pass", "warn", "fail", "not run")
RESULTS_DIR = "results"  # under the output directory

with open(os.path.join(settings.SCHEMAS_DIR, "result.schema.json"), encoding="utf-8") as f:
    SCHEMA = json.load(f)


def validate(result):
    jsonschema.validate(result, SCHEMA)


def from_ui(test, ui):
    """A UI test's result. Doc Detective skipping a step on the page fails it."""
    result = {"test_id": test.test_id, "runner": "ui", "kind": "ui", "claim": test.description, "line": test.line}
    if not ui:
        return {**result, "status": "not run", "checked": "", "details": f"{test.test_id}: not run"}
    status = "fail" if len(ui["steps"]) < test.steps else ui["status"]
    failed = f", {ui['failed']} failed" if ui["failed"] else ""
    steps = f"{len(ui['steps'])} steps{failed}"
    return {**result, "status": status, "checked": steps, "details": f"{test.test_id}: {steps}"}


def from_record(test, rec):
    """A code test's result, from its record."""
    kind = kinds.of(test)
    result = {"test_id": test.test_id, "runner": "code", "kind": kind.NAME, "claim": test.description, "line": test.line}
    if not rec:
        return {**result, "status": "not run", "checked": "", "details": f"{test.test_id}: not run"}
    result.update(status=rec["status"], checked=kind.checked(test, rec), details=kind.details(test, rec))
    if rec["status"] == "fail":
        result.update(category=rec.get("category", ""), message=rec.get("message", ""))
    return result


def load_other(output_dir=None):
    """Other runners' results, from output/results/*.json, each checked against the schema."""
    found = []
    for path in sorted(glob.glob(os.path.join(output_dir or settings.OUTPUT_DIR, RESULTS_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            items = json.load(f)
        if not isinstance(items, list):
            raise ValueError(f"{path}: expected a list of results")
        for item in items:
            try:
                validate(item)
            except jsonschema.ValidationError as e:
                raise ValueError(f"{path}: {item.get('test_id', '?')}: {e.message}") from e
            if item["runner"] in ("ui", "code"):
                raise ValueError(f"{path}: {item['test_id']}: runner {item['runner']!r} is reserved for this tooling's own tests")
        found += items
    return found


def for_page(page, ui_results, records, other=()):
    """Every test's result for a parsed page, in page order; other runners' results last, in their order."""
    by_id = {r["test_id"]: r for r in records}
    own = [from_ui(t, ui_results.get(t.test_id)) for t in page.ui_tests]
    own += [from_record(t, by_id.get(t.test_id)) for t in page.code_tests.values()]
    return sorted(own, key=lambda r: r["line"]) + list(other)


def overall(results):
    """The page's result: fail if any test failed or didn't run, warn if any warned, else pass."""
    statuses = {r["status"] for r in results}
    return "fail" if statuses & {"fail", "not run"} else "warn" if "warn" in statuses else "pass"
