# Concept: SenseML reference examples as tests

Status: draft for discussion · updated 2026-09-23 · session `docs-as-tests` · PR #725

Original prompt: [original-prompt.md](original-prompt.md)

## The idea

Borrowed from LangChain (via *Docs as Test & AI*): treat every code sample in the docs as a test, run it in CI on a schedule, and get notified when a sample stops doing what the docs say it does.

For the SenseML reference, an "example" is a unit of three things:

1. **Config**: a fenced `json` block of SenseML
2. **Example document**: a URL to a PDF (or other supported file)
3. **Output**: a fenced `json` block showing the `parsed_document` the config produces

The test for each example asks three questions:

> Does the document URL resolve? Does the config run? Does Sensible's output still match the **Output** block?

**Testable surfaces are declared explicitly with HTML-comment annotations.** They are *not* inferred from page structure. The existing `**Config**` / `**Example document**` / `**Output**` convention is used only for a **coverage report** that flags examples that look testable but aren't annotated yet.

- **Phase 1 goal:** a weekly GitHub Action runs every annotated example and opens (or updates) one GitHub issue on any failure.
- **Later goal:** propose fixes as PRs.
- **Playground:** `docs/welcome/draft-getting-started-ai.md` on `doc-detective-poc`. It's a hidden draft topic where the Row example (a copy of `layout-based-methods/row.md`) is now committed. All experiments happen there and no real topic is touched until the annotation format settles. The page can grow as big and messy as the experiments need.

---

## Decisions so far

| # | Decision | Source |
|---|---|---|
| D1 | ReadMe preserves HTML comments through sync. HTML comments are a viable annotation layer | You checked |
| D2 | Testable surfaces are declared with HTML comments, not inferred from docs structure | You |
| D3 | Deterministic (layout-based) examples come first. LLM examples come later and need defined acceptable-variation measures | You |
| D4 | About 90 extractions a week is a trivial cost for deterministic examples | You |
| D5 | The Row section in `draft-getting-started-ai.md` is a stand-in: one topic for many experiments | You |
| D6 | The Row section is committed on `doc-detective-poc` (`7123fb518`) | Done |
| D7 | Doc Detective syntax is the **annotation wrapper**. A custom Python runner does the **extraction test and comparison**. Doc Detective's `httpRequest` assertions aren't used for output comparison | Research below. Proposed, awaiting your OK |

---

## Doc Detective: can we use its comments? (investigated)

**Short answer: yes as the annotation layer, no as the assertion engine.**

This research covers `doc-detective` 4.38.4 (v3 schemas), read from source at commit `dc88004` (2026-09-08). A subagent read the source and schemas and ran the comparator code in isolation. **Nobody has run Doc Detective end to end against this repo yet.** Experiments E2–E4 below close that gap.

### What works in our favor

- **Default Markdown inline statements** (HTML flavor), which are already used in the hello-world POC on this page:
  - `<!-- test {...} -->` … `<!-- test end -->` bound a test
  - `<!-- step {...} -->` declares a step
  - `<!-- test ignore start -->` / `<!-- test ignore end -->` exclude regions
- **Custom inline statements are supported.** In config, use `fileTypes: [{ extends: "markdown", inlineStatements: {...}, markup: [...] }]`. Custom regexes are unioned with the defaults, and capture group 1 is the statement body. (The published docs page for custom formats still shows v2 key names, so trust the schema over the docs.)
- **Markup regexes can capture whole fenced blocks** and turn them into steps. One regex can span the config, URL and output and emit several steps.
- **`httpRequest` covers the API sequence.** It does env-var substitution (`$SENSIBLE_API_KEY`), saves response values into variables (`"variables": {"EXTRACTION_ID": "$$response.body.id"}`), and polls via `onFail: [{"retry": {"limit", "delay", "backoff"}}]`.
- **`runShell` / `runCode` (Python)** check exit codes and stdout.
- **CI support:**
  - The `doc-detective/github-action@v1` action has `create_issue_on_fail`, issue labels and assignees, and `create_pr_on_change`.
  - Reporters include JSON, JUnit, HTML and Markdown.
  - `--test` / `--spec` regex filters and `--dry-run` let you see what got detected.

