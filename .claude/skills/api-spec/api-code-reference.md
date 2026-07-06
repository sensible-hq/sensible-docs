# Sensible API Code Reference

Reference for writing or updating `reference/openapi_*.json` specs. All paths are relative to `~/GitHub/sensible` (the backend repo).

---

## `openapi_email.json` — spec structure reference

**File**: `reference/openapi_email.json`

### Paths

| Method | Path | operationId | Request schema | Response schema |
|--------|------|-------------|----------------|-----------------|
| GET | `/processors/email` | `list-email-processors` | — | array of `EmailProcessorOutput` |
| GET | `/processors/email/{name}` | `get-email-processor` | — | `EmailProcessorOutput` |
| PUT | `/processors/email/{name}` | `upsert-email-processor` | `EmailProcessorInput` | `EmailProcessorOutput` |
| DELETE | `/processors/email/{name}` | `delete-email-processor` | — | 204 No Content |

### Schema relationships

```
EmailProcessorInput
  webhooks: WebhookList  (array of Webhook | EnvironmentWebhook)
  bodySpec?: SingleDocTypeSpec
  attachmentSpecs?: AttachmentSpec[]

EmailProcessorOutput  (same shape as Input, plus name + created)
  name: string
  created: string
  webhooks: WebhookList
  bodySpec?: SingleDocTypeSpec
  attachmentSpecs?: AttachmentSpec[]

AttachmentSpec  (oneOf, discriminator: kind)
  ├── SingleDocTypeSpec   { kind: "doctype",        docTypeId: string }
  ├── ClassificationSpec  { kind: "classification", docTypeIds: string[] }
  └── PortfolioSpec       { kind: "portfolio",      docTypeIds: string[], segmentDocumentsWith?: string }

WebhookList  (array)
  ├── Webhook             { url: string }               — element 0, required
  └── EnvironmentWebhook  { url: string, environment: string } — elements 1+
```

**Key constraints not enforceable in OAS 3.0.3:**
- `webhooks[0]` must be a plain `Webhook`; `webhooks[1+]` must be `EnvironmentWebhook`
- Either `bodySpec` or `attachmentSpecs` must be present (or both)

---

## `openapi_extraction.json` — spec structure reference

**File**: `reference/openapi_extraction.json`

### Paths

| Method | Path | operationId | Request schema | Response schema |
|--------|------|-------------|----------------|-----------------|
| POST | `/extract/{document_type}` | `extract-data-from-a-document` | multipart body | `ExtractionSingleResponse` |
| POST | `/extract/{document_type}/{config_name}` | `extract-data-from-a-document-with-config` | multipart body | `ExtractionSingleResponse` |
| POST | `/extract_from_url/{document_type}` | `extract-from-url` | `ExtractFromUrlRequest` | `ExtractFromUrlResponse` |
| POST | `/extract_from_url/{document_type}/{config_name}` | `provide-a-download-url-with-config` | `ExtractFromUrlRequest` | `ExtractFromUrlResponse` |
| POST | `/extract_from_url` | `provide-a-download-url-for-a-pdf-portfolio` | inline (types, document_url, extra_data, …) | `ExtractFromUrlPortfolioResponse` |
| POST | `/generate_upload_url/{document_type}` | `generate-an-upload-url` | `GenerateUrlRequest` | `UploadResponse` |
| POST | `/generate_upload_url/{document_type}/{config_name}` | `generate-an-upload-url-with-config` | `GenerateUrlRequest` | `UploadResponse` |
| POST | `/generate_upload_url` | `generate-an-upload-url-for-a-pdf-portfolio` | inline (types, extra_data, …) | `UploadPortfolioResponse` |
| GET | `/documents/{id}` | `retrieving-results` | — | oneOf `ExtractionSingleRetrievalResponse` \| `ExtractionPortfolioRetrievalResponse` |
| GET | `/extractions` | `list-extractions` | — | `ExtractionsResponseFiltered` |
| GET | `/extractions/statistics` | `statistics` | — | `StatisticsResponse` |
| GET | `/generate_excel/{ids}` | `get-excel-extraction` | — | binary |
| GET | `/generate_csv/{ids}` | `get-csv-extraction` | — | binary |
| POST | `/account/auth_tokens` | `account-auth-tokens` | — | `AuthTokenResponse` |

