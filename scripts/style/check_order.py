#!/usr/bin/env python3
"""Check that every docs page and subdirectory appears in its directory's _order.yaml.

  python3 scripts/style/check_order.py

ReadMe orders the sidebar from _order.yaml. A page missing from it still syncs but lands in an
arbitrary position. Prints each page or directory left out, and each _order.yaml entry with no
matching page, and exits 1 if there are any. index.md and draft-* pages are exempt. Directories without
an _order.yaml are skipped.
Registry rule: sensible-order-registration.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def main():
    problems = []
    for order in sorted((ROOT / "docs").rglob("_order.yaml")):
        d = order.parent
        listed = [str(x) for x in (yaml.safe_load(order.read_text()) or [])]
        # index.md is the category page, and draft-* pages are hidden; ReadMe places both itself.
        present = ({p.stem for p in d.glob("*.md") if p.stem != "index" and not p.stem.startswith("draft-")}
                   | {p.name for p in d.iterdir() if p.is_dir()})
        rel = order.relative_to(ROOT)
        for name in sorted(present - set(listed)):
            problems.append(f"{rel}: missing {name}")
        for name in listed:
            if name not in present and not (d / f"{name}.md").exists():
                problems.append(f"{rel}: lists {name}, which doesn't exist")
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
