#!/usr/bin/env python3
"""
Generate llms.txt from _order.yaml files in docs/ and reference/.

_order.yaml files are the source of truth for page inventory and order.
Files with `hidden: true` in frontmatter are excluded.
Descriptions are read from `metadata.description` in frontmatter.

Structure:
  - docs/_order.yaml top-level categories  → ## sections
  - reference/_order.yaml categories        → ## api reference > flat entries
  - all pages within a category are flat bullet list entries (no subheadings)
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

HEADER = """\
# Sensible

> Sensible is a developer-first platform for extracting structured data from documents, including PDFs, emails, spreadsheets, and images. Use Sensible to build document-automation features into your vertical SaaS products.

This file contains links to the Sensible documentation to help LLMs understand the platform.
"""

# Top-level slugs in docs/_order.yaml to skip
DOCS_SKIP = {"llms.txt"}

# Top-level slugs in reference/_order.yaml to skip.
# ReadMeConfig is a platform config folder, not docs.
# SenseML and MCP Server are ReadMe.com linking artifacts with no real content.
REFERENCE_SKIP = {"ReadMeConfig", "SenseML", "MCP Server"}


def parse_front_matter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    end = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end:
        return {}
    try:
        return yaml.safe_load(content[3 : end.start() + 3]) or {}
    except yaml.YAMLError:
        return {}


def get_page_info(md_path: Path, repo_root: Path) -> dict | None:
    """Return page info for a .md file, or None if the page is hidden."""
    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception:
        return None
    fm = parse_front_matter(content)
    # hidden: true means the page is excluded from ReadMe.com's published nav;
    # we mirror that exclusion in llms.txt so LLMs don't get sent to unpublished pages
    if fm.get("hidden") is True:
        return None
    rel_path = quote(str(md_path.relative_to(repo_root)), safe="/")
    title = fm.get("title") or md_path.stem.replace("-", " ").title()
    description = (fm.get("metadata") or {}).get("description") or ""
    return {"path": rel_path, "title": title, "description": description}


def format_entry(path: str, title: str, description: str) -> str:
    if description:
        return f"- [{title}]({path}): {description}"
    return f"- [{title}]({path})"


def read_order(order_path: Path) -> list[str]:
    # Returns [] on any read/parse error so callers can treat missing files as empty
    try:
        slugs = yaml.safe_load(order_path.read_text(encoding="utf-8")) or []
        return [s for s in slugs if isinstance(s, str)]
    except Exception:
        return []


def resolve_slug(slug: str, parent_dir: Path) -> Path | None:
    """Resolve a slug to a .md file or subdirectory, in that priority order."""
    if slug == "index":
        f = parent_dir / "index.md"
        return f if f.exists() else None
    md = parent_dir / f"{slug}.md"
    if md.exists():
        return md
    d = parent_dir / slug
    if d.is_dir():
        return d
    return None


def collect_entries(order_path: Path, repo_root: Path) -> list[str]:
    """Recursively collect all visible page entries from an _order.yaml tree, flat."""
    lines = []
    parent_dir = order_path.parent
    for slug in read_order(order_path):
        resolved = resolve_slug(slug, parent_dir)
        if resolved is None:
            continue
        if resolved.is_dir():
            # read_order silently returns [] for a missing _order.yaml, so no exists() check needed
            lines.extend(collect_entries(resolved / "_order.yaml", repo_root))
        else:
            info = get_page_info(resolved, repo_root)
            if info:
                lines.append(format_entry(**info))
    return lines


def collect_categories(
    root_dir: Path, order_path: Path, skip: set[str], repo_root: Path
) -> list[tuple[str, list[str]]]:
    """Return [(category_name, entry_lines), ...] for each non-empty category under root_dir."""
    result = []
    for slug in read_order(order_path):
        if slug in skip:
            continue
        cat_dir = root_dir / slug
        if not cat_dir.is_dir():
            continue
        # read_order handles missing _order.yaml gracefully, so no exists() check needed
        entries = collect_entries(cat_dir / "_order.yaml", repo_root)
        if entries:
            result.append((cat_dir.name, entries))
    return result


def generate(repo_root: Path) -> str:
    lines = [HEADER]

    # docs/: each category gets its own ## heading
    for name, entries in collect_categories(
        repo_root / "docs", repo_root / "docs" / "_order.yaml", DOCS_SKIP, repo_root
    ):
        lines.append(f"## {name.lower()}")
        lines.append("")
        lines.extend(entries)
        lines.append("")

    # reference/: all categories collapsed under a single ## heading
    ref_categories = collect_categories(
        repo_root / "reference", repo_root / "reference" / "_order.yaml", REFERENCE_SKIP, repo_root
    )
    ref_entries = [entry for _, entries in ref_categories for entry in entries]
    if ref_entries:
        lines.append("## api reference")
        lines.append("")
        lines.extend(ref_entries)

    return "\n".join(lines).rstrip() + "\n"


def find_repo_root() -> Path:
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "docs").is_dir() and (candidate / "reference").is_dir():
        return candidate
    cwd = Path.cwd()
    if (cwd / "docs").is_dir() and (cwd / "reference").is_dir():
        return cwd
    raise SystemExit("Could not find repo root (expected docs/ and reference/ directories)")


def main():
    parser = argparse.ArgumentParser(description="Generate llms.txt from _order.yaml files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated content without writing to disk",
    )
    args = parser.parse_args()

    repo_root = find_repo_root()
    content = generate(repo_root)

    if args.dry_run:
        print(content, end="")
        return 0

    llms_path = repo_root / "llms.txt"
    existing = llms_path.read_text(encoding="utf-8") if llms_path.exists() else ""
    if content == existing:
        print("llms.txt is already up to date")
        return 0

    llms_path.write_text(content, encoding="utf-8")
    print(f"Generated llms.txt ({len(content.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
