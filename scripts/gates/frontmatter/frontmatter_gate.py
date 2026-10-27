#!/usr/bin/env python3
"""Frontmatter gate: checks the `docops:` block in docs/**/*.md frontmatter.

Implements SPEC.md v0.1.0 in this folder; tests.yaml is the acceptance test.

Usage: frontmatter_gate.py [--root DIR] [--require] [--json]
Exit: 0 no errors, 1 at least one error, 2 the check couldn't run.
"""
import argparse
import json
import sys
from pathlib import Path

import yaml

PAGE_TYPES = ("tutorial", "how-to", "reference", "explanation")
DOCOPS_KEYS = ("page_type", "related")
MAX_RELATED = 5
BAD_SLUG_CHARS = (":", "#", "/")


class Page:
    def __init__(self, path, slug):
        self.path = path          # repo-relative, '/'-separated
        self.slug = slug
        self.related = []         # valid, distinct, non-self entries, in order
        self.related_all = set()  # every string entry of a well-formed list (for symmetry)


def slug_for(rel_path):
    parts = rel_path.split("/")
    stem = parts[-1][: -len(".md")]
    if stem == "index" and len(parts) >= 2:
        return parts[-2]
    return stem


def as_subject(value):
    """Render a YAML value as a string subject."""
    if isinstance(value, str):
        return value
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, default=str, sort_keys=True, ensure_ascii=False)


def is_bare_slug(entry):
    if entry == "":
        return False
    if any(c in entry for c in BAD_SLUG_CHARS):
        return False
    return not any(c.isspace() for c in entry)


def read_frontmatter(text):
    """Return the frontmatter text, or None if there is no well-formed --- block."""
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i] == "---":
            return "\n".join(lines[1:i])
    return None


def check_page(page, text, problems, require):
    def report(rule, subject=None, severity="error"):
        problems.add((page.path, rule, severity, subject))

    fm_text = read_frontmatter(text)
    if fm_text is None:
        report("no-frontmatter")
        return
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        report("bad-yaml")
        return
    if not isinstance(fm, dict):
        report("bad-yaml")
        return

    if "docops" not in fm:
        report("missing-docops", severity="error" if require else "warning")
        return
    docops = fm["docops"]
    if not isinstance(docops, dict):
        report("docops-not-mapping")
        return

    for key in docops:
        if key not in DOCOPS_KEYS:
            report("unknown-key", as_subject(key))

    if "page_type" not in docops:
        report("missing-page-type")
    else:
        page_type = docops["page_type"]
        if not (isinstance(page_type, str) and page_type in PAGE_TYPES):
            report("bad-page-type", as_subject(page_type))

    if "related" not in docops:
        return
    related = docops["related"]
    if not isinstance(related, list) or not all(isinstance(e, str) for e in related):
        report("related-not-list")
        return

    if len(related) > MAX_RELATED:
        report("related-too-many")

    seen = set()
    for entry in related:
        if not is_bare_slug(entry):
            report("related-not-slug", entry)
            continue
        page.related_all.add(entry)
        if entry in seen:
            report("related-duplicate", entry)
            continue
        seen.add(entry)
        if entry == page.slug:
            report("related-self", entry)
            continue
        page.related.append(entry)


def run(root, require):
    """Return (problems, page_count). Raises OSError/UnicodeDecodeError if a page can't be read."""
    docs = root / "docs"
    paths = sorted(
        p for p in docs.rglob("*.md") if p.is_file()
    )
    pages = []
    problems = set()
    for p in paths:
        rel = p.relative_to(root).as_posix()
        page = Page(rel, slug_for(rel))
        text = p.read_text(encoding="utf-8")
        check_page(page, text, problems, require)
        pages.append(page)

    by_slug = {}
    for page in pages:
        by_slug.setdefault(page.slug, []).append(page)
    for slug, group in by_slug.items():
        if len(group) > 1:
            for page in group:
                problems.add((page.path, "duplicate-slug", "error", slug))

    for page in pages:
        for slug in page.related:
            targets = by_slug.get(slug, [])
            if len(targets) != 1:
                problems.add((page.path, "related-unresolved", "error", slug))
            elif page.slug not in targets[0].related_all:
                problems.add((page.path, "related-asymmetric", "error", slug))

    return problems, len(pages)


def sort_key(problem):
    path, rule, _severity, subject = problem
    return (path, rule, (0, "") if subject is None else (1, subject))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check docops: frontmatter in docs/**/*.md.")
    parser.add_argument("--root", default=".", help="repository root (default: .)")
    parser.add_argument("--require", action="store_true", help="missing docops: is an error")
    parser.add_argument("--json", action="store_true", help="print problems as a JSON array")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not (root / "docs").is_dir():
        print(f"frontmatter gate: {root / 'docs'} doesn't exist", file=sys.stderr)
        return 2
    try:
        problems, page_count = run(root, args.require)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"frontmatter gate: can't read a page: {exc}", file=sys.stderr)
        return 2

    ordered = sorted(problems, key=sort_key)
    errors = sum(1 for p in ordered if p[2] == "error")
    warnings = len(ordered) - errors

    if args.json:
        out = [{"path": p, "rule": r, "severity": s, "subject": sub} for p, r, s, sub in ordered]
        sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    else:
        lines = [
            f"{p}: {s}: {r}" + ("" if sub is None else f": {sub}") for p, r, s, sub in ordered
        ]
        lines.append(f"frontmatter gate: {errors} error(s), {warnings} warning(s), {page_count} page(s)")
        sys.stdout.write("\n".join(lines) + "\n")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
