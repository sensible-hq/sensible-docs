# Docs triage

Every Monday and Thursday, `.github/workflows/docs-triage.yml` runs `triage.py` over the
sensible-hq/sensible PRs merged in the last 4 days. Jev, TypeSafe's judge model, answers the
yes/no questions in `criteria.md` about each PR, and the script adds one of two labels:

- **`docs_needed_ai`:** confident that the PR needs docs, such as a new SenseML parameter, a new
  input format, or an LLM model change, with nothing suggesting a bug fix, unfinished work, a
  hidden feature, or a one-customer change.
- **`docs_triage_ai`:** the PR may need docs; a human decides. This includes confident PRs that
  might be hidden, unfinished, or customer-specific, following the changelog skill's
  `investigate` rule: don't drop them, check them.

The AI labels are kept separate from `doc_changes_needed` and `docs_done` on purpose: the human
labels are the ground truth for measuring this classifier, so the bot never writes them.

## What gets scored

A merged PR is skipped when it already has a docs label (human or AI), when a bot opened it, or
when a human has removed an AI label from it before.

Jev sees the PR's title, its description with any label names removed, the changed files, a
diff excerpt that starts with the config schema and API files, and the public endpoints from
`reference/openapi_*.json`. Extractor goldens, OCR caches, and lockfiles are left out.
`criteria.md` gives the decision rule.

## Calibration (November 2026)

353 PRs, scored through this script: a tuning sample, a holdout, and 113 PRs the changelog
skill categorized as not documented. "Docs" means `docs_done` or `doc_changes_needed`;
"hidden" means `docs_dont_publicly_doc` or `docs_future_not_yet_blocked`.

| Human label | `docs_needed_ai` | `docs_triage_ai` | No label |
|---|---|---|---|
| Docs (99) | 56 | 36 | 7 |
| Hidden (15) | 4 | 10 | 1 |
| None (239) | 1 | 23 | 215 |

- `docs_needed_ai`: 56 of 61 were docs work. 4 of the other 5 were features chosen not to be
  documented publicly (fullDocument mode, classifyAndQuery, the sort preprocessor), which the
  PR text doesn't reveal.
- `docs_triage_ai`: about half are docs work, and another seventh are hidden features.
- Misses: 7 docs PRs got no label, mostly small behavior changes that Jev read as bug fixes.

Treat these as optimistic. The misses that Jev also missed were never reviewed, and the label
fixes made during calibration came from Jev's own flags. The real measure is new PRs: compare
the AI labels with the labels humans apply. Scoring costs about $0.0002 per PR.

Known weak spots:
- Endpoint reimplementations (such as the SST migration) get triaged unless the description
  says customers see no change.

## Until the GitHub App exists: issues instead of labels

The workflow needs the App's token to read sensible, so until then, run the script locally
with `--issues`. It uses your own `gh` login and labels nothing in sensible. Instead it opens,
in sensible-docs:

- one **`Docs needed (AI): sensible#N`** issue per `docs_needed_ai` PR
- one **`Docs triage (AI)`** issue per run, with a checkbox for each `docs_triage_ai` PR

```bash
python3 scripts/docs_triage/triage.py --issues --dry-run   # print the issues it would open
python3 scripts/docs_triage/triage.py --issues             # open them
```

sensible-docs is public, so the issues contain only PR numbers, links, and the id of the
question that flagged each PR (such as `T-config`): no titles, descriptions, or scores. PRs
already mentioned in any sensible-docs issue, open or closed, are skipped, so running twice
doesn't open duplicates. Run it Mondays and Thursdays, as the workflow will; with
`--since-days 4`, the default, consecutive runs overlap rather than leave gaps.

## Running it locally

```bash
export TYPESAFE_API_KEY=...        # gh must be logged in with access to sensible
python3 scripts/docs_triage/triage.py --dry-run                 # last 4 days, no labels
python3 scripts/docs_triage/triage.py --dry-run --pr 3474       # specific PRs
```

Locally the script prints titles and the top scores. In GitHub Actions it prints only counts
and PR numbers, because this repo's logs are public and sensible is private.

## Setup

1. Create a GitHub App in the sensible-hq org with repository permissions **Contents: read** and
   **Pull requests: write**, and install it on `sensible-hq/sensible` only.
2. In this repo, create an environment named `docs-triage`, limited to the `v0` branch, with:
   - variable `DOCS_TRIAGE_APP_ID`
   - secret `DOCS_TRIAGE_APP_PRIVATE_KEY`
   - secret `TYPESAFE_API_KEY`
3. Run the workflow once by hand with **dry_run** checked.

## Tests

```bash
cd scripts/docs_triage/test/tests && python -m pytest -q
```
