#!/usr/bin/env python3
"""
Extract the SenseML config from a blog post draft and write it to a file.

Reads the content between <!-- CONFIG:START --> and <!-- CONFIG:END --> markers,
strips the surrounding fenced code block, and writes the raw config text.

Usage:
    python .claude/skills/blog-how-to-parse-x/extract_config_from_draft.py <draft.md> <output.json>
"""

import re
import sys
from pathlib import Path


def extract_config(draft_path: Path, output_path: Path) -> None:
    content = draft_path.read_text(encoding="utf-8")

    match = re.search(
        r"<!-- CONFIG:START -->\n```\w*\n(.*?)\n```\n<!-- CONFIG:END -->",
        content,
        re.DOTALL,
    )
    if not match:
        print(f"Error: no CONFIG:START/END markers found in {draft_path}", file=sys.stderr)
        sys.exit(1)

    config_text = match.group(1)
    output_path.write_text(config_text, encoding="utf-8")
    print(f"Wrote {len(config_text)} chars to {output_path}")


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <draft.md> <output.json>", file=sys.stderr)
        sys.exit(1)

    extract_config(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
