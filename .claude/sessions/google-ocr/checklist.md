# google-ocr checklist

Claude Code session name: google-ocr
Claude Code session ID: bc2d327b-1002-40d8-9161-f39ecf5a8273
Session directory: /home/franc/GitHub/sensible-docs
Docs PR: sensible-hq/sensible-docs#801 (branch `fe_google_ocr_page_limit_docs`, worktree `~/GitHub/sensible-docs-google-ocr-page-limit`)
App PRs: sensible-hq/sensible-app#1905, sensible-hq/sensible-app#1906 (stacked on #1905)
Earlier in this session: sensible-hq/sensible-docs#798 (Lazarus deprecation, merged)

See [progress.md](progress.md) for what happened and [decisions.md](decisions.md) for why.

## Lazarus deprecation (sensible-hq/sensible#3468), docs PR #798
- [x] OCR engine page: Lazarus marked deprecated, reroute to Microsoft explained, removed from excerpt
- [x] OpenAPI: `lazarus` removed from `ocr_engine` enum, with `x-internal-note`
- [x] `x-internal-note`: Amazon is the default for new doc types (Microsoft only when no engine is stored)
- [x] Reverted the wrong "Microsoft is the default for doc types" commit
- [x] Vale, JSON, Redocly, CI checks; squash-merged as 457c445be
- [x] Changelog entry drafted: `drafts/changelog-entry-lazarus-ocr.md` in the main repo (uncommitted, by design)
- [x] Worktree removed, local branch deleted, v0 pulled
- [ ] close-docs-pr: create and close the sensible-docs issue (blocked by permissions; body in session scratchpad, command in chat)
- [ ] close-docs-pr: swap sensible#3468 label `doc_changes_needed` → `docs_done` (blocked by permissions)
- [ ] Decide which month's changelog gets the Lazarus entry (engine PR merged 2026-09-15)

## App help text: default engine, sensible-app#1905
- [x] DocTypeForm.tsx and SettingsTab.tsx: "Amazon is the default engine"
- [ ] Review (Kevin, asked in #frontend) and merge

## Google OCR page limit and line merging, docs PR #801 and app PR #1906
- [x] Confirm in code: no page cap (5-page chunks, 5 at a time, since sensible#1120)
- [x] Confirm no other engine-wide page cap (grep of `src/`; only a response-size 413)
- [x] Find the June 2022 origin of "25 pages" (Slack #engineering thread, sensible-app#541)
- [x] Test: 72-page image-only PDF with Google OCR, plus `prevent_default_merge_lines` and Amazon control
- [x] Turn the test into fixture `fixture_ocr_google_page_limit` (renamed in place in the test account)
- [x] Commit fixture files and `scripts/test/assets/beazley_scanned_72_pages.pdf`; runner `fixture_drift` reports no drift
- [x] OCR engine page: Google row drops the 5-page limit and the "doesn't merge words" claim
- [x] App PR #1906: drop 25 pages, rewrite merge-lines sentence, drop contradictory "Amazon is an alternative"
- [x] Vale on ocr-engine.md: 0 errors, 0 warnings
- [ ] Review and merge docs PR #801
- [ ] Merge app #1905, then #1906 (retargets to main)
- [ ] Optional: check the Merge Lines page's handwriting example ("Google by default groups text into words") by rerunning it
- [ ] Optional: runner support for fixture tests that compare `parsed_document`, so a page can test this fixture
- [ ] After #801 merges: run close-docs-pr (issue, labels if any engine PR applies, worktree cleanup)
- [ ] After app PRs merge: remove worktrees `~/GitHub/sensible-app-ocr-default-help` and `~/GitHub/sensible-app-google-ocr-help`

## Other follow-ups found along the way
- [ ] `microsoftRead` OCR engine exists in the engine but isn't documented (asked Horacio in Slack 2026-09-15)
