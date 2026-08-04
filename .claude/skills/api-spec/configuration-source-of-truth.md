# Configuration API Source of Truth

Reference for verifying and updating `reference/openapi_configuration.json`.
All paths are relative to `~/GitHub/sensible`.

---

## The core rule

**Configuration bodies are always strings.** SenseML is stored and returned serialized as a string, not a parsed object. Never model `configuration` as an object in the spec.

---

## Request body shapes

### PostConfiguration

- **File**: `src/api/doc-type/configuration-handlers.ts:548-554`
- Fields: `name` (required), `configuration` (required, stringified SenseML), `content_type?`, `publish_as?`
- `editor` is **not** accepted on POST — only on PUT. Confirmed live (POST with `editor` returns 400 "body must NOT have additional properties")

### PutConfiguration

- **File**: `src/api/doc-type/configuration-handlers.ts:556-565`
- Fields: `name?`, `configuration?`, `content_type?`, `publish_as?`, `current_draft?`, `note?` (max 512 chars), `editor?`
- `current_draft` is required when a draft already exists and `configuration` is being replaced — optimistic locking
- Source of truth for `current_draft` semantics: `putConfigToConfigurationUpdate()` at lines 328–398

### Name schema (shared across all name fields)

- **File**: `src/api/validation/index.ts`
- Pattern: `^[a-z0-9_]+$`, minLength: 3, maxLength: 128
- Backend enforces the same `nameRegex` everywhere — confirmed by code tracing

### ConfigurationContentType

- **File**: `src/api/doc-type/configuration-handlers.ts`
- Values: `"application/json" | "application/yaml"` (TextContentType)

### ConfigurationEditor

- **File**: `src/api/validation/index.ts:1481-1494` (custom AJV keyword `sensible_valid_configuration_editor`)
- Values: `1 | 2 | 5 | 6` (internal bitmask — not exposed as enum in public spec by design)
- Meaning: `1` = JSON config + JSON output, `2` = JSON config + UI output, `5` = visual config + JSON output, `6` = visual config + UI output
- Source constant names: `JSONEditorId = 1`, `InstructEditorId = 2` — `src/configuration/local.ts:298-302`
- Semantics: "preferred editor" stored per config, used by frontend to reopen in correct display mode — `src/api/doc-type/entity.ts:418`

---

## Response body shapes

### ConfigurationResponse (GET/POST/PUT configurations)

- **File**: `src/api/doc-type/configuration-handlers.ts:566-573`
- Fields: `name`, `created`, `configuration` (stringified SenseML), `content_type` (required), `version_id` (not publicly documented), `versions[]`, `editor?`
- `content_type` is required in the response — confirmed live

### ConfigurationVersion

- **File**: `src/api/doc-type/configuration-handlers.ts:575-583`
- Fields: `version_id`, `datetime`, `environments?[]`, `draft`, `note?`, `published_by?`
- `published_by`: display name (full name, first name, or account name as fallback) — resolved by `getPublishedByName()` in `src/api/doc-type/configurations.ts` — **not** an email address

### DocumentTypeOutput (GET /document_types)

- **File**: `src/engine/types.ts` — `DoctypeSettings` interface
- Fields: `ocr_engine?`, `ocr_level?`, `fingerprint_mode?`, `validations?`, `prevent_default_merge_lines?`, `review_triggers?`
- `prevent_file_metadata`: returned by backend but deliberately not publicly documented

### review_triggers shape

- **File**: `src/engine/types.ts:1895-1908`
- Type: **object**, not string[]
- Fields: `coverage_threshold?` (number 0–1), `validation_errors_threshold?` (integer), `validation_warnings_threshold?` (integer), `selected_validations?` (boolean, always `true` when present)

> **Past spec error**: `review_triggers` was typed as `string[]`. It is always an object with the four fields above.

### GoldenResponse (full — create/get single)

- **File**: `src/api/doc-type/entity.ts`
- Fields: `id` (required), `name`, `created`, `configuration?`, `error?`, `upload_url?`, `download_url?`, `thumbnail_url?`, `converted_url?`

### GoldenSummaryResponse (list)

- **File**: `src/api/doc-type/entity.ts`
- Fields: `id`, `name`, `created`, `present` (false until file uploaded to S3), `configuration?`, `error?`
- `present: false` after creation until file is uploaded via `upload_url`

### extract_text_from_golden response

- **File**: `src/api/extract-from-golden/handler.ts`
- Shape: `{ "text": { "pages": [...] } }` — the handler wraps `ResponseStandardText` in a `text` property

> **Past spec error**: The spec returned a bare `pages` array. The real response is always `{ text: { pages: [...] } }`.

---

## Version management semantics

`DELETE /{config-name}/{version}` has dual behavior (confirmed live):
- Delete by draft `version_id` → removes the draft
- Delete by environment name (`"production"` / `"development"`) → unpublishes the tag but keeps version history

Source: `PutConfigByVersion` / delete handlers in `src/api/doc-type/configuration-handlers.ts`

---

## Fields deliberately not publicly documented

| Field | Schema | Reason |
|---|---|---|
| `version_id` | `ConfigurationResponse`, `ConfigurationVersion` | Internal — not publicly documented |
| `prevent_file_metadata` | `DocumentTypeOutput` | Not productized, low demand |
| `ocr_level: 6` | `ocr_level` enum | Internal-only value |

---

## Where to look when the code changes

| If this changes... | Check here |
|---|---|
| POST/PUT configuration body fields | `src/api/doc-type/configuration-handlers.ts` (PostConfiguration, PutConfiguration types) |
| ConfigurationResponse fields | `src/api/doc-type/configuration-handlers.ts:566-573` (ConfigResponse) |
| ConfigurationVersion fields | `src/api/doc-type/configuration-handlers.ts:575-583` |
| `published_by` resolution | `src/api/doc-type/configurations.ts` (`getPublishedByName`) |
| `editor` bitmask values | `src/api/validation/index.ts:1481-1494` (AJV keyword) |
| `editor` semantics | `src/api/doc-type/entity.ts:418` |
| Name pattern/length constraints | `src/api/validation/index.ts` (nameRegex) |
| DocumentTypeOutput / DoctypeSettings | `src/engine/types.ts` |
| review_triggers shape | `src/engine/types.ts:1895-1908` |
| GoldenResponse fields | `src/api/doc-type/entity.ts` |
| Golden extraction response shape | `src/api/extract-from-golden/handler.ts` |
| 204 DELETE behavior | `src/api/common.ts` (`success()`) |
