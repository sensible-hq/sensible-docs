# XLSB / spreadsheet upload bugs found while documenting sensible-hq/sensible#3474

**TL;DR:** XLSB works through upload URLs, but `POST /extract`, `/classify`, and `/classify/async`
reject raw XLS, XLSM, and XLSB bodies with "Missing request body". The cause is that the API
Gateway `binaryMediaTypes` list in `gatewayV1.ts` omits all three, which has been true since XLS
and XLSM support shipped. The fix is to add three content types to that list. Separately,
`/classify` rejects CSV because its handler reads only binary bodies, and content type checks
are case-sensitive, so `macroEnabled` (the casing Python sends) gets a 415.

Tested against production (`https://api.sensible.so/v0`) on 2026-10-12 by the docs team.
Repro: `bash scripts/test/file_types/smoke_test_xlsb.sh` in sensible-hq/sensible-docs
(branch `fe_xlsb_docs`, PR sensible-docs#741). Sample: `tests/data/test.xlsb` from #3474.

## Smoke test results

The smoke test runs 13 checks and prints this table at the end, flagging any check whose
result differs from the 2026-10-12 baseline. The sections below explain each bug.

| # | What it sends | Today | After fix | What it shows |
| --- | --- | --- | --- | --- |
| 1 | XLSB → `POST /classify` | ❌ 400 Missing request body | 400 No match found* | Bug 1 (gateway) |
| 2 | XLSB → `POST /classify/async`, then poll `download_link` | ❌ 400 Missing request body; poll skipped | 200 with link; poll returns No match found* | Bug 1 |
| 3 | XLSB → `POST /extract/cells` | ❌ 400 Missing request body or body.document | 200 COMPLETE | Bug 1 |
| 4 | XLSB reference document: create, upload, check, delete | ✅ processed, deleted | same | Reference document upload works |
| 5 | XLSX → `/classify` (control) | ✅ reaches the engine* | same | Baseline: XLSX works |
| 6 | XLSX bytes declared as XLSM → `/classify` (control) | ❌ 400 Missing request body | No match found* | XLSM broken too, so the bug predates XLSB |
| 7 | XLSB bytes declared as XLSX → `/classify` (control) | ✅ reaches the engine* | same | The engine reads XLSB fine |
| 8 | XLSX bytes declared as XLS → `/classify` (control) | ❌ 400 Missing request body | No match found* | XLS broken too |
| 9 | XLSB declared as `macroEnabled` (capital E) → `/classify` | ❌ 415 | same as check 1 after its fix | Bug 3 (case-sensitive) |
| 10 | CSV → `/classify` | ❌ 400 Missing request body | No match found* | Bug 2 (classify ignores text bodies) |
| 11 | CSV → `/extract/cells` | ✅ 200 COMPLETE | same | Contrast with 10: `/extract` reads CSV |
| 12 | XLSB → `generate_upload_url`, upload, retrieve | ✅ COMPLETE, 2 pages | same | Workaround: async extraction |
| 13 | XLSB as base64 JSON → `/extract/cells` | ✅ COMPLETE, 2 pages | same | Workaround: sync extraction |

\* For classification, "No match found" means the request reached the engine: the sample isn't
an invoice or bank statement, so there's no type to match.

Fixing Bug 1 should turn checks 1, 2, 3, 6, and 8 into passes. Check 9 also needs Bug 3's fix,
and check 10 needs Bug 2's. Each run uses 4 extraction credits (checks 3, 11, 12, and 13).

## Bug 1: Sync endpoints drop XLS, XLSM, and XLSB request bodies (high)

**Symptom:** `POST /extract/{type}`, `POST /classify`, and `POST /classify/async` with a binary
body and content type `application/vnd.ms-excel`, `...sheet.macroenabled.12`, or
`...sheet.binary.macroenabled.12` return HTTP 400 `Missing request body` (or
`Missing request body or body.document` from `/extract`).

**Evidence:**

| Request | Result |
| --- | --- |
| XLSB bytes, XLSB content type, `/extract/cells` | 400 Missing request body or body.document |
| XLSB bytes, XLSB content type, `/classify`, `/classify/async` | 400 Missing request body |
| XLSX bytes, **XLSM** content type, `/classify` | 400 Missing request body |
| XLSX bytes, **XLS** content type, `/classify` | 400 Missing request body |
| XLSX bytes, XLSX content type, `/classify` | reaches engine (No match found) |
| **XLSB bytes, XLSX content type**, `/extract/cells` | 200 COMPLETE, page_count 2 |
| XLSB via `generate_upload_url` + PUT, and via `extract_from_url` | COMPLETE, content_type XLSB, page_count 2 |
| XLSB reference document (`POST /document_types/{id}/goldens` + PUT) | processed, no error |

The engine reads XLSB fine; only binary bodies with these three content types fail, and the
upload-URL routes (which skip API Gateway's body handling) work.

**Cause:** `packages/infra-stage-ephemeral/infra/gatewayV1.ts` sets `binaryMediaTypes` to PDF,
JPEG, PNG, TIFF, XLSX, DOC, and DOCX only. XLS, XLSM, and XLSB are missing, so API Gateway
doesn't base64-pass those bodies and the handler sees no buffer. #3474 added XLSB to every
app-level allowlist but not to this list. XLS and XLSM were already broken the same way, so
this predates #3474.

**Fix:** add `application/vnd.ms-excel`, `application/vnd.ms-excel.sheet.macroenabled.12`, and
`application/vnd.ms-excel.sheet.binary.macroenabled.12` to `binaryMediaTypes`. Consider
deriving the list from `CONTENT_TYPES_HANDLED_BY_ENGINE` in `src/common.ts` so the next format
can't miss it. Re-run the smoke test; [1], [2], [3], [6], [8] should pass.

## Bug 2: `/classify` rejects CSV bodies (medium)

**Symptom:** `POST /classify` with a real CSV body and `Content-Type: text/csv` returns 400
`Missing request body`. The same CSV to `POST /extract/cells` returns 200 COMPLETE.

**Cause:** CSV isn't in `binaryMediaTypes`, so it arrives as a text body. The extract handler's
`parseDocument` (`src/api/extract/handler.ts`) handles a string body with
`Buffer.from(body, "utf8")`. The classify handler's `sniffBuffer`
(`src/api/classify/handler.ts`) uses only the decoded binary buffer and throws
`MISSING_BODY_RESPONSE` when it's absent.

**Fix:** give the classify handler the same string-body branch as `parseDocument`, or add
`text/csv` to `binaryMediaTypes` (check that extract's string path still works if you do).
The spec and the Supported file types page both say CSV classification is supported.

## Bug 3: Content type check is case-sensitive (low–medium)

**Symptom:** `Content-Type: application/vnd.ms-excel.sheet.binary.macroEnabled.12` (capital E)
returns HTTP 415, listing the lowercase form as allowed. Same for XLSM.

**Why it matters:** media types are case-insensitive (RFC 9110 §8.3.1). The capital-E form is
the IANA-registered casing and what clients generate: Python's `mimetypes.guess_type("a.xlsb")`
and `/etc/mime.types` both return `...binary.macroEnabled.12`. A Python integration that sets
the content type from the filename gets a 415.

**Fix:** lowercase the content type before validating, everywhere it's checked. After Bug 1's
fix, also confirm whether API Gateway's `binaryMediaTypes` match is case-sensitive.

## Worth a look (unverified)

`DOCUMENT_CONTENT_TYPE_FOR_EXTENSIONS` in `src/common.ts` maps `".xls"` to the XLSX content
type (`...spreadsheetml.sheet`), not `application/vnd.ms-excel`. It's used by the email
processor and `src/processors/entities/{matcher,task}.ts`, so `.xls` email attachments may be
typed as XLSX. Not tested; the sniffer may correct it.

## Known limitation or bug? (checked 2026-10-12)

- **Specs:** no `x-internal-note` or description restricts content types on the sync routes.
  The extraction and classification request bodies list XLS and XLSM (and now XLSB) as
  binary bodies with no caveat. The internal notes cover other topics (malware scan, undocumented
  fields, camelCase).
- **Docs:** Supported file types marks spreadsheet formats as supported for single-file
  extraction with SDKs or API and for classification by type. `classify.md` says nothing about
  file types.
- **Engine history:** XLS (sensible#2739, 2024-12) and XLSM (sensible#3100, 2025-10) each changed
  the app-level allowlists but neither touched the gateway's `binaryMediaTypes` (then in
  `serverless.yml`). Neither PR mentions sync routes, the gateway, or a limitation. That points to
  an oversight repeated three times, not a decision.
- **Bug 3 caveat:** the spec enums list only the lowercase form, so a strict reading is
  "send it lowercase." HTTP says media types are case-insensitive, so this is still a bug, but
  the weakest of the three.

## Customer workaround until Bug 1 is fixed

Send XLS, XLSM, and XLSB files with `generate_upload_url` or `extract_from_url`. For sync
`/extract`, the documented base64 option works: JSON body `{"document": "<base64>",
"content_type": "application/vnd.ms-excel.sheet.binary.macroenabled.12"}` returned COMPLETE,
page_count 2. Only the raw-bytes body fails. Classification has no upload-URL route, so XLS,
XLSM, XLSB, and CSV classification has no workaround.
