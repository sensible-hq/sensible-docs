# API contract tests: proposal

Status: proposal. This is the complement to [concept.md](concept.md): that doc finds drift by reading the backend
source, and this one finds drift by calling the live API.

## Goal

As the API spec maintainer, you can check, on your own schedule, that the live API behaves the way the specs in
`reference/` say it does. You don't need backend access, AWS credentials, or the backend team.

## Summary

Grow the existing prober (`scripts/test/probe_endpoints/`) into a contract test suite:

1. Call **production** (`https://api.sensible.so/v0`) with the dedicated test account. That's the API the docs
   describe, so there's no stage to deploy.
2. **Validate every request and response against the spec** in strict mode. Don't only diff against the previous
   run.
3. Drive the calls from a **request catalog** keyed by `operationId`, so coverage is measurable: every spec operation
   either has a scenario or appears in the coverage gap list.
4. Run it **locally or from a manual/weekly GitHub Actions workflow** in this repo, using the existing
   `SENSIBLE_TEST_API_KEY` secret.

Cost isn't a constraint (on-demand or weekly runs), so the suite can run real extractions, including portfolios and
LLM-based configs.

## Why not reuse the backend's tests

The backend has two suites:

- **Integration tests** (`*.int.ts`): call handlers in-process against local Docker services. They bypass API Gateway
  and need the backend repo and its toolchain.
- **SST smoke tests**: real HTTP against a deployed *ephemeral stage*, covering about 40 API paths. Running them needs
  an ephemeral stage deploy, AWS credentials, stage-keyed secrets, and the backend repo, because the tests import
  backend types. They also check selected fields (`toMatchObject`) rather than full response shape, and they don't run
  in CI.

Reuse their **coverage list** (which endpoints and scenarios matter) as a checklist for the catalog, but don't run them.
Calling production with an API key needs no build, no stage, and no credentials beyond the key.

Why not plain curl scripts: curl is fine for sending requests (the repo already has `curl_script_template.sh`), but
validating a response against an OpenAPI schema needs code. Keep Python and standard-library HTTP like the
current prober, and add a validator.

## Design

### Inputs

