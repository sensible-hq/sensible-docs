#!/usr/bin/env python3
"""
Add or update a metadata description in a markdown file's front matter.

Usage: add_description.py <file_path> <description>
"""

import re
import sys
from pathlib import Path


def update_file_with_description(file_path: Path, description: str) -> bool:
    """Update the file's front matter with the new description."""
    content = file_path.read_text(encoding="utf-8")

    if not content.startswith("---"):
        return False

    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return False

    front_matter = content[3:end_match.start() + 3]
    rest_of_file = content[end_match.end() + 3:]

    # Escape single quotes in description
    escaped_description = description.replace("'", "''")

    has_metadata_block = "metadata:" in front_matter

    if has_metadata_block:
        # Check if description line exists in metadata block
        if re.search(r"(metadata:\s*\n(?:[ \t]+\w+:.*\n)*)([ \t]+description:\s*)['\"]?['\"]?\s*\n", front_matter):
            front_matter = re.sub(
                r"(metadata:\s*\n(?:[ \t]+\w+:.*\n)*)([ \t]+description:\s*)['\"]?['\"]?\s*\n",
                rf"\1\2'{escaped_description}'\n",
                front_matter
            )
        else:
            # Add description after metadata: line
            front_matter = re.sub(
                r"(metadata:\s*\n)",
                rf"\1  description: '{escaped_description}'\n",
                front_matter
            )
    else:
        # Add metadata block
        front_matter = front_matter.rstrip() + f"\nmetadata:\n  description: '{escaped_description}'\n"

    new_content = f"---{front_matter}---\n{rest_of_file}"
    file_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_path> <description>", file=sys.stderr)
        return 1

    file_path = Path(sys.argv[1])
    description = sys.argv[2]

    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    if update_file_with_description(file_path, description):
        print(f"Updated: {file_path}")
        return 0
    else:
        print(f"Error: Could not update {file_path}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
