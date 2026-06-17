---
name: api-spec
description: Creates or updates OpenAPI JSON spec files in the /reference directory of sensible-docs, based on backend PRs from sensible-hq/sensible. Use this skill whenever the user provides PR numbers or GitHub URLs from the backend repo and wants to document new API endpoints, update existing endpoint schemas, or add new fields to an existing API reference. Also triggers when the user mentions "new API", "update the spec", "API reference from PRs", "write a spec for [feature]", or provides a list of PRs and asks to document them. This skill handles the end-to-end workflow: reading PRs, extracting API surface changes from diffs and Zod/TypeScript schemas, drafting OpenAPI 3.0.3 JSON, creating supporting markdown files, and updating _order.yaml navigation files.
---

# Sensible API Spec Skill

**Docs repo**: `sensible-hq/sensible-docs` (local: `/home/franceselliott/GitHub/sensible-docs`)  
**Backend repo**: `sensible-hq/sensible`  
**Spec files**: `reference/openapi_*.json`  
**New spec naming**: `reference/openapi_{domain}.json` (e.g., `openapi_email.json`)

---

## Step 1: Parse input, fetch PR titles, confirm

Accept PR numbers or GitHub URLs from `sensible-hq/sensible`. Fetch titles in parallel:

```bash
gh pr view <number> --repo sensible-hq/sensible --json number,title,mergedAt
```

Present a structured summary before doing any more work:

```
## PRs — please confirm before I continue

- [#3237](https://github.com/sensible-hq/sensible/pull/3237) — "email processors - endpoints - part 1" (merged 2026-02-17)
- [#3242](https://github.com/sensible-hq/sensible/pull/3242) — "email processors - endpoints - part 2" (merged 2026-04-01)

Proceed?
```

Wait for confirmation before continuing.

---

## Step 2: Fetch full PR context

For each confirmed PR, fetch body and diff in parallel:

```bash
gh pr view <number> --repo sensible-hq/sensible --json title,body,mergedAt,labels
gh pr diff <number> --repo sensible-hq/sensible
```

From body and diff, extract:
- New route paths and HTTP methods (look for `.addRoute(`, handler files, router config)
- Request body schemas (look for `schemas.ts`, Zod schema definitions, `z.object(`, `z.union(`, `z.discriminatedUnion(`)
- Response shapes (look for `mappers.ts`, response type exports, integration test response body assertions)
- New path/query/header parameters
- New error codes and the conditions that trigger them
- Changes to existing endpoints — new fields in request or response

**The diff is the ground truth.** PR bodies explain intent; diffs show what actually shipped. When they conflict, trust the diff.

**Skip**: import reordering, test helper utilities, CI config, internal refactors that don't change any route or schema.

---

## Step 3: Categorize changes and flag mixed PRs

Sort each discovered change into one of three buckets:

**New spec** — new route paths that don't exist in any current spec (e.g., `/processors/email/*`). These will become a new `openapi_{domain}.json` file.

**Update existing spec** — new fields, parameters, or response codes added to routes already documented in an existing spec. Current specs and their route coverage:
- `openapi_extraction.json` — `/extract/*`, `/generate_upload_url/*`, `/retrieve/*`
- `openapi_classification.json` — `/classify/*`
- `openapi_configuration.json` — `/document_types/*`, `/configurations/*`, `/reference_documents/*`
- `sensible.json` — `/generate/*` (document generation), and miscellaneous account endpoints like `/account`

**Mixed PR** — a single PR that does both. Flag this explicitly before proceeding:

```
⚠️  PR #3237 touches two categories:
- New routes (/processors/email) → new spec: openapi_email.json
- Existing endpoint (GET /account, adding fields: aliases, domain) → update sensible.json

I'll handle both. Continuing...
```

After categorizing all PRs, state clearly:
- Which new spec file(s) you'll create and what they'll contain
- Which existing spec file(s) you'll update and what changes you'll make

Ask for any corrections before drafting.

---

## Step 4: Read reference material before drafting

Do this before writing a single line of the spec. Read in parallel.

### 4a. Read the spec template and schema reference

Read the annotated template before writing anything:
```
/home/franc/GitHub/sensible-docs/.claude/skills/api-spec/openapi_template.jsonc
```

Also read the spec structure reference to understand existing schema relationships before drafting any changes:
```
/home/franc/GitHub/sensible-docs/.claude/skills/api-spec/api-code-reference.md
```

