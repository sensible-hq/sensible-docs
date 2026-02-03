#!/usr/bin/env python3
"""
Check llms.txt coverage against actual .md files.

Reports:
- Missing: .md files that exist but aren't listed in llms.txt
- Orphaned: Entries in llms.txt pointing to files that don't exist
- Hidden in llms.txt: Files with hidden: true that shouldn't be listed
- Ignored in llms.txt: Files in description_ignore.txt that shouldn't be listed

Skips files with hidden: true in front matter.
Respects ignore list in scripts/descriptions/description_ignore.txt.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

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

    end_match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end_match:
        return None

    front_matter_text = content[3:end_match.start() + 3]

    try:
        return yaml.safe_load(front_matter_text) or {}
    except yaml.YAMLError:
        return None


def get_llms_txt_paths(llms_path: Path) -> set[str]:
    """Extract all .md file paths from llms.txt."""
    content = llms_path.read_text(encoding="utf-8")

    # Match markdown links: [text](path.md)
    pattern = r"\[[^\]]+\]\(([^)]+\.md)\)"

    paths = set()
    for match in re.finditer(pattern, content):
        path = unquote(match.group(1))
        paths.add(path)

    return paths


def get_actual_md_files(repo_root: Path, ignore_list: set[str]) -> set[str]:
    """Get all visible .md files in docs/ and reference/ directories.

    Skips files that are in the ignore list or have hidden: true in frontmatter.
    """
    md_files = set()
    search_dirs = ["docs", "reference"]

    for search_dir in search_dirs:
        dir_path = repo_root / search_dir
        if not dir_path.exists():
            continue

        for md_path in dir_path.rglob("*.md"):
            relative_path = str(md_path.relative_to(repo_root))

            if relative_path in ignore_list:
                continue

            # Check for hidden: true in frontmatter
            try:
                content = md_path.read_text(encoding="utf-8")
            except Exception:
                continue

            front_matter = parse_front_matter(content)
            if front_matter and front_matter.get("hidden", False):
                continue

            md_files.add(relative_path)

    return md_files


def check_coverage(repo_root: Path, ignore_list: set[str]) -> dict:
    """
    Check llms.txt coverage against actual files.
    Returns dict with missing, orphaned, hidden, and ignored files.
    """
    llms_path = repo_root / "llms.txt"

    llms_paths = get_llms_txt_paths(llms_path)
    actual_files = get_actual_md_files(repo_root, ignore_list)

    # Files that exist but aren't in llms.txt
    missing = sorted(actual_files - llms_paths)

    # Check each llms.txt entry that's not in actual_files
    orphaned = []  # File doesn't exist at all
    hidden_in_llms = []  # File exists but has hidden: true
    ignored_in_llms = []  # File exists but is in ignore list

    for path in sorted(llms_paths - actual_files):
        file_path = repo_root / path

        if not file_path.exists():
            orphaned.append(path)
            continue

        # File exists - check why it was excluded
        if path in ignore_list:
            ignored_in_llms.append(path)
            continue

        # Check if hidden
        try:
            content = file_path.read_text(encoding="utf-8")
            front_matter = parse_front_matter(content)
            if front_matter and front_matter.get("hidden", False):
                hidden_in_llms.append(path)
                continue
        except Exception:
            pass

        # If we get here, it's truly orphaned (shouldn't happen but just in case)
        orphaned.append(path)

    return {
        "missing": missing,
        "orphaned": orphaned,
        "hidden_in_llms": hidden_in_llms,
        "ignored_in_llms": ignored_in_llms,
        "covered": len(llms_paths & actual_files),
        "total_files": len(actual_files),
        "total_entries": len(llms_paths),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Check llms.txt coverage against actual .md files"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    args = parser.parse_args()

    # Determine repo root
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent

    if not (repo_root / "llms.txt").exists():
        repo_root = Path.cwd()

    llms_path = repo_root / "llms.txt"
    if not llms_path.exists():
        if args.json:
            print(json.dumps({"error": "llms.txt not found"}))
        else:
            print(f"Error: llms.txt not found at {llms_path}")
        return 1

    # Load ignore list
    ignore_list = load_ignore_list(script_dir)

    # Check coverage
    result = check_coverage(repo_root, ignore_list)

    # JSON output mode
    if args.json:
        print(json.dumps(result))
        return 0

    # Human-readable output
    print("Checking llms.txt coverage...")
    print(f"Repository: {repo_root}\n")

    if ignore_list:
        print(f"Ignoring {len(ignore_list)} file(s) from description_ignore.txt\n")

    if result["missing"]:
        print("=" * 60)
        print("MISSING FROM llms.txt")
        print("=" * 60)
        for path in result["missing"]:
            print(f"  - {path}")
        print()

    if result["orphaned"]:
        print("=" * 60)
        print("ORPHANED ENTRIES (file doesn't exist)")
        print("=" * 60)
        for path in result["orphaned"]:
            print(f"  - {path}")
        print()

    if result["hidden_in_llms"]:
        print("=" * 60)
        print("WARNING: Hidden files listed in llms.txt (remove these)")
        print("=" * 60)
        for path in result["hidden_in_llms"]:
            print(f"  - {path}")
        print()

    if result["ignored_in_llms"]:
        print("=" * 60)
        print("WARNING: Ignored files listed in llms.txt (remove these)")
        print("=" * 60)
        for path in result["ignored_in_llms"]:
            print(f"  - {path}")
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total .md files:     {result['total_files']}")
    print(f"  Covered in llms.txt: {result['covered']}")
    print(f"  Missing entries:     {len(result['missing'])}")
    print(f"  Orphaned entries:    {len(result['orphaned'])}")
    print(f"  Hidden in llms.txt:  {len(result['hidden_in_llms'])}")
    print(f"  Ignored in llms.txt: {len(result['ignored_in_llms'])}")

    total_issues = (
        len(result["missing"]) +
        len(result["orphaned"]) +
        len(result["hidden_in_llms"]) +
        len(result["ignored_in_llms"])
    )

    if total_issues == 0:
        print("\n✓ llms.txt is fully in sync with .md files!")
    else:
        print(f"\n✗ {total_issues} issue(s) found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
