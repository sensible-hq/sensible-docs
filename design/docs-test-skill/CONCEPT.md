# Concept: a skill that adds tests for new doc claims

Status: draft · 2026-10-13 · session `doc-detective` · branch `doc-test-skill`

## The idea

When a skill writes or changes a doc, it also adds tests for the doc's **testable claims**. It uses judgment: not every claim can be tested realistically, and a test that can't fail, or that fails at random, is worse than no test. The doc-writing skills call this skill as a step near their end instead of each one inventing its own testing.

Working name: **`add-doc-tests`**.

It builds on two pieces of existing work:
- **The docs-test tooling on PR #737** (`scripts/doc-detective/`):
  - UI tests: Doc Detective inline `<!-- test -->` and `<!-- step -->` comments;
  - code tests: `<!-- code test -->` with `example document`, `example config` and `example output` markers, run by `code_tests.py`;
  - the LLM judge, regression envelopes, `run.sh`, and the HTML report.
- **The API drift and contract-test design on PR #744** (`design/`), which this concept reuses for API changes rather than redesigning.

---

## What Doc Detective recommends (research 2026-10-13)

Sources: Doc Detective's docs (`docs.doc-detective.com`, indexed by `/docs/llms.txt`) and its **agent-tools** plugin (`github.com/doc-detective/agent-tools`). That plugin ships Claude Code skills, a specialist subagent, hooks, an MCP server and an LSP server for writing tests with AI. **Finding:** the official docs have no best-practices page for designing tests. Most of the judgment guidance is in agent-tools.

**Adopt:**
- **Test promises, not the product.** Each testable claim is a *procedure* with an action, a context and an expected outcome. "Testing exhaustively" is listed as an anti-pattern: "Test documentation's promises, not everything about the product" (agent-tools specialist agent).
- **One test per distinct procedure,** where every step is an assertion ("Each individual step acts as an assertion", *How testing works*).
- **Selectors:** literal visible text first, then `data-testid`, then stable IDs; avoid CSS paths, "so tests mirror what a real user does". `elementText` matches the **whole** element; use `/regex/` for a partial match (*find*).
- **Waits:** "Wait for a condition rather than for a fixed time". Raise the step's `timeout` instead of adding `wait`; a fixed wait "is either too short (still flaky) or too long (slow)" (*Troubleshooting*).
- **Code:**
  - use `runCode` for multi-line snippets (javascript, python, bash only), `runShell` for one-liners;
  - assert on the exit code **and** on `stdio` ("A command that exits cleanly can still print the wrong thing");
  - mark fences that must not run with `testIgnore` (*Run shell and code*, *Markdown input format*).
- **Volatile output:** put dynamic fields in `response.required`, not `response.body`; don't assert timestamps or paths; use committed fixtures (*HTTP and API*, agent-tools heuristics).
- **Inline tests** "for small tests that you want to keep close to the content … You update them alongside the content". **All test and step comments must be on a single line** (*Inline tests*).
- **With explicit inline steps,** set `detectSteps: false`, which is what `.doc-detective.json` already does (agent-tools inject skill).
- **The agent workflow:**
  - validate the spec, then **confirm with a real run**, because a spec can pass the validator and still fail at runtime;
  - show a **preview diff** before injecting tests into a page;
  - use a **fix loop capped at 3 tries**, after which the test is marked "needs manual review" (agent-tools generate, doc-testing and fix references).
- **AI-judged checks:** tests are ranked deterministic > grounded probabilistic > ungrounded, and **CI gates use only deterministic tests**. For an AI judge: structured output, temperature 0, confidence zones (auto-pass ≥ 90%, human review 31–89%, auto-fail ≤ 30%). "AI should report what it observed, not what it expected."
- **Hook:** agent-tools has a PostToolUse hook (`post-edit-warn-inline-tests`) that warns, after any edit to a page with inline tests, that the tests "may need updating". Worth copying for this repo.

**Where its guidance doesn't fit us:**
- **Its testability scoring skips reference material:** reference tables score 15%, which falls in "skip", and its first scan ignores API specifications. For Sensible, **parameter tables and the API reference are high-value claims**, so this skill needs its own rubric for them (below).
- **Visual regression:** screenshot comparison (`maxVariation`, for example 0.05) only reports **WARNING** when drift exceeds it, "a signal to review rather than a hard break". Keep screenshots out of scope.
- **The CLI exits 0 on failure** unless you pass `--exit-on-fail`. `run.sh` already handles this.
- **Nothing on cost budgets or changed-files-only runs.** We decide both ourselves.

**Use agent-tools directly, or write our own skill?** Write our own, and borrow its patterns. Its generator targets generic procedures, skips reference material, and doesn't know our code-test markup, the LLM judge, envelopes or the test account. Worth trying: **its LSP server** (schema diagnostics inside inline tests while editing) and **its post-edit hook**.

