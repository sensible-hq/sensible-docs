# Extraction API Source of Truth

Reference for verifying and updating `reference/openapi_extraction.json`.
All paths are relative to `~/GitHub/sensible`.

---

## The core rule

**Response field presence depends on which serializer runs, not which endpoint you're on.**

- Full responses (POST /extract, GET /documents/{id}) → `toExtractionResponse()` in `entity.ts`
- Summary responses (GET /extractions list) → `toExtractionSummaryResponse()` in `entity.ts`
- Upload responses (POST /generate_upload_url) → `toUploadUrlResponse()` in `entity.ts`

Fields that appear in full responses are often absent from summaries. Check the serializer, not the endpoint.

---

## Request body shapes

### Supported file types / content types

| Source of truth | File | Notes |
|---|---|---|
| `DOCUMENT_TYPES` constant | `src/common.ts` | Full list of accepted MIME types — this is what `sensible_content_type: true` validates against |
| `EXTRACTION_INPUT_TYPES` constant | `src/api/extract/handler.ts` | Subset of DOCUMENT_TYPES accepted as Content-Type headers for multipart extraction |
| `contentTypes` field on route config | `src/api/extract/handler.ts:74-87` | Per-route override of allowed Content-Type values |

> **Past spec error**: ContentTypeParameter enum had multiple content types comma-joined as a single string value (e.g. `"application/pdf,image/png"`). Each MIME type must be a separate enum entry. Source: `EXTRACTION_INPUT_TYPES` array in `handler.ts`.

### encodedPdf / base64 body

- **File**: `src/api/extract/handler.ts:45-59`
- **Shape**: `{ document: string, content_type?: DocumentContentType }`
- `content_type` is optional; if omitted, the backend sniffs from the base64 payload (`parseDocument()` at lines 102–135)

### extract_from_url request body

- **File**: `src/api/extract-from-url/handler.ts`
- Fields: `document_url` (required), `content_type?`, `webhook?`, `extra_data?`, `ocr_engine?` (not publicly documented), `ocr_every_page?` (not publicly documented)

### generate_upload_url request body

- **File**: `src/api/generate-upload-url/handler.ts`
- Fields: `webhook?`, `content_type?`, `extra_data?`
- Note: `ocr_engine`, `segment_documents_with`, `ocr_every_page` are blocked by `additionalProperties: false` — do not document

### Portfolio request bodies (no `{document_type}`)

Both `/extract_from_url` and `/generate_upload_url` portfolio variants accept:
`types` (required, string[]), `document_url` (required), `content_type?`, `webhook?`, `segment_documents_with?`, `extra_data?`
Not publicly documented: `ocr_engine?`, `ocr_every_page?`

---

## Response body shapes

### Single extraction — full response

- **Source**: `SingleExtraction.toExtractionResponse()` — `src/api/extract/entity.ts:563-609`
- **Type**: `SingleExtractionResponse` — `src/api/extract/response-types.ts:63-80`
- Fields beyond `ExtractionResponseBase`: `type`, `configuration`, `configuration_version`, `parsed_document`, `validations`, `errors`, `classification_summary`, `file_metadata`, `webhook`, `download_url`, `converted_url`, `postprocessorOutput`, `content_type`, `reviewStatus`

### Single extraction — summary (GET /extractions list)

- **Source**: `SingleExtraction.toExtractionSummaryResponse()` — `src/api/extract/entity.ts`
- Fields beyond `ExtractionResponseBase`: `type`, `configuration`, `configuration_version`, `content_type`, `errors`, `validations`, `reviewStatus`
- **Absent**: `parsed_document`, `download_url`, `classification_summary`, `extra_data`, `file_metadata`

### Portfolio extraction — full response

- **Source**: `MultiExtraction.toExtractionResponse()` — `src/api/extract/entity.ts:910-965`
- **Type**: `MultiExtractionResponse` — `src/api/extract/response-types.ts:110-120`
- Fields beyond `ExtractionResponseBase`: `types`, `segment_documents_with?`, `documents?[]`, `errors?`, `webhook?`, `download_url?`, `content_type?`, `reviewStatuses?`

> **Past spec error**: Portfolio documents had `parsed_document` and `file_metadata` in snake_case. The real API returns `parsedDocument` and `fileMetadata` (camelCase) on `DocumentInPortfolio.output`. Check `MultiExtractionDocumentResponse` in `response-types.ts` for field casing.

### Upload URL response (generate_upload_url)

