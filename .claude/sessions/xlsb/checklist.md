# xlsb docs checklist

Claude Code session name: xlsb
Claude Code session ID: 1e71441a-3c84-48a0-baa5-c36aac379bbb
Source PR: sensible-hq/sensible#3474 (Accept xlsb workbooks as a spreadsheet input)
Frontend PR: sensible-hq/sensible-app#1882 (Frontend side of xlsb support)

- [x] Read engine PR and diff
- [x] Search docs/ and reference/ for xlsm, xlsx, and spreadsheet MIME types
- [x] Add XLSB to the spreadsheet formats list in concepts/file-types.md
- [x] Add `application/vnd.ms-excel.sheet.binary.macroenabled.12` to request bodies and content-type enums in openapi_extraction.json, openapi_classification.json, openapi_configuration.json
- [ ] Vale check (vale MCP server failed to connect this session; change is one token in an existing list)
- [x] Open docs PR
- [x] Confirm the Extract tab accepts .xlsb: yes, sensible-hq/sensible-app#1882 (merged) adds it to the dropzone and golden/quick-extraction pickers
- [ ] After merge: run close-docs-pr

## Production API tests (2026-10-12), sample: tests/data/test.xlsb from sensible-hq/sensible#3474

- Reference document (configuration API): create on `cells` with xlsb content_type → 200; PUT to upload_url → 200; GET shows converted_url + thumbnail, error null. Deleted afterward (204, then 404). **Works.**
- Binary request body endpoints all fail with "Missing request body" (400) for BOTH macroenabled types:
  - POST /classify, POST /classify/async, POST /extract/{type}, with xlsb or xlsm content type
  - Control: same bytes declared as xlsx reach the engine ("No match found"), so the reader is fine
  - 415 message for a wrong-case header lists the xlsb type as allowed, so #3474 is deployed
  - Likely cause: API gateway binary media types don't include the macroenabled types. Pre-existing for xlsm.
- [x] Add repeatable test: scripts/test/file_types/smoke_test_xlsb.sh (sample in scripts/test/assets/xlsb_sample.xlsb)
- [ ] Report the gateway bug to engineering; decide whether to hold PR #741
