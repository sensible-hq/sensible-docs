#!/usr/bin/env python3
"""
Copy metadata.description → excerpt for docs where excerpt is empty.

Does a targeted in-place replacement of the excerpt line so the rest of the
frontmatter is untouched. Skips files where excerpt is already set, or where
metadata.description is absent/empty.

Usage:
  python sync_excerpt.py           # write changes
  python sync_excerpt.py --dry-run # report without writing
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


def parse_frontmatter(content: str) -> dict | None:
    if not content.startswith("---"):
        return None
    end = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end:
        return None
    try:
        return yaml.safe_load(content[3 : end.start() + 3]) or {}
    except yaml.YAMLError:
        return None


def yaml_scalar(value: str) -> str:
    """Return the YAML representation of value as a bare scalar (no key, no newline)."""
    dumped = yaml.dump({"k": value}, default_flow_style=False, allow_unicode=True)
    # dumped is "k: value\n" or "k: 'value with: colon'\n"
    return dumped.split(": ", 1)[1].rstrip("\n")


def sync_excerpt(path: Path, dry_run: bool) -> bool:
    """Return True if the file was (or would be) updated."""
    content = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    if fm is None:
        return False

    description = (fm.get("metadata") or {}).get("description") or ""
    if not description:
        return False

    excerpt = fm.get("excerpt", None)
    if excerpt:
        return False

    new_excerpt_line = f"excerpt: {yaml_scalar(description)}"
    new_content = re.sub(r"^excerpt:.*$", new_excerpt_line, content, count=1, flags=re.MULTILINE)

    if new_content == content:
        return False

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Copy metadata.description to excerpt")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    args = parser.parse_args()

    repo_root = find_repo_root()
    updated = []

    for md_path in sorted(repo_root.glob("docs/**/*.md")):
        if sync_excerpt(md_path, args.dry_run):
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
