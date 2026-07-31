#!/usr/bin/env python3
"""
Generate llms.txt from _order.yaml files in docs/ and reference/.

_order.yaml files are the source of truth for page inventory and order.
Files with `hidden: true` in frontmatter are excluded.
Descriptions are read from `metadata.description` in frontmatter.

Structure:
  - docs/_order.yaml top-level categories  → ## sections
  - reference/_order.yaml categories        → ## API Reference > ### subsections
  - subdirectory slugs within any section  → next heading level
  - leaf .md slugs                         → bullet list entries
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

HEADER = """\
# Sensible

> Sensible is a developer-first platform for extracting structured data from documents, including PDFs, emails, spreadsheets, and images. Use Sensible to build document-automation features into your vertical SaaS products.

This file contains links to the Sensible documentation to help LLMs understand the platform.
"""

# Top-level slugs in docs/_order.yaml to skip
DOCS_SKIP = {"llms.txt"}

# Top-level slugs in reference/_order.yaml to skip (ReadMe.com config, not docs)
REFERENCE_SKIP = {"ReadMeConfig"}


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


def format_title(name: str) -> str:
    """Convert a directory/slug name to a lowercase section title."""
    return name.replace("-", " ").lower()


def url_encode_path(rel_path: str) -> str:
    return rel_path.replace(" ", "%20")


def get_page_info(md_path: Path, repo_root: Path) -> dict | None:
    """Read a .md file and return page info, or None if the page is hidden."""
    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception:
        return None
    fm = parse_front_matter(content)
    if fm.get("hidden") is True:
        return None
    rel_path = str(md_path.relative_to(repo_root))
    title = fm.get("title") or md_path.stem.replace("-", " ").title()
    description = (fm.get("metadata") or {}).get("description") or ""
    return {"path": rel_path, "title": title, "description": description}


def format_entry(path: str, title: str, description: str) -> str:
    encoded = url_encode_path(path)
    if description:
        return f"- [{title}]({encoded}): {description}"
    return f"- [{title}]({encoded})"


def read_order(order_path: Path) -> list[str]:
    try:
        slugs = yaml.safe_load(order_path.read_text(encoding="utf-8")) or []
        return [s for s in slugs if isinstance(s, str)]
    except Exception:
        return []


def resolve_slug(slug: str, parent_dir: Path) -> Path | None:
    """Resolve a slug to a .md file or subdirectory."""
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


def generate_entries(
    order_path: Path,
    repo_root: Path,
    heading_level: int,
    skip: set[str] | None = None,
) -> list[str]:
    """
    Recursively process an _order.yaml and return llms.txt lines.

    Collects child lines before emitting a section heading so sections with
    no visible pages are suppressed entirely.
    heading_level is the Markdown heading depth for subdirectory sections.
    """
    lines = []
    skip = skip or set()
    parent_dir = order_path.parent

    for slug in read_order(order_path):
        if slug in skip:
            continue

        resolved = resolve_slug(slug, parent_dir)
        if resolved is None:
            continue

        if resolved.is_dir():
            sub_order = resolved / "_order.yaml"
            sub_lines = (
                generate_entries(sub_order, repo_root, heading_level + 1)
                if sub_order.exists()
                else []
            )
            if sub_lines:
                lines.append("")
                lines.append("#" * heading_level + " " + format_title(resolved.name))
                lines.append("")
                lines.extend(sub_lines)
        else:
            info = get_page_info(resolved, repo_root)
            if info:
                lines.append(format_entry(**info))

    return lines


def generate(repo_root: Path) -> str:
    lines = [HEADER]

    # docs/ section: each top-level category → ## heading
    docs_order = repo_root / "docs" / "_order.yaml"
    for slug in read_order(docs_order):
        if slug in DOCS_SKIP:
            continue
        cat_dir = repo_root / "docs" / slug
        if not cat_dir.is_dir():
            continue
        cat_order = cat_dir / "_order.yaml"
        cat_lines = generate_entries(cat_order, repo_root, heading_level=3) if cat_order.exists() else []
        if cat_lines:
            lines.append(f"## {format_title(cat_dir.name)}")
            lines.append("")
            lines.extend(cat_lines)
            lines.append("")

    # reference/ section: single ## heading, categories as ###
    ref_order = repo_root / "reference" / "_order.yaml"
    ref_lines = []
    for slug in read_order(ref_order):
        if slug in REFERENCE_SKIP:
            continue
        cat_dir = repo_root / "reference" / slug
        if not cat_dir.is_dir():
            continue
        cat_order = cat_dir / "_order.yaml"
        cat_lines = generate_entries(cat_order, repo_root, heading_level=4) if cat_order.exists() else []
        if cat_lines:
            ref_lines.append(f"### {format_title(cat_dir.name)}")
            ref_lines.append("")
            ref_lines.extend(cat_lines)
            ref_lines.append("")

    if ref_lines:
        lines.append("## api reference")
        lines.append("")
        lines.extend(ref_lines)

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
