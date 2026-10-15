"""The doc-detective failure issue: failed UI tests, failed code tests, and triage for LLM fields."""

from . import text, wording


def body(ui_results, records, run_url=None, pr_url=None):
    lines = [
        "Doc Detective tests failed on `v0`.",
        "",
        "> " + wording.judge_disclaimer("`[judge]`"),
    ]
    if run_url:
        lines.append(f"\nWorkflow run: {run_url}")
    if pr_url:
        lines.append(f"\nProposed docs fix (review before merging, it may codify a product regression): {pr_url}")

    for test_id, result in ui_results.items():
        if result["status"] != "fail":
            continue
        lines.append(f"\n### `{test_id}` (UI test)\n")
        for step in result["steps"]:
            if step["result"] == "fail":
                lines.append(f"- **{step['description'] or step['action']}** failed: {step['message']}")

    for record in records:
        if record["status"] != "fail":
            continue
        lines.append(f"\n### `{record['test_id']}` (code test)\n\nFile: `{record['file']}`\n")
        lines.append("```\n" + "\n".join(text.summary(record)) + "\n```")

    rows = [(r["test_id"], *row) for r in records for row in wording.triage_rows(r)]
    if rows:
        lines += [
            "", "### LLM fields the judge failed or couldn't decide", "",
            "The judge asks whether the docs are still right; the [envelope] asks whether the product's behavior shifted "
            "from its baseline. Together they suggest what kind of problem it is:", "",
            "| Test | Field | Judge | Envelope | What it suggests |", "| --- | --- | --- | --- | --- |",
        ]
        lines += [f"| `{test}` | `{path}` | {verdict} | {state} | {note} |" for test, path, verdict, state, note in rows]
    return "\n".join(lines)