Use the schema relationship trees in `api-code-reference.md` to:
- Identify which existing schemas a new field or endpoint touches
- Avoid duplicating schemas that are already shared (e.g. `ExtractionSummaryBase`, `PortfolioBase`)
- Wire new schemas into the correct inheritance chain rather than creating standalone duplicates
- Confirm which endpoint response shapes are used by the list endpoint vs the retrieval endpoint vs the async pending response

The template is the primary reference. It covers:
- All structural decisions (operationId naming, path parameter placement, `$ref` usage, `additionalProperties`, discriminated unions, error code selection, `x-internal-note`)
- Prose style rules embedded directly in the description fields (sentence case summaries, full sentence vs. noun phrase, trailing period rule, active voice, backtick formatting, `doc:slug` links, multi-step numbered lists, enum casing)

Use it as a skeleton — copy the relevant sections and replace placeholders. For a real-world example of CRUD-style endpoints, also read `openapi_configuration.json`. For async extraction patterns, read `openapi_extraction.json`.

### 4b. Read the Sensible prose style guides

Read both files before drafting any descriptions or excerpt text:

```
/home/franc/GitHub/sensible-docs/.claude/style-guide/writing-rules.md
/home/franc/GitHub/sensible-docs/.claude/style-guide/glossary.md
```

Also read the parameter description guidance in:
```
/home/franc/GitHub/sensible-docs/.claude/style-guide/sentence-word-guidance.md
```
Focus on: "Parameter table: how to write each column" and "Sentence construction". The parameter table conventions don't apply literally (this isn't a SenseML page), but the underlying principles — lead with what it does, explicit subjects, gerunds over nominalizations — apply directly to OpenAPI schema property descriptions and endpoint `description` fields.

---

## Step 5: Draft the spec

### For a new spec file

Start from `openapi_template.jsonc` — copy the relevant sections and replace placeholders. Do not reconstruct the skeleton from scratch. The template's structure and comments are the spec for how to write the spec.

The top-level structure:
1. `openapi`, `servers`, `info`, `security` — top matter
2. `tags` — one tag per logical group of endpoints
3. `paths` — all new routes, each with operations for every supported method
4. `components` — reusable schemas, parameters, request bodies, security scheme

For discriminated union request bodies (e.g., `bodySpec`/`attachmentSpecs` with multiple `kind` values), use `oneOf` with a `discriminator`:

```json
"attachmentSpec": {
  "oneOf": [
    { "$ref": "#/components/schemas/SingleDocTypeSpec" },
    { "$ref": "#/components/schemas/ClassificationSpec" },
    { "$ref": "#/components/schemas/PortfolioSpec" }
  ],
  "discriminator": { "propertyName": "kind" }
}
```

### For an update to an existing spec

Locate the relevant path object and schema definitions. Add new fields to the right schema object. Don't remove or rename anything already present — existing clients depend on it.

### Prose quality in descriptions

Every `description` field in the spec and every `excerpt` in a markdown stub is published prose. The template encodes the API-reference-specific rules (sentence case, full sentence vs. noun phrase, trailing periods, active voice, backtick formatting, `doc:slug` links). The style guides cover Sensible-specific terminology and voice:

- **Terminology** (`glossary.md`): "config" not "template" or "schema"; "output" not "result object"; "Sensible" always capitalized; "the Sensible app" not "the UI"; "null" not "empty"
- **Subjects** (`writing-rules.md`): "Sensible [does X]" for platform behavior; "You [do Y]" for user actions; no passive constructions that hide the actor
- **Gerunds** (`writing-rules.md`): "automates extracting" not "automates the extraction of"
- **Em dashes** (`writing-rules.md`): split compound clauses into two sentences instead
- **Terse and precise**: no filler ("please note that", "it's important to remember")

The `excerpt` in each markdown stub should be copied from the endpoint's `description` in the spec, not rewritten.

### Showing the draft

Present the full draft before writing any files. For specs longer than ~150 lines, show the structure summary and key sections (all path operations + main component schemas), then ask if the user wants to see the full JSON before you write it.

---

## Step 6: Review with user

> "Does this look right? Any changes before I write the files?"

Incorporate feedback. Do not write any files until the user explicitly approves.

---

## Step 7: Write files and update navigation

### 7a. Write the spec

For a new spec, write to `reference/openapi_{domain}.json`.  
For an update, edit the specific object(s) in the existing spec file.

### 7b. Create the endpoint markdown pages (new specs only)

