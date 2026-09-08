#!/usr/bin/env python3
"""
Copy excerpt → metadata.description for docs where they differ.

excerpt is the source of truth. This script propagates any excerpt value
into metadata.description, overwriting whatever was there before.
Skips files where excerpt is absent or empty, or where metadata.description
is already in sync.

Usage:
  python sync_description.py           # write changes
  python sync_description.py --dry-run # report without writing
"""

import argparse
import re
import sys
from pathlib import Path

import yaml


def find_repo_root() -> Path:
    candidate = Path(__file__).resolve().parent.parent.parent
    if (candidate / "docs").is_dir():
        return candidate
    cwd = Path.cwd()
    if (cwd / "docs").is_dir():
        return cwd
    raise SystemExit("Could not find repo root (expected docs/ directory)")


def parse_frontmatter(content: str) -> tuple[dict | None, int]:
    """Return (parsed front matter, end offset) or (None, -1) on failure."""
    if not content.startswith("---"):
        return None, -1
    end = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end:
        return None, -1
    try:
        fm = yaml.safe_load(content[3 : end.start() + 3]) or {}
        return fm, end.end() + 3
    except yaml.YAMLError:
        return None, -1


def sync_description(path: Path, dry_run: bool) -> bool:
    """Return True if the file was (or would be) updated."""
    content = path.read_text(encoding="utf-8")
    fm, rest_start = parse_frontmatter(content)
    if fm is None:
        return False

    excerpt = fm.get("excerpt") or ""
    if not excerpt:
        return False

    metadata = fm.get("metadata") or {}
    if not isinstance(metadata, dict):
        return False

    if metadata.get("description") == excerpt:
        return False

    fm["metadata"]["description"] = excerpt

    new_front_matter = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    if not dry_run:
        path.write_text(f"---\n{new_front_matter}---\n{content[rest_start:]}", encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Copy excerpt to metadata.description")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    args = parser.parse_args()

    repo_root = find_repo_root()
    updated = []

    for md_path in sorted(repo_root.glob("docs/**/*.md")):
        if sync_description(md_path, args.dry_run):
            updated.append(md_path.relative_to(repo_root))

    if not updated:
        print("Nothing to update.")
        return 0

    label = "Would update" if args.dry_run else "Updated"
    for p in updated:
        print(f"{label}: {p}")
    print(f"\n{label} {len(updated)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
