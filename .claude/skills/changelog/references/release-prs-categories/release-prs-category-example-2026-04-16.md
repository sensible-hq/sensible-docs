# Release PRs Categorization Example — April 16, 2026

**Source:** #documentation, April 16 2026
**Published changelog:** https://docs.sensible.so/changelog/april-2026
**Slack thread:** https://sensiblehq.slack.com/archives/C0215T9K86P/p1776380094083859

---

## investigated, not documenting

- **sections: skip anchors inside a section y-boundary after an explicit stop (#3275)** — bug fix?

---

## release notes reviewed (not documented)

### April (Devon)
- webhook extractions: change from Record to array with taskId (#3297)
- dependabot fix for lodash (#3298)
- conversion-lambda: skip rebuilding if images exist (#3294)
- Limit extraction errors to 20 with deduplication (#3292)
- add null-safe substr to json logic (#3293)
- classify timed-out async extractions via SQS SentTimestamp (#3291)
- avoid zod in types used by ts-json-schema (#3290)
- fix: send docType IDs instead of names in email processor payloads (#1803)
- feat: show creation date on email processor cards (#1804)
- feat: show document name in extraction breadcrumbs (#1801)

### April (Horacio)
- fix: bundle inbound rate limit Lua script with Lambda (#3277)
- Block RFC 2606/6761 reserved domains as webhook destinations (#3281)

### April (Horacio)
- feat: expose segment_documents_with in portfolio extraction responses (#3276)
- Usage alerts for metered accounts (#3274)
- Add inbound rate limiting for auth endpoints (50 req/5min per IP) (#3270)
- Bump mailparser from 3.7.4 to 3.9.3 (#3262)
- Upgrade vulnerable packages (#3273)
- fix deps (#1794)
- Remove portfolio filter alert on configuration filter (#1790)
- feat: merge document type and configuration columns in extractions table (#1792)
- security: resolve 17 of 20 npm audit vulnerabilities (#1791)

### Covered last month
- deps: upgrade canvas from 2.11.2 to 3.2.1 (#3269)
- Fix SSRF: block private/reserved IP ranges in URL validation (#3266)
- feat: disable quick edit per account (#3265)
- sections: allow stop lines that sort before the anchor on the same visual row (#3268)
- Filter extractions by configuration - backfill (#3263)
- email-decoder: fix recipient detection for aliased addresses (#3264)
- Accept gclid/gbraid/wbraid in signup and forward to Segment (#3258)
- Filter-extractions-by-configuration - enable filtering for Portfolio extractions (#3259)
- email-decoder: move to per-stage ApplicationStack (#3261)
- Sanitize CSV export functionality for formula-related characters (#3260)
- feat: improve trial banners with upgrade + support contact (#1784)
- feat: improve subscription UX for non-admin users (#1783)
- Capture gclid/gbraid/wbraid from Google Ads cookies at signup (#1781)
