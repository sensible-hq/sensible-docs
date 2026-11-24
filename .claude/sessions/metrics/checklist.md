# metrics checklist

Claude Code session name: metrics
Claude Code session ID: d32f2166-35fb-4ec7-a267-5f5b90720310
Started: 2026-11-24

This checklist is the progress record. The design is in `design.md`; how it's built is in `implementation.md`.

## Context

- Goal: measure whether the skill rework reduced draft-to-merge back-and-forth on docs PRs that follow a backend change.
- Frances approved draft survival, post-merge fixes, size normalization, and reporting size and feature type next to each number. The design calls are Claude's.
- Claude Code transcripts only go back to 2026-10-26 (the 30-day default cleanup), so session correction turns can't be compared before and after.

## Tasks

- [x] Design doc
- [x] Implementation doc
- [x] Pure functions and unit tests
- [x] Git and GitHub adapters, end-to-end test on a throwaway repo (25 tests pass)
- [x] Live run on the real PR history
  - [x] Exclude referencing PRs that change no doc files (#734, #741, #826)
  - [x] Add commits after the draft, because single-commit PRs score 100% survival trivially
  - [x] Spot-check #798 by hand: its 7 commits match the counts; fix candidates #509 and #812 are real follow-ups, #727 looks unrelated
- [x] Snapshot of the report: `report-2026-11-24.md`
- [x] PR
- [ ] Rerun once 8 or more "after" PRs have merged and their 30-day fix windows have closed
- [x] Audit: draft survival was inflated and hand edits undercounted; fixed on the metrics PR
- [x] Transcript retention set to 365 days (`cleanupPeriodDays` in `~/.claude/settings.json`)
- [x] Stacked PR: classify revisions with Jev (`classification-design.md`)
  - [x] Probe questions on 15 hunks with telling commit messages
  - [x] Random sample exposed "says something different" firing on additions; switched to a contradiction question
  - [x] Blind test on 20 more: 14 right, 6 unsettled, 0 wrong, 0 false factual
  - [x] Full run: 755 hunks, 585 through Jev, recordings committed; replay is byte-identical
- [ ] Rerun both reports once 8 or more "after" PRs have merged
