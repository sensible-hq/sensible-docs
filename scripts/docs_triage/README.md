# Docs triage

Every Monday and Thursday, `.github/workflows/docs-triage.yml` runs `triage.py` over the
sensible-hq/sensible PRs merged in the last 4 days. Jev, TypeSafe's judge model, answers the
yes/no questions in `criteria.md` about each PR. A PR that may need docs gets the
`docs_triage_ai` label, and a human decides what happens next.

`docs_triage_ai` is kept separate from `doc_changes_needed` and `docs_done` on purpose: the
human labels are the ground truth for measuring this classifier, so the bot never writes them.

## What gets scored

A merged PR is skipped when it already has a docs label (`doc_changes_needed`, `docs_done`,
`docs_dont_publicly_doc`, `docs_future_not_yet_blocked`, or `docs_triage_ai`), when a bot
opened it, or when a human has removed `docs_triage_ai` from it before.

Jev sees the PR's title, its description with any label names removed, the changed files, a
diff excerpt that starts with the config schema and API files, and the public endpoints from
`reference/openapi_*.json`. Extractor goldens, OCR caches, and lockfiles are left out.

A PR is labeled when any `T-*` question scores 0.70 or higher and neither `X-*` question does.

## Calibration (November 2026)

Against existing labels, treating any docs label as "needs a docs decision":

| Set | PRs | Recall | False-positive rate |
|---|---|---|---|
| Tuning sample | 65 labeled, 57 not | 0.91 | 7% |
| Holdout | 45 labeled, 95 not | 0.89 | 7% |

Treat these as optimistic. The misses that Jev also missed were never reviewed, and the label
fixes made during calibration came from Jev's own flags. The real measure is new PRs: compare
`docs_triage_ai` with the labels humans apply. Scoring costs about $0.0002 per PR.

Known weak spots:
- Jev can't tell a feature that shouldn't be documented publicly from one that should.
  Those PRs get flagged, and a human applies `docs_dont_publicly_doc`.
- Endpoint reimplementations (such as the SST migration) get flagged unless the description
  says customers see no change.

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
