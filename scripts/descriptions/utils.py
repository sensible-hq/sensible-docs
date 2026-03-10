#!/usr/bin/env python3
"""Shared utilities for the descriptions scripts."""

import re
from pathlib import Path

import yaml

SEARCH_DIRS = ["docs", "reference"]


def find_repo_root(script_dir: Path) -> Path:
    """Find the repo root from the script directory, falling back to cwd."""
    repo_root = script_dir.parent.parent
    if (repo_root / "docs").exists() or (repo_root / "llms.txt").exists():
        return repo_root
    return Path.cwd()


def load_ignore_list(script_dir: Path) -> set[str]:
    """Load list of files to ignore from description_ignore.txt."""
    ignore_file = script_dir / "description_ignore.txt"
    if not ignore_file.exists():
        return set()

    ignore_list = set()
    for line in ignore_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            ignore_list.add(line)
    return ignore_list


def parse_front_matter(content: str) -> tuple[dict | None, str | None]:
    """Extract YAML front matter from markdown content.

    Returns (parsed_dict, None) on success.
    Returns (None, None) if no front matter found.
    Returns (None, error_message) on parse error.
    """
    if not content.startswith("---"):
        return None, None

    end_match = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end_match:
        return None, None

    front_matter_text = content[3:end_match.start() + 3]

    try:
        return yaml.safe_load(front_matter_text) or {}, None
    except yaml.YAMLError as e:
        return None, str(e)
