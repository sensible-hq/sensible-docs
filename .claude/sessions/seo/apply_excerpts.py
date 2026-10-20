#!/usr/bin/env python3
"""Apply the reviewed "Proposed excerpt" from keywords-draft.md to each page's frontmatter.

Deterministic: reads each `### <n>. <title>` block in the draft, takes its `File:` path and the
line after `#### Proposed excerpt`, and sets `excerpt` and `metadata.description` to that text.
Text-level edit: only those two values change; other frontmatter keys, the body, and line endings
are preserved. Pages without an `excerpt` key (spec-generated reference pages) are skipped.

Usage (from the repo root):
  python3 .claude/sessions/seo/apply_excerpts.py            # dry run
  python3 .claude/sessions/seo/apply_excerpts.py --write
"""
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[3]
DRAFT = Path(__file__).with_name("keywords-draft.md")
MAX_LENGTH = 160  # hard cap (scripts/descriptions/frontmatter.py); target <= 150
WRITE = "--write" in sys.argv


def parse_draft():
    pages, n, path, lines = [], None, None, DRAFT.read_text(encoding="utf-8").split("\n")
    for i, line in enumerate(lines):
        if m := re.match(r"^### (\d+)\. ", line):
            n, path = int(m.group(1)), None
        elif n is not None and line.startswith("File: "):
            path = re.search(r"`([^`]+)`", line).group(1)
            path = path if path.startswith("reference/") else "docs/" + path
        elif n is not None and line.startswith("#### Proposed excerpt"):
            pages.append((n, path, lines[i + 1].strip()))
    return pages


def replace_value(fm_text, key_re, indent, new, nl):
    """Replace the scalar for the key on the line matching key_re (plain, quoted, or folded)."""
    lines = fm_text.split(nl)
    for i, line in enumerate(lines):
        if re.match(key_re, line):
            j = i + 1
            while j < len(lines) and lines[j].strip() and len(lines[j]) - len(lines[j].lstrip(" ")) > indent:
                j += 1
            key = line.strip().split(":")[0]
            dumped = yaml.safe_dump({key: new}, width=10_000, allow_unicode=True).rstrip("\n")
            lines[i:j] = [" " * indent + dumped]
            return nl.join(lines), True
    return fm_text, False


def main():
    pages = parse_draft()
    assert len(pages) == len({n for n, _, _ in pages}), "duplicate page numbers in draft"
    changed = skipped = 0
    for n, rel, new in sorted(pages):
        assert len(new) <= MAX_LENGTH, f"#{n} is {len(new)} chars"
        path = REPO / rel
        with open(path, encoding="utf-8", newline="") as f:
            raw = f.read()
        _, fm_text, body = raw.split("---", 2)
        old = yaml.safe_load(fm_text) or {}
        if "excerpt" not in old:
            print(f"SKIP #{n} {rel}: no excerpt key (spec-generated)")
            skipped += 1
            continue
        nl = "\r\n" if "\r\n" in fm_text else "\n"
        fm2, _ = replace_value(fm_text, r"^excerpt:", 0, new, nl)
        if "description" in (old.get("metadata") or {}):
            fm2, _ = replace_value(fm2, r"^  description:", 2, new, nl)
        check = yaml.safe_load(fm2)
        assert check["excerpt"] == new, rel
        assert all(check[k] == old[k] for k in old if k not in ("excerpt", "metadata")), rel
        om, cm = old.get("metadata") or {}, check.get("metadata") or {}
        assert all(cm[k] == om[k] for k in om if k != "description"), rel
        if "description" in om:
            assert cm["description"] == new, rel
        if old["excerpt"] == new and om.get("description", new) == new:
            continue
        changed += 1
        print(f"#{n:>2} [{len(new):>3}] {rel}")
        if WRITE:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write("---" + fm2 + "---" + body)
    print(f"{'Changed' if WRITE else 'Would change'}: {changed}; skipped: {skipped}")


if __name__ == "__main__":
    main()
