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
import re
import sys
from pathlib import Path

import yaml


def load_ignore_list(script_dir: Path) -> set[str]:
    """Load list of files to ignore from description_ignore.txt."""
    ignore_file = script_dir / "description_ignore.txt"
    if not ignore_file.exists():
        return set()

    ignore_list = set()
    for line in ignore_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            ignore_list.add(line)
    return ignore_list


def parse_front_matter(content: str) -> dict | None:
    """Extract YAML front matter from markdown content."""
    if not content.startswith("---"):
        return None

    # Find the closing ---
    end_match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end_match:
        return None

    front_matter_text = content[3:end_match.start() + 3]

    try:
        return yaml.safe_load(front_matter_text) or {}
    except yaml.YAMLError:
        return None


def check_descriptions(repo_root: Path, ignore_list: set[str]) -> tuple[list[dict], list[str]]:
    """
    Find all .md files with empty metadata.description.
    Only targets files that have the description key but with an empty/blank value.
    Returns tuple of (list of files with issues, list of ignored file paths).
    """
    issues = []
    ignored_files = []
    search_dirs = ["docs", "reference"]

    for search_dir in search_dirs:
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

            front_matter = parse_front_matter(content)
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
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    # Determine repo root (script location's grandparent or current directory)
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent

    # Verify we found the right directory
    if not (repo_root / "docs").exists():
        repo_root = Path.cwd()

    # Load ignore list
    ignore_list = load_ignore_list(script_dir)

    issues, ignored_files = check_descriptions(repo_root, ignore_list)

    if args.json:
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

    # Summary
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
