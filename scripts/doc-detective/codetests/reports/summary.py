"""The Markdown summary a CI run shows on its own page ($GITHUB_STEP_SUMMARY): each test's result,
what it checked, and a link to the full HTML report."""

import os

from .. import markup
from . import html, text


def test_rows(page, ui_results, records):
    """(test ID, type, status, what it checked) for each test on the page, in page order."""
    by_id = {r["test_id"]: r for r in records}
    rows = []
    for test in page.ui_tests:
        result = ui_results.get(test.test_id)
        status = result["status"] if result else "not run"
        if result and len(result["steps"]) < test.steps:
            status = "fail"
        steps = len(result["steps"]) if result else 0
        failed = f", {result['failed']} failed" if result and result["failed"] else ""
        rows.append((test.line, test.test_id, "UI test", status, f"{steps} steps{failed}"))
    for test in page.code_tests.values():
        rec = by_id.get(test.test_id)
        if not rec:
            rows.append((test.line, test.test_id, "Code test", "not run", ""))
            continue
        checked = html.details_label(test, rec) if rec.get("segments") or rec.get("fingerprint") else f"documented output vs Sensible: {rec['overall']}" if rec.get("overall") else ""
        rows.append((test.line, test.test_id, "Code test", rec["status"], checked))
    return [row[1:] for row in sorted(rows, key=lambda r: r[0])]


RESULT = {"pass": "✅ Passed", "warn": "⚠️ Passed with warnings", "fail": "❌ Failed", "not run": "❌ Not run"}


def body(page_path, ui_results, records, report_url=None, run_url=None):
    page = markup.parse_page(page_path)
    rows = test_rows(page, ui_results, records)
    statuses = [status for _, _, status, _ in rows]
    overall = "fail" if any(s in ("fail", "not run") for s in statuses) else "warn" if "warn" in statuses else "pass"
    shown = os.path.relpath(page_path) if os.path.isabs(page_path) else page_path
    lines = [f"## Docs tests: {RESULT[overall]}", "", f"`{shown}`"]
    links = []
    if report_url:
        links.append(f"**[Open the full HTML report]({report_url})** (opens in the browser; you need to be signed in to GitHub)")
    if run_url and not report_url:
        links.append(f"Reports: the artifacts at the bottom of [this run]({run_url})")
    if links:
        lines += [""] + links
    lines += ["", "| Test | Type | Result | Checked |", "| --- | --- | --- | --- |"]
    lines += [f"| `{test_id}` | {kind} | {RESULT[status]} | {checked} |" for test_id, kind, status, checked in rows]

    warnings = [(r["test_id"], w["source"], w["text"]) for r in records for w in r["warnings"]]
    if warnings:
        lines += ["", "### Warnings", ""]
        lines += [f"- `{test_id}` [{source}] {warning}" for test_id, source, warning in warnings]

    for test_id, result in ui_results.items():
        if result["status"] == "fail":
            lines += ["", f"<details><summary><code>{test_id}</code> failed</summary>", ""]
            lines += [f"- **{step['description'] or step['action']}** failed: {step['message']}" for step in result["steps"] if step["result"] == "fail"]
            lines += ["", "</details>"]

    failed = [r for r in records if r["status"] == "fail"]
    for rec in failed:
        lines += ["", f"<details><summary><code>{rec['test_id']}</code> failed</summary>", "", "```",
                  *text.summary(rec), "```", "", "</details>"]
    return "\n".join(lines)
