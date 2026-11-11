#!/usr/bin/env python3
"""Baseline metrics for AI-assisted docs PRs: how much rework each PR needed.

  python3 scripts/style_baseline/pr_metrics.py --since 2026-06-01 [--toggl toggl.csv] [--out DIR]

For each merged PR that changes docs/ or reference/ Markdown, it reads:
  GitHub       timing, commits, review comments (gh api; branch commits via refs/pull/N/head)
  git          lines added per commit on content files, against the PR's final diff (churn)
  Vale         warnings and errors on the changed pages at the first commit and at the last
  transcripts  your prompts, interruptions, and correction-like prompts on the PR's branch
               (~/.claude/projects; Claude Code deletes these after cleanupPeriodDays)
  Toggl        hours whose description names the PR number or branch (optional detailed CSV)

Writes prs.csv (one row per PR), revisions.csv (one row per revision commit, with an empty
rule_id column to label by hand), and summary.md. Rerun with the same window after the cleanup
and compare the two summaries.
"""
import argparse
import csv
import json
import re
import statistics
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                           check=True).stdout.strip())
REPO = "sensible-hq/sensible-docs"
CONTENT = re.compile(r"^(docs|reference)/.*\.md$")
CLAUDE = re.compile(r"Co-Authored-By: Claude", re.I)
TRANSCRIPTS = Path.home() / ".claude/projects"
VALE = next((p for p in ["vale", str(Path.home() / ".local/bin/vale")]
             if subprocess.run(["which", p], capture_output=True).returncode == 0
             or Path(p).exists()), None)

# Rough categories for revision commit messages. Hand labels in revisions.csv are the real data.
CATEGORIES = [
    ("style", r"style|wording|word|framing|voice|tone|phras|em dash|comment|capitali|terminolog|"
              r"excerpt|rename|heading|you-centric|intro|reword|sentence"),
    ("example", r"example|output|config|screenshot|pdf|image|sample"),
    ("fact", r"correct|accura|verif|behavio|null|claim|wrong|clarif|note"),
    ("structure", r"restructur|move|section|order|consolidat|split|merge .*section|remove|drop|cut"),
]
CORRECTION = re.compile(
    r"^\s*(no\b|nope|don'?t|do not|why (did|are|is)|actually|instead|wrong|that'?s not|not quite|"
    r"you (missed|forgot|didn'?t)|should(n'?t)? |stop |undo|revert|again)", re.I)


def sh(*args, cwd=ROOT, check=True):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=check).stdout


def gh(path):
    """Every item of a paginated list endpoint."""
    out = sh("gh", "api", "--paginate", "--jq", ".[]", f"{path}?per_page=100")
    return [json.loads(l) for l in out.splitlines() if l.strip()]


def merged_prs(since):
    out = sh("gh", "pr", "list", "-R", REPO, "--state", "merged", "--limit", "300", "--json",
             "number,title,headRefName,createdAt,mergedAt,author,files,mergeCommit")
    prs = []
    for pr in json.loads(out):
        files = [f["path"] for f in pr["files"] if CONTENT.match(f["path"])]
        if pr["mergedAt"][:10] >= since and files and pr["author"]["login"] != "app/github-actions":
            prs.append(dict(pr, content_files=files))
    return sorted(prs, key=lambda p: p["number"])


def numstat(sha, files):
    """Lines added on content files by one commit."""
    out = sh("git", "show", "--numstat", "--format=", sha, "--", *files, check=False)
    return sum(int(a) for a, *_ in (l.split("\t") for l in out.splitlines()) if a.isdigit())


def vale_alerts(sha, files):
    """Warnings and errors Vale reports on these pages as of one commit."""
    if not VALE:
        return None
    total = 0
    with tempfile.TemporaryDirectory() as tmp:
        for f in files:
            text = subprocess.run(["git", "show", f"{sha}:{f}"], cwd=ROOT, capture_output=True,
                                  text=True).stdout
            if not text:
                continue
            p = Path(tmp) / f
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
            out = subprocess.run([VALE, "--config", str(ROOT / ".vale.ini"), "--output=JSON",
                                  "--minAlertLevel=warning", str(p)], capture_output=True, text=True).stdout
            try:
                total += sum(len(v) for v in json.loads(out or "{}").values())
            except json.JSONDecodeError:
                pass
    return total


def transcript_index():
    """Your prompts per branch: (timestamp, text)."""
    idx = {}
    for f in TRANSCRIPTS.glob("-home-franc-GitHub-sensible-docs*/*.jsonl"):
        if "-gen" in f.parent.name:
            continue
        for line in f.open():
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            c = d.get("message", {}).get("content") if d.get("type") == "user" else None
            if isinstance(c, list):
                c = " ".join(x.get("text", "") for x in c if x.get("type") == "text")
            if c and not c.startswith("<"):
                idx.setdefault(d.get("gitBranch"), []).append((d.get("timestamp", ""), c))
    return idx


def toggl_hours(path):
    """(description, hours) for each row of a Toggl detailed-report CSV."""
    rows = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            h, m, s = (int(x) for x in r.get("Duration", "0:0:0").split(":"))
            rows.append((r.get("Description", ""), h + m / 60 + s / 3600))
    return rows


def diff(after, before):
    """Alerts the PR added to its pages (negative: it fixed existing ones)."""
    return after - before if after is not None and before is not None else ""


