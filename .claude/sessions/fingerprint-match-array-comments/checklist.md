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

Three statements about how many tests must pass for a standalone document:

1. `fingerprint.md:45` (standalone example comment) and `json5-comments-reference.md:19`: "by default all tests must pass for the config to run"
2. `fingerprint-mode.md:32`: "A config passes if 50% or more of tests in a config match text in document."
3. `fingerprint.md:108` (Tips > test criteria): "Sensible must find 50% of all matches anywhere in the document by default"

### After a closer reading

**#2 vs #3 is probably just loose wording.**
- `fingerprint.md:33` defines the unit: "each test is a string, a Match object, or array of Match objects."
- `fingerprint.md:107`, the bullet just above #3, treats a match array as belonging to one test ("matches in the array ... for the test to pass").
- #3's portfolio half is worded the same loose way ("100% of all matches in all tests").
- So "50% of all matches" in #3 most likely means 50% of tests.
- What neither doc says: whether a match-array test counts as a single pass/fail unit in standalone scoring, or whether each match in it counts separately. The AVOID-example comment depends on the first reading.

**#1 is still a contradiction. It's most likely the wrong statement.**
- "By default" can't refer to a Fingerprint Mode setting. In the fingerprint-mode.md table, Normal and Strict both use the 50% rule ("Same"). The modes differ only in what happens when every config fails.
- `fingerprint.md:58`, just below the example, says the config "preferentially runs if the fingerprint finds the phrases." That reads like a soft score, which fits 50%, not "all tests."
- Likely source of the error: the portfolio rule (100% of tests, `fingerprint.md:108`) got copied into the standalone comment.

### To do
- [ ] Confirm with engineering that the standalone rule is 50% of tests, and that a match-array test counts as one unit
- [ ] If confirmed, fix the comment at fingerprint.md:45 and json5-comments-reference.md:19, e.g. "by default, the config passes if 50% or more of tests match"
- [ ] Optional: reword fingerprint.md:108 from "matches" to "tests" so it matches fingerprint-mode.md
