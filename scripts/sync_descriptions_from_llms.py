#!/usr/bin/env python3
"""
Update .md files' metadata.description from llms.txt descriptions.

Uses llms.txt as the source of truth and updates the front matter
in the corresponding .md files.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml


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
    pattern = r"\[([^\]]+)\]\(([^)]+\.md)\):\s*(.+?)(?:\n|$)"
    matches = re.findall(pattern, content)

    paths = {}
    for _, path, description in matches:
        decoded_path = unquote(path)
        paths[decoded_path] = description.strip()

    return paths


def parse_front_matter(content: str) -> tuple[dict, str, str]:
    """
    Parse front matter from markdown content.
    Returns (front_matter_dict, front_matter_raw, body).
    """
    if not content.startswith("---"):
        return {}, "", content

    # Find the closing ---
    match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not match:
        return {}, "", content

    front_matter_end = match.start() + 3
    front_matter_raw = content[3:front_matter_end]
    body_start = match.end() + 3
    body = content[body_start:]

    try:
        front_matter = yaml.safe_load(front_matter_raw) or {}
    except yaml.YAMLError:
        return {}, front_matter_raw, body

    return front_matter, front_matter_raw, body


def has_metadata_description(front_matter: dict) -> bool:
    """Check if front matter has metadata.description key."""
    if not isinstance(front_matter.get("metadata"), dict):
        return False
    return "description" in front_matter["metadata"]


def update_front_matter(content: str, new_description: str) -> str | None:
    """
    Update metadata.description in the front matter.
    Returns updated content, or None if update failed.
    """
    front_matter, _, body = parse_front_matter(content)

    if not front_matter:
        return None

    if not isinstance(front_matter.get("metadata"), dict):
        return None

    if "description" not in front_matter["metadata"]:
        return None

    front_matter["metadata"]["description"] = new_description

    # Rebuild the file with updated front matter
    new_front_matter = yaml.dump(
        front_matter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=1000,  # Prevent line wrapping
    )

    return f"---\n{new_front_matter}---\n{body}"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update .md files' metadata.description from llms.txt"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
    )
    args = parser.parse_args()

    # Determine repo root
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent

    if not (repo_root / "llms.txt").exists():
        repo_root = Path.cwd()

    print(f"Syncing descriptions from llms.txt in: {repo_root}")
    if args.dry_run:
        print("(DRY RUN - no files will be modified)\n")
    else:
        print()

    llms_entries = parse_llms_txt(repo_root / "llms.txt")

    updated = 0
    skipped_in_sync = 0
    skipped_no_key = []
    errors = 0

    for rel_path, llms_description in sorted(llms_entries.items()):
        file_path = repo_root / rel_path

        if not file_path.exists():
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"ERROR reading {rel_path}: {e}")
            errors += 1
            continue

        front_matter, _, _ = parse_front_matter(content)

        # Skip files without metadata:description key
        if not has_metadata_description(front_matter):
            skipped_no_key.append(rel_path)
            continue

        current_description = front_matter["metadata"].get("description", "") or ""

        if current_description == llms_description:
            skipped_in_sync += 1
            continue

        # Update the file
        new_content = update_front_matter(content, llms_description)

        if new_content is None:
            print(f"WARNING: Could not update {rel_path}")
            errors += 1
            continue

        print(f"{'Would update' if args.dry_run else 'Updating'}: {rel_path}")
        print(f"  From: \"{current_description}\"")
        print(f"  To:   \"{llms_description}\"")

        if not args.dry_run:
            file_path.write_text(new_content, encoding="utf-8")

        updated += 1

    # Report files missing metadata:description
    if skipped_no_key:
        print()
        print("=" * 60)
        print("SKIPPED (missing metadata:description key)")
        print("=" * 60)
        for path in skipped_no_key:
            print(f"  - {path}")

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  {'Would update' if args.dry_run else 'Updated'}: {updated}")
    print(f"  Already in sync: {skipped_in_sync}")
    print(f"  Skipped (no metadata:description): {len(skipped_no_key)}")
    if errors:
        print(f"  Errors: {errors}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
