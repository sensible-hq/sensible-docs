---
name: sensible-api-spec
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

### 4a. Read an existing spec for JSON format reference

For CRUD-style endpoint groups, `openapi_configuration.json` is the best model. For extraction-style async patterns, use `openapi_extraction.json`.

JSON format patterns to carry forward consistently:
- **OpenAPI version**: `3.0.3`
- **Server**: `{"url": "https://api.sensible.so/v0", "description": "Production server (uses live data)"}`
- **Security**: `bearerAuth` in `components.securitySchemes`, referenced via `security: [{bearerAuth: []}]`
- **operationId**: kebab-case verb-noun (e.g., `get-email-processor`, `list-email-processors`, `upsert-email-processor`)
- **Descriptions**: markdown prose, doc links in `doc:slug` format (e.g., `[quickstart](doc:quickstart)`)
- **`$ref` components**: use for any schema referenced in more than one place
- **Required fields**: declared in the parent `required: [...]` array, not inline
- **Discriminated unions**: model with `oneOf` + `discriminator.propertyName`
- **Error responses**: include at minimum 200, 400, and any endpoint-specific codes (403, 404, 409)

### 4b. Read the Sensible prose style guides

Read both files before drafting any descriptions or excerpt text:

```
/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/writing-rules.md
/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/glossary.md
```

Also read the parameter description guidance in:
```
/home/franceselliott/GitHub/sensible-docs/.claude/style-guide/sentence-word-guidance.md
```
Focus on: "Parameter table: how to write each column" and "Sentence construction". The parameter table conventions don't apply literally (this isn't a SenseML page), but the underlying principles — lead with what it does, explicit subjects, gerunds over nominalizations — apply directly to OpenAPI schema property descriptions and endpoint `description` fields.

---

## Step 5: Draft the spec

### For a new spec file

Write the full OpenAPI 3.0.3 JSON. Structure:
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

Every `description` field in the spec and every `excerpt` in a markdown stub is published prose. Apply the style guides:

- **Terminology** (`glossary.md`): "config" not "template" or "schema"; "output" not "result object"; "Sensible" always capitalized; "the Sensible app" not "the UI"; "null" not "empty"
- **Subjects** (`writing-rules.md`): "Sensible [does X]" for platform behavior; "You [do Y]" for user actions; no passive constructions that hide the actor
- **Gerunds** (`writing-rules.md`): "automates extracting" not "automates the extraction of"
- **Em dashes** (`writing-rules.md`): split compound clauses into two sentences instead
- **Lead with what it does** (`sentence-word-guidance.md`): start schema property descriptions with a verb or noun phrase — "Specifies the webhook URL", "The name of the processor" — not "This field..." or "Use this to..."
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

### 7c. Update `_order.yaml` files

**New top-level section**: Add the new directory name to `reference/_order.yaml`. Ask the user where in the ordering it should appear before writing.

**New subdirectory**: Create `reference/{Section}/_order.yaml` listing subdirectory names.

**New endpoint group**: Create `reference/{Section}/{group}/_order.yaml` listing endpoint page filenames (without `.md` extension).

Read `reference/_order.yaml` before editing to see current ordering:

```bash
cat /home/franceselliott/GitHub/sensible-docs/reference/_order.yaml
```

---

## Quick reference: directory structure example

Look at `reference/Classification/` as the simplest existing example:
- `reference/Classification/_order.yaml` → `[document]`
- `reference/Classification/document/_order.yaml` → `[classify-document, classify-document-sync]`
- `reference/Classification/document/classify-document.md` → frontmatter with `api.file` + `api.operationId`
- `reference/Classification/document/index.md` → just title

Mirror this pattern for new sections.
