#!/usr/bin/env python3
"""Reports from a run's output: Doc Detective's UI test results plus the code-test records.

Usage:
  report.py html --page PAGE             write output/report.html
  report.py verify-ui --page PAGE        exit 1 if a UI test on the page has no Doc Detective result
  report.py issue [--run-url URL] [--pr-url URL] [--report-url URL]    print the failure issue body (Markdown)
  report.py summary --page PAGE [--run-url URL] [--report-url URL]     print the run summary (Markdown)
  report.py envelope-issue [--run-url URL]          print {"state", "fingerprint", "body"} as JSON

Every subcommand takes --output DIR (default: scripts/doc-detective/output).
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(HERE, ".deps"), HERE]

from codetests import markup, record, settings, usage  # noqa: E402
from codetests.reports import doc_detective, envelope_issue, html, issue, summary  # noqa: E402


def usage_summary(output_dir):
    """This run's API usage, plus the test account's month to date from Sensible. Called after the
    tests run. A failure here never fails the report: it shows why the numbers are missing."""
    settings.load_dotenv()
    summary = {"run": usage.load_run(output_dir), "budget": usage.budget()}
    try:
        key_var = settings.sensible_key_var()
    except ValueError as e:
        summary["error"] = str(e)
        return summary
    key = settings.key(key_var)
    if not key:
        summary["error"] = f"{key_var} isn't set"
        return summary
    try:
        summary["month"] = usage.month_to_date(key)
    except Exception as e:  # noqa: BLE001
        summary["error"] = settings.redact(f"{type(e).__name__}: {e}")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["html", "verify-ui", "issue", "summary", "envelope-issue"])
    parser.add_argument("--page", help="The docs page that was tested (html, verify-ui)")
    parser.add_argument("--output", default=settings.OUTPUT_DIR)
    parser.add_argument("--run-url")
    parser.add_argument("--pr-url")
    parser.add_argument("--report-url", help="The HTML report's artifact URL, to link from the issue or summary")
    args = parser.parse_args()
    if args.command in ("html", "verify-ui", "summary") and not args.page:
        parser.error(f"{args.command} needs --page")

    ui_results = doc_detective.load_results(args.output)
    records = record.load_all(os.path.join(args.output, "code-tests"))

    if args.command == "html":
        print(f"Wrote {html.render(args.page, ui_results, records, os.path.join(args.output, 'report.html'), usage_summary(args.output))}")
    elif args.command == "verify-ui":
        problems = doc_detective.verify_ui(markup.parse_page(args.page), ui_results)
        for problem in problems:
            print(f"FAIL {problem}")
        return 1 if problems else 0
    elif args.command == "issue":
        print(issue.body(ui_results, records, args.run_url, args.pr_url, args.report_url))
    elif args.command == "summary":
        print(summary.body(args.page, ui_results, records, args.report_url, args.run_url))
    else:
        print(json.dumps(envelope_issue.decide(records, args.run_url)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
