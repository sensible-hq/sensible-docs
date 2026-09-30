# Session: fingerprint-match-array-comments
Claude Code session name: fingerprint-match-array-comments
Claude Code session ID: abbb26a9-022f-426d-b62a-97bc541c74e3
Session directory: /home/franc/GitHub/sensible-docs
Worktree: /home/franc/GitHub/sensible-docs-fingerprint-match-array-comments (branch `fingerprint-match-array-comments`)
PR: https://github.com/sensible-hq/sensible-docs/pull/727
Resume: `cd /home/franc/GitHub/sensible-docs && claude --resume abbb26a9-022f-426d-b62a-97bc541c74e3`

## RESUME HERE (paused 2026-09-29)

State when paused:
- Branch is in sync with origin at Frances's commit 85ed43dfd. Frances is mid-rewrite of fingerprint.md: new structure (Standalone / Portfolios / Fingerprint scoring / Notes > Tips) with inline TODO and LEFT OFF markers (listed below).
- Backend facts are verified against the `sensible` repo @ 242e382fd (see "Backend findings" below). Use them as ground truth over the older doc-based reasoning in this file.
- Pending, not yet in the file: Claude's corrected "nested vs flat array" summary comment (in the last conversation turn). Its key correction: a **flat** array does NOT require separate lines; elements are searched independently and can match the same line. Frances hasn't said where it goes. It likely fills `/* flat array: TODO LEFT OFF */` (~line 219) and/or `/* further nested array behavior LEFT OFF */` (~line 256).
- **Open disagreement** (see "OPEN DISAGREEMENT" near the end): whether portfolio tests pass/fail as a unit. Resolve it with the validator test described there before changing test/match terminology.
- Next steps: (1) work through the inline TODOs below, (2) reorganize the Notes/Tips, (3) re-verify every claim against the Backend findings.

## To do: inline TODOs in fingerprint.md (as of 85ed43dfd)

Line numbers are approximate. Search for `TODO` / `LEFT OFF`.

- [ ] **~41, `tests` parameter row, LEFT OFF:** the description cell has the moved "Portfolio fingerprints differ..." text, plus a TODO to side-note that scoring isn't by test but by match (except chained match arrays).
  - Backend: standalone scoring counts **matcher groups**. A simple-syntax test = 1 group. A nested `[[ ]]` = 1 group. Each element of a flat portfolio `match: [ ]` = its own group (fingerprints.ts:57, 97; standardize.ts:43). So "by match, except chained arrays" is right.
  - Also in that cell: "100% of tests must pass for Sensible to segment a document in a portfolio" is **wrong** per backend. Each test is an independent per-page signal. Within one test, all groups must be found on the page (multi-extract.ts:274).
- [ ] **~56, standalone example:** `[[ // TODO: talk single vs flat array and make this a better example (see config library?)`. Uses `//`, and the rule is `/* */` only. Look in sensible-configuration-library for a real example.
- [ ] **~86:** "TODO: add a screenshot of how that evaluates??" (standalone example). Probably a validator screenshot, via screenshots/ to final/.
- [ ] **~136:** "TODO: add to that example how it evaluates?" (the portfolio.md example link)
- [ ] **~142, `## Fingerprint scoring`:** "TODO: fill in and make it so it could be a standalone concept topic". Source material: Backend findings > Scoring, plus the flat vs nested section.
- [ ] **~158, fallbacks tip:** "TODO: verify if this can actually be done?" Backend says **yes**. Separate `last` tests emit independent `last` signals, and either one ends the document (multi-extract.ts:258–290, 356). Could still confirm in the app.
- [ ] **~170, test and verify fingerprints:** "Sensible automatically converts them TODO link". Needs the link to the validator docs (see "point readers to the fingerprint validation option" below). Typo: "If your write" should be "If you write".
- [ ] **~176, "Prefer nested match arrays for stricter syntax":** TODO asks whether this is portfolio-specific, or whether to split into (a) nested match arrays and (b) combining page tests into arrays for portfolios.
  - Backend: **not portfolio-specific.** Nested vs flat changes ordering in both modes, and changes scoring in standalone (1 group vs N). In portfolios, the count doesn't change pass/fail. Suggests splitting as the TODO proposes. Typo: "doesn'tneed".
