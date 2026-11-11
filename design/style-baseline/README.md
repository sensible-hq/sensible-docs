# Style cleanup: baseline and evals

How to show that cleaning up the style system ([style-system-map.md](../style-system-map.md)) cuts the rework on AI-written docs. There are four layers, from cheapest to most rigorous. Layers 1 and 4 run today. Layer 2 reuses the end-to-end eval in `sensible-docs-gen`. Layer 3 comes with each new rule.

| layer | question | data | runs |
| ----- | -------- | ---- | ---- |
| 1. Field baseline | How much rework did real PRs need? | GitHub, git, Vale, transcripts, Toggl | `scripts/style_baseline/pr_metrics.py`, before and after |
| 2. Replay eval | On the same tasks, does the cleaned-up system draft closer to what you merged? | frozen past PRs, re-run 3 times each | `sensible-docs-gen` L7 (`evals/cases`, `evals/score.py`) |
| 3. Rule evals | Does each rule fire when it should, and only then? | labeled fixtures per rule | Vale test files; Jev calibration (`sensible-docs-gen` L6) |
| 4. Guidance health | Is the guidance itself smaller and consistent? | the guide files | a count, by hand or script |

## 1. Field baseline (historical)

`summary.md` in this directory is the first run: 29 merged content PRs since 2026-06-01. `prs.csv` has one row per PR and `revisions.csv` one row per revision commit. Medians for the 22 page tasks (PRs that change 6 pages or fewer; bulk excerpt rewrites are reported separately):

| metric | baseline | what it shows |
| ------ | -------: | ------------- |
| revision commits per PR | 5 | rework after the first draft |
| style revision commits per PR | 1.5 | the part of that rework the cleanup targets (keyword heuristic, see caveats) |
| churn (lines written / lines merged) | 1.39 | 39% of written lines were rewritten or thrown away |
| Vale alerts introduced, first draft | 0 | **current Vale catches almost none of what you correct** |
| hours open to merge | 14.7 | includes idle time; Toggl replaces it |
| your prompts per PR | 7 | the real back-and-forth (only 6 PRs still have transcripts) |
| GitHub review comments per PR | 0 | you correct in chat, not on GitHub, so this metric is not useful |

What this says, plainly: the rework is real (5 revisions, 39% churn) and none of it shows up in Vale. So the metric that should move after the cleanup isn't "Vale alerts". It's **revision commits and prompts that a deterministic rule would have prevented**. Measuring that needs one manual step, below.

### Label the revisions (the key step)

Fill the `rule_id` column in `revisions.csv` with the ID from the style map that the revision fixed (`C1`, `D1`, `J4`, …), `fact` for a factual correction, or `none`. 257 rows, 233 of them from the 22 page-task PRs; labeling those is one to two hours. Then:

- **preventable share** = revisions labeled with a `D*` rule / all revisions. This is the ceiling on what deterministic work can save.
- **judgment share** = revisions labeled `J*` or `C*`. This is what needs Jev, or a decision on a contradiction.
- **top rules by revisions** tells you which rules to build first. Do this before writing any rule.

Labeling the transcripts' correction prompts the same way gives a second, richer source, but only for PRs from 2026-10-13 on (see retention, below).

### Toggl

Export a **detailed report** CSV (columns `Description`, `Start date`, `Duration`) and run:

```bash
python3 scripts/style_baseline/pr_metrics.py --since 2026-06-01 --toggl ~/Downloads/toggl.csv
```

An entry matches a PR when its description contains `#<number>` or the branch name. From now on, two habits make Toggl precise:

- Put the PR number or branch in the entry description.
- Tag entries `draft`, `correct`, `review`, or `tooling`. **Correction time** (`correct`) is the headline metric: it's the time the cleanup is meant to remove. `tooling` keeps the cleanup work itself from counting as writing time, and it's what you compare the savings against.

### Transcript retention

Claude Code deletes transcripts after `cleanupPeriodDays` (default 30). Your oldest sensible-docs transcript is from 2026-10-13, so prompts and corrections for earlier PRs are gone, and the rest are being deleted as they age. Set `"cleanupPeriodDays": 3650` in `~/.claude/settings.json` now if you want them in the after comparison.

### Caveats

