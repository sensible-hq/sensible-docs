# doc-test-skill: progress and decisions

Handover file for whoever picks up the `add-doc-tests` skill. Read this, then the checklist, then the concept.

- Checklist: `.claude/sessions/doc-test-skill/checklist.md`
- Design: `design/docs-test-skill/CONCEPT.md` (the reasoning behind everything below)
- Skill: `.claude/skills/add-doc-tests/SKILL.md` (first version)
- Tooling the skill drives: `scripts/doc-detective/README.md` (on `v0`, plus the classification additions on #741)
- PR: sensible-docs#749 (draft), branch `doc-test-skill`, worktree `~/GitHub/sensible-docs-doc-test-skill`

Sessions that worked on this branch:

| Session | ID | What it did |
| --- | --- | --- |
| `doc-detective` | `720fe7cf-48da-4332-8c4b-866ca3fa807d` | Concept, Doc Detective research, parameter-table prototype (2026-10-13 to 2026-10-14) |
| `xlsb` | `1e71441a-3c84-48a0-baa5-c36aac379bbb` | Wrote the first version of the skill while testing the XLSB docs (#741), 2026-11-10 |

A new session taking over should add itself to this table, update `.claude-session` at the worktree root, and commit both.

## Where things stand (2026-11-11)

- **The skill exists but hasn't been reviewed.** Frances hasn't reviewed the concept's open questions or the skill. Nothing calls the skill yet: the hook steps in the doc-writing skills aren't added.
- **It depends on #741 (open).** #741 adds classification claims (`expect {"compare": "classification"}`), spreadsheet reference documents for fixtures, curl commands in the report, and saved reports (`DOC_TESTS_SAVE_REPORT=1`). The skill's markup table and Step 6 refer to them, so #741 merges before #749.
- **#737 (docs-test tooling) merged.** **#744 (API contract tests) is still open**; the skill routes API spec claims there.
- **The branch is 67 commits behind `v0`** (as of 2026-11-11). Merge `v0` in before more work; expect conflicts only in session pointer files (keep this branch's).
- **The PR description is out of date** in places; the "Status" section added on 2026-11-11 says what's current.
- **The parameter-table prototype** (`scripts/param-tables/`) works and found 6 real docs problems on 5 pages; nothing has been fixed, and its 17 gap warnings aren't triaged.

## Progress log

### 2026-10-13 (session `doc-detective`)
- Drafted the concept: triage rubric, per-surface tests (UI, code, SenseML reference, API), and where each doc-writing skill would call the new skill.
- Researched Doc Detective's docs and its agent-tools plugin, and folded the useful guidance into the concept (test promises not the product, one test per procedure, prove a test can fail, cap the fix loop at 3, deterministic tests only in CI gates).

### 2026-10-14 (session `doc-detective`)
- Decided how parameter tables are tested (no per-row markup, no spec files; see Decisions).
- Prototyped `scripts/param-tables/check_param_tables.py` with 18 offline tests. First full run: 6 real docs problems on 5 pages, 17 gap warnings.
- Added the Doc Detective-compatibility requirement and the licensing rule (compliance flagged AGPL).
- Renamed the code-test markers in the concept to `inline` / `fixture` / `expect`, matching #737.

### 2026-11-10 (session `xlsb`, while testing #741's XLSB claims)
- Wrote `.claude/skills/add-doc-tests/SKILL.md`, first version: list claims, triage, pick the markup from the README, preview, prove each test can fail, run and save the report, capped fix loop, claims table in the PR.
- In #741, extended the runner with classification claims, persistent-fixture classification, spreadsheet reference documents, curl commands and file links in the report, and saved reports. Updated the skill's markup table to match.

## Decisions

| Date | Decision | Why | Who |
| --- | --- | --- | --- |
| 2026-10-13 | Write our own skill; borrow Doc Detective agent-tools' ideas, don't install it | Its generator skips reference tables and API specs, and doesn't know our code-test markup, judge, envelopes, or test account | Claude, in the concept |
| 2026-10-13 | Tests stay inline in the page, not in separate spec files | Doc Detective recommends inline for tests kept close to content; spec files drift | Concept (open question 1 still lists it for review) |
| 2026-10-14 | Parameter tables: schema checks need no markup; behavior checks (defaults, described effects) get one `<!-- param tests {...} -->` comment above the table | Per-row comments break Markdown tables and there are hundreds of rows; sidecar specs repeat every name and drift | Frances |
| 2026-10-14 | Every custom test format stays analogous to Doc Detective, with a migration guide written as part of its design | Keep a switch to Doc Detective cheap | Frances |
| 2026-10-14 | Avoid AGPL; Doc Detective only as the pinned, unmodified CLI; no agent-tools, its LSP, hooks, or hosted MCP; check licenses of new tools | Compliance flagged AGPL as viral; the repo is public | Compliance, via Frances |
| 2026-10-14 | API spec claims go to #744's contract-test suite, not page markup | #744 already reads claims from the spec and reports docs impact | Concept |
| 2026-11-10 | Skill lives on #749 with its concept; runner changes ship with the docs claim that needed them (#741) | A doc claim and its test ship together; the skill builds on the concept | Claude (Frances didn't object) |
| 2026-11-10 | Extend the runner, in the existing `<!-- name {json} -->` shape, when no markup fits a claim, and propose it to Frances first | Classification needed it; the skill's "Extending the runner" section records the steps | Frances agreed, in the xlsb session |
| 2026-11-10 | Reports Frances should see get saved and committed (`DOC_TESTS_SAVE_REPORT=1`, `scripts/doc-detective/reports/`), and show each request's curl command and links to test files | Frances wanted a permanent HTML report she can read without rerunning | Frances |
| 2026-11-10 | Prefer persistent `fixture_` doc types she can open in the app over temporary ones | Frances wanted to view the doc type in her Sensible account | Frances |
| 2026-11-11 | Test documents, doc types, and configs are realistic business documents (sparse is fine), named after the business document, with invented values | Abstract fixtures like `fixture_spreadsheet_classify` don't show a reader or reviewer what a real customer would test | Frances |
| standing | Test account only: `SENSIBLE_TEST_API_KEY`, never `SENSIBLE_API_KEY`; never print keys | Test runs create and delete resources | Frances |

## Open questions (for Frances)

From the concept (unanswered):
1. Budget: what can new tests cost per PR (extractions, judge calls)? A cap per run beyond the existing 20 extractions?
2. When tests run: every docs PR (`--check-syntax` only), merge to `v0` (full), weekly?
3. Defaults: ask engineering to add `default` to the SenseML schema, so default claims become a free check?
4. UI state: a cleanup convention for procedures that create objects in the shared test account?
5. Judge confidence zones: align with agent-tools (auto-pass ≥ 90%) or keep ours (pass ≥ 70%)?

From the skill's first version:
6. Is the skill's Step 4 (preview the markup before writing it) worth the extra round trip on every page?
7. Should the skill also save the report for pages with only `--check-syntax` (no keys)?

## Next steps

See the checklist's "Next steps". In order: review (Frances), merge #741, merge `v0` into this branch, add the hook steps to the doc-writing skills, the post-edit hook, then mark #749 ready.
