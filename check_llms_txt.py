#!/usr/bin/env python3
"""
Compare llms.txt against .md files in the repository.

Reports:
- Topics in .md files that are missing from llms.txt
- Topics in llms.txt that reference deleted or hidden .md files
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote


def parse_front_matter(content: str) -> dict:
    """Extract YAML front matter from markdown content."""
    if not content.startswith("---"):
        return {}

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return {}

    front_matter_text = content[3:end_match.start() + 3]

    # Simple YAML parsing for the fields we care about
    result = {}
    for line in front_matter_text.split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key == "hidden":
                result["hidden"] = value.lower() == "true"
            elif key == "title":
                result["title"] = value

    return result


def get_md_files(repo_root: Path) -> dict[str, dict]:
    """
    Find all .md files in docs/ and reference/ directories.
    Returns dict mapping relative path -> front matter info.
    Excludes files with hidden: true.
    """
    md_files = {}
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
                print(f"Warning: Could not read {relative_path}: {e}")
                continue

            front_matter = parse_front_matter(content)

            # Skip hidden files
            if front_matter.get("hidden", False):
                continue

            md_files[str(relative_path)] = {
                "title": front_matter.get("title", relative_path.stem),
                "path": str(relative_path),
            }

    return md_files


def parse_llms_txt(llms_path: Path) -> set[str]:
    """
    Extract all .md file references from llms.txt.
    Returns set of relative paths (URL-decoded).
    """
    if not llms_path.exists():
        print(f"Error: llms.txt not found at {llms_path}")
        sys.exit(1)

    content = llms_path.read_text(encoding="utf-8")

    # Match markdown links: [text](path.md) or [text](path.md):
    # Pattern captures paths ending in .md
    pattern = r"\[([^\]]+)\]\(([^)]+\.md)\)"
    matches = re.findall(pattern, content)

    paths = set()
    for _, path in matches:
        # URL-decode the path (e.g., %20 -> space)
        decoded_path = unquote(path)
        paths.add(decoded_path)

    return paths


def check_llms_txt_accuracy(repo_root: Path) -> tuple[list, list]:
    """
    Compare llms.txt against actual .md files.

    Returns:
        - missing_from_llms: .md files not referenced in llms.txt
        - stale_in_llms: llms.txt references to non-existent/hidden files
    """
    llms_path = repo_root / "llms.txt"

    # Get all visible .md files
    md_files = get_md_files(repo_root)
    md_paths = set(md_files.keys())

    # Get all paths referenced in llms.txt
    llms_paths = parse_llms_txt(llms_path)

    # Find discrepancies
    missing_from_llms = []
    for path in sorted(md_paths - llms_paths):
        info = md_files[path]
        missing_from_llms.append({
            "path": path,
            "title": info["title"],
        })

    stale_in_llms = []
    for path in sorted(llms_paths - md_paths):
        full_path = repo_root / path
        if full_path.exists():
            # File exists but is hidden
            reason = "hidden (has hidden: true in front matter)"
        else:
            reason = "file does not exist"
        stale_in_llms.append({
            "path": path,
            "reason": reason,
        })

    return missing_from_llms, stale_in_llms


def main():
    # Determine repo root (script location or current directory)
    script_dir = Path(__file__).parent.resolve()

    # Check if llms.txt exists in script directory
    if (script_dir / "llms.txt").exists():
        repo_root = script_dir
    else:
        repo_root = Path.cwd()

    print(f"Checking llms.txt accuracy in: {repo_root}\n")

    missing_from_llms, stale_in_llms = check_llms_txt_accuracy(repo_root)

    has_issues = False

    # Report missing topics
    if missing_from_llms:
        has_issues = True
        print("=" * 60)
        print("MISSING FROM llms.txt")
        print("These .md files are not referenced in llms.txt:")
        print("=" * 60)
        for item in missing_from_llms:
            print(f"  - {item['path']}")
            print(f"    Title: {item['title']}")
        print()

    # Report stale references
    if stale_in_llms:
        has_issues = True
        print("=" * 60)
        print("STALE REFERENCES IN llms.txt")
        print("These paths in llms.txt are invalid:")
        print("=" * 60)
        for item in stale_in_llms:
            print(f"  - {item['path']}")
            print(f"    Reason: {item['reason']}")
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Missing from llms.txt: {len(missing_from_llms)}")
    print(f"  Stale references:      {len(stale_in_llms)}")

    if not has_issues:
        print("\n✓ llms.txt is up to date!")
        return 0
    else:
        print("\n✗ llms.txt needs updating.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
