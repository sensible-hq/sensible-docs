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
| API key | `SENSIBLE_API_KEY` env var. Locally, from your shell. In Actions, mapped from the `SENSIBLE_TEST_API_KEY` secret. |
| Request catalog | `scripts/test/probe_endpoints/catalog/*.yaml`, one file per spec file |
| Test assets | PDFs in `assets/pdfs/` (already used by the prober) plus configs checked in next to the catalog |

Make sure the local `SENSIBLE_API_KEY` is the test account's key, not a personal or production account's key, before
the first run. The suite creates and deletes resources.

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

### Test account hygiene

- Prefix every resource the suite creates (document types, configs, goldens, processors) with `drift_probe_<run-id>_`.
- Run destructive operations (DELETE) only on resources created in the same run.
- A cleanup step at the end of every run, and at the start of the next run, deletes leftover `drift_probe_*`
  resources.
- Long-lived fixtures that scenarios read but never modify (for example, the `api_skill_*` document types) are created
  idempotently by a setup step from configs checked into the repo. That makes the suite work against any test account,
  which is item 1 in the current prober's checklist.

### Running it

- **Locally**: `python3 scripts/test/probe_endpoints/contract.py [--only extraction] [--update-snapshots]`
- **GitHub Actions**: new workflow with `workflow_dispatch` and an optional weekly `schedule`, `SENSIBLE_API_KEY:
  ${{ secrets.SENSIBLE_TEST_API_KEY }}`. Upload the report and raw responses as a workflow artifact. Optionally open or
  update a GitHub issue when there's DRIFT that isn't in the accepted list.
- **Accepted differences**: same format as concept.md (`fact`, `reason`, `recheck` date).

### Output

`outputs/<timestamp>/report.md`: DRIFT, then REVIEW, then coverage gaps, then the shape diff since the last snapshot.
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
- **Coverage depends on scenarios.** Fields that only appear under conditions no scenario triggers (rare errors,
  specific document types, account settings) go unchecked. The coverage report makes the gaps visible but can't fill
  them.
- **Loose spec nodes** (`additionalProperties: true`, objects with no `properties`) can't be checked in strict mode.
  Shape snapshots still show changes there.
- **Webhooks** need a public receiver. Options are a request-bin style service or skipping webhook payloads at first.
  Webhook payloads aren't in the OpenAPI response schemas anyway.
- **LLM output varies** between runs. Shape snapshots ignore values, but optional fields an LLM sometimes omits can
  cause noise. Mark those paths as optional in the shape comparison.

## Optional: generated requests

After the catalog exists, Schemathesis (`schemathesis run reference/openapi_extraction.json --url ... -H
"Authorization: Bearer $SENSIBLE_API_KEY"`) can generate requests from the spec, including edge cases, and check
responses against it. It's useful for exploring request-side drift: values the spec allows that the API rejects, or
the other way around. It creates resources freely, so run it only against the test account, and start with read-only
operations.

## Optional: backend smoke-test hook

If the backend team is ever interested: the same strict validation can run inside their SST smoke tests through
their single HTTP wrapper, so it checks every response with no per-test changes. That catches drift on an ephemeral
stage before production. It's their call, and this proposal doesn't depend on it.

## Plan

1. Add strict spec validation and shape snapshots to the existing extraction prober (no catalog yet). Run it once and
   triage.
2. Move scenarios into the catalog; add coverage reporting; cover all four spec files.
3. Add error-code scenarios.
4. Add the fixtures setup and cleanup steps, then the GitHub Actions workflow.
5. Optional: Schemathesis exploration.
