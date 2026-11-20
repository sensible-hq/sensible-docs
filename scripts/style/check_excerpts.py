#!/usr/bin/env python3
"""Check excerpts in docs pages: length, sync with metadata.description, and self-naming.

  python3 scripts/style/check_excerpts.py [file ...]     # default: every .md file under docs/

Flags:
  - an excerpt over 160 characters (the hard cap in scripts/descriptions/frontmatter.py), and, as a
    warning, over 150
  - metadata.description that differs from excerpt
  - an excerpt that names the page's own feature: the title followed by method, preprocessor,
    parameter, object, setting, or operator, or the title with its own capitalization as a name
    ("Use the Region method to…", "Region extracts…")

The self-naming check applies to SenseML element pages only (not concepts/ or other sections). Skips
hidden pages, index.md, and pages without an excerpt. Prints path: [error|warning] message and
exits 1 on any error. Registry rules: sensible-excerpt-length, sensible-excerpt-self-naming.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
HARD, SOFT = 160, 150
KINDS = r"(?:method|preprocessor|computed field method|parameter|object|setting|operator|postprocessor)"


def frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return None


def self_named(title: str, excerpt: str) -> bool:
    """Whether the excerpt names the page's own feature."""
    t = re.escape(title.strip())
    if re.search(rf"\b{t}\s+{KINDS}\b", excerpt, re.I):
        return True
    # A multi-word or capitalized title used as a proper name, not as an ordinary word at the start
    # of the sentence: "Use the Region method", "Query Group extracts".
    if " " in title.strip() or title[:1].isupper():
        for m in re.finditer(rf"\b{t}\b", excerpt):
            if m.start() > 0 or " " in title.strip():
                return True
    return False


def element_page(rel: str) -> bool:
    """SenseML element pages (methods, preprocessors, settings, objects), where the excerpt must not
    name the page's own feature. Concept and overview pages name their topic, which is fine."""
    return rel.startswith("docs/Senseml reference/") and "/concepts/" not in rel


def check(path: Path) -> list[tuple[str, str]]:
    fm = frontmatter(path.read_text())
    if not fm or fm.get("hidden") or path.name == "index.md":
        return []
    rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    excerpt = str(fm.get("excerpt") or "").strip()
    if not excerpt:
        return []
    out = []
    if len(excerpt) > HARD:
        out.append(("error", f"excerpt is {len(excerpt)} characters (cap {HARD})"))
    elif len(excerpt) > SOFT:
        out.append(("warning", f"excerpt is {len(excerpt)} characters (target {SOFT})"))
    desc = str((fm.get("metadata") or {}).get("description") or "").strip()
    if desc != excerpt:
        out.append(("error", "metadata.description differs from excerpt; set both together"))
    title = str(fm.get("title") or "")
    if title and element_page(rel) and self_named(title, excerpt):
        out.append(("warning", f"excerpt names the page's own feature ({title!r}); the title already does"))
    return out


def main(argv):
    files = [Path(a).resolve() for a in argv] or sorted((ROOT / "docs").rglob("*.md"))
    errors = 0
    for f in files:
        if f.suffix != ".md" or not f.is_file():
            continue
        rel = f.relative_to(ROOT) if f.is_relative_to(ROOT) else f
        for level, msg in check(f):
            errors += level == "error"
            print(f"{rel}: [{level}] {msg}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
