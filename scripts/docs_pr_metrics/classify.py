#!/usr/bin/env python3
"""Classify each revision after the AI draft: factual change, copy edit, elaboration, and so on.

A revision is one diff hunk on a doc file in a commit after the draft (see metrics.py).
Code settles what it can see: pure additions, pure deletions, and formatting-only edits.
Jev answers atomic yes-or-no questions about the rest, and the truth table in `decide`
turns those answers into one class.

Jev responses are recorded under jev-recordings/, keyed by a hash of the request.
`--replay` answers from those recordings only, so a rerun is byte-identical and free.

Design: .claude/sessions/metrics/classification-design.md
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[0] / "style"))
import metrics as M  # noqa: E402
import jev  # noqa: E402

MODEL = "jev-1.14.0"        # pinned, so a new Jev release can't change a recorded run
YES, NO = 0.7, 0.3          # Noul thresholds; between them the question isn't settled
MAX_SIDE_CHARS = 6000       # truncate very large hunks per side, and flag them

CLASSES = ["factual", "copy_edit", "typo", "elaboration", "rewrite", "addition", "deletion", "formatting", "unsettled"]

# Every word Jev sees is here, so the questions are audited and edited in one place.
QUESTIONS = {
    "contradicts": {
        "type": "noul",
        "instructions": "Does `after` contradict something that `before` tells the reader about the product?",
        "criteria": {
            "true": "`before` states a value, default, limit, location in the app, supported file type, requirement, "
                    "or behavior, and `after` states a different one for the same thing, so a reader who believed "
                    "`before` would now be wrong.",
            "false": "Everything a reader learned from `before` is still true according to `after`. Adding new "
                     "information, cutting information, or calling the same thing by another name or term doesn't "
                     "contradict it.",
        },
    },
    "same_meaning": {
        "type": "noul",
        "instructions": "Do `before` and `after` say the same thing in different words?",
        "criteria": {
            "true": "The edit rewords, tightens, reorders, or fixes grammar, spelling, or terminology, "
                    "and every claim in `before` is still in `after`.",
            "false": "`after` makes a claim `before` doesn't, or drops a claim `before` made.",
        },
    },
    "adds_information": {
        "type": "noul",
        "instructions": "Does `after` give the reader information that `before` doesn't contain?",
        "criteria": {
            "true": "`after` adds a new fact, example, step, caveat, or explanation.",
            "false": "Everything `after` says, `before` already said.",
        },
    },
    "drops_information": {
        "type": "noul",
        "instructions": "Does `after` leave out information that `before` gave the reader?",
        "criteria": {
            "true": "A fact, example, step, caveat, or explanation in `before` is gone from `after`.",
            "false": "Everything `before` said is still in `after`, possibly reworded.",
        },
    },
}


@dataclass
class Hunk:
    pr: int
    period: str
    commit: str
    claude: bool
    path: str
    before: str
    after: str
    lines: int
    truncated: bool = False
    cls: str = ""
    decided_by: str = ""
    contradicts: float | None = None
    same_meaning: float | None = None
    adds_information: float | None = None
    drops_information: float | None = None


# ---------- pure logic ----------

HUNK_HEADER = re.compile(r"^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@")


def parse_hunks(diff: str) -> list[tuple[str, list[str], list[str]]]:
    """Split a `-U0` diff into (path, removed lines, added lines) per hunk, doc files only."""
    hunks = []
    path = None
    cur = None
    old_path = None
    for line in diff.splitlines():
        if line.startswith("diff --git"):
            cur = None
        elif line.startswith("--- "):
            old_path = M._diff_path(line[4:])
        elif line.startswith("+++ "):
            path = M._diff_path(line[4:]) or old_path
        elif HUNK_HEADER.match(line):
            cur = (path, [], [])
            if path and M.is_doc_file(path):
                hunks.append(cur)
        elif cur is not None and line.startswith("-"):
            cur[1].append(line[1:])
        elif cur is not None and line.startswith("+"):
            cur[2].append(line[1:])
    return hunks


FORMAT_CHARS = re.compile(r"[*_`#>|\-\s]+")
FENCE = re.compile(r"^\s*(```|~~~)\w*\s*$")
TYPO_MAX_CHARS = 2


def formatting_only(before: str, after: str) -> bool:
    """True when the two sides differ only in markdown marks and whitespace."""
    return FORMAT_CHARS.sub("", before) == FORMAT_CHARS.sub("", after)


def precheck(before: str, after: str) -> str | None:
    """The class code can settle without Jev, or None."""
    if not before.strip():
        return "addition"
    if not after.strip():
        return "deletion"
    if formatting_only(before, after):
        return "formatting"
    if all(FENCE.match(x) for x in before.splitlines() + after.splitlines()):
        return "formatting"     # a code block's language label
    if is_typo_fix(before, after):
        return "typo"
    return None


def is_typo_fix(a: str, b: str) -> bool:
    """At most TYPO_MAX_CHARS characters inserted or deleted, none replaced, and no digit in or beside them.

    Replacements stay with Jev: one character can flip a value (a check mark to a cross,
    "2.5" to "3.1", "min" to "max").
    """
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    changed = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        if op == "replace":
            return False
        changed += max(i2 - i1, j2 - j1)
        near = a[max(i1 - 1, 0):i2 + 1] + b[max(j1 - 1, 0):j2 + 1]
        if any(ch.isdigit() for ch in near):
            return False
    return 0 < changed <= TYPO_MAX_CHARS


def decide(a: dict[str, float]) -> str:
    """Truth table from Jev's four answers to one class. Every combination has a row."""
    contra, same = a["contradicts"], a["same_meaning"]
    adds, drops = a["adds_information"], a["drops_information"]
    if contra >= YES:
        return "factual"
    if same >= YES:
        return "copy_edit"
    if adds >= YES and drops <= NO:
        return "elaboration"
    if drops >= YES and adds <= NO:
        return "deletion"
    if adds >= YES and drops >= YES:
        return "rewrite"
    return "unsettled"