- [ ] **~219, PREFER/flat example:** `/* flat array: TODO LEFT OFF */`
- [ ] **~253–254, nested comment:** says a flat array scores NARS and Name of Insured "as separate matches appearing in separate lines". **Wrong.** Flat elements can match the same line.
- [ ] **~256:** `/* further nested array behavior LEFT OFF: ...`
- [ ] **~276:** "TODO add a screenshot of the different behaviors for each of these from the validator!"

## To do: reorganize the Notes/Tips section

- [ ] Frances doesn't like the "grab-bag" nature of the notes. Reorganize them.
  - Current structure (85ed43dfd): `## Notes` > `### Fingerprint strictness`, `### Tips for authoring fingerprints` > `#### fallbacks`, `#### Turn off preprocessors`, `#### Standalone-specific tips`, `#### Portfolio-specific tips`.
  - Possible grouping: (1) how fingerprints are scored (move to `## Fingerprint scoring`), (2) choosing match syntax (flat vs nested, CSE guidance), (3) authoring workflow (turn off preprocessors, validate in the app), (4) portfolio page types and fallbacks. Fingerprint strictness links to fingerprint-mode.md.

## History / completed work

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
- [x] (Chose nested; restored `[[ ]]`, reindented, and added an inline comment explaining the nesting) PREFER example: decide flat `[A, B]` (unordered AND on one page; 2 groups in standalone) vs nested `[[A, B]]` (ordered chain; 1 group in standalone). Fix the comments to match. The current "must find in order" / "succeeds the line containing NARS" comments are wrong for the flat version.
- [ ] AVOID example "unwanted effect" comment (if restored): only true relative to the nested PREFER form.
- [ ] Portfolio expansion example: wrong shape. The real expansion is one `any` test whose match holds three groups, all required on one page. Update the code and the "100% of tests" comment.
- [ ] fingerprint.md table (`match` "array of Match objects") and match-arrays.md: document that in portfolio syntax, a flat array = independent groups and a nested array = chained match array.
- [ ] Remove the inline TODO at fingerprint.md:35 (answered above).

## To do: document flat `[ ]` vs nested `[[ ]]` in portfolio-syntax fingerprint tests

The docs never explain this, and they call a flat portfolio `match` array a "match array" (fingerprint.md:33, :116, test criteria tip; portfolio.md:227–228). The docs need to explain:

- [ ] **Order.** For order to matter, use `"match": [[A, B]]`. This is a real match array: Sensible must find A, then B on a later line (anchor.ts:250–299). If order shouldn't matter, use `"match": [A, B]`. Sensible searches for A and B independently (standardize.ts:43 turns it into `[[A], [B]]`).
- [ ] **How many units it counts as.** The syntax also sets how many units Sensible scores:
  - `[[A, B]]` counts as **1** unit. It passes or fails as a whole.
  - `[A, B]` counts as **2** units, scored individually.
  - Where this matters: when Sensible runs a portfolio-syntax config on a **standalone** document, it flattens all the units and passes the config if 50% or more are found (fingerprints.ts:57, 97). So `[A, B]` passes on A alone, and `[[A, B]]` doesn't.
  - Where it doesn't: in a **portfolio**, every unit in a test must be found on the page (threshold 1, multi-extract.ts:274), so 1 vs 2 units makes no difference to pass/fail. Only order and same-page matter there.
- [ ] Both forms require all units on the same page in a portfolio.
- [ ] Where to document it: the fingerprint.md `match` parameter row (add "array of Match arrays"), the test criteria tip, match-arrays.md, and the portfolio.md comment that calls a flat array a "match array"
- [ ] Rework the AVOID/PREFER tip around this. Its original point (group the phrases so they pass or fail together) only holds with `[[ ]]`.

