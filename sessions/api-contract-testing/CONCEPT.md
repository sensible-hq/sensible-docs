# Concept: API contract testing

Status: draft · started 2026-10-01 · session `doc-detective` (second terminal) · branch `doc-detective-getting-started-tests` (PR #737)

Related: [docs-as-tests concept](../../sessions/docs-as-tests/CONCEPT.md) on `doc-detective-poc` (#725), which tests SenseML examples. This concept tests the API reference.

## The idea

From *Docs as Test & AI*: contract testing checks that both sides of an API agree on the interface. Does the documented endpoint exist? Does it accept the documented parameters? Does the response match the documented shape? Each check is binary and automatable.

For Sensible it's a three-way check, because there are three artifacts and one source of truth:

```
            code (sensible-hq/sensible)  ← source of truth
                 │
        leg 1    │  does the spec describe what the code does?
                 ▼
   spec  (reference/openapi_*.json in this repo)
                 │
        leg 2    │  does the published reference show the spec?
                 ▼
   published API reference  (docs.sensible.so/reference, rendered by ReadMe)
                 │
        leg 3    │  does the real API behave the way the published reference says?
                 ▼
   live API  (api.sensible.so)
```

When all three legs hold, the API reference is telling the truth. AI-written specs make this more urgent: a common failure is a plausible parameter or response field that doesn't exist.

**Starting scope:** one endpoint, the sync extraction, `POST /extract/{document_type}` (operationId `extract-data-from-a-document`, in `reference/openapi_extraction.json`). Its reference page, `reference/Extraction/document-1/extract-data-from-a-document.md`, is only frontmatter pointing at the operation, so **everything on the page is rendered from the spec**.

---

## Leg 1: code ↔ spec

Research 2026-10-01, from reading and running the backend code in a throwaway clone. This repo is public, so code references are kept out of it. See [codegen-report.md](codegen-report.md) for the API-level differences; the full version is outside the repo.

- **The backend doesn't generate an API spec today.** The public spec is hand-maintained.
- **Generating one is feasible** (shown 2026-10-01):
  - **response:** the backend's existing schema generator produced a full JSON Schema of the extraction response, after a one-line change;
  - **request:** the backend's request-validation schemas and allowed Content-Types are importable;
  - **routes:** declared in infrastructure code.
- **Existing backend tests check behavior, not the response shape.** Nothing validates responses against a schema.
- **Approach:** generate a bare-bones OpenAPI file from the backend, then compare it with `reference/` using an allowlist of deliberate omissions. It runs where the backend source is available: this repo's CI with read access, or the backend's CI.

---

### How much work is auto-generating a spec from the backend? (estimate, 2026-10-01)

Not measured end to end; based on what the backend has and lacks.

- **Has:**
  - JSON Schema request validation for most endpoints;
  - named, exported response types for most endpoints;
  - routes declared in one place;
  - a schema generator already in use.
- **Lacks:**
  - any link from a route to its response type (handlers aren't typed with their response);
  - typed error responses (plain-text messages mapped to status codes centrally);
  - standard equivalents for the custom validation keywords.

| Goal | Effort |
|---|---|
| **A. Structure-only spec for contract testing:** paths, params, request and response models, no prose. A mapping file for the ~42 documented operations, an assembler script, small backend changes (export body schemas, fix the odd type the generator can't read) | **About 2–4 days.** The extraction spec's ~10 operations first, roughly 1 day |
| **B. The backend as the spec's source of truth:** generated on every build, with hand-written descriptions merged in | **A 1–2 week engineering project,** plus ongoing discipline |

**Recommendation: A.** It's enough for leg 1, and it doesn't change how anyone works: descriptions and examples stay hand-written in `reference/`.

### How the comparison works (deterministic, rules-based)

No LLM. The same two inputs always give the same result.

1. **Resolve references** on both sides (`$ref` into `components/schemas` or `definitions`). Cut recursive types and mark them.
2. **Normalize the two dialects into one form:**
   - OpenAPI 3.0 `nullable` and the generator's `anyOf [X, null]` both become "or null";
   - maps (`additionalProperties`) count as objects, and tuple `items` as arrays;
   - merge `allOf`;
   - drop prose (descriptions, examples, `x-*`).
3. **Flatten into paths:** `.` for properties, `[]` for array items, such as `classification_summary[].score.penalties`. Each path records its type, enum values and required status.
4. **Compare path by path with explicit rules:**

| Situation | Rule |
|---|---|
| Path in both | Compare type families: `integer` = `number` (TypeScript has no integer); map = object; enums as **sets**; formats ignored |
| Only in the backend | Undocumented field: an error unless allowlisted |
| Only in the spec | **Documented field that doesn't exist (hallucination): always an error** |
| Required in the backend, not in the spec | The spec should mark it required |

5. **Direction matters.**
   - **Responses:** the spec must be a subset of the backend.
   - **Requests:** the spec must not accept what the backend rejects. A *stricter* spec, like today's `environment` enum, is a warning, not an error.
6. **Allowlist:** a checked-in list of deliberate omissions and known equivalences, each with a reason. For example `version_id` and `batchId`, and fields that only `GET /documents/{id}` returns.

**First result (prototype, sync extraction response model):**
- 51 paths match;
- 2 real type differences: `environment` (string vs. enum) and `errors[].type` (enum vs. string);
- 49 paths exist only in the backend, mostly nested under undocumented or GET-only fields;
- **0 exist only in the spec.**

**The prototype's known weak spots**, to fix before relying on it:
- unions use only the first object branch;
- it stops at 5 levels;
- it compares text labels instead of structured nodes;
- it ignores request vs. response direction;
- it has no allowlist yet.

**The real version:** about 200 lines of structured comparison, with no depth limit, branch-by-branch unions, direction-aware rules, an allowlist and an HTML view. Prove it with unit tests on hand-made schema pairs, including ones that must fail.

**Off-the-shelf alternative:** wrap the generated schema in a minimal OpenAPI document and run **oasdiff**. It's deterministic and mature, but it answers "is this a breaking API change?", not "do the docs match the implementation?". Useful as a second opinion.

---

## Leg 2: spec ↔ published reference

Two parts, both deterministic and cheap.

### 2a. Is ReadMe serving the spec in the repo?

- **How specs reach ReadMe** (ReadMe v2 API, `GET /v2/branches/stable/apis`, using `README_API_KEY`):

  | File | Source | Last updated in ReadMe |
  |---|---|---|
  | `openapi_classification.json` | `bidi` (git sync) | 2026-08-04 |
  | `openapi_configuration.json` | `bidi` | 2026-08-06 |
  | `openapi_email.json` | `bidi` | 2026-08-06 |
  | `openapi_extraction.json` | `bidi` | 2026-09-15 |
  | `sensible.json` | `apidesigner` (edited in ReadMe, **not** git-synced) | 2025-11-20 |

- **Check:** fetch `GET /v2/branches/stable/apis/openapi_extraction.json` and compare `data.schema` with `reference/openapi_extraction.json` on `v0`, keys sorted.
- **Result 2026-10-01: identical.** Both copies were last updated 2026-09-15 (repo commit `f9d028e42`).
- **Risk to watch:** `sensible.json` is edited in ReadMe's API Designer, so it can drift from `reference/sensible.json` in the repo with no sync to catch it. *(Which pages use `sensible.json` is not yet checked.)*

### 2b. Does the rendered page show that spec?

- ReadMe serves each reference page as Markdown: `https://docs.sensible.so/reference/extract-data-from-a-document.md` (public, `text/markdown`, linked from `llms.txt`). **It embeds the operation's spec JSON.** A test can parse that JSON and compare it with the repo spec. That's deterministic, needs no browser, and is what AI agents reading the docs actually see.
- Optional: a Doc Detective browser test on the HTML page that `find`s each documented parameter and response field. It only matters if we suspect ReadMe's renderer drops things. Lower priority.

---

## Leg 3: published reference ↔ live API

### What Doc Detective offers (read from its docs and source, v4.38.1)

- Register a spec under `integrations.openApi`, or point a step at it with `httpRequest.openApi.descriptionPath`. Reference the operation by `operationId`.
- `validateAgainstSchema`: `request`, `response`, `both` (default), or `none`. It validates with **plain Ajv** after resolving `$ref`s (`core/openapi.js`, `core/tests/httpRequest.js`).
- `useExample`: build the request from the spec's examples. `mockResponse: true` returns the spec's example instead of calling the API, which **validates the docs' own examples against the schema** without spending an extraction.
- Authentication is manual: it doesn't read `securitySchemes`. Set `openApi.headers.Authorization: "Bearer $SENSIBLE_TEST_API_KEY"`.

### Experiment, 2026-10-01: Doc Detective against the live sync endpoint

Setup: the test account, document type `layout_basics`, `1_extract_your_first_data.pdf` sent as base64 JSON (`{"document": ...}`), spec = `reference/openapi_extraction.json` from `v0`. Each run cost 1 extraction.

| Run | Result | Why |
|---|---|---|
| `validateAgainstSchema: "both"` | **FAIL:** request body "must be string" | Doc Detective validates the request against the **first** content type in `requestBody` (`application/pdf`, a binary string), not the one we sent (`application/json`) |
| `"response"`, path parameter in `request.parameters` | **400** "Specified document type does not exist" | Doc Detective called `/extract/senseml_basics`. It filled `{document_type}` from the **spec's example** and ignored our `request.parameters.document_type` |
| `"response"`, explicit `url` | **PASS:** 200, "Response data matched the OpenAPI schema" | |

### Why a schema PASS isn't enough here (necessary but insufficient)

`ExtractionSyncResponse` declares **no `required` fields and doesn't set `additionalProperties: false`**. So schema validation passes when documented fields are missing *and* when undocumented fields appear. The live response vs. the spec:

| Field | Spec | Live response |
|---|---|---|
| `version_id` | not documented (deliberate, per `x-internal-note`) | present |
| `reviewStatus`, `postprocessorOutput` | documented as situational | absent |
| everything else (20 fields) | documented | present, types match |

So leg 3 needs a **field-level comparison** on top of schema validation:

- every documented field appears, or is on an allowlist of situational fields with the condition written down;
- every returned field is documented, or is on an allowlist of deliberate omissions (`version_id`, and `batchId` from the `/extract/batch/*` API);
- types, `format`s and `enum`s match, using an OpenAPI-aware validator (handles `nullable`, registers formats).

---

## Tools by leg

| Tool | What it does | Fits |
|---|---|---|
| **Spectral** | Lints an OpenAPI file against rules: examples must validate, required fields, descriptions, no `x-internal-note` in published specs (custom rule) | Spec quality; runs on every PR, no secrets |
| **oasdiff** | Structural diff between two OpenAPI files, flags breaking changes | Leg 1, if the code can generate a spec; leg 2a as a stricter diff |
| **Doc Detective** | `httpRequest` + `openApi` against the live API; `mockResponse` to check examples; browser `find` on rendered pages | Leg 3 (with the workarounds above); leg 2b (browser variant) |
| **Schemathesis** | Generates many requests from the spec (property-based), checks responses conform | Leg 3 negative paths (400/401/415 shapes). **Every request is a real extraction**: only cheap or error paths, with a cap |
| **Prism** | Mock server, or a validating proxy, from the spec | Checking examples; optional |
| **Custom Python** (like `run_examples.py`) | The field-level comparison, the allowlists, the ReadMe API fetch, parsing the `.md` page | Leg 2a, 2b, and leg 3's comparison |

Likely shape: **Spectral** on PRs for spec quality, a **Python runner** for legs 2a, 2b and leg 3's field comparison, and **Doc Detective** as the orchestrator and reporter, as with the getting-started tests. Leg 1's tool depends on the code research.

---

## Findings so far

1. **`x-internal-note` values are publicly readable.** The published `.md` page and the downloadable spec include them; ReadMe hides them only in the HTML view. **Decided 2026-10-01:** keep the notes inline in the spec and make them acceptable for external readers, though they aren't written for them. They may be fine as they are. Review the ones that cite backend source paths (7 across the extraction and email specs) and remove those paths.
2. **The documented Try It value doesn't exist for new accounts.** The `document_type` description and example say to use `senseml_basics`. The test account, created 2026-09-30, has `layout_basics`, `llm_basics` and `tutorial`. Calling `/extract/senseml_basics` returns `400 "Specified document type does not exist"`. *To verify: whether older accounts still have `senseml_basics`.*
3. **The response schema can't catch missing or extra fields** (see leg 3).
4. **The `created` example has no timezone** (`2022-10-31T16:27:53.433`). The API returns `…Z`. A strict `date-time` check would reject the docs' own example; Spectral's example validation would catch it.
5. **Doc Detective validates the request against the first content type,** so this endpoint needs `validateAgainstSchema: "response"` (or the spec lists `application/json` first).
6. **Doc Detective fills path parameters from the spec's example, not `request.parameters`.** Workaround: set `url` explicitly. *To check whether this is a Doc Detective bug worth reporting upstream.*
7. **Doc Detective records the resolved `Authorization` header in its results files,** so the API key ends up in plain text. The `run.sh` scrub covers it.
8. **Doc Detective's validator is plain Ajv:** no OpenAPI 3.0 `nullable`, and no visible format registration. Not a problem for this endpoint's 200 response today. *Not tested with a `null` field yet.*
9. **Spec vs. code mismatches** (leg 1 table): the `environment` enum is stricter than the code; YAML and xlsb uploads are undocumented; `document_name` limits, 302/413 large-response behavior and the 415 body text are undocumented.
10. **An engineering bug turned up while reading the backend.** Details are kept out of this public repo; report it to engineering.

---

## Open questions

1. ~~Does the `sensible` code generate a schema of its API?~~ No (leg 1). Is engineering open to generating one with the schema generator they already use?
2. ~~Strip `x-internal-note` from published specs?~~ Decided: keep them inline and make them acceptable for external readers (finding 1).
3. Should the deliberate omissions (`version_id`, `batchId`) and situational fields live as allowlists in this repo, or as `x-` annotations in the spec itself?
4. Live calls cost extractions on the test account. Is roughly 1 extraction per endpoint per run acceptable, and how often: on spec changes only, or weekly?
5. Where should leg 1 run: in this repo's CI (needs read access to `sensible`), or in the `sensible` repo's CI (needs this repo's spec)?
6. Start with `openapi_extraction.json` only, then the other `bidi` specs? And what about `sensible.json` (API Designer)?

## Next steps

- [x] Fill in leg 1 from the code research (2026-10-01)
- [ ] Build the real leg 1 comparison (structured, direction-aware, allowlist, unit tests), starting with the extraction spec (goal A)
- [ ] Ask engineering about goal A's small backend changes (export body schemas, generator-friendly types) and about CI access to the backend
- [ ] Verify the leg 1 mismatches against the live API where it's cheap (errors don't create extractions): `environment=foo`, a YAML body, a 257-character `document_name`, a missing Content-Type
- [ ] Report the engineering bug (finding 10) to engineering, privately
- [ ] Review the `x-internal-note` values that cite backend source paths and remove the paths (finding 1)
- [ ] Prototype leg 2a + 2b for `openapi_extraction.json`: ReadMe API fetch + `.md` page parse, compared with `v0`
- [ ] Prototype leg 3's field-level comparison for the sync endpoint, with allowlists, run from Doc Detective
- [ ] Try Spectral with a starter ruleset (validate examples, flag `x-internal-note`) on `openapi_extraction.json`
- [ ] Check finding 2 against an older account; check finding 6 against Doc Detective's issues
- [ ] Decide on the open questions above
