# API contract tests with Doc Detective: concept

Status: concept. This is an alternative way to build [contract-tests.md](contract-tests.md), using Doc Detective as
the test runner instead of a custom Python suite. It reuses that proposal's test account design (fixtures, seed
script, coverage matrix) unchanged.

Sources: Doc Detective's [Generate requests from OpenAPI](https://docs.doc-detective.com/docs/test-docs/generate-tests-from-openapi),
[Test HTTP and APIs](https://docs.doc-detective.com/docs/test-docs/http-and-api),
[`httpRequest`](https://docs.doc-detective.com/docs/actions/httprequest), and the
[`openApi`](https://docs.doc-detective.com/reference/schemas/openapi) and
[`retry`](https://docs.doc-detective.com/reference/schemas/retry) references, read 2026-10-13. Coverage and snapshot
behavior was checked against the full docs index (`https://docs.doc-detective.com/docs/llms.txt`), the config
reference, and the `doc-detective/doc-detective` source and ADRs. Nothing here has been
run yet. Items marked **verify** are assumptions to check on the first run.

## Why it might be simpler

Doc Detective already does most of what the custom suite would hand-build:

| Need | Doc Detective feature |
| --- | --- |
| Build the request from the spec | `httpRequest.openApi` with an `operationId`. The method, URL, and path come from the spec, and path params fill from `request.parameters`. |
| Validate request and response against the spec | `validateAgainstSchema`, which **defaults to `both`**. A mismatch fails the step. |
| Check status codes | `statusCodes` (default `[200, 201]`) or `openApi.statusCode`, which also picks the response schema to validate against |
| Auth | `openApi.headers: { "Authorization": "Bearer $SENSIBLE_TEST_API_KEY" }`. `$VAR` is substituted from the environment at run time. |
| Chain calls (create, then retrieve) | Step-level `variables`, for example `"EXTRACTION_ID": "$$response.body.id"`, then `$EXTRACTION_ID` in later steps |
| Poll async extractions | A step `onFail` handler with `retry: { limit, delay, backoff }` on the retrieve step, plus a `response.body` expectation such as `{ "status": "COMPLETE" }` |
| Uploads the HTTP step can't express | `runShell` running `curl -T file.pdf "$UPLOAD_URL"` |
| Require fields without pinning values | `response.required: ["id", "validation_summary.fields"]` |
| Save responses | `path` and `directory` on the step. `maxVariation` and `overwrite` give text-based snapshot comparison. |
| Use spec examples as test data | `useExample: "request" \| "response" \| "both"` and `exampleKey` |

The tests are JSON or YAML spec files, so you maintain test *data* and Doc Detective maintains the runner. (The custom design's YAML catalog is also data. What differs is who owns the runner.)

## What it doesn't do

Each gap below is something the custom proposal treats as essential:

1. **It doesn't generate a suite from the spec.** "Generate requests from OpenAPI" means one step per operation, built
   from its `operationId`. You still write a step for every scenario. Each step is short, but coverage is only as good
   as the steps you write.
2. **Schema validation isn't strict.** Validation follows the spec as written, and most of our object schemas don't
   set `additionalProperties`, so JSON Schema allows extra fields. **A new or renamed field passes.** In the source,
   both request and response validation compile the operation's schema with Ajv (`strictSchema: false`,
   `allErrors: true`, `coerceTypes: false`). Nothing tightens it. `allowAdditionalFields: false` doesn't help: it
   checks against the fields declared in the step's `response.body`, not against the spec. It also silently did
   nothing until a fix in mid-2026 (ADR 01012, 2026-06-30), so pin a Doc Detective version from after that if you use
   it.
3. **It only tests documented status codes if you ask for them.** A step accepts whatever `statusCodes` lists, so a
   documented code that the API can never return is only caught if a scenario tries to trigger it. **Verify** what
   happens when the live response code has no schema in the spec.
4. **No observed-field coverage or shape snapshots.** Checked against the docs index, the reference schemas, and the
   source on 2026-10-13:
   - **Coverage**: Doc Detective once had a `runCoverage` command, but it measured *documentation* coverage (how much
     doc markup such as UI text, links, and code blocks had tests), not API operations or response fields. It was
     removed in v3 (ADR 00103, 2025-04-10: "coverage measurement and test suggestion are no longer available"). The
     `coverageResults-<timestamp>.html` filename on the current reporters page is a leftover from it.
   - **Snapshots**: saving a response with `path` and setting `maxVariation` compares the raw text against the saved
     file with a character-level Levenshtein distance divided by length (`calculateFractionalDifference`). It
     compares *values*, not structure, and exceeding the threshold is only a WARNING. IDs, timestamps, and LLM output
     change every run, so it's noisy or needs a threshold loose enough to hide real changes. Levenshtein is also
     quadratic in response size, which could be slow on large extraction responses with `text` or
     `parsed_document`.
5. **It doesn't read security schemes.** You set the `Authorization` header yourself. This is a one-line config entry.
6. **Binary request bodies are unclear.** `request.body` is a string or JSON. Sending a raw PDF to `/extract`
   or uploading to an `upload_url` probably needs `runShell` and curl (**verify**).
7. **Our specs have few examples.** Only 3 of 41 operations have request-body examples, and 3 have response examples,
   so `useExample` has little to work with today. Steps will mostly set `request.body` and `request.parameters`
   explicitly from the fixtures.

## Design: Doc Detective plus two small scripts

Use Doc Detective as the runner, and close gaps 2 and 4 with a pre-run script and a post-run script. Together they're
a fraction of the custom suite.

```
tests/api-contract/
  .doc-detective.json          # registers the four specs (strict copies) and the auth header
  specs/
    extraction.spec.json       # one test per scenario, steps reference operationIds
    configuration.spec.json
    classification.spec.json
    email.spec.json
  strictify.mjs                # pre-run: reference/*.json -> build/strict/*.json
  report.mjs                   # post-run: saved responses -> fixture gaps + shape diff
  build/                       # gitignored: strict specs, saved responses, Doc Detective results
```

Fixtures, `seed.py`, and `seed.py --check` stay exactly as described in
[contract-tests.md](contract-tests.md#test-account-rich-reproducible-data). Seeding needs idempotent create-or-update
logic and file uploads, and that's easier in a script than in declarative steps.

### Pre-run: strict copies of the specs

`strictify.mjs` reads each `reference/openapi_*.json` and writes a copy in which every object schema that doesn't
set `additionalProperties` gets `additionalProperties: false`. Doc Detective loads the strict copies, so
undocumented fields fail schema validation (closes gap 2). The real specs aren't modified.

### Config

```json
{
  "input": "tests/api-contract/specs",
  "integrations": {
    "openApi": [
      { "name": "extraction",     "descriptionPath": "tests/api-contract/build/strict/openapi_extraction.json",
        "headers": { "Authorization": "Bearer $SENSIBLE_TEST_API_KEY" } },
      { "name": "configuration",  "descriptionPath": "tests/api-contract/build/strict/openapi_configuration.json",
        "headers": { "Authorization": "Bearer $SENSIBLE_TEST_API_KEY" } },
      { "name": "classification", "descriptionPath": "tests/api-contract/build/strict/openapi_classification.json",
        "headers": { "Authorization": "Bearer $SENSIBLE_TEST_API_KEY" } },
      { "name": "email",          "descriptionPath": "tests/api-contract/build/strict/openapi_email.json",
        "headers": { "Authorization": "Bearer $SENSIBLE_TEST_API_KEY" } }
    ]
  }
}
```

Use the named form (`{ "name": "extraction", "operationId": ... }`) in steps, not the string shorthand: the shorthand
takes the first matching `operationId` across all registered specs.

**Verify** whether config-level `headers` apply when a step references the spec by `name`. The docs show headers at
both levels.

### Example test: async extraction from URL

```json
{
  "tests": [
    {
      "testId": "extract-from-url-single-doc",
      "steps": [
        {
          "description": "Start an async extraction from a document URL.",
          "httpRequest": {
            "openApi": { "name": "extraction", "operationId": "extract-from-url" },
            "request": {
              "parameters": { "document_type": "probe_w2s", "environment": "production" },
              "body": {
                "document_url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/postprocessor.pdf",
                "extra_data": { "applicant_id": "A-123" }
              }
            },
            "statusCodes": [200]
          },
          "variables": { "EXTRACTION_ID": "$$response.body.id" }
        },
        {
          "description": "Poll until the extraction finishes, then validate the full response.",
          "httpRequest": {
            "openApi": { "name": "extraction", "operationId": "retrieving-results" },
            "request": { "parameters": { "id": "$EXTRACTION_ID" } },
            "response": { "body": { "status": "COMPLETE" } },
            "path": "extract-from-url-single-doc.retrieve.json",
            "directory": "tests/api-contract/build/responses",
            "overwrite": "true"
          },
          "onFail": [ { "retry": { "limit": 36, "delay": 5000, "backoff": "fixed" } } ]
        }
      ]
    }
  ]
}
```

**Verify** three things:
- Whether `request.parameters` fills both path and query params, and how it decides which is which.
- The exact `onFail` syntax: an array of routing entries.
- That `overwrite` is the string `"true"`. The schema lists accepted values `true`, `false`, and `aboveVariation`.

### Example test: documented error code

```json
{
  "testId": "extract-from-url-missing-body",
  "steps": [
    {
      "httpRequest": {
        "openApi": { "name": "extraction", "operationId": "extract-from-url", "statusCode": 400 },
        "request": { "parameters": { "document_type": "probe_w2s" }, "body": {} }
      }
    }
  ]
}
```

Setting `openApi.statusCode` makes Doc Detective accept that code and validate the body against that code's response
schema.

### Post-run: coverage and shape

Every step saves its response under `build/responses/` (`path` and `directory`). `report.mjs` then reads those files
and the strict specs, and writes `build/report.md`:

- **Operation coverage**: spec `operationId`s that no step references. A `jq` over the spec files and test files
  is enough.
- **Fixture gaps**: response paths the spec documents that no saved response contains (closes gap 4).
- **Shape diff**: each response reduced to JSON paths and types, compared with the last committed shape snapshot
  (closes gap 4).

Doc Detective's own results give PASS or FAIL per step, with schema errors. The report adds what Doc Detective doesn't
measure.

### Running it

- **Locally**: `node tests/api-contract/strictify.mjs && npx doc-detective --config tests/api-contract/.doc-detective.json
  && node tests/api-contract/report.mjs`, with `SENSIBLE_TEST_API_KEY` set to the test account's key.
- **GitHub Actions**: `workflow_dispatch` and an optional weekly `schedule`, with
  `SENSIBLE_TEST_API_KEY: ${{ secrets.SENSIBLE_TEST_API_KEY }}`. Run `seed.py --check` first.

### Keep the key out of artifacts

This repo is public, and workflow artifacts can be downloaded. Before uploading Doc Detective's results as an artifact,
**verify** whether its reports include resolved request headers. If they do, the `Authorization` header contains the
real key. Redact the reports or don't upload them, and never upload raw results without checking. Saved response
bodies don't contain the key.

## Bonus: test the examples in the docs

Two Doc Detective features apply to the published docs, not just the specs:

- **Spec examples become tests.** If you add request examples to the specs and seed fixtures whose names match them
  (for example, the document type an example uses), steps with `useExample: "request"` send the published example
  exactly as written. A broken example in the API reference then fails a test. That also fixes gap 7 over time.
- **Detected tests in Markdown.** Doc Detective can detect steps in doc source files. Its default Markdown patterns
  include HTTP request code blocks. Pointing it at `docs/` could test curl samples in guides. This is a separate project,
  but it's the same tool and the same test account.

## Doc Detective or the custom suite

| | Doc Detective (this doc) | Custom Python ([contract-tests.md](contract-tests.md)) |
| --- | --- | --- |
| Getting started | Config plus JSON steps; no framework code | Write the runner, validator, and polling yourself |
| Schema validation | Built in (request and response); strict mode needs `strictify.mjs` | `openapi-core` plus strict rewrite |
| Async polling | `onFail` retry | Code |
| File uploads | `runShell` and curl | Code |
| Coverage, fixture gaps, shape diff | `report.mjs` over saved responses | Built into the runner |
| Request-side drift (sent fields not in spec) | Built in (`validateAgainstSchema` includes the request) | Code |
| Test docs examples and curl blocks | Yes, same tool | No |
| Debugging failures | Through Doc Detective's output | Your own code, full control |
| Risk | Depends on a younger tool's OpenAPI features; several **verify** items | More code to own |

**What the runner actually saves.** Either way you write the fixtures, `seed.py`, the strict-spec pass, and the
coverage and shape report. Those are most of the work, and they're the same in both designs. What Doc Detective
replaces is the remaining runner: building a request from an `operationId`, calling the validator, a polling loop,
and passing IDs between steps. In a custom script that's a few hundred lines on top of a library such as
`openapi-core`. So the saving is real but modest.

Not an advantage: declarative tests. The custom design's request catalog is already YAML scenarios that you edit as
data. In both designs, scenarios are data; the only difference is who maintains the runner that reads them.

Its real advantages:

- **Maintained plumbing.** Request and response validation, CI reporters (`junit`, `html`, `json`, `runFolder`), and
  a fail-the-build switch (`exitOnFail`) come with the tool.
- **One tool for docs testing.** This is the advantage the custom suite can't match. The same tool, config, and test
  account can later test curl samples in `docs/` (detected tests) and the request examples in the specs
  (`useExample`).

Its costs:

- **Unknowns.** The **verify** items above (raw uploads, how parameters are placed, whether reports include the
  `Authorization` header) are all known quantities in your own code.
- **A moving target.** The CLI self-updates on startup by default (`autoUpdate: true` in the config reference), and
  its behavior has changed recently: `allowAdditionalFields` was fixed in mid-2026, and coverage was removed in v3.
  Pin a version and set `autoUpdate: false`, or a run can change behavior without any change on your side.
- **Two toolchains.** Doc Detective is Node. The seed script and the existing prober are Python. Either accept both,
  or write the scripts in Node.
- **Debugging.** When a step fails, you debug through Doc Detective's output instead of your own code.

**Recommendation:** if you want Doc Detective for testing the docs themselves (curl samples, spec examples), use it
here too. Contract testing is a good first use, and the second use is nearly free. If contract testing is the only
goal, the custom suite costs about the same to build and has no unknowns. Either way, build the fixtures, seed script,
strict-spec pass, and report first: they carry over to either runner unchanged.

## Plan

1. Fixtures and `seed.py` from [contract-tests.md](contract-tests.md) (unchanged, and needed by either runner).
2. Spike: one config, `strictify.mjs`, and the async extraction test above. Resolve every **verify** item.
3. Write tests for each operation in `openapi_extraction.json`, including error codes. Add `report.mjs`.
4. Extend to the other three specs.
5. Add the GitHub Actions workflow with artifact redaction.
6. Optional: add request examples to the specs and switch matching steps to `useExample`.
