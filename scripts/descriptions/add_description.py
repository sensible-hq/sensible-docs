#!/usr/bin/env python3
"""
Update an existing metadata.description in a markdown file's front matter.

Only updates files that already have a metadata.description key.
Will not create the key if it doesn't exist.
Respects ignore list in scripts/descriptions/description_ignore.txt.

Usage: add_description.py <file_path> <description>
"""

import re
import sys
from pathlib import Path

import yaml

from utils import find_repo_root, load_ignore_list


def update_file_with_description(file_path: Path, description: str) -> bool:
    """Update the file's front matter with the new description."""
    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return False

    end_match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end_match:
        return False

    front_matter_text = content[3:end_match.start() + 3]
    rest_of_file = content[end_match.end() + 3:]

    # Parse YAML front matter
    try:
        front_matter = yaml.safe_load(front_matter_text) or {}
    except yaml.YAMLError:
        return False

    # Only update if metadata.description key already exists
    metadata = front_matter.get("metadata")
    if not isinstance(metadata, dict) or "description" not in metadata:
        return False

    front_matter["metadata"]["description"] = description

    # Dump back to YAML, preserving reasonable formatting
    new_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True, sort_keys=False)

    new_content = f"---\n{new_front_matter}---\n{rest_of_file}"
    file_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_path> <description>", file=sys.stderr)
        return 1

    file_path = Path(sys.argv[1])
    description = sys.argv[2]

    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    script_dir = Path(__file__).parent.resolve()
    ignore_list = load_ignore_list(script_dir)

    # Normalize path for comparison
    try:
        repo_root = find_repo_root(script_dir)
        relative_path = str(file_path.resolve().relative_to(repo_root))
    except ValueError:
        relative_path = str(file_path)

    if relative_path in ignore_list:
        print(f"Skipped (in ignore list): {file_path}")
        return 0

    if update_file_with_description(file_path, description):
        print(f"Updated: {file_path}")
        return 0
    else:
        print(f"Error: Could not update {file_path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
