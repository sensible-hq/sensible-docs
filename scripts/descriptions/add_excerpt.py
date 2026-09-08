#!/usr/bin/env python3
"""
Write or update the excerpt field in a markdown file's front matter.

excerpt is the source of truth for SEO descriptions. This script inserts
the excerpt key if absent, or updates it if already present.
Respects ignore list in scripts/descriptions/description_ignore.txt.

Usage: add_excerpt.py <file_path> <excerpt_text>
"""

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


def update_file_with_excerpt(file_path: Path, excerpt: str) -> bool:
    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return False

    end_match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end_match:
        return False

    front_matter_text = content[3:end_match.start() + 3]
    rest_of_file = content[end_match.end() + 3:]

    try:
        front_matter = yaml.safe_load(front_matter_text) or {}
    except yaml.YAMLError:
        return False

    if "excerpt" in front_matter:
        front_matter["excerpt"] = excerpt
    else:
        # Insert excerpt after title to preserve expected key order.
        new_fm = {}
        for k, v in front_matter.items():
            new_fm[k] = v
            if k == "title":
                new_fm["excerpt"] = excerpt
        if "excerpt" not in new_fm:
            new_fm["excerpt"] = excerpt
        front_matter = new_fm

    new_front_matter = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True, sort_keys=False)
    file_path.write_text(f"---\n{new_front_matter}---\n{rest_of_file}", encoding="utf-8")
    return True


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_path> <excerpt_text>", file=sys.stderr)
        return 1

    file_path = Path(sys.argv[1])
    excerpt = sys.argv[2]

    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    script_dir = Path(__file__).parent.resolve()
    ignore_list = load_ignore_list(script_dir)

    try:
        repo_root = script_dir.parent.parent
        relative_path = str(file_path.resolve().relative_to(repo_root))
    except ValueError:
        relative_path = str(file_path)

    if relative_path in ignore_list:
        print(f"Skipped (in ignore list): {file_path}")
        return 0

    if update_file_with_excerpt(file_path, excerpt):
        print(f"Updated: {file_path}")
        return 0
    else:
        print(f"Error: Could not update {file_path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
