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
- [x] Apply Frances's 4 PR review comments to the PREFER example comments (lines 160, 165, 166, 173)
- [x] Line 160: "passes or fails if" → "passes only if"
- [x] Replace the standalone example with a multi-test Wells Fargo example (match array, Match object, string), and update the intro and outro sentences
- [x] Cut "by default" from the 50% rule (not configurable, per Frances) in the example comment, json5-comments-reference.md:19, and the test criteria tip
- [x] Add a "Portfolio expansion" example after the standalone example: shows the `"page": "any"` expansion, explains the drawbacks (100% rule, match array must be on a single page so test 1 fails, `any` gives no boundaries), and recommends full portfolio syntax
- [ ] Review: "equivalent to" in the expansion intro. The exact internal expansion shape (Match object vs. single-element array) isn't documented, so the example is illustrative
- [ ] Check the real statement footer: `endsWith "page 2"` fails on "Page 2 of 6"-style footers
- [ ] Confirm the config and document type names in the new example intro ("wells_fargo_checking", "bank statements" are placeholders)
- [ ] Reply to / resolve the PR review comments on GitHub (not done; Frances to handle or ask)

## For review: conflicting pass rules for standalone fingerprints

Three statements about how many tests must pass for a standalone document:

1. `fingerprint.md:45` (standalone example comment) and `json5-comments-reference.md:19`: "by default all tests must pass for the config to run"
2. `fingerprint-mode.md:32`: "A config passes if 50% or more of tests in a config match text in document."
3. `fingerprint.md:108` (Tips > test criteria), original wording: "Sensible must find 50% of all matches anywhere in the document by default". **Now fixed** to "50% of tests must pass by default".

### After a closer reading

**#2 vs #3 is probably just loose wording.**
- `fingerprint.md:33` defines the unit: "each test is a string, a Match object, or array of Match objects."
- `fingerprint.md:107`, the bullet just above #3, treats a match array as belonging to one test ("matches in the array ... for the test to pass").
- #3's portfolio half is worded the same loose way ("100% of all matches in all tests").
- So "50% of all matches" in #3 most likely means 50% of tests.
- What neither doc says: whether a match-array test counts as a single pass/fail unit in standalone scoring, or whether each match in it counts separately. The AVOID-example comment depends on the first reading. **Resolved:** Frances confirmed a match array resolves to one line (pass/fail); see evidence below.

**#1 was wrong. Resolved:** Frances confirmed "all tests must pass" applies only to portfolios. Fixed in this PR.
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
5. **Boolean matches also resolve to one line or nothing.** match.md:202: `any` "finds a line that meets any of the match conditions", `all` "finds a line that meets all of the match conditions", and `not` "finds a line if it doesn't meet the match condition." Sub-matches are conditions on a single candidate line, not separate searches. So a Boolean match is one Match object that finds one line or nothing, and its sub-matches have no pass/fail of their own. (`not` on its own would match almost any line, the same problem as `first` in point 3.)
   - Difference from match arrays: `all` requires the conditions on the *same line*, while a match array requires successive lines in order (and, in portfolios, on the same page). `{"type":"all","matches":[NARS, Name of Insured]}` only passes if both phrases are on one line, so it isn't a substitute for the PREFER example.
6. **A test is a string, a Match object, or a match array** (fingerprint.md:33). By 1, 2 and 5, each of those resolves to one line or nothing. So each test is binary, and the test is the smallest unit Sensible can score.
7. **The fingerprint docs already treat the test as the pass unit.** fingerprint.md:107: Sensible must find all the matches in the array on the same page "for the test to pass." Pass/fail is attached to the test, not to each match.
8. **Reconciling #3.** When every test is a single match, "matches" and "tests" count the same thing, so the loose wording in fingerprint.md:108 is harmless there. For match-array tests, only the test-level reading holds up, per 3 and 4. So fingerprint.md:108 should say "tests".

Consequences:
- The AVOID-example comment is correct. With two single-match tests, one passing test ("Name of Insured") is 50%, so the config passes. The PREFER example is one test that passes or fails as a whole, so a generic phrase alone can't pass it.
- Statement #1 ("all tests must pass") was wrong for standalone documents and is now fixed.

