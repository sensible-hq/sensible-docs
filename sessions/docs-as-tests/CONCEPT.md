# Concept: SenseML reference examples as tests

Status: draft for discussion · 2026-09-23 · session `docs-as-tests`

## The idea

Borrowed from LangChain (via *Docs as Test & AI*): treat every code sample in the docs as a test. Run each one in CI on a schedule, and get notified when a sample stops doing what the docs say it does.

For the SenseML reference, an "example" is a unit of three things that already appear in a consistent pattern:

1. **Config**: a fenced `json` block of SenseML
2. **Example document**: a table row holding a download URL for a PDF
3. **Output**: a fenced `json` block showing the `parsed_document` the config produces

The test for each example is the same:

> Does the document URL resolve? Does the config run? Does Sensible's output still match the **Output** block?

**Phase 1 goal:** a weekly GitHub Action that answers that question for every example and opens (or updates) one GitHub issue when any answer is "no."

**Later goal:** propose a fix as a PR.

**POC scope:** the `## Row method example` in `docs/welcome/draft-getting-started-ai.md` on the `doc-detective-poc` branch.

---

## What's actually in the repo (measured, not assumed)

| Fact | Number | Why it matters |
|---|---|---|
| Pages in `docs/Senseml reference/` | 120 | |
| Pages with at least one `**Config**` block | 64 | This is the test surface |
| `**Config**` blocks | 93 (90 fenced as `json`) | Roughly 90 tests |
| `**Output**` blocks | 95 (91 fenced as `json`) | |
| Configs that are **not strict JSON** | 62 of 90 | Canonical `/* */` comments (54) and trailing commas. The runner needs a JSON5 parser. The POC Row config has a trailing comma after `"position": "left",` |
| Outputs that are not strict JSON | 4 | Hand-edited, truncated, or fragments (one Output fence starts with `"computed_fields": [`). These need an annotation or a fix |
| Pages where Config count ≠ Output count | 3 | `conditional.md` (1/0), `custom-computation.md` (2/3), `deprecated-query.md` (2/3). Pairing blocks by order alone will mis-pair on these pages |
| Unique example-doc URLs | 93, all `raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/...` | Easy to check |
| Broken example-doc URLs today | 1: `TBD.pdf` in `draft-jsonschema-postprocessor.md` (404) | A draft, so expected. It shows the check would catch real breakage |
| Non-PDF example docs | 1 `.xlsx` | Check that URL extraction handles it |
| LLM-based method pages with examples | 3 (`nlp-table`, `query-group`, `list`) | Output is **not deterministic**. See Dimensions |

### API facts that shape the design

- **No endpoint extracts with an inline config.** Every extraction runs against a config saved in a document type. The runner therefore has to write each example's config into a dedicated doc type first (`PUT /document_types/{id}/configurations/{name}`), then extract with `configuration_name`.
- **The Python SDK (`sensibleapi`) only extracts and classifies.** It has no config management, so the runner uses the SDK for `extract` + `wait_for` and plain `requests` for the Configuration API. The alternative is to skip the SDK and use `requests` for everything, which gives one fewer dependency and one auth path.
- The Configuration API takes `configuration` as a **stringified** config and "doesn't reject requests with configuration errors" unless you set `publish_as`. Publishing with `publish_as: "development"` forces validation, so an invalid example config fails loudly at upload time. That's the behavior we want.
- **Not verified:** whether the API accepts JSON5 comments inside the stringified config. The SenseML editor tolerates them, but I haven't tested the API. The safe default is to parse with JSON5 and send strict JSON.

---

## Honest take on Bluehawk

The LangChain analogy only half fits, and Bluehawk may be the wrong tool here.

**Why LangChain needed it.** Their samples are *imperative code* against a *fast-moving library*. Each sample needs setup and teardown (imports, clients, fixtures) that you don't want readers to see. Bluehawk's job is to let the **runnable file be the source of truth** while it strips the scaffolding (`:remove-start:`, `:snippet-start:`) out of what lands in the docs.

**Why your case is different:**

1. **There's no scaffolding to hide.** Your examples are *declarative data* (config + doc URL + expected output). The harness is identical for every example (upload config → extract → diff), so it lives once in a Python script and never needs to appear in the docs.
2. **Your structure is already machine-parseable.** `**Config**` / `**Example document**` / `**Output**` is a convention a ~100-line parser can extract deterministically. Bluehawk markup would add annotations for something you already have.
3. **ReadMe has no file-include.** Bluehawk's model is: code files → extracted snippets → *included* into docs at build time. ReadMe markdown can't include a file, so "stitch back" would mean a generator that **rewrites the fenced blocks inside the `.md` files** and commits the result. Your repo round-trips with ReadMe (the `Update doc ...` commits), so anyone who edits a config in the ReadMe UI would edit generated text. The next stitch would overwrite that edit, or the two would conflict.
4. **Not verified:** whether Bluehawk parses markers in `.md` files at all. It keys comment syntax off file extension. I'd need to test this before relying on it.

