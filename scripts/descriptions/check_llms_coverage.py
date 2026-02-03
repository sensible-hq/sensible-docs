#!/usr/bin/env python3
"""
Check and optionally fix llms.txt coverage against actual .md files.

Reports:
- Missing: .md files that exist but aren't listed in llms.txt
- Orphaned: Entries in llms.txt pointing to files that don't exist
- Hidden in llms.txt: Files with hidden: true that shouldn't be listed
- Ignored in llms.txt: Files in description_ignore.txt that shouldn't be listed
- Duplicates: Multiple entries for the same file

Use --fix to automatically:
- Remove orphaned/hidden/ignored entries
- Remove duplicate entries (keeping the one with longest description)
- Add missing files to an "Uncategorized" section

Skips files with hidden: true in front matter.
Respects ignore list in scripts/descriptions/description_ignore.txt.
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


def parse_front_matter(content: str) -> tuple[dict | None, str | None]:
    """Extract YAML front matter from markdown content.

    Returns tuple of (parsed_dict, error_message).
    If no frontmatter, returns (None, None).
    If parse error, returns (None, error_message).
    """
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


def get_llms_txt_entries(llms_path: Path) -> tuple[set[str], dict[str, list[dict]]]:
    """Extract all .md file paths and entries from llms.txt.

    Returns:
        - set of unique paths
        - dict mapping path -> list of entries (for duplicate detection)
          Each entry has: line_num, title, description, full_line
    """
    content = llms_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Match: [title](path.md) with optional ": description"
    pattern = r"^\-? ?\[([^\]]+)\]\(([^)]+\.md)\)(?::\s*(.*))?$"

    paths = set()
    entries_by_path: dict[str, list[dict]] = {}

    for line_num, line in enumerate(lines):
        match = re.match(pattern, line)
        if match:
            title = match.group(1)
            path = unquote(match.group(2))
            description = (match.group(3) or "").strip()

            paths.add(path)

            if path not in entries_by_path:
                entries_by_path[path] = []
            entries_by_path[path].append({
                "line_num": line_num,
                "title": title,
                "description": description,
                "full_line": line,
            })

    return paths, entries_by_path


def get_actual_md_files(repo_root: Path, ignore_list: set[str]) -> tuple[set[str], list[dict]]:
    """Get all visible .md files in docs/ and reference/ directories.

    Skips files that are in the ignore list or have hidden: true in frontmatter.
    Returns tuple of (set of file paths, list of yaml errors).
    """
    md_files = set()
    yaml_errors = []
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

            front_matter, yaml_error = parse_front_matter(content)
            if yaml_error:
                yaml_errors.append({"path": relative_path, "error": yaml_error})
                continue

            if front_matter and front_matter.get("hidden", False):
                continue

            md_files.add(relative_path)

    return md_files, yaml_errors


def get_file_info(file_path: Path) -> dict | None:
    """Get title and description from a markdown file's frontmatter."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return None

    front_matter, _ = parse_front_matter(content)
    if not front_matter:
        return None

    title = front_matter.get("title", "")
    metadata = front_matter.get("metadata", {})
    description = metadata.get("description", "") if isinstance(metadata, dict) else ""

    return {
        "title": title or file_path.stem,
        "description": description or "No description available",
    }


def check_coverage(repo_root: Path, ignore_list: set[str]) -> dict:
    """
    Check llms.txt coverage against actual files.
    Returns dict with missing, orphaned, hidden, ignored, duplicate files, and yaml errors.
    """
    llms_path = repo_root / "llms.txt"

    llms_paths, entries_by_path = get_llms_txt_entries(llms_path)
    actual_files, yaml_errors = get_actual_md_files(repo_root, ignore_list)

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
            front_matter, _ = parse_front_matter(content)
            if front_matter and front_matter.get("hidden", False):
                hidden_in_llms.append(path)
                continue
        except Exception:
            pass

        # If we get here, it's truly orphaned (shouldn't happen but just in case)
        orphaned.append(path)

    # Find duplicates (paths with more than one entry)
    duplicates = []
    for path, entries in entries_by_path.items():
        if len(entries) > 1:
            duplicates.append({
                "path": path,
                "count": len(entries),
                "entries": entries,
            })
    duplicates.sort(key=lambda x: x["path"])

    return {
        "missing": missing,
        "orphaned": orphaned,
        "hidden_in_llms": hidden_in_llms,
        "ignored_in_llms": ignored_in_llms,
        "duplicates": duplicates,
        "yaml_errors": yaml_errors,
        "covered": len(llms_paths & actual_files),
        "total_files": len(actual_files),
        "total_entries": sum(len(e) for e in entries_by_path.values()),
    }


