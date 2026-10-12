# xlsb docs checklist

Claude Code session name: xlsb
Claude Code session ID: 1e71441a-3c84-48a0-baa5-c36aac379bbb
Source PR: sensible-hq/sensible#3474 (Accept xlsb workbooks as a spreadsheet input)

- [x] Read engine PR and diff
- [x] Search docs/ and reference/ for xlsm, xlsx, and spreadsheet MIME types
- [x] Add XLSB to the spreadsheet formats list in concepts/file-types.md
- [x] Add `application/vnd.ms-excel.sheet.binary.macroenabled.12` to request bodies and content-type enums in openapi_extraction.json, openapi_classification.json, openapi_configuration.json
- [ ] Vale check (vale MCP server failed to connect this session; change is one token in an existing list)
- [x] Open docs PR
- [ ] Confirm whether the Sensible app's Extract tab upload picker accepts .xlsb (file-types table claims spreadsheet formats work there; PR #3474 is engine-only)
- [ ] After merge: run close-docs-pr
