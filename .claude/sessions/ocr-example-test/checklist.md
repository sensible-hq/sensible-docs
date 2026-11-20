# ocr-example-test checklist

Claude Code session name: (not set; resumed from the ocrIfMissing handoff)
Claude Code session ID: 182a711b-cc3c-4499-b338-54f7a8efa58c
PR: sensible-hq/sensible-docs#840, branch `ocr-example-test`, worktree `~/GitHub/sensible-docs-ocr-example-test`

## Why
Frances chose a documented-output test on the OCR preprocessor example over building `schema` and `contrast` claim kinds (2026-11-20): the costly drift is a documented example that stops working, and the existing output kind catches it.

## Done
- [x] Example marked up as code test `extract_ocr_if_missing_quote`
- [x] Page added to `test-pages.json`, priority 2, watching the example PDF
- [x] Local run passes (output identical); report saved; matrix regenerated; 298 unit tests pass

## To do
- [ ] Review and merge #840
- [ ] After merge: confirm the push to `v0` runs the page in CI, then `close-docs-pr`
