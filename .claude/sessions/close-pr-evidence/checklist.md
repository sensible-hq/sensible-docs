# close-pr-evidence checklist

- Session: xlsb (1e71441a-3c84-48a0-baa5-c36aac379bbb)
- Worktree: `~/GitHub/sensible-docs-close-pr-evidence`, branch `fe_close_pr_test_evidence`

Frances (2026-11-12): when a docs PR merges, close-docs-pr attaches the final HTML test report, with a link that opens it rendered. It's the evidence the merge is OK.

- [x] New Step 3 in close-docs-pr: comment on the docs PR with a rendered link per tested page. The saved report is linked through githack, pinned to the merge commit (permanent); if the PR saved none, the skill runs the page in CI on v0 and links that run's report (rendered for signed-in users, but expires after 90 days) and asks about saving a permanent one
- [x] Checked: githack serves a committed report as text/html at a commit-pinned URL; CI artifacts are named `doc-tests-<page>-report.html`
- [ ] Frances: optionally add `Bash(gh workflow run:*)`, `Bash(gh run:*)`, `Bash(git show:*)`, `Bash(curl:*)`, and `Bash(python3 scripts/doc-detective/test_matrix.py:*)` to the skill's `allowed-tools`. The auto-mode classifier blocked Claude from widening the skill's own permissions, so these commands prompt for now
