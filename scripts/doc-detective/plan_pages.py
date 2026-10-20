#!/usr/bin/env python3
"""Decide which registered pages (config/pages.json) a doc-tests-pages.yml run tests.

- push: each page whose tests, or files its tests depend on, changed. should_run.py decides: a push
  that changed only a page's prose skips it. A page with "gate": false runs on any change to it.
- schedule: every page
- workflow_dispatch: the pages named in --pages (comma-separated slugs), or every page for "all"

Prints matrix=<JSON> and any=true|false (for $GITHUB_OUTPUT), and writes a table of each page's
decision to --summary (Markdown, for $GITHUB_STEP_SUMMARY).

Usage: plan_pages.py --event EVENT [--before SHA] [--after SHA] [--pages all|slug,slug] [--summary FILE]
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_secrets  # noqa: E402
import should_run  # noqa: E402
from codetests import markup  # noqa: E402

REGISTRY = os.path.join(HERE, "config", "pages.json")
WORKFLOW = ".github/workflows/doc-tests-pages.yml"
# Files every page's tests depend on
COMMON_WATCH = ["scripts/doc-detective/**", WORKFLOW]


DEFAULTS = {"watch": [], "secrets": ["SENSIBLE_TEST_API_KEY"], "gate": True, "propose_fixes": False, "envelope_issue": False}
FIELDS = {"slug", "title", "page", "timeout_minutes"} | set(DEFAULTS)


def load(path=REGISTRY, repo_root=check_secrets.REPO_ROOT):
    """The registered pages, checked, with defaults filled in."""
    with open(path, encoding="utf-8") as f:
        pages = [{**DEFAULTS, **p} for p in json.load(f)["pages"]]
    known_secrets = set(check_secrets.read_names(check_secrets.SECRETS_FILE))
    slugs = set()
    for p in pages:
        if not re.fullmatch(r"[a-z0-9_]+", p.get("slug", "")) or p["slug"] in slugs:
            raise ValueError(f"pages.json: slug {p.get('slug')!r} must be unique lowercase letters, digits, and underscores")
        slugs.add(p["slug"])
        if set(p) - FIELDS:
            raise ValueError(f"pages.json: {p['slug']} has unknown fields {', '.join(sorted(set(p) - FIELDS))}")
        if not p.get("page") or not p.get("title") or type(p.get("timeout_minutes")) is not int or not isinstance(p["watch"], list):
            raise ValueError(f"pages.json: {p['slug']} needs page, title, timeout_minutes (integer), and watch (a list)")
        if not os.path.isfile(os.path.join(repo_root, p["page"])):
            raise ValueError(f"pages.json: {p['slug']}: no page {p['page']}")
        if not set(p["secrets"]) <= known_secrets:
            raise ValueError(f"pages.json: {p['slug']}: secrets {', '.join(sorted(set(p['secrets']) - known_secrets))} aren't in config/secrets.txt")
        if not all(isinstance(p[k], bool) for k in ("gate", "propose_fixes", "envelope_issue")):
            raise ValueError(f"pages.json: {p['slug']}: gate, propose_fixes, and envelope_issue are true or false")
    return pages


def _changed(before, after):
    return [f for f in should_run.git("diff", "--name-only", before, after).splitlines() if f]


def _decide(page, before, after):
    watch = page["watch"] + COMMON_WATCH
    if page["gate"]:
        return should_run.decide(page["page"], before, after, watch)
    # No gate: any change to the page, or to a file its tests use, runs it
    if not before or set(before) == {"0"}:
        return True, "no previous commit to compare with"
    try:
        changed = _changed(before, after)
    except Exception:  # noqa: BLE001
        return True, f"can't diff {before[:9]}..{after}"
    hits = [f for f in changed if f == page["page"] or any(should_run.fnmatch.fnmatch(f, g) for g in watch)]
    return (True, f"the push changed {hits[0]}" + (f" and {len(hits) - 1} more file(s)" if len(hits) > 1 else "")) if hits else \
        (False, "the push changed nothing this page's tests use")


def plan(pages, event, before="", after="HEAD", wanted="all"):
    """[(page, run, reason)] for each registered page."""
    if event == "workflow_dispatch" and wanted.strip() not in ("", "all"):
        names = [s.strip() for s in wanted.split(",") if s.strip()]
        unknown = sorted(set(names) - {p["slug"] for p in pages})
        if unknown:
            raise ValueError(f"no registered page {', '.join(unknown)}; pages: {', '.join(p['slug'] for p in pages)}")
        return [(p, p["slug"] in names, "named in the manual run" if p["slug"] in names else "not named in the manual run") for p in pages]
    if event != "push":
        return [(p, True, f"{event}: every page runs") for p in pages]
    return [(p, *_decide(p, before, after)) for p in pages]


def matrix_entry(page):
    """What a test job needs about a page. ui_tests comes from the page itself: Doc Detective is
    installed only for pages with UI tests."""
    return {"slug": page["slug"], "title": page["title"], "page": page["page"], "timeout_minutes": page["timeout_minutes"],
            "secrets": page["secrets"], "ui_tests": bool(markup.parse_page(os.path.join(check_secrets.REPO_ROOT, page["page"])).ui_tests),
            "propose_fixes": page["propose_fixes"], "envelope_issue": page["envelope_issue"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--event", required=True)
    parser.add_argument("--before", default="")
    parser.add_argument("--after", default="HEAD")
    parser.add_argument("--pages", default="all")
    parser.add_argument("--summary")
    args = parser.parse_args()
    try:
        decisions = plan(load(), args.event, args.before, args.after, args.pages)
    except ValueError as e:
        print(f"ERROR {e}", file=sys.stderr)
        return 2
    include = [matrix_entry(p) for p, run, _ in decisions if run]
    print(f"matrix={json.dumps({'include': include})}")
    print(f"any={'true' if include else 'false'}")
    lines = ["## Docs test pages", "", "| Page | Tests | Why |", "| --- | --- | --- |"]
    lines += [f"| `{p['page']}` | {'run' if run else 'skipped'} | {reason} |" for p, run, reason in decisions]
    for line in lines[4:]:
        print(line, file=sys.stderr)
    if args.summary:
        with open(args.summary, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
