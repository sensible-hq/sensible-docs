#!/usr/bin/env python3
"""Summarize failed Doc Detective tests as Markdown, for a GitHub issue body.

Usage: report.py <output dir> [--run-url URL] [--pr-url URL]
Reads the newest testResults-*.json in the output directory.
"""

import argparse
import glob
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    parser.add_argument("--run-url")
    parser.add_argument("--pr-url")
    args = parser.parse_args()

    results = sorted(glob.glob(os.path.join(args.output_dir, "testResults-*.json")))
    if not results:
        print("Doc Detective didn't write a results file. See the workflow run log.")
        return 0
    data = json.load(open(results[-1], encoding="utf-8"))

    lines = [
        "Doc Detective tests failed on `v0`.",
        "",
        "> Every check is deterministic (an exact comparison) unless it's labeled `[judge]`. A judge result is "
        "probabilistic: an LLM decided it, and the same input can get a different verdict or confidence on another run.",
    ]
    if args.run_url:
        lines.append(f"\nWorkflow run: {args.run_url}")
    if args.pr_url:
        lines.append(f"\nProposed docs fix (review before merging, it may codify a product regression): {args.pr_url}")

    for spec in data.get("specs", []):
        for test in spec.get("tests", []):
            if test.get("result") != "FAIL":
                continue
            lines.append(f"\n### `{test['testId']}`\n\nFile: `{os.path.relpath(test.get('contentPath', spec.get('specId', '')))}`\n")
            for context in test.get("contexts", []):
                for step in context.get("steps", []):
                    if step.get("result") != "FAIL":
                        continue
                    action = next((k for k in step if k in ACTIONS), "step")
                    lines.append(f"- **{action}** failed: {step.get('resultDescription', '')}")
                    stdout = ((step.get("outputs") or {}).get("stdio") or {}).get("stdout", "").strip()
                    if stdout:
                        lines.append(f"\n```\n{stdout}\n```\n")
    print("\n".join(lines))
    return 0


ACTIONS = {"goTo", "find", "click", "type", "runShell", "runCode", "httpRequest", "checkLink", "screenshot", "wait"}

if __name__ == "__main__":
    sys.exit(main())
