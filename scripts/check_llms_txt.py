#!/usr/bin/env python3
"""
Compare llms.txt against .md files in the repository.

Reports:
- Topics in .md files that are missing from llms.txt
- Topics in llms.txt that reference deleted or hidden .md files
- Descriptions in llms.txt that don't match the file's metadata.description
"""

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

    # Parse YAML - handle nested metadata block
    result = {
        "title": "",
        "hidden": False,
        "description": "",
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
                result["description"] = value

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
                "description": front_matter.get("description", ""),
            }

    return md_files


def parse_llms_txt(llms_path: Path) -> dict[str, str]:
    """
    Extract all .md file references and descriptions from llms.txt.
    Returns dict mapping relative path (URL-decoded) -> description.
    """
    if not llms_path.exists():
        print(f"Error: llms.txt not found at {llms_path}")
        sys.exit(1)

    content = llms_path.read_text(encoding="utf-8")

    # Match markdown links with descriptions: [text](path.md): description
    # Pattern captures: link text, path, and description
    pattern = r"\[([^\]]+)\]\(([^)]+\.md)\):\s*(.+?)(?:\n|$)"
    matches = re.findall(pattern, content)

    paths = {}
    for _, path, description in matches:
        # URL-decode the path (e.g., %20 -> space)
        decoded_path = unquote(path)
        paths[decoded_path] = description.strip()

    return paths


def check_llms_txt_accuracy(repo_root: Path) -> tuple[list, list, list]:
    """
    Compare llms.txt against actual .md files.

    Returns:
        - missing_from_llms: .md files not referenced in llms.txt
        - stale_in_llms: llms.txt references to non-existent/hidden files
        - description_mismatches: files where llms.txt description != file's metadata.description
    """
    llms_path = repo_root / "llms.txt"

    # Get all visible .md files
    md_files = get_md_files(repo_root)
    md_paths = set(md_files.keys())

    # Get all paths and descriptions referenced in llms.txt
    llms_entries = parse_llms_txt(llms_path)
    llms_paths = set(llms_entries.keys())

    # Find missing files
    missing_from_llms = []
    for path in sorted(md_paths - llms_paths):
        info = md_files[path]
        missing_from_llms.append({
            "path": path,
            "title": info["title"],
        })

    # Find stale references
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

    # Find description mismatches (for files that exist in both)
    description_mismatches = []
    for path in sorted(md_paths & llms_paths):
        file_description = md_files[path]["description"]
        llms_description = llms_entries[path]

        if file_description != llms_description:
            description_mismatches.append({
                "path": path,
                "title": md_files[path]["title"],
                "file_description": file_description,
                "llms_description": llms_description,
            })

    return missing_from_llms, stale_in_llms, description_mismatches


def main():
    # Determine repo root (script location's parent or current directory)
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent

    # Verify we found the right directory
    if not (repo_root / "llms.txt").exists():
        repo_root = Path.cwd()

    print(f"Checking llms.txt accuracy in: {repo_root}\n")

    missing_from_llms, stale_in_llms, description_mismatches = check_llms_txt_accuracy(repo_root)

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

    # Report description mismatches
    if description_mismatches:
        has_issues = True
        print("=" * 60)
        print("DESCRIPTION MISMATCHES")
        print("These files have different descriptions in llms.txt vs front matter:")
        print("=" * 60)
        for item in description_mismatches:
            print(f"  - {item['path']}")
            print(f"    Title: {item['title']}")
            print(f"    In file:     \"{item['file_description']}\"")
            print(f"    In llms.txt: \"{item['llms_description']}\"")
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Missing from llms.txt:    {len(missing_from_llms)}")
    print(f"  Stale references:         {len(stale_in_llms)}")
    print(f"  Description mismatches:   {len(description_mismatches)}")

    if not has_issues:
        print("\n✓ llms.txt is up to date!")
        return 0
    else:
        print("\n✗ llms.txt needs updating.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
