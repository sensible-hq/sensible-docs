# Design: tested claims as durable evidence (proposal, not built)

Status: proposed by Claude on 2026-11-19, shaped by Frances's direction in the same session. Nothing below is implemented yet except the `extract-testable-claims` skill itself (this PR).

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

### 2. One pointer comment per page

Instead of markup per claim, the page carries one short comment listing the IDs of its record-only claims:

```
{/* tested-claims: see TEST-MATRIX.md, ids ocr_ifm_embedded, ocr_ifm_page_range, ocr_ifm_array */}
```

The details live in the matrix and the evidence, not the page.

### 3. Evidence records

One committed JSON file per claim, `scripts/doc-detective/evidence/<page>/<id>.json`, with a schema in `schemas/`:

- the claim, quoted (not a line number, which drifts), its page, and its kind (from `extract-testable-claims/criteria.md`);
- each config that ran, the document, expected and actual values, and the extraction IDs;
- the environment (prod or dev, which account), the engine commit or date, and when it ran;
- the verdict (holds, contradicted, bug reported) and what changed on the page because of it;
- Frances's approval and date.

Fixture configs and PDFs go in `scripts/doc-detective/fixtures/` like today's fixtures, so the test can be recreated.

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

## Open questions

1. Today's evidence ran in Frances's personal account with `omit`. Record it as (a) what actually ran, documented as such, now, and (b) a rerun in the docs test account with `ocrIfMissing` after the deploy? Claude recommends (a) now, (b) after.
2. Pointer comment granularity: one per page (Frances's lean), or one per section when a page has many?
3. Should stale record-only evidence warn in CI, and after how long?
4. Build `contrast` and `schema` kinds now, or only the record-only path first?
5. Where the evidence schema lives: alongside `schemas/record.schema.json` as a new top-level schema, or as a record kind?
6. Does a contradicted claim get an evidence record (it documents why the page changed), or only claims that hold?
