#!/usr/bin/env python3
"""
Deterministically shorten excerpt and metadata.description values over 160 characters.

Search engines truncate descriptions at about 160 characters, and the LLM that
generates excerpts doesn't reliably count characters. This script applies
rules from least to most invasive, stopping as soon as the text fits:

  1. Drop filler openers ("Learn how to use X" -> "Use X", "Overview of X" -> "X").
  2. Cut at a sentence end.
  3. Cut at a clause break (", ", "; ", " — ") that isn't inside a list.
  4. Cut inside a trailing list, if the dropped tail is short, and restore the
     "and"/"or" before the last kept item.
  5. Cut before a phrase-starting word ("with", "using", "to", ...).
  6. Cut at a word boundary, trimming dangling connector words.

Within each rule, the longest result that fits wins.

The same input always produces the same output, and text that already fits
is never changed.

Respects ignore list in scripts/descriptions/description_ignore.txt.

Usage:
  python shorten_excerpt.py           # fix all docs/**/*.md
  python shorten_excerpt.py --check   # report and exit 1 if any are too long
  python shorten_excerpt.py --dry-run # print before/after without writing
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

MAX_LENGTH = 160

# Shortest result a cut may produce. Below this, fall through to the next rule
# so the excerpt keeps more of its meaning.
MIN_LENGTH = 60

# Longest list tail (words after the final ", and"/", or") that a list cut may drop.
MAX_LIST_TAIL_WORDS = 4

# (pattern, replacement) applied to the start of the text, in order.
OPENER_RULES = [
    (re.compile(r"^Learn how to "), ""),
    (re.compile(r"^Learn how "), "How "),
    (re.compile(r"^Learn about (the )?"), ""),
    (re.compile(r"^(An )?[Oo]verview of "), ""),
]

SENTENCE_BREAK = re.compile(r"\. ")
CLAUSE_BREAK = re.compile(r", |; | — ")
LIST_END = re.compile(r", (and|or) ")
PHRASE_WORDS = r"across|by|for|from|in|including|into|letting|like|that|to|using|via|while|with|within"
PHRASE_START = re.compile(rf" (?=({PHRASE_WORDS}) )")
# Where a list can start: after a previous list's conjunction or a phrase-starting word.
LIST_START = re.compile(rf", (and|or) | ({PHRASE_WORDS}|such as) ")

# Words that read as unfinished at the end of a sentence.
DANGLING = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "including", "into",
    "like", "of", "on", "or", "such", "the", "to", "using", "via", "with",
}


def find_repo_root() -> Path:
    candidate = Path(__file__).resolve().parent.parent.parent
    if (candidate / "docs").is_dir():
        return candidate
    cwd = Path.cwd()
    if (cwd / "docs").is_dir():
        return cwd
    raise SystemExit("Could not find repo root (expected docs/ directory)")


def load_ignore_list(script_dir: Path) -> set[str]:
    ignore_file = script_dir / "description_ignore.txt"
    if not ignore_file.exists():
        return set()
    return {
        line.strip()
        for line in ignore_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }


def capitalize_first(text: str) -> str:
    return text[:1].upper() + text[1:]


def end_sentence(text: str) -> str:
    words = text.rstrip(" ,;:—-").split(" ")
    while len(words) > 1 and words[-1].lower() in DANGLING:
        words.pop()
    return " ".join(words).rstrip(" ,;:—-") + "."


def drop_openers(text: str) -> str:
    for pattern, replacement in OPENER_RULES:
        new = pattern.sub(replacement, text, count=1)
        if new != text:
            return capitalize_first(new)
    return text


def longest_fitting(candidates) -> str | None:
    fitting = [c for c in candidates if MIN_LENGTH <= len(c) <= MAX_LENGTH]
    return max(fitting, key=len) if fitting else None


def cut_sentence(text: str) -> str | None:
    return longest_fitting(text[: m.start()] + "." for m in SENTENCE_BREAK.finditer(text))


def cut_clause(text: str) -> str | None:
    """Cut at a break whose remainder doesn't continue a list."""
    return longest_fitting(
        end_sentence(text[: m.start()])
        for m in CLAUSE_BREAK.finditer(text)
        if not LIST_END.search(text[m.start() :])
    )


