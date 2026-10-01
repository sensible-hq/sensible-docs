# Checklist: getting-started-tests

Claude Code session name: doc-detective (renamed from getting-started-tests; checklist dir keeps the old name)
Claude Code session ID: 720fe7cf-48da-4332-8c4b-866ca3fa807d
Branch: doc-detective-getting-started-tests (renamed from getting-started-tests 2026-10-01) · started 2026-09-30 from /home/franc/GitHub/sensible-docs
PR: #737 (draft). Replaced #735, which GitHub closed when the head branch was renamed
Resume: `cd /home/franc/GitHub/sensible-docs && claude --resume 720fe7cf-48da-4332-8c4b-866ca3fa807d`

Goal: add real Doc Detective tests to `docs/document extraction/getting-started.md`, a mix of UI tests (Sensible app steps) and code tests (code samples).

Prior art: `doc-detective-poc` branch (PR #725), `sessions/docs-as-tests/CONCEPT.md`. Key findings to carry over:
- Inline statements: `<!-- test {...} -->` … `<!-- test end -->`, `<!-- step {...} -->`. ReadMe preserves HTML comments (D1).
- `detectSteps` is on by default, so every link gets a `checkLink` unless disabled.
- CLI exits 0 on failure unless `--exit-on-fail`.
- Don't use `httpRequest` response assertions to compare Sensible output (null crash, order-insensitive arrays).
- Doc Detective 4.38.1 installed globally (`doc-detective`).

- [x] Create worktree and draft PR
- [x] UI test auth: dedicated account frances+doc-detective@sensible.so; `SENSIBLE_TEST_EMAIL` / `SENSIBLE_TEST_PASSWORD` in git-ignored `.env`
- [x] Dry run: 1 test, 7 steps, no auto-detected steps (`detectSteps: false` in `.doc-detective.json`)
- [x] UI test `app_document_types_page`: sign in, Document Types loads. Real run green; wrong-password run fails at step 5 (exit 1)
- [x] Secrets: Doc Detective writes typed keys in plain text to JSON/HTML reports (no masking option; upstream issue doc-detective/doc-detective#204, open since 2025-02). Workaround: `scripts/doc-detective/run.sh` scrubs secret values from reports after the run
- [ ] Gotcha: `.env` (via `loadVariables`) overrides shell env vars. In CI, don't write a `.env`; pass secrets as env vars only
- [ ] UI tests: remaining app steps in the tutorial (New document type dialog, editor), if wanted
- [ ] Code tests: annotate example doc, config, and claimed output with HTML comments (reuse option A grammar from docs-as-tests CONCEPT.md: `<!-- example config -->`, `<!-- example document {"url": ...} -->`, `<!-- example output {...} -->`)
- [ ] Code tests: run them via the sensible repo's `extract-all` harness instead of the API (Horacio's suggestion, Slack C0215T9K86P p1790190316244059). Already tracked on docs-as-tests (#725) as "Follow up w/ Horacio" and E11; do the getting-started trial here
  - Suite layout: `extractors/<suite>/<doc_type>/<config>.json` + `goldens/<doc>.pdf` + `goldens/<doc>.pdf.extracted.json`; `extract-all` fails with OUTPUT CHANGED on any diff (full-output snapshot)
  - Goldens are full output, docs Output blocks are partial: need a separate subset check of docs Output vs golden
  - Existing `extractors/account_seed/layout_basics` suite looks like seeded in-app tutorials; check overlap with getting-started
  - Open Qs for eng: config-to-document matching when a doc type has several configs; runtime requirements; running against released engine vs HEAD
- [x] extract-all trial (2026-09-30, fresh shallow clone of sensible @ 4175b8c in scratchpad, no AWS creds on machine):
  - Suite: `extractors/docs/auto_insurance_quotes/anyco.json` (config copied verbatim from getting-started.md lines 93–162; harness accepts `/* */` comments) + `goldens/auto_insurance_anyco.pdf`
  - `extract-all -e docs`: 12.7s wall, 6.4s extraction
  - Layout fields (`policy_period`, `comprehensive_premium`, `policy_number`) match the docs Output block exactly, with no AWS creds or network
  - LLM fields (`bodily_injury_premium`, `customer_service_phone` from `queryGroup`) = null: "ConfigurationError: Could not load credentials from any providers" (LLM calls go through AWS; cache miss in `extraction-cache/ocr/GPT-3`)
  - Costs measured: shallow clone 1.9 GB (613 MB .git, 779 MB extractors/); cold `pnpm i` 1m16s, 783 MB node_modules. Eng CI: checkout ~30s, cached install 15–46s, full suite (~800 docs) ~504s
  - Estimate for a weekly docs Action: ~2 min/run, dominated by setup
- [ ] Decide: LLM `queryGroup` in the layout tutorial's first config. Options: compare layout fields only; get AWS creds from eng; commit LLM cache entries to the sensible repo
- [ ] Decide: where the suite lives (generated each run in docs CI vs committed to sensible repo's extractors/)
- [x] Switched code tests to the API for now (2026-09-30). `scripts/doc-detective/run_examples.py`: parses `<!-- example config|document|output -->` markers inside the Doc Detective test, uploads config as `<testId>` in doc type `docs_ci_examples` (published to development), extracts with the Python SDK (`sensibleapi` 0.0.17), subset-compares against the docs Output block, deletes the doc type at the end (`--keep` to skip). Doc Detective calls it via a `runShell` step in test `extract_auto_insurance_anyco`
  - Deps: `pip install --target scripts/doc-detective/.deps -r scripts/doc-detective/requirements.txt` (no python3-venv on this machine)
  - DELETE /document_types removes configs and reference docs but NOT extraction history in the app
  - Full Doc Detective run (UI + code): 45s
- [x] API key: switched to the docs test account's key, `SENSIBLE_TEST_API_KEY` in `.env` (2026-10-01). Runner never falls back to `SENSIBLE_API_KEY`; refuses with exit 2 if unset. Verified test account (3 doc types) != main account (58); both secrets absent from reports and terminal output
- [x] Extraction history: accepted. Can't be deleted (no public API, and not in the app for this user). Main account keeps about 6 `ci__extract_auto_insurance_anyco.pdf` extractions from 2026-09-30; each future run adds one to the test account
- [ ] Docs drift found: `bodily_injury_premium.source` is `"100"`, docs say `"$100"` (3/3 runs). Fix the Output block?
- [x] Example doc URL: single source of truth. `<!-- example document -->` (no URL) sits directly above the visible download link; the runner reads the first link after it. Verified: changing the visible link makes the runner test the new URL (404 → DOCUMENT_UNREACHABLE). Code test `<!-- test -->` start moved to just before the "Configure the extraction" list
- [x] LLM fields: LLM-as-judge guardrail (`scripts/doc-detective/llm_judge.py`). Judge model configurable: `--judge-model`, `DOC_EXAMPLES_JUDGE_MODEL`, default `claude-sonnet-5-5` (2026-10-01: user dropped the "judge must differ from generator" logic and the llm-models.md lookup; Sensible's generators never overlap with it anyway). Routing (`FieldIndex`): walks the whole config, so LLM methods (queryGroup, list, nlpTable) nested in sections, conditionals, or any container count; each mismatch is decided by the innermost path segment that's a known field ID; a fallback chain mixing layout + LLM under one ID is judged and flagged. Only mismatches are sent, with path, prompt, documented, actual. Structured output per claim: path, claim, observed, match, confidence, reasoning. pass ≥0.7 = OK; partial/low-confidence = WARNING (passes); fail = LLM_DRIFT. Offline tests: `python3 -m unittest discover -s scripts/doc-detective` (12, also run in CI)
  - [x] Real runs: with claude-opus-5, `"$100"`→`"100"` pass (0.85, 0.75), wrong values fail (0.95, 0.98); with claude-sonnet-5-5, `"$100"`→`"100"` pass (0.90) and phone separators pass (0.97). Full suite green; no secrets in reports/log
  - [x] Comparison summary in every run's output (so in the Doc Detective HTML report and failure issues): overall identical / matches, not identical (what the docs leave out, parts marked ..., LLM values decided by the judge) / mismatch; per documented field: layout, LLM, or fallback, and exact match / exact mismatch / judged path with verdict, confidence, model; "docs show N of M items" for shortened arrays; judge reasoning. 16 offline tests
  - [x] Judge prompts and settings moved out of code into `scripts/doc-detective/judge/` (2026-10-01): `config.json` (model, min_pass_confidence, max_tokens, file names), `system-prompt.md`, `user-prompt.md` and `claim-template.md` (`string.Template` placeholders), `output-schema.json`. `DOC_EXAMPLES_JUDGE_MODEL` still overrides the model
  - [x] Readable report `scripts/doc-detective/output/report.html` from `html_report.py` (run.sh generates it before the secret scrub; CI artifact includes it): tests table; per code test the LLM fields with extraction prompt and result, layout fields as a count (listed only on mismatch), not-compared parts, judge verdict cards (docs vs Sensible values, verdict, confidence, reasoning), collapsible full system/user prompt and raw judge JSON. Text summary in the Doc Detective report trimmed to match. Verified by screenshot. 18 offline tests
  - [x] Declared types in judge claims (2026-10-01): `FieldIndex.type_for` reads each value's type from the config (Query Group query `type`; List property / NLP Table column `type`, innermost wins; NLP Table column IDs read from `columns[i].id` in the documented output; configurable `{id, options}` form kept; default `string` per types.md). Each claim carries the declared type, that type's output example parsed from `docs/Senseml reference/field-query-object/types.md` (`types_reference_file` in judge/config.json; 17 types have examples, Images/Table don't), and the whole typed field (documented and returned) so value/source/unit are compared together. System prompt: value decides; source is raw text; wrong JSON type for the declared type, a different output type, or a different unit = fail. Real judge on crafted claims: same value/different source = pass (0.90); "one hundred" for type number = fail (0.97); € vs $ = fail (0.98). Type shown in report.html. 25 offline tests
  - [x] Report order: layout fields → not compared → LLM fields → judge reasoning, so LLM fields sit next to the judge's reasoning (HTML and text summary)
  - [x] Report: deterministic vs probabilistic (2026-10-01). Disclaimer "Every check is deterministic (an exact comparison) unless it's labeled judge…" at the top of report.html, in the text summary, and in the failure issue; every judge-decided result carries a `judge` chip (HTML) or `[judge]` tag (text): LLM field result, reasoning heading, each verdict card, and the tests table row. Verified by screenshot
  - [ ] Regression envelope testing for each LLM-judged field (docs-as-tests book): run the example N times to baseline each field's output characteristics (formats seen, length range, null rate, type and unit), store a per-field baseline, and flag runs that fall outside it. One envelope per field, since each field varies differently (phone separators vs currency source text vs free-text length). The judge compares docs vs product; the envelope compares run vs baseline, which catches behavior shifts that still pass the judge. Open Qs: N, where baselines live (committed JSON per test/field?), how a baseline is refreshed, and whether an envelope breach fails or warns
  - [ ] Known routing limit: a list property or nested key that has the same name as a layout field ID elsewhere would be routed by that ID
  - [ ] Watch judge confidence near the 0.7 threshold for pass/warn flapping
- [ ] Investigate Doc Detective's capabilities for API contract testing: test-level `openApi` property, their docs pages `test-code/generate-tests-from-openapi.mdx` and `test-code/http-and-api.mdx`, `httpRequest` response validation against our specs in `reference/`. Related item already on docs-as-tests (#725) checklist
- [x] Abbreviated output and variable values (2026-10-01, user's design; rejected the `required`/`prefix` marker options): every key and value the docs show must agree with fresh output; omitted keys are ignored; `...` (bare or the string "...", also "…") means "don't check": a value, an object member, or the rest of an array (`[a, b, ...]` = prefix, `[a, ..., z]` = first/last). Arrays without `...` must match in full. Fix PRs never touch `...` and skip blocks with a bare `...`. 17 offline cases pass; real run unchanged. Trade-off: a timestamp shown with a real value fails until the author writes `...`
- [x] Syntax checks (2026-10-01), run before any network call and standalone via `--check-syntax` (no key needed): config = JSON + comments + trailing commas; output = JSON + comments + `...`, no trailing commas; both reject duplicate keys and NaN/Infinity; errors give the doc line (duplicate key/NaN give the block's start line only). Verified with 8 deliberately broken copies
- [x] E5 answered (2026-10-01): Sensible accepts configs with `/* */` comments and trailing commas (upload 200 + extraction COMPLETE with all fields). Runner now uploads the config exactly as the doc shows it
- [ ] Optional: run `--check-syntax` on pull requests (no secrets needed, a few seconds)
- [ ] Self-audit both tests against the docs-as-tests failure modes for AI-written deterministic tests (requested 2026-10-01; do later). "Insufficient" coverage across the page is OK for now with only 2 tests, but each test must be thorough within its own scope:
  - [ ] Necessary but insufficient: checks that something happened but not what (e.g. an API call returning 200 but its content never checked)
  - [ ] Missing implicit assertions: things that seem obvious from the docs but aren't explicitly checked
  - [ ] Testing inferred or hallucinated claims: what the test expects the docs to say, rather than what they actually say
  - [ ] Silent or swallowed errors: broad error handling that treats any unexpected result as a pass, so the test can't fail
  - Suspects to check first (unverified):
    - UI test: does finding the text "New document type" prove the logged-in Document Types page loaded, or could another page or state show it? Do the tutorial's other claims in that step (the tab name, the dialog) need checks?
    - Code test: `upload_config` publishes with `publish_as`, but does a config with errors still return 200 and extract? (The API says it doesn't reject configs with errors.) Is the `requests.head` check on the PDF enough (status only, no content type or size)?
    - Swallowed errors: `run.sh` uses `set -uo pipefail` without `-e`; `propose_fix` returns False quietly; workflow steps use `continue-on-error`; `delete_doc_type` runs in a `finally` that could hide the original error; `report.py` returns 0 when no results file exists
    - Found 2026-10-01: Doc Detective skips an invalid test spec with a WARNING ("No tests detected") and exits 0. Check whether `exitOnFail` covers this; if not, a malformed inline `<!-- test -->` could silently drop a test from CI
    - Each check should be shown to fail: so far a wrong password, a changed link, wrong output values, and broken syntax have each been shown to fail; list any checks that never have
- [ ] Code tests: API/integration samples
- [ ] Local green run
- [x] CI workflow `.github/workflows/doc-detective-getting-started.yml` (2026-10-01): push to **v0 only** (no `pull_request`, so it doesn't run on this PR) + `workflow_dispatch`, `paths` filter. Pins doc-detective 4.38.1 with `--no-auto-update`. Missing `.env` in CI verified harmless. **Merging this PR triggers the first run**, so add secrets first. Original plan:
  - Paths: `docs/document extraction/getting-started.md`, `scripts/doc-detective/**`, `.doc-detective.json`
  - Repo secrets: `SENSIBLE_TEST_EMAIL`, `SENSIBLE_TEST_PASSWORD`, `SENSIBLE_TEST_API_KEY`. Pass as env vars; don't write a `.env` (it overrides env)
  - `concurrency:` group so two runs don't share `docs_ci_examples` (one run's cleanup would delete the other's config)
  - Steps: install doc-detective (pin version), `pip install -r scripts/doc-detective/requirements.txt`, `scripts/doc-detective/run.sh -i "docs/document extraction/getting-started.md"`; upload scrubbed reports as an artifact
  - Known gap: example PDF links point at `/v0/`, so a PR that changes the PDF tests the old one until merged
  - Optional: local `pre-push` git hook for the same run (not `pre-commit`: ~45s per commit is too slow)
  - [x] Repo secrets added (2026-10-01): `SENSIBLE_TEST_EMAIL`, `SENSIBLE_TEST_PASSWORD`, `SENSIBLE_TEST_API_KEY`
  - [x] On failure (2026-10-01): one standing issue labeled `doc-detective` (comment on the open one, else create); for OUTPUT_DRIFT, a draft PR from reused branch `doc-detective/getting-started-fixes` that rewrites only the mismatched values (`--propose-fixes` / `DOC_EXAMPLES_PROPOSE_FIXES=1`; skips output blocks with comments). `scripts/doc-detective/report.py` builds the issue body from Doc Detective results. Verified with a local CI simulation (scratch worktree, no `.env`, env-only secrets): fix diff was exactly `"$100"` → `"100"`, no secrets in reports/log
  - [ ] Not verified on GitHub yet: issue/PR creation, label creation, fix-branch push (first real run happens on merge)
  - [ ] Until LLM guardrails exist, fix PRs will also propose LLM variation (e.g. phone formatting), and a later run can flip it back
