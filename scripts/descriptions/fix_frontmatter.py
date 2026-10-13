#!/usr/bin/env python3
"""
Repair invalid YAML front matter in docs/ markdown files.

Runs before the excerpt scripts so that one broken file doesn't block the
whole workflow. Only touches files whose front matter fails to parse, and
applies conservative text-level repairs, keeping the rest of the file as is:

  1. Tabs used for indentation are replaced with two spaces.
  2. Stray continuation lines (for example, a wrapped value whose second line
     lost its indentation) are joined onto the previous line.
  3. Unquoted values that contain YAML-significant characters (for example,
     ": " or " #") are wrapped in single quotes.

A repair is only written if the result parses. Files that still don't parse
are reported as unfixable.

Usage:
  python fix_frontmatter.py                 # fix all docs/**/*.md
  python fix_frontmatter.py --dry-run       # report without writing
  python fix_frontmatter.py --json          # machine-readable report
  python fix_frontmatter.py path/to/a.md    # fix specific files
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

import frontmatter

KEY_LINE = re.compile(r"^(?P<indent>\s*)(?P<dash>- )?(?P<key>[\w.\-]+):(?P<sep>\s+|$)(?P<value>.*)$")
LIST_ITEM = re.compile(r"^\s*- ")
BLOCK_SCALAR = re.compile(r"^[|>][-+0-9]*\s*(#.*)?$")


def yaml_error(text: str) -> str | None:
    try:
        yaml.safe_load(text)
        return None
    except yaml.YAMLError as e:
        return str(e)


def fix_tabs(lines: list[str]) -> list[str]:
    return [re.sub(r"^\t+", lambda m: "  " * len(m.group(0)), line) for line in lines]


def join_continuations(lines: list[str]) -> list[str]:
    out: list[str] = []
    block_indent: int | None = None  # indent of the key that owns an active | or > block

    for line in lines:
        indent = len(line) - len(line.lstrip())

        if block_indent is not None:
            if not line.strip() or indent > block_indent:
                out.append(line)
                continue
            block_indent = None

        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "---":
            out.append(line)
            continue

        match = KEY_LINE.match(line)
        if match:
            if BLOCK_SCALAR.match(match.group("value").strip()):
                block_indent = indent
            out.append(line)
            continue

        if LIST_ITEM.match(line):
            out.append(line)
            continue

        # Continuation line: fold it onto the last non-blank line, the same way
        # YAML folds a correctly indented multi-line plain scalar.
        for i in range(len(out) - 1, -1, -1):
            if out[i].strip():
                out[i] = f"{out[i].rstrip()} {stripped}"
                break
        else:
            out.append(line)

    return out


def needs_quoting(value: str) -> bool:
    if not value or value[0] in "'\"[{|>&*!":
        return False
    return ": " in value or " #" in value or value.endswith(":") or value[0] in "@`%"


def quote_values(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        match = KEY_LINE.match(line)
        value = match.group("value").rstrip() if match else ""
        if match and needs_quoting(value):
            quoted = "'" + value.replace("'", "''") + "'"
            line = f"{match.group('indent')}{match.group('dash') or ''}{match.group('key')}: {quoted}"
        out.append(line)
    return out


def repair(text: str) -> str | None:
    """Return repaired front matter text, or None if it can't be repaired."""
    lines = text.split("\n")
    for step in (fix_tabs, join_continuations, quote_values):
        lines = step(lines)
        candidate = "\n".join(lines)
        if yaml_error(candidate) is None:
            return candidate
    return None


def fix_file(path: Path, dry_run: bool) -> tuple[str, str | None]:
    """Return (status, error) where status is 'ok', 'fixed', or 'unfixable'."""
    content = path.open(encoding="utf-8", newline="").read()
    parts = frontmatter.split(content)
    if parts is None:
        return "ok", None

    rest = content[parts.closing :]
    newline = "\r\n" if "\r\n" in parts.text else "\n"
    normalized = parts.text.replace("\r\n", "\n")
    error = yaml_error(normalized)
    if error is None:
        return "ok", None

    repaired = repair(normalized)
    if repaired is None:
        return "unfixable", error

    if not dry_run:
        repaired = repaired.replace("\n", newline)
        path.open("w", encoding="utf-8", newline="").write(f"---{repaired}{rest}")
    return "fixed", None


def main():
    parser = argparse.ArgumentParser(description="Repair invalid YAML front matter in docs/")
    parser.add_argument("paths", nargs="*", help="Files to check (default: docs/**/*.md)")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    repo_root = frontmatter.find_repo_root()
    paths = [Path(p) for p in args.paths] or [path for path, _ in frontmatter.iter_docs(repo_root)]

    fixed, unfixable = [], []
    for path in paths:
        status, error = fix_file(path, args.dry_run)
        try:
            rel = str(path.resolve().relative_to(repo_root))
        except ValueError:
            rel = str(path)
        if status == "fixed":
            fixed.append(rel)
        elif status == "unfixable":
            unfixable.append({"path": rel, "error": error})

    if args.json:
        print(json.dumps({"fixed": fixed, "unfixable": unfixable}))
        return 0

    label = "Would fix" if args.dry_run else "Fixed"
    for p in fixed:
        print(f"{label}: {p}")
    for item in unfixable:
        print(f"Could not fix: {item['path']}\n  {item['error']}")
    if not fixed and not unfixable:
        print("All front matter is valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
