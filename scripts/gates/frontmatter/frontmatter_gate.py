#!/usr/bin/env python3
"""Frontmatter gate: checks the `docops:` block in docs pages' frontmatter.

Behavior is defined by SPEC.md (v0.3.0) and tests.yaml in this folder.
"""

import argparse
import base64
import datetime
import json
import math
import os
import re
import sys

import yaml

PAGE_TYPES = ("tutorial", "how-to", "reference", "explanation")
ALLOWED_KEYS = ("page_type", "related")
MAX_RELATED = 5

# Unicode White_Space property.
WHITESPACE = frozenset(
    "\t\n\v\f\r \x85\xa0\u1680"
    "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a"
    "\u2028\u2029\u202f\u205f\u3000"
)
NOT_SLUG_CHARS = frozenset(":#/") | WHITESPACE

NO_SUBJECT = object()
LINE_BREAK = re.compile(r"\r\n|\r|\n")


# --- YAML loading -----------------------------------------------------------
# Safe-load (YAML 1.1), but numbers and timestamps keep the text they were
# written as, so subjects can render "as YAML wrote them".


class SrcInt(int):
    def __new__(cls, value, src):
        obj = int.__new__(cls, value)
        obj.src = src
        return obj


class SrcFloat(float):
    def __new__(cls, value, src):
        obj = float.__new__(cls, value)
        obj.src = src
        return obj


class SrcDatetime(datetime.datetime):
    pass


class Loader(yaml.SafeLoader):
    pass


def _construct_int(loader, node):
    return SrcInt(yaml.constructor.SafeConstructor.construct_yaml_int(loader, node), node.value)


def _construct_float(loader, node):
    return SrcFloat(yaml.constructor.SafeConstructor.construct_yaml_float(loader, node), node.value)


def _construct_timestamp(loader, node):
    value = yaml.constructor.SafeConstructor.construct_yaml_timestamp(loader, node)
    if isinstance(value, datetime.datetime):
        wrapped = SrcDatetime(
            value.year, value.month, value.day, value.hour, value.minute,
            value.second, value.microsecond, value.tzinfo,
        )
        wrapped.src = node.value
        return wrapped
    return value


Loader.add_constructor("tag:yaml.org,2002:int", _construct_int)
Loader.add_constructor("tag:yaml.org,2002:float", _construct_float)
Loader.add_constructor("tag:yaml.org,2002:timestamp", _construct_timestamp)


# --- Subjects ---------------------------------------------------------------


