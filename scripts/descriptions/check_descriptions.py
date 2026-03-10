#!/usr/bin/env python3
"""
Check that every .md topic in dirs "docs" and "reference" that has a
metadata.description key has a non-empty value.

Reports files that have the metadata.description field but it's empty.
Skips files with hidden: true in front matter.
Skips files without a metadata.description key (intentionally omitted).
Respects ignore list in scripts/descriptions/description_ignore.txt.
"""

import argparse
import json
import sys
from pathlib import Path

from utils import SEARCH_DIRS, find_repo_root, load_ignore_list, parse_front_matter


def check_descriptions(repo_root: Path, ignore_list: set[str]) -> tuple[list[dict], list[str]]:
    """
    Find all .md files with empty metadata.description.
    Only targets files that have the description key but with an empty/blank value.
    Returns tuple of (list of files with issues, list of ignored file paths).
    """
    issues = []
    ignored_files = []

    for search_dir in SEARCH_DIRS:
        dir_path = repo_root / search_dir
        if not dir_path.exists():
            continue

        for md_path in dir_path.rglob("*.md"):
            relative_path = md_path.relative_to(repo_root)

            # Skip files in ignore list
            if str(relative_path) in ignore_list:
                ignored_files.append(str(relative_path))
                continue

            try:
                content = md_path.read_text(encoding="utf-8")
            except Exception as e:
                issues.append({
                    "path": str(relative_path),
                    "title": "Unknown",
                    "reason": f"Could not read file: {e}",
                })
                continue

            front_matter, yaml_error = parse_front_matter(content)
            if yaml_error:
                issues.append({
                    "path": str(relative_path),
                    "title": "Unknown",
                    "reason": f"Invalid YAML frontmatter: {yaml_error}",
                })
                continue

            if front_matter is None:
                continue

            # Skip hidden files
            if front_matter.get("hidden", False):
                continue

            # Skip files without a metadata block
            metadata = front_matter.get("metadata")
            if not isinstance(metadata, dict):
                continue

            # Skip files without a description key (intentionally omitted)
            if "description" not in metadata:
                continue

            # Flag files where description key exists but value is empty or blank
            description = metadata.get("description")
            if description is None or (isinstance(description, str) and not description.strip()):
                issues.append({
                    "path": str(relative_path),
                    "title": front_matter.get("title", "Unknown"),
                    "reason": "Empty metadata.description",
                })

    return issues, ignored_files


def main():
    parser = argparse.ArgumentParser(description="Check for missing metadata descriptions in .md files")
    parser.add_argument("--json", action="store_true", help="Output results as JSON (summary printed to stderr)")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    repo_root = find_repo_root(script_dir)
    ignore_list = load_ignore_list(script_dir)

    issues, ignored_files = check_descriptions(repo_root, ignore_list)

    if args.json:
        print(f"Missing descriptions: {len(issues)} file(s) need descriptions.", file=sys.stderr)
        print(json.dumps(issues))
        return 0  # Always return 0 in JSON mode; workflow handles the count

    print("Running ./scripts/descriptions/check_descriptions.py...")
    print(f"Checking metadata descriptions in: {repo_root}\n")

    if issues:
        print("=" * 60)
        print("FILES MISSING METADATA DESCRIPTION")
        print("=" * 60)
        for item in sorted(issues, key=lambda x: x["path"]):
            print(f"  - {item['path']}")
            print(f"    Title: {item['title']}")
            print(f"    Issue: {item['reason']}")
        print()

    if ignored_files:
        print("=" * 60)
        print("FILES SKIPPED (in description_ignore.txt)")
        print("=" * 60)
        for path in sorted(ignored_files):
            print(f"  - {path}")
        print()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Files missing description: {len(issues)}")
    print(f"  Files skipped (ignored):   {len(ignored_files)}")

    if not issues:
        print("\n✓ All visible .md files have metadata descriptions!")
    else:
        print(f"\n✗ {len(issues)} file(s) need descriptions added.")

    return 0  # Always return 0; workflow uses JSON output count to decide next steps


if __name__ == "__main__":
    sys.exit(main())
