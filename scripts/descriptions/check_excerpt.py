#!/usr/bin/env python3
"""
Check that every .md topic in docs/ has a non-empty excerpt.

For docs/: flags files where excerpt is missing entirely OR empty/blank.
For reference/: only flags files where excerpt exists but is empty/blank
(missing key is treated as intentionally omitted).

Skips files with hidden: true in front matter.
Respects ignore list in scripts/descriptions/description_ignore.txt.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


def load_ignore_list(script_dir: Path) -> set[str]:
    ignore_file = script_dir / "description_ignore.txt"
    if not ignore_file.exists():
        return set()

    ignore_list = set()
    for line in ignore_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            ignore_list.add(line)
    return ignore_list


def parse_front_matter(content: str) -> tuple[dict | None, str | None]:
    if not content.startswith("---"):
        return None, None

    end_match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end_match:
        return None, None

    front_matter_text = content[3:end_match.start() + 3]

    try:
        return yaml.safe_load(front_matter_text) or {}, None
    except yaml.YAMLError as e:
        return None, str(e)


def check_excerpts(repo_root: Path, ignore_list: set[str]) -> tuple[list[dict], list[str]]:
    issues = []
    ignored_files = []
    search_dirs = ["docs", "reference"]

    for search_dir in search_dirs:
        dir_path = repo_root / search_dir
        if not dir_path.exists():
            continue

        for md_path in dir_path.rglob("*.md"):
            relative_path = md_path.relative_to(repo_root)

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

            if front_matter.get("hidden", False):
                continue

            excerpt = front_matter.get("excerpt", None)

            # For docs/: flag missing key entirely, as well as empty values.
            # For reference/: treat missing key as intentionally omitted.
            if excerpt is None:
                if search_dir == "docs":
                    issues.append({
                        "path": str(relative_path),
                        "title": front_matter.get("title", "Unknown"),
                        "reason": "Missing excerpt key",
                    })
                continue

            if isinstance(excerpt, str) and not excerpt.strip():
                issues.append({
                    "path": str(relative_path),
                    "title": front_matter.get("title", "Unknown"),
                    "reason": "Empty excerpt",
                })

    return issues, ignored_files


def main():
    parser = argparse.ArgumentParser(description="Check for missing excerpts in .md files")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent

    if not (repo_root / "docs").exists():
        repo_root = Path.cwd()

    ignore_list = load_ignore_list(script_dir)
    issues, ignored_files = check_excerpts(repo_root, ignore_list)

    if args.json:
        print(json.dumps(issues))
        return 0

    print("Running ./scripts/descriptions/check_excerpt.py...")
    print(f"Checking excerpts in: {repo_root}\n")

    if issues:
        print("=" * 60)
        print("FILES MISSING EXCERPT")
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
    print(f"  Files missing excerpt:   {len(issues)}")
    print(f"  Files skipped (ignored): {len(ignored_files)}")

    if not issues:
        print("\n✓ All visible .md files have excerpts!")
    else:
        print(f"\n✗ {len(issues)} file(s) need excerpts added.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
