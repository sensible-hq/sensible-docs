#!/usr/bin/env python3
"""
Generate excerpts for docs using Claude.

Writes the excerpt (the source of truth) and syncs metadata.description to
match. In reference/, fills whichever of excerpt or metadata.description
exists but is empty.

Excerpts longer than 160 characters are sent back to Claude with their actual
length, up to MAX_ATTEMPTS times. Anything still too long is shortened
deterministically with shorten_excerpt.shorten().

Usage:
  python generate_excerpts.py --missing               # files check_excerpt.py would flag
  python generate_excerpts.py <file1> [<file2> ...]   # regenerate specific files
  python generate_excerpts.py --all                   # regenerate all docs/**/*.md
  python generate_excerpts.py --missing --dry-run     # print without writing

Requires ANTHROPIC_API_KEY. Exits 1 if any file failed.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

import frontmatter
from frontmatter import MAX_LENGTH
from shorten_excerpt import shorten

MODEL = "claude-sonnet-5"
MAX_ATTEMPTS = 3
CONTENT_CHARS = 4000

PROMPT = (
    "Write a one-line excerpt for this documentation page, at most 150 characters. "
    "It summarizes what the page covers in plain language, for SEO. "
    "Return only the excerpt text, without quotes.\n\n"
    "Title: {title}\n\nContent:\n{content}"
)
RETRY_PROMPT = "That's {length} characters. Rewrite it in at most 150 characters. Return only the excerpt text."


def call_claude(messages: list[dict], api_key: str) -> str:
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({"model": MODEL, "max_tokens": 200, "messages": messages}).encode(),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"API error {e.code}: {e.read().decode(errors='replace')[:300]}") from e
    text = next((block["text"] for block in result.get("content", []) if block.get("type") == "text"), "")
    text = " ".join(text.split()).strip('"')
    if not text:
        raise RuntimeError(f"Empty response: {json.dumps(result)[:300]}")
    return text


def generate_excerpt(doc: frontmatter.Doc, api_key: str) -> str:
    title = doc.fm.get("title") or doc.path.stem
    body = doc.content[doc.body :].strip()[:CONTENT_CHARS]
    messages = [{"role": "user", "content": PROMPT.format(title=title, content=body)}]

    excerpt = call_claude(messages, api_key)
    for _ in range(MAX_ATTEMPTS - 1):
        if len(excerpt) <= MAX_LENGTH:
            break
        messages += [
            {"role": "assistant", "content": excerpt},
            {"role": "user", "content": RETRY_PROMPT.format(length=len(excerpt))},
        ]
        excerpt = call_claude(messages, api_key)
    return shorten(excerpt)


def target_field(rel: str, fm: dict, missing_only: bool) -> str | None:
    if missing_only:
        return frontmatter.missing_field(rel, fm)
    if fm.get("hidden"):
        return None
    if not frontmatter.is_reference(rel) or "excerpt" in fm:
        return "excerpt"
    # Regenerating a reference/ file: only touch fields it already has.
    return "metadata.description" if frontmatter.has_description_key(fm) else None


def apply(rel: str, fm: dict, field: str, text: str) -> dict:
    if field == "metadata.description":
        return frontmatter.set_description(fm, text)
    fm = frontmatter.set_excerpt(fm, text)
    # docs/ always get a derived description; reference/ only if the key already exists.
    if not frontmatter.is_reference(rel) or frontmatter.has_description_key(fm):
        fm = frontmatter.set_description(fm, text)
    return fm


def warn(rel: str, message: str) -> None:
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::warning file={rel}::{message}")
    else:
        print(f"  Warning: {message}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Generate excerpts for docs using Claude")
    parser.add_argument("files", nargs="*", help="Files to regenerate")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--missing", action="store_true", help="Process files with a missing or empty excerpt")
    group.add_argument("--all", action="store_true", help="Regenerate all docs/**/*.md")
    parser.add_argument("--dry-run", action="store_true", help="Print generated excerpts without writing")
    args = parser.parse_args()

    if not (args.missing or args.all or args.files):
        parser.print_help()
        return 1

    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY or ANTHROPIC_KEY not set", file=sys.stderr)
        return 1

    repo_root = frontmatter.find_repo_root()
    if args.files:
        paths = [Path(f).resolve() for f in args.files]
        targets = [(p, p.relative_to(repo_root).as_posix()) for p in paths]
    else:
        targets = list(frontmatter.iter_docs(repo_root, ("docs", "reference") if args.missing else ("docs",)))

    failed = 0
    for path, rel in targets:
        doc = frontmatter.read(path)
        if doc.fm is None:
            if doc.error:
                warn(rel, "Skipped: invalid YAML frontmatter")
            continue
        field = target_field(rel, doc.fm, args.missing)
        if field is None:
            continue

        print(f"Generating {field}: {rel}")
        try:
            text = generate_excerpt(doc, api_key)
        except (RuntimeError, urllib.error.URLError, TimeoutError) as e:
            warn(rel, f"Could not generate {field}: {e}")
            failed += 1
            continue
        print(f"  → ({len(text)}) {text}")
        if not args.dry_run:
            frontmatter.write(doc, apply(rel, doc.fm, field, text))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
