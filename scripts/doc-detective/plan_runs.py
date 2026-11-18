#!/usr/bin/env python3
"""Decide which docs pages a CI run tests, from test-pages.json and the event that started the run.

  Priority 1: weekly (WEEKLY_CRON). Priority 2: monthly (MONTHLY_CRON). Priority 3: on demand only.
  A push to v0 runs each priority 1 or 2 page whose tests changed (should_run.py), or whose watched
  files or the test tooling changed. Never priority 3.
  On demand (workflow_dispatch): every page at --priority (1, 2, 3, or "all"), or just --page.

Prints the GitHub Actions matrix as JSON on stdout ({"include": [<page entry>, ...]}), and why each
page runs or doesn't on stderr.

  plan_runs.py --event push --before SHA [--after SHA]
  plan_runs.py --event schedule --schedule "0 15 * * 1"
  plan_runs.py --event workflow_dispatch --priority 2 [--page PAGE]
  plan_runs.py --check        fail if a page with test markup isn't listed, or an entry is invalid

Keep WEEKLY_CRON and MONTHLY_CRON in step with the schedule in .github/workflows/doc-tests.yml.
"""

import argparse
import fnmatch
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

PAGES_FILE = os.path.join(HERE, "test-pages.json")
WEEKLY_CRON = "0 15 * * 1"  # Mondays, 15:00 UTC
MONTHLY_CRON = "30 15 1 * *"  # the 1st, 15:30 UTC
SCHEDULES = {WEEKLY_CRON: 1, MONTHLY_CRON: 2}
# A change to any of these reruns every priority 1 and 2 page on push
TOOLING = ["scripts/doc-detective/**", ".github/workflows/doc-tests.yml"]
# Except these: the tooling's own docs and its saved evidence, which change nothing a test runs.
# Keep in step with the "!" paths in .github/workflows/doc-tests.yml.
NOT_TOOLING = [
    "scripts/doc-detective/reports/**",
    "scripts/doc-detective/tests/pages/**",
    "scripts/doc-detective/sample-reports/**",
    "scripts/doc-detective/README.md",
    "scripts/doc-detective/TEST-MATRIX.md",
]
# Fixtures live under the tooling, but a fixture change reruns only the pages whose tests use it
FIXTURES = "scripts/doc-detective/fixtures/**"
# The test job's timeout in doc-tests.yml is 45 minutes; a page's step timeout must end first, so the
# scrub, issue, and fix PR steps still run
MAX_TIMEOUT_MINUTES = 40
# Any test markup: a UI test, code test, or table test
MARKUP_RE = re.compile(r"<!--\s*(?:test|code test|table test)\s+\{")
NAME_RE = re.compile(r"[a-z0-9][a-z0-9-]*")
REQUIRED = {"page": str, "priority": int, "name": str, "title": str, "issue_label": str, "watch": list,
            "timeout_minutes": int, "ui": bool, "propose_fixes": bool, "envelope_issue": bool}


def load(path=PAGES_FILE):
    with open(path, encoding="utf-8") as f:
        return json.load(f)["pages"]


def problems(entries, repo_root=REPO_ROOT, docs_glob=None):
    """Everything wrong with test-pages.json: invalid entries, and pages with test markup it doesn't list."""
    found = []
    seen = {"page": set(), "name": set(), "issue_label": set()}
    for i, entry in enumerate(entries):
        where = f"test-pages.json entry {i} ({entry.get('page', '?')})"
        for key, kind in REQUIRED.items():
            if not isinstance(entry.get(key), kind) or (kind is int and isinstance(entry.get(key), bool)):
                found.append(f"{where}: needs \"{key}\" ({kind.__name__})")
        if isinstance(entry.get("timeout_minutes"), int) and not 1 <= entry["timeout_minutes"] <= MAX_TIMEOUT_MINUTES:
            found.append(f"{where}: timeout_minutes must be 1 to {MAX_TIMEOUT_MINUTES}, so the job's own timeout never cuts off the scrub and issue steps")
        if entry.get("priority") not in (1, 2, 3):
            found.append(f"{where}: priority must be 1, 2, or 3")
        if isinstance(entry.get("name"), str) and not NAME_RE.fullmatch(entry["name"]):
            found.append(f"{where}: name must be lowercase letters, digits, and hyphens")
        if entry.get("propose_fixes") and not entry.get("fix_branch"):
            found.append(f"{where}: propose_fixes needs \"fix_branch\"")
        if isinstance(entry.get("page"), str) and not os.path.isfile(os.path.join(repo_root, entry["page"])):
            found.append(f"{where}: no such page")
        for key in seen:
            value = entry.get(key)
            if value in seen[key]:
                found.append(f"{where}: {key} {value!r} is used by another entry")
            seen[key].add(value)
    listed = {e.get("page") for e in entries}
    from codetests import markup

    marked = set()
    for path in sorted(glob.glob(docs_glob or os.path.join(repo_root, "docs", "**", "*.md"), recursive=True)):
        if MARKUP_RE.search(markup.read_page(path)):
            rel = os.path.relpath(path, repo_root)
            marked.add(rel)
            if rel not in listed:
                found.append(f"{rel} has test markup but isn't in test-pages.json, so CI never runs it. Add it with a priority")
    # A listed page that lost its markup, for example to an editor that rewrote its comments, would run nothing
    for i, entry in enumerate(entries):
        page = entry.get("page")
        if isinstance(page, str) and os.path.isfile(os.path.join(repo_root, page)) and page not in marked:
            found.append(f"test-pages.json entry {i} ({page}): the page has no test markup, so its runs test nothing. "
                         "Restore its tests, or remove the entry")
    return found


