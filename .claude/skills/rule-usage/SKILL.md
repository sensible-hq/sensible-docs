---
name: rule-usage
description: Weekly style rule usage scores from Frances's local Claude Code transcripts. Counts which Vale and Jev rules fired while the agent wrote docs, whether the agent acted on each, and whether the change was reverted or pushed back on; writes style-rules/usage/<week>.json, commits it on a branch, and opens a PR so the usage report workflow renders the HTML. Invoke when Frances asks for the weekly usage run, rule usage scores, "which rules are firing", or "did I accept the style rewrites".
allowed-tools: Bash(python3 scripts/style/rule_usage.py:*), Bash(git worktree:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr create:*), Bash(gh pr view:*), Read
---

Transcripts live only on this machine and Claude Code deletes them after 30 days, so this runs locally once a week. Only counts are committed: the repo is public, so no message text leaves the machine.

1. Sync and branch: from the main checkout, `git checkout v0 && git pull`, then `git worktree add ../sensible-docs-rule-usage-<week> -b rule-usage-<week>` and work there.
2. Collect: `python3 scripts/style/rule_usage.py collect --local-excerpts` (the last complete ISO week; `--week 2026-W46` for another, within 30 days). It prints the week file it wrote and the path of a local HTML report that includes the pushback excerpts (Frances's own messages after a style fix). Open that local report for Frances; it's never committed or uploaded.
3. Read the numbers back in two or three sentences: firings this week, the rules with the most firings, any rule whose acted-on firings were reverted or pushed back on, and registered rules that never fired.
4. Commit only `style-rules/usage/<week>.json`, push the branch, and open a PR against v0 titled "Style rule usage: <week>". When it merges, the "Style rule usage report" workflow renders every week as an HTML report and links it from the run summary.
