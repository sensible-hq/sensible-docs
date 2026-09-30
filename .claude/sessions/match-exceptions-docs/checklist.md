# match-exceptions-docs checklist

Claude Code session name: match-exceptions-docs
Claude Code session ID: 9bb92619-2b00-442e-9dc7-828734bf1dc3
Goal: document once (match.md) that match parameters accept string, object, or array; elsewhere only note EXCEPTIONS.
Source of truth: sensible-hq/sensible origin/main src/engine/types.ts (AnchorMatch = string | Matcher | RepeatMatcher | array) + standardizeMatch() in src/engine/configurations/standardize.ts

## Convention (decided 2026-09-30)
In param tables, "[Match object](doc:match)" implies string, object, or array. Only note when a param DOESN'T support all three.
- AnchorMatch rows: replace "Match object or array of Match objects" / "string, Match object, or array..." with "[Match object](doc:match)"
- Exception rows: keep "Match object" AND add an explicit note (e.g., "Doesn't support strings or arrays.")

## Done
- [x] Add string/object/array table to top of match.md

## Accept string/object/array (AnchorMatch) — simplify value column
- [x] cell-rows.md:31 stop
- [x] layout-based-methods/document-range.md:34 stop
- [x] layout-based-methods/regex.md:30 stop
- [x] layout-based-methods/fixed-table.md:34 stop
- [x] layout-based-methods/text-table.md:39 stop (also number, {"type": "last"})
- [x] deprecated-features/deprecated-table.md:36 stop
- [ ] field-query-object/index.md:70 anchor — Anchor, not a match param; leave?
- [x] field-query-object/anchor.md:64-65 match, start
- [ ] field-query-object/anchor.md: check `end` row
- [x] sections/index.md:60 stop
- [ ] sections/index.md:59 anchor — Anchor, not a match param; leave?
- [x] preprocessors: ocr-preprocessor.md:30, remove-header.md:29, remove-footer.md:31, split-lines.md:27, rotate-page.md:25, linearize.md:36, remove-page.md:22, remove-lines.md:22
- [ ] preprocessors: scale.md:28 (samples[].match), deskew.md:30 (fixedPoints[].match) — nested, check wording
- [x] config-settings/fingerprint.md:97, draft-fingerprint.md:64 match

Out of scope: string-only params (wordFilters, terms, stopTerms, text, pattern).

Exception note wording (user, 2026-09-30): "limited support for [Match](doc:match) object (doesn't support Match arrays or strings as values)". Link style: [Match](doc:match) object, never [Match object](doc:match), in value cells.
lineFilters/lineSelection: "array of [Match](doc:match) objects (doesn't support strings or single Match objects as values)" — engine uses .some(), i.e. any-of, not a match array.

## Exceptions — keep explicit
- [x] layout-based-methods/label.md:30 stop: `first`, `gap`, or a single Match object (no string, no array)
- [ ] layout-based-methods/column.md stop: single Match object — PR #729 currently says "[Match object](doc:match)", which now implies all 3; needs exception note
- [x] match.md:208 any/all `matches`: array of Match objects only
- [x] match.md:209 not `match`: single Match object only
- [x] match.md repeat `match`: Match object or array, no string (check line ~305)
- [x] VERIFY: method.md:36 lineFilters says "Match object" — code type is Matcher[] (array only)
- [x] VERIFY: sections/index.md:71 lineFilters says object or array — code type is Matcher[]; also vertical sections lineSelection is Matcher[]

## Follow-ups
- [ ] sections/index.md:157 example passes lineFilters as a single object; schema requires array (sections.ts concat() may tolerate it at runtime)
- [ ] config-settings/fingerprint.md:35 prose still lists "a string, a Match object, or array"

## Wrap-up
- [ ] Vale + glossary check on every changed file
- [ ] Review and merge PR
- [ ] After merge: remove worktree ~/GitHub/sensible-docs-match-exceptions, delete branch, remove from additionalDirectories, pull v0