### To do
- [x] Match-array test counts as one pass/fail unit (confirmed by Frances; evidence above)
- [x] Standalone threshold is 50% of tests; "all tests must pass" applies only to portfolios (confirmed by Frances)
- [x] Fix the standalone example comment in fingerprint.md and json5-comments-reference.md:19 to "array of tests; for standalone documents, the config passes if 50% or more of the tests pass"
- [ ] Same stale comment remains in drafts/blog-oocl-delivery-orders-20260622.md (lines 33, 269; untracked draft in main checkout, not in this PR)
- [x] Reword fingerprint.md:108 from "matches" to "tests" so it matches fingerprint-mode.md

## For review: the "fallbacks" tip may contradict the 100% portfolio rule

- fingerprint.md:112 (Tips > fallbacks) says to handle two revisions of a last page by writing two separate `last` tests, one per wording.
- fingerprint.md:108 says "100% of tests must pass for Sensible to segment a document in a portfolio."
- Taken together: a revision-1 document fails the revision-2 test, so the segment never passes.
- A single test with an `any` Boolean match (wording A or wording B) seems to be the correct fallback pattern.
- [ ] Confirm with engineering how separate same-page-type tests combine in portfolios, then fix the fallbacks tip or clarify the 100% rule

## To do: point readers to the fingerprint validation option in the Sensible app

- [ ] Add a pointer in fingerprint.md to the new option for validating fingerprints in the Sensible app. It's a new entry under the **Options** button in the SenseML editor.
  - Get the exact menu entry name and what it reports (pass/fail per test? matched lines? portfolio segments?) before writing
  - Decide where it goes. Candidates: the standalone Examples section, Tips > test criteria, or a Notes entry
  - Check whether an existing doc already covers the Options menu, and link to it
  - Screenshots go in screenshots/ and docs reference final/ (see image processing pipeline)

## To do: how Sensible treats portfolio syntax in a standalone document (Frances's TODO at fingerprint.md:35)

Frances's inline TODO: does this doc already explain how Sensible treats portfolio syntax in single-document files? Does it ignore `page` and just un-expand it, or turn it into page `any`? What happens to multi-page arrays? (Test?)

Where the page already partly answers this:
- fingerprint.md:27: "If you use a config for both portfolio and standalone versions of the same document, Sensible automatically converts between the two and uses the appropriate fingerprint." It doesn't say how.
- fingerprint.md:118 (Page parameter, Notes): "If you reuse the same config between portfolios and standalone documents, then for standalone document extractions, Sensible ignores the configured value of this parameter." That answers "ignores `page`", but not whether ignoring it amounts to un-expanding or to `any`. The two may behave the same, since in both cases any page can match.
- fingerprint.md:128 (Tips > test criteria): "In single-file documents, matches can occur anywhere in a document." This suggests the portfolio same-page rule for match arrays doesn't apply to standalone documents, so multi-page arrays would pass. But it's stated for standalone fingerprints in general, not specifically for portfolio syntax reused on a standalone document.

Still unknown, so test in the Sensible app:
- [ ] Portfolio-syntax fingerprint run on a standalone document: is `page` ignored for all page types (`first`, `last`, `every`), or do some still restrict which pages match?
- [ ] Match array that spans pages, in portfolio syntax, run on a standalone document: does the test pass?
- [ ] Does the pass threshold switch from 100% (portfolio) to 50% (standalone) when the config runs on a standalone document?
- [ ] Remove the inline TODO from fingerprint.md:35 before merging

## To do: are all Match object types supported in fingerprints? (e.g. Boolean matches)

- [x] Check the backend (sibling repo `sensible`) for whether fingerprint tests support every Match type: string (`equals`, `startsWith`, `endsWith`, `includes`), `regex`, `first`, Boolean (`any`, `all`, `not`), and `repeat`. Look at config validation/schema and the matcher code path fingerprints use.