### Schema relationships

```
ExtractionSummaryBase                         ← base for GET /extractions list items
  ├── SingleExtractionSummaryResponse         (allOf + type, configuration, errors, validations)
  └── MultiExtractionSummaryResponse          (allOf + types, documents[]: MultiExtractionSummaryDocument)

ExtractionsResponseFiltered                   ← GET /extractions response
  └── extractions[]: anyOf SingleExtractionSummaryResponse | MultiExtractionSummaryResponse

ExtractionSingleResponse                      ← POST /extract (sync) response
ExtractionSingleRetrievalResponse             ← GET /documents/{id} single (allOf ExtractionSingleResponse, no extra props)

ExtractionPortfolioRetrievalResponse          ← GET /documents/{id} portfolio
  └── documents[]: DocumentInPortfolio

ExtractFromUrlResponse                        ← POST /extract_from_url/{type} (pending ID + status only)
ExtractFromUrlPortfolioResponse               ← POST /extract_from_url portfolio (allOf PortfolioBase)
UploadResponse                                ← POST /generate_upload_url (ID + upload_url)
UploadPortfolioResponse                       ← POST /generate_upload_url portfolio (allOf PortfolioBase)
PortfolioBase                                 ← { id, created, status }
```

**Notable:**
- `extra_data` appears in request bodies (`ExtractFromUrlRequest`, `GenerateUrlRequest`, and the inline portfolio request bodies) and in full retrieval responses (`ExtractionSingleResponse`, `ExtractionPortfolioRetrievalResponse`, `ExtractFromUrlResponse`). It is **not** on `ExtractionSummaryBase` — the list endpoint (`GET /extractions`) intentionally omits it. In `entity.ts`, `toExtractionSummaryResponse()` does not populate `extra_data`; only `toExtractionResponse()` does.
- `POST /extract_from_url` and `POST /generate_upload_url` (portfolio variants, no `{document_type}`) define their request body inline rather than as a named schema.
- `ExtractionSingleRetrievalResponse` is a named alias for `ExtractionSingleResponse` with no added properties.

---

## `openapi_configuration.json` — spec structure reference

**File**: `reference/openapi_configuration.json`

Three nested CRUD resources: **DocumentType → Configuration → Golden** (reference document).

### Paths

| Method | Path | operationId | Request | Response |
|--------|------|-------------|---------|----------|
| GET | `/document_types` | `list-document-types` | — | array of `DocumentType` |
| POST | `/document_types` | `create-document-type` | `PostDocumentType` | `DocumentType` |
| GET | `/document_types/{type-id}` | `get-document-type` | — | `DocumentType` |
| PUT | `/document_types/{type-id}` | `update-document-type` | `PutDocumentType` | `DocumentType` |
| DELETE | `/document_types/{type-id}` | `delete-document-type` | — | 204 |
| GET | `…/{type-id}/configurations` | `list-configurations` | — | array of `ConfigurationResponse` |
| POST | `…/{type-id}/configurations` | `create-configuration` | `PostConfiguration` | `ConfigurationResponse` |
| GET | `…/{type-id}/configurations/{config-name}` | `get-configuration` | — | `ConfigurationResponse` |
| PUT | `…/{type-id}/configurations/{config-name}` | `update-configuration` | `PutConfiguration` | `ConfigurationResponse` |
| DELETE | `…/{type-id}/configurations/{config-name}` | `delete-configuration` | — | 204 |
| GET | `…/{config-name}/versions` | `get-configuration-versions` | — | `ConfigurationVersionsResponse` |
| GET | `…/{config-name}/{version}` | `get-configuration-by-version` | — | `ConfigurationResponse` |
| PUT | `…/{config-name}/{version}` | `publish-configuration-by-version` | `PublishConfigurationVersion` | `ConfigurationResponse` |
| DELETE | `…/{config-name}/{version}` | `delete-configuration-by-version` | — | 204 |
| GET | `…/{type-id}/goldens` | `list-reference-documents` | — | array of `GoldenResponse` |
| POST | `…/{type-id}/goldens` | `create-reference-document` | `PostGolden` | `GoldenResponse` |
| GET | `…/{type-id}/goldens/{document-name}` | `get-reference-document` | — | `GoldenResponse` |
| PUT | `…/{type-id}/goldens/{document-name}` | `update-reference-document` | `PutGolden` | `GoldenResponse` |
| DELETE | `…/{type-id}/goldens/{document-name}` | `delete-reference-document` | — | 204 |
| DELETE | `…/{type-id}/goldens/{document-name}/configuration` | `delete-reference-document-association` | — | 204 |
| POST | `/extract_text_from_golden/{type-name}` | `extract-all-text-from-reference-document` | `PostGoldenExtraction` | `ResponseStandardText` |