def category(msg):
    return next((name for name, pat in CATEGORIES if re.search(pat, msg, re.I)), "other")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-06-01")
    ap.add_argument("--toggl")
    ap.add_argument("--out", default=str(ROOT / "design/style-baseline"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    talk = transcript_index()
    toggl = toggl_hours(a.toggl) if a.toggl else []
    rows, revisions = [], []
    for pr in merged_prs(a.since):
        n, files = pr["number"], pr["content_files"]
        sh("git", "fetch", "-q", "origin", f"pull/{n}/head:refs/baseline/pr-{n}", check=False)
        commits = (gh(f"repos/{REPO}/pulls/{n}/commits"))
        comments = (gh(f"repos/{REPO}/pulls/{n}/comments"))
        reviews = (gh(f"repos/{REPO}/pulls/{n}/reviews"))
        content = [c for c in commits if len(c["parents"]) == 1 and numstat(c["sha"], files) > 0]
        if not content:
            continue
        base_alerts = vale_alerts(content[0]["parents"][0]["sha"], files)
        added = [numstat(c["sha"], files) for c in content]
        final = numstat(pr["mergeCommit"]["oid"], files) if pr.get("mergeCommit") else 0
        for c in content[1:]:
            msg = c["commit"]["message"].split("\n")[0]
            revisions.append({"pr": n, "sha": c["sha"][:9], "by": "claude" if CLAUDE.search(
                c["commit"]["message"]) else "human", "category": category(msg), "message": msg,
                "rule_id": ""})
        prompts = talk.get(pr["headRefName"], [])
        hours = sum(h for d, h in toggl if f"#{n}" in d or pr["headRefName"] in d)
        opened = datetime.fromisoformat(pr["createdAt"].replace("Z", "+00:00"))
        merged = datetime.fromisoformat(pr["mergedAt"].replace("Z", "+00:00"))
        rows.append({
            "pr": n, "title": pr["title"][:70], "branch": pr["headRefName"], "merged": pr["mergedAt"][:10],
            "pages": len(files), "hours_open": round((merged - opened).total_seconds() / 3600, 1),
            "content_commits": len(content), "revision_commits": len(content) - 1,
            "human_commits": sum(1 for c in content if not CLAUDE.search(c["commit"]["message"])),
            "style_revisions": sum(1 for r in revisions if r["pr"] == n and r["category"] == "style"),
            "review_comments": sum(1 for c in comments if c["user"]["type"] != "Bot"),
            "review_rounds": sum(1 for r in reviews if r["user"]["type"] != "Bot"),
            "lines_final": final, "lines_written": sum(added),
            "churn": round(sum(added) / final, 2) if final else "",
            "cohort": "page-task" if len(files) <= 6 else "bulk",
            "vale_introduced_first": diff(vale_alerts(content[0]["sha"], files), base_alerts),
            "vale_introduced_merged": diff(vale_alerts(content[-1]["sha"], files), base_alerts),
            "prompts": len(prompts) or "",
            "correction_prompts": sum(1 for _, t in prompts if CORRECTION.search(t)) or "",
            "interrupts": sum(1 for _, t in prompts if "[Request interrupted" in t) or "",
            "toggl_hours": round(hours, 2) if toggl else "",
        })
        print(f"#{n}: {rows[-1]['revision_commits']} revisions, churn {rows[-1]['churn']}")

    for name, data in (("prs.csv", rows), ("revisions.csv", revisions)):
        if data:
            with open(out / name, "w", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(data[0]))
                w.writeheader()
                w.writerows(data)
    write_summary(out / "summary.md", rows, revisions, a, toggl)


def med(rows, key):
    vals = [r[key] for r in rows if isinstance(r[key], (int, float))]
    return (statistics.median(vals), len(vals)) if vals else ("n/a", 0)


def write_summary(path, rows, revisions, a, toggl):
    keys = [("revision_commits", "Revision commits per PR"), ("style_revisions", "Style revision commits per PR"),
            ("human_commits", "Your hand-edit commits per PR"), ("review_comments", "Review comments per PR"),
            ("churn", "Churn (lines written / lines merged)"), ("vale_introduced_first", "Vale alerts introduced, first draft"),
            ("vale_introduced_merged", "Vale alerts introduced, merged"), ("hours_open", "Hours from open to merge"),
            ("prompts", "Your prompts per PR (transcripts)"), ("correction_prompts", "Correction prompts per PR"),
            ("toggl_hours", "Toggl hours per PR")]
    cats = {}
    for r in revisions:
        cats[r["category"]] = cats.get(r["category"], 0) + 1
    task = [r for r in rows if r["cohort"] == "page-task"]
    bulk = [r for r in rows if r["cohort"] == "bulk"]
    lines = [f"# Style baseline: merged content PRs since {a.since}", "",
             f"Generated {datetime.now():%Y-%m-%d} by `scripts/style_baseline/pr_metrics.py`. "
             f"{len(rows)} PRs: {len(task)} page tasks (6 pages or fewer), {len(bulk)} bulk.", "",
             "Medians; n = PRs with data.", "",
             "| metric | page tasks | n | bulk | n |", "| ------ | ---------: | -: | ---: | -: |"]
    lines += [f"| {label} | {med(task, k)[0]} | {med(task, k)[1]} | {med(bulk, k)[0]} | {med(bulk, k)[1]} |"
              for k, label in keys]
    lines += ["", "Revision commits by message category (keyword heuristic; label `rule_id` in revisions.csv):", "",
              "| category | commits |", "| -------- | ------: |"]
    lines += [f"| {c} | {n} |" for c, n in sorted(cats.items(), key=lambda x: -x[1])]
    if toggl:
        lines += ["", f"Toggl: {sum(h for _, h in toggl):.1f} hours in the export, "
                      f"{sum(r['toggl_hours'] or 0 for r in rows):.1f} matched to a PR."]
    path.write_text("\n".join(lines) + "\n")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
