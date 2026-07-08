# Release PRs Categorization — July 8, 2026

**Release notes covered:** June 16 – July 1, 2026 (#engineering)
**Categorized:** July 8, 2026

---

## document in changelog

- Upgrade Gemini models to 3.x + make confidence-signals LLM engine configurable (#3346) — already docs'd June 22
- region method: support percentOverlapX/percentOverlapY thresholds (#3375) — already docs'd July 2
- Add a today operator to JSONLogic (#3374) — already docs'd July 7
- Add bulk actions to Reference Documents (delete, assign, unassociate) (#1830)

---

## investigate

- Support selective config import from the config library (#3364) + Allow selecting individual configs when importing from library (#1831) — user-facing UI feature, likely one changelog entry
- Support Cmd+click to insert bounding box text on macOS (#1826) — small but user-facing
- Add word wrap toggle to config editor (#1827) — UI quality-of-life
- email-decoder: keep order-email label/value pairs together across PDF page breaks (#3369) — could be relevant for email processor users
- Processors complete best-effort instead of all-or-nothing (#3372) — behavior change for email processor users
- email processors: preserve original attachment filenames as document_name (#3373) — user-facing API change
- Autogen: improve performance, step 1 (#3384) — could be worth a brief mention

---

## don't document

- Per-engineer (per-eph) frontends (#3365) — internal
- infra-global: grant nicolas console + accounts-manager access (#3367) — internal
- Speed up HumanReview e2e setup and cache Next.js build in CI (#1832) — internal
- Upgrade react-pdf 7.7.3 to 10.4.1 (#1829) — internal dep upgrade
- Resolve node-fetch url-handling deprecations in Lambda (#3379) — internal
- Use correct page numbers in search by summarization prompt (#3378) — bug fix
- Default PDFDocument.load to empty password so restricted PDFs load (#3380) — bug fix
- Restrict self-serve sign-up to allowlist on dev and exp1 (#3376) — internal
- Malware-scan S3 uploads via GuardDuty for accounts that require it (#3371) — infra/security
- Fix LLM error message (#3370) — bug fix
- Resolve all pnpm audit vulnerabilities (1 critical, 31 high, 33 mod/low) (#1833) — internal
- infra-stage-data: add 1-day data retention for incentiv-thrive's POC (#3383) — infra
- Group extraction-queue messages by account to enable SQS fair queues (#3382) — infra
- Provide wasmUrl so pdf.js 5 can decode JPEG2000 images (#1838) — internal fix
- Add Pfizer SAML SSO provider (#3386) — customer-specific
- accounts CLI: add malware-scan command to toggle per-account document scanning (#3385) — internal CLI
