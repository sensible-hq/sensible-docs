#!/usr/bin/env python3
"""Style screenshots into the final images the docs use, restyling only what changed.

Each PNG in assets/images/screenshots/ (top level only) gets a styled copy with the same name in
assets/images/final/. assets/images/final/.sources.json maps each styled image to the SHA-256 of
the screenshot it was styled from. A run:

1. restyles every screenshot whose hash differs from the mapping, or whose styled copy is missing;
2. deletes the styled copy of every screenshot that no longer exists, and drops it from the mapping;
3. writes the mapping.

Only styled images listed in the mapping are ever deleted. Images placed directly in final/,
without a screenshot, are never touched. Output is deterministic (no embedded timestamps), so
restyling an unchanged screenshot produces identical bytes.

With no mapping yet (the first run), every screenshot is restyled.

Usage: style_images.py [--root REPO_ROOT] [--dry-run]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

SCREENSHOTS = Path("assets/images/screenshots")
FINAL = Path("assets/images/final")
MAPPING = FINAL / ".sources.json"

# Drop shadow, as before. -strip and the excluded chunks drop timestamps, so output is reproducible.
STYLE_ARGS = [
    "-bordercolor", "white", "-border", "0",
    "(", "+clone", "-background", "black", "-shadow", "80x3+2+2", ")",
    "+swap", "-background", "white", "-layers", "merge", "+repage",
    "-strip", "-define", "png:exclude-chunks=date,time",
]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_mapping(path):
    if not path.exists():
        return {}
    try:
        mapping = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"error: {path} is not valid JSON ({e}). Fix or delete it; deleting restyles every image.")
    if not isinstance(mapping, dict):
        sys.exit(f"error: {path} must be a JSON object of image name -> source SHA-256")
    return mapping


def style(convert, src, dst):
    subprocess.run([convert, str(src), *STYLE_ARGS, str(dst)], check=True)


def sync(root, dry_run=False, convert=None):
    """Returns (styled, deleted) image names."""
    convert = convert or os.environ.get("STYLE_IMAGES_CONVERT", "convert")
    screenshots, final, mapping_path = root / SCREENSHOTS, root / FINAL, root / MAPPING
    mapping = load_mapping(mapping_path)
    updated = dict(mapping)

    sources = sorted(p for p in screenshots.glob("*.png") if p.is_file())
    styled = []
    for src in sources:
        digest = sha256(src)
        dst = final / src.name
        if updated.get(src.name) != digest or not dst.exists():
            if not dry_run:
                style(convert, src, dst)
            updated[src.name] = digest
            styled.append(src.name)

    names = {p.name for p in sources}
    deleted = []
    for name in sorted(set(updated) - names):
        if not dry_run:
            (final / name).unlink(missing_ok=True)
        del updated[name]
        deleted.append(name)

    if not dry_run and updated != mapping:
        mapping_path.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n")
    return styled, deleted


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path("."), help="repo root (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", help="report what would change; write nothing")
    args = parser.parse_args()
    styled, deleted = sync(args.root, dry_run=args.dry_run)
    verb = "would " if args.dry_run else ""
    for name in styled:
        print(f"{verb}style {FINAL / name}")
    for name in deleted:
        print(f"{verb}delete {FINAL / name} (its screenshot was removed)")
    if args.dry_run:
        print(f"{len(styled)} to style, {len(deleted)} to delete")
    else:
        print(f"{len(styled)} styled, {len(deleted)} deleted")


if __name__ == "__main__":
    main()
