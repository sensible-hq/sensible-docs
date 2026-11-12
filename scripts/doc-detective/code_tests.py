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
  code_tests.py --file PAGE --check-fixtures      report fixtures that differ from the test account (no changes)
  code_tests.py --file PAGE --probe-blank         rerun each test that names a document on a blank page instead,
                                                  and print JSON: does the output come back the same?

Needs SENSIBLE_TEST_API_KEY, and an Anthropic key to judge LLM values, in .env or the environment.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Local installs: pip install --target scripts/doc-detective/.deps -r scripts/doc-detective/requirements.txt
sys.path[:0] = [os.path.join(HERE, ".deps"), HERE]

from codetests import envelope, judge, markup, record, runner, settings, usage  # noqa: E402
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
    parser.add_argument("--check-fixtures", action="store_true", help="Compare the code tests' fixtures with the test account and report differences, without changing anything")
    parser.add_argument("--probe-blank", action="store_true",
                        help="Run each code test that names a document on a blank page instead, compare with the inline output, "
                             "and print JSON: [{testId, unchanged, detail}]. Unchanged means the example doesn't read its document")
    parser.add_argument("--keep", action="store_true", help=f"Don't delete the {settings.DOC_TYPE} document type afterward (to inspect it in the app)")
    args = parser.parse_args()
    if args.probe_blank and (args.list or args.check_syntax or args.check_fixtures or args.build_envelope or args.extend_envelope):
        parser.error("--probe-blank can't be combined with --list, --check-syntax, --check-fixtures, or the envelope options")
    settings.load_dotenv()
    # A probe prints only its JSON to stdout; everything else goes to stderr, and anything that stops it exits 2
    log = sys.stderr if args.probe_blank else sys.stdout
    cant_run = 2 if args.probe_blank else 1

    try:
        page = markup.parse_page(args.file)
    except CodeTestError as e:
        print(f"FAIL {args.file}  {e}", file=log)
        return cant_run
    if args.list:
        for t in sorted(page.ui_tests + list(page.code_tests.values()), key=lambda t: t.line):
            kind = "UI test  " if isinstance(t, markup.UiTest) else "code test"
            document = "  (no document: runs on a blank page)" if getattr(t, "blank_document", False) else f"  {getattr(t, 'document_url', '')}"
            print(f"{kind}  {t.test_id}  (line {t.line})" + (document if kind == "code test" else ""))
        return 0

    unknown = [t for t in args.test or [] if t not in page.code_tests]
    if unknown:
        print(f"FAIL  no code test {', '.join(unknown)} in {args.file}", file=log)
        return cant_run
    selected = [page.code_tests[t] for t in (args.test or page.code_tests)]
    if not selected:
        print(f"No code tests in {args.file}", file=log)
        if args.probe_blank:
            print("[]")
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

    try:
        key_var = settings.sensible_key_var()
    except ValueError as e:
        print(e, file=sys.stderr)
        return 2
    key = settings.key(key_var)
    if not key:
        print(f"{key_var} isn't set in .env or the environment ({settings.ENV_VAR}={settings.env()})", file=sys.stderr)
        return 2
    print(f"Sensible environment: {settings.env()} ({settings.api()})", file=log)
    client = SensibleClient(key)

    if args.probe_blank:
        return probe_blank(args, selected, client)

    if args.check_fixtures:
        return check_fixtures(selected, client)

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
        cleanup(args, client)
        usage.save_run(client.counts)
    return 1 if failed else 0


def probe_blank(args, selected, client):
    """Rerun each selected test that names a document on the blank page, and print the results as JSON."""
    probed = [t for t in selected if runner.probeable(t)]
    for test in selected:
        if test not in probed:
            why = "names no document" if test.blank_document else "is a fixture, portfolio, fingerprint, or classification test"
            print(f"SKIP {test.test_id}: {why}", file=sys.stderr)
    if not probed:
        print("[]")
        return 0
    try:
        status = client.document_status(settings.BLANK_DOCUMENT_URL)
    except Exception as e:  # noqa: BLE001 -- no network, for example: the probe can't run
        print(settings.redact(f"Couldn't reach the blank page {settings.BLANK_DOCUMENT_URL}: {type(e).__name__}: {e}"), file=sys.stderr)
        return 2
    if status != 200:
        print(f"The blank page {settings.BLANK_DOCUMENT_URL} returned {status}. It resolves once assets/pdfs/blank_page.pdf is on v0.", file=sys.stderr)
        return 2
    try:
        results = [runner.probe_blank(test, client) for test in probed]
    finally:
        cleanup(args, client, out=sys.stderr)
        print(f"Sensible usage: {client.counts['extractions']} extraction(s), {client.counts['requests']} API request(s)", file=sys.stderr)
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


def cleanup(args, client, out=None):
    """Delete the temporary document type. A failure here is reported but never hides a test's own
    result or error: records are already saved, and the next run reuses the document type."""
    # Only delete the temporary doc type if this run used it: another page's run may be using it now
    if args.keep or not getattr(client, "used_temp_doc_type", True):
        return
    try:
        if client.delete_doc_type():
            print(f"Deleted document type {settings.DOC_TYPE}", file=out or sys.stdout)
    except Exception as e:  # noqa: BLE001
        print(settings.redact(f"WARN couldn't delete document type {settings.DOC_TYPE}: {type(e).__name__}: {e}"), file=sys.stderr)


def check_fixtures(selected, client):
    """Report each fixture that differs from the test account, for example after an edit in the app.
    Changes nothing; a normal run restores the committed version and warns."""
    names = list(dict.fromkeys(name for test in selected for name in test.fixtures))
    if not names:
        print("No fixtures in the selected code tests")
        return 0
    drifted = 0
    for name in names:
        try:
            refs = markup.fixture_references(name)
            state = client.fixture_drift(*markup.fixture_files(name), refs)
        except CodeTestError as e:
            print(f"FAIL {name}  {e}")
            drifted += 1
            continue
        note = "  (an unpublished edit in the app differs from the published config; tests use the published version)" if state["draft"] else ""
        if state["drift"]:
            drifted += 1
            print(f"DRIFT {name}{note}")
            print("\n".join(f"  {d}" for d in state["drift"]))
        else:
            print(f"OK    {name}{note}")
        print(f"      editor: {markup.editor_url(state['name'], state['config_name'], refs[0]['name'])}")
    if drifted:
        print(f"{drifted} fixture(s) differ from the committed files. A normal run restores them and warns.")
    return 1 if drifted else 0


def build_envelopes(args, selected, client):
    if args.build_envelope and args.extend_envelope:
        print("Use --build-envelope or --extend-envelope, not both", file=sys.stderr)
        return 2
    if os.path.abspath(args.file).startswith(settings.SELF_TEST_PAGES_DIR + os.sep) and not os.environ.get(settings.ENVELOPES_DIR_VAR):
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
        cleanup(args, client)
    return 0


if __name__ == "__main__":
    sys.exit(main())