**Result (Boolean support):** all Match types that anchors accept are supported, including Boolean. Evidence (sensible @ 242e382fd):
- Schema: `configuration.schema.json` `Fingerprint.tests` is an array of `AnchorMatch` or `FingerprintMatch`. `FingerprintMatch.match` is `AnchorMatch` or an array of them. `AnchorMatch` = string | Matcher | RepeatMatcher | array. `Matcher` variants: `equals/startsWith/includes/endsWith`, `regex`, `any`, `all`, `not`, `first`.
- Runtime: fingerprints call `findMatches` (anchor.ts:174), then `matchNext`, then `getMatchResult` (helpers.ts:169), which handles `any`/`all`/`not` first. It's the same code path as anchors.
- `repeat` is expanded by `standardizeMatch` (standardize.ts:151–155).
- NOT allowed in fingerprints: `page` and `firstInSection` matchers (they're `AnchorComponent`, not `AnchorMatch`).
- Caveat: no unit test covers Boolean matches in fingerprints (fingerprints.test.ts, multi-extract.test.ts).

## Backend findings: several beliefs in this PR are wrong (sensible @ 242e382fd)

### How Sensible standardizes a fingerprint (standardize.ts:27–57)
- **Simple (standalone) syntax** `tests: [T1, T2, T3]` becomes ONE test: `{page: "any", match: [std(T1), std(T2), std(T3)]}`. It is not three `any` tests.
- **Portfolio syntax** `{page, match: X}`: `(Array.isArray(X) ? X : [X]).map(standardizeMatch)`.
  - `"match": [A, B]` becomes `[[A], [B]]`: two **independent** matcher groups. This is NOT a match array.
  - `"match": [[A, B]]` becomes `[[A, B]]`: one chained match array.
  - The nested `[[...]]` in the original PREFER example was therefore meaningful. Removing it changed the semantics.

### Match order
- **Order matters inside a chained match array.** `matchArrayInner` (anchor.ts:250–299) reduces over the matchers. Each one searches from `prevMatch.lineIndex + 1` (anchor.ts:276), and `matchNext` only scans forward (anchor.ts:301–329).
- **Order doesn't matter between independent groups:** standalone tests, or the elements of a flat portfolio `"match": [A, B]`. Each group runs its own `findMatches` (fingerprints.ts:49).
- So Frances is right that order doesn't matter for the current PREFER example (flat `[NARS, Name of Insured]`). But it does matter for Wells Fargo test 1 (a nested array in simple syntax) and for `[[A, B]]` in portfolio syntax.

### Scoring
- **Standalone:** `filterConfigurationsOnFingerprints` (fingerprints.ts:97) flattens every test's matcher groups, ignores `page` and `offset`, searches the whole document, and passes if groups found / total groups ≥ 0.5 (fingerprints.ts:14, 57).
  - Portfolio-syntax config used standalone: `"match": [A, B]` counts as **2 groups**. So the flat PREFER example has the same "only 'Name of Insured' passes" weakness as the AVOID example. `[[A, B]]` counts as 1.
  - Answers the TODO at fingerprint.md:35: `page` is ignored, and multi-page chained arrays can pass (the search spans pages).
- **Portfolio:** `matchPages` (multi-extract.ts:258–290) evaluates **each test independently on each page**, with threshold 1 (line 274): every matcher group *in that test* must be found on that page. Each passing test emits its own first/last/every/any signal. A failing `every` test emits `every_failed`.
  - So "100% of tests must pass" is wrong. It's 100% of the matcher groups within a test, per page. My edit to fingerprint.md:108 ("matches" to "tests") made it less accurate. The original "100% of all matches in all tests" was closer.
  - The **fallbacks tip is correct**. Two separate `last` tests give two independent `last` signals, and either one ends the document. My concern was wrong.
  - AVOID vs PREFER in a portfolio with `every`: two one-group tests and one test with two flat groups behave the same (both groups required on every page).

### Needs fixing in this PR
- [ ] fingerprint.md:108: revert or reword. Within a test, all matcher groups must be found on the same page. Tests are independent signals.
- [ ] PREFER example: decide flat `[A, B]` (unordered AND on one page; 2 groups in standalone) vs nested `[[A, B]]` (ordered chain; 1 group in standalone). Fix the comments to match. The current "must find in order" / "succeeds the line containing NARS" comments are wrong for the flat version.
- [ ] AVOID example "unwanted effect" comment (if restored): only true relative to the nested PREFER form.
- [ ] Portfolio expansion example: wrong shape. The real expansion is one `any` test whose match holds three groups, all required on one page. Update the code and the "100% of tests" comment.
- [ ] fingerprint.md table (`match` "array of Match objects") and match-arrays.md: document that in portfolio syntax, a flat array = independent groups and a nested array = chained match array.
- [ ] Remove the inline TODO at fingerprint.md:35 (answered above).
