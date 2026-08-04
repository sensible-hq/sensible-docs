# API Error Response Source of Truth

Reference for verifying and updating error response schemas in `reference/openapi_*.json`.
All paths are relative to `~/GitHub/sensible`.

---

## The core rule

**Plain text vs JSON is determined by which code path fires, not by the endpoint.**

- `errorResponse()` (`src/api/common.ts:243-271`) → always **JSON**: `{ message, errors?, context? }`
- Named constants (e.g. `NO_CONTENT_TYPE_RESPONSE`, `NOT_FOUND`) → always **plain text**

The spec got these wrong historically because authors guessed from docs rather than reading the code. Every time you document a 400 or 403, verify which path actually fires.

---

## Single source of truth: `src/api/common.ts`

Every error constant and both core response functions live here. Check this file first.

### `errorResponse()` — lines 243–271
- Status: **400**
- Format: **JSON**
- Shape: `{ "message": "string", "errors": [...], "context": {...} }`
- Triggered by: `validation/index.ts:920-923` (accumulates schema validation failures), and any handler that calls `errorResponse()` directly for business logic failures

### `success()` — lines 273–326
- Status: **200** with data, **204** with no data (empty body, no Content-Type header)
- Live-confirmed: `DELETE /document_types/{id}` returns 204 with empty body and no Content-Type header

### Plain-text 400 constants

| Constant | Lines | Body text | When fired |
|---|---|---|---|
| `NO_CONTENT_TYPE_RESPONSE` | 519–523 | "Must provide the Content-Type header" | `validation/index.ts:784` — fires *before* schema validation, only for endpoints that require a Content-Type header |
| `BAD_CONTENT_TYPE` | 328–332 | "Bad Content-Type" | `validation/index.ts:903` |
| `MISMATCHED_CONTENT_TYPE` | 333–337 | "Mismatched Content-Type" | `validation/index.ts:914` |
| `MISSING_PATH_PARAM` | 338–342 | "Missing path parameter" | Path param validation |
| `MISSING_QUERY_PARAM` | 343–347 | "Missing query parameter" | Query param validation |
| `INVALID_BODY` | 348–352 | "Invalid body" | Body validation failure |
| `PDF_MISSING` | 428–432 | "PDF is required" | Missing document |
| `PASSWORD_PROTECTED_PDF_RESPONSE` | 438–442 | "Document is password protected" | PDF processing |

### Plain-text 401/403 constants

| Constant | Lines | Body text | When fired |
|---|---|---|---|
| `UNAUTHORIZED_RESPONSE` | 353–357 | "Unauthorized" | `checkAuthentication()` — missing auth |
| `FORBIDDEN_RESPONSE` | 358–362 | "Forbidden" | `checkAuthentication()` — invalid token type or insufficient permissions |
| `FEATURE_NOT_ACTIVATED_RESPONSE` | 363–367 | "Feature not activated" | `router.ts:533` (no enabled aliases) and `checkAuthentication()` |
| `ALREADY_SIGNED_IN` | 368–372 | "Already signed in" | Anonymous endpoint receives auth token |

> **Example of past spec error**: Email processor 403 was documented as "This endpoint requires at least one active account alias." but `FEATURE_NOT_ACTIVATED_RESPONSE` literally says "Feature not activated". Always copy the exact string from the constant, not from memory.

### Plain-text 404 constant

| Constant | Lines | Body text |
|---|---|---|
| `NOT_FOUND` | 373–377 | "Not found" |

### 429 responses (two different shapes)

| Source | Lines | Status | Format | Body |
|---|---|---|---|---|
| `USAGE_LIMIT_RESPONSE_FROM_ACCOUNT()` | 408–415 | 429 | Plain text | Plan-dependent: "Free tier usage limit exceeded" or "Plan usage limit exceeded" |
| Rate limiter in `router.ts` | 237–260 | 429 | **JSON** | `{ "error": "Rate limit exceeded" }` with `Retry-After` header |

