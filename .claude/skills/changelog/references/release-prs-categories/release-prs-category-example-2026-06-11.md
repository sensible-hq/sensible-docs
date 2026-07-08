# Release PRs Categorization Example — June 11, 2026

**Source:** #documentation, June 11 2026
**Published changelog:** https://docs.sensible.so/changelog/june-2026
**Slack thread:** https://sensiblehq.slack.com/archives/C0215T9K86P/p1781205752224129

## Pattern

Frances posts the changelog link as the main message, then replies to herself with:
- `## investigated, not documenting` — items she looked at but skipped (often with a brief reason)
- raw release notes text from #engineering — the full blocks she reviewed to make the decision

Items marked "save for next changelog" are deferred, not dropped.

---

## investigated, not documenting

- **doc-type: default ocr_engine to amazon in createDocType (#3355)** — bug fix, no docs
- **region: add asImage option to output a rendered data-URI image (#3351)** — save for next changelog
- **extractions: attribute each extraction to the actor that initiated it (#3349)** — save for next changelog

---

## release notes reviewed (not documented)

### June 9 (Devon)
- Add classifyAndQuery SenseML method (single-call classify + extract over the full document) (#3361) — no public docs for now
- Dependency cleanup and vulnerability remediation (#3363)
- Remove packages/infra-sst-v2 (#3362)
- infra-global: grant engineers deploy-time permissions (#3360)
- Drop Pulumi import: adoption directives (#3359)
- Capture hubspotutk on trial signups for HubSpot attribution (#1825)

### June 2 (Horacio)
- checkbox transform fix (#3343)
- Scope queryGroup pageRange to the subdocument in portfolios (#3356) — bug fix, no docs
- quotas: pace all services via GCRA reservations instead of exponential backoff (#3353)
- Retire infra-sst-v2 application stack (#3348)
- doc-type: default ocr_engine to amazon in createDocType (#3355)
- log-watcher: refactor error dispatch and harden Slack thread updates (#3354)
- fix update conflict when xlsx bytes are uploaded under a declared xls content type (#3352)
- infra-region: migrate per-region resources out of legacy v2 stack (#3345)
- textract: drop dormant per-stage Textract infra from v2 (#3347)

### May 26 (Horacio)
- Bump uuid from 8.3.2 to 14.0.0 (#3317)
- extractions: denormalize total cost onto the dynamo extraction item (#3344)
- infra-global: split global resources out of the legacy v2 stack (#3336)
- rate-limit script: accept data-stage format like dev-uswest2 (#3341)
- event-collector: capture queue events into a test-local buffer (#3340)

### May 19 (Horacio)
- email processor: render PDF preview for PNG/JPG attachments (#3338)
- email decoder: exclude body-embedded images from attachments (#3339)
- treat xls/xlsx/xlsm as interchangeable for content-type validation (#3337)
- infra-stage-ephemeral: restore lambda memory/timeout parity with legacy serverless.yml (#3335)
- extraction page: show extraction id alongside document name (#1820)

### May 11
*(covered by last month's changelog)*