Each endpoint needs a markdown file so readme.com can render it. Follow this structure for a new domain (example: Email Processors):

```
reference/
  Email Processors/
    _order.yaml              ← lists subdirectory names
    index.md                 ← group title page
    email-processor/
      _order.yaml            ← lists endpoint page filenames (no .md)
      index.md               ← subgroup title page
      list-email-processors.md
      get-email-processor.md
      upsert-email-processor.md
      delete-email-processor.md
```

Each endpoint markdown page uses this frontmatter:

```markdown
---
title: <Human-readable endpoint title>
excerpt: >
  <One or two sentence description of what this endpoint does.>
api:
  file: openapi_{domain}.json
  operationId: <operationId from the spec>
hidden: false
---
```

The `excerpt` here should match the `description` in the spec — copy it, don't paraphrase.

`index.md` files just need `title` and `hidden`:

```markdown
---
title: Email processors
hidden: false
---
```

### 7c. Update `api-code-reference.md`

If the changes add new paths, rename schemas, change the inheritance hierarchy, or add new fields to existing response schemas, update the relevant spec structure section in `api-code-reference.md`. Keep the paths table and schema relationship tree in sync with the actual spec file.

If the change is a minor description edit or a new property on a leaf schema (not a base/shared schema), no update is needed.

### 7d. Update `_order.yaml` files

**New top-level section**: Add the new directory name to `reference/_order.yaml`. Ask the user where in the ordering it should appear before writing.

**New subdirectory**: Create `reference/{Section}/_order.yaml` listing subdirectory names.

**New endpoint group**: Create `reference/{Section}/{group}/_order.yaml` listing endpoint page filenames (without `.md` extension).

Read `reference/_order.yaml` before editing to see current ordering:

```bash
cat /home/franceselliott/GitHub/sensible-docs/reference/_order.yaml
```

---

## Step 8: Generate test scripts from the spec

After writing the spec, generate one curl script per endpoint. Save to `scripts/test/{domain}/` (e.g., `scripts/test/email_processor/`).

**Template**: copy from `references/curl_script_template.sh` in this skill directory. All scripts must follow this template exactly — it contains the HTTP status code capture, JSON pretty-print with raw fallback, and timestamped output file pattern.

**Naming**: convert `operationId` from kebab-case to snake_case for the filename (e.g., `get-email-processor` → `get_email_processor.sh`).

**Adapting the template per method**:

| Method | Path params | Request body | Notes |
|--------|-------------|--------------|-------|
| GET (list) | none | none | Remove `-H "Content-Type"` and `-d` lines |
| GET (single) | optional arg: `NAME=${1:-default}` | none | Remove `-H "Content-Type"` and `-d` lines |
| PUT / POST | optional or required arg | include `-d` block with full example body | Use realistic placeholder values from the spec's examples or known test data |
| DELETE | required arg: `NAME=${1:?Usage: ...}` | none | Remove `-H "Content-Type"` and `-d` lines; response body will be empty on 204 |

After writing all scripts, confirm with the user:
```
Scripts written to scripts/test/{domain}/:
  - list_{domain}.sh
  - get_{name}.sh
  - upsert_{name}.sh
  - delete_{name}.sh

Run them to generate output before Step 9.
```

---

## Step 8b: Compare against backend tests before writing edge case scripts

Before writing error-case or edge-case scripts, check what the backend test suite already covers so curl scripts extend coverage rather than duplicate it. Run:

```bash
gh pr diff <number> --repo sensible-hq/sensible | grep -E "test|spec|describe|it\(" | head -60
```

Or search the backend repo for test files related to the new endpoints:

```bash
gh api repos/sensible-hq/sensible/git/trees/main?recursive=1 \
  | python3 -c "import json,sys; [print(f['path']) for f in json.load(sys.stdin)['tree'] if 'test' in f['path'] and 'email' in f['path']]"
```

**What backend unit/integration tests typically cover (skip these in curl scripts):**
- Schema validation errors: missing required fields, invalid enum values, wrong types, empty arrays where minItems > 0
- These are caught at the Zod/schema layer before any route logic runs

**What curl scripts should add (not covered by backend tests):**
- End-to-end happy paths for every valid input variation (each `kind` variant, optional fields present vs omitted, multiple webhooks)
- Ordering and positional constraints the schema cannot enforce (e.g., `EnvironmentWebhook` must not be first in the webhooks array — validators pass, only the API catches it)
- 404 behavior for GET/DELETE on nonexistent resources — backend service may be a no-op; route-level behavior needs verification
- Any behavior the spec explicitly flags as "schema validators will not catch this"

