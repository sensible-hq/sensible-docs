"""The Markdown summary a CI run shows on its own page ($GITHUB_STEP_SUMMARY): each test's result,
what it checked, and a link to the full HTML report."""

import os

from .. import markup, results
from . import text


def test_rows(page, ui_results, records, other=()):
    """(test ID, type, status, what it checked) for each test on the page, in page order, then other runners' tests."""
    labels = {"ui": "UI test", "code": "Code test"}
    return [(r["test_id"], labels.get(r["runner"], r["runner"]), r["status"], r.get("checked", ""))
            for r in results.for_page(page, ui_results, records, other)]


RESULT = {"pass": "✅ Passed", "warn": "⚠️ Passed with warnings", "fail": "❌ Failed", "not run": "❌ Not run"}


def body(page_path, ui_results, records, report_url=None, run_url=None, other=()):
    page = markup.parse_page(page_path)
    rows = test_rows(page, ui_results, records, other)
    overall = results.overall([{"status": status} for _, _, status, _ in rows])
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
    warnings += [(r["test_id"], r["runner"], w) for r in other for w in r.get("warnings", [])]
    if warnings:
        lines += ["", "### Warnings", ""]
        lines += [f"- `{test_id}` [{source}] {warning}" for test_id, source, warning in warnings]

    for test_id, result in ui_results.items():
        if result["status"] == "fail":
            lines += ["", f"<details><summary><code>{test_id}</code> failed</summary>", ""]
            lines += [f"- **{step['description'] or step['action']}** failed: {step['message']}" for step in result["steps"] if step["result"] == "fail"]
            lines += ["", "</details>"]

    for result in other:
        if result["status"] == "fail":
            lines += ["", f"<details><summary><code>{result['test_id']}</code> failed ({result['runner']})</summary>", "",
                      "```", f"{result.get('category', '')}: {result.get('message', '')}".lstrip(": "), "```", "", "</details>"]

    failed = [r for r in records if r["status"] == "fail"]
    for rec in failed:
        lines += ["", f"<details><summary><code>{rec['test_id']}</code> failed</summary>", "", "```",
                  *text.summary(rec), "```", "", "</details>"]
    return "\n".join(lines)