def clip(text: str) -> tuple[str, bool]:
    if len(text) <= MAX_SIDE_CHARS:
        return text, False
    return text[:MAX_SIDE_CHARS], True


def state_for(h: Hunk) -> dict:
    return {
        "page": h.path,
        "about": "One edit made while revising a draft of Sensible's developer documentation. "
                 "`before` is the text the edit replaced and `after` is the text it put in its place.",
        "before": h.before,
        "after": h.after,
    }


# ---------- collection ----------

def collect(git: M.Git, prs: list[dict], cutoff: datetime) -> list[Hunk]:
    out = []
    for pr in sorted(prs, key=lambda p: p["number"]):
        merge = pr["mergeCommit"]["oid"]
        head = git.fetch_pr(pr["number"])
        base = git.merge_base(head, f"{merge}^1")
        commits = git.commits(base, head)
        draft = M.draft_commit(commits)
        period = M.period(M.ts(pr["createdAt"]), cutoff)
        for c in M.after_draft(commits, draft):
            for path, old, new in parse_hunks(git.diff(f"{c['sha']}^", c["sha"])):
                before, t1 = clip("\n".join(old))
                after, t2 = clip("\n".join(new))
                out.append(Hunk(pr=pr["number"], period=period, commit=c["sha"][:9], claude=c["claude"],
                                path=path, before=before, after=after, lines=len(old) + len(new),
                                truncated=t1 or t2))
    return out


def classify(hunks: list[Hunk]) -> None:
    for h in hunks:
        pre = precheck(h.before, h.after)
        if pre:
            h.cls, h.decided_by = pre, "code"
            continue
        resp = jev.call(json.dumps(state_for(h), ensure_ascii=False), QUESTIONS, model=MODEL)
        answers = {k: round(resp["answers"][k]["noul"], 3) for k in QUESTIONS}
        for k, v in answers.items():
            setattr(h, k, v)
        h.cls, h.decided_by = decide(answers), "jev"


# ---------- report ----------

def summarize(hunks: list[Hunk], doc_lines: dict[int, tuple[int, str]]) -> dict[str, dict]:
    out = {}
    for period in ("before", "after"):
        g = [h for h in hunks if h.period == period]
        prs = {n for n, p in doc_lines.items() if p[1] == period}
        size = sum(doc_lines[n][0] for n in prs)
        by = defaultdict(lambda: [0, 0])
        for h in g:
            by[h.cls][0] += 1
            by[h.cls][1] += h.lines
        out[period] = {"prs": len(prs), "doc_lines": size, "hunks": len(g),
                       **{c: {"hunks": by[c][0], "lines": by[c][1],
                              "per100": round(100 * by[c][1] / size, 2) if size else None} for c in CLASSES}}
    return out