**Where Bluehawk (or extract-to-files) *does* earn its place:** Phase 3, auto-fix PRs. If configs and expected outputs lived as standalone `examples/<id>/config.json5` + `expected.json` files, a bot could edit those files and regenerate the docs. That's cleaner than a bot doing regex surgery on markdown. It's also a big authoring-workflow change, and it conflicts with ReadMe edits (point 3). Defer it.

**Recommendation:** in Phases 1–2, keep **the markdown as the source of truth**. Extract deterministically from the existing convention, and add HTML-comment annotations *only for exceptions*. Your Doc Detective POC (`50574dfb3`) was testing exactly whether ReadMe preserves HTML comments through sync. That result decides whether annotations are viable at all.

---

## Proposed architecture (Phases 1–2)

```
docs/Senseml reference/**/*.md
        │
        ▼
extract_examples.py ──► examples.json          (deterministic manifest; can be committed or kept as a CI artifact)
        │
        ▼
run_examples.py
  for each example:
    1. URL check     GET doc URL → 200, non-empty, plausible content-type
    2. Parse         JSON5 → strict JSON (fail = "config is malformed in docs")
    3. Upload        PUT config into doc type `docs_examples_ci`, name = example id, publish_as=development
    4. Extract       extract_from_url(..., configuration_name=id, environment=development) + wait_for
    5. Compare       parsed_document vs **Output** block
        │
        ▼
report.py ──► GitHub issue (create / update / close-when-green) + Actions job summary
```

### Extractor

- Walk each page and split it on headings. Inside each example section, grab the `**Config**` fence, the first URL in the `**Example document**` table, and the `**Output**` fence.
- Record the source file and line numbers so the issue can link straight to the line on GitHub.
- **Example IDs:** default to `<page-slug>-<n>`. Position-based IDs break when someone inserts an example above, so let an annotation pin a stable ID.

### Annotations (optional, HTML comments, exceptions only)

```html
<!-- example-test {"id": "row-two-tables"} -->
<!-- example-test {"skip": "LLM output varies; checked manually"} -->
<!-- example-test {"compare": "keys-and-types"} -->
<!-- example-test {"ignore": ["$.some_field.value"]} -->
<!-- example-test {"document": "https://.../other.pdf"} -->
```

Place one directly above the `**Config**` it modifies. If there's no annotation, the defaults apply.

### Comparison semantics (the hardest design decision)

Doc outputs are curated, not raw dumps. Readers see trimmed, sometimes reordered subsets. Options, from strictest to loosest:

| Mode | Passes when | Use for |
|---|---|---|
| `exact` | Deep-equal | Rarely. Too brittle |
| **`subset`** (proposed default) | Every key/value in the docs Output exists in the actual output. Extra actual fields are OK | Most layout-based examples |
| `keys-and-types` | Same field IDs, same `type`, non-null where the docs show non-null | LLM methods |
| `skip` | Always | Fragments and conceptual snippets |

Normalize before comparing: key order, whitespace, float precision.

### Reporting

- Reuse the pattern already in `scripts/sdk_check/check_sdk_readme.py`: one standing issue that gets created or updated, not a new issue every week. Close it automatically when the run goes green.
- For each failure, the issue body includes: page link at line, failure category (URL / parse / upload-validation / extraction error / output drift), a unified diff of expected vs actual, and a SenseML editor deep link to the config in `docs_examples_ci` so you can debug in the app.
- Also write a Markdown table to `$GITHUB_STEP_SUMMARY`.
- Optional: Slack post via webhook.

### Triggers

- `schedule`: weekly (for example, Monday 14:00 UTC)
- `workflow_dispatch`: manual runs
- Later: `pull_request` on `docs/Senseml reference/**`, testing only the pages that changed. Catch: on a PR, a changed PDF only exists on the PR branch, so rewrite `/v0/` URLs to the PR head SHA.

---

## POC plan (Row example only)

1. Create a hand-made `docs_examples_ci` doc type in the Sensible app, or have the script create it idempotently (needs your OK, see Q3).
2. `extract_examples.py` parses **only** `draft-getting-started-ai.md` → one-entry manifest. Confirm it survives the trailing comma and `/* */` comments.
3. `run_examples.py` runs that one entry locally with your `SENSIBLE_API_KEY` and prints pass/fail + diff.
4. Break it on purpose three ways (bad URL, change `"Javascript"` → `"Java"` in Output, invalid method id) and confirm each shows up as the right failure category.
5. Wrap it in `.github/workflows/test-examples.yml` with `workflow_dispatch` only. Add the secret and run it once from Actions.
6. Add issue reporting. Only then add the cron.

Exit criterion: one green run, three correctly classified red runs, and one issue opened and auto-closed.

Side note I found while reading the POC section: the field ID `python_change_in_TIBOE_rating` misspells TIOBE. Fixing it changes the expected output key, so fix it in the Config and Output together.

---

## Dimensions you may not have considered

