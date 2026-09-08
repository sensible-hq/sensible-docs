#!/usr/bin/env python3
"""
Generate or regenerate excerpts for docs using Claude.

Calls the Claude API to generate a concise excerpt for each specified file,
writes it to the excerpt field (which is the source of truth), then syncs
metadata.description to match.

Usage:
  python generate_excerpts.py <file1> [<file2> ...]   # specific files
  python generate_excerpts.py --all                   # all docs/**/*.md

Requires ANTHROPIC_API_KEY environment variable.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent.parent


def find_repo_root() -> Path:
    candidate = Path(__file__).resolve().parent.parent.parent
    if (candidate / "docs").is_dir():
        return candidate
    cwd = Path.cwd()
    if (cwd / "docs").is_dir():
        return cwd
    raise SystemExit("Could not find repo root (expected docs/ directory)")


def parse_frontmatter(content: str) -> tuple[dict | None, int]:
    if not content.startswith("---"):
        return None, -1
    end = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end:
        return None, -1
    try:
        fm = yaml.safe_load(content[3 : end.start() + 3]) or {}
        return fm, end.end() + 3
    except yaml.YAMLError:
        return None, -1


def write_excerpt(file_path: Path, excerpt: str) -> None:
    content = file_path.open(encoding="utf-8", newline="").read()
    fm, rest_start = parse_frontmatter(content)
    if fm is None:
        raise ValueError(f"No front matter in {file_path}")

    if "excerpt" in fm:
        fm["excerpt"] = excerpt
    else:
        new_fm = {}
        for k, v in fm.items():
            new_fm[k] = v
            if k == "title":
                new_fm["excerpt"] = excerpt
        if "excerpt" not in new_fm:
            new_fm["excerpt"] = excerpt
        fm = new_fm

    new_front_matter = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    file_path.open("w", encoding="utf-8", newline="").write(f"---\n{new_front_matter}---\n{content[rest_start:]}")


def sync_description(file_path: Path) -> None:
    content = file_path.open(encoding="utf-8", newline="").read()
    fm, rest_start = parse_frontmatter(content)
    if fm is None:
        return

    excerpt = fm.get("excerpt") or ""
    if not excerpt:
        return

    metadata = fm.get("metadata") or {}
    if not isinstance(metadata, dict):
        return

    if metadata.get("description") == excerpt:
        return

    fm["metadata"]["description"] = excerpt
    new_front_matter = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False)
    file_path.open("w", encoding="utf-8", newline="").write(f"---\n{new_front_matter}---\n{content[rest_start:]}")


def generate_excerpt(file_path: Path, api_key: str) -> str:
    content = file_path.open(encoding="utf-8", newline="").read()
    fm, _ = parse_frontmatter(content)
    title = (fm or {}).get("title", file_path.stem)

    # Strip front matter for the content snippet
    body_start = content.find("---", 3)
    body = content[body_start + 3:].strip() if body_start != -1 else content

    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 160,
        "messages": [{
            "role": "user",
            "content": (
                "Generate a concise 1-line excerpt (max 160 characters) for this documentation page. "
                "The excerpt should summarize what the page covers in plain language suitable for SEO. "
                "Do NOT include quotes. Return the plain text only.\n\n"
                f"Title: {title}\n\nContent:\n{body[:4000]}"
            ),
        }],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    return result["content"][0]["text"].strip()


def main():
    parser = argparse.ArgumentParser(description="Generate excerpts for docs using Claude")
    parser.add_argument("files", nargs="*", help="Files to process")
    parser.add_argument("--all", action="store_true", help="Process all docs/**/*.md")
    parser.add_argument("--dry-run", action="store_true", help="Print generated excerpts without writing")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY or ANTHROPIC_KEY not set", file=sys.stderr)
        return 1

    repo_root = find_repo_root()

    if args.all:
        paths = sorted(repo_root.glob("docs/**/*.md"))
    elif args.files:
        paths = [repo_root / f if not Path(f).is_absolute() else Path(f) for f in args.files]
    else:
        parser.print_help()
        return 1

    for path in paths:
        fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        if fm and fm.get("hidden"):
            print(f"Skipped (hidden): {path}")
            continue

        print(f"Generating: {path.relative_to(repo_root)}")
        try:
            excerpt = generate_excerpt(path, api_key)
            print(f"  → {excerpt}")
            if not args.dry_run:
                write_excerpt(path, excerpt)
                sync_description(path)
        except Exception as e:
            print(f"  Error: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
