# Design: tested claims as durable evidence

Status: proposed by Claude on 2026-11-19, shaped by Frances's direction; Frances answered the open questions the same day (see Answers). Built: the review step (§6), evidence records with schema and checks (§3), the pointer comment (§2), matrix rows (§4, linking the record rather than an HTML report), the stale warning, and the SQLite load (§7). Not built: HTML reports from records, and the `contrast` and `schema` kinds (§5).

## Why

`extract-testable-claims` finds the claims in a docs change worth testing, and on 2026-11-19 its tests found two wrong claims on the OCR preprocessor page (sensible-hq/sensible-docs#825). But the proof of those tests is weak:

- **It lives in account state.** The runs are in Frances's own account; an editor link shows a doc type's config *now*, so editing or deleting it loses what ran.
- **It's not in the repo.** Nothing ties a run to the claim's wording, the page, the commit, or the environment.
- **Nothing reruns it.** Claims rot: the `omit` → `ocrIfMissing` rename broke every test config within a day.

QA practice for this is a **traceability matrix** (claim ↔ test ↔ result) backed by **objective evidence**: expected vs. actual, inputs, version, date, environment, enough to reproduce (the regulated-validation standard; ISO/IEC/IEEE 29119-3 for test documentation). This repo already has both: the docs-test framework (`scripts/doc-detective/`) runs claims from page markup, saves scrubbed reports with `DOC_TESTS_SAVE_REPORT=1`, and generates `TEST-MATRIX.md`.

What it lacks, per Frances: **some claims shouldn't add runnable markup to the page.** Markup is visible in the page's HTML source, and a page with a dozen tested claims would be bloated with it. Many tested claims (schema compatibility, edge cases) don't need a weekly rerun either.

## Proposal

### 1. A "record only" priority, below priority 3

Today pages have priority 1 (weekly), 2 (monthly), or 3 (on demand only), in `test-pages.json` (see `.claude/sessions/doc-test-priorities/`). A **record-only** claim isn't runnable from the page at all. Its evidence is a committed record; anyone can recreate the test by hand from the record's fixtures.

### 2. One pointer comment per section

Instead of markup per claim, each section with record-only claims carries one short comment listing their IDs (Frances chose per section over per page):

```
{/* tested claims {"ids": ["ocr_if_missing_match_array", "ocr_if_missing_ocrs_every_page"]} */}
```

Each record names its section, and `evidence.py check` fails when the page's comment doesn't list the claim under that section.

The details live in the matrix and the evidence, not the page.

### 3. Evidence records

One committed JSON file per claim, `scripts/doc-detective/evidence/<feature>-<parameter>/<id>.json` (for example `ocr-ocr-if-missing`), with its own top-level schema, `schemas/evidence.schema.json`:

- the claim, quoted (not a line number, which drifts), its page, and its kind (from `extract-testable-claims/criteria.md`);
- each config that ran, the document, expected and actual values, and the extraction IDs;
- the environment (prod or dev, which account), the engine commit or date, and when it ran;
- the verdict (holds, contradicted, bug reported) and what changed on the page because of it;
- Frances's approval and date.

The configs, PDFs, and responses go in `evidence/<feature>-<parameter>/files/`, each cited with its SHA-256, so the test can be recreated and an edit is caught. Not in `fixtures/`: those folders are test-account fixtures with a manifest, which the runner restores before each run.

### 4. A durable report and a matrix row

A scrubbed HTML report generated from each record, saved in `reports/` like today's saved reports. `test_matrix.py` reads the evidence records too, so each claim gets a matrix row: "record only (not run)", the evidence date, and the report link.

### 5. Promotion

A record-only claim can later become runnable by giving it a code-test kind. Two kinds the 2026-11-19 tests needed and the framework lacks:

- **`contrast`**: several configs on one document, each with expected field values; covers claims that need a control run (both tests above).
- **`schema`**: publish a config, expect it accepted or rejected; covers type, required, and compatibility claims.

### 6. A review step in `extract-testable-claims`

After tests run, the skill presents each proposed matrix entry (claim, what ran, result, proposed priority) and the exact pointer comment for the page. Frances approves, edits, rejects, or changes the priority per claim. Nothing goes into the matrix, the evidence folder, or the page until she approves it, and the approval is recorded in the evidence.

## Conflicts with the current framework

1. **"A marked-up test with no result is 'not run', which fails the page"** (from `.claude/sessions/doc-test-results/`). The pointer comment isn't a test, so the runner must read it as a pointer. The cost: record-only evidence can go stale without failing anything. Mitigation: the matrix shows each record's age; optionally a CI warning after N months.
2. **`TEST-MATRIX.md` is generated; don't edit it by hand.** Still true: rows come from evidence records.
3. **Priority is per page today; record-only is per claim.** A page can have both runnable and record-only claims, so record-only can't just be a page priority value.

### 7. Ready for a database

Frances may build a database (SQLite) on the traceability matrix later. The matrix stays a generated view; the database would be a second view of the same committed JSON, so neither can drift from the records. The records are shaped for that:

- **Stable keys.** `claim_id` is unique across the repo (the same namespace as code test IDs); `run_id` is unique within a record; files are keyed by SHA-256, so two claims citing one PDF share a row.
- **One table per level, no nesting below it.** A record is one `claims` row; each run one `runs` row; each checked field one `run_fields` row. `expected` and `actual` are any JSON value, stored as JSON text.
- **Enums and ISO dates** for verdict, role, environment, account, claim kind, and run dates, so queries can group and compare them.
- **`schema_version`**, so a loader can migrate old records when a field changes meaning.

`evidence.py sqlite FILE` does the load today, and a unit test loads records into SQLite with foreign keys on. Example: `SELECT claim_id, run_id, field, expected, actual FROM run_fields JOIN runs USING (claim_id, run_id) WHERE role = 'test' AND expected <> actual` lists the two runs where the OCR page's claims and reality diverged. Saved results (`reports/*.json`) and page markup aren't loaded yet; they already have stable test IDs, so they'd add `tests` and `test_results` tables keyed the same way.

## Answers (2026-11-19)

1. **Evidence that already ran:** record it now as what ran (`omit`, production, Frances's personal account, marked `account: personal`), and rerun in the docs test account with `ocrIfMissing` after the deploy.
2. **Pointer comment:** one per section, not one per page.
3. **Stale evidence:** CI annotates a record whose newest run is more than 183 days old; it never fails the run.
4. **Code-test kinds:** the record-only path first; `schema` next, since 2 of #825's 3 untested claims are publish-accepts-or-rejects claims.
5. **Schema location:** a new top-level `schemas/evidence.schema.json`; `record.schema.json` describes one automated code-test result.
6. **Contradicted claims:** get a record, with `page_change` naming the commit that fixed the page.
