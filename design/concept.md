# API spec drift detection: concept

Status: design. A throwaway prototype validated this approach on 2026-10-12. It found the drift fixed in sensible-docs#748, and its
scripts were deliberately not committed (see [Where it runs](#where-it-runs)). This document is enough to rebuild a
cleaner version.

## Problem

The OpenAPI specs in `reference/` are hand-maintained. Nothing tells you when the backend changes an endpoint,
a parameter, a request field, a response field, or a status code, so the specs drift silently.

## Approach

Generate a **skeleton** OpenAPI description from the backend source, then compare its *structure* to the
hand-maintained specs. Ignore prose (descriptions, examples, summaries). The skeleton is never published. It only
exists to be diffed.

No annotations or decorators are added to the backend. Everything comes from what the code already declares:

| What | Where it comes from in the backend |
| --- | --- |
| Deployed routes (method + path) and their handler | The infra API resource definition: the chain of `.withHandler(name, { handler: "<file>.<export>" })` followed by `.addRoute(method \| [methods], path)` calls. Search for `addRoute(`. |
| Path, query, and body schemas; accepted content types | Each handler's exported `router({ routes, ...options })` call. `routes` maps a path to `{ pathSchema, queryStringSchema, handlers: { METHOD: { bodySchema, contentTypes, func } } }`. Schemas are JSON Schema object literals (a few are Zod). |
| Success response shape | The TypeScript type of the argument passed to `success(x)` in code reachable from the handler's `func`. `success()` takes `unknown`, so the type must be read at the call site with the type checker. |
| Error status codes | Named response constants (`{ statusCode: N, ... }`) reachable from `func`; `errorResponse()` (400) and `conflictResponse()` (409); router behavior driven by route options; and `translateError()`, which maps thrown exceptions to responses for every route. |

Why not a decorator library (tsoa, NestJS Swagger, and so on): the routes are object literals, not classes, so
decorators can't attach to them, and decorators are a second hand-maintained description that drifts the same way.
Why not Zod-to-OpenAPI: almost all schemas are plain JSON Schema, not Zod.

## Architecture

Three stages with a stable intermediate representation (IR) between them. The prototype went straight from code to
OpenAPI with `x-` extensions and then reverse-engineered that in the diff. Don't repeat that.

```
backend source ──extract──▶ routes IR (JSON) ──normalize──▶ facts ◀──normalize── hand specs
                                  │                            │
                                  └──emit──▶ skeleton OpenAPI  └──compare──▶ report (md) + exit code
```

1. **extract** (`ts-morph`, read-only, static): backend → `routes.json`.
2. **normalize**: both the IR and each hand spec → a flat, sorted list of **facts**.
3. **compare**: set comparison of facts plus a severity table → markdown report and exit code.
4. **emit** (optional): IR → skeleton OpenAPI, useful for eyeballing or bootstrapping a new spec.

### Routes IR

One record per deployed method + path:

```json
{
  "method": "POST",
  "path": "/extract/{type}",
  "pathKey": "POST /extract/{}",
  "handler": "<handler file>.<export>",
  "options": { "usageTracked": true, "requirePersistence": false, "anonymous": false },
  "pathParams":  { "schema": { /* JSON Schema */ }, "source": "<file>:<line>" },
  "query":       { "schema": { }, "source": "<file>:<line>" },
  "body":        { "contentTypes": ["application/json", "application/pdf"], "schema": { }, "source": "<file>:<line>" },
  "responses": [
    { "status": 200, "contentType": "application/json", "schema": { }, "typeName": "SingleExtractionResponse", "source": "<file>:<line>" },
    { "status": 400, "name": "MALWARE_SCAN_REQUIRED_RESPONSE", "origin": "handler", "source": "<file>:<line>" },
    { "status": 429, "name": "USAGE_LIMIT_RESPONSE", "origin": "router-option:usageTracked" }
  ],
  "unresolved": [ { "what": "body", "reason": "zod schema", "source": "<file>:<line>" } ]
}
```

Every item carries a `source` (file:line). The prototype only had sources for responses, so verifying a finding by
hand took longer than it should have.

### Facts

Normalize both sides into the same vocabulary, then compare sets:

```
op            POST /extract/{}
pathParamCount POST /extract/{}  1
query         POST /extract/{}  environment  string  optional
reqContentType POST /extract/{} application/pdf
reqField      POST /extract/{}  document            string  required
resField      POST /extract/{}  200 validation_summary.fields  number  optional
resOpen       POST /extract/{}  200 webhook.payload          (no declared shape below this node)
status        POST /extract/{}  400  origin=handler
```

Normalization rules (each of these was a false positive in the prototype):

- **Paths**: replace every `{name}` with `{}`. The spec and code name path params differently (`{type}` against `{document_type}`).
  Compare by count and position, and report name differences as info only.
- **Path-level parameters**: merge `paths[p].parameters` into each operation, and dedupe by `in` + `name` (some
  operations repeat them).
- **Types**: treat `integer` as `number` (TypeScript has no integer); a union of string literals is `string`; drop
  `null` from unions and record it as nullable; `Date` is `string`/`date-time`; `Buffer` is binary.
- **Field paths**: dot notation, with `[]` for array items (`documents[].output.configuration`). Limit depth to 4.
- **`required`**: a field is required only if every `oneOf`/`anyOf` branch requires it *and* every ancestor is
  required.
- **Open nodes**: an object with no `properties`, an array with no `items`, `additionalProperties`, or an
  `unknown`/`any` type. Don't report children *under* an open node on either side. Open on the code side means you
  can't know; open on the spec side means the spec is deliberately loose (for example, a deprecated field documented as
  "empty array").
- **Custom JSON Schema keywords**: query strings are strings on the wire. Map
  `sensible_valid_querystring_number: { kind: "integer" }` to `integer` and so on. Drop other `sensible_*` keywords.
- **Content types**: the router accepts `application/yaml` wherever it accepts JSON bodies. Ignore it unless the
  spec ever documents YAML.

### Severity

| Fact difference | Severity | Why |
| --- | --- | --- |
| Spec has an op that no deployed route has | DRIFT | Documented endpoint doesn't exist |
| Path param count differs | DRIFT | Wrong URL shape |
| Spec has a field or param that the code doesn't, and no open ancestor on the code side | DRIFT | Documented field doesn't exist |
| Code has a **required** request field or query param that the spec omits | DRIFT | Requests built from the docs get a 400 |
| Type mismatch after normalization | DRIFT | |
| Spec lists a status code that no code path returns | DRIFT | |
| Code has an **optional** field, param, or content type that the spec omits | REVIEW | Often intentional, or caused by wide TS types |
| Handler-reachable status code that the spec omits | REVIEW | |
| Global status codes (router or `translateError`) that the spec omits | SUMMARY | Report once with a count, not per op |
| Deployed op in no spec and not in the internal allowlist | REVIEW | Possibly undocumented public endpoint |

Exit code: non-zero if there is any DRIFT that isn't covered by the accepted-differences file. Then it can gate CI.

## Extract stage: implementation notes

Use `ts-morph` with the backend `tsconfig.json`, `skipAddingFilesFromTsConfig: true`, and add files on demand. The
backend's `node_modules` don't need to be installed. Missing external types degrade to `any`, but every type that
matters is local. The full run took about 7 seconds over 114 routes.

### Static evaluator

You need a small evaluator that turns object-literal expressions into plain JSON. It's used for the infra route
table, the router config, and every schema. Cases to handle:

- Literals: string, no-substitution template, number, `true`/`false`/`null`, unary minus.
- Pass-through: `as`, `satisfies`, parentheses, type assertions.
- Object literals: property assignments (quoted, identifier, and **computed** keys such as `` [`/${route}`] ``),
  spreads (merge; record unresolved spreads instead of dropping them), method declarations (treat as functions).
- **Shorthand properties** (`{ routes }`): `getSymbol()` on the name returns the *property*, not the variable. Use
  `nameNode.getDefinitionNodes()[0]` to reach the variable declaration. The prototype missed every router config until
  this was fixed.
- Identifiers: resolve the symbol, follow aliases (`getAliasedSymbol()` for imports), then evaluate the variable
  initializer. Return a `{ $fn: node }` marker for function declarations, arrow functions, and function expressions.
- Property access (`X.y`): evaluate `X` and take `y`; otherwise check for an enum member or property assignment.
- Template literals with spans: concatenate when every span resolves.
- **Factory calls** (for example, a helper that returns `{ routes: {...} }` built from its arguments): resolve the
  callee to a function declaration, bind parameter declarations to argument nodes in an environment map, then evaluate
  the last top-level `return` expression. Identifiers that resolve to a bound `ParameterDeclaration` evaluate the
  bound argument.
- Anything else: `{ $unresolved: "<source text>", source }`. Never guess. If a Zod expression (`z.object(...)`) is
  unresolved, record it as "zod" and treat it as open.
- Embedded JSON Schema `definitions` with `$ref: "#/definitions/X"`: inline them at extraction time, with a recursion
  guard, so the IR schemas are self-contained. Otherwise every `$ref` resolves against the wrong root later.
- Guard against a schema *property* literally named `$ref` (configuration schemas have them). Only treat `$ref` as a
  reference when its value is a string.

### Response types

From each route's `func`, walk the call graph:

- For each `CallExpression`, resolve the callee (use the name node of property-access callees, so that methods
  resolve).
- If the callee is `success` declared in the API `common.ts`, record
  `checker.getTypeAtLocation(arg0)` and the content-type argument. A call with no argument means 204.
- Otherwise, if the callee's declaration is a function, method, or arrow-function variable inside the API source
  tree, recurse. Use a visited set and a depth limit of about 5.

Convert TS types to JSON Schema with your own converter rather than `ts-json-schema-generator`. The type objects are
already in hand, and the converter needs to record *where* types are `unknown`:

- Hoist named types (alias or interface symbol, not `__type`, not generic, declared outside `node_modules`) into
  `components` by name, with a placeholder first to break recursion.
- Object types: `getProperties()`, then `getTypeAtLocation(valueDeclaration)`. Skip properties with call signatures
  (methods aren't serialized). Use `isOptional()` for required-ness and the string index type for
  `additionalProperties`.
- Record every `any`/`unknown` with its context path (route, then field path) in an `untyped` list. Count distinct
  *root* paths. The prototype counted every recursive visit, and its "11,924 untyped spots" was meaningless.

Prototype results: 102 of 114 routes resolved a concrete 200 type and 0 were `unknown` at the top level. The rest
were 204s plus a handful of unresolved routes, which appear as warnings.

### Error codes

- **Handler-reachable**: while walking the call graph, record identifiers matching `^[A-Z][A-Z0-9_]+$` whose
  declaration is a variable with an object-literal initializer (or an arrow function returning one) that has a numeric
  `statusCode`. Also record inline `statusCode: N` property assignments with N ≥ 300, and calls to
  `errorResponse()` and `conflictResponse()`.
- **Router**: the shared validation step returns 400 on schema failure, and returns 415 *only when the handler declares
  `contentTypes`*. Authenticated routes can return 401 and 403. `usageTracked` adds 429, and `requirePersistence`
  adds 400. The auth-route rate limiter adds 429 to auth routes only.
- **Thrown**: analyze `translateError()` once, the same way, and attach its codes to every route with
  `origin: "thrown"`.

## Configuration (private)

Keep all of this out of the public repo:

```yaml
backend: ../sensible
specs: [reference/openapi_extraction.json, reference/openapi_classification.json,
        reference/openapi_configuration.json, reference/openapi_email.json]
internalRoutes:            # deployed, intentionally undocumented: matched by pathKey glob
  - "* /account/**"
accepted:                  # known, reviewed differences, so they don't fail CI
  - fact: "resField GET /documents/{} 200 documents[].output.classificationSummary"
    reason: "TS type omits it; handler re-adds it at runtime. Spec is correct."
    recheck: 2027-01-01
```

`accepted` entries need a reason and a recheck date, so they expire instead of hiding drift forever.

## Known limitations

- **Type differs from runtime.** A narrow type (a storage type that `Omit`s fields the handler adds back) produces
  false "in spec, not in code" findings. A wide type (an async endpoint whose type is the full extraction response
  but which returns a pending stub) produces many optional "missing from spec" REVIEW lines. Neither can be fixed
  statically. Handle them with `accepted`.
- **Validation inside handlers** (manual parsing, value checks such as "expires within 30 days") is invisible. Drift
  there goes undetected.
- **Zod schemas** aren't evaluated statically. Either evaluate them at runtime with `z.toJSONSchema` (this requires
  installing backend deps and importing the module) or treat them as open.
- **Exceptions thrown deep in the engine** are only attributable globally (through `translateError`), not per route.
- **Deep error-code tracing** follows calls only within the API source tree and only to a fixed depth.

## Improvements over the prototype

1. A stable IR between extract and compare, instead of OpenAPI with `x-` fields.
2. Shared normalization for both sides, so the diff doesn't need special cases.
3. A `source` on every IR item, not just responses.
4. A severity table as data, plus an exit code for CI.
5. An `accepted` file with reasons and recheck dates, and an `internalRoutes` allowlist.
6. Correct untyped counting (distinct roots).
7. Deterministic output (sorted keys and facts), so you can diff skeleton snapshots between backend commits. That
   also gives an "API changed since last release" list for changelogs.
8. Tests against a tiny fixture backend that covers each evaluator case above (shorthand, spread, computed key,
   factory call, embedded definitions, Zod, `$ref` property).

## Where it runs

The scripts read backend internals, and their outputs (the full deployed route list, internal endpoints, the
`internalRoutes` allowlist) map the non-public API surface. So:

- **Don't commit the scripts, the IR, the skeleton, the reports, or the config to this public repo.**
- Preferred: a CI job in the private backend repo that fetches the public specs from this repo and comments on any
  backend PR that changes the API surface. That catches drift when it's introduced.
- Fallback: run it locally from a private repo, and fix confirmed drift here in normal docs PRs that describe only
  public behavior.