> The 429 has two different formats depending on which limit is hit. The spec must document both.

### 409 conflict

| Function | Lines | Format | Body |
|---|---|---|---|
| `conflictResponse()` | 229–235 | Plain text | "Conflict" |

---

## Validation flow: `src/api/validation/index.ts`

`validateEvent()` (lines 761–946) orchestrates all request validation in order:

1. Path params → accumulates into `accErrors[]`
2. Query params → accumulates into `accErrors[]`
3. Content-Type required? → throws `NO_CONTENT_TYPE_RESPONSE` (plain text, stops here)
4. Content-Type in allowed list? → throws 415 plain text (stops here)
5. Body vs Zod schema → accumulates into `accErrors[]`
6. `checkAuthentication()` → throws 401/403 constants (plain text, stops here)
7. If any `accErrors`: throws `errorResponse(accErrors, context)` → **JSON 400**

**Key implication**: A path-validation 400 always produces JSON (step 1 accumulates then step 7 fires), not plain text. The spec previously documented these as plain text — that was wrong.

`checkAuthentication()` (lines 654–730): throws only plain-text constants; never calls `errorResponse()`.

---

## Router middleware: `src/api/router.ts`

Fires in `handleEvent()` (lines 479–564) before the route handler:

| Line | Check | Error thrown |
|---|---|---|
| 516 | Quota exceeded | `USAGE_LIMIT_RESPONSE_FROM_ACCOUNT(account)` — 429 plain text |
| 525 | Persistence not enabled | `PERSISTENCE_NONE_RESPONSE` — 400 plain text |
| 533 | `requireAliases: true` + no enabled aliases | `FEATURE_NOT_ACTIVATED_RESPONSE` — 403 plain text |

---

## Module-specific: email processor

**`src/api/processors/email/handler.ts`**
- Router configured with `requireAliases: true` (lines 79–82) → 403 "Feature not activated" if no enabled aliases
- `upsertProcessorHandler()` calls `validateDocTypeIds()` (line 40); if missing doc types, calls `errorResponse(...)` → **JSON 400**
- GET/DELETE handlers return `NOT_FOUND` (plain text) if processor not found

**`src/api/processors/email/schemas.ts`**
- Zod schema `processorUpsertSchema` (lines 43–54) is the source of truth for PUT request body validation — schema failures produce JSON 400 via `errorResponse()`
- Two distinct PUT 400 failure modes: missing Content-Type header (plain text, `NO_CONTENT_TYPE_RESPONSE`) vs body/path validation (JSON, `errorResponse()`)

**`src/api/processors/email/validator.ts`**
- `validateDocTypeIds()` (lines 32–41) — validates referenced doc type IDs exist; failures produce JSON 400

---

## Module-specific: configuration API

**`src/api/doc-type/configuration-handlers.ts`**
- Business logic 400s go through `errorResponse()` → JSON
- Shared 204 response for DELETE is empty body with no Content-Type header (live-confirmed)

---

## Where to look when the code changes

| If this changes... | Check here |
|---|---|
| Any error message string | `src/api/common.ts` — named constants (lines 328–442) |
| JSON error body shape | `src/api/common.ts:243-271` (`errorResponse`) |
| Validation error accumulation | `src/api/validation/index.ts:920-923` |
| Auth/permission errors (401/403) | `src/api/validation/index.ts:654-730` (`checkAuthentication`) |
| Router-level quota/alias enforcement | `src/api/router.ts:516,525,533` |
| Rate limit response shape | `src/api/router.ts:237-260` |
| Email processor body validation | `src/api/processors/email/schemas.ts` (Zod schema) |
| Email processor business logic errors | `src/api/processors/email/handler.ts:40-42`, `validator.ts:32-41` |
| 204 no-content behavior | `src/api/common.ts` (`success()` lines 273–326) |
| Configuration API errors | `src/api/doc-type/configuration-handlers.ts` |
