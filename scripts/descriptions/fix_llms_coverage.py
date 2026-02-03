#!/usr/bin/env python3
"""
Fix llms.txt coverage issues.

Automatically:
- Removes orphaned entries (files that don't exist)
- Removes hidden entries (files with hidden: true)
- Removes ignored entries (files in description_ignore.txt)

For missing files, adds them to an "Uncategorized" section at the end
with their title and description from frontmatter.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

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


def get_file_info(file_path: Path) -> dict | None:
    """Get title and description from a markdown file's frontmatter."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    front_matter = parse_front_matter(content)
    if not front_matter:
        return None

    title = front_matter.get("title", "")
    metadata = front_matter.get("metadata", {})
    description = metadata.get("description", "") if isinstance(metadata, dict) else ""

    return {
        "title": title or file_path.stem,
        "description": description or "No description available",
    }


def fix_llms_txt(repo_root: Path, ignore_list: set[str], dry_run: bool = False) -> dict:
    """
    Fix llms.txt by removing invalid entries and adding missing files.
    Returns dict with changes made.
    """
    llms_path = repo_root / "llms.txt"
    content = llms_path.read_text(encoding="utf-8")
    original_content = content

    # Track changes
    removed = []
    added = []

    # Pattern to match markdown links: - [text](path.md): description
    # We need to match the whole line to remove it
    link_pattern = r"^- \[[^\]]+\]\(([^)]+\.md)\):.*$"

    lines = content.split("\n")
    new_lines = []
    paths_in_llms = set()

    for line in lines:
        match = re.match(link_pattern, line)
        if match:
            path = unquote(match.group(1))
            paths_in_llms.add(path)
            file_path = repo_root / path

            # Check if file should be removed
            should_remove = False
            reason = ""

            if not file_path.exists():
                should_remove = True
                reason = "file doesn't exist"
            elif path in ignore_list:
                should_remove = True
                reason = "in ignore list"
            else:
                # Check if hidden
                try:
                    file_content = file_path.read_text(encoding="utf-8")
                    front_matter = parse_front_matter(file_content)
                    if front_matter and front_matter.get("hidden", False):
                        should_remove = True
                        reason = "hidden: true"
                except Exception:
                    pass

            if should_remove:
                removed.append({"path": path, "reason": reason})
                continue  # Skip this line

        new_lines.append(line)

    # Find missing files that should be added
    search_dirs = ["docs", "reference"]
    missing_files = []

    for search_dir in search_dirs:
        dir_path = repo_root / search_dir
        if not dir_path.exists():
            continue

        for md_path in dir_path.rglob("*.md"):
            relative_path = str(md_path.relative_to(repo_root))

            if relative_path in ignore_list:
                continue

            if relative_path in paths_in_llms:
                continue

            # Check if hidden
            try:
                file_content = md_path.read_text(encoding="utf-8")
                front_matter = parse_front_matter(file_content)
                if front_matter and front_matter.get("hidden", False):
                    continue
            except Exception:
                continue

            # Get file info for the entry
            info = get_file_info(md_path)
            if info:
                missing_files.append({
                    "path": relative_path,
                    "title": info["title"],
                    "description": info["description"],
                })

    # Add missing files to an "Uncategorized" section
    if missing_files:
        # Check if we need to add the section header
        content_str = "\n".join(new_lines)
        if "## Uncategorized" not in content_str:
            new_lines.append("")
            new_lines.append("## Uncategorized")
            new_lines.append("")

        for item in sorted(missing_files, key=lambda x: x["path"]):
            # URL-encode spaces in path
            encoded_path = quote(item["path"], safe="/")
            entry = f"- [{item['title']}]({encoded_path}): {item['description']}"
            new_lines.append(entry)
            added.append(item)

    new_content = "\n".join(new_lines)

    # Write changes if not dry run and there are changes
    if not dry_run and new_content != original_content:
        llms_path.write_text(new_content, encoding="utf-8")

    return {
        "removed": removed,
        "added": added,
        "has_changes": new_content != original_content,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fix llms.txt coverage issues"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
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

    # Fix llms.txt
    result = fix_llms_txt(repo_root, ignore_list, dry_run=args.dry_run)

    # JSON output mode
    if args.json:
        print(json.dumps(result))
        return 0

    # Human-readable output
    action = "Would fix" if args.dry_run else "Fixing"
    print(f"{action} llms.txt coverage issues...")
    print(f"Repository: {repo_root}\n")

    if result["removed"]:
        print("=" * 60)
        print("REMOVED" if not args.dry_run else "WOULD REMOVE")
        print("=" * 60)
        for item in result["removed"]:
            print(f"  - {item['path']} ({item['reason']})")
        print()

    if result["added"]:
        print("=" * 60)
        print("ADDED" if not args.dry_run else "WOULD ADD")
        print("=" * 60)
        for item in result["added"]:
            print(f"  - {item['path']}")
            print(f"    Title: {item['title']}")
            print(f"    Description: {item['description']}")
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Entries removed: {len(result['removed'])}")
    print(f"  Entries added:   {len(result['added'])}")

    if not result["has_changes"]:
        print("\n✓ No changes needed - llms.txt is already correct!")
    elif args.dry_run:
        print(f"\n→ Run without --dry-run to apply these changes.")
    else:
        print(f"\n✓ llms.txt has been updated!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
