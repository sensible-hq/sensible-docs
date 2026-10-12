# api-contract

Claude Code session name: api-contract
Claude Code session ID: e9f96182-829b-4f55-9faf-40475a33c4c1
Session directory: /home/franc/GitHub/sensible-docs
Worktree: /home/franc/GitHub/sensible-docs-openapi-drift (branch openapi-drift)

Goal: detect drift between the hand-maintained OpenAPI specs in /reference and the
backend (checked 2026-10-12), and fix confirmed drift.

## Done
- [x] Prototype a skeleton-spec generator and structural diff (kept out of this repo for now)
- [x] Verify each DRIFT finding against backend source by hand
- [x] Fix confirmed drift in openapi_extraction.json and openapi_configuration.json
- [x] Redocly lint: valid, no new warnings vs base
- [x] Re-run drift check: only 2 known false positives remain (GET /documents/{id}
      classificationSummary and configuration are correctly documented)

## Open
- [ ] PR review + merge
- [ ] Decide whether drift tooling lives in this public repo (see sensitivity discussion)
- [ ] Review-level findings not fixed in this PR: generate_upload_url missing ocr_engine,
      ocr_every_page, force_malware_scan; undocumented query params withMetadata,
      include_invalid, next, batch_id, extraction_id, environment