### Why it shouldn't do the comparison

1. **Its subset comparator crashes on `null`.** Any `null` in the expected body (or an expected object meeting an actual `null`) throws a `TypeError`. Sensible output is full of `null`s. Whether that surfaces as a test FAIL or a runner crash is unverified.
2. **Its array matching ignores order and count.** `[{x:1},{x:1}]` passes against `[{x:1}]`. That's a false pass for table and row outputs, where order and count matter.
3. **Comments get silently mangled in step bodies.** Statement bodies go through `JSON.parse`, then a YAML fallback. Trailing commas survive, but `/* */` comments turn into key names **with no error**. Our configs carry canonical comments (54 of 90).
4. **A captured expected output stays a string.** It's never parsed into an object, so it can't be asserted structurally.
5. **Env-var substitution touches everything.** Any `$WORD` in a config or output would be replaced at runtime.
6. **Polling can't stop early on FAILED.** Retry-until-COMPLETE keeps retrying a FAILED extraction until it hits the retry limit.

### Gotchas to design around

- **Default step detection runs automatically.** `detectSteps` is on by default, so Doc Detective will `checkLink` every link on the page unless it's disabled per test or per file type. On the monster test page this is probably fine, even useful, but it's noisy.
- **The CLI exits 0 even when tests fail**, unless you pass `--exit-on-fail` / `exitOnFail`.
- **Multi-line statements may or may not work.** The docs say comments must be single-line, but the regexes are multi-line capable. Unverified (experiment E3).

---

## Annotation design (proposed)

The goal is to **wrap** each example in Doc Detective's test boundaries, so one annotation set serves both tools. Inside the wrapper, **role markers** point at the blocks. Doc Detective ignores the role markers because they don't match its `test`/`step` regexes, and the Python runner reads them.

````markdown
<!-- test {"testId": "row-two-tables"} -->

<!-- example config -->
```json
{ "fields": [ ... ] }
```