def fix_coverage(repo_root: Path, issues: dict) -> dict:
    """
    Fix llms.txt by removing invalid/duplicate entries and adding missing files.
    Returns dict with changes made.
    """
    llms_path = repo_root / "llms.txt"
    content = llms_path.read_text(encoding="utf-8")

    # Collect all paths to remove entirely
    paths_to_remove = set(
        issues["orphaned"] +
        issues["hidden_in_llms"] +
        issues["ignored_in_llms"]
    )

    # For duplicates, find lines to remove (keep the one with longest description)
    duplicate_lines_to_remove = set()
    deduplicated = []
    for dup in issues.get("duplicates", []):
        entries = dup["entries"]
        # Sort by description length descending, keep the first (longest)
        sorted_entries = sorted(entries, key=lambda e: len(e["description"]), reverse=True)
        keep = sorted_entries[0]
        for entry in sorted_entries[1:]:
            duplicate_lines_to_remove.add(entry["line_num"])
        deduplicated.append({
            "path": dup["path"],
            "kept_description": keep["description"],
            "removed_count": len(entries) - 1,
        })

    # Remove invalid entries line by line
    lines = content.split("\n")
    new_lines = []
    removed = []

    # Match entries with or without description: "- [text](path.md): desc" or "[text](path.md)"
    link_pattern = r"^-? ?\[[^\]]+\]\(([^)]+\.md)\)(?::.*)?$"

    for line_num, line in enumerate(lines):
        # Check if this is a duplicate line to remove
        if line_num in duplicate_lines_to_remove:
            continue

        match = re.match(link_pattern, line)
        if match:
            path = unquote(match.group(1))
            if path in paths_to_remove:
                # Determine reason
                if path in issues["orphaned"]:
                    reason = "file doesn't exist"
                elif path in issues["hidden_in_llms"]:
                    reason = "hidden: true"
                else:
                    reason = "in ignore list"
                removed.append({"path": path, "reason": reason})
                continue
        new_lines.append(line)

    # Add missing files - place near siblings or create new section
    added = []
    link_pattern_for_dir = r"^-? ?\[[^\]]+\]\(([^)]+\.md)\)"

    # Track which new sections we've added (to avoid duplicates)
    new_sections_added = set()

    for missing_path in issues["missing"]:
        file_path = repo_root / missing_path
        info = get_file_info(file_path)
        if not info:
            continue

        encoded_path = quote(missing_path, safe="/")
        entry = f"- [{info['title']}]({encoded_path}): {info['description']}"

        # Get the parent directory of the missing file
        parent_dir = str(Path(missing_path).parent)

        # Find the last line that has an entry from the same directory
        last_sibling_idx = None
        for idx, line in enumerate(new_lines):
            match = re.match(link_pattern_for_dir, line)
            if match:
                existing_path = unquote(match.group(1))
                existing_parent = str(Path(existing_path).parent)
                if existing_parent == parent_dir:
                    last_sibling_idx = idx

        if last_sibling_idx is not None:
            # Insert after the last sibling
            new_lines.insert(last_sibling_idx + 1, entry)
        else:
            # No siblings - create a new section based on parent directory
            # Convert path like "docs/welcome/cheat" to heading "Cheat"
            section_name = Path(parent_dir).name.replace("-", " ").replace("_", " ").title()
            section_heading = f"## {section_name}"

            # Only add section heading if we haven't already for this dir
            if parent_dir not in new_sections_added:
                new_lines.append("")
                new_lines.append(section_heading)
                new_lines.append("")
                new_sections_added.add(parent_dir)

            new_lines.append(entry)

        added.append({
            "path": missing_path,
            "title": info["title"],
            "description": info["description"],
        })

    # Write changes
    new_content = "\n".join(new_lines)
    llms_path.write_text(new_content, encoding="utf-8")

    return {"removed": removed, "added": added, "deduplicated": deduplicated}


def main():
    parser = argparse.ArgumentParser(
        description="Check llms.txt coverage against actual .md files"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically fix issues (remove invalid entries, add missing files)"
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

    total_issues = (
        len(result["missing"]) +
        len(result["orphaned"]) +
        len(result["hidden_in_llms"]) +
        len(result["ignored_in_llms"]) +
        len(result["duplicates"]) +
        len(result["yaml_errors"])
    )

    # Apply fixes if requested
    fix_result = None
    if args.fix and total_issues > 0:
        fix_result = fix_coverage(repo_root, result)

    # JSON output mode
    if args.json:
        output = result
        if fix_result:
            output["fixed"] = fix_result
        print(json.dumps(output))
        return 0

    # Human-readable output
    action = "Fixing" if args.fix else "Checking"
    print(f"{action} llms.txt coverage...")
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

    if result["duplicates"]:
        print("=" * 60)
        print("DUPLICATE ENTRIES (keeping longest description)")
        print("=" * 60)
        for dup in result["duplicates"]:
            print(f"  - {dup['path']} ({dup['count']} entries)")
        print()

    if result["yaml_errors"]:
        print("=" * 60)
        print("YAML ERRORS (invalid frontmatter)")
        print("=" * 60)
        for err in result["yaml_errors"]:
            print(f"  - {err['path']}")
            print(f"    Error: {err['error']}")
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
    print(f"  Duplicate entries:   {len(result['duplicates'])}")
    print(f"  YAML errors:         {len(result['yaml_errors'])}")

    if total_issues == 0:
        print("\n✓ llms.txt is fully in sync with .md files!")
    elif fix_result:
        dedup_count = len(fix_result.get('deduplicated', []))
        print(f"\n✓ Fixed: {len(fix_result['removed'])} removed, {len(fix_result['added'])} added, {dedup_count} deduplicated.")
    else:
        print(f"\n✗ {total_issues} issue(s) found. Use --fix to repair.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
