# Checklist: getting-started-tests

Claude Code session name: doc-detective (renamed from getting-started-tests; checklist dir keeps the old name)
Claude Code session ID: 720fe7cf-48da-4332-8c4b-866ca3fa807d
Branch: getting-started-tests · started 2026-09-30 from /home/franc/GitHub/sensible-docs
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
- [ ] LLM fields: build expected-variation guardrails for passing (decided 2026-09-30). Trigger: `customer_service_phone.value` was `"1800-123-4567"` in 1 of 3 runs (docs: `"1800 123 4567"`). Open Qs: which variation is acceptable per field type (punctuation/whitespace for strings, numeric tolerance, presence-only); declared per example on `<!-- example output {...} -->` or per field; how many runs to sample before calling a field flaky
- [ ] Investigate Doc Detective's capabilities for API contract testing: test-level `openApi` property, their docs pages `test-code/generate-tests-from-openapi.mdx` and `test-code/http-and-api.mdx`, `httpRequest` response validation against our specs in `reference/`. Related item already on docs-as-tests (#725) checklist
- [x] Abbreviated output and variable values (2026-10-01, user's design; rejected the `required`/`prefix` marker options): every key and value the docs show must agree with fresh output; omitted keys are ignored; `...` (bare or the string "...", also "…") means "don't check": a value, an object member, or the rest of an array (`[a, b, ...]` = prefix, `[a, ..., z]` = first/last). Arrays without `...` must match in full. Fix PRs never touch `...` and skip blocks with a bare `...`. 17 offline cases pass; real run unchanged. Trade-off: a timestamp shown with a real value fails until the author writes `...`
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
