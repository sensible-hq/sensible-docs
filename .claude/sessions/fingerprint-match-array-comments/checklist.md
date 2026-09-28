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

### "Matches passing" vs "tests passing": evidence

Conclusion: the unit of pass/fail is the **test**. "50% of tests" (fingerprint-mode.md:32) is the precise wording. "50% of all matches" (fingerprint.md:108) is loose wording, and taken literally it describes something the engine can't count.

1. **A match finds a line.** match.md:17: "Matches are search criteria for matching lines of text in a document." Each Match object resolves to a line or to nothing.
2. **A match array also resolves to one line or nothing.** match-arrays.md:18: "Sensible matches the last element in a Match array if" the elements target successive lines in order. The array returns the last element's line only if the whole chain succeeds. No partial result is exposed.
3. **Elements after the first depend on the line the previous element matched, so they can't be scored on their own.**
   - match.md:163: a `first` match "matches the first line encountered ... after the preceding matched line in a match array." Scored separately, a `first` element would match almost any line in the document. Counting it as a passing match would be meaningless.
   - match.md:42: `reverse` "searches for a match in lines that precede the previous match in the array." It has no meaning without the previous element's result.
4. **Repeat match shows the array is all-or-nothing.** match.md:299 and 331: `"type": "repeat", "times": 5` finds the 5th occurrence, and Sensible expands it into a 5-element match array. If array elements were scored individually, a document with only 3 occurrences would "pass 60%". But the Repeat match finds the 5th occurrence or nothing, so the expanded array must be pass/fail too.
5. **A test is a string, a Match object, or a match array** (fingerprint.md:33). By 1 and 2, each of those resolves to one line or nothing. So each test is binary, and the test is the smallest unit Sensible can score.
6. **The fingerprint docs already treat the test as the pass unit.** fingerprint.md:107: Sensible must find all the matches in the array on the same page "for the test to pass." Pass/fail is attached to the test, not to each match.
7. **Reconciling #3.** When every test is a single match, "matches" and "tests" count the same thing, so the loose wording in fingerprint.md:108 is harmless there. For match-array tests, only the test-level reading holds up, per 3 and 4. So fingerprint.md:108 should say "tests".

Consequences:
- The AVOID-example comment is correct. With two single-match tests, one passing test ("Name of Insured") is 50%, so the config passes. The PREFER example is one test that passes or fails as a whole, so a generic phrase alone can't pass it.
- Statement #1 ("all tests must pass") is still the outlier.

### To do
- [x] Match-array test counts as one pass/fail unit (confirmed by Frances; evidence above)
- [ ] Confirm with engineering that the standalone threshold is 50% of tests
- [ ] If confirmed, fix the comment at fingerprint.md:45 and json5-comments-reference.md:19, e.g. "by default, the config passes if 50% or more of tests match"
- [ ] Optional: reword fingerprint.md:108 from "matches" to "tests" so it matches fingerprint-mode.md
