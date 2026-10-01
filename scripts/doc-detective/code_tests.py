#!/usr/bin/env python3
"""Run a docs page's code tests: each documented SenseML config on its example document, checked
against the documented output. See scripts/doc-detective/README.md for the markup and the checks.

Usage:
  code_tests.py --file PAGE                       run every code test on the page
  code_tests.py --file PAGE --test ID             run one (repeatable)
  code_tests.py --file PAGE --list                list the page's UI tests and code tests
  code_tests.py --file PAGE --check-syntax        check markup and code blocks only (no keys, no network)
  code_tests.py --file PAGE --build-envelope 10   build each code test's regression baseline from 10 runs
  code_tests.py --file PAGE --extend-envelope 10  add 10 runs to each saved baseline

Needs SENSIBLE_TEST_API_KEY, and an Anthropic key to judge LLM values, in .env or the environment.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Local installs: pip install --target scripts/doc-detective/.deps -r scripts/doc-detective/requirements.txt
sys.path[:0] = [os.path.join(HERE, ".deps"), HERE]

from codetests import envelope, judge, markup, record, runner, settings  # noqa: E402
from codetests.errors import CodeTestError  # noqa: E402
from codetests.reports import text  # noqa: E402
from codetests.sensible import SensibleClient  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", required=True, help="Docs page with code tests")
    parser.add_argument("--test", action="append", help="Code test ID to run (repeatable). Default: all on the page")
    parser.add_argument("--list", action="store_true", help="List the page's tests and exit")
    parser.add_argument("--check-syntax", action="store_true", help="Check markup and code blocks only. No keys or network needed")
    parser.add_argument("--propose-fixes", action="store_true", default=os.environ.get(settings.PROPOSE_FIXES_VAR) == "1",
                        help=f"On a mismatch, rewrite the documented output with the actual values (default: {settings.PROPOSE_FIXES_VAR}=1)")
    parser.add_argument("--judge-model", help=f"Judge model ID (default: {settings.JUDGE_MODEL_VAR} or {judge.DEFAULT_MODEL})")
    parser.add_argument("--build-envelope", type=int, metavar="N", help="Extract each code test N times and save its LLM fields' baseline")
    parser.add_argument("--extend-envelope", type=int, metavar="N", help="Extract each code test N more times and add the runs to its saved baseline")
    parser.add_argument("--keep", action="store_true", help=f"Don't delete the {settings.DOC_TYPE} document type afterward (to inspect it in the app)")
    args = parser.parse_args()
    settings.load_dotenv()

    try:
        page = markup.parse_page(args.file)
    except CodeTestError as e:
        print(f"FAIL {args.file}  {e}")
        return 1
    if args.list:
        for t in sorted(page.ui_tests + list(page.code_tests.values()), key=lambda t: t.line):
            kind = "UI test  " if isinstance(t, markup.UiTest) else "code test"
            print(f"{kind}  {t.test_id}  (line {t.line})" + (f"  {t.document_url}" if kind == "code test" else ""))
        return 0

    unknown = [t for t in args.test or [] if t not in page.code_tests]
    if unknown:
        print(f"FAIL  no code test {', '.join(unknown)} in {args.file}")
        return 1
    selected = [page.code_tests[t] for t in (args.test or page.code_tests)]
    if not selected:
        print(f"No code tests in {args.file}")
        return 0

    if args.check_syntax:
        failed = 0
        for test in selected:
            try:
                markup.check_syntax(test)
                print(f"PASS {test.test_id}  syntax")
            except CodeTestError as e:
                print(f"FAIL {test.test_id}  {e}")
                failed += 1
        return 1 if failed else 0

    key = settings.key(settings.SENSIBLE_KEY_VAR)
    if not key:
        print(f"{settings.SENSIBLE_KEY_VAR} isn't set in .env or the environment", file=sys.stderr)
        return 2
    client = SensibleClient(key)

    if args.build_envelope or args.extend_envelope:
        return build_envelopes(args, selected, client)

    failed = 0
    try:
        for test in selected:
            rec = runner.run_code_test(test, client, judge_key=runner.judge_key(), judge_model=args.judge_model, fix=args.propose_fixes)
            record.save(rec)
            print("\n".join(text.summary(rec)))
            failed += rec["status"] == "fail"
    finally:
        if not args.keep and client.delete_doc_type():
            print(f"Deleted document type {settings.DOC_TYPE}")
    return 1 if failed else 0


def build_envelopes(args, selected, client):
    if args.build_envelope and args.extend_envelope:
        print("Use --build-envelope or --extend-envelope, not both", file=sys.stderr)
        return 2
    if os.path.abspath(args.file).startswith(settings.FIXTURES_DIR + os.sep) and not os.environ.get(settings.ENVELOPES_DIR_VAR):
        print("Refusing to build envelopes from a fixture: it would overwrite the real baselines in envelopes/. "
              f"Set {settings.ENVELOPES_DIR_VAR} to a scratch folder to build fixture baselines.", file=sys.stderr)
        return 2
    runs, extend = args.build_envelope or args.extend_envelope, bool(args.extend_envelope)
    try:
        for test in selected:
            built = runner.build_envelope(test, client, runs, extend)
            if built is None:
                print(f"SKIP {test.test_id}: no LLM fields")
                continue
            action = f"Added {runs} runs to" if extend else "Wrote"
            print(f"{action} {os.path.relpath(envelope.path(test.test_id))} ({built['runs']} runs in total, {len(built['slots'])} slots)")
    except CodeTestError as e:
        print(f"FAIL  {e}")
        return 1
    finally:
        if not args.keep and client.delete_doc_type():
            print(f"Deleted document type {settings.DOC_TYPE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