1. **Is it a docs bug or a product regression?** If output drifts because the Sensible engine changed, the docs aren't wrong; the product changed. Sometimes that's intended, sometimes it's a bug. Your weekly run is effectively a **regression canary for engineering**. Decide who gets the issue (see Q6). This also argues against auto-updating Output blocks (Phase 3), because an auto-update can codify a regression.
2. **Nondeterminism.** LLM methods (3 pages) and possibly OCR-dependent examples won't reproduce byte-for-byte. Without `keys-and-types` or `skip`, they'll fail randomly and people will learn to ignore the issue. Alert fatigue kills these projects.
3. **Flakiness policy.** Transient API errors or timeouts shouldn't page anyone. Proposal: retry each failing example once, and report extraction *errors* separately from output *drift*.
4. **Cost and quota.** About 90 extractions a week ≈ 4,700 a year, and LLM methods cost more per run. Whose account pays, and does this count against a plan limit? (Q2)
5. **Test pollution.** About 90 configs in a doc type in a real account. That's fine if the doc type is clearly named and isolated. Configs get overwritten every run (idempotent PUT), so they don't accumulate, and keeping them lets you open failures in the editor.
6. **Fragments and conceptual snippets.** Some Config blocks aren't runnable on their own (partial `computed_fields`, examples that depend on a preprocessor defined elsewhere). The first full run will surface them. Expect roughly 10–20% to need a `skip` or a small docs fix. That's a useful audit in itself.
7. **Images drift too.** Each example has a screenshot (`row.png`) of the output. This harness can't tell when the screenshot goes stale. Out of scope, but worth knowing about.
8. **Inline comments and the json5-commenter skill.** Canonical comments get injected into configs. That's fine as long as the runner parses JSON5. It's also a reason *not* to move configs into separate files yet, because the commenter operates on markdown.
9. **Doc Detective overlap.** You've already started Doc Detective. It's good at link checks and simple HTTP assertions. For this use case it would need the config and output *duplicated* into the test annotation, since it can't reference the neighboring fenced block. The async extract-then-poll flow is also awkward there (**not verified**: I haven't checked its current polling support). A custom Python runner fits better, and Doc Detective can keep doing links.
10. **Scope creep to other pages.** Integration guides, the Python/Node SDK guides, and API reference examples are also runnable. Design the manifest format generically (`kind: senseml-example`), but only build the SenseML kind now.

---

## Secrets and keys

| Secret | Needed for | Status |
|---|---|---|
| `SENSIBLE_API_KEY` | Uploading configs and running extractions | **Not in this repo's Actions secrets** (`gh secret list` shows only `ANTHROPIC_API_KEY`, `DEV_README_KEY`, `README_API_KEY`, `README_OAS_KEY`, and debug flags). It may exist at the org level, which that command doesn't show. Present in your local env |
| `GITHUB_TOKEN` | Opening and updating issues | Built in. The workflow needs `permissions: issues: write` |
| `SLACK_WEBHOOK_URL` | Optional Slack notification | Doesn't exist. Only needed if you want Slack |
| `ANTHROPIC_API_KEY` | Phase 3 only (Claude proposes fixes) | Already exists |
| `GITHUB_TOKEN` with `contents: write`, `pull-requests: write` | Phase 3 only (bot opens PRs) | Built in, needs workflow permissions |

---

## Phases

1. **POC:** Row example, local and then `workflow_dispatch`, issue reporting.
2. **Coverage:** all SenseML reference pages, annotations for exceptions, weekly cron, triage the first-run failures (expect a real docs-fix backlog).
3. **Proposed fixes:** on drift, a Claude-powered job opens a PR that updates the Output block (or the config), with the diff and reasoning. **Always human-reviewed, never auto-merged**, because of dimension 1. Reconsider extract-to-files or Bluehawk at this point.

---

## Questions for you

1. **HTML comments through ReadMe:** did the Doc Detective POC confirm that ReadMe preserves `<!-- -->` comments round-trip? If not, annotations need another home (for example, a sidecar `examples.overrides.yaml` keyed by page + index).
2. **Account and cost:** which Sensible account should CI run against (a docs account, a dedicated CI account, or yours)? Does about 90 extractions a week matter for billing or quota?
3. **Doc type:** may the script create a `docs_examples_ci` document type and overwrite configs in it, or do you want to create it by hand?
4. **Secret:** can you add `SENSIBLE_API_KEY` to this repo's Actions secrets, or confirm it exists at the org level?
5. **Comparison default:** is `subset` right? Are there examples where the Output block is *intentionally* not what the config produces, for example illustrative edits?
6. **Who gets notified:** only you (issue assigned to you), or also engineering when the failure looks like engine drift rather than docs drift? Where: GitHub issue only, or Slack too?
7. **LLM examples:** in Phase 2, `keys-and-types` or `skip`?
8. **Where the tests run first:** is the `draft-getting-started-ai.md` Row example the real target, or a stand-in? It's a copy of `docs/Senseml reference/layout-based-methods/row.md` (same config, same `TIBOE` typo). If it's a stand-in, the POC could point at the reference page directly and skip the `doc-detective-poc` branch.
9. **Branch strategy:** this work lives on `doc-detective-poc` (PR #725), next to the Doc Detective hello-world test. The Row section in `draft-getting-started-ai.md` is still uncommitted in this worktree. Should the harness test that draft section (commit it first) or `layout-based-methods/row.md` directly?
