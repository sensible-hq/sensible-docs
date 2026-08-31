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


def yaml_scalar(value: str) -> str:
    """Return the YAML scalar representation of value (no key, no trailing newline)."""
    dumped = yaml.dump({"k": value}, default_flow_style=False, allow_unicode=True)
    return dumped.split(": ", 1)[1].rstrip("\n")


def update_file_with_excerpt(file_path: Path, excerpt: str) -> bool:
    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return False

    end_match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end_match:
        return False

    new_excerpt_line = f"excerpt: {yaml_scalar(excerpt)}"

    # If excerpt key already exists, do a targeted in-place replacement.
    if re.search(r"^excerpt:", content, flags=re.MULTILINE):
        new_content = re.sub(r"^excerpt:.*$", new_excerpt_line, content, count=1, flags=re.MULTILINE)
        file_path.write_text(new_content, encoding="utf-8")
        return True

    # excerpt key is absent — insert it after the title line.
    new_content = re.sub(r"^(title:.*)$", rf"\1\n{new_excerpt_line}", content, count=1, flags=re.MULTILINE)
    if new_content == content:
        return False

    file_path.write_text(new_content, encoding="utf-8")
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