### Schema relationships

```
DocumentType          { name, id, created, schema: DocumentTypeOutput }
DocumentTypeOutput    { fingerprint_mode, ocr_engine, prevent_default_merge_lines,
                        ocr_level, validations, review_triggers }

ConfigurationResponse { name, created, configuration (SenseML as string), version_id, versions[] }
ConfigurationVersion  { version_id, datetime, environments[], draft }

GoldenResponse        { name, created, configuration, error, upload_url, download_url, thumbnail_url }

PostConfiguration / PutConfiguration
  configuration: StringifiedConfigurationRequest  (SenseML JSON serialized as a string)
  publish_as: Environment  ("production" | "development")

ResponseGoldenExtraction  allOf: [Extraction]   ← same shape as a standard extraction response
```

**Notable:**
- Configuration bodies are stringified JSON — SenseML is stored and returned as a string, not a parsed object.
- Goldens can be pinned to a specific config via `configuration` in `PostGolden`/`PutGolden`; the association is removed separately via `DELETE …/configuration`.
- `ResponseGoldenExtraction` is `allOf: [Extraction]` with no additional properties — a named alias for the retrieval context.

---

## Email processor API

**Routes**: `GET /processors/email`, `GET /processors/email/{name}`, `PUT /processors/email/{name}`, `DELETE /processors/email/{name}`

| File | Role |
|------|------|
| `src/api/processors/email/handler.ts` | Route definitions and HTTP dispatch |
| `src/api/processors/email/schemas.ts` | Zod validation schemas — source of truth for request shape |
| `src/api/processors/email/mappers.ts` | Converts DB entities to API response objects |
| `src/api/processors/email/service.ts` | Business logic and DB operations |
| `src/api/processors/email/validator.ts` | Cross-field validation (e.g. checks referenced doc type IDs exist) |

### Key types

**Request input** (`schemas.ts`):
```typescript
processorUpsertSchema = z.union([
  z.strictObject({ webhooks: webhooksSchemas, bodySpec: singleDocTypeSpecSchema }),
  z.strictObject({ webhooks: webhooksSchemas, bodySpec: singleDocTypeSpecSchema.optional(), attachmentSpecs: z.array(attachmentSpecSchema).nonempty() }),
])
```
- `webhooks` is required in both variants — first element must be a plain `Webhook` (`{url}`), additional elements must be `EnvironmentWebhook` (`{url, environment}`)
- Either `bodySpec` or `attachmentSpecs` must be present; both may be present

