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

## D-013 One hook script for two events, replacing `vale-check.sh`

The `vale-setup` memory records Vale as one `PostToolUse` hook plus CI, with no new integrations. `vale_gate.py` keeps one script and one Vale config, but it adds a `PreToolUse` entry, because checking text before it lands is the point of write-time enforcement. The pre-write gate denies only on rules with `gate: block` in the registry (em dashes, Latin abbreviations, model names, UI names, draft links, code fences), and lets an edit through after 3 denials on one file. To go back to the old shape, delete the `PreToolUse` entry in `.claude/settings.json`; the `PostToolUse` half still works alone. Frances chose to keep it on 2026-11-18, and the `vale-setup` memory now describes this shape.

## D-014 The registry check runs in the existing pytest workflow

`test-scripts.yml` gains `scripts/style/test`, and its path filter gains the guides, skills, preferences, Vale styles, and `style-rules/`. A PR that edits a rule's guide text without updating the registry now fails. This adds no Vale runner: the Vale-dependent tests skip in CI, where Vale isn't installed.

## D-015 The after-write report compares with the last commit

`PostToolUse` doesn't get the file's previous text, so "changed lines" means lines that differ from `HEAD`. Over a session that includes earlier uncommitted edits, which is still the agent's own work. The pre-write gate compares with the file as it is before the edit, so it sees only the new text.

## D-016 Markers inside fenced code don't count

`style-rules/README.md` shows a marker in an example code block, and the checker flagged it as an unregistered link. Markers inside fences are examples, so the checker skips fenced code.

## D-017 The PR doesn't merge `v0`

The branch is stacked on `style-map`. Merging `v0` here would add unrelated `v0` commits to the PR's diff against `style-map`. Sync with `v0` when #808 merges and this branch is rebased.

## Proposed memory edits (not applied; see D-005)

If this PR merges, these memories should shrink to pointers, so the rule lives in the repo and memory points at it:

| memory | change |
| ------ | ------ |
| `feedback_you_centric_style` | Replace "revise-doc-style's default is wrong" with: the boundary is in `writing-rules.md` (Explicit subjects); registry rule `sensible-explicit-actor`. |
| `feedback_block_comments_only` | Remove the stale claim that `sentence-word-guidance.md` prescribes `//`. Point at registry rule `sensible-code-fences`, which the hook now blocks. |
| `feedback_keep_code_fence_language` | Point at `sensible-code-fences`; the guides now state it, and the hook blocks `json5` fences. |
| `feedback_excerpt_rules` | Point at `style-guide-overview.md` (Frontmatter) and `scripts/style/check_excerpts.py`. |
| `feedback_anthropic_model_naming`, `project_label_method_near_deprecated` | Point at `sensible-model-names` (blocked by the hook) and `sensible-label-method`. |
| `feedback_full_style_pass` | Shrink: the hook and CI enforce the deterministic rules. Keep "copy sibling wording", now `sensible-copy-sibling-wording`. |
| `project_vale_setup` | Done 2026-11-18. |
| `blog_post_template` | Delete: it duplicates `.claude/style-guide/blog-post-template.md`. |

## D-018 Jev decides the Vale rules that also match correct text

Frances's call (2026-11-18), implemented in this PR. `AgainstPhrasing`, `Terminology`, `InternalTerms`, `Filler`, and the word lists (`Sensible.WordList`, `Google.WordListCase`) are now `kind: judgment` with `gate: judge`: Vale finds candidates, Jev answers a choice question per hit, and the after-write hook lists these hits apart as possibly fine. Each has 8 labeled cases (3 to 5 violations).

The first calibration trusted three of the five. `Terminology` (recall 0.20) didn't know which terms the glossary avoids, and `WordList` (precision 0.83) didn't know that "above" in Sensible docs usually means position on the page. Both questions now carry that context, and both reached precision and recall of 1.00. That revision came after seeing the results on the same 16 cases, so these two rules' numbers are optimistic until Frances's own labels confirm them.
