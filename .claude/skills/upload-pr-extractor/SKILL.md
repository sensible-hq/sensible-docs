---
name: upload-pr-extractor
description: Given a sensible-hq/sensible PR number, find any new/modified extractor test directories and upload their configs and golden PDFs to the Sensible account via the API.
argument-hint: <pr-number>
disable-model-invocation: true
allowed-tools: Bash(gh pr diff:*), Bash(gh pr view:*), Bash(python3:*), Bash(python:*), Glob, Read
---

You are uploading extractor test configs and golden PDFs from a sensible-hq/sensible pull request to the Sensible account.

The PR number is: **$ARGUMENTS**

## Step 1 — Find affected extractor directories

Fetch the PR diff and identify any files added or modified under `extractors/`:

```
gh pr diff $ARGUMENTS --repo sensible-hq/sensible
```

Look for file paths matching `extractors/{customer}/{doctype}/...`. Collect each unique `{customer}/{doctype}` pair.

Only proceed with directories that have **both** a config JSON file (e.g. `all.json`) and at least one golden PDF in `goldens/`. Skip any that are missing either.

## Step 2 — Locate the files

The sensible engine repo is at `../sensible` relative to this repo (sensible-docs). For each `{customer}/{doctype}` pair found:

- Config file(s): `../sensible/extractors/{customer}/{doctype}/*.json`
- Golden PDF(s): `../sensible/extractors/{customer}/{doctype}/goldens/*.pdf`

Use Glob or Read to confirm the files exist before proceeding.

## Step 3 — Upload each config + golden

For each config file and each golden PDF, call the upload script:

```bash
python3 scripts/upload_pr_extractor.py \
  --doc-type {doctype} \
  --config ../sensible/extractors/{customer}/{doctype}/{config}.json \
  --golden ../sensible/extractors/{customer}/{doctype}/goldens/{golden}.pdf \
  --config-name {config_stem}
```

The script uses `SENSIBLE_API_KEY` from the environment. It will:
- Create the document type if it doesn't exist
- Publish the config to production
- Upload the golden PDF as a reference document

If there are multiple config files, run the script once per config. If there are multiple golden PDFs, run the script once per golden (reusing the same config each time).

## Step 4 — Report results

Tell the user:
- Which extractor directories were found and processed
- The Sensible app URLs printed by the script for viewing the results
- Any errors or skipped directories
