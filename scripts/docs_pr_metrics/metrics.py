#!/usr/bin/env python3
"""Measure draft-to-merge back-and-forth on docs PRs that follow a backend change.

Compares merged sensible-docs PRs created before and after a cutoff tag on:
human commits, human-edited doc lines, AI draft survival, post-merge fixes,
and backend-to-docs lag, each normalized per 100 doc lines changed.

Design: .claude/sessions/metrics/design.md
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import statistics
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path

DOCS_REPO = "sensible-hq/sensible-docs"
DEFAULT_CUTOFF = "skills-archive-2026-10"
FIX_WINDOW_DAYS = 30
FIX_MAX_DOC_FILES = 10
FIX_MIN_LINE_CHARS = 15

BACKEND_REF = re.compile(
    r"(?:github\.com/sensible-hq/(sensible(?:-app)?)/pull/(\d+))"
    r"|(?:(?<![\w/-])(?:sensible-hq/)?(sensible(?:-app)?)#(\d+))"
)
# "sensible#3519, #3533 and #3540": bare numbers continuing a list belong to the same repo.
LIST_TAIL = re.compile(r"(?:,\s*|,?\s+and\s+|\s*/\s*)#(\d+)")
# The docs skill's own invocation, "/update-docs-from-pr 3235", names an engine PR.
SKILL_REF = re.compile(r"update-docs-from-pr\s+((?:\d+[\s,]*)+)")
CLAUDE_TRAILER = re.compile(r"^co-authored-by:\s*claude\b", re.I | re.M)


# ---------- pure logic ----------

def backend_refs(text: str) -> list[tuple[str, int]]:
    """Return sorted unique (repo, number) backend PR references in text."""
    text = text or ""
    refs = set()
    for m in BACKEND_REF.finditer(text):
        repo = m.group(1) or m.group(3)
        refs.add((repo, int(m.group(2) or m.group(4))))
        pos = m.end()
        while tail := LIST_TAIL.match(text, pos):
            refs.add((repo, int(tail.group(1))))
            pos = tail.end()
    for m in SKILL_REF.finditer(text):
        refs.update(("sensible", int(n)) for n in re.findall(r"\d+", m.group(1)))
    return sorted(refs)


def is_doc_file(path: str) -> bool:
    if path.startswith("docs/") and path.endswith(".md"):
        return True
    return path.startswith("reference/") and path.count("/") == 1 and path.endswith(".json")


def is_claude_commit(message: str) -> bool:
    return bool(CLAUDE_TRAILER.search(message or ""))


def draft_commit(commits: list[dict]) -> str | None:
    """The PR's first commit that touches doc files, when Claude co-authored it.

    `commits` is oldest first; each has `sha`, `claude` (bool), `doc_files` (list).
    Every later commit is revision, whoever wrote it: dictated edits land as
    Claude commits, so a longer "draft" would absorb the revisions it should measure.
    A PR whose first doc commit is Frances's has no AI draft.
    """
    for c in commits:
        if c["doc_files"]:
            return c["sha"] if c["claude"] else None
    return None


def _norm(line: str) -> str:
    return line.strip()


def survival(draft_added: dict[str, list[str]], net_added: dict[str, list[str]]) -> tuple[int, int]:
    """(survived, total) significant draft-added lines that the merged PR still adds.

    Matched against the PR's net added lines, not the whole final file, so a draft
    line identical to one already on the page can't survive by coincidence.
    Multiset match per file, whitespace-trimmed: each net line can claim one draft line.
    Lines too short to carry content (fences, table rules, braces) aren't counted.
    """
    survived = total = 0
    for path, lines in draft_added.items():
        pool = Counter(_norm(x) for x in net_added.get(path, []))
        for line in lines:
            key = _norm(line)
            if not significant(key):
                continue
            total += 1
            if pool[key] > 0:
                pool[key] -= 1
                survived += 1
    return survived, total


def word_survival(draft_added: dict[str, list[str]], net_added: dict[str, list[str]]) -> tuple[int, int]:
    """(survived, total) words of the draft's added lines that the merged PR still adds, in order.

    Per file, the longest matching blocks between the two word sequences
    (difflib with autojunk off, so the result doesn't depend on a heuristic).
    One reworded word in a table row costs one word, not the whole row.
    """
    survived = total = 0
    for path, lines in draft_added.items():
        draft_words = " ".join(lines).split()
        net_words = " ".join(net_added.get(path, [])).split()
        total += len(draft_words)
        sm = difflib.SequenceMatcher(None, draft_words, net_words, autojunk=False)
        survived += sum(b.size for b in sm.get_matching_blocks())
    return survived, total


def significant(line: str) -> bool:
    s = line.strip()
    return len(s) >= FIX_MIN_LINE_CHARS and any(ch.isalpha() for ch in s)


def fix_overlap(added: dict[str, list[str]], later_deleted: dict[str, list[str]]) -> int:
    """Count significant lines a later PR deleted that this PR added, per file."""
    hits = 0
    for path, lines in later_deleted.items():
        mine = {_norm(x) for x in added.get(path, []) if significant(x)}
        hits += sum(1 for x in lines if _norm(x) in mine)
    return hits


def period(created: datetime, cutoff: datetime) -> str:
    return "after" if created >= cutoff else "before"


def post_draft_commits(commits: list[dict], draft: str | None) -> int:
    """Doc-touching commits after the draft commit: the PR's revision rounds."""
    return len(after_draft(commits, draft))


def after_draft(commits: list[dict], draft: str | None) -> list[dict]:
    """Doc-touching commits after the draft, oldest first."""
    if draft is None:
        return []
    shas = [c["sha"] for c in commits]
    return [c for c in commits[shas.index(draft) + 1:] if c["doc_files"]]


def per100(count: float | None, size: int) -> float | None:
    if count is None or not size:
        return None
    return round(100 * count / size, 2)


def parse_diff(diff: str) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Split a unified diff (`git diff -U0`) into added and deleted lines per doc file."""
    added: dict[str, list[str]] = {}
    deleted: dict[str, list[str]] = {}
    old_path = new_path = None
    for line in diff.splitlines():
        if line.startswith("--- "):
            old_path = _diff_path(line[4:])
        elif line.startswith("+++ "):
            new_path = _diff_path(line[4:])
        elif line.startswith("+") and new_path and is_doc_file(new_path):
            added.setdefault(new_path, []).append(line[1:])
        elif line.startswith("-") and old_path and is_doc_file(old_path):
            deleted.setdefault(old_path, []).append(line[1:])
    return added, deleted


def _diff_path(raw: str) -> str | None:
    raw = raw.strip()
    if raw.startswith('"'):
        raw = raw[1:-1].encode().decode("unicode_escape").encode("latin-1").decode("utf-8")
    if raw == "/dev/null":
        return None
    return raw[2:] if raw[:2] in ("a/", "b/") else raw


# ---------- git and GitHub adapters ----------

def run(cmd: list[str], cwd: Path | None = None) -> str:
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True).stdout


class Git:
    def __init__(self, repo: Path):
        self.repo = repo

    def __call__(self, *args: str) -> str:
        return run(["git", "-c", "core.quotepath=off", *args], cwd=self.repo)

    def fetch_pr(self, number: int) -> str:
        ref = f"refs/pr/{number}"
        try:
            self("rev-parse", "--verify", "-q", ref)
        except subprocess.CalledProcessError:
            self("fetch", "-q", "origin", f"pull/{number}/head:{ref}")
        return self("rev-parse", ref).strip()

    def merge_base(self, a: str, b: str) -> str:
        return self("merge-base", a, b).strip()

    def commits(self, base: str, head: str) -> list[dict]:
        out = self("log", "--reverse", "--no-merges", "--no-renames", "--format=%x1e%H%x1f%B%x1f", "--numstat", f"{base}..{head}")
        commits = []
        for rec in out.split("\x1e")[1:]:
            sha, msg, stat = rec.split("\x1f")
            doc_files, doc_lines = [], 0
            for row in stat.strip().splitlines():
                parts = row.split("\t")
                if len(parts) == 3 and is_doc_file(parts[2]):
                    doc_files.append(parts[2])
                    if parts[0] != "-":
                        doc_lines += int(parts[0]) + int(parts[1])
            commits.append({"sha": sha, "claude": is_claude_commit(msg),
                            "doc_files": doc_files, "doc_lines": doc_lines})
        return commits

    def diff(self, a: str, b: str) -> str:
        return self("diff", "-U0", "--no-renames", a, b, "--", "docs", "reference")

    def tag_date(self, tag: str) -> datetime:
        return datetime.fromisoformat(self("log", "-1", "--format=%cI", tag).strip())


class GitHub:
    def __init__(self, cache: Path):
        self.cache = cache
        cache.mkdir(parents=True, exist_ok=True)

    def _cached(self, name: str, cmd: list[str]):
        f = self.cache / name
        if f.exists():
            return json.loads(f.read_text())
        data = json.loads(run(cmd))
        f.write_text(json.dumps(data))
        return data

    def merged_prs(self, refresh: bool = False) -> list[dict]:
        if refresh:
            (self.cache / "merged_prs.json").unlink(missing_ok=True)
        return self._cached("merged_prs.json", [
            "gh", "pr", "list", "-R", DOCS_REPO, "--state", "merged", "--limit", "2000",
            "--json", "number,title,body,createdAt,mergedAt,mergeCommit"])

    def fetched_at(self) -> str:
        f = self.cache / "merged_prs.json"
        return datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M") if f.exists() else "never"

    def backend_merged_at(self, repo: str, number: int) -> str | None:
        data = self._cached(f"backend_{repo}_{number}.json", [
            "gh", "pr", "view", str(number), "-R", f"sensible-hq/{repo}", "--json", "mergedAt"])
        return data.get("mergedAt")


# ---------- assembly ----------

@dataclass
class PRMetrics:
    number: int
    title: str
    period: str
    created: str
    merged: str
    backend: str
    doc_lines: int = 0
    new_pages: int = 0
    commits: int = 0
    human_commits: int = 0
    human_doc_lines: int = 0
    draft_lines: int | None = None
    draft_kept: int | None = None
    draft_words: int | None = None
    draft_words_kept: int | None = None
    draft_word_survival: float | None = None
    post_draft_commits: int = 0
    revision_lines: int | None = None
    revision_lines_claude: int | None = None
    revision_lines_per100: float | None = None
    draft_survival: float | None = None
    fixes: int = 0
    fix_prs: str = ""
    fix_window: str = "closed"
    lag_days: float | None = None
    human_commits_per100: float | None = None
    human_doc_lines_per100: float | None = None
    fixes_per100: float | None = None
    _added: dict = field(default_factory=dict, repr=False)


def ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def measure_pr(git: Git, gh: GitHub, pr: dict, cutoff: datetime) -> PRMetrics:
    refs = backend_refs(f"{pr['title']}\n{pr['body']}")
    m = PRMetrics(number=pr["number"], title=pr["title"],
                  period=period(ts(pr["createdAt"]), cutoff),
                  created=pr["createdAt"][:10], merged=pr["mergedAt"][:10],
                  backend=" ".join(f"{r}#{n}" for r, n in refs))
    merge = pr["mergeCommit"]["oid"]
    added, _ = parse_diff(git.diff(f"{merge}^1", merge))
    m._added = added
    numstat = git("diff", "--numstat", "--no-renames", f"{merge}^1", merge)
    for row in numstat.splitlines():
        a, d, p = row.split("\t")
        if is_doc_file(p) and a != "-":
            m.doc_lines += int(a) + int(d)
    m.new_pages = sum(1 for row in git("diff", "--name-status", "--no-renames",
                                       f"{merge}^1", merge).splitlines()
                      if row.startswith("A\t") and is_doc_file(row[2:]))

    head = git.fetch_pr(pr["number"])
    base = git.merge_base(head, f"{merge}^1")
    commits = git.commits(base, head)
    m.commits = len(commits)
    human = [c for c in commits if not c["claude"]]
    m.human_commits = len(human)
    m.human_doc_lines = sum(c["doc_lines"] for c in human)

    draft = draft_commit(commits)
    m.post_draft_commits = post_draft_commits(commits, draft)
    if draft:
        draft_added, _ = parse_diff(git.diff(f"{draft}^", draft))
        kept, total = survival(draft_added, added)
        revisions = after_draft(commits, draft)
        m.revision_lines = sum(c["doc_lines"] for c in revisions)
        m.revision_lines_claude = sum(c["doc_lines"] for c in revisions if c["claude"])
        m.draft_lines, m.draft_kept = total, kept
        m.draft_words_kept, m.draft_words = word_survival(draft_added, added)
        if m.draft_words:
            m.draft_word_survival = round(m.draft_words_kept / m.draft_words, 3)
        m.draft_survival = round(kept / total, 3) if total else None

    merged_dates = [d for d in (gh.backend_merged_at(r, n) for r, n in refs) if d]
    if merged_dates:
        m.lag_days = round((ts(pr["mergedAt"]) - max(ts(d) for d in merged_dates)).total_seconds() / 86400, 1)

    m.human_commits_per100 = per100(m.human_commits, m.doc_lines)
    m.human_doc_lines_per100 = per100(m.human_doc_lines, m.doc_lines)
    m.revision_lines_per100 = per100(m.revision_lines, m.doc_lines)
    return m


def attach_fixes(git: Git, rows: list[PRMetrics], all_prs: list[dict], now: datetime) -> None:
    deleted_cache: dict[int, tuple[int, dict]] = {}

    def later_deleted(pr: dict):
        if pr["number"] not in deleted_cache:
            merge = pr["mergeCommit"]["oid"]
            added, deleted = parse_diff(git.diff(f"{merge}^1", merge))
            deleted_cache[pr["number"]] = (len(set(added) | set(deleted)), deleted)
        return deleted_cache[pr["number"]]

    by_number = {p["number"]: p for p in all_prs}
    all_prs = sorted(all_prs, key=lambda p: p["number"])
    for m in rows:
        start = ts(by_number[m.number]["mergedAt"])
        end = start + timedelta(days=FIX_WINDOW_DAYS)
        if end > now:
            m.fix_window = "open"
        touched = set(m._added)
        hits = []
        for p in all_prs:
            if not p.get("mergeCommit") or p["number"] == m.number:
                continue
            if not (start < ts(p["mergedAt"]) <= end):
                continue
            n_files, deleted = later_deleted(p)
            if n_files > FIX_MAX_DOC_FILES or not touched & set(deleted):
                continue
            if fix_overlap(m._added, deleted):
                hits.append(p["number"])
        m.fixes = len(hits)
        m.fix_prs = " ".join(f"#{n}" for n in sorted(hits))
        m.fixes_per100 = per100(m.fixes, m.doc_lines)


# ---------- report ----------

# (field, label, lower_is_better). Medians are per PR; pooled rates are sum over sum.
MEDIAN_METRICS = [
    ("doc_lines", "Doc lines changed (PR size)"),
    ("commits", "Commits"),
    ("post_draft_commits", "Doc commits after the AI draft"),
    ("revision_lines_per100", "Revision lines after the draft, per 100 doc lines"),
    ("human_doc_lines_per100", "Lines Frances committed herself, per 100 doc lines"),
    ("draft_word_survival", "AI draft survival, words"),
    ("draft_survival", "AI draft survival, whole lines"),
    ("fixes_per100", "Post-merge fixes per 100 doc lines"),
    ("lag_days", "Lag, backend merge to docs merge (days)"),
]


def median(values: list) -> float | None:
    vals = [v for v in values if v is not None]
    return round(statistics.median(vals), 3) if vals else None


def pooled(group: list[PRMetrics], num: str, den: str, scale: int = 100) -> float | None:
    """Sum of `num` over sum of `den`, skipping PRs where either is missing."""
    pairs = [(getattr(r, num), getattr(r, den)) for r in group
             if getattr(r, num) is not None and getattr(r, den)]
    total = sum(d for _, d in pairs)
    return round(scale * sum(n for n, _ in pairs) / total, 2) if total else None


def summarize(rows: list[PRMetrics]) -> dict[str, dict]:
    out = {}
    for name in ("before", "after"):
        g = [r for r in rows if r.period == name]
        n = len(g)
        s = {"n": n,
             "new_page_share": round(sum(1 for r in g if r.new_pages) / n, 2) if n else None,
             "revised_share": round(sum(1 for r in g if r.post_draft_commits) / n, 2) if n else None,
             "no_draft": sum(1 for r in g if r.draft_lines is None),
             "fixes_total": sum(r.fixes for r in g),
             "open_windows": sum(1 for r in g if r.fix_window == "open"),
             "doc_lines_total": sum(r.doc_lines for r in g),
             "pooled_revision": pooled(g, "revision_lines", "doc_lines"),
             "pooled_human": pooled(g, "human_doc_lines", "doc_lines"),
             "pooled_survival": pooled(g, "draft_kept", "draft_lines", scale=1),
             "pooled_word_survival": pooled(g, "draft_words_kept", "draft_words", scale=1),
             "pooled_word_survival_revised": pooled([r for r in g if r.post_draft_commits],
                                                    "draft_words_kept", "draft_words", scale=1),
             "pooled_fixes": pooled(g, "fixes", "doc_lines")}
        for key, _ in MEDIAN_METRICS:
            s[key] = median([getattr(r, key) for r in g])
        out[name] = s
    return out


def fmt(v) -> str:
    if v is None:
        return "–"
    if isinstance(v, float) and 0 < v <= 1 and v != int(v):
        return f"{v:.2f}"
    return str(v)


def render_report(rows: list[PRMetrics], cutoff_tag: str, cutoff: datetime,
                  excluded: list[int] | None = None, as_of: datetime | None = None,
                  fetched: str | None = None) -> str:
    s = summarize(rows)
    b, a = s["before"], s["after"]
    small = min(b["n"], a["n"])
    lines = [
        "# Docs PR metrics: before and after the skill rework",
        "",
        f"Cutoff: `{cutoff_tag}` ({cutoff.date()}). A PR is \"after\" when it was created on or after the cutoff.",
        *([f"As of: {as_of.date()}. PR list fetched from GitHub: {fetched}. "
           "Rerunning with the same `--as-of` and cache gives the same numbers; `--refresh` picks up newer PRs."]
          if as_of else []),
        f"Population: merged sensible-docs PRs that reference a sensible or sensible-app PR. "
        f"n = {b['n']} before, {a['n']} after.",
        *([f"Excluded because they change no doc files: {', '.join(f'#{n}' for n in excluded)}."] if excluded else []),
        "",
    ]
    if small < 8:
        lines += [f"> **Small sample.** The smaller period has {small} PRs, so one PR can move any number below. "
                  "Read the per-PR table before quoting an aggregate.", ""]
    lines += [
        "## Aggregates",
        "",
        "Pooled rates divide the period's total by its total doc lines, so large PRs weigh more. "
        "Medians weigh every PR equally.",
        "",
        "| Metric | Before | After |",
        "|---|---|---|",
        f"| PRs | {b['n']} | {a['n']} |",
        f"| Doc lines changed, total | {b['doc_lines_total']} | {a['doc_lines_total']} |",
        f"| Revision lines after the draft per 100 doc lines, pooled | {fmt(b['pooled_revision'])} | {fmt(a['pooled_revision'])} |",
        f"| Lines Frances committed herself per 100 doc lines, pooled | {fmt(b['pooled_human'])} | {fmt(a['pooled_human'])} |",
        f"| AI draft survival, words, pooled | {fmt(b['pooled_word_survival'])} | {fmt(a['pooled_word_survival'])} |",
        f"| AI draft survival, words, pooled, PRs revised after the draft only | {fmt(b['pooled_word_survival_revised'])} | {fmt(a['pooled_word_survival_revised'])} |",
        f"| AI draft survival, whole lines, pooled | {fmt(b['pooled_survival'])} | {fmt(a['pooled_survival'])} |",
        f"| Post-merge fixes per 100 doc lines, pooled | {fmt(b['pooled_fixes'])} | {fmt(a['pooled_fixes'])} |",
        f"| Post-merge fixes, total | {b['fixes_total']} | {a['fixes_total']} |",
    ]
    for key, label in MEDIAN_METRICS:
        lines.append(f"| {label}, median | {fmt(b[key])} | {fmt(a[key])} |")
    lines += [
        f"| Share of PRs revised after the draft | {fmt(b['revised_share'])} | {fmt(a['revised_share'])} |",
        f"| Share of PRs adding a new page | {fmt(b['new_page_share'])} | {fmt(a['new_page_share'])} |",
        f"| PRs with no AI draft (first doc commit is Frances's) | {b['no_draft']} | {a['no_draft']} |",
        "",
        "Lower is better for revision lines, Frances's lines, fixes, and lag. Higher is better for draft survival. "
        "PR size and the new-page share check that the periods compare like with like.",
        "",
        "## How to read each number",
        "",
        "- **AI draft:** the PR's first commit that touches doc files, when Claude co-authored it. Everything after it is revision.",
        "- **Revision lines:** lines added plus deleted on doc files in every commit after the draft, whoever made it. "
        "This is the main back-and-forth measure, because edits Frances dictates to Claude land as Claude commits.",
        "- **Lines Frances committed herself:** doc lines in commits without a Claude co-author trailer. "
        "A floor on her hand edits: an edit she makes in her editor and Claude then commits counts as Claude's.",
        "- **AI draft survival, words:** the share of the draft's added words that the merged PR still adds, in order. "
        "The headline survival number. A PR with no commits after the draft scores 1.0 by construction, "
        "so the revised-only row shows survival without those PRs.",
        "- **AI draft survival, whole lines:** the share of the draft's added lines, 15 or more characters with a letter, that the merged PR "
        "still adds unchanged. One reworded word makes a line not survive. A draft spread over several commits "
        "only counts its first commit, so later additions lower the denominator, not the rate.",
        "- **Post-merge fixes:** later PRs of 10 or fewer doc files, merged within "
        f"{FIX_WINDOW_DAYS} days, that delete a line this PR added. Matched on text, not intent: check the list. "
        f"{a['open_windows'] + b['open_windows']} PRs still have an open window, so their counts can grow.",
        "- **Lag:** from the latest-merged backend PR the docs PR references. An old reference inflates it: context only.",
        "- **Practice effect:** Frances's prompting has improved over the same months, and no PR metric separates that "
        "from the skill changes.",
        "",
        "## Per PR",
        "",
        "| PR | Period | Merged | Doc lines | New pages | Commits | Commits after draft | Revision lines "
        "| Revision per 100 | Frances's lines | Draft words | Survival, words | Survival, lines | Fixes | Lag (days) |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in sorted(rows, key=lambda r: (r.merged, r.number)):
        fixes = f"{r.fixes} ({r.fix_prs})" if r.fixes else "0"
        if r.fix_window == "open":
            fixes += ", open"
        lines.append(
            f"| #{r.number} | {r.period} | {r.merged} | {r.doc_lines} | {r.new_pages} | {r.commits} "
            f"| {r.post_draft_commits} | {fmt(r.revision_lines)} | {fmt(r.revision_lines_per100)} "
            f"| {r.human_doc_lines} | {fmt(r.draft_words)} | {fmt(r.draft_word_survival)} | {fmt(r.draft_survival)} | {fixes} | {fmt(r.lag_days)} |")
    return "\n".join(lines) + "\n"


def write_csv(rows: list[PRMetrics], path: Path) -> None:
    dicts = [{k: v for k, v in asdict(r).items() if not k.startswith("_")} for r in rows]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(dicts[0]))
        w.writeheader()
        w.writerows(dicts)


def main(argv: list[str] | None = None) -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cutoff", default=DEFAULT_CUTOFF, help="tag or commit that splits before from after")
    ap.add_argument("--since", default="2026-01-01", help="ignore PRs merged before this date")
    ap.add_argument("--as-of", help="date that closes fix windows (default: today); pin it to reproduce a run")
    ap.add_argument("--refresh", action="store_true", help="refetch the merged PR list instead of using the cache")
    ap.add_argument("--out", type=Path, default=here / "output")
    ap.add_argument("--cache", type=Path, default=here / "output" / "cache")
    ap.add_argument("--repo", type=Path, default=here.parents[1])
    args = ap.parse_args(argv)

    git, gh = Git(args.repo), GitHub(args.cache)
    cutoff = git.tag_date(args.cutoff)
    tz = cutoff.tzinfo
    since = datetime.fromisoformat(args.since).replace(tzinfo=tz)
    as_of = (datetime.fromisoformat(args.as_of).replace(tzinfo=tz) + timedelta(days=1)
             if args.as_of else datetime.now(tz))
    all_prs = [p for p in gh.merged_prs(args.refresh) if p.get("mergeCommit") and ts(p["mergedAt"]) < as_of]
    population = [p for p in all_prs
                  if ts(p["mergedAt"]) >= since and backend_refs(f"{p['title']}\n{p['body']}")]

    rows = []
    for p in sorted(population, key=lambda p: p["number"]):
        print(f"#{p['number']} {p['title'][:60]}", file=sys.stderr)
        rows.append(measure_pr(git, gh, p, cutoff))
    excluded = [r.number for r in rows if not r.doc_lines]
    rows = [r for r in rows if r.doc_lines]
    attach_fixes(git, rows, [p for p in all_prs if ts(p["mergedAt"]) >= since], now=as_of)

    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(rows, args.out / "per_pr.csv")
    (args.out / "report.md").write_text(render_report(rows, args.cutoff, cutoff, excluded,
                                                           as_of - timedelta(days=1) if args.as_of else as_of,
                                                           gh.fetched_at()))
    print(f"wrote {args.out / 'report.md'} and per_pr.csv ({len(rows)} PRs)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
