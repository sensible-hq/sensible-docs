---
name: extract-testable-claims
description: After drafting or updating a docs page, extract the claims Frances will want to test (defaults, value types, required parameters, compatibility, null/empty/missing input, scope, restrictions, example output), score each against the criteria with Jev, look up evidence in the engine code, and present the ones worth testing with a proposed test for each. Use after update-docs-from-pr, update-existing-doc, create-new-doc, or create-docs-example, or when asked "what should I test", "extract testable claims", "which claims need verifying".
argument-hint: "[docs page path or docs PR number] [engine PR number]"
disable-model-invocation: true
allowed-tools: Bash(git:*), Bash(gh pr view:*), Bash(gh pr diff:*), Bash(python3 .claude/skills/extract-testable-claims/score_claims.py:*), Bash(python3 scripts/doc-detective/codetests/evidence.py:*), Bash(python3 scripts/doc-detective/test_matrix.py:*), Read, Grep, Write
---

You are finding the claims in a docs change that Frances will want to test before it ships, and presenting them with evidence and a proposed test. You don't run the tests unless she asks.

The arguments are: **$ARGUMENTS**. A docs page path or docs PR number; with neither, use the docs pages the current branch changes against `origin/v0`. An engine PR number, if given, is the source PR. Repos and paths come from `.claude/settings.json` (see `.claude/repos.md`).

**What goes where.** Only docs text (claims and the sentences they came from) goes to Jev. Engine code, diffs, and file excerpts stay with Claude.

## Step 1 — Collect the changed text

```bash
git fetch origin
git diff -U0 origin/v0 -- <docs page>
```

Take every added or changed line: prose, parameter table rows (the key, value, and description columns all carry claims), and the config and Output blocks of examples. For a new page, take the whole page.

## Step 2 — Split into claims

Read `.claude/skills/extract-testable-claims/criteria.md`. Split each sentence or table cell into claims that each state one behavior, and rewrite each so it stands alone (name the parameter instead of "this parameter"). Table columns carry implicit claims: a value column of `integer. default: 0` is a type claim and a default claim; `(**required** unless …)` is a required claim. An example is one output claim: "the example config on the example document produces the Output block."

Write the claims to a JSON file in the scratchpad: a list of `{"claim", "sentence", "page", "line"}`, plus `"kind": "output"` on output claims. The scorer marks those `test` without asking Jev, which scored them inconsistently.

## Step 3 — Score them

```bash
python3 .claude/skills/extract-testable-claims/score_claims.py <claims.json> --out <scored.json>
```

Jev answers the criteria question for each claim. `test` (p ≥ 0.70) and `unsure` go forward; `skip` doesn't, but count it in the report. Exit code 3 means Jev was unavailable: say so, and fall back to judging the claims against `criteria.md` yourself, marked as unscored.

## Step 4 — Find the evidence

For each claim going forward, look for evidence, strongest first:

1. **A live run** in this session or recorded on the docs PR: name the doc type and extraction ID.
2. **Engine code** on `origin/main` (run `git -C "$ENGINE_DIR" fetch origin` first): the type in `src/engine/types.ts`, the generated schema in `src/engine/__generated__/`, and the code that reads the parameter. Cite `file:line`.
3. **The engine PR's description or review comments.** Weaker: it says what was intended, not what shipped.

Mark each claim **contradicted** (the evidence disagrees), **none**, **PR text only**, **code**, or **run**. Code evidence is enough for a type or schema claim. For behavior, especially edge cases, code is a reading, not a test; say so.

## Step 5 — Propose a test for each

A good test gives a different result if the claim is false. A test that passes either way proves nothing.

- **Pair it with a control.** For example, run the same document without the parameter, or swap the order of a match array, so only the claim explains the difference.
- **Schema claims (types, required, compatibility):** publish the config. Drafts skip schema validation; only publishing checks it.
- **Behavior claims:** make the expected output differ depending on whether the behavior happened. A field that's null unless OCR ran is better than timing; the API response has no OCR cost field, and timing is only a hint.
- **One config per document type**, so Sensible can't choose a different config.
- **Check the environment.** A parameter can be merged but not deployed. Run every test in the docs test account, `https://api.sensible.so/v0` with `SENSIBLE_TEST_API_KEY`, never `SENSIBLE_API_KEY` (see `CLAUDE.md`). If publishing fails schema validation with the new name, it isn't deployed there.
- Use fictional data in any document you build.

## Step 6 — Present

Lead with the claims Frances most needs to test, in this order: contradicted, none, PR text only, code (behavior), code (schema), run. For each:

| claim | kind | p | evidence | proposed test |
| ----- | ---- | - | -------- | ------------- |

`kind` is one of the kinds in `criteria.md`. Keep each proposed test to the config change, the document, and the result that would confirm or contradict the claim.

After the table, list the `unsure` claims in one line each, and give the number of claims scored `skip`. Don't list those; Frances can ask.

Offer to run the tests. Don't run them, publish configs, or create document types until she says to.

## Step 7 — Review, then record

Only after tests ran. Nothing goes into `scripts/doc-detective/evidence/`, `TEST-MATRIX.md`, or the page until Frances approves it here.

For each tested claim, present one entry:

| claim ID | claim, as tested | kind | runs (test and control) | expected vs. actual | verdict | proposed priority |
| -------- | ---------------- | ---- | ----------------------- | ------------------- | ------- | ----------------- |

- **Verdict** is `holds`, `holds_with_bug`, or `contradicted`. A contradicted claim gets a record too: it documents why the page changed.
- **Proposed priority** is 1, 2, or 3 (runnable markup on the page, at that page's cadence; see `test-pages.json`) or **record only** (no markup; evidence only). Propose record only unless the claim is the kind that breaks silently when the engine changes and a code-test kind can run it.
- Below the table, give the exact `tested claims` comment for each section with record-only claims, one comment per section, placed after the section's heading and its table or prose: `{/* tested claims {"ids": ["<claim_id>", ...]} */}`.

Frances approves, edits, rejects, or changes the priority of each entry. Then, for the approved record-only claims:

1. Write each record to `scripts/doc-detective/evidence/<page slug>/<claim_id>.json` and its files to `files/` beside it (shape: `scripts/doc-detective/schemas/evidence.schema.json`), with `approval` set to Frances and the date she approved.
2. Add the approved comments to the page.
3. Run `python3 scripts/doc-detective/codetests/evidence.py check` and `python3 scripts/doc-detective/test_matrix.py`, and fix anything `check` reports.

For approved claims at priority 1 to 3, write the page markup instead (see `scripts/doc-detective/README.md`, "Markup").

