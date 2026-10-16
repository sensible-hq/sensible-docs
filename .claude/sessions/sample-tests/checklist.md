# sample-tests

Session: fingerprint-match-array-comments (Claude Code session abbb26a9-022f-426d-b62a-97bc541c74e3). Worktree: /home/franc/GitHub/sensible-docs-sample-tests. Stacked on `docs-test-reports` (#756): merge #756 first.

Goal: test the inline fingerprint samples in fingerprint.md and portfolio.md, so the syntax claims are verified.

## Decisions (Frances, 2026-10-16)
- Placeholder samples (alternate wordings, AVOID / ALT ONE / ALT TWO): rewrite with real text so each sample runs as written.
- Standalone Wells Fargo example: syntax + pass/fail run in strict fingerprint mode, plus variants for the 50% rule.
- Getting started: no gate (rarely changes).

## Verified before writing (scratch doc types, deleted)
Phrases checked against Sensible's lines (`POST /extract_text_from_golden`), then run:
- Alternate wordings: first "U.S. Individual Income Tax Return"; last `any` of "Form 1040 (2020)" / "Form 1040 (2021)" → pages 1–2 (portfolio_bank_paystub_tax.pdf).
- AVOID: separate every tests "August 11, 2021" + "Page" (case-sensitive) → pages 2–7 (pulls in tax return p2). ALT ONE (flat) and ALT TWO (chained) → pages 3–7.
- Wells Fargo standalone (new `assets/pdfs/wells_fargo_checking.pdf` = portfolio pp. 3–7), strict mode: 3/3 runs; 2/3 runs; 1/3 → FAILED, errors [].
- Note: "Form 1040 (2020) Page 2" is not one line in Sensible's text ("Form 1040 (2020)" / "Page" / "2"), so fixture_fp_demo_any_alternate's second wording never matched.

## Work
- [ ] Docs: rewrite the 4 placeholder samples; example document links; markers on all 5 fingerprint samples + portfolio.md's 2.
- [ ] Markup: `inline config {"fragment": "fingerprint", "doc_type", "config"}`, several per test; `expect {"compare": "documents"}` from inline configs, expected documents from the inline output's `documents` when not given; `expect {"compare": "fingerprint", "passes", "variants": [{"break": [...], "passes"}]}`.
- [ ] Runner: temporary doc types (`docs_ci_tmp_*`), development environment, deleted after; strict mode for fingerprint compare.
- [ ] Records/schema, HTML/text/summary reports.
- [ ] Workflow for portfolio.md (gate + summary), fingerprint gate already covers fingerprint.md.
- [ ] Unit tests; live run of both pages.
- [ ] Follow-up (not in scope): the fixture_fp_demo_any_alternate / fixture_fp_portfolio_* fixtures are no longer needed.
