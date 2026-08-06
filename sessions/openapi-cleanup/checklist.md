# openapi-cleanup session

PR: https://github.com/sensible-hq/sensible-docs/pull/656
Branch: `openapi-cleanup` | Worktree: `~/GitHub/sensible-docs-openapi-cleanup`

## Done

- [x] `Actor` description: removed auth_token case, added x-internal-note documenting deliberate omission
- [x] `ConvertedUrlDocument`: trimmed " -- Word documents are converted..." clause from description
- [x] `Name` schema: changed example to `insurance_quote` (neutral across doc type/config/golden), added x-internal-note on allOf tradeoff
- [x] `ConfigurationEditor`: improved description to explain two-dimensional bitmask (SenseML display mode + output display mode)
- [x] `DocumentTypeOutput`: removed `prevent_file_metadata`, added x-internal-note documenting deliberate omission
- [x] `ConfigurationVersion` + `ConfigurationResponse` `version_id`: added x-internal-note that field is not publicly documented
- [x] `DocumentInPortfolio.output`: improved user-facing description; moved camelCase naming note to x-internal-note
- [x] Source-of-truth knowledge layers committed to v0 (`.claude/skills/api-spec/`)

## Done: processor_type

- [x] `ProcessorType` / `processor_type`: omitted from `DocumentType` and `PostDocumentType`. Field is accepted by the API and echoed back but has no functional effect — never read by any backend logic to gate behavior. Added during early email processor development (backend 2401a0d5, Jul 2024), never productized or surfaced in UI. Added x-internal-note to `DocumentType`. Same treatment as `prevent_file_metadata`.

## To do: review Devon's new/changed descriptions

Only descriptions where the text itself is genuinely new or changed (not just fields that gained a `$ref` to an already-existing described schema). Diffed `43973ea88~1` vs current v0.

### Extraction spec

**New schemas — review as a group:**
- [x] `AuthorizationGrant` — accepted as-is
- [x] `AuthorizationGrant.properties.path` — updated: explains key/value structure and gives concrete example
- [x] `AuthTokenUsage.properties.ip` + `.used` — accepted as-is
- [x] `ScorePortfolio` — updated: first sentence matches `Score`; added "Unlike single-document Score, includes coverage"; added x-internal-note on camelCase vs snake_case inconsistency
- [x] `ScorePortfolio.properties.score` — updated: added "In the absence of fingerprints..." sentence from `Score.value`
- [x] `ScorePortfolio.properties.coverage`, `.fieldsPresent`, `.penalties` — accepted as-is
- [x] `Grants` — updated: simplified to "At least one grant is required for an authorization token."

**New fields on existing schemas:**
- [x] `AuthTokenResponse.properties.created_by` — accepted as-is
- [x] `AuthTokenResponse.properties.revoked` — accepted as-is
- [x] `ExtractionSingleRetrievalResponse` — short user-facing description ("Extracted document data from a single-document extraction."); mechanism detail moved to x-internal-note; sync endpoint updated with note pointing to GET /documents/{id}
- [x] `ExtractionPortfolioRetrievalResponse` — added short user-facing description ("Extracted data from a multiple-document extraction.")
- [ ] `ExtractionErrorMessage` — description of the top-level `error` field for FAILED extractions
- [ ] `ExtractionUploaded` + `ExtractionProcessingStarted` — lifecycle timestamp descriptions
- [ ] `DocumentInPortfolio.properties.output.properties.needsReview` — "Whether this specific document in the portfolio needs human review..."
- [ ] `ExtractionsResponseFiltered.properties.continuation_token` — pagination token description
- [ ] `ExtractionsResponseFiltered.properties.last_evaluated_creation_date` — pagination field description
- [ ] `components.responses.400.content.application/json.schema` + `.properties.message/errors/context` — new JSON error shape on the shared 400

**Changed descriptions:**
- [ ] `AuthTokenResponse.properties.usage` — OLD: `"array"` → NEW: `"Record of each time this token has been used."` (was literally just the word "array")
- [ ] `encodedPdf.properties.document` — expanded from PDF-only to all supported document types
- [ ] `components.parameters.environments` — casing change: `PRODUCTION/DEVELOPMENT` → `production/development` (probably fine, just confirm it matches the enum values)
- [ ] `components.responses.400` — now describes both plain-text and JSON shapes

**Skipping** (clearly correct fixes, no judgment call needed): `DocumentTypeId` ("user-friendly name" → "Unique ID"), `BinaryDocument`, `UploadUrl`, `GeneratedFileUrl`, `ConvertedUrlDocument` (done), `DocumentInPortfolio.output` (done)

### Configuration spec

**New schemas/fields:**
- [ ] `ConfigurationContentType` — "Content type of the stringified `configuration`. Defaults to `application/json`."
- [ ] `ConfigurationVersion.properties.note` — "Optional user-supplied note describing this version."
- [x] `ConfigurationVersion.properties.published_by` — accepted as-is
- [ ] `PutConfiguration.properties.note` — "Optional note describing this version of the configuration."
- [ ] `GoldenResponse.properties.converted_url` — "If present, the URL to GET the PDF Sensible converted this reference document to..."
- [ ] `PostGolden.properties.content_type` — "Content type of the document you'll upload to `upload_url`."
- [ ] `DocumentTypeOutput.properties.review_triggers` properties (4): `coverage_threshold`, `validation_errors_threshold`, `validation_warnings_threshold`, `selected_validations`

**Changed descriptions:**
- [ ] `DocumentTypeOutput.properties.review_triggers` (schema-level) — changed from describing a `string[]` to the real object shape
- [ ] `paths./extract_text_from_golden/{type-name}.post.responses.200` — now mentions the `text` property wrapper
- [ ] `components.responses.204` — now says "empty body and no `Content-Type` header"

**Skipping** (done): `ConfigurationEditor`, `ProcessorType`

### After all description reviews complete

- [ ] Write friction log entries documenting what changed vs Devon's original PR: what was accepted as-is, what was reworded and why, what was omitted with x-internal-notes. Commit to v0.

### Classification spec

- [ ] `BinaryDocument` — same schema as in extraction; "non-encoded document bytes as the entire request body" (brief, likely fine)

### Email spec

**New descriptions:**
- [ ] `DocTypeIds` — "The IDs of the document types Sensible uses to classify each document."
- [ ] Shared 400 `application/json` shape: `.schema`, `.properties.context/errors/message`
- [ ] PUT-specific 400 `application/json` shape: `.schema`, `.properties.context/errors/message`

**Changed descriptions:**
- [ ] `components.responses.400` — now describes the path-validation-specific plain-text response
- [ ] `paths./processors/email/{name}.put.responses.400` — now explains the two content types