**Script naming convention for error/edge cases:**
- `upsert_{variant}.sh` — valid body variation (expect 200/201)
- `error_{scenario}.sh` — intentionally invalid input (expect 4xx); include a comment stating the expected HTTP code and why

---

## Step 9: Update spec examples from real API output

Once the user has run the scripts and output files exist in `scripts/test/{domain}/outputs/`, read the most recent output file for each GET/LIST endpoint and use the real response data to populate `example` values in the spec.

**What to update**:
- Response schema `example` fields for 200 responses
- Request body `example` fields for PUT/POST operations, if the GET output reveals realistic field values (e.g., real IDs, real processor names)

**What not to update**:
- Any `example` that already contains a real-looking value (non-placeholder)
- Error response examples (400, 404, etc.) — keep these as minimal illustrative examples

**Process**:
1. Read output files: `scripts/test/{domain}/outputs/list_*.json` and `get_*.json` (most recent timestamp)
2. Identify fields in the response that map to schema properties
3. Update `example` values in `components/schemas` in the spec JSON
4. Show a diff summary of what changed before writing: "Updating X example fields in Y schemas"
5. Write the updated spec

---

## Quick reference: directory structure example

Look at `reference/Classification/` as the simplest existing example:
- `reference/Classification/_order.yaml` → `[document]`
- `reference/Classification/document/_order.yaml` → `[classify-document, classify-document-sync]`
- `reference/Classification/document/classify-document.md` → frontmatter with `api.file` + `api.operationId`
- `reference/Classification/document/index.md` → just title

Mirror this pattern for new sections.

---

## Pre-publish checklist

Before finalizing any spec, verify each item. Add new items here as they're discovered.

### Text edits
- [ ] **Grep before committing**: Before committing any text change, grep the whole spec file for all instances of the pattern you're replacing — not just the one you found. A single phrase like "extracts against" can appear in schema descriptions, property descriptions, and examples across the file.

### Naming consistency
- [ ] **Casing convention**: Compare every new field name against existing specs. Sensible's extraction API uses `snake_case` (e.g. `segment_documents_with`, `ocr_engine`). If a new endpoint uses `camelCase` for the same concept, flag it as a potential inconsistency and confirm with eng before publishing. Do not silently document the inconsistency — surface it.
- [ ] **Enum values**: Compare enum values against `src/common.ts` (`OCR_ENGINE_TYPES`) and `src/engine/types.ts` (`portfolioSplittingMethodSchema`) — do not invent or omit values.

### Semantic consistency
- [ ] For each new parameter, search existing specs for a parameter with the same meaning. If one exists, verify the name, type, and allowed values match. If they differ, document the discrepancy and ask for a decision.
- [ ] Cross-reference shared types (see `api-code-reference.md`) — `OcrEngineType`, `PortfolioSplittingMethod`, webhook shapes — to ensure the spec reflects the actual backend types.

### Error responses
- [ ] For every endpoint, verify the error codes it actually returns by reading the handler in the backend repo. Do not assume 400/401/404/500 are present — confirm each one. A missing or spurious error code in the spec is misleading to API consumers.

### Docs gaps
- [ ] Run `grep -n "ocrEveryPage\|ocr_every_page\|ocrEngine\|ocr_engine" src/api/*/handler.ts` in the backend repo to check whether any request params accepted by the backend are missing from the spec. Document intentional omissions as TODOs.
- [ ] **x-internal-note audit**: Run `grep -rn "x-internal-note" reference/openapi_*.json` to list all intentionally undocumented params across existing specs. For each, check whether the new endpoint accepts the same param — if it does, apply the same omission decision (hide it, add an `x-internal-note`) rather than accidentally documenting it.

### Template review
- [ ] After the spec is finalized, check whether any decisions made during this session (new patterns, edge cases, corrections) should be added to `openapi_template.jsonc`. Update the template before closing out.

### Known open questions (as of 2026-05)
See `api-code-reference.md` for the full list. Current blockers:
1. `segmentDocumentsWith` (email API) vs `segment_documents_with` (extraction API) — casing inconsistency, pending eng confirmation
2. Default OCR engine for portfolio extraction via email API
3. Whether `microsoft5` and `pdf` should be publicly exposed in `ocrEngine`
4. Whether `ocr_engine` and `ocr_every_page` on portfolio extraction endpoints should be added to `openapi_extraction.json`