---

## What the skill does

1. **Find the claims.** Read the new or changed text, using the diff for an update, and list each concrete claim a reader would act on. Examples:
   - "Click **New document type**";
   - "this config outputs `{...}`";
   - "`position`: `right`, `left`. Default: `right`";
   - "returns `400` if …".
2. **Triage each claim** with the rubric below: **test**, **test later**, or **don't test**. Write down the reason for every claim that isn't tested.
3. **Write the tests** in the form that matches the surface (UI, code, SenseML reference, API). Follow the tooling's conventions (README on #737).
4. **Validate, then prove each test can fail.** Run `--check-syntax` (and Doc Detective's spec validation for UI tests). Before keeping a test, make it fail once on purpose: a wrong value, a wrong selector, a broken link. Then confirm it passes on the real page. A test that's never been seen to fail isn't kept. This answers the "a test that can't fail" failure mode from *Docs as Test*.
5. **Run it.** Use `run.sh <page>` for UI and code tests, or `--check-syntax` when there are no keys or network.
6. **Fix loop, capped.** If a new test fails on the real page, decide whether the *doc* or the *test* is wrong. Fix the test at most 3 times. Never "fix" a doc claim to make a test pass without flagging it. After 3 tries, mark it "needs manual review".
7. **Preview, then report:** show the markup diff before writing it into the page. Then post a claims table in the PR description: what's tested, how, what isn't, and why.

## Triage rubric: what to test

Test a claim when **all** of these hold:

| Question | Why |
|---|---|
| Is it **concrete and checkable**? (a value, a label, a status code, an output) | Vague claims ("easy", "fast", "accurate") can't fail |
| Would a reader **act on it**, so being wrong costs them? | Prioritizes procedures, examples, parameter values |
| Can it be checked **with the test account and the public API or app**? | No customer data, no private systems |
| Is the result **stable**, or can its variation be described (`...`, the LLM judge, envelopes)? | Flaky tests get ignored |
| Is the **cost** acceptable? (extractions, LLM calls, run time) | About 1 extraction per code test per run |

**Don't test** (write down the reason instead):
- marketing or comparative claims;
- claims about other products;
- timing and performance;
- anything that needs a paid plan, an admin role, a third-party account (QuickBooks, Zapier), or customer data;
- screenshots (a test can't detect a stale image);
- one-time or destructive operations (deleting account data);
- UI steps that change shared state, unless there's cleanup.

**Test later:** testable in principle, but blocked on something: fixtures, a test-account setting, a tooling feature (for example API contract tests until #744 lands). Add these to the checklist with the blocker.

---

## By surface

### 1. UI changes (procedures in the Sensible app)

- **Form:** Doc Detective inline `<!-- test -->` and `<!-- step -->` comments, one action per step, each with a `description`. Sign in with the docs test account (`$SENSIBLE_TEST_EMAIL`, `$SENSIBLE_TEST_PASSWORD`).
- **Test the claims the procedure makes:**
  - the named button or tab exists, found by its **text** (`elementText`), since the doc names it;
  - each step leads where the doc says, so `find` something only that destination shows;
  - default values the doc mentions.
- **Selectors:** prefer the visible text the doc quotes (`elementText`, a whole-element match), which tests the claim itself and matches Doc Detective's guidance. Fall back to `data-testid`, `aria` or a stable ID; avoid CSS paths.
- **Waits:** wait for an element that proves the page loaded (`waitUntil.find`), not a fixed delay.
- **State:** procedures that create things (a document type, a config) need cleanup (`after` or `afterAll`), or must target throwaway names. The test account is shared by every run.
- **Proving it can fail:** point a step at a misspelled label once; it must fail.
- **Skip:** screenshots (Doc Detective can capture and compare them, but comparisons drift with every UI tweak; see the research section); multi-account and role flows; billing.

### 2. Code changes (code samples: SDK snippets, curl, scripts)

- **Form:** `runCode` (multi-line Python, JavaScript or bash) or `runShell` (one-liners such as `curl`) steps that run the snippet as the doc shows it, with `$SENSIBLE_TEST_API_KEY` substituted. Mark fences that shouldn't run with `testIgnore`. Assert on the exit code **and on content:** a 200 alone is "necessary but insufficient".
- **What to test:**
  - the snippet runs as written (imports, method names, arguments);
  - it produces the output the doc shows, with the same comparison rules as code tests (`...`, required keys);
  - pinned SDK versions match what the doc says to install.
- **Snippets that aren't runnable on their own** (fragments, placeholders like `YOUR_API_KEY`): have the skill write a small harness around them, or mark them **don't test** with the reason. Never edit the visible snippet to make it testable.
- **Secrets:** keys only through environment variables, never in the page. `run.sh` scrubs reports.

### 3. SenseML reference changes (examples and parameter tables)

Two different kinds of claim.

**a. Examples** (config + example document + output): use the existing **code test** markup. This is what the tooling on #737 does. The skill adds the markers around the example the doc-writing skill produced (`create-docs-example` already runs a real extraction to get the output).

**b. Parameter tables.** Each row claims a name, whether it's required, a type or allowed values, a default, and a behavior. These need different checks:

| Claim in the row | Check | Deterministic? | Cost |
|---|---|---|---|
| The parameter exists, and its name is right | Look it up in the public SenseML JSON Schema (`schema.sensible.so/configuration.schema.json`) for that method | yes | none |
| Required or optional | The schema's `required` list | yes | none |
| Type and allowed values (`right`, `left`) | The schema's `type` and `enum` | yes | none |
| Each documented value is accepted | Upload a config using each value with `publish_as: development`, which validates it | yes | config uploads, no extractions |
| The default (`default: right`) | **The schema has no defaults** (0 of its properties declare one). Behavioral check: the example config without the parameter and with it set to the default must give identical output | yes | 2 extractions per default |
| The behavior described | A code test example that shows the effect, ideally two outputs that differ when the value changes | depends on the method | 1–2 extractions |

- **Also catches gaps:** schema parameters the table doesn't document, after excluding global parameters, which are read from `method.md`'s own table. (Row's 12 schema parameters are fully covered: 4 in `row.md`, 8 global ones in `method.md`.)

**Decision: how parameter tables are marked up (2026-10-14).** Neither per-row inline tests nor separate spec files:

| Check | Markup | Why |
|---|---|---|
| Schema checks: names, required, types, allowed values, defaults that the schema would reject, gaps | **None.** The table's `id` row (for example `` `row` ``) names the schema definition | The table is the claim, so parsing it tests exactly what readers see and can't drift. It runs over every reference page with no page edits, like a linter |
| Each documented value is accepted | None: built from the table | Config uploads only |
| Defaults and described behavior (costs extractions) | **One comment above the table**, naming the page's code-test example and the rows to check, for example `<!-- param tests {"example": "row_two_tables", "defaults": ["position", "includeAnchor"]} -->` | Opt-in per row, because it costs extractions. It sits next to the table, as Doc Detective recommends for inline tests |

Not per-row comments: a comment inside a Markdown table breaks the table, and there are a few hundred rows. Not spec files: these checks aren't Doc Detective actions, and a sidecar would repeat every parameter name and drift ("harder to maintain strict parallelism with documentation", Doc Detective). *Not yet verified: how ReadMe renders a comment directly above a table; keep a blank line between them.*

**Prototype (2026-10-14): `scripts/param-tables/check_param_tables.py`.** No dependencies, no markup, reads the public schema. `--all` checks every page under `docs/Senseml reference/`.
- **Parses** each `key | value | description` table separately, using that table's `id` row. On `types.md` it prefers type definitions, since types and methods share ids like `paragraph`. It treats "default: none / infinity / no change" as prose.
- **Reads the schema's shapes:** finds definitions defined inline and behind URL-encoded `$ref`s. Merges a method's variants: a parameter is valid if any variant has it, and required only if every variant requires it.
- **Proved it can fail:** 7 broken copies of `row.md` (misspelled name, disallowed value, wrong required flag, wrong type, disallowed default; missing row, unlisted value). The first five fail with exit 1 at the right line, and the last two warn. 18 offline unit tests (`python3 -m unittest discover -s scripts/param-tables`).
- **First full run (31 pages with method tables):** 12 errors, which come down to **6 real docs problems on 5 pages**, each checked by hand against the page and the schema:

  | Page | Problem |
  |---|---|
  | `signature.md` | No row marked required; the schema requires `id`, `start`, `offsetX`, `offsetY`, `width`, `height` |
  | `text-table.md` | The table says `id` is `` `table` ``; the schema and the page's own examples use `textTable` |
  | `query-group.md` | `queries` is required in every schema variant, not marked |
  | `add-computed-fields.md` | `fields` is required, not marked |
  | `get-file-metadata.md` | `type` is required, not marked |

  Plus 17 warnings: schema parameters no table lists, such as `source_id` on several computed-field pages, Query Group's chunking options, and Box's `overlapX`/`overlapY`. **These are leads, not findings.** Some are documented elsewhere or deliberately undocumented; not yet checked.
- **Early versions produced false errors** (one table's `id` applied to the whole page, one variant picked instead of all, "default: none" read as a value, `` `number` `` read as a type word). Each is now a unit test. Expect more page conventions to surface as the tool sees more pages.

### 4. API changes (OpenAPI specs in `reference/`)

**Reuse PR #744; don't redesign it.**
- #744 already has three designs (`design/concept.md`, `contract-tests.md`, `doc-detective-contract-tests.md`) and live pytest contract tests (`scripts/test/probe_endpoints/contract/`). Every test reads its claim from the spec, runs against the test account, and ends with a "docs impact" summary.
- The `api-spec` skill already has testing steps: Step 8 (curl scripts per endpoint), 8b (compare with backend tests), 9 (probe snapshots), 10 (update spec examples from real output).

For API changes, this skill's job is narrower:
1. **For each new or changed claim** (a field, an enum, a status code, a required flag, an example), add or extend a contract test **in #744's suite**, following its conventions: read the claim from the spec, use the test account, print the docs impact.
2. **Claims in prose** (descriptions that promise behavior, such as "returns the current draft"): a named test like #744's `test_pr748_doc_text_claims.py`.
3. **Examples:** validate the spec's request and response examples against the spec's own schemas (strict copies, per #744), which needs no live call.
4. **Out of scope here:** whether the spec matches the backend code (leg 1 in `sessions/api-contract-testing/CONCEPT.md` on #737). That needs the private backend source and doesn't run from this public repo.

---

## Wiring it into the doc skills

The doc-writing skills call `add-doc-tests` as a step **after the page is written and before the commit**, passing the page and the surface. The skill writes the tests into the same branch, so the doc and its tests ship in one PR.

| Skill | Writes | Surface(s) | Hook |
|---|---|---|---|
| `create-new-doc` | new SenseML reference pages | SenseML reference (examples + parameter table) | before Step 5 (branch, commit, PR) |
| `update-existing-doc` | changed pages | whatever changed: diff-scoped | before Step 5 |
| `update-docs-from-pr` | orchestrates the two above | per page | after Step 5 (style check), before Step 6 (commit) |
| `create-concept-doc` | concept topics | mostly prose; examples if any | before Step 4; often all "don't test" |
| `create-docs-example` | example sections from an extractor | SenseML example (code test) | after Step 6 (write example), before Step 7 (commit). It already has a real extraction |
| `api-spec` | OpenAPI specs | API | alongside Steps 8–10: route new claims to #744's suite |
| `blog-how-to-parse-x` | blog drafts (published to Notion) | config + output | optional: it already runs a live extraction and cross-checks output (Steps 4, 6.6). Blogs aren't in this repo's docs tree |
| `blog-short` | blog drafts, no code | — | skip: no testable claims by design |
| `changelog` | monthly changelog | — | skip (as you said) |

Tooling-only skills (`json5-commenter`, `revise-doc-style`, `docs-checker`) don't write claims. They should **preserve** test markup, not add it. *Check that `json5-commenter` and `revise-doc-style` leave `<!-- test -->` and `<!-- example -->` comments alone.*

---

## Open questions

1. **Where tests live:** inline, as today. Doc Detective recommends inline for tests kept close to the content, and standalone spec files only for large suites, noting they make it "harder to maintain strict parallelism with documentation". Revisit if a page's tests grow long.
2. **Budget:** the cost per PR of new tests (extractions, judge calls)? A cap per run?
3. **When tests run:** on every docs PR (`--check-syntax` only), on merge to `v0` (full, as on #737), or weekly?
4. **Defaults:** the SenseML schema has none. Is it worth asking engineering to add `default` to the schema, so default claims become a free deterministic check?
5. **UI state:** a cleanup convention for procedures that create objects in the shared test account?
6. ~~**Global parameters:** a list?~~ Read from `method.md`'s table instead, so no separate list to maintain.
7. **Judge confidence zones:** agent-tools suggests auto-pass ≥ 90%, review 31–89%, auto-fail ≤ 30%; our judge passes at ≥ 70%. Align?

## Next steps

- [x] Fold in the Doc Detective best-practices research (2026-10-13)
- [ ] Try agent-tools' LSP server and copy its post-edit "tests may need updating" hook
- [ ] Merge or settle #737 (tooling) and #744 (API tests), which this skill depends on
- [x] Prototype the parameter-table schema check (`scripts/param-tables/`, 2026-10-14): `row.md` passes; first full run found 6 docs problems on 5 pages
- [ ] Decide whether to fix the 6 parameter-table problems, in a separate docs PR
- [ ] Triage the 17 gap warnings (documented elsewhere, deliberately undocumented, or missing)
- [ ] Add the opt-in behavioral checks (defaults, each value accepted) driven by the `<!-- param tests -->` marker
- [ ] Run the schema check on docs PRs (no secrets, a few seconds)
- [ ] Write the skill (`.claude/skills/add-doc-tests/SKILL.md`) and add its hook to the skills above
- [ ] Check that `json5-commenter` and `revise-doc-style` preserve test markup
