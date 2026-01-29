#!/usr/bin/env python3
"""
Check that every .md topic in dirs "docs" and "reference" that has a
metadata.description key has a non-empty value.

Reports files that have the metadata.description field but it's empty.
Skips files with hidden: true in front matter.
Skips files without a metadata.description key (intentionally omitted).
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


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


def check_descriptions(repo_root: Path) -> list[dict]:
    """
    Find all .md files with empty metadata.description.
    Only targets files that have the description key but with an empty/blank value.
    Returns list of files with issues.
    """
    issues = []
    search_dirs = ["docs", "reference"]

    for search_dir in search_dirs:
        dir_path = repo_root / search_dir
        if not dir_path.exists():
            continue

        for md_path in dir_path.rglob("*.md"):
            relative_path = md_path.relative_to(repo_root)

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

    return issues


def main():
    parser = argparse.ArgumentParser(description="Check for missing metadata descriptions in .md files")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    # Determine repo root (script location's parent or current directory)
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent

    # Verify we found the right directory
    if not (repo_root / "docs").exists():
        repo_root = Path.cwd()

    issues = check_descriptions(repo_root)

    if args.json:
        print(json.dumps(issues))
        return 0  # Always return 0 in JSON mode; workflow handles the count

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

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Files missing description: {len(issues)}")

    if not issues:
        print("\n✓ All visible .md files have metadata descriptions!")
    else:
        print(f"\n✗ {len(issues)} file(s) need descriptions added.")

    return 0  # Always return 0; workflow uses JSON output count to decide next steps


if __name__ == "__main__":
    sys.exit(main())
