# openapi-cleanup friction log

## Accuracy issues found in Devon's PR

### Wrong field name in `review_triggers`: `review_trigger` → `needs_review`

**What Devon's PR said:** Each validation selected to trigger review carries a `review_trigger: true` property. The `Validation` schema had no `review_trigger` field (and `additionalProperties: false`, so it would have blocked it).

**What actually happens:** The backend field is `needs_review`. `src/engine/review-triggers.ts` filters `schema.validations` by `v.needs_review`. Confirmed live: POST `/document_types` with `"needs_review": true` on a validation object was accepted and echoed back correctly.

**How it was caught:** Reading `src/engine/review-triggers.ts` — the field name in the description didn't match the code.

**Fix:** Updated `review_triggers` schema-level description and `selected_validations` to reference `needs_review`. Added `needs_review` as a documented field on `Validation` (was missing entirely).

---

### `processor_type` documented but has no functional effect

**What Devon's PR said:** `processor_type` is a real field on document types with enum `"document" | "email"`, reflecting the kind of processor the doc type belongs to.

**What actually happens:** The field is accepted on POST and echoed back on GET, but is never read by any backend logic to gate behavior or filter operations. It was added during early email processor development (backend commit `2401a0d5`, Jul 2024) and never productized. The email processor validator (`validateDocTypeIds`) only checks whether referenced doc type IDs exist — it does not check `processor_type`.

**How it was caught:** Searching for all usages of `processorType` in the backend — only found in the doc-type module itself (entity, handlers, storage). Never consumed elsewhere. Not present in the frontend app at all.

**Fix:** Omitted from `DocumentType` and `PostDocumentType`. Added `x-internal-note` documenting the deliberate omission. Same treatment as `prevent_file_metadata`.

---

## Wording patterns established

Apply these going forward rather than waiting for correction.

### Simplify descriptions that over-explain

If the reason is self-evident from the rule, drop it.

- `"At least one grant is required -- a token with no grants can't authorize anything."` → `"At least one grant is required for an authorization token."`

### Em dashes in descriptions

Replace ` -- ` with a period and start a new sentence. If the second clause is a pointer, lead with "For more information, see X."

- `"...depending on what caused the failure -- see the two content types below."` → `"...depending on what caused the failure. For more information, see the two content types below."`

### Timing vs. order

"just before X" implies a timing guarantee. Use "prior to X" when the intent is sequencing, not simultaneity.

- `"just before setting the extraction's status to PROCESSING"` → `"prior to setting the extraction's status to PROCESSING"`

### Threshold prepositions

Use "for" not "on" with threshold and bound descriptions.

- `"Inclusive upper bound (0-1) on coverage score"` → `"Inclusive upper bound (0-1) for coverage score"`

### Internal mechanism detail belongs in `x-internal-note`, not the description

The description should say what a field is and what it does for the user. If it describes how the backend implements it (naming conventions, internal transitions, schema extensions), move it to `x-internal-note`.

- `ExtractionSingleRetrievalResponse`: replaced 4-sentence description of WAITING-to-PROCESSING transitions and URL signing with `"Extracted document data from a single-document extraction."` + `x-internal-note`
- `DocumentInPortfolio.output`: replaced camelCase naming explanation with user-facing description + `x-internal-note`
- `ScorePortfolio`: removed "exposes the engine's internal field names" from description; moved to `x-internal-note`

### Clarify abstract field descriptions with structure

If a field's purpose isn't obvious from its name and type alone, add a concrete example or explain the key/value structure.

- `AuthorizationGrant.path`: `"Values for the route's path parameters, keyed by parameter name."` → full explanation with example showing `{"id": "<extraction-id>"}` for route `/documents/{id}`
- `last_evaluated_creation_date`: `"The 'created' date-time of the last extraction in this page of results."` → `"The creation date of the last extraction on this page of results (find this value in an extraction's 'created' parameter)."`

### Point users to GET /documents/{id} from sync endpoint descriptions

Sync endpoints don't return all fields (no download URLs, no top-level error). Add a note at the end of sync endpoint descriptions pointing to `GET /documents/{id}` for the full picture.

### Align parallel schemas

When two schemas represent the same concept (e.g. `Score` and `ScorePortfolio`), align first sentences and note differences explicitly.

- `ScorePortfolio` first sentence aligned to `Score`: `"The score for the extraction, used to help choose the best extraction."`. Added: `"Unlike the single-document extraction Score, includes a coverage field."`
- `ScorePortfolio.score`: added missing fingerprint-fallback sentence from `Score.value`
