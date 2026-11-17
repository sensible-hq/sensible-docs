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