- **Source**: `SingleExtraction.toUploadUrlResponse(url)` / `MultiExtraction.toUploadUrlResponse(url)` — `entity.ts`
- Shape: `{ id, created, status, type?, configuration?, upload_url }`
- `extra_data` is NOT echoed here — only returned on GET /documents/{id} after completion

### ExtractionResponseBase (shared base)

- **File**: `src/api/extract/response-types.ts`
- Fields: `id`, `created`, `completed?`, `status`, `error?`, `validation_summary?`, `page_count?`, `document_name?`, `environment`, `coverage?`, `batchId?` (not publicly documented), `charged?`, `version_id?` (not publicly documented), `taskId?` (not publicly documented), `extra_data?`, `actor?`

---

## Field-specific sources

### reviewStatus vs reviewStatuses

- **Single doc**: `reviewStatus?: HumanReviewStatus` — `src/api/extract/response-types.ts:78`
- **Portfolio**: `reviewStatuses?: (HumanReviewStatus | null)[]` — `src/api/extract/response-types.ts:119`
- These are different fields on different types — do not share a schema between single and portfolio summaries

> **Past spec error**: `reviewStatuses` (plural, array) was incorrectly on the shared base summary schema. Single-doc summaries use singular `reviewStatus`.

### Webhook payload type

- **File**: `src/api/extract/response-types.ts:20-28`
- **Type**: `payload?: Record<string, unknown> | string | number | boolean | Array<unknown>`
- Not a plain string — must be `anyOf` in the spec

### Pagination (GET /extractions)

- **File**: `src/api/extractions/handler.ts:123-125, 147-154, 456`
- **Type**: `ExtractionsResult` — fields: `extractions[]`, `continuation_token` (base64url cursor, the real pagination mechanism), `last_evaluated_creation_date` (deprecated but still returned)

> **Past spec error**: The spec described `continuation_token` in prose but the schema only modeled `cutoff_date`. Both `continuation_token` and `last_evaluated_creation_date` must be in the schema.

### Auth token response (POST /account/auth_tokens)

- **File**: `src/api/account/auth-token.ts:34-59, 77`
- Key fields: `created_by` (line 47), `revoked` (line 77 — tracked via DynamoDB attribute)
- `AuthTokenUsage`: is an **array**, not a string — was mistyped in the old spec

### Actor field

- **File**: `src/api/extract/response-types.ts` (in `ExtractionResponseBase`)
- Value: `'api_key: <name>'`, `'api_key'`, `'legacy: <account>'`, or the initiating user's email
- auth_token-initiated extractions are not a real code path — omit that case from public docs

---

## Enums and types

### ExtractionStatus

- **File**: `src/common.ts:204`
- Values: `"WAITING" | "FAILED" | "COMPLETE" | "PROCESSING"`

### OcrEngineType

- **File**: `src/common.ts`
- Values: `"amazon" | "google" | "lazarus" | "microsoft" | "microsoft5" | "pdf"`

### PortfolioSplittingMethod

- **File**: `src/engine/types.ts` (`portfolioSplittingMethodSchema`)
- Values: `"llm" | "fingerprints"`

### DocumentContentType / SupportedFileTypes

- **File**: `src/common.ts` — `DOCUMENT_TYPES` constant is the canonical list

---

## Where to look when the code changes

| If this changes... | Check here |
|---|---|
| Accepted file types / MIME types | `src/common.ts` (`DOCUMENT_TYPES`) |
| Accepted Content-Type headers per endpoint | `src/api/extract/handler.ts` (`contentTypes` field on route config) |
| Single extraction response fields | `src/api/extract/response-types.ts` (`SingleExtractionResponse`) + `entity.ts` (`toExtractionResponse`) |
| Portfolio response fields | `src/api/extract/response-types.ts` (`MultiExtractionResponse`) + `entity.ts` (`toExtractionResponse`) |
| List/summary response fields | `entity.ts` (`toExtractionSummaryResponse`) |
| Upload URL response fields | `entity.ts` (`toUploadUrlResponse`) |
| Shared base fields (id, status, actor, etc.) | `src/api/extract/response-types.ts` (`ExtractionResponseBase`) |
| reviewStatus / reviewStatuses | `src/api/extract/response-types.ts:78,119` |
| Webhook payload shape | `src/api/extract/response-types.ts:20-28` |
| Pagination fields | `src/api/extractions/handler.ts` (`ExtractionsResult`) |
| Auth token fields | `src/api/account/auth-token.ts` |
| ExtractionStatus enum | `src/common.ts:204` |
