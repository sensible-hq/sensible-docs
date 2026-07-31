#!/usr/bin/env python3
"""
Generate llms.txt from _order.yaml files in docs/ and reference/.

This repo is a ReadMe.com-managed docs site. ReadMe uses _order.yaml files
in each directory to control sidebar navigation order. Those same files are
used here as the source of truth for what goes in llms.txt and in what order,
so the two stay in sync without a separate manifest.

Files with `hidden: true` in frontmatter are excluded — ReadMe hides those
pages from its published nav, so they shouldn't appear in llms.txt either.
Descriptions come from `metadata.description` in frontmatter, which is also
what ReadMe surfaces in search results and SEO meta tags.

Structure:
  - docs/_order.yaml top-level categories  → ## sections
  - reference/openapi_*.json spec files     → ## api reference > spec links
  - all pages within a category are flat bullet list entries (no subheadings)
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

HEADER = """\
# Sensible

> Sensible is a developer-first platform for extracting structured data from documents, including PDFs, emails, spreadsheets, and images. Use Sensible to build document-automation features into your vertical SaaS products.

This file contains links to the Sensible documentation to help LLMs understand the platform.

## Instructions for AI Agents

- For clean Markdown of any page, append `.md` to the page URL
"""

# docs/_order.yaml lists a "llms.txt" category that is the source file for
# this script's output — skip it to avoid a self-referential entry.
DOCS_SKIP = {"llms.txt"}

# reference/_order.yaml contains several categories that aren't real API docs:
# - ReadMeConfig: a platform config folder ReadMe uses internally, not a doc page
# - SenseML: a redirect stub ReadMe uses to link its sidebar to the SenseML
#   reference in docs/; the actual SenseML content lives under docs/Senseml reference/
# - MCP Server: the _order.yaml for this category is empty because it was
#   auto-committed by ReadMe's GitHub sync when the page was created in the UI,
#   and the slug was placed in the root _order.yaml instead of here
REFERENCE_SKIP = {"ReadMeConfig", "SenseML", "MCP Server"}

# ReadMe doesn't expose a public (unauthenticated) download URL for uploaded
# specs — the reference UI itself links to these raw GitHub URLs. Specs are
# discovered dynamically by globbing reference/openapi_*.json so new specs
# are picked up automatically without touching this file.
OPENAPI_BASE_URL = "https://raw.githubusercontent.com/sensible-hq/sensible-docs/refs/heads/v0/reference"


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
    """Return page info for a .md file, or None if the page should be excluded."""
    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception:
        return None
    fm = parse_front_matter(content)
    # ReadMe sets hidden: true on draft pages and pages intentionally omitted
    # from the published nav (e.g. cheat sheets, deprecated methods). Mirror
    # that here so LLMs aren't pointed at unpublished or intentionally obscured content.
    if fm.get("hidden") is True:
        return None
    rel_path = quote(str(md_path.relative_to(repo_root)), safe="/")
    # Fall back to a title derived from the filename if the page has no title
    # frontmatter, which can happen for stub or auto-generated pages.
    title = fm.get("title") or md_path.stem.replace("-", " ").title()
    # metadata.description is the ReadMe field that also drives SEO meta tags
    # and search result snippets, so it's the right description to surface here.
    description = (fm.get("metadata") or {}).get("description") or ""
    return {"path": rel_path, "title": title, "description": description}


def format_entry(path: str, title: str, description: str) -> str:
    if description:
        return f"- [{title}]({path}): {description}"
    return f"- [{title}]({path})"


def read_order(order_path: Path) -> list[str]:
    # Silently returns [] for missing or malformed files so callers don't need
    # to check existence — stale slugs in _order.yaml just resolve to nothing.
    try:
        slugs = yaml.safe_load(order_path.read_text(encoding="utf-8")) or []
        return [s for s in slugs if isinstance(s, str)]
    except Exception:
        return []


def resolve_slug(slug: str, parent_dir: Path) -> Path | None:
    """Resolve a ReadMe slug to a .md file or subdirectory.

    ReadMe slugs are bare filenames without the .md extension, or directory
    names for nested category groups. The special slug "index" maps to the
    index.md landing page of a directory. We check .md first, then directory —
    this mirrors ReadMe's own resolution order.
    """
    if slug == "index":
        f = parent_dir / "index.md"
        return f if f.exists() else None
    md = parent_dir / f"{slug}.md"
    if md.exists():
        return md
    # A slug that resolves to a directory is a nested category with its own
    # _order.yaml. ReadMe renders these as collapsible groups in the sidebar.
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
            # ReadMe treats each category's index.md as its implicit overview page —
            # it's never listed in _order.yaml, but it exists and is published.
            # Include it first so the overview page leads the section's entries.
            index_md = resolved / "index.md"
            if index_md.exists():
                info = get_page_info(index_md, repo_root)
                if info:
                    lines.append(format_entry(**info))
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
        entries = collect_entries(cat_dir / "_order.yaml", repo_root)
        if entries:
            result.append((cat_dir.name, entries))
    return result


def collect_openapi_specs(repo_root: Path) -> list[str]:
    """Return llms.txt entries for each openapi_*.json file in reference/, sorted by name."""
    lines = []
    for spec_path in sorted((repo_root / "reference").glob("openapi_*.json")):
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            title = spec.get("info", {}).get("title") or spec_path.stem
        except Exception:
            title = spec_path.stem
        url = f"{OPENAPI_BASE_URL}/{spec_path.name}"
        lines.append(f"- [{title}]({url}): OpenAPI specification")
    return lines


def generate(repo_root: Path) -> str:
    lines = [HEADER]

    # docs/ contains conceptual guides, tutorials, and the SenseML reference.
    # Each top-level category gets its own ## heading so the broad topic areas
    # (integrations, document extraction, etc.) are clear.
    for name, entries in collect_categories(
        repo_root / "docs", repo_root / "docs" / "_order.yaml", DOCS_SKIP, repo_root
    ):
        lines.append(f"## {name.lower()}")
        lines.append("")
        lines.extend(entries)
        lines.append("")

    # reference/ is a separate ReadMe UI from docs/ — it has its own navigation
    # and doesn't share a table of contents with docs/. Users move between the
    # two via top-level breadcrumbs, not the sidebar. Link to the OpenAPI specs
    # directly rather than individual pages so LLMs get machine-readable definitions.
    spec_lines = collect_openapi_specs(repo_root)
    if spec_lines:
        lines.append("## api reference")
        lines.append("")
        lines.append("The Sensible API is described by the following OpenAPI specifications:")
        lines.append("")
        lines.extend(spec_lines)

    return "\n".join(lines).rstrip() + "\n"


def check_order(order_path: Path, repo_root: Path) -> list[str]:
    """Recursively validate an _order.yaml file, returning a list of issue strings."""
    issues = []
    parent_dir = order_path.parent
    for slug in read_order(order_path):
        resolved = resolve_slug(slug, parent_dir)
        if resolved is None:
            issues.append(f"{order_path.relative_to(repo_root)}: '{slug}' does not resolve to a file or directory")
        elif resolved.is_dir():
            issues.extend(check_order(resolved / "_order.yaml", repo_root))
    return issues


def check(repo_root: Path) -> list[str]:
    """Validate all _order.yaml files and return a list of issue strings.

    Catches two failure modes:
    1. A top-level category slug points to a directory that doesn't exist —
       the whole section silently vanishes from llms.txt (e.g. 'Email extraction'
       after the directory was moved or renamed).
    2. A slug within any _order.yaml doesn't resolve to a file or directory —
       the page silently drops out of llms.txt without any error.
    """
    issues = []

    for root_dir, order_path, skip in [
        (repo_root / "docs",      repo_root / "docs" / "_order.yaml",      DOCS_SKIP),
        (repo_root / "reference", repo_root / "reference" / "_order.yaml", REFERENCE_SKIP),
    ]:
        for slug in read_order(order_path):
            if slug in skip:
                continue
            cat_dir = root_dir / slug
            if not cat_dir.is_dir():
                issues.append(f"{order_path.relative_to(repo_root)}: '{slug}' does not resolve to a directory")
            else:
                issues.extend(check_order(cat_dir / "_order.yaml", repo_root))

    return issues


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
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate _order.yaml files and exit nonzero if any slugs don't resolve",
    )
    args = parser.parse_args()

    repo_root = find_repo_root()

    if args.check:
        issues = check(repo_root)
        if issues:
            print(f"Found {len(issues)} unresolved slug(s):")
            for issue in issues:
                print(f"  {issue}")
            return 1
        print("All _order.yaml slugs resolve correctly")
        return 0

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
