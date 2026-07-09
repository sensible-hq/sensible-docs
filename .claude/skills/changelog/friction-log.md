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

## 4. Structural check is downstream of drafting

**Current state:** The entry template lives in `structural-check.md`, which is a post-draft verification subskill. This means a developer could draft without consulting the template.

**Suggested solution (not yet implemented):** Promote entry templates to a dedicated `references/entry-templates/` directory with one file per section type (`new-feature.md`, `improvement.md`, `ux-improvement.md`). Step 4 in SKILL.md would reference these directly as the drafting starting point, making structural correctness a precondition rather than an afterthought.