def join_list(kept: str, conjunction: str) -> str:
    """Put the conjunction back before the last item of a list that lost its tail."""
    starts = [m.end() for m in LIST_START.finditer(kept)]
    start = starts[-1] if starts else 0
    commas = kept.count(", ", start)
    if commas == 0:
        return kept
    i = kept.rindex(", ")
    separator = f", {conjunction} " if commas >= 2 else f" {conjunction} "
    return kept[:i] + separator + kept[i + 2 :]


def cut_list(text: str) -> str | None:
    """Drop items from the end of a trailing list whose last item is short."""
    ends = list(LIST_END.finditer(text))
    if not ends:
        return None
    final = ends[-1]
    if len(text[final.end() :].split()) > MAX_LIST_TAIL_WORDS:
        return None
    conjunction = final.group(1)
    candidates = []
    for m in re.finditer(r", ", text):
        if m.start() > final.start():
            break
        kept = text[: m.start()]
        candidates.append(end_sentence(join_list(kept, conjunction)))
    return longest_fitting(candidates)


def cut_phrase(text: str) -> str | None:
    return longest_fitting(end_sentence(text[: m.start()]) for m in PHRASE_START.finditer(text))


def cut_words(text: str) -> str:
    cut = text[:MAX_LENGTH]
    if " " in cut:
        cut = cut[: cut.rindex(" ")]
    result = end_sentence(cut)
    while len(result) > MAX_LENGTH:
        result = end_sentence(result[: result.rindex(" ")])
    return result


def shorten(text: str) -> str:
    if len(text) <= MAX_LENGTH:
        return text
    text = drop_openers(text)
    if len(text) <= MAX_LENGTH:
        return text
    return cut_sentence(text) or cut_clause(text) or cut_list(text) or cut_phrase(text) or cut_words(text)


def split_frontmatter(content: str) -> tuple[dict, str] | None:
    if not content.startswith("---"):
        return None
    end = re.search(r"\n---\s*(\n|$)", content[3:])
    if not end:
        return None
    try:
        fm = yaml.safe_load(content[3 : end.start() + 3]) or {}
    except yaml.YAMLError:
        return None
    return fm, content[end.end() + 3 :]


def shorten_file(path: Path, dry_run: bool) -> list[tuple[str, str, str]]:
    """Return a list of (field, old, new) for each value that was (or would be) shortened."""
    content = path.open(encoding="utf-8", newline="").read()
    parts = split_frontmatter(content)
    if parts is None:
        return []
    fm, rest = parts

    changes = []
    excerpt = fm.get("excerpt")
    if isinstance(excerpt, str) and shorten(excerpt) != excerpt:
        fm["excerpt"] = shorten(excerpt)
        changes.append(("excerpt", excerpt, fm["excerpt"]))

    metadata = fm.get("metadata")
    description = metadata.get("description") if isinstance(metadata, dict) else None
    if isinstance(description, str) and shorten(description) != description:
        metadata["description"] = shorten(description)
        changes.append(("metadata.description", description, metadata["description"]))

    if changes and not dry_run:
        new_front_matter = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False, width=float("inf"))
        path.open("w", encoding="utf-8", newline="").write(f"---\n{new_front_matter}---\n{rest}")
    return changes


def main():
    parser = argparse.ArgumentParser(description=f"Shorten excerpts and descriptions over {MAX_LENGTH} characters")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Report without writing; exit 1 if any are too long")
    mode.add_argument("--dry-run", action="store_true", help="Print before/after without writing")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    repo_root = find_repo_root()
    ignore_list = load_ignore_list(script_dir)

    total = 0
    for md_path in sorted(repo_root.glob("docs/**/*.md")):
        rel = str(md_path.relative_to(repo_root))
        if rel in ignore_list:
            continue
        changes = shorten_file(md_path, dry_run=args.check or args.dry_run)
        for field, old, new in changes:
            total += 1
            if args.check:
                print(f"{rel}: {field} is {len(old)} characters (max {MAX_LENGTH})")
            else:
                label = "Would shorten" if args.dry_run else "Shortened"
                print(f"{label}: {rel} [{field}]\n  - ({len(old)}) {old}\n  + ({len(new)}) {new}")

    if total == 0:
        print(f"All excerpts and descriptions are {MAX_LENGTH} characters or fewer.")
        return 0
    if args.check:
        print(f"\n{total} value(s) over {MAX_LENGTH} characters. Run shorten_excerpt.py to fix.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
