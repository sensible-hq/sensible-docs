#!/usr/bin/env python3
"""
Deterministically shorten excerpts over 160 characters.

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

Only excerpt is changed; sync_description.py copies it to metadata.description.
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

import frontmatter
from frontmatter import MAX_LENGTH

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


def shorten_file(path: Path, dry_run: bool) -> tuple[str, str] | None:
    """Return (old, new) if the excerpt was (or would be) shortened, else None.

    Only excerpt is touched; sync_description.py copies it to metadata.description.
    """
    doc = frontmatter.read(path)
    excerpt = (doc.fm or {}).get("excerpt")
    if not isinstance(excerpt, str):
        return None
    new = shorten(excerpt)
    if new == excerpt:
        return None
    if not dry_run:
        frontmatter.write(doc, frontmatter.set_excerpt(doc.fm, new))
    return excerpt, new


def main():
    parser = argparse.ArgumentParser(description=f"Shorten excerpts over {MAX_LENGTH} characters")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Report without writing; exit 1 if any are too long")
    mode.add_argument("--dry-run", action="store_true", help="Print before/after without writing")
    args = parser.parse_args()

    total = 0
    for path, rel in frontmatter.iter_docs(frontmatter.find_repo_root()):
        change = shorten_file(path, dry_run=args.check or args.dry_run)
        if change is None:
            continue
        old, new = change
        total += 1
        if args.check:
            print(f"{rel}: excerpt is {len(old)} characters (max {MAX_LENGTH})")
        else:
            label = "Would shorten" if args.dry_run else "Shortened"
            print(f"{label}: {rel}\n  - ({len(old)}) {old}\n  + ({len(new)}) {new}")

    if total == 0:
        print(f"All excerpts are {MAX_LENGTH} characters or fewer.")
        return 0
    if args.check:
        print(f"\n{total} excerpt(s) over {MAX_LENGTH} characters. Run shorten_excerpt.py to fix.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
