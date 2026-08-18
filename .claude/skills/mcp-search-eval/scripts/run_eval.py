#!/usr/bin/env python3
"""
run_eval.py — MCP Search Eval runner

Runs the 18-question eval set against the Sensible docs MCP, compares results
against ground-truth.json, and reports pass/fail flips from the baseline.

Usage (must be run from the sensible-docs repo root):
    python .claude/skills/mcp-search-eval/scripts/run_eval.py
    python .claude/skills/mcp-search-eval/scripts/run_eval.py --compare-only --results-dir <path>

Requirements:
    - claude CLI in PATH
    - mcp__sensible-docs configured in .claude/settings.json (auto-loaded from repo root)
    - sessions/mcp-search-eval/ground-truth.json present

Output:
    - Per-question JSON saved to RESULTS_DIR/YYYY-MM-DD/raw/<id>.json
    - Markdown report saved to RESULTS_DIR/YYYY-MM-DD/report.md
    - Report printed to stdout
"""

import argparse
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
GROUND_TRUTH_PATH = REPO_ROOT / "sessions/mcp-search-eval/ground-truth.json"
DEFAULT_RESULTS_DIR = Path.home() / "GitHub/sensible-docs-mcp-search-eval/sessions/mcp-search-eval/results/runs"
MAX_WORKERS = 5  # WSL2 network bridge limit

AGENT_PROMPT = """\
You are running one question from the Sensible docs MCP search eval.

Question ID: {id}
Question: {question}

Steps:
1. Call mcp__sensible-docs__search with 1-2 relevant query variants for this question.
2. Call mcp__sensible-docs__fetch on each result ID returned.
3. Based ONLY on the fetched content (no prior knowledge), decide: is this question \
answerable? pass = the fetched docs contain a clear answer. fail = the answer is not \
in the docs, or the wrong docs were returned.

Output a JSON object with exactly these fields and no other text:
{{
  "question_id": "{id}",
  "search_queries": ["<query1>", "<query2>"],
  "fetched_page_ids": ["<id1>", "<id2>"],
  "pass_fail": "pass",
  "answer_summary": "<one sentence: the answer, or why it fails>"
}}
"""


def run_question(entry: dict, raw_dir: Path) -> dict | None:
    """Run a single eval question via claude CLI. Returns parsed result or None on error."""
    qid = entry["id"]
    out_path = raw_dir / f"{qid}.json"

    if out_path.exists():
        print(f"  {qid}: already exists, skipping")
        with open(out_path) as f:
            return json.load(f)

    prompt = AGENT_PROMPT.format(**entry)

    try:
        proc = subprocess.run(
            [
                "claude", "-p", prompt,
                "--output-format", "json",
                "--dangerously-skip-permissions",
            ],
            capture_output=True, text=True, timeout=180, cwd=REPO_ROOT,
        )
        raw_output = proc.stdout.strip()

        # claude --output-format json wraps the response; extract assistant text
        try:
            wrapper = json.loads(raw_output)
            text = wrapper.get("result", raw_output)
        except json.JSONDecodeError:
            text = raw_output

        # Extract the JSON object from the assistant's response text
        match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if not match:
            raise ValueError(f"No JSON object found in output:\n{text[:300]}")

        result = json.loads(match.group())
        out_path.write_text(json.dumps(result, indent=2))
        print(f"  {qid}: {result.get('pass_fail', '?')} — {result.get('answer_summary', '')[:80]}")
        return result

    except subprocess.TimeoutExpired:
        print(f"  {qid}: TIMEOUT", file=sys.stderr)
    except Exception as e:
        print(f"  {qid}: ERROR — {e}", file=sys.stderr)

    return None


def run_all(ground_truth: list, raw_dir: Path) -> list:
    """Run all eval questions in batches of MAX_WORKERS."""
    results = []
    for i in range(0, len(ground_truth), MAX_WORKERS):
        batch = ground_truth[i : i + MAX_WORKERS]
        batch_ids = [q["id"] for q in batch]
        print(f"Batch {i // MAX_WORKERS + 1}: {batch_ids}")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            futures = {ex.submit(run_question, q, raw_dir): q["id"] for q in batch}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        print()

    return results


def load_results(raw_dir: Path, ground_truth: list) -> list:
    """Load existing result JSON files from raw_dir."""
    results = []
    for entry in ground_truth:
        path = raw_dir / f"{entry['id']}.json"
        if path.exists():
            with open(path) as f:
                results.append(json.load(f))
        else:
            print(f"  Warning: no result file for {entry['id']}", file=sys.stderr)
    return results


