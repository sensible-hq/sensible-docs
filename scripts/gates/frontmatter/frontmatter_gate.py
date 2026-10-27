#!/usr/bin/env python3
"""Frontmatter gate: checks the docops: block in docs/ pages.

Behavior is defined by SPEC.md and tests.yaml in this folder.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

PAGE_TYPES = {"tutorial", "how-to", "reference", "explanation"}
DOCOPS_KEYS = {"page_type", "related"}
MAX_RELATED = 5
BAD_SLUG_CHARS = {":", "#", "/"}


def subject_text(value):
    """A subject as the text YAML would write for it (2024, true, 2024-01-01)."""
    if value is None or isinstance(value, str):
        return value
    text = yaml.safe_dump(value, default_flow_style=True, allow_unicode=True)
    text = text.strip()
    if text.endswith("\n..."):
        text = text[: -len("\n...")]
    elif text.endswith("..."):
        text = text[: -len("...")].rstrip()
    return text


def is_unset(value):
    return value is None or value == "" or value == []


def find_pages(docs):
    """Every file matching docs/**/*.md, as paths relative to the root."""
    pages = []
    for dirpath, dirnames, filenames in os.walk(docs):
        dirnames.sort()
        for name in sorted(filenames):
            if name.endswith(".md"):
                full = Path(dirpath) / name
                if full.is_file():
                    pages.append(full)
    return pages


def slug_of(path):
    return path.parent.name if path.name == "index.md" else path.stem


def read_frontmatter(path):
    """Returns (rule, mapping): rule is a problem ID, or None if mapping is valid."""
    try:
        text = path.read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return "unreadable", None
    if text.startswith("\ufeff"):
        text = text[1:]
    # Split on \n only: str.splitlines also breaks on U+2028 and friends.
    lines = text.split("\n")
    if lines[0].rstrip("\r") != "---":
        return "no-frontmatter", None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r") == "---":
            body = "\n".join(lines[1:i])
            break
    else:
        return "no-frontmatter", None
    try:
        data = yaml.safe_load(body)
    except yaml.YAMLError:
        return "bad-yaml", None
    if not isinstance(data, dict):
        return "bad-yaml", None
    return None, data


def is_slug(entry):
    return entry != "" and not any(c in BAD_SLUG_CHARS or c.isspace() for c in entry)


class Gate:
    def __init__(self, root, require):
        self.root = root
        self.require = require
        self.problems = set()

    def report(self, rel, rule, subject=None):
        if rule == "missing-docops" and not self.require:
            severity = "warning"
        else:
            severity = "error"
        self.problems.add((rel, rule, severity, subject_text(subject)))

    def check_docops(self, rel, docops):
        """Checks one page's docops block. Returns its valid related slugs."""
        for key in docops:
            if key not in DOCOPS_KEYS:
                self.report(rel, "unknown-key", key)

        page_type = docops.get("page_type")
        if is_unset(page_type):
            self.report(rel, "missing-page-type")
        elif not (isinstance(page_type, str) and page_type in PAGE_TYPES):
            self.report(rel, "bad-page-type", page_type)

        related = docops.get("related")
        if is_unset(related):
            return []
        if not isinstance(related, list):
            self.report(rel, "related-not-list")
            return []
        if len(related) > MAX_RELATED:
            self.report(rel, "related-too-many")

        slugs = []
        for entry in related:
            if not isinstance(entry, str):
                self.report(rel, "related-not-string", entry)
            elif not is_slug(entry):
                self.report(rel, "related-not-slug", entry)
            else:
                slugs.append(entry)
        return slugs

    def run(self):
        paths = find_pages(self.root / "docs")
        pages = []  # (rel, slug, related slugs or None if the page is broken)
        for path in paths:
            rel = path.relative_to(self.root).as_posix()
            rule, data = read_frontmatter(path)
            if rule:
                self.report(rel, rule)
                pages.append((rel, slug_of(path), None))
                continue
            if "docops" not in data:
                self.report(rel, "missing-docops")
                pages.append((rel, slug_of(path), None))
                continue
            docops = data["docops"]
            if not isinstance(docops, dict):
                self.report(rel, "docops-not-mapping")
                pages.append((rel, slug_of(path), None))
                continue
            pages.append((rel, slug_of(path), self.check_docops(rel, docops)))

        by_slug = {}
        for rel, slug, related in pages:
            by_slug.setdefault(slug, []).append((rel, related))

        for rel, slug, related in pages:
            if related is None:
                continue
            if len(by_slug[slug]) > 1:
                self.report(rel, "duplicate-slug", slug)
            seen = set()
            for entry in related:
                if entry in seen:
                    self.report(rel, "related-duplicate", entry)
                    continue
                seen.add(entry)
                if entry == slug:
                    self.report(rel, "related-self", entry)
                    continue
                targets = by_slug.get(entry, [])
                if len(targets) != 1:
                    self.report(rel, "related-unresolved", entry)
                    continue
                target_related = targets[0][1] or []
                if slug not in target_related:
                    self.report(rel, "related-asymmetric", entry)

        return len(pages)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check docops: frontmatter in docs/ pages.")
    parser.add_argument("--root", default=".", help="repository root (default: .)")
    parser.add_argument("--require", action="store_true", help="missing docops: is an error")
    parser.add_argument("--json", action="store_true", help="print problems as JSON")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not (root / "docs").is_dir():
        print(f"frontmatter gate: {root / 'docs'} is not a folder", file=sys.stderr)
        return 2

    gate = Gate(root, args.require)
    count = gate.run()
    problems = sorted(gate.problems, key=lambda p: (p[0], p[1], p[3] or ""))
    errors = sum(1 for p in problems if p[2] == "error")
    warnings = len(problems) - errors

    if args.json:
        out = [
            {"path": path, "rule": rule, "severity": severity, "subject": subject}
            for path, rule, severity, subject in problems
        ]
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        for path, rule, severity, subject in problems:
            line = f"{path}: {severity}: {rule}"
            if subject is not None:
                line += f": {subject}"
            print(line)
        print(f"frontmatter gate: {errors} error(s), {warnings} warning(s), {count} page(s)")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
