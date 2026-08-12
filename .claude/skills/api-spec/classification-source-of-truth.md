# Classification API Source of Truth

Reference for verifying and updating `reference/openapi_classification.json`.
All paths are relative to `~/GitHub/sensible`.

---

## The core rule

**`reference_documents` and `classification_summary` are arrays, not objects.** These were mistyped as objects in the old spec. Both are typed as `ClassificationScore[]` in the backend.

---

## Request body shapes

### doctype query parameter

- **File**: `src/api/classify/classify.ts` or the classification handler
- Type: **string** (a single document type name), not an array
- Example format: `?doctype=auto_insurance_quotes` — not comma-separated, not an array

> **Past spec error**: The spec had the wrong type (array) and wrong example format. It is a single string.

---

## Response body shapes

### Classification response

- **File**: `src/api/classify/classify.ts:19-73`
- **Type**: `ClassificationOutput`
- Key fields:
  - `reference_documents: ClassificationScore[]` — **array**, not object
  - `classification_summary: ClassificationScore[]` — **array**, not object

> **Past spec error**: Both fields were typed as `object` (schema type: object). They are arrays of `ClassificationScore` items.

### BinaryDocument (shared schema for file upload)

- Shared across classification and extraction specs
- Source of truth: whichever handler accepts the binary body — check the `contentTypes` field on the route config in the classification handler

---

## Where to look when the code changes

| If this changes... | Check here |
|---|---|
| Classification response shape | `src/api/classify/classify.ts` (`ClassificationOutput` type) |
| `reference_documents` / `classification_summary` types | `src/api/classify/classify.ts:19-23` |
| Accepted file types for classification | Classification handler `contentTypes` field |
| `doctype` query param type/format | Classification handler query param schema |
