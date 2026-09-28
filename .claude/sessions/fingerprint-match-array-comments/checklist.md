# Session: fingerprint-match-array-comments
Session ID: abbb26a9-022f-426d-b62a-97bc541c74e3
Session directory: /home/franc/GitHub/sensible-docs

- [x] Add inline comments to `#### text matches` examples in fingerprint.md (match array behavior, portfolio same-page rule, match order, unwanted effect of avoid syntax)
- [x] Remove extra nested array brackets in the prefer example
- [x] Fix parse errors (missing commas after "page", trailing commas)
- [x] Open PR for review
- [ ] Optional: mention match order in the `#### test criteria` prose
- [ ] Verify "Name of Insured" follows "NARS" on the real form
- [x] Apply style guides; all example comments use `/* */`
- [x] Update style guides to require `/* */` for all comments (sentence-word-guidance.md, style-guide-overview.md, concept-topic-template.md)

## For review: conflicting pass rules for standalone fingerprints

The docs disagree on how many fingerprint tests must pass for a standalone document:

- [ ] **"All tests must pass":** the comment on `"tests"` in the standalone example, `docs/Senseml reference/config-settings/fingerprint.md:45`. The same wording is the canonical comment in `.claude/style-guide/json5-comments-reference.md:19`, so the json5-commenter skill copies it into every example it enriches.
- [ ] **"50% of tests":** `docs/Senseml reference/document-type-settings/fingerprint-mode.md:32` says "A config passes if 50% or more of tests in a config match text in document."
- [ ] **"50% of matches":** `fingerprint.md:108` (Tips > test criteria) says "Sensible must find 50% of all matches anywhere in the document by default." That counts *matches*, not *tests*.

Why it matters for this PR: the "unwanted effect" comment in the AVOID example (`fingerprint.md` ~line 147) relies on the 50%-of-**tests** rule. With that rule, two single-match tests let a document pass on "Name of Insured" alone, while one match-array test needs both phrases.
- If the rule is really 50% of **matches**, the PREFER example has the same weakness (1 of 2 matches = 50%), and the tip's justification fails for standalone documents.
- If the rule is really **all tests**, the AVOID example has no unwanted effect for standalone documents either.

To resolve:
- [ ] Confirm the actual rule with engineering: 50% of tests, 50% of matches, or all tests
- [ ] Fix whichever of fingerprint.md:45, fingerprint.md:108, fingerprint-mode.md:32 and json5-comments-reference.md:19 is wrong
- [ ] Re-check the AVOID-example comment against the confirmed rule