<!-- example document {"url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/row_column.pdf"} -->
| Example document | [Download link](https://raw.githubusercontent.com/.../row_column.pdf) |

<!-- example output {"compare": "subset"} -->
```json
{ "number_1_language_on_github": { ... } }
```

<!-- test end -->
````

### Rules

- **`testId` is the example's stable ID.** The runner uses it as the config name in the CI doc type, so it must match `^[a-z0-9_]+$`. That means underscores, not hyphens, in real IDs.
- **`<!-- example config -->`** must immediately precede a fenced block. The runner parses that block as JSON5 and sends strict JSON.
- **`<!-- example document {...} -->`**: the URL is explicit in the annotation. Scraping the table is the fallback if `url` is omitted. The runner checks that the annotation URL and the visible link match, which catches drift between the two.
- **`<!-- example output {...} -->`** must immediately precede a fenced block. Options: `compare` (`subset` | `exact` | `keys-and-types` | `tolerance`), `ignore` (JSONPath list), and `skip` (reason string).
- **Optional Doc Detective-native steps inside the wrapper,** where Doc Detective is genuinely good:
  - `<!-- step {"checkLink": "<doc url>"} -->`
  - `<!-- step {"runShell": {"command": "python scripts/example_tests/run_examples.py --test row_two_tables", "exitCodes": [0]}} -->`: lets Doc Detective orchestrate and report while the runner does the real work. This is optional (see Q10).

### Alternatives considered

| Option | Verdict |
|---|---|
| **A. Doc Detective wrapper + custom role markers** (above) | **Recommended.** One syntax, ReadMe-safe, Doc Detective-compatible, and the runner works without Doc Detective installed |
| B. Pure custom comments (`<!-- senseml-test ... -->`) | Simpler, no Doc Detective coupling. You lose Doc Detective's link checks, reporters and Action for free |
| C. Pure Doc Detective (markup regex + `httpRequest` + `runCode`) | Rejected. It hits all six problems above, and puts JSON5 and escaping inside regex captures |
| D. Doc Detective custom `inlineStatements` for the role markers | Possible, but no benefit unless Doc Detective itself consumes them. Revisit if we move to option C for some subset |

### Coverage report (the one use of docs structure)

A lint pass finds every `**Config**` fence in `docs/Senseml reference/` that isn't inside an annotated test block, and lists it with a file:line link. That's how you track the "annotate everything" backlog without the structure driving extraction.

---

## What's in the repo (measured)

| Fact | Number | Why it matters |
|---|---|---|
| Pages with at least one `**Config**` block | 64 of 120 | The eventual annotation backlog |
| `**Config**` blocks | 93 (90 fenced as `json`) | About 90 tests at full coverage |
| Configs that aren't strict JSON | 62 of 90 | Canonical `/* */` comments and trailing commas. The runner needs JSON5. The Row config has a trailing comma after `"position": "left",` |
| Outputs that aren't strict JSON | 4 | Fragments or hand edits. Annotate as `skip` or fix |
| Pages where Config count ≠ Output count | 3 | `conditional.md`, `custom-computation.md`, `deprecated-query.md`. Explicit annotations make this a non-issue |
| Unique example-doc URLs | 93 | 1 broken today: `TBD.pdf` in `draft-jsonschema-postprocessor.md` |
| Non-PDF example docs | 1 `.xlsx` | |
| LLM-method pages with examples | 3 (`nlp-table`, `query-group`, `list`) | Phase 3 (D3) |

Side note: the Row example's field ID `python_change_in_TIBOE_rating` misspells TIOBE, in both `row.md` and the draft copy.

---

## API facts that shape the design

- **No endpoint extracts with an inline config.** The runner has to write each config into a dedicated doc type (`PUT /document_types/{id}/configurations/{name}`), then extract with `configuration_name`.
- **The Python SDK (`sensibleapi`) only extracts and classifies.** Config management uses plain HTTP. Proposal: use `requests` for everything, so there's one dependency and one auth path.
- **Validation needs `publish_as`.** The Configuration API takes a stringified config and skips validation unless you set `publish_as`. With `publish_as: "development"`, invalid example configs fail at upload time with a clear category.
- **Not verified:** whether the API accepts JSON5 comments in the stringified config (E5). The safe default is to strip them client-side.

---

## Test artifacts (Q3, still open)

Each run creates:

- **Configs** in the CI doc type: one per `testId`, overwritten each run via an idempotent PUT. They don't accumulate, but each PUT creates a new **config version**, so version history grows by about 90 entries a week. That's probably harmless, but worth knowing.
- **Extractions:** one per example per run, about 4,700 a year.

What the API offers (from the OpenAPI spec in `reference/`):

- **No public endpoint deletes extractions.** Delete exists only for doc types, configs, config versions, reference docs and email processors.
- **Isolation is possible.** `GET /extractions` filters by `document_type_ids` and `environments`, so a dedicated doc type plus the `development` environment keeps CI extractions out of real dashboards and statistics, as long as people filter.
- **Tagging is possible.** Async extraction accepts `document_name` (for example `ci__row_two_tables__<run_id>.pdf`) and `extra_data` (for example `{"ci_run": "<run id>", "git_sha": "..."}`) for traceability.
- **Unverified leads:**
  - The spec mentions "custom data retention policies." An account-level retention setting might auto-expire CI extractions.
  - An error string says "To use the asynchronous flow you must have persistence enabled." That implies **sync** `/extract/{type}/{config}` may not persist extractions on accounts with persistence off. If so, sync extraction with a local file upload might create no stored artifacts at all. Ask engineering (E6).
- **A dedicated account sidesteps all of this.** A CI-only Sensible account makes artifacts a non-issue (see Q2).

---

## Honest take on Bluehawk (unchanged conclusion, updated reasoning)

Bluehawk solves "runnable source file is the truth, strip scaffolding, include snippets into docs." Your examples are declarative data with an identical harness for every test, so there's no scaffolding to strip. ReadMe can't include files, so "stitch back" would mean a bot rewriting markdown that ReadMe users also edit.

Now that HTML-comment annotations are confirmed safe (D1), they give you the explicit, deterministic extraction Bluehawk markers would have, without moving the source of truth out of the markdown. **Revisit Bluehawk (or extract-to-files) only in the fix-PR phase,** if editing markdown in place proves too fragile.

---

## Architecture

```
docs/**/*.md
   │
   ▼
extract_examples.py ─► examples.json   (reads <!-- test --> wrappers + <!-- example ... --> role markers)
   │                    also: coverage.md (un-annotated **Config** blocks)
   ▼
run_examples.py  (standalone; optionally invoked per test by Doc Detective runShell)
  per example:
    1. URL check   GET → 200, non-empty, content-type plausible; annotation URL == visible link
    2. Parse       JSON5 → strict JSON            fail category: DOCS_MALFORMED
    3. Upload      PUT config, publish_as=development   fail: CONFIG_INVALID
    4. Extract     POST extract_from_url/{type}/{testId}, poll GET /documents/{id}
                   stop early on FAILED            fail: EXTRACTION_ERROR
    5. Compare     parsed_document vs Output per `compare` mode   fail: OUTPUT_DRIFT
   │
   ▼
report ─► JUnit + JSON + $GITHUB_STEP_SUMMARY
       ─► one standing GitHub issue: create / update / close when green
          (reuse scripts/sdk_check/check_sdk_readme.py pattern, or the Doc Detective Action's create_issue_on_fail)
```

### Comparison modes

| Mode | Passes when | Use for |
|---|---|---|
| `exact` | Deep-equal after normalization | Rarely |
| **`subset`** (default) | Every key/value in the docs Output exists in the actual output. Extra actual fields are OK. **Arrays are positional and length-checked.** `null` is a real value | Layout-based examples |
| `keys-and-types` | Same field IDs and `type`s, non-null where the docs show non-null | Early LLM coverage |
| `tolerance` (Phase 3) | Per-field rules: numeric ±, string similarity threshold, set membership, "non-empty" | LLM acceptable variation (D3) |

Normalization: key order, whitespace, float precision.

### Triggers

- `workflow_dispatch`
- `schedule`: weekly
- Later: `pull_request` on annotated pages, running only the changed tests. For PRs, rewrite `/v0/` asset URLs to the PR head SHA.

---

## POC: experiments on the playground topic

Run in order. Each one answers a question the design depends on.

| # | Experiment | Answers |
|---|---|---|
| E1 | Annotate the Row example (option A). `extract_examples.py --file draft-getting-started-ai.md` emits a one-entry manifest | Does the annotation grammar extract deterministically? JSON5 handling of the trailing comma and comments |
| E2 | Run Doc Detective locally on the page (`npx doc-detective --input docs/welcome/draft-getting-started-ai.md --dry-run`, then for real) | Does Doc Detective ignore the `<!-- example ... -->` markers? What does default `detectSteps` pick up? Do the hello-world and Row tests coexist? |
| E3 | Add a multi-line `<!-- step ... -->` | Are multi-line statements OK? (The docs say no, the regex says yes) |
| E4 | A throwaway Doc Detective `httpRequest` with `null` in the expected body | Confirms the null crash and how it surfaces. Documents *why* we don't use it |
| E5 | PUT the Row config with comments left in vs. stripped | Does the API accept JSON5 in the stringified config? |
| E6 | Sync vs. async extraction, then check `GET /extractions` | Which paths persist artifacts? |
| E7 | Local green run of `run_examples.py` for the Row test | End-to-end happy path |
| E8 | Intentional reds: bad URL, `"Javascript"` → `"Java"` in Output, invalid method id, visible link ≠ annotation URL | Each lands in the right failure category |
| E9 | `workflow_dispatch` workflow + issue reporting (create → update → auto-close) | CI plumbing and notifications |
| E10 | (Optional) Doc Detective `runShell` step invoking the runner for `row_two_tables` | Is Doc Detective orchestration worth it versus the runner standalone? |

Exit criterion: E7 green, E8 correctly classified, and E9 opens and closes an issue.

---

## Dimensions to keep in view

1. **Is it a docs bug or a product regression?** Output drift can be an intended engine change, a regression, or a docs error. The weekly run is a **regression canary for engineering**. That's also why fix-PRs must be human-reviewed: auto-updating Output blocks can codify a regression.
2. **Alert fatigue.** Flaky or nondeterministic tests get the issue ignored. Retry transient API errors once, and report `EXTRACTION_ERROR` separately from `OUTPUT_DRIFT`.
3. **Annotation noise in the source.** About 5–7 comment lines per example across 64 pages. That's invisible on the site, but it affects authoring and ReadMe-editor users. Keep the grammar minimal.
4. **The json5-commenter skill injects comments into configs.** That's fine because the runner parses JSON5. Also confirm the skill doesn't touch or reorder the `<!-- example ... -->` markers.
5. **Screenshots drift too.** `row.png` shows the output, and this harness can't detect a stale image. Out of scope.
6. **Fragments and conceptual snippets.** Some Config blocks aren't runnable alone. Those just don't get annotated, or get `skip` with a reason. The coverage report lists them honestly.
7. **Scope beyond SenseML.** SDK guides, integration guides and API-reference examples are also runnable. Keep `examples.json` generic (`kind: senseml-example`), but only build that kind now.

---

## Secrets and keys

| Secret | Needed for | Status |
|---|---|---|
| `SENSIBLE_API_KEY` | Config upload and extraction | Not in this repo's Actions secrets (`gh secret list`). You'll add it or confirm it's set at the org level (Q4) |
| `GITHUB_TOKEN` | Issues | Built in. The workflow needs `permissions: issues: write` |
| `SLACK_WEBHOOK_URL` | Optional Slack notification | Doesn't exist |
| `ANTHROPIC_API_KEY` | Fix-PR phase | Exists |
| `GITHUB_TOKEN` with `contents: write`, `pull-requests: write` | Fix-PR phase | Built in, needs workflow permissions |

---

## Phases

1. **POC:** experiments E1–E10 on the playground topic.
2. **Deterministic coverage:** annotate layout-based examples across `docs/Senseml reference/`, run the coverage report, weekly cron, and triage the first-run failures (expect a real docs-fix backlog).
3. **LLM examples:** define `tolerance` rules per field (D3) and annotate the 3 LLM pages.
4. **Proposed fixes:** on drift, a Claude-powered job opens a PR updating the Output block or config, with the diff and reasoning. Always human-reviewed, never auto-merged. Reconsider extract-to-files or Bluehawk here.

---

## Open questions

Answered and moved to Decisions: old Q1 (D1), Q2 cost (D4), Q8 (D5), Q9 (D6). Q7 (LLM examples) is partly answered by D3.

2. **Account:** which Sensible account should CI run against? A CI-only account would also solve artifact clutter.
3. **Doc type and artifacts (TBD):** may the runner create and overwrite a `docs_examples_ci` document type? What's the policy for accumulated extractions and config versions? See "Test artifacts" and E6.
4. **Secret:** add `SENSIBLE_API_KEY` to repo Actions secrets, or confirm it's at the org level.
5. **Comparison default:** is `subset` (positional arrays, `null` as a real value) right? Are there examples where the Output block is *intentionally* not what the config produces?
6. **Notifications:** only you, or engineering too when the failure looks like engine drift? GitHub issue only, or Slack too?
7. **LLM variation (Phase 3):** which kinds of variation are acceptable? Numeric tolerance, wording differences, extra or missing optional fields?
10. **Doc Detective's role:** annotation syntax only (it never runs), or also run it in CI for `checkLink` plus orchestration via `runShell`? This affects whether to use its GitHub Action for issues or the existing `sdk_check` pattern.
11. **Annotation grammar:** is option A OK? Any naming preference for the role markers (`example config` vs `senseml config` vs something else)?
