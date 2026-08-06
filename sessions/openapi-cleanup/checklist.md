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
- [x] `ExtractionErrorMessage` — accepted as-is
- [x] `ExtractionUploaded` + `ExtractionProcessingStarted` — accepted; changed "just before" to "prior to" in ExtractionUploaded
- [x] `DocumentInPortfolio.properties.output.properties.needsReview` — accepted as-is
- [x] `ExtractionsResponseFiltered.properties.continuation_token` — accepted as-is
- [x] `ExtractionsResponseFiltered.properties.last_evaluated_creation_date` — reworded for clarity
- [x] `components.responses.400.content.application/json.schema` + `.properties.message/errors/context` — accepted as-is

**Changed descriptions:**
- [x] `AuthTokenResponse.properties.usage` — accepted as-is
- [x] `encodedPdf.properties.document` — accepted as-is
- [x] `components.parameters.environments` — casing confirmed correct; accepted as-is
- [x] `components.responses.400` — updated: replaced em dash with period, added "For more information"

**Skipping** (clearly correct fixes, no judgment call needed): `DocumentTypeId` ("user-friendly name" → "Unique ID"), `BinaryDocument`, `UploadUrl`, `GeneratedFileUrl`, `ConvertedUrlDocument` (done), `DocumentInPortfolio.output` (done)

### Configuration spec

**New schemas/fields:**
- [x] `ConfigurationContentType` — accepted as-is
- [x] `ConfigurationVersion.properties.note` — accepted as-is
- [x] `ConfigurationVersion.properties.published_by` — accepted as-is
- [x] `PutConfiguration.properties.note` — accepted as-is
- [x] `GoldenResponse.properties.converted_url` — accepted as-is
- [x] `PostGolden.properties.content_type` — accepted as-is
- [x] `DocumentTypeOutput.properties.review_triggers` properties (4) — updated: "on" → "for"; `selected_validations` clarified to "when the user configures specific validations to trigger review"

**Changed descriptions:**
- [x] `DocumentTypeOutput.properties.review_triggers` (schema-level) — updated: "includes a parameter" → "contains a property"
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