def render(value):
    """Render any YAML value as a subject string (SPEC.md "Subjects")."""
    if isinstance(value, str):
        return value
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (SrcInt, SrcFloat, SrcDatetime)):
        return value.src
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _jsonable(value):
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, float):
        if math.isinf(value) or math.isnan(value):
            return render(value)
        return float(value)
    if isinstance(value, int):
        return int(value)
    if isinstance(value, (datetime.date, datetime.datetime)):
        return render(value)
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, dict):
        return {render(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (set, frozenset)):
        return sorted((_jsonable(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return str(value)


# --- Pages ------------------------------------------------------------------


class Page:
    def __init__(self, path, rel):
        self.path = path  # filesystem path
        self.rel = rel  # repo-relative, '/'-separated
        parts = rel.split("/")
        name = parts[-1]
        self.slug = parts[-2] if name == "index.md" else name[:-3]
        self.related = None  # list of entries other pages may match, or None


def find_pages(root):
    """Regular files matching docs/**/*.md; symbolic links are not followed."""
    pages = []

    def walk(directory, rel_dir):
        with os.scandir(directory) as entries:
            for entry in entries:
                rel = rel_dir + "/" + entry.name
                if entry.is_dir(follow_symlinks=False):
                    walk(entry.path, rel)
                elif entry.is_file(follow_symlinks=False) and entry.name.endswith(".md"):
                    pages.append(Page(entry.path, rel))

    walk(os.path.join(root, "docs"), "docs")
    return pages


def is_unset(value):
    """Absent, null, empty string, and empty list all mean "not set"."""
    return value is None or (isinstance(value, (str, list)) and len(value) == 0)


def check_page(page, require, report):
    """Per-page checks. Sets page.related for the cross-page checks."""
    try:
        with open(page.path, "rb") as f:
            data = f.read()
        text = data.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        report(page, "unreadable")
        return None
    if text.startswith("\ufeff"):
        text = text[1:]

    lines = LINE_BREAK.split(text)
    if lines[0] != "---":
        report(page, "no-frontmatter")
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        report(page, "no-frontmatter")
        return None

    try:
        front = yaml.load("\n".join(lines[1:end]), Loader=Loader)
    except Exception:  # any parse or construction failure (incl. impossible dates)
        report(page, "bad-yaml")
        return None
    if not isinstance(front, dict):
        report(page, "bad-yaml")
        return None

    if "docops" not in front:
        report(page, "missing-docops", severity="error" if require else "warning")
        return None
    docops = front["docops"]
    if not isinstance(docops, dict):
        report(page, "docops-not-mapping")
        return None

    for key in docops:
        if not (isinstance(key, str) and key in ALLOWED_KEYS):
            report(page, "unknown-key", key)

    page_type = docops.get("page_type")
    if is_unset(page_type):
        report(page, "missing-page-type")
    elif not (isinstance(page_type, str) and page_type in PAGE_TYPES):
        report(page, "bad-page-type", page_type)

    related = docops.get("related")
    if is_unset(related):
        page.related = []
        return []
    if not isinstance(related, list):
        report(page, "related-not-list")
        return None
    page.related = related

    if len(related) > MAX_RELATED:
        report(page, "related-too-many")

    valid = []  # valid slugs, in order, duplicates included
    for entry in related:
        if not isinstance(entry, str):
            report(page, "related-not-string", entry)
        elif entry == "" or any(c in NOT_SLUG_CHARS for c in entry):
            report(page, "related-not-slug", entry)
        else:
            valid.append(entry)

    seen = set()
    for slug in valid:
        if slug in seen:
            report(page, "related-duplicate", slug)
        seen.add(slug)
    return valid


def run(root, require):
    pages = find_pages(root)
    problems = {}

    def report(page, rule, subject=NO_SUBJECT, severity="error"):
        subject = None if subject is NO_SUBJECT else render(subject)
        problems[(page.rel, rule, subject)] = severity

    valid_entries = {}
    for page in pages:
        valid_entries[page.rel] = check_page(page, require, report)

    by_slug = {}
    for page in pages:
        by_slug.setdefault(page.slug, []).append(page)
    for slug, owners in by_slug.items():
        if len(owners) > 1:
            for page in owners:
                report(page, "duplicate-slug", slug)

    for page in pages:
        entries = valid_entries[page.rel]
        if not entries:
            continue
        for slug in dict.fromkeys(entries):  # distinct, in order
            if slug == page.slug:
                report(page, "related-self", slug)
                continue
            owners = by_slug.get(slug, [])
            if len(owners) != 1:
                report(page, "related-unresolved", slug)
                continue
            if len(by_slug[page.slug]) != 1:
                continue  # symmetry only between pages whose slugs are unique
            other = owners[0]
            if other.related is None or not any(
                isinstance(e, str) and e == page.slug for e in other.related
            ):
                report(page, "related-asymmetric", slug)

    def sort_key(item):
        (path, rule, subject), _ = item
        return (path, rule, subject is not None, subject or "")

    out = [
        {"path": path, "rule": rule, "severity": severity, "subject": subject}
        for (path, rule, subject), severity in sorted(problems.items(), key=sort_key)
    ]
    return out, len(pages)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check docops: frontmatter in docs/ pages.")
    parser.add_argument("--root", default=".", help="repository root (default: .)")
    parser.add_argument("--require", action="store_true", help="missing docops: is an error")
    parser.add_argument("--json", action="store_true", help="print problems as a JSON array")
    args = parser.parse_args(argv)

    docs = os.path.join(args.root, "docs")
    if os.path.islink(docs) or not os.path.isdir(docs):
        sys.stderr.write(f"frontmatter gate: {docs} doesn't exist or isn't a folder\n")
        return 2
    try:
        problems, page_count = run(args.root, args.require)
    except OSError as exc:
        sys.stderr.write(f"frontmatter gate: can't list pages: {exc}\n")
        return 2

    errors = sum(1 for p in problems if p["severity"] == "error")
    warnings = len(problems) - errors
    if args.json:
        output = json.dumps(problems, indent=2, ensure_ascii=False) + "\n"
    else:
        lines = []
        for p in problems:
            line = f"{p['path']}: {p['severity']}: {p['rule']}"
            if p["subject"] is not None:
                line += f": {p['subject']}"
            lines.append(line + "\n")
        lines.append(
            f"frontmatter gate: {errors} error(s), {warnings} warning(s), {page_count} page(s)\n"
        )
        output = "".join(lines)
    sys.stdout.buffer.write(output.encode("utf-8", "surrogateescape"))
    sys.stdout.flush()
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