**AttachmentSpec** discriminated union (`schemas.ts`):
```typescript
// kind: "doctype"
{ kind: "doctype", docTypeId: string }

// kind: "classification"
{ kind: "classification", docTypeIds: string[] }

// kind: "portfolio"
{ kind: "portfolio", docTypeIds: string[], ocrEngine?: OcrEngineType, segmentDocumentsWith?: PortfolioSplittingMethod, ocrEveryPage?: boolean }
```
`ocrEveryPage` and `ocrEngine` exist **only** in the email API's `PortfolioSpec`. They do not appear in the extraction API portfolio handlers.

**Response output** (`mappers.ts`):
```typescript
type EmailProcessorOutput = {
  name: string;
  created: string;
  webhooks: (Webhook | EnvironmentWebhook)[];
  bodySpec?: SingleDocTypeSpec;
  attachmentSpecs?: AttachmentSpec[];  // always 0 or 1 elements in practice
}
```
`toAttachmentSpecsOutput()` returns `undefined` (not `[]`) when no specs are configured.

**Email address format** (`packages/infra-sst-v2/infra/resources/email-decoder/email-parsing.ts`):
```
[{environment}.]{processorAlias|processorId}.{accountAlias}@{domain}
```
`development.` is the only supported environment prefix. No environment prefix routes to production.

**`webhooks` ordering enforced at the API level**: the Zod tuple `z.tuple([webhookSchema]).rest(environmentWebhookSchema)` means element 0 must be a plain `Webhook`; elements 1+ must be `EnvironmentWebhook`. OAS 3.0.3 cannot enforce this constraint in arrays.

**DELETE returns 204** (no body). Source: `success()` in `src/api/common.ts:317` — `statusCode: response ? 200 : 204`.

---

## Extraction API

**Routes**: All routes in `openapi_extraction.json`

