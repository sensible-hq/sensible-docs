#!/usr/bin/env python3
"""Check fenced code blocks in docs pages: json fences, /* */ comments, one JSON5 header comment.

  python3 scripts/style/check_code_blocks.py [file ...]     # default: every .md file under docs/

Flags:
  - a ```json5 fence (ReadMe doesn't render it; use ```json)
  - a // comment inside a json or json5 fence (use /* */); // inside a string or a /* */ comment is
    fine, so URLs don't count. Unlabeled fences are skipped: they can hold JavaScript.
  - the "Sensible uses JSON5 to support in-line comments" header comment more than once on a page

Prints path:line: message for each problem and exits 1 if there are any. Registry rule:
sensible-code-fences.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w+-]*)")
HEADER = re.compile(r"/\*\s*Sensible uses JSON5 to support in-line comments\s*\*/")


def line_comments(lines: list[str]) -> list[int]:
    """Indexes of lines with a // comment outside strings and block comments."""
    hits, in_block = [], False
    for i, line in enumerate(lines):
        j, in_str = 0, False
        while j < len(line):
            two = line[j:j + 2]
            if in_block:
                if two == "*/":
                    in_block, j = False, j + 2
                    continue
            elif in_str:
                if line[j] == "\\":
                    j += 2
                    continue
                if line[j] == '"':
                    in_str = False
            elif line[j] == '"':
                in_str = True
            elif two == "/*":
                in_block, j = True, j + 2
                continue
            elif two == "//":
                hits.append(i)
                break
            j += 1
    return hits


def check(path: Path) -> list[str]:
    rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    lines = path.read_text().splitlines()
    problems, i, headers = [], 0, []
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        marker, lang = m.group(1), m.group(2).lower()
        start = i
        i += 1
        while i < len(lines) and not lines[i].strip().startswith(marker):
            i += 1
        body = lines[start + 1:i]
        i += 1
        if lang == "json5":
            problems.append(f"{rel}:{start + 1}: use a ```json fence, not ```json5 (ReadMe doesn't render json5)")
        if lang in ("json", "json5"):
            for k in line_comments(body):
                problems.append(f"{rel}:{start + 2 + k}: use /* */ for comments, not //")
            headers += [start + 2 + k for k, line in enumerate(body) if HEADER.search(line)]
    for n in headers[1:]:
        problems.append(f"{rel}:{n}: the JSON5 header comment belongs on the first commented block only")
    return problems


def main(argv):
    files = [Path(a).resolve() for a in argv] or sorted((ROOT / "docs").rglob("*.md"))
    problems = [p for f in files if f.suffix == ".md" and f.is_file() for p in check(f)]
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
