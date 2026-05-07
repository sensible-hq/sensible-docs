# Sensible API Code Reference

Reference for writing or updating `reference/openapi_*.json` specs. All paths are relative to `~/GitHub/sensible` (the backend repo).

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
