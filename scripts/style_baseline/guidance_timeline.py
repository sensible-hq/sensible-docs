#!/usr/bin/env python3
"""When each skill, guide, and Vale file was started, last majorly revised, and last touched.

  python3 scripts/style_baseline/guidance_timeline.py

A major revision is a commit whose added plus deleted lines reach 20% of the file's current
length. Dates are from `git log --follow`, so files moved in from outside the repo start at the move.
"""
import glob
import subprocess

FILES = (sorted(glob.glob(".claude/skills/*/SKILL.md")) + sorted(glob.glob(".claude/style-guide/*.md"))
         + [".claude/preferences/editorial-preferences.md", ".claude/knowledge/fingerprints.md",
            ".claude/skills/blog-short/blog-short-template.md", ".claude/skills/changelog/structural-check.md",
            ".vale.ini", ".claude/hooks/vale-check.sh", ".github/styles/config/vocabularies/Sensible/accept.txt"]
         + sorted(glob.glob(".github/styles/Sensible/*.yml")))

print("file\tstarted\tmajor_done\tlast\tcommits\tmajor")
for f in FILES:
    size = max(1, sum(1 for _ in open(f)))
    out = subprocess.run(["git", "log", "--follow", "--format=@%ad", "--date=short", "--numstat", "--", f],
                         capture_output=True, text=True).stdout
    commits = []
    for line in out.splitlines():
        if line.startswith("@"):
            commits.append([line[1:], 0])
        elif line.strip() and commits:
            a, d, *_ = line.split("\t")
            commits[-1][1] += sum(int(x) for x in (a, d) if x.isdigit())
    if not commits:
        print(f"{f}\tuncommitted")
        continue
    commits.reverse()
    major = [c for c in commits if c[1] >= 0.2 * size] or commits[:1]
    print(f"{f}\t{commits[0][0]}\t{major[-1][0]}\t{commits[-1][0]}\t{len(commits)}\t{len(major)}")
