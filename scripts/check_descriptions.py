#!/usr/bin/env python3
"""
Check that every .md topic in  dirs "docs" and "reference" has a description 
in the YAML metadata front matter.

Reports files that are missing the metadata.description field or have it empty.
Skips files with hidden: true in front matter.
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_front_matter(content: str) -> dict:
    """Extract YAML front matter from markdown content."""
    if not content.startswith("---"):
        return {}

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return {}

    front_matter_text = content[3:end_match.start() + 3]

    # Parse YAML - handle nested metadata block
    result = {
        "title": "",
        "hidden": False,
        "metadata_description": "",
    }

    in_metadata_block = False

    for line in front_matter_text.split("\n"):
        stripped = line.strip()

        # Check for metadata block start
        if stripped == "metadata:":
            in_metadata_block = True
            continue

        # Check if we've exited the metadata block (non-indented line)
        if in_metadata_block and line and not line.startswith(" ") and not line.startswith("\t"):
            in_metadata_block = False

        if ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip().strip("'\"")

            if key == "hidden":
                result["hidden"] = value.lower() == "true"
            elif key == "title" and not in_metadata_block:
                result["title"] = value
            elif key == "description" and in_metadata_block:
                result["metadata_description"] = value

    return result


def check_descriptions(repo_root: Path) -> list[dict]:
    """
    Find all .md files missing metadata.description.
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

            # Skip hidden files
            if front_matter.get("hidden", False):
                continue

            description = front_matter.get("metadata_description", "")

            if not description:
                issues.append({
                    "path": str(relative_path),
                    "title": front_matter.get("title", "Unknown"),
                    "reason": "Missing or empty metadata.description",
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
        return 0
    else:
        print(f"\n✗ {len(issues)} file(s) need descriptions added.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
