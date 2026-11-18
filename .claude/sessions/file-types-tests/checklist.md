# file-types-tests checklist

- Session: xlsb continuation (2ee92462-6c8b-42e1-bea3-6b1926a1caf5)
- Worktree: `~/GitHub/sensible-docs-file-types-tests`, branch `fe_file_types_tests`

- [x] Embedded classification tests under footnote 3 of `file-types.md`: `classify_excel_formats_as_xlsx` (8 requests, including the XLSX control) and `classify_csv_not_supported` (2 requests), against `fixture_spreadsheet_classify` (commission statement files)
- [x] `file-types.md` back in `test-pages.json` at priority 3 (on demand)
- [x] Saved report and results at commit e3057fb48: both pass; TEST-MATRIX.md regenerated
- [ ] Footnote 1's extraction claims (XLS, XLSM, and XLSB need base64 on the synchronous endpoint; lowercase content types) aren't covered: no claim kind sends a file's bytes to an extraction endpoint by content type. `scripts/test/file_types/smoke_test_xlsb.sh` checks them outside the embedded tests