| File | Role |
|------|------|
| `src/api/extract/handler.ts` | POST /extract/{type} and /extract/{type}/{configuration} — synchronous extraction. Calls `createSingleExtraction` without `extraData` or `webhook`; body schema (`Base64PDF`) only accepts `document` + `content_type`. `extra_data` is therefore never set on the entity and is absent from the response even though `toExtractionResponse()` includes the field unconditionally. |
| `src/api/extract/extract.ts` | Core extraction engine invocation |
| `src/api/extract/storage.ts` | DynamoDB/S3 persistence; `createExtractionQueryStringSchema` (query param source of truth) |
| `src/api/extract/response-types.ts` | `ExtractionResponseBase`, `SingleExtractionResponse`, `MultiExtractionResponse` |
| `src/api/extract/entity.ts` | Entity classes; `SingleExtractionSummaryResponse`, `MultiExtractionSummaryResponse`, `ExtractionStatus` |
| `src/api/extract-from-url/handler.ts` | POST /extract_from_url/* — async URL-based extraction |
| `src/api/generate-upload-url/handler.ts` | POST /generate_upload_url/* — async pre-signed S3 upload flow |
| `src/api/extractions/handler.ts` | GET /documents/{id}, GET /extractions, GET /extractions/statistics; `ExtractionsQueryParams`, `ExtractionStatsQueryParams` |
| `src/api/generate-file/excel/handler.ts` | GET /generate_excel/{ids} |
| `src/api/generate-file/csv/handler.ts` | GET /generate_csv/{ids} |
| `src/api/account/auth-token-handlers.ts` | POST /account/auth_tokens |

### Key types

**POST /extract body** (`extract/handler.ts`):
```typescript
type Base64PDF = {
  document: string;           // base64-encoded document
  content_type?: DocumentContentType;
};
```

**Query string (all /extract routes)** (`extract/storage.ts:createExtractionQueryStringSchema`):
```typescript
type CreateExtractionQueryStringParams = {
  environment?: string;
  document_name?: string;
};
```
`webhook` and `extra_data` travel in the **request body** for /extract_from_url and /generate_upload_url. For POST /extract, they can come from either body or query string.

**POST /extract_from_url portfolio request body** (`extract-from-url/handler.ts`):

| Field | Type | Notes |
|-------|------|-------|
| `types` | `string[]` | Required. Doc type names |
| `document_url` | `string` | Required. URL of document to fetch |
| `segment_documents_with` | `"llm" \| "fingerprints"` | How to split portfolio into sub-docs |
| `ocr_engine` | `OcrEngineType` | Exists in backend; **not publicly documented** |
| `ocr_every_page` | `boolean` | Exists in backend; **not publicly documented** |
| `webhook` | `Webhook` | Optional async callback |
| `content_type` | `DocumentContentType` | Optional MIME hint |
| `extra_data` | `ExtraDataRecord` | Optional passthrough data |

`ocr_engine` and `ocr_every_page` are the same for the /generate_upload_url portfolio variant. Decision to expose publicly is pending (confirmed 2026-05-07: deliberately not documented).

**ExtractionStatus** (`src/common.ts:204`):
```typescript
type ExtractionStatus = "WAITING" | "FAILED" | "COMPLETE" | "PROCESSING";
```

**GET /extractions query params** (`extractions/handler.ts:ExtractionsQueryParams`):
```typescript
type ExtractionsQueryParams = {
  start_date?: string;            // ISO 8601
  end_date?: string;
  limit?: string;                 // integer ≥ 1, default 20
  document_type_ids?: string;     // comma-separated UUIDs
  configuration_ids?: string;     // comma-separated UUIDs
  environments?: string;          // comma-separated names
  statuses?: string;              // comma-separated ExtractionStatus values
  min_coverage?: string;          // 0–1
  max_coverage?: string;          // 0–1
  batch_id?: string;              // UUID
  extraction_id?: string;         // UUID — retrieve a single extraction via the list endpoint
  review_statuses?: string;       // comma-separated HumanReviewStatus values
  continuation_token?: string;    // opaque base64url-encoded pagination cursor
};
```

**GET /extractions/statistics query params** (`extractions/handler.ts:ExtractionStatsQueryParams`):
```typescript
type ExtractionStatsQueryParams = {
  start_date: string;   // required, ISO 8601
  end_date: string;     // required, ISO 8601
  environments?: string;
};
```
Response includes `coverage_histogram: number[]` — a 10-bin distribution of coverage values per date/environment/config row.

**Notable**:
- POST /extract is synchronous and returns the full result immediately. POST /extract_from_url and POST /generate_upload_url are async — they return `status: "WAITING"` and fire a webhook on completion.
- `src/docs/Senseml reference/document-type-settings/ocr-engine.md:26` states portfolio extraction uses Microsoft OCR and ignores document-type OCR settings. This refers to doc-type-level settings; the request-level `ocr_engine` parameter may override it. Verify with eng before documenting.

### Request and response shapes (from source)

#### Shared base

**`ExtractionResponseBase`** (`response-types.ts`) — base for `SingleExtractionResponse`, `MultiExtractionResponse`, `SingleExtractionSummaryResponse`, and `MultiExtractionSummaryResponse`:
```typescript
type ExtractionResponseBase = {
  id: string;
  created: string;
  completed?: string;
  status: ExtractionStatus;          // "WAITING" | "PROCESSING" | "COMPLETE" | "FAILED"
  error?: unknown;
  validation_summary?: ValidationSummary;
  page_count?: number;
  document_name?: string;
  environment: string;
  coverage?: number;
  batchId?: string;
  charged?: number;
  version_id?: string;
  taskId?: string;                   // set when produced by a processor execution
  extra_data?: ExtraDataRecord;      // present on full responses; absent from summary responses
  actor?: string;                    // best-effort label for the initiating user/credential; omitted for system-initiated extractions
};
```

**`Webhook`** (`response-types.ts`):
```typescript
type Webhook = {
  url?: string;
  payload?: Record<string, unknown> | string | number | boolean | Array<unknown>;
};
```

#### POST /extract/{document_type} — sync

**Request body** (multipart bytes OR JSON):
```typescript
// JSON variant:
type Base64PDF = { document: string; content_type?: DocumentContentType; };
// Binary variant: raw bytes as request body; content-type header identifies doc type
```

**Response** — `SingleExtractionResponse` = `ExtractionResponseBase` plus:
```typescript
{
  type: string;
  configuration?: string;
  configuration_version?: string;
  parsed_document?: ParsedDocument;          // Record<string, VerboseFieldValue>
  validations?: DocumentValidationOutput[];
  errors: ExtractionError[];
  classification_summary?: ClassificationSummaryResponse[];
  file_metadata?: FileMetadata;
  webhook?: Webhook;
  download_url?: string;
  content_type?: DocumentContentType;
  reviewStatus?: HumanReviewStatus;
  postprocessorOutput?: unknown;
  text?: StandardizedText;                   // only when verbosity >= 3
  parsed_document_with_metadata?: ParsedDocumentWithMetadata; // only when withMetadata=true
}
```
Built by `SingleExtraction.toExtractionResponse(withMetadata)` in `entity.ts`.

#### POST /extract_from_url/{document_type} — async, single doc

**Request body** (`ExtractFromUrlRequest`):
```typescript
{
  document_url: string;              // required
  content_type?: DocumentContentType;
  webhook?: Webhook;
  extra_data?: ExtraDataRecord;
  ocr_engine?: OcrEngineType;        // not publicly documented
  ocr_every_page?: boolean;          // not publicly documented
}
```

**Response** — same `SingleExtractionResponse` shape, but `parsed_document` is absent (status is `WAITING`). `extra_data` is echoed immediately.

#### POST /extract_from_url — async, portfolio

**Request body**:
```typescript
{
  document_url: string;              // required
  types: string[];                   // required, minItems: 1
  content_type?: DocumentContentType;
  webhook?: Webhook;
  segment_documents_with?: "llm" | "fingerprints";
  extra_data?: ExtraDataRecord;
  ocr_engine?: OcrEngineType;        // not publicly documented
  ocr_every_page?: boolean;          // not publicly documented
}
```

**Response** — `MultiExtractionResponse` = `ExtractionResponseBase` plus:
```typescript
{
  types: string[];
  segment_documents_with?: PortfolioSplittingMethod;
  documents?: MultiExtractionDocumentResponse[];  // absent on initial WAITING response
  errors?: MultiExtractionError[];
  webhook?: Webhook;
  download_url?: string;
  content_type?: DocumentContentType;
  reviewStatuses?: (HumanReviewStatus | null)[];
}
```

#### POST /generate_upload_url/{document_type} — async, single doc

**Request body** (`ExtractionCreationParams`, schema restricts to subset):
```typescript
{
  webhook?: Webhook;
  content_type?: DocumentContentType;
  extra_data?: ExtraDataRecord;
  // ocr_engine, segment_documents_with, ocr_every_page blocked by additionalProperties:false
}
```

**Response** — `ExtractionFromUploadUrlResponse` (built by `SingleExtraction.toUploadUrlResponse(url)`):
```typescript
{
  id: string;
  created: string;
  status: ExtractionStatus;
  type?: string;
  configuration?: string;
  upload_url: string;
}
```
Note: `extra_data` is NOT echoed here. It is only returned by `GET /documents/{id}` once the extraction completes.

#### POST /generate_upload_url — async, portfolio

**Request body**:
```typescript
{
  types: string[];                   // required, minItems: 1
  webhook?: Webhook;
  content_type?: DocumentContentType;
  segment_documents_with?: "llm" | "fingerprints";
  extra_data?: ExtraDataRecord;
  ocr_engine?: OcrEngineType;        // not publicly documented
  ocr_every_page?: boolean;          // not publicly documented
}
```

**Response** — same `ExtractionFromUploadUrlResponse` shape, but `type` and `configuration` are absent (built by `MultiExtraction.toUploadUrlResponse(url)`):
```typescript
{ id: string; created: string; status: ExtractionStatus; upload_url: string; }
```

#### GET /documents/{id}

**Query params:** `{ withMetadata?: "true" }`

**Response** — `SingleExtractionResponse` or `MultiExtractionResponse` (fully hydrated from S3). Key difference from POST responses: `parsed_document`/`documents` are populated, `download_url` is a signed S3 URL, and `extra_data` is present. `withMetadata=true` adds `parsed_document_with_metadata` (single) or per-doc `parsedDocumentWithMetadata` (portfolio).

Built by `extraction.toExtractionResponse(withMetadata)` in `entity.ts`.

#### GET /extractions — list

**Response**:
```typescript
type ExtractionsResult = {
  extractions: (SingleExtractionSummaryResponse | MultiExtractionSummaryResponse)[];
  continuation_token: string | null;   // base64url { user, created, id }; default page 20
};
```

**`SingleExtractionSummaryResponse`** = `ExtractionResponseBase` plus `{ type, configuration, configuration_version, content_type, errors, validations, reviewStatus }`. Built by `toExtractionSummaryResponse()` — does **not** include `extra_data`, `parsed_document`, `download_url`, or `classification_summary`.

**`MultiExtractionSummaryResponse`** = `ExtractionResponseBase` plus `{ types, segment_documents_with, reviewStatuses, documents[] }`. Per-document `output` is stripped to `{ errors, validations }` only.

#### GET /extractions/statistics

**Response**:
```typescript
type ExtractionStatsResult = {
  statistics: {
    date: string;                // YYYY-MM-DD
    environment: string;
    document_type_id: string;   // "UNCLASSIFIED_PORTFOLIO" if doc type no longer exists
    document_type_name: string;
    configuration_id: string;
    configuration_name: string;
    coverage_histogram: number[]; // 12-bin distribution per date/config row
  }[];
};
```

---

## Configuration API

**Routes**: All routes in `openapi_configuration.json`

| File | Role |
|------|------|
| `src/api/doc-type/doc-type-handlers.ts` | CRUD for /document_types |
| `src/api/doc-type/configuration-handlers.ts` | CRUD for configurations + version management; `ConfigResponse`, `ConfigurationVersion`, `PutConfigByVersion` |
| `src/api/doc-type/golden-handlers.ts` | CRUD for goldens + golden–config association; `PostGolden`, `PutGolden` |
| `src/api/doc-type/entity.ts` | Entity classes; `GoldenResponse`, `GoldenSummaryResponse`, `GoldenContentType`, `ProcessorType` |
| `src/api/doc-type/doc-type.ts` | DynamoDB storage for document types; `CreateDocType`, `UpdateDocType` |
| `src/api/doc-type/configurations.ts` | S3 blob storage for configuration bodies; version tagging and draft management |
| `src/api/doc-type/goldens.ts` | S3 + DynamoDB for golden files; `toGoldenResponse` |
| `src/api/extract-from-golden/handler.ts` | POST /extract_text_from_golden/{type} |

### Key types

**Document type** (`doc-type.ts`, `entity.ts`):
```typescript
type CreateDocType = {
  name: string;
  schema: DoctypeSettings;
  processor_type?: ProcessorType;   // "email" | "document"
};

// DoctypeSettings (src/engine/types.ts)
interface DoctypeSettings {
  ocr_engine?: OcrEngineType;
  ocr_level?: OCRLevel;
  fingerprint_mode?: "strict" | "fallback_to_all";
  validations?: DocumentValidation[];
  prevent_default_merge_lines?: boolean;
  review_triggers?: ReviewTriggers;
}
```

**Configuration** (`configuration-handlers.ts`):
```typescript
// POST body
interface PostConfiguration {
  name: string;
  configuration: string;       // SenseML JSON serialized as a string
  content_type?: TextContentType;  // "application/json" | "application/yaml"
  publish_as?: string;         // publish to this environment immediately
}

// PUT body — all fields optional; current_draft required if a draft already exists
interface PutConfiguration {
  name?: string;
  configuration?: string;
  content_type?: TextContentType;
  publish_as?: string;
  current_draft?: string;      // expected draft version UUID — optimistic locking
  note?: string;               // max 512 chars
}

interface ConfigResponse {
  name: string;
  created: string;
  configuration: string;       // SenseML JSON as a string
  content_type: TextContentType;
  version_id: string;          // UUID of current draft version
  versions: ConfigurationVersion[];
}

interface ConfigurationVersion {
  version_id: string;
  datetime: string;            // ISO 8601
  environments?: string[];     // e.g. ["production", "staging"]
  draft: boolean;
  note?: string;
  published_by?: string;
}

// PUT /configurations/{name}/versions/{version}
interface PutConfigByVersion {
  publish_as: string;          // environment name
  note?: string;
}
```

**Golden** (`golden-handlers.ts`, `entity.ts`):
```typescript
type PostGolden = {
  name: string;
  configuration?: string;      // config name to associate
  content_type?: GoldenContentType;
};

type PutGolden = {
  name?: string;
  configuration?: string;
};

// Full response (create / get single)
interface GoldenResponse {
  id: string;
  name: string;
  created: string;
  configuration?: string;      // associated config name
  error?: string;
  upload_url?: string;         // signed S3 URL for uploading the file
  download_url?: string;       // signed S3 URL for downloading
  thumbnail_url?: string;
  converted_url?: string;
}

// Summary response (list)
interface GoldenSummaryResponse {
  id: string;
  name: string;
  created: string;
  present: boolean;            // false until file has been uploaded to S3
  configuration?: string;
  error?: string;
}
```

**Notable**:
- `configuration` in POST/PUT configuration is always a string — SenseML JSON is stored and returned serialized, not as a parsed object.
- `current_draft` in PUT configuration is used for optimistic locking: if a draft exists and `current_draft` is not supplied or doesn't match, the request is rejected with a conflict error.
- `GoldenResponse` (create/get single) includes `upload_url`/`download_url` (signed S3 URLs); `GoldenSummaryResponse` (list) replaces those with `present: boolean`.
- Golden `present` is `false` after creation until the file is uploaded via the `upload_url`. A golden can exist as a metadata-only record with `present: false`.
- DELETE golden association (`DELETE …/goldens/{name}/configuration`) is a separate endpoint from DELETE golden itself.
- `extract_text_from_golden` lives in `src/api/extract-from-golden/handler.ts`, not the doc-type handlers — it returns `{ text: StandardizedText }`.

---

## Shared types

| Type | File | Value |
|------|------|-------|
| `OcrEngineType` | `src/common.ts` | `"amazon" \| "google" \| "lazarus" \| "microsoft" \| "microsoft5" \| "pdf"` |
| `OCR_ENGINE_TYPES` | `src/common.ts` | Array used to derive the above union |
| `PortfolioSplittingMethod` | `src/engine/types.ts` | `"llm" \| "fingerprints"` (from `portfolioSplittingMethodSchema`) |
| `Webhook` (extraction) | `src/api/extract/response-types.ts` | `{url?: string, payload?: ...}` |
| `Webhook` (email) | `src/api/processors/email/schemas.ts` | `{url: string}` — different type, same name |
| `EnvironmentWebhook` | `src/api/processors/email/schemas.ts` | `{url: string, environment: string}` |

**Open questions for eng** (as of 2026-05):
1. `segmentDocumentsWith` (camelCase, email API) vs `segment_documents_with` (snake_case, extraction API) — is this intentional?
2. Does the extraction API's `ocr_engine` request param override the document-type-level OCR setting noted in `ocr-engine.md:26`?

**Confirmed** (2026-05-07): `ocrEngine` and `ocrEveryPage` on `PortfolioSpec` (email API) and `ocr_engine`/`ocr_every_page` on extraction portfolio endpoints are deliberately not publicly documented.
