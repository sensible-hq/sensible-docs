#!/usr/bin/env python3
"""List SenseML parameters whose descriptions differ from page to page.

  python3 scripts/style/compare_param_descriptions.py [--key KEY]

Reads every parameter table (header row starting `| key |` or `| id |`) under docs/Senseml reference/,
groups rows by parameter key, and prints each key whose description isn't identical on every page,
with a similarity score. This is the detector for the judgment rule sensible-copy-sibling-wording:
only the engine source says whether two parameters share an implementation, and only then should
the wording match word for word. Report only; always exits 0.
"""
import argparse
import difflib
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / "docs/Senseml reference"
HEADER = re.compile(r"^\|\s*(key|id)\s*\|", re.I)
GLOBAL = re.compile(r"For information about this global parameter", re.I)


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def key_name(cell: str) -> str:
    cell = re.sub(r"\*\*\(?Deprecated\)?\*\*|\(\*\*required\*\*\)|`", "", cell, flags=re.I)
    return cell.strip().split()[0] if cell.strip() else ""


def tables(path: Path):
    lines = path.read_text().splitlines()
    i = 0
    while i < len(lines):
        if HEADER.match(lines[i]):
            i += 2
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                row = cells(lines[i])
                if len(row) >= 3 and key_name(row[0]) and not GLOBAL.search(row[2]):
                    yield key_name(row[0]), row[2], i + 1
                i += 1
        i += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key")
    a = ap.parse_args()
    seen = defaultdict(list)
    for path in sorted(REF.rglob("*.md")):
        if path.name.startswith("draft-"):
            continue
        for key, desc, line in tables(path):
            seen[key].append((str(path.relative_to(ROOT)), line, desc))
    differing = 0
    for key in sorted(seen):
        if a.key and key != a.key:
            continue
        rows = seen[key]
        descs = {d for _, _, d in rows}
        if len(rows) < 2 or len(descs) < 2:
            continue
        differing += 1
        base = rows[0][2]
        print(f"\n{key}: {len(rows)} pages, {len(descs)} wordings")
        for path, line, desc in rows:
            ratio = difflib.SequenceMatcher(None, base, desc).ratio()
            print(f"  {ratio:4.2f}  {path}:{line}  {desc[:110]}")
    print(f"\n{differing} parameters have more than one wording")


if __name__ == "__main__":
    main()
