#!/usr/bin/env python3
"""
Copy excerpt → metadata.description for docs where they differ.

excerpt is the source of truth. This script propagates any excerpt value
into metadata.description, overwriting whatever was there before, and creates
the metadata block if it's absent. Skips files where excerpt is absent or
empty, or where metadata.description is already in sync.

Usage:
  python sync_description.py           # write changes
  python sync_description.py --dry-run # report without writing
"""

import argparse
import sys
from pathlib import Path

import frontmatter


def sync_description(path: Path, dry_run: bool) -> bool:
    """Return True if the file was (or would be) updated."""
    doc = frontmatter.read(path)
    if doc.fm is None:
        return False

    excerpt = doc.fm.get("excerpt")
    if not excerpt or not isinstance(excerpt, str):
        return False
    metadata = doc.fm.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        return False
    if frontmatter.get_description(doc.fm) == excerpt:
        return False

    if not dry_run:
        frontmatter.write(doc, frontmatter.set_description(doc.fm, excerpt))
    return True


def main():
    parser = argparse.ArgumentParser(description="Copy excerpt to metadata.description")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    args = parser.parse_args()

    updated = [rel for path, rel in frontmatter.iter_docs(frontmatter.find_repo_root()) if sync_description(path, args.dry_run)]

    if not updated:
        print("Nothing to update.")
        return 0

    label = "Would update" if args.dry_run else "Updated"
    for rel in updated:
        print(f"{label}: {rel}")
    print(f"\n{label} {len(updated)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
