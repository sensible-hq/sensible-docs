# column-stop-docs checklist

Claude Code session name: column-stop-docs
Claude Code session ID: 9bb92619-2b00-442e-9dc7-828734bf1dc3
Source PR: sensible-hq/sensible#3477 (merged 2026-09-22)
Docs PR: sensible-hq/sensible-docs#729

## Done
- [x] Read PR #3477 diff (column.ts, types.ts)
- [x] Add Stop parameter row to column.md, aligned with Document Range / Text Table Stop wording
- [x] Full style pass (all style-guide files, revise-doc-style, you-centric framing)
- [x] "Stop at the next label" example added, then removed per user (superfluous)
- [x] Create column_stop.pdf; upload to doc type column_stop; verify output via extract API
- [x] Address review comment on intro sentence (line 23)
- [x] Update existing "Extract a column" example with Stop param, row_column_example.pdf, user's config (verified in SenseML editor)
- [x] Inline comments: canonical + authored, after commas, in all configs
- [x] Vale: 0 errors; remaining warnings are spatial "above"

## Open
- [x] Stop example: no example document (column_stop.pdf and .png dropped per user)
- [x] column_stop_blank.pdf: not committed (no Stop example PDF in docs)
- [x] Neighboring-column sentence: keep. User confirmed it is intended behavior, not a bug (2026-09-30)
- [ ] Optional: republish column_example config in Sensible account with after-comma comment style
- [ ] Optional: delete test doc types column_stop / column_example from the Sensible account
- [ ] Review and merge docs PR #729
- [ ] After merge: remove worktree ~/GitHub/sensible-docs-column-stop, delete branch, remove it from additionalDirectories, pull v0