- The commit categories are keyword guesses. "add inline comments" counts as style but is new content. Use the hand labels, not the categories, in any claim.
- Hours open to merge counts nights and weekends. Use Toggl.
- Things that changed besides the guidance: the model (Opus 5.5 since 2026-11), the task mix, and your own faster reviewing. Layer 2 controls for all three; layer 1 can't.

## 2. Replay eval (controlled)

`sensible-docs-gen` already has the harness: L7 replays real past PRs, 3 runs per case, scored by `evals/score.py` against an answer key (`evals/cases/pr-3457/expected.yaml`). Add style to it rather than building a second harness.

**Case set.** Freeze 6–8 page-task PRs that cover the main page types and had the most style rework. Candidates from the baseline: #729 (Column Stop, 13 revisions, churn 6.1), #718 (JsonLogic operators, 15), #730 (Region includeAnchor), #798 (deprecation), #742 (concept, 6 pages), #590 (portfolio images). Each case runs from the docs commit **before** the PR, so the merged answer isn't in the repo. Hold 2 cases out, unused while you tune rules, to check you didn't overfit.

**Conditions.** The same cases and the same pinned model under:

1. `baseline`: guidance and skills as of `v0@39ff57219`.
2. `cleaned`: after the contradictions are resolved and the new rules are in place.
3. Optionally `cleaned-no-guides`: the new rules and hook only, with the long guide files removed from the skill. This shows whether the rules replace the guides or only add to them.

**Scores per run.** Measure every condition with the **same final rule set**. If baseline is scored with the old Vale and cleaned with the new one, the numbers move because the ruler changed.

| score | how |
| ----- | --- |
| deterministic violations per 100 changed lines | all D-rules (Vale + scripts) on the diff |
| judgment violations per 100 changed lines | Jev on the J-rules' detector hits |
| distance to merged | word-level edit distance between the run's changed sections and your merged version, normalized by length. This is the closest proxy for "edits you'd still make". |
| first-sentence agreement | J1's verdict matches the merged page |
| self-corrections | hook fires per run, and whether the agent fixed them (from the run log) |
| cost | tokens and wall time per run (docs-gen `report/cost.py`) |
| facts | the existing answer-key items, so a style gain that loses accuracy shows up |

Report the median and spread over the 3 runs, per case. A difference smaller than the spread between runs of the same condition isn't an improvement.

## 3. Rule evals (per rule, before shipping it)

Every rule spec in the style map already has `examples.fail` and `examples.pass`. Make them the test:

- **Deterministic rules:** a fixture file per rule under `.github/styles/Sensible/tests/`, with the fail lines and pass lines. CI runs Vale on it and asserts the exact alert lines. Also run the rule on the whole corpus and record its hit count. A new rule with 300 hits is either finding a real backlog or is too broad, and you should know which before agents start "fixing" 300 sentences.
- **Judgment rules:** label 30–50 detector hits from the corpus (yes or no). Jev's agreement with your labels is the gate, as in docs-gen L6. Track precision (Jev flags only real problems) more than recall: a judge that cries wolf trains the agent to ignore it.

| per-rule metric | target |
| --------------- | ------ |
| fixture pass | 100% |
| corpus hits, deterministic | reviewed; known false positives listed in the rule |
| Jev agreement with your labels | ≥ 90% on held-out labels |
| agent fix rate | share of hook alerts the writing agent fixes in one turn without breaking meaning (from replay logs) |

## 4. Guidance health (static, today)

Cheap to count, and it shows the cleanup even before the evals run.

| metric | today | after |
| ------ | ----: | ----: |
| contradictions (style map §2) | 9 + 7 smaller | |
| rules stated in more than one place (§3) | 13 | |
| glossary avoid-terms enforced by Vale | 3 of 23 | |
| skills that run a missing tool | 3 | |
| guide words a reference-page skill loads | count when needed: `wc -w` on the files each skill reads | |
| rules that are deterministic (Vale or script) / all rules | count after §5 is labeled | |

## Order

1. Set `cleanupPeriodDays`, and start the Toggl description and tag habits **now**. Every day before that is lost baseline data.
2. Send the Toggl export, rerun layer 1, and label `revisions.csv`.
3. Pick the replay cases from the labeled PRs, and record baseline scores with the rule set you're about to build.
4. Do the cleanup, building rules in order of labeled revision counts, each with its rule eval.
5. Rerun layers 1, 2, and 4. For layer 1, compare PRs after the cleanup against this baseline, page tasks only.