## To do: guidance on when to use nested `[[ ]]` vs flat `[ ]` (from the CSE team)

Raw input from CSE, verbatim. Generalize and shorten before publishing. **Don't name the customer in public docs.**

> almost always use [[ ]] if it's for a first/last portfolio fingerprint.
>
> And doc type size is another huge factor. A customer like Vividly has a doc type with 1,000+ configs and many of them are for the same distributors with different layouts, so using a sequence of 3-4 lines tends to heavily derisk overlap.
>
> One other situation worth calling is I'd say it's better to use [[ ]] for customers with a strict fingerprinting setup. Usually they're looking to avoid being billed for docs that we haven't configured yet, so I tend to use more restrictive fingerprints, and looking for a sequence of lines probably our best tool for that

- [ ] Draft generalized guidance. Candidate points:
  - Use `[[ ]]` for `first` and `last` portfolio tests.
  - Use `[[ ]]` (a sequence of 3–4 lines) when a document type has many configs with similar layouts, for example many layouts from the same vendor. It reduces overlap between configs.
  - Use `[[ ]]` with strict Fingerprint Mode, where the goal is to avoid extracting (and being billed for) documents you haven't configured yet.
- [ ] Decide where it goes: Tips > text matches (alongside AVOID/PREFER), or a new tip. Cross-link from fingerprint-mode.md for the strict-mode point.
- [ ] Check whether billing belongs in a SenseML reference page, or should be phrased as "avoid extracting documents you haven't configured."

## Pending text: corrected nested vs flat summary comment (not yet placed in fingerprint.md)

Frances drafted this, and Claude corrected it. Placement TBD (likely ~line 219 or ~256).

```
/* A nested array ("match": [[ ]]) enforces stricter criteria than a flat array. In a nested array, or "chained matches",
   each element matches a separate line, and Sensible must find all the lines in the document in the same order as in the array.
   In a flat array ("match": [ ]), Sensible searches for each element independently, so the lines can occur in any order
   in the document, and more than one element can match the same line.
   For either array syntax, criteria are stricter in portfolios. In a portfolio, all the lines in the array must co-occur
   on a single page. In a standalone document, the lines can occur across multiple pages.
   Array syntax also affects fingerprint scoring. Sensible scores a nested array as one match that either succeeds or fails.
   For example, if Sensible finds 3 out of 5 elements, it scores the array as 0 out of 1 matches.
   Sensible scores each element in a flat array independently. For example, if Sensible finds 3 out of 5 elements,
   it scores the array as 3 out of 5 matches. In a portfolio, Sensible must find every element in either syntax,
   so scoring affects standalone documents only. */
```

## To do: "test" vs "match" terminology

Frances's proposal: there's no such thing as a test that passes or fails. A fingerprint is an array of matches, and each match passes or fails (a nested match array is one unit). So drop "test" terminology and refer to "matches".

What the backend says:
- **Standalone: Frances is right.** Sensible flattens every test into a list of match units and scores units found / total ≥ 0.5 (fingerprints.ts:57, 97). A unit is a string, a Match object, or a nested match array. It's also each element of a flat portfolio-syntax `match: [ ]`. Nothing is scored at the "test" level.
- **Portfolio: tests are real.** `matchPages` (multi-extract.ts:258–290) evaluates **each test** on each page. The test passes on that page if all its match units are found there (threshold 1, line 274). A passing test emits a first/last/every/any signal. A failing `every` test emits `every_failed`. That's pass/fail at the test level, and page types and offset only exist on tests.
- `tests` is also the literal config key, so the word can't disappear entirely.

