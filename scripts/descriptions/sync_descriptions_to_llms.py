#!/usr/bin/env python3
"""
Update llms.txt descriptions from .md files' metadata.description.

Uses the YAML front matter as the source of truth and updates
the corresponding entries in llms.txt.
Respects ignore list in scripts/descriptions/description_ignore.txt.
"""

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
    """Parse front matter from markdown content."""
    if not content.startswith("---"):
        return None

    match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not match:
        return None

    front_matter_raw = content[3:match.start() + 3]

    try:
        return yaml.safe_load(front_matter_raw) or {}
    except yaml.YAMLError:
        return None


def get_md_descriptions(repo_root: Path, ignore_list: set[str]) -> tuple[dict[str, str], set[str]]:
    """
    Get all metadata.description values from .md files.
    Returns:
        - dict mapping relative path -> description (for files with non-empty descriptions)
        - set of relative paths for files with empty/missing descriptions
    """
    descriptions = {}
    empty_descriptions = set()
    search_dirs = ["docs", "reference"]

    for search_dir in search_dirs:
        dir_path = repo_root / search_dir
        if not dir_path.exists():
            continue

        for md_path in dir_path.rglob("*.md"):
            relative_path = str(md_path.relative_to(repo_root))

            if relative_path in ignore_list:
                continue

            try:
                content = md_path.read_text(encoding="utf-8")
            except Exception:
                continue

            front_matter = parse_front_matter(content)
            if front_matter is None:
                continue

            metadata = front_matter.get("metadata")
            if not isinstance(metadata, dict):
                continue

            if "description" not in metadata:
                continue

            description = metadata.get("description")
            if description and isinstance(description, str) and description.strip():
                descriptions[relative_path] = description.strip()
            else:
                empty_descriptions.add(relative_path)

    return descriptions, empty_descriptions


def update_llms_txt(llms_path: Path, md_descriptions: dict[str, str], empty_descriptions: set[str], dry_run: bool) -> dict:
    """
    Update llms.txt with descriptions from .md files.
    Returns stats about what was updated.
    """
    content = llms_path.read_text(encoding="utf-8")
    original_content = content

    # Match markdown links with descriptions: [text](path.md): description
    pattern = r"(\[[^\]]+\]\()([^)]+\.md)(\):\s*)(.+?)(\n|$)"

    updates = []
    already_in_sync = 0
    warnings = []

    def replace_description(match):
        nonlocal already_in_sync
        prefix = match.group(1)
        path = match.group(2)
        mid = match.group(3)
        current_desc = match.group(4).strip()
        suffix = match.group(5)

        decoded_path = unquote(path)

        # Check if llms.txt has a description but frontmatter is empty
        if decoded_path in empty_descriptions and current_desc:
            warnings.append({
                "path": decoded_path,
                "llms_description": current_desc,
            })
            return match.group(0)

        if decoded_path in md_descriptions:
            new_desc = md_descriptions[decoded_path]
            if current_desc != new_desc:
                updates.append({
                    "path": decoded_path,
                    "from": current_desc,
                    "to": new_desc,
                })
                return f"{prefix}{path}{mid}{new_desc}{suffix}"
            else:
                already_in_sync += 1

        return match.group(0)

    new_content = re.sub(pattern, replace_description, content)

    if not dry_run and new_content != original_content:
        llms_path.write_text(new_content, encoding="utf-8")

    return {
        "updates": updates,
        "in_sync": already_in_sync,
        "warnings": warnings,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update llms.txt descriptions from .md files' metadata.description"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
    )
    args = parser.parse_args()

    # Determine repo root
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent.parent

    if not (repo_root / "llms.txt").exists():
        repo_root = Path.cwd()

    llms_path = repo_root / "llms.txt"
    if not llms_path.exists():
        print(f"Error: llms.txt not found at {llms_path}")
        return 1

    print(f"Syncing descriptions to llms.txt in: {repo_root}")
    if args.dry_run:
        print("(DRY RUN - no files will be modified)\n")
    else:
        print()

    # Load ignore list
    ignore_list = load_ignore_list(script_dir)
    if ignore_list:
        print(f"Ignoring {len(ignore_list)} file(s) from description_ignore.txt\n")

    # Get descriptions from .md files
    md_descriptions, empty_descriptions = get_md_descriptions(repo_root, ignore_list)
    print(f"Found {len(md_descriptions)} .md files with metadata.description\n")

    # Update llms.txt
    result = update_llms_txt(llms_path, md_descriptions, empty_descriptions, args.dry_run)

    # Report warnings (llms.txt has description but frontmatter is empty)
    if result["warnings"]:
        print("=" * 60)
        print("WARNING: Empty frontmatter but llms.txt has description. reconcile.")
        print("=" * 60)
        for item in result["warnings"]:
            print(f"  - {item['path']}")
            print(f"      llms.txt: \"{item['llms_description']}\"")
        print()

    # Report updates
    if result["updates"]:
        print("=" * 60)
        print("UPDATED" if not args.dry_run else "WOULD UPDATE")
        print("=" * 60)
        for item in result["updates"]:
            print(f"  - {item['path']}")
            print(f"      From: \"{item['from']}\"")
            print(f"      To:   \"{item['to']}\"")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  {'Would update' if args.dry_run else 'Updated'}: {len(result['updates'])}")
    print(f"  Already in sync: {result['in_sync']}")
    if result["warnings"]:
        print(f"  Warnings: {len(result['warnings'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
