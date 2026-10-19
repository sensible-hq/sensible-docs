#!/usr/bin/env python3
"""Decide whether a push needs a docs-test run: only if it changed something a test runs.

A push that changed only PAGE's prose (for example, a ReadMe save) skips the run; the monthly run
still covers product drift. It runs if the push changed another file the workflow watches
(--watch: the workflow's other push paths, such as fixtures and tooling), or the page's tests:
their markup, configs, documents, expectations, or the row count of a tagged table.

Prints "run=true" or "run=false" (for $GITHUB_OUTPUT), and the reason on stderr.

Usage: should_run.py --page PAGE --before SHA [--after SHA] [--watch GLOB ...]
"""

import argparse
import dataclasses
import fnmatch
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from codetests import markup  # noqa: E402

# Where a test is, and how it's described, don't change what it runs
IGNORED = {"file", "line", "config_line", "output_line", "output_span", "description"}


def spec(path):
    """What the page's tests run, in a comparable form."""
    page = markup.parse_page(path)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    tables = {}
    for tag in markup.TABLE_TAG_RE.finditer(text):
        tables[tag.group(1)] = markup._table_rows(text, tag.end())
    return {
        "ui": [(t.test_id, t.steps) for t in page.ui_tests],
        "ui_markup": [m.group(0) for m in markup.UI_TEST_RE.finditer(text)],
        "code": [{k: v for k, v in dataclasses.asdict(t).items() if k not in IGNORED} for t in page.code_tests.values()],
        "tables": tables,
    }


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def decide(page, before, after="HEAD", watch=()):
    """(run, reason)."""
    if not before or set(before) == {"0"}:
        return True, "no previous commit to compare with"
    try:
        changed = [f for f in git("diff", "--name-only", before, after).splitlines() if f]
    except subprocess.CalledProcessError:
        return True, f"can't diff {before[:9]}..{after}"
    others = [f for f in changed if f != page and any(fnmatch.fnmatch(f, g) for g in watch)]
    if others:
        return True, f"the push changed {others[0]}" + (f" and {len(others) - 1} more file(s)" if len(others) > 1 else "")
    if page not in changed:
        return True, "the push didn't change the page"
    try:
        old_text = git("show", f"{before}:{page}")
    except subprocess.CalledProcessError:
        return True, "the page is new"
    try:
        new = spec(page)
    except Exception as e:  # noqa: BLE001 -- broken markup: run, so the run reports it
        return True, f"the page's test markup doesn't parse ({type(e).__name__})"
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(old_text)
    try:
        old = spec(f.name)
    except Exception:  # noqa: BLE001 -- the old markup was broken or used older syntax
        return True, "the previous version's test markup doesn't parse"
    finally:
        os.remove(f.name)
    if old != new:
        return True, "the page's tests changed"
    return False, "only the page's prose changed"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--page", required=True)
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--watch", nargs="*", default=[], help="The workflow's other push paths (globs)")
    args = parser.parse_args()
    run, reason = decide(args.page, args.before, args.after, args.watch)
    print(f"run={'true' if run else 'false'}")
    print(f"{'Running' if run else 'Skipping'} the tests: {reason}", file=sys.stderr)


if __name__ == "__main__":
    main()