def render(hunks: list[Hunk], doc_lines: dict[int, tuple[int, str]], replay: bool) -> str:
    s = summarize(hunks, doc_lines)
    b, a = s["before"], s["after"]
    jev_n = sum(1 for h in hunks if h.decided_by == "jev")
    lines = [
        "# Revisions after the AI draft, by kind",
        "",
        f"Model: `{MODEL}`. {len(hunks)} revision hunks; code settled {len(hunks) - jev_n} and Jev {jev_n}. "
        f"{'Answers replayed from recordings.' if replay else 'Answers fetched live and recorded.'}",
        f"PRs: {b['prs']} before, {a['prs']} after. Doc lines changed: {b['doc_lines']} before, {a['doc_lines']} after.",
        "",
        "A hunk is one contiguous block of changed lines in a diff: the lines an edit removed and the lines it put in "
        "their place. A hunk's size is its removed plus added lines. Moved text is counted twice, because git shows a "
        "move as a deletion hunk plus an addition hunk.",
        "",
        "## Revision lines per 100 doc lines, pooled",
        "",
        "| Kind | Before | After | Hunks before | Hunks after |",
        "|---|---|---|---|---|",
    ]
    for c in CLASSES:
        lines.append(f"| {c.replace('_', ' ')} | {b[c]['per100']} | {a[c]['per100']} | {b[c]['hunks']} | {a[c]['hunks']} |")
    lines += [
        "",
        "**Factual** is the closest proxy for a factual error corrected: after the edit, the page contradicts what the "
        "draft told a reader about the product. It also catches a fact that changed because the PR's scope changed, "
        "so check the list below. **Rewrite** replaced content without contradicting it.",
        "",
        "## Per PR",
        "",
        "| PR | Period | Doc lines | " + " | ".join(c.replace("_", " ") for c in CLASSES) + " |",
        "|---|---|---|" + "---|" * len(CLASSES),
    ]
    per = defaultdict(lambda: defaultdict(int))
    for h in hunks:
        per[h.pr][h.cls] += h.lines
    for n in sorted(doc_lines):
        size, period = doc_lines[n]
        lines.append(f"| #{n} | {period} | {size} | " + " | ".join(str(per[n][c]) for c in CLASSES) + " |")
    lines += ["", "## Factual changes", "", "Each hunk Jev called factual, for a reader to confirm.", ""]
    for h in hunks:
        if h.cls == "factual":
            lines.append(f"- #{h.pr} `{h.commit}` {h.path} ({h.contradicts}): "
                         f"`{_short(h.before)}` → `{_short(h.after)}`")
    return "\n".join(lines) + "\n"


def _short(text: str, n: int = 110) -> str:
    one = " ".join(text.split()).replace("`", "'")
    return one if len(one) <= n else one[: n - 1] + "…"


def validate(labels_path: Path) -> str:
    """Score the classifier against hand labels; returns a markdown table per labeled set."""
    rows = json.loads(labels_path.read_text())
    hunks = [Hunk(pr=r["pr"], period="", commit=r["commit"], claude=False, path=r["path"],
                  before=r["before"], after=r["after"], lines=0) for r in rows]
    classify(hunks)
    out = ["| Set | Hunks | Right | Unsettled | Wrong class | Called factual, wrongly |", "|---|---|---|---|---|---|"]
    for name in dict.fromkeys(r["set"] for r in rows):
        pairs = [(r["label"], h.cls) for r, h in zip(rows, hunks) if r["set"] == name]
        right = sum(a == b for a, b in pairs)
        unsettled = sum(b == "unsettled" for a, b in pairs)
        false_fact = sum(b == "factual" and a != "factual" for a, b in pairs)
        out.append(f"| {name} | {len(pairs)} | {right} | {unsettled} | {len(pairs) - right - unsettled} | {false_fact} |")
    misses = [f"- {r['set']} #{r['pr']} `{r['commit']}`: labeled {r['label']}, got {h.cls}"
              for r, h in zip(rows, hunks) if r["label"] != h.cls]
    return "\n".join(out + [""] + misses) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--metrics", type=Path, default=HERE / "output" / "per_pr.csv",
                    help="per_pr.csv from metrics.py; sets the PRs and their periods")
    ap.add_argument("--cutoff", default=M.DEFAULT_CUTOFF)
    ap.add_argument("--recordings", type=Path, default=HERE / "jev-recordings")
    ap.add_argument("--replay", action="store_true", help="answer only from recordings; never call the API")
    ap.add_argument("--validate", action="store_true",
                    help="score against classification-labels.json instead of classifying the PRs")
    ap.add_argument("--out", type=Path, default=HERE / "output")
    ap.add_argument("--cache", type=Path, default=HERE / "output" / "cache")
    ap.add_argument("--repo", type=Path, default=HERE.parents[1])
    args = ap.parse_args(argv)

    os.environ["JEV_REPLAY" if args.replay else "JEV_RECORD"] = str(args.recordings)
    if args.validate:
        print(validate(HERE / "classification-labels.json"), end="")
        return 0
    git, gh = M.Git(args.repo), M.GitHub(args.cache)
    cutoff = git.tag_date(args.cutoff)
    rows = list(csv.DictReader(args.metrics.open()))
    doc_lines = {int(r["number"]): (int(r["doc_lines"]), r["period"]) for r in rows}
    prs = [p for p in gh.merged_prs() if p["number"] in doc_lines]

    hunks = collect(git, prs, cutoff)
    classify(hunks)

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "revisions.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(hunks[0])))
        w.writeheader()
        w.writerows(asdict(h) for h in hunks)
    (args.out / "revisions.md").write_text(render(hunks, doc_lines, args.replay))
    print(f"wrote {args.out / 'revisions.md'} and revisions.csv ({len(hunks)} hunks)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