def compare(results: list, ground_truth: list) -> list:
    """Compare run results against ground truth. Return list of finding dicts."""
    gt_index = {q["id"]: q for q in ground_truth}
    findings = []

    for result in results:
        qid = result.get("question_id")
        if not qid or qid not in gt_index:
            continue

        gt = gt_index[qid]
        fetched_ids = set(result.get("fetched_page_ids", []))
        run_pass = result.get("pass_fail") == "pass"
        baseline_pass = gt["human_pass"]
        missing_anchors = [aid for aid in gt["anchor_doc_ids"] if aid not in fetched_ids]

        finding = {
            "id": qid,
            "baseline_pass": baseline_pass,
            "run_pass": run_pass,
            "flip": run_pass != baseline_pass,
            "flip_direction": (
                "fail→pass" if (run_pass and not baseline_pass)
                else "pass→fail" if (not run_pass and baseline_pass)
                else None
            ),
            "missing_anchors": missing_anchors,
            "answer_summary": result.get("answer_summary", ""),
        }
        findings.append(finding)

    return findings


def write_report(findings: list, run_date: str, report_path: Path) -> str:
    total = len(findings)
    passed = sum(1 for f in findings if f["run_pass"])
    regressions = [f for f in findings if f["flip_direction"] == "pass→fail"]
    improvements = [f for f in findings if f["flip_direction"] == "fail→pass"]
    missing = [f for f in findings if f["missing_anchors"]]

    lines = [
        f"# MCP Search Eval — {run_date}",
        "",
        f"**Questions:** {total} · **Pass:** {passed}/{total} · "
        f"**Regressions:** {len(regressions)} · **Improvements:** {len(improvements)} · "
        f"**Missing anchor docs:** {len(missing)}",
        "",
        "---",
        "",
        "## Regressions (pass→fail)",
        "",
    ]
    if regressions:
        for f in regressions:
            lines.append(f"- **{f['id']}**")
            if f["missing_anchors"]:
                lines.append(f"  - Missing anchors: {', '.join(f['missing_anchors'])}")
            lines.append(f"  - {f['answer_summary']}")
    else:
        lines.append("None.")

    lines += ["", "## Improvements (fail→pass)", ""]
    if improvements:
        for f in improvements:
            lines.append(f"- **{f['id']}**: {f['answer_summary']}")
    else:
        lines.append("None.")

    lines += ["", "## Missing anchor docs", ""]
    if missing:
        for f in missing:
            lines.append(f"- **{f['id']}**: missing {', '.join(f['missing_anchors'])}")
    else:
        lines.append("None.")

    lines += [
        "",
        "## Full results",
        "",
        "| ID | Baseline | This run | Flip | Missing anchors |",
        "|---|---|---|---|---|",
    ]
    for f in findings:
        b = "pass" if f["baseline_pass"] else "fail"
        r = "pass" if f["run_pass"] else "fail"
        flip = f["flip_direction"] or "—"
        anchors = ", ".join(f["missing_anchors"]) if f["missing_anchors"] else "—"
        lines.append(f"| {f['id']} | {b} | {r} | {flip} | {anchors} |")

    report = "\n".join(lines)
    report_path.write_text(report)
    return report


def main():
    parser = argparse.ArgumentParser(description="Run the MCP search eval")
    parser.add_argument(
        "--compare-only", action="store_true",
        help="Skip running agents; compare existing results in --results-dir"
    )
    parser.add_argument(
        "--results-dir", type=Path, default=None,
        help="Directory containing raw/<id>.json files (defaults to dated dir under DEFAULT_RESULTS_DIR)"
    )
    args = parser.parse_args()

    ground_truth = json.loads(GROUND_TRUTH_PATH.read_text())
    run_date = date.today().isoformat()

    if args.results_dir:
        run_dir = args.results_dir
    else:
        run_dir = DEFAULT_RESULTS_DIR / run_date

    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    if args.compare_only:
        print(f"Loading results from {raw_dir}")
        results = load_results(raw_dir, ground_truth)
    else:
        print(f"Running {len(ground_truth)} questions → {raw_dir}")
        print()
        results = run_all(ground_truth, raw_dir)

    print("Comparing against ground truth...")
    findings = compare(results, ground_truth)

    report_path = run_dir / "report.md"
    report = write_report(findings, run_date, report_path)

    print()
    print(report)
    print()
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