def ignored(path):
    return any(fnmatch.fnmatch(path, g) for g in NOT_TOOLING)


def changed_files(before, after):
    out = subprocess.run(["git", "diff", "--name-only", before, after], check=True, capture_output=True, text=True, cwd=REPO_ROOT)
    return [f for f in out.stdout.splitlines() if f and not ignored(f)]


def fixture_globs(page):
    """Globs for the folders of the fixtures a page's tests use, read from its markup. Empty if the
    markup doesn't parse: the page's own run reports that."""
    from codetests import markup

    try:
        tests = markup.parse_page(os.path.join(REPO_ROOT, page)).code_tests.values()
        folders = {markup.fixture_dir(name) for test in tests for name in test.fixtures}
    except Exception:  # noqa: BLE001 -- planning shouldn't fail on a page's markup; its test run reports the problem
        return []
    return sorted(os.path.relpath(folder, REPO_ROOT) + "/**" for folder in folders)


def plan_push(entries, before, after, changed=None, decide=None, fixtures_of=fixture_globs):
    """[(entry, reason)] for pages a push should run; skipped pages are logged on stderr."""
    if decide is None:
        import should_run
        decide = should_run.decide
    if changed is None:
        if not before or set(before) == {"0"}:
            changed = None  # no previous commit: run every priority 1 and 2 page
        else:
            try:
                changed = changed_files(before, after)
            except subprocess.CalledProcessError:
                changed = None
    runs = []
    for entry in entries:
        if entry["priority"] == 3:
            log(entry, False, "priority 3 runs on demand only")
            continue
        if changed is None:
            runs.append((entry, "can't tell what the push changed"))
            continue
        own = fixtures_of(entry["page"])
        # Other pages' fixtures aren't this page's tooling
        page_changed = [f for f in changed if not (fnmatch.fnmatch(f, FIXTURES) and not any(fnmatch.fnmatch(f, g) for g in own))]
        watched = [entry["page"], *entry["watch"], *own, *TOOLING, os.path.relpath(PAGES_FILE, REPO_ROOT)]
        if not any(fnmatch.fnmatch(f, g) for f in page_changed if not ignored(f) for g in watched):
            log(entry, False, "the push didn't change the page, its fixtures or watched files, or the test tooling")
            continue
        run, reason = decide(entry["page"], before, after, [g for g in watched if g != entry["page"]], NOT_TOOLING, changed=page_changed)
        if run:
            runs.append((entry, reason))
        else:
            log(entry, False, reason)
    return runs


def plan(entries, event, before="", after="HEAD", schedule="", priority="", page=""):
    if event == "push":
        runs = plan_push(entries, before, after)
    elif event == "schedule":
        level = SCHEDULES.get(schedule)
        if level is None:
            raise SystemExit(f"Unknown schedule {schedule!r}; expected one of {sorted(SCHEDULES)}")
        runs = [(e, f"scheduled run for priority {level}") for e in entries if e["priority"] == level]
        if not runs:
            # A schedule that tests nothing would pass every week while testing nothing
            raise SystemExit(f"No pages have priority {level}, so the {schedule!r} schedule would test nothing. Give a page priority {level}, or remove the schedule")
    elif event == "workflow_dispatch":
        if page:
            runs = [(e, "run on demand") for e in entries if e["page"] == page]
            if not runs:
                raise SystemExit(f"{page} isn't in test-pages.json")
        else:
            wanted = {1, 2, 3} if priority in ("", "all") else {int(priority)}
            runs = [(e, f"run on demand (priority {priority or 'all'})") for e in entries if e["priority"] in wanted]
    else:
        raise SystemExit(f"Unknown event {event!r}")
    for entry, reason in runs:
        log(entry, True, reason)
    return {"include": [entry for entry, _ in runs]}


def log(entry, run, reason):
    print(f"{'Running' if run else 'Skipping'} {entry['page']} (priority {entry['priority']}): {reason}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="Only check test-pages.json")
    parser.add_argument("--event", choices=["push", "schedule", "workflow_dispatch"])
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--schedule", default="")
    parser.add_argument("--priority", default="", choices=["", "1", "2", "3", "all"])
    parser.add_argument("--page", default="")
    args = parser.parse_args()
    entries = load()
    found = problems(entries)
    for problem in found:
        print(f"FAIL {problem}", file=sys.stderr)
    if found:
        return 1
    if args.check:
        print(f"PASS test-pages.json lists every page with test markup ({len(entries)} pages)", file=sys.stderr)
        return 0
    if not args.event:
        parser.error("--event is required unless --check")
    print(json.dumps(plan(entries, args.event, args.before, args.after, args.schedule, args.priority, args.page)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
