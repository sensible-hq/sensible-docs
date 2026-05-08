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
- `extra_data` is a direct property on `ExtractionSummaryBase`, `ExtractionSingleResponse`, `ExtractionPortfolioRetrievalResponse`, `ExtractFromUrlResponse`, `ExtractFromUrlRequest`, and `GenerateUrlRequest`. No schema inherits it twice.
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

## Extraction API — portfolio endpoints

**Routes**:
- `POST /extract_from_url` (and `/extract_from_url/{type}`, `/extract_from_url/{type}/{configuration}`)
- `POST /generate_upload_url` (and `/{type}`, `/{type}/{configuration}`)

| File | Role |
|------|------|
| `src/api/extract-from-url/handler.ts` | Route handler for download-then-extract flow |
| `src/api/generate-upload-url/handler.ts` | Route handler for pre-signed S3 upload URL flow |
| `src/api/extract/storage.ts` | Shared extraction persistence (`createAsyncExtractionFromParameters`) |
| `src/api/extract/response-types.ts` | Response type definitions (`ExtractionResponseBase`, `SingleExtractionResponse`, `MultiExtractionResponse`) |

### Full portfolio request shape (as of 2026-05)

Both portfolio endpoints accept these fields (`extract-from-url/handler.ts:60–68`, `generate-upload-url/handler.ts:55–80`):

| Field | Type | Notes |
|-------|------|-------|
| `types` | `string[]` | Required. Doc type names |
| `segment_documents_with` | `"llm" \| "fingerprints"` | How to split portfolio into sub-docs |
| `ocr_engine` | `OcrEngineType` | **Documented in extraction spec**: no. **Exists in backend**: yes |
| `ocr_every_page` | `boolean` | **Documented in extraction spec**: no. **Exists in backend**: yes |
| `document_url` | `string` | `extract_from_url` only |
| `webhook` | `Webhook` | Optional async callback |
| `content_type` | `DocumentContentType` | Optional MIME hint |
| `extra_data` | `ExtraDataRecord` | Optional audit/passthrough data |

`ocr_engine` and `ocr_every_page` are **docs gaps** in `reference/openapi_extraction.json` — they exist in the backend but are not in the spec. Decision on whether to expose them publicly is pending.

**Note**: `src/docs/Senseml reference/document-type-settings/ocr-engine.md:26` states portfolio extraction uses Microsoft OCR and ignores OCR settings in document types. This refers to document-type-level settings; the `ocr_engine` request parameter may override this. Verify with eng before documenting.

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
