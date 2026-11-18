#!/usr/bin/env python3
"""Check that an engine branch changes only schema descriptions.

  python3 check_schema_diff.py <engine-worktree> [--base origin/main]

Passes when the diff against BASE touches only src/engine/types.ts and the schemas generated from it, and:
  - every changed line in types.ts is a comment line (/** */, *, or //);
  - every changed line in the generated schemas is a "description" line, a line that only gained or lost
    a trailing comma, or a NonEmptyPartialUnion definition name whose byte offsets moved. The generator
    names those definitions after offsets in types.ts, so any edit that changes the file's length renames
    them; every engine PR that touches types.ts shows this churn.

Exits 0 when the diff is description-only, 1 otherwise, listing each line that isn't.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter

TYPES = "src/engine/types.ts"
SCHEMAS = {"src/engine/__generated__/configuration.schema.json",
           "src/engine/__generated__/doctype-settings.schema.json"}
COMMENT = re.compile(r"^\s*(/\*\*|\*|\*/|//)")
DESCRIPTION = re.compile(r'^\s*"description":')
OFFSETS = re.compile(r"(NonEmptyPartialUnion(?:<|%3C))[^>%]*((?:>|%3E))")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout


def changed_lines(repo, base, path):
    """(removed, added) line lists from a zero-context diff."""
    removed, added = [], []
    for line in git(repo, "diff", "-U0", base, "--", path).splitlines():
        if line.startswith(("---", "+++")):
            continue
        if line.startswith("-"):
            removed.append(line[1:])
        elif line.startswith("+"):
            added.append(line[1:])
    return removed, added


def normalize(line):
    return OFFSETS.sub(r"\1…\2", line.rstrip().rstrip(","))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--base", default="origin/main")
    a = ap.parse_args(argv)

    problems = []
    files = [f for f in git(a.repo, "diff", "--name-only", a.base).splitlines() if f]
    for f in files:
        if f != TYPES and f not in SCHEMAS:
            problems.append(f"{f}: only {TYPES} and its generated schemas may change")

    removed, added = changed_lines(a.repo, a.base, TYPES)
    for line in removed + added:
        if line.strip() and not COMMENT.match(line):
            problems.append(f"{TYPES}: not a comment line: {line.strip()[:120]}")

    descriptions = 0
    for schema in sorted(SCHEMAS & set(files)):
        removed, added = changed_lines(a.repo, a.base, schema)
        descriptions += sum(bool(DESCRIPTION.match(l)) for l in added)
        rest_removed = Counter(normalize(l) for l in removed if not DESCRIPTION.match(l))
        rest_added = Counter(normalize(l) for l in added if not DESCRIPTION.match(l))
        for line in (rest_removed - rest_added) + (rest_added - rest_removed):
            problems.append(f"{schema}: not a description change: {line.strip()[:120]}")

    if problems:
        print("\n".join(problems))
        return 1
    print(f"ok: {len(files)} files, {descriptions} description lines added or changed, nothing else")
    return 0


if __name__ == "__main__":
    sys.exit(main())
