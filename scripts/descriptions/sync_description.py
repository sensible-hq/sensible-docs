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


def with_description(metadata: dict | None, description: str) -> dict:
    """Return metadata with description set, in the shape ReadMe uses for every doc."""
    if metadata is None:
        return {"title": "", "description": description, "robots": "index"}
    if "description" in metadata:
        return {**metadata, "description": description}
    # Insert after title to keep ReadMe's key order.
    out = {}
    for key, value in metadata.items():
        out[key] = value
        if key == "title":
            out["description"] = description
    out.setdefault("description", description)
    return out


def with_hidden(fm: dict) -> dict:
    """Return fm with hidden: false added if absent, after deprecated/excerpt/title."""
    if "hidden" in fm:
        return fm
    after = next((k for k in ("deprecated", "excerpt", "title") if k in fm), None)
    out = {}
    for key, value in fm.items():
        out[key] = value
        if key == after:
            out["hidden"] = False
    out.setdefault("hidden", False)
    return out


def sync_description(path: Path, dry_run: bool) -> bool:
    """Return True if the file was (or would be) updated."""
    content = path.open(encoding="utf-8", newline="").read()
    fm, rest_start = parse_frontmatter(content)
    if fm is None:
        return False

    excerpt = fm.get("excerpt") or ""
    if not excerpt:
        return False

    metadata = fm.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        return False
    if (metadata or {}).get("description") == excerpt:
        return False

    fm["metadata"] = with_description(metadata, excerpt)
    fm = with_hidden(fm)

    new_front_matter = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False, width=float("inf"))
    if not dry_run:
        path.open("w", encoding="utf-8", newline="").write(f"---\n{new_front_matter}---\n{content[rest_start:]}")
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
