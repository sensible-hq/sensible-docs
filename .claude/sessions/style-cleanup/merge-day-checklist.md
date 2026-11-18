# Merge day: style cleanup (2026-11-18)

For Frances. #808 (style system map) and #822 (registry, Vale rules, write-time gate, Jev judge, repo variables) are ready, mergeable, and passing CI. Work top to bottom; each step says what to check before moving on.

## Before merging

- [ ] **Create the rollback release.** The release was blocked in the Claude session, so it's yours:

  ```bash
  gh release create pre-style-cleanup-2026-11-17 -R sensible-hq/sensible-docs \
    --target "$(git -C ~/GitHub/sensible-docs rev-parse origin/v0)" --latest=false \
    --title "Before style cleanup (2026-11-17)" --notes "Snapshot of v0 before #808 and #822 merge."
  ```

  Check: the release page shows the tag on today's `v0`, and it isn't marked Latest.

- [ ] **Decide on the pre-write hook.** `vale_gate.py` checks an edit before it's written and denies it on a blocking rule. The `vale-setup` memory says Vale should be one after-write hook plus CI. Keep it (and update the memory), or delete the `PreToolUse` entry for `vale_gate.py` in `.claude/settings.json`. Recommended: keep. Context: `.claude/sessions/style-cleanup/decisions.md`, D-013.

- [ ] **Decide on false-positive questions for five Vale rules.** `AgainstPhrasing`, `Terminology`, `InternalTerms`, `Filler`, and `WordList` sometimes flag good text. Option a: give each a Jev judgment spec that uses the Vale rule as its detector, and make its write-time gate report-only. Option b: leave them as warnings. Recommended: a, as a follow-up PR after the merge.

- [ ] **Skim the guide resolutions** in #822's `.claude/style-guide/` diff. The one most worth a look: reference pages open in third person ("Extracts…"), with an exception for Extra Data (`style-guide-overview.md`, Voice and tone).

- [ ] **Review the Jev labels.** `style-rules/judgment/labels/` has 61 cases labeled by Claude. Fix any you disagree with, then run `python3 scripts/style/calibrate.py --write` (needs `TYPESAFE_API_KEY`) and commit the changed specs. Trust is provisional until then; it can wait until after the merge.

## Merge

- [ ] **Merge #808, point #822 at `v0`, merge #822.** Use merge commits, not squash: a squashed #808 leaves #822 with conflicts.

  ```bash
  gh pr merge 808 -R sensible-hq/sensible-docs --merge
  gh api -X PATCH repos/sensible-hq/sensible-docs/pulls/822 -f base=v0
  gh pr merge 822 -R sensible-hq/sensible-docs --merge
  ```

  (`gh pr edit --base` fails on gh 2.45, hence the API call.)

## After merging

- [ ] **Pull and check:**

  ```bash
  cd ~/GitHub/sensible-docs && git checkout v0 && git pull
  python3 scripts/style/check_registry.py      # 0 problems
  python3 scripts/style/test_rules.py          # 19 fixtures, 0 problems
  python3 -m pytest -q scripts/style/test      # 23 passed
  bash scripts/vale-doctor.sh                  # all checks pass
  ```

- [ ] **Start a new Claude session** in `~/GitHub/sensible-docs`, so the new hooks and environment variables load. `echo "$DOCS_REPO"` should print `sensible-hq/sensible-docs`.

- [ ] **Apply or reject the proposed memory edits** listed at the end of `.claude/sessions/style-cleanup/decisions.md`: eight memories become pointers to registry rules, and the duplicate `blog_post_template` memory goes.

## Test the skills in the private copy

The copy (`fscelliott/sensible-docs-private-test`, cloned at `~/GitHub/sensible-docs-private-test`) has the docs for these two engine PRs removed, and its variables point at itself. A sandbox guard blocks writes to `sensible-hq` repos.

- [ ] `cd ~/GitHub/sensible-docs-private-test && claude`, then `/update-docs-from-pr 3374` (JsonLogic Today operator). Compare the PR it opens in the copy with the original, sensible-hq/sensible-docs#642.
- [ ] Same for `/update-docs-from-pr 3351` (Region `asImage`). Compare with the `asImage` parts of sensible-hq/sensible-docs#637. Watch whether it adds Region back to the Image processing page.
- [ ] Don't run `close-docs-pr`'s label step or the changelog publish step from the copy. The guard blocks the label writes; nothing blocks readme.com publishing.
- [ ] Note what each run got wrong, as rows in the correction inventory (`design/style-system-map.md`, section 7), not in memory.

## Housekeeping

- [ ] Keep Claude transcripts for the baseline: add `"cleanupPeriodDays": 3650` to `~/.claude/settings.json`. They're deleted after 30 days by default.
- [ ] Export Toggl (detailed report CSV), then `python3 scripts/style_baseline/pr_metrics.py --since 2026-06-01 --toggl <file>`.
- [ ] Remove the worktrees once merged: `sensible-docs-style-map`, `sensible-docs-style-cleanup`, `sensible-docs-style-jev`, `sensible-docs-repo-vars`, `sensible-docs-remove-test-docs`.
- [ ] Pick fixes from the backlog in `.claude/sessions/style-cleanup/progress.md`: 56 `//` comments in JSON code blocks, a stale `Email extraction` entry in `docs/_order.yaml`, two integration pages missing from the sidebar order.
