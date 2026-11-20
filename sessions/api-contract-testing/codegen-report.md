# Code-generated spec vs. hand-maintained spec: sync extraction

Date: 2026-10-01 · endpoint `POST /extract/{document_type}` · spec: `reference/openapi_extraction.json` on `v0` (`ExtractionSyncResponse`)

This repo is public, so this report describes API-level differences only. The full version, with the generation recipe, the generated schemas, and code references, is kept outside the repo, in Frances's local `sensible-docs-private/api-contract-testing/` folder.

## Is generating a spec from the code feasible?

Yes, with little work:

- **Response:** the backend already uses `ts-json-schema-generator` for other schemas (the SenseML schema at schema.sensible.so). Run on the extraction response type, it produced a full JSON Schema in about 5 seconds. **It needed one one-line change first:** one property uses a TypeScript construct the generator can't resolve.
- **Request:** the backend validates requests with JSON Schema objects. The query and path schemas and the list of allowed Content-Types are importable as they are; the body schema needs to be exported.
- **Routes:** declared in the backend's infrastructure code. Not extracted yet.
- **Still to build:** a script that assembles these into a bare-bones OpenAPI file and compares it with the hand-maintained spec.

## Differences found

### Response

| | Backend | Spec |
|---|---|---|
| Properties | 34 | 22 |
| Always present (required) | `id`, `created`, `status`, `type`, `environment`, `errors` | none marked required |

- **Every field in the spec exists in the backend.** No documented field is invented.
- **`environment`:** any valid name in the backend; the spec has an enum `production`, `development`.
- **In the backend but not in the spec:** `uploaded`, `processing_started`, `error`, `webhook`, `text` (verbosity ≥ 3), `extra_data`, `taskId` (declared but never set), and `version_id`, `batchId` (deliberately undocumented, per `x-internal-note`).
- **Shared with `GET /documents/{id}`, so not real differences for the sync endpoint:** `download_url`, `converted_url`, `parsed_document_with_metadata`.
- **Noise to filter out:** `charged` and `page_count` are `number` in TypeScript (which has no integer type) and `integer` in the spec.

### Request

| Topic | Backend | Spec |
|---|---|---|
| `environment` | any lowercase name (letters, numbers, underscores); default `production` | enum `production`, `development` |
| `document_name` | max 256 characters; no HTML entities | no limits documented |
| Content-Types | 14 entries, including `application/yaml` and xlsb (`application/vnd.ms-excel.sheet.binary.macroenabled.12`) | 11 |
| 415 response body | `Content-Type must be <list of types>` | "Unsupported file type…" |
| Unknown config name (`/extract/{document_type}/{config_name}`) | `400 "Specified document type does not exist"` | not documented |
| Large responses | compressed, or a `302` redirect to a download URL; `413` in extreme cases | not documented |

### Confirmed against the live API (test account)

One sync extraction (`layout_basics`) returned 21 top-level fields:
- `version_id` was present, as expected (deliberately undocumented).
- `reviewStatus` and `postprocessorOutput` were absent (documented as situational).
- None of the other backend-only fields appeared.

## What to do with this

1. **Decide which differences are spec gaps and which are deliberate.** Candidates for the spec:
   - mark the always-present fields `required`;
   - document the `document_name` limits and the large-response behavior;
   - decide whether YAML and xlsb uploads are supported features;
   - loosen or keep the `environment` enum.
2. **Keep an allowlist of deliberate omissions** so automated comparisons don't flag them every run.
3. **Automate leg 1** (see `CONCEPT.md`). That needs the backend source, so it runs either with read access from this repo's CI or in the backend's CI.
