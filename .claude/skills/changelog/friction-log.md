# Changelog Skill — Friction Log

Problems encountered during skill development and use, with suggested solutions. Add to this file whenever you hit a gap or awkward workflow moment.

---

## 1. Doc links missing from draft entries

**What happened:** July 2026 draft was reviewed and three UX improvement sections had no doc links. The style check (docs-checker) didn't catch it.

**Why it happened:** The docs-checker only scans for terminology violations — it has no step for structural completeness. The changelog skill's Step 4 mentioned `[text](doc:slug)` as a reminder but didn't enforce it.

**Solution implemented:**
- Added `structural-check.md` subskill that explicitly verifies doc links per section after drafting.
- Added an entry template to `structural-check.md` with a `For more information, see [topic](doc:slug)` placeholder — template is now used upfront in Step 4 so the slot is present from the start.
- Added `<!-- DOC LINK NEEDED -->` convention for sections where no public page exists yet.

**Remaining gap:** No public doc page exists for Reference Documents (bulk actions entry). When that page ships, the `<!-- DOC LINK NEEDED -->` comment in the draft should be replaced with the real link.

---

## 2. Image format not enforced

**What happened:** July 2026 draft used markdown `![alt](url)` image syntax. The style guide requires JSX `<Image>` syntax. Neither the docs-checker nor the skill flagged it.

**Why it happened:** The changelog style guide documents the correct format, but no automated or manual check step verified it before review.

**Solution implemented:** `structural-check.md` Step 2 now explicitly scans for markdown image syntax and flags it.

**Long-term suggestion:** When entry templates are promoted to `references/entry-templates/`, image stubs can be pre-formatted as `<Image>` in the template itself, preventing the error at source.

---

## 3. Categorization knowledge was session-only

**What happened:** PR categorization rules (document / investigate / skip) were derived from reading Frances's Slack threads during the session. They would have been lost at session end.

**Why it happened:** No persistent knowledge layer existed for this workflow — the patterns lived only in the examples, not as a distilled ruleset.

**Solution implemented:** Created `references/categorization-rules.md` with rules extracted from Frances's past inline comments. `fetch-release-prs.md` now reads this file before annotating each PR batch.

---

## 5. "Docs PR exists" is not a reliable signal for `document`

**What happened:** #3412 (verbosity levels 2 and 4) was annotated `document: clear user-facing feature` partly because docs PR #676 already existed. Frances's call: no docs — eng said it's an interim hack and not granular enough.

**Why it happened:** Categorization rules treat an in-progress docs PR as a positive signal for documenting. But a docs PR can be drafted before eng decides to keep the feature private or defer it. The docs PR existence reflects intent at draft time, not a cleared eng decision.

**Suggested rule addition:** A docs PR in flight counts as `investigate`, not `document`. Only treat it as `document` if Frances has already reviewed and approved the docs PR, or if it's merged.

---

## 6. Changes to privately-documented features are hard to detect from PR titles

**What happened:** #3388 (list: detect spreadsheet fallback) was annotated `investigate: List method behavior change`. Frances's call: it's a bug fix, and the underlying feature (detectSpreadsheet on List) is intentionally not publicly documented — so it's a skip regardless.

Similarly, #3402 (per-request OCR engine override) was annotated `investigate: likely document-worthy`. Frances's call: not a public API endpoint, no docs.

**Why it happened:** Both PRs touched user-facing methods or mentioned API-adjacent behavior, which looked like document candidates. But the underlying features they improved were never publicly shipped. The PR titles gave no hint of this.

**Suggested rule addition:** Add to categorization rules: if the PR touches a method or parameter that has no existing public docs page, default to `investigate` and fetch the PR body to look for signals like "not public API", "internal endpoint", or an undocumented parent feature. Don't assume user-facing = public.

---

## 7. Eng "not ready to publicize" is a distinct skip signal not in the rules

**What happened:** #3412 was skipped not because it's internal infra, but because eng considers the implementation an interim hack — same result shipped to users, but eng doesn't want it documented yet.

**Why it happened:** Categorization rules have `skip: infra` and `skip: named-customer-specific`, but no category for "user-facing but eng wants to defer public documentation." Frances's signal: "eng says it's still an ugly hack."

**Suggested rule addition:** Add to categorization rules: `investigate` (not `document`) when the PR title or body contains signals like "interim", "hack", "workaround", "not ready", or "step 1 of". These warrant confirmation with eng before documenting.

---

## 8. Mixed PRs need split dispositions, not one annotation

**What happened:** #3394 (priority extraction queue) was annotated `investigate: could be named-customer-specific or a tier feature`. Frances's call: the queue itself is internal (skip), but the new `uploaded`/`processing_started` timestamp fields added to the API response are document-worthy.

**Why it happened:** The annotation system applies one disposition per PR. When a PR has both an internal component and a user-facing API surface change, the single-annotation format buries the documentable part.

**Suggested improvement:** When annotating a PR with mixed internal/public scope, use `investigate (partial)` and note which specific part is potentially document-worthy — e.g., `investigate: queue is infra/skip, but API response adds uploaded/processing_started timestamps — check if those are public`.

---

## 4. Structural check is downstream of drafting

**Current state:** The entry template lives in `structural-check.md`, which is a post-draft verification subskill. This means a developer could draft without consulting the template.

**Suggested solution (not yet implemented):** Promote entry templates to a dedicated `references/entry-templates/` directory with one file per section type (`new-feature.md`, `improvement.md`, `ux-improvement.md`). Step 4 in SKILL.md would reference these directly as the drafting starting point, making structural correctness a precondition rather than an afterthought.
