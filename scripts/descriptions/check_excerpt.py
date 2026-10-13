#!/usr/bin/env python3
"""
Report docs that need a generated excerpt (or, in reference/, a description).

For docs/: flags files where excerpt is missing entirely OR empty/blank.
For reference/: only flags excerpt or metadata.description keys that exist but
are empty (a missing key is treated as intentionally omitted).
Also flags files whose front matter doesn't parse, and docs/ files with no title
(reference/ endpoint pages get their title from the API spec).

Skips files with hidden: true and files in description_ignore.txt.

Usage:
  python check_excerpt.py          # human-readable report
  python check_excerpt.py --json   # list of {path, title, reason}
"""

import argparse
import json
import sys
from pathlib import Path

import frontmatter


def check_excerpts(repo_root: Path) -> list[dict]:
    issues = []
    for path, rel in frontmatter.iter_docs(repo_root, ("docs", "reference")):
        doc = frontmatter.read(path)
        if doc.error:
            issues.append({"path": rel, "title": "Unknown", "reason": f"Invalid YAML frontmatter: {doc.error}"})
            continue
        if doc.fm is None:
            continue
        if "title" not in doc.fm and not frontmatter.is_reference(rel):
            issues.append({"path": rel, "title": "Unknown", "reason": "Missing title key"})
        field = frontmatter.missing_field(rel, doc.fm)
        if field is None:
            continue
        key_absent = field == "excerpt" and "excerpt" not in doc.fm
        reason = f"Missing {field} key" if key_absent else f"Empty {field}"
        issues.append({"path": rel, "title": doc.fm.get("title", "Unknown"), "reason": reason})
    return issues


def main():
    parser = argparse.ArgumentParser(description="Check for missing excerpts in .md files")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    issues = check_excerpts(frontmatter.find_repo_root())

    if args.json:
        print(json.dumps(issues))
        return 0

    for item in issues:
        print(f"  - {item['path']}\n    Title: {item['title']}\n    Issue: {item['reason']}")
    if issues:
        print(f"\n✗ {len(issues)} file(s) need excerpts added.")
    else:
        print("✓ All visible .md files have excerpts!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
