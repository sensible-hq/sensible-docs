# sample-tests

Session: fingerprint-match-array-comments (Claude Code session abbb26a9-022f-426d-b62a-97bc541c74e3). Worktree: /home/franc/GitHub/sensible-docs-sample-tests. Stacked on `docs-test-reports` (#756): merge #756 first.

Goal: test the inline fingerprint samples in fingerprint.md and portfolio.md, so the syntax claims are verified.

## Decisions (Frances, 2026-10-16)
- Placeholder samples (alternate wordings, AVOID / ALT ONE / ALT TWO): rewrite with real text so each sample runs as written.
- Standalone Wells Fargo example: syntax + pass/fail run in strict fingerprint mode, plus variants for the 50% rule.
- Getting started: no gate (rarely changes).

## Verified before writing (scratch doc types, deleted)
Phrases checked against Sensible's lines (`POST /extract_text_from_golden`), then run:
- Alternate wordings: first "U.S. Individual Income Tax Return"; last `any` of "Preparer's name" (straight apostrophe, as in the document) / "Preparer’s name" (curly, as OCR can read it) → pages 1–2 (portfolio_bank_paystub_tax.pdf). Rewritten 2026-10-19 (Frances): the first version used the form's revision years (2020 / 2021), but separate revisions belong in separate configs, so the sample is now one phrase in two OCR forms.
- AVOID / ALT ONE / ALT TWO (rewritten 2026-10-19, Frances: the date was a poor fingerprint; use phrases about the content). No phrase about the content is on every statement page (only the date and "Page N of 7"), so the samples use first + last tests instead of every: first "Wells Fargo" (distinctive) and "Account" (generic, case-sensitive: also on tax return p2, "Account number" in the refund section); last "Minimum daily balance" (statement p7 only). AVOID → [2,2] and [3,7] (tax return p2 becomes a separate bank statement); ALT ONE (flat) and ALT TWO (chained: "Account options" is 21 lines after "Wells Fargo" on p3) → [3,7].
- Wells Fargo standalone (new `assets/pdfs/wells_fargo_checking.pdf` = portfolio pp. 3–7), strict mode: 3/3 runs; 2/3 runs; 1/3 → FAILED, errors [].
- Note: "Form 1040 (2020) Page 2" is not one line in Sensible's text ("Form 1040 (2020)" / "Page" / "2"), so fixture_fp_demo_any_alternate's second wording never matched.

## Work
- [x] Docs: rewrite the 4 placeholder samples; example document links; markers on all 5 fingerprint samples + portfolio.md's 2.
- [x] Markup: `inline config {"fragment": "fingerprint", "doc_type", "config"}`, several per test; `expect {"compare": "documents"}` from inline configs, expected documents from the inline output's `documents` when not given; `expect {"compare": "fingerprint", "passes", "variants": [{"break": [...], "passes"}]}`.
- [x] Runner: temporary doc types (`docs_ci_tmp_*`), development environment, deleted after; strict mode for fingerprint compare.
- [x] Records/schema, HTML/text/summary reports.
- [x] Workflow for portfolio.md (gate + summary), fingerprint gate already covers fingerprint.md.
- [x] Unit tests; live run of both pages.
- [ ] Follow-up (Frances, 2026-10-16): evaluate using Jev for the envelope tests (cheaper).
- [ ] Follow-up (not in scope): the fixture_fp_demo_any_alternate / fixture_fp_portfolio_* fixtures are no longer needed.

## Results (2026-10-16)
- Unit tests: 158 pass (new test_samples.py; gate test for prose above a sample).
- Live: fingerprint.md 10/10 (the Wells Fargo PDF via the branch URL until merge), portfolio.md 1/1. No docs_ci_tmp_* doc types left behind.
- Vale: no new alerts on changed lines (fixed one Quotes, one Parens).
- [ ] After #756 and this merge: the first v0 runs of doc-tests-fingerprint (12 extractions) and doc-tests-portfolio (1) pass.
