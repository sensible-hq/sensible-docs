# Revision classification: design

Stacked on the docs PR metrics. `scripts/docs_pr_metrics/classify.py` answers the question the metrics can't: of the revisions after the AI draft, how many corrected a fact and how many were copy edits?

## Unit

A revision is one diff hunk on a doc file in a commit after the AI draft, as `metrics.py` defines the draft. The commit's author doesn't matter: a copy edit Frances dictates to Claude counts the same as one she types.

A hunk is one contiguous block of changed lines in a diff: the lines an edit removed and the lines it put in their place. Unchanged lines mark where one hunk ends and the next begins, so a commit that fixes three separate sentences on a page is three hunks. The unit is the hunk rather than the commit because one commit often mixes kinds of edit, such as a factual fix and a rewording, and a single label per commit would blur them.

Only committed changes are classified. Session back-and-forth before Claude's first commit, history replaced by a force-push, and feedback that changed nothing never reach a hunk. `design.md`, "What counts as a revision", has the full list.

A hunk's size in lines is its removed lines plus its added lines, the same convention `git diff --numstat` uses. A one-line rewording is 2 lines.

## Who decides what

Code settles what it can see, and Jev answers only the judgments that need language. Code then maps Jev's answers to a class through a truth table.

| Class | Decided by | Rule |
|---|---|---|
| addition | code | The hunk removes nothing. |
| deletion | code | The hunk adds nothing. |
| formatting | code | The two sides differ only in markdown marks and whitespace, or only in a code block's language label. |
| typo | code | At most 2 characters inserted or deleted, none replaced, and no digit in or beside them. A replacement stays with Jev, because one character can flip a value: ✅ to ❌, "2.5" to "3.1", "min" to "max". |
| factual | Jev | `contradicts` ≥ 0.7. |
| copy edit | Jev | `same_meaning` ≥ 0.7, without a factual yes. |
| elaboration | Jev | `adds_information` ≥ 0.7 and `drops_information` ≤ 0.3. |
| deletion | Jev | `drops_information` ≥ 0.7 and `adds_information` ≤ 0.3. |
| rewrite | Jev | `adds_information` and `drops_information` both ≥ 0.7: content replaced without contradicting it. |
| unsettled | Jev | Every other combination. |

The four questions are Nouls, each one atomic judgment, all in one request per hunk with the shared state `{page, about, before, after}`. Their wording lives in `QUESTIONS` at the top of `classify.py`.

"Factual" is the proxy for a factual error corrected: after the edit, the page contradicts what the draft told a reader. It also catches a fact that changed because the PR's scope changed, so the report lists every factual hunk for a reader to confirm.

## Determinism

- The model is pinned to `jev-1.14.0`, never `jev-latest`.
- Every response is recorded in `scripts/docs_pr_metrics/jev-recordings/`, keyed by a hash of the request, and committed. `--replay` answers only from recordings and fails rather than calling the API, so a rerun is byte-identical and free.
- When the same hunk appears twice, as when a commit repeats an edit in two files, the two requests are identical and share one recording, so the replayed answer is the later of the two live ones.
- Jev's answers aren't perfectly repeatable: the same request moved by about 0.04 between calls during testing. That makes the recordings the source of truth, not a convenience.

## Validation

`classification-labels.json` holds 50 hunks Claude labeled by hand, in three sets. `--validate` replays them and prints the table.

| Set | Purpose |
|---|---|
| tuning (15) | Hunks with telling commit messages, used to write the questions. |
| tuning-2 (15) | A random sample, labeled before seeing answers. It scored 6 of 15 against the first question set, which exposed that "says something different" fires on plain additions. The questions changed after it, so it counts as tuning. |
| blind-test (20) | A second random sample, labeled before any answer was seen, after the last change to the questions. Nothing was tuned on it. |

Scored from the committed recordings, the blind test matched 14 of 20. All 6 misses landed in "unsettled" rather than a wrong class, and no hunk in any set was wrongly called factual. During testing, before the recordings existed, the same 20 scored 15: the difference is Jev's call-to-call variation on hunks near a threshold. These are labels by one annotator, Claude, and several are judgment calls, such as whether renaming an API schema is factual.

## Known limits

- **Unsettled hunks.** Copy edits that also trim a clause often land just under 0.7 on `same_meaning`. Lowering the threshold to catch them would be fitting it to the labeled set, so they stay unsettled and the report counts them.
- **Moved text is counted twice.** Git's hunks are positional, so a moved paragraph is two hunks: a deletion where it was and an addition where it landed. Its lines count once in each, so the move costs twice its length, and it's classified as a deletion plus an addition rather than as one move. PRs that reorganize pages, such as #622 and #715, are inflated most.
- **Large hunks.** Sides over 6,000 characters are truncated and flagged in `revisions.csv`.