| Input | Source |
| --- | --- |
| Specs | `reference/openapi_*.json` from the working tree, so you can test a spec change before merging it |
| API key | `SENSIBLE_TEST_API_KEY` env var, the dedicated test account's key. In Actions, it comes from the repo secret of the same name. |
| Request catalog | `scripts/test/probe_endpoints/catalog/*.yaml`, one file per spec file |
| Test account data | Fixtures in `scripts/test/probe_endpoints/fixtures/` (document types, configs, references, processors) and sample documents in `assets/pdfs/`. See [Test account](#test-account-rich-reproducible-data). |

Use only `SENSIBLE_TEST_API_KEY`. Never fall back to `SENSIBLE_API_KEY` or any other key, and exit with an error if
the test key isn't set. The suite creates and deletes resources, so it must only ever touch the test account. The
existing prober reads `SENSIBLE_API_KEY`; switch it as part of step 2 of the plan.

### Request catalog

One entry per scenario, keyed by the spec's `operationId`:

```yaml
- operation: extract-from-url              # operationId in the spec
  scenario: single-doc-async
  path: { document_type: "api_skill_w2s" }
  query: { environment: production, document_name: drift-probe }
  body:
    document_url: "{{asset:postprocessor.pdf}}"
    extra_data: { applicant_id: "A-123" }
  expect: [200]
  then:                                    # follow-up call that captures the async result
    operation: retrieving-results
    path: { id: "{{response.id}}" }
    poll_until: { status: [COMPLETE, FAILED] }

- operation: extract-from-url
  scenario: missing-required-field
  path: { document_type: "api_skill_w2s" }
  body: {}
  expect: [400]
```

Scenarios to cover per operation, in priority order:

1. **Happy path** for each documented content type (JSON body, raw PDF, and so on).
2. **Conditional shapes**: portfolio as well as single document, `withMetadata`, `extra_data`, and webhooks
   (see [Limitations](#limitations)).
3. **Documented error codes**: for each status code the spec lists, one scenario that triggers it. That includes 400
   for a bad body, 401 for a bad key, 404 for an unknown ID, 415 for a wrong `Content-Type`, and 429 only if it's cheap
   to trigger. A documented code that no scenario can trigger is a finding in itself. sensible-docs#744 removed exactly
   such codes (415 on GET operations).

### Validation (what makes this a contract test)

For each call:

- **Status code**: the spec must document the returned code for that operation.
- **Response body**: validate against the operation's response schema for that code and content type. Use
  `openapi-core` (Python, validates OpenAPI 3.0 directly, handles `$ref` and `nullable`) or `jsonschema` after a small
  OpenAPI-to-JSON-Schema conversion.
- **Strict mode**: before validating, rewrite the spec in memory so every object schema without `additionalProperties`
  gets `additionalProperties: false`. Without this, a new or renamed field passes silently. Report these as
  "undocumented field", separately from type errors.
- **Request body**: validate what the scenario *sent* against the request schema. A field the scenario sends that
  the spec doesn't list is an undocumented parameter. A field the spec marks required that a passing scenario
  didn't send means the spec is wrong.
- **Coverage**: list spec operations, status codes, and content types that no scenario exercised.

Findings use the same severity words as [concept.md](concept.md): **DRIFT** for type errors, undocumented status
codes, and spec-required fields that weren't needed, and **REVIEW** for undocumented optional fields.

### Snapshots (what changed since last run)

Keep snapshots, but store **shapes**, not values: each JSON path with its type (`documents[].output.parsed_document:
object`). Shape snapshots make the `VOLATILE_KEYS` list unnecessary, because IDs and timestamps don't appear in a
shape. A shape diff answers "did the API change since last week?" even where the spec is too loose to catch it
(`additionalProperties: true`, empty object schemas).

### Test account: rich, reproducible data

What the API returns depends on the account's data as much as on the request. Many response fields appear only when
the document and the document type's config trigger them. For example, `validation_summary` needs validations,
`reviewStatuses` needs review triggers, `classification_summary` needs a portfolio with fingerprints,
`postprocessorOutput` needs a postprocessor, and `file_metadata` needs a PDF with metadata. A thin test account
produces responses that pass strict validation only because they're mostly empty. So the test account's data is part
of the test suite. It has to be rich, version-controlled, and rebuildable from scratch.

#### Fixtures in the repo

Everything the suite depends on is checked in as files that map directly to configuration API request bodies:

```
scripts/test/probe_endpoints/fixtures/
  README.md                              # account bootstrap steps that the API can't do (see below)
  manifest.yaml                          # what to seed, in order
  document_types/
    probe_w2s.json                       # body for POST /document_types: name + schema
                                         #   (fingerprint_mode, ocr_engine, review_triggers, validations, ...)
    probe_w2s/
      configs/w2_2024.json               # SenseML; seeded with POST .../configurations, publish_as
      configs/w2_2024.v2.json            # optional second version, so versions endpoints have data
      goldens/w2_sample.yaml             # name, associated configuration, path to the PDF
  processors/
    probe_invoices.json                  # body for PUT /processors/email/{name}
assets/pdfs/                             # sample documents (existing folder, already public)
```

Name long-lived fixtures with a fixed prefix (`probe_`), and name resources that a single run creates and destroys
with `drift_probe_<run-id>_`, so the two never collide.

#### Seed script

`seed.py` rebuilds the account from the fixtures, using only the documented configuration API:

1. **Document types**: create with `POST /document_types`, or update with `PUT /document_types/{id}` if the name
   already exists.
2. **Configs**: create with `POST /document_types/{id}/configurations` and publish with `publish_as`. Seed a second
   version where the manifest asks for one, and publish versions to different environments, so the versions endpoints
   and environment handling have data.
3. **Reference documents (goldens)**: `POST /document_types/{id}/goldens` returns an `upload_url`. Upload the PDF to it
   with a PUT, then associate the configuration.
4. **Email processors**: `PUT /processors/email/{name}`.

It's idempotent (safe to rerun), matches resources by name, and records the name-to-ID map that the request catalog
uses. Two more modes:

- `seed.py --check`: compare the live account with the fixtures, and report anything missing, changed, or extra.
  Run it at the start of every contract run, so an account someone edited by hand doesn't masquerade as API drift.
- `export.py`: pull the current account into fixture files. Use it once to bootstrap from today's test account, and
  again whenever you deliberately change fixtures in the Sensible app instead of in the files.

#### Coverage matrix

Track which fixture triggers which conditional part of the API, and grow it until the observed-field report
(below) is clean:

| Response feature | Fixture that triggers it |
| --- | --- |
| `validations`, `validation_summary` (errors, warnings, skipped) | Config with validations that fail, warn, and skip |
| `reviewStatuses`, review status | Document type with `review_triggers` plus a document that trips them |
| Portfolio: `documents[]`, page ranges, `classification_summary` | Multi-document PDF plus at least two document types with fingerprints |
| `coverage`, field-level `errors` | Config where some fields can't be found |
| `postprocessorOutput` | Config with a postprocessor |
| Computed fields, sections, tables | Config using each |
| LLM-based methods | Config with Query Group and other LLM methods |
| `file_metadata` | PDF with document metadata (open item in the current prober's checklist) |
| `extra_data` | Request scenarios, no fixture needed |
| Content types | One sample each: PDF, scanned PDF, JPEG, PNG, TIFF, DOCX, XLSX, XLSB, CSV |
| Error codes | Password-protected PDF, corrupt PDF, a document no fingerprint matches |
| Email processors | At least one processor per supported setup |

Good sources of fixtures: the existing samples in `assets/pdfs/` and the open-source configuration library, which
already pairs sample documents with configs. Every fixture document must be synthetic or public, because this repo
is public. No real customer data and no real PII.

#### Observed-field coverage

Operation coverage isn't enough. During every run, record each JSON path seen in any response, then compare against
every path in the spec's response schemas. Paths the spec documents but no response ever contained are **fixture
gaps**. That's the measurable version of "the test account is rich enough", and the report lists them after the
coverage gaps.

#### What the API can't recreate

Some account state can't be set through the documented API: creating the account and its API key, account-level
feature settings, and anything set only by Sensible support. List these as manual bootstrap steps in
`fixtures/README.md`. Before relying on a fixture, confirm whether its behavior (for example, human review) needs an
account-level setting. I haven't checked which ones do.

#### Run hygiene

- Run destructive operations (DELETE) only on `drift_probe_<run-id>_` resources created in the same run. Never delete
  `probe_` fixtures.
- A cleanup step at the end of every run, and at the start of the next run, deletes leftover `drift_probe_*`
  resources.

### Running it

- **Locally**: `python3 scripts/test/probe_endpoints/contract.py [--only extraction] [--update-snapshots]`
- **GitHub Actions**: new workflow with `workflow_dispatch` and an optional weekly `schedule`, `SENSIBLE_TEST_API_KEY:
  ${{ secrets.SENSIBLE_TEST_API_KEY }}`. Upload the report and raw responses as a workflow artifact. Optionally open or
  update a GitHub issue when there's DRIFT that isn't in the accepted list.
- **Accepted differences**: same format as concept.md (`fact`, `reason`, `recheck` date).

### Output

`outputs/<timestamp>/report.md`: account check (`seed.py --check`), then DRIFT, then REVIEW, then coverage gaps
(operations, status codes, content types), then fixture gaps (documented fields never observed), then the shape diff
since the last snapshot.
Raw responses go next to it. Keep `outputs/` gitignored.

## Public repo: what's safe

Unlike concept.md's tooling, this suite is safe to commit here. It calls only documented endpoints through the
public API and reads only the public specs, so the code, catalog, and snapshots reveal nothing that the published docs
don't already. The rules:

- Never log request headers. The key is in `Authorization`.
- Snapshots and reports contain test-account data only.
- Don't add scenarios for undocumented endpoints. If you find one worth testing, document it first.

## Limitations

- **It runs after deploy.** It finds drift once a change is live in production, not when the backend PR merges. The
  static skeleton in concept.md covers the pre-merge side.
- **Coverage depends on scenarios and fixtures.** Fields that only appear under conditions no scenario or fixture
  triggers (rare errors, unusual documents, account settings) go unchecked. The fixture-gap report makes them visible.
  Filling them means adding fixtures, and some states may be impractical to trigger on purpose.
- **Loose spec nodes** (`additionalProperties: true`, objects with no `properties`) can't be checked in strict mode.
  Shape snapshots still show changes there.
- **Webhooks** need a public receiver. Options are a request-bin style service or skipping webhook payloads at first.
  Webhook payloads aren't in the OpenAPI response schemas anyway.
- **LLM output varies** between runs. Shape snapshots ignore values, but optional fields an LLM sometimes omits can
  cause noise. Mark those paths as optional in the shape comparison.

## Optional: generated requests

After the catalog exists, Schemathesis (`schemathesis run reference/openapi_extraction.json --url ... -H
"Authorization: Bearer $SENSIBLE_TEST_API_KEY"`) can generate requests from the spec, including edge cases, and check
responses against it. It's useful for exploring request-side drift: values the spec allows that the API rejects, or
the other way around. It creates resources freely, so run it only against the test account, and start with read-only
operations.

## Optional: backend smoke-test hook

If the backend team is ever interested: the same strict validation can run inside their SST smoke tests through
their single HTTP wrapper, so it checks every response with no per-test changes. That catches drift on an ephemeral
stage before production. It's their call, and this proposal doesn't depend on it.

## Plan

1. Write `export.py` and snapshot today's test account into `fixtures/`, so the account is recoverable before
   anything else changes. Then write `seed.py` and `seed.py --check`, and prove them by seeding a second, empty
   account.
2. Add strict spec validation, shape snapshots, and observed-field coverage to the existing extraction prober (no
   catalog yet). Run it once and triage.
3. Move scenarios into the catalog; add coverage reporting; cover all four spec files.
4. Work through the coverage matrix: add fixtures until the fixture-gap report contains only paths you've decided
   to accept.
5. Add error-code scenarios, run cleanup, and the GitHub Actions workflow.
6. Optional: Schemathesis exploration.
