# probe_endpoints improvement checklist

- [ ] Save test configs + PDFs locally so tests can be regenerated against different accounts without depending on remote assets
- [ ] Fix `extract_sync` test: it should use a local file upload, not polling — verify it's not inadvertently hitting the async path
- [ ] Figure out how to get `file_metadata` to appear in snapshot responses (currently only `info` sub-keys show up for the test PDF; need a PDF that triggers `metadata` and top-level `error` fields)
- [ ] Define deterministic rules (or a skill) for comparing sample responses in the web API reference against snapshots — currently done ad-hoc
- [ ] Reduce `PORTFOLIO_TYPES` to just the `api_skill_*` prefixed type (currently `["bank_statements", "api_skill_pay_stubs", "1040s"]`)
