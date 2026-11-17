# Style cleanup decisions

Each decision: what was decided, why, and how to reverse it. Numbered in order; never renumbered.

## D-001 Stack the branch on `style-map`

The cleanup builds on `design/style-system-map.md`, which is in PR #808 and not yet merged. The branch starts from `style-map`, and the PR targets `style-map`, so it shows only the cleanup diff. If #808 is squash-merged first, rebase this branch onto `v0` and retarget the PR.

## D-002 Working files live in `.claude/sessions/style-cleanup/`; plans live in `design/style-cleanup/`

Checklists go under `.claude/sessions/<session>/`, per the existing convention. The design and the implementation plan are reviewable artifacts like the map, so they sit beside it in `design/`.

## D-003 The registry lives in `style-rules/`, not in `.github/styles/Sensible/`

Vale loads every `.yml` file in a style directory as a rule, so a registry there would break Vale. `style-rules/` is neutral ground between `.claude/` (guides) and `.github/styles/` (Vale).

## D-004 No content in `docs/` or `reference/` changes

Fixing existing violations changes published pages and deserves review page by page. This PR reports them as a backlog with counts per rule.

## D-005 Claude memory isn't edited

Memory lives outside the repo, so a PR can't show the change. Proposed memory edits are listed at the end of this file.

## D-006 `.claude-session` points at this session

The file was committed on `v0` pointing at the `seo` session (`.claude/sessions/seo/checklist.md`). This branch points it at `style-cleanup`, per the worktree-session convention. On merge, `v0`'s copy changes too. Restore the old line on merge if that pointer still matters.

## D-007 `Sensible.WordList` keeps only what `Google.WordListCase` doesn't

50 of its 71 swaps were also in `Google.WordListCase`, so a word got two alerts. The duplicates are removed from `Sensible.WordList`. `Google.WordListCase` is vendored and stays as it is. The `application` swap (dead: the vocabulary accepts "application") and `touch: tap` (a mobile UI rule; Sensible docs use "touch" for geometry) went with them. `Google.WordListCase` still flags "touch" twice in `checkbox.md`; editing vendored Google rules is out of scope.

## D-008 `Sensible.EmDash` replaces `Google.EmDash`

Google's rule bans only spaced dashes, so its fix (`a—b`) still breaks the house rule. Turned off in `.vale.ini`. En dashes in ranges (1–3) are allowed.

## D-009 New rules start at warning; changelog structure rules are errors

New rules report on added lines in CI (vale-action's default) and don't fail the job. The two changelog rules are errors because they're unambiguous and run only on changelog drafts, which CI doesn't lint.

## D-010 Rules narrowed after the corpus run

- `LinkArticle`: one-word link text only. Multi-word text ("a [computed fields array to sections]") matched on the last word.
- `NoteBlockquote`: only blockquotes that start with Note, Tip, Important, or Warning. `getting-started-email.md` quotes an email body in a blockquote, which is right.
- `ParamNameCode`: dropped "object". Output keys such as `postprocessorOutput` are JSON keys, which the guide says to backtick.

## D-011 Vale behaviors that rule authors need to know

Found while testing; recorded in `style-rules/README.md`.

- An existence rule wraps each token in word boundaries. A token that starts or ends with a symbol (`![`, `<Image`, `^## `) never matches unless the rule sets `nonword: true`.
- `scope: raw` sees the Markdown source.
- Words in the accepted vocabulary suppress any match that contains them. "config" is accepted, so "SenseML config editor" couldn't be flagged until `Terminology` set `vocab: false`.
- When two `.vale.ini` sections match a file, the later one wins.

## D-012 Rules not built

- Fractions in words beyond thirds, tenths, and quarters: no corpus hits worth the noise.
- A `parse` rule: already in the vocabulary's reject list.
- Glossary terms that depend on context ("response", "segment", "section", "key", "empty"): judgment rule `sensible-context-terms`.