Proposal:
- [ ] Keep "test" as the name of a `tests` array element (the config structure).
- [ ] Standalone sections: describe scoring in terms of matches ("the config passes if Sensible finds 50% or more of the matches"), and note that a nested match array counts as one match.
- [ ] Portfolio sections: keep test-level pass/fail ("a test passes on a page if Sensible finds all its matches on that page"), because page types attach to tests.
- [ ] Sweep fingerprint.md, fingerprint-mode.md:32 ("50% or more of tests"), json5-comments-reference.md:19, and the example comments for "test passes/fails" wording, and apply the rule above.

## OPEN DISAGREEMENT: is there a test-level pass/fail in portfolios?

**Frances's position:** even in portfolios, Sensible scores each match in a test separately, and each MATCH must pass. There's no pass/fail for tests as such. Maybe talk about "pages" instead.

**Claude's position (full rationale):**

The code groups the "every match must pass" check by test, not across the whole fingerprint. From `multi-extract.ts:258–290` (sensible @ 242e382fd):

```ts
for (const fingerprint of fingerprints) {          // each test
  if (fingerprintMatch(cleanText, fingerprint.match, /* this page only */, 1)?.passed) {
    pageMatches[pageNumber].push({ ..., type: fingerprint.page });   // label the page
  } else if (fingerprint.page === "every") {
    pageMatches[pageNumber].push({ ..., type: "every_failed" });
  }
}
```

- **Matches are scored separately, but only within one test.** `fingerprintMatch` searches for each match in `fingerprint.match` on its own, and with a threshold of `1` all of them must be found on the page. Frances is right about that part.
- **The result is one pass/fail per test.** `.passed` is a single yes or no for that test's matches, and it decides whether that test's `page` label goes on the page. Other tests' matches aren't part of that decision.

**Frances's model breaks on fallbacks.** Take two `last` tests, one matching wording X and one matching wording Y:
- **Frances's model:** every match must pass, so the page needs both X and Y, and a revision-1 page with only X is never marked as a last page.
- **The code:** test A passes on X alone and marks the page as a last page, and test B failing doesn't undo that.

This is why the fallbacks tip works. It only works because the test is where "all matches must pass" stops.

**"Pages" is a good way to phrase it, as long as it still names the test.** For example: "For each page, Sensible checks each test. If Sensible finds all of a test's matches on that page, it labels the page with the test's page type (`first`, `last`, `every` or `any`)." That avoids "a test passes" and fits the fact that the output is page labels. Dropping the test as the grouping would make the fallbacks tip wrong.

**To resolve:**
- [ ] Settle it empirically in the app's fingerprint validator: a portfolio config with two `last` tests (wording X and wording Y), run on a portfolio whose last page has only X. If that page is labeled `last`, the test is the grouping boundary (Claude's position). If it isn't, Frances's position holds.
- [ ] Optionally, confirm with engineering
- [ ] Then finalize the "test vs match terminology" item above

## To do: mirror key tips as inline comments in the code examples

Frances wants several of the Notes/Tips repeated as inline comments in the examples, where readers will see them while copying code. Use `/* */` only, and `json` fences only.

- [ ] **Turn off preprocessors** (Notes > Tips > Turn off preprocessors): add a commented-out `"preprocessors"` block to an example, with a comment such as `/* Sensible runs fingerprints before preprocessors. Comment out preprocessors while you author fingerprints, so the editor shows the lines exactly as the fingerprint sees them */`.
- [ ] Candidates for the other tips (decide which ones earn an inline comment):
  - **fallbacks:** in a portfolio example, two `last` tests with alternate wordings, with a comment that either one can label the page as a last page. Depends on the OPEN DISAGREEMENT above being settled.
  - **Nested vs flat match arrays:** already partly in the PREFER example comments. Reuse the pending corrected summary text.
  - **Test and verify fingerprints:** a comment that points to the validator entry under the SenseML editor's Options button.
  - **Fingerprint strictness:** a comment in the standalone example noting that strict Fingerprint Mode returns an error when no config passes (fingerprint-mode.md).
- [ ] Keep each prose tip too. The inline comment is a pointer, not a replacement. Or decide to cut the prose version if the comment says it all. This ties in with the Notes reorganization item above.
