# Release PRs Categorization Example — March 16, 2026

**Source:** #documentation, March 16 2026
**Published changelog:** https://docs.sensible.so/changelog/march-2026
**Slack thread:** https://sensiblehq.slack.com/archives/C0215T9K86P/p1773705153012869

**Note:** Filter-extractions-by-configuration (#3259) was initially in "investigated, not documenting" but was added to the changelog after discussion with Jason and Horacio.

---

## investigated, not documenting

- **image file support in sensible app** — still not working properly (open PR), won't announce till it's fixed
- **Filter-extractions-by-configuration - enable filtering for Portfolio extractions (#3259)** — initially seemed like a bug fix; added to changelog after team discussion
- **upgrade uses of GPT 4 variants (#3224)** — internal/backend changes
- **Excel reader: handle pseudo-XLS files (#3257)** — bug fix (some systems save tab-delimited or XML text with .xls extension); could be boasted as feature if thorny enough, but treated as fix
- **add us-east-2 region (#3246)** — checked w/ Horacio, no user-facing update necessary

---

## release notes reviewed (not documented)

### March 10 (Horacio)
- Accept gclid/gbraid/wbraid in signup and forward to Segment (#3258)
- email-decoder: move to per-stage ApplicationStack (#3261)
- Sanitize CSV export functionality for formula-related characters (#3260)
- feat: improve trial banners with upgrade + support contact (#1784)
- feat: improve subscription UX for non-admin users (#1783)
- Capture gclid/gbraid/wbraid from Google Ads cookies at signup (#1781)

### March 3 (Horacio)
- feat: add extraction response types for frontend sync (#3253)
- zod validation support in api (#3249)
- queryDynamoWithPaging is time boxed (#3255)
- Change source of "Your trial is almost over" email from Josh to Jason (#3254)
- replace chalk.blue/gray with visible colors for dark terminals (#3252)
- feat: replace Extraction type with synced backend response types (#1775)
- Extractions table: partial page alert and remove portfolio filter warning (#1776)
- Update customer logos on sign-in page (#1777)

### Feb 24 (Horacio)
- log-watcher: enrich Slack thread titles with request context and fix us-east-2 test URL (#3248)
- Fix smoke tests for HTTP API v2 compatibility and add custom API URL support (#3247)
- fix: restore sync-to-app workflow (#3238)
- Bump ajv from 8.17.1 to 8.18.0 (#3245)
- Documentation: Reorganize Claude Code skills and update project documentation (#3216)
- security: fix dependency vulnerabilities (Feb 2026 audit) (#1774)
- test: add comprehensive test coverage across app (#1764)
- Fix frontend type errors from backend sync (#1765)
- Claude Code setup: CLAUDE.md and skills config (#1766)
- Fix stale token cache causing stuck page after refresh (#1771)

### Feb 17 (Horacio)
- fix: resolve 5 security vulnerabilities via dependency updates (#3244)
- email processors - endpoints - part 1 (#3237)
- Fix topologicalSort dropping lines involved in cycles (#3239)
- remove jay's users from global stage (#3231)
- clean-up router deprecated options (#3241)
- Remove legacy Zuplo gateway code and configuration mode (#3240)
- email processors - portfolio extractions support - int tests (#3236)
- email processors - portfolio extractions support (#3235)
- Use Vertex generateContent endpoint for gemini LLM calls (#3233)
- email-extractions-endpoints - step 2 - allow extractions targeting specific environments (#3220)
- Fix URL path handling in generate_upload_url to avoid trailing slash (#1768)

### Feb 10 (Horacio)
- use anchor to determine whether to run method with fullDocument mode (queryGroup) (#3229)
- fix: resolve security vulnerabilities from pnpm audit (#3228)
- Fix deployment to production related procedures (#3225)
- add above scope to map_with_index (#3227)
- fix: resolve security vulnerabilities from pnpm audit (#1762)

### Feb 3
*(covered by last month)*
