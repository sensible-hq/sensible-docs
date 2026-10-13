"""Live checks for the request and response field changes in sensible-docs#744.

Each test reads the claim from the spec in reference/ (not a hard-coded copy),
then checks it against the live API using the test account:

- POST /account/auth_tokens: `expires` is a documented, required request field.
- ReviewStatuses: an array with one status (or null) per portfolio document.
- GET /extractions: the response no longer includes `cutoff_date`.

Run from the repo root (-s shows each request, its response, and what to expect):
  python3 -m pytest scripts/test/probe_endpoints/contract -v -s --report-chars=s
The key comes from SENSIBLE_TEST_API_KEY in the environment, or from the
gitignored .env at the repo root (see conftest.py).

Side effect: test_auth_token_expires creates one auth token that expires 15
minutes later. Error-code changes in the same PR (404, 415) aren't tested here.
"""

from datetime import datetime, timedelta, timezone

import pytest

from conftest import schema_errors


def expect(text: str) -> None:
    """Print what the next request should show. Visible with pytest -s."""
    print(f"\n>>> EXPECT: {text}")


def _first_extraction_id(api) -> str:
    status, body = api.request("GET", "/extractions", {"limit": 1})
    assert status == 200, f"GET /extractions returned {status}: {body}"
    if not body.get("extractions"):
        pytest.skip("The test account has no extractions to grant access to.")
    return body["extractions"][0]["id"]


# ── expires on POST /account/auth_tokens ─────────────────────────────────────

@pytest.mark.docs_impact(
    change="Added `expires` to the request body and marked it required.",
    where="reference/openapi_extraction.json > paths./account/auth_tokens.post.requestBody",
    pages="API reference: Get token for review link (ref:account-auth-tokens)",
    if_pass="Correct as published. The API requires `expires`, accepts the documented body, and its "
            "response matches AuthTokenResponse. No docs change needed.",
    if_fail="The spec is wrong. If the POST without `expires` returned 200, remove `expires` from "
            "`required`. If the POST with `expires` failed or its response didn't validate, fix the "
            "request schema, its example, or AuthTokenResponse to match the printed response.",
    if_skip="Unverified: the test account has no extraction to build a grant from. Run any extraction "
            "on the test account, then rerun.",
)
def test_auth_token_expires(api, specs):
    spec = specs["extraction"]
    request_schema = spec["paths"]["/account/auth_tokens"]["post"]["requestBody"]["content"][
        "application/json"]["schema"]
    response_schema = spec["components"]["schemas"]["AuthTokenResponse"]

    # Claim 1: the spec documents `expires` and marks it required.
    assert "expires" in request_schema["properties"], "spec doesn't document `expires`"
    assert "expires" in request_schema.get("required", []), "spec doesn't mark `expires` required"

    print("\n=== test_auth_token_expires: `expires` is a documented, required request field ===")
    expect("HTTP 200 with an `extractions` list. The test only uses the first extraction's `id`, "
           "to build a grant for the auth token.")
    extraction_id = _first_extraction_id(api)
    grants = [{"route": "/documents/{id}", "method": "GET", "path": {"id": extraction_id}}]
    expires = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat(timespec="milliseconds")
    expires = expires.replace("+00:00", "Z")

    # Claim 2: a body with `expires` matches the documented request schema and succeeds.
    body = {"grants": grants, "expires": expires}
    assert schema_errors(spec, request_schema, body) == []
    expect("HTTP 200. The request body has `grants` and `expires` (15 minutes from now). The response "
           "has `token`, `created`, `expires` (the value you sent), `grants`, and `usage` (empty). "
           "The `token` is a live credential for the test account until it expires.")
    status, resp = api.request("POST", "/account/auth_tokens", body=body)
    assert status == 200, f"POST with expires returned {status}: {resp}"
    assert schema_errors(spec, response_schema, resp) == [], "response doesn't match AuthTokenResponse"
    assert "expires" in resp

    # Claim 3: the API rejects a body without `expires`, as the spec's `required` says.
    expect("HTTP 400. Same request without `expires`, so the API's validation rejects it. The body is a "
           "validation error that names `expires` as missing. A 200 here would mean the spec is wrong.")
    status, resp = api.request("POST", "/account/auth_tokens", body={"grants": grants})
    assert status == 400, f"POST without expires returned {status}, expected 400: {resp}"


# ── ReviewStatuses is an array, one entry per portfolio document ─────────────

@pytest.mark.docs_impact(
    change="Changed ReviewStatuses from a string to an array of nullable strings.",
    where="reference/openapi_extraction.json > components.schemas.ReviewStatuses "
          "(used by MultiExtractionSummaryResponse and ExtractionPortfolioRetrievalResponse)",
    pages="API reference: List extractions (ref:list-extractions) and Retrieve extraction "
          "(ref:retrieving-results); guide sample in docs/document extraction/portfolio.md, "
          "which already shows an array",
    if_pass="Correct as published. Live portfolio extractions return an array with one status per "
            "document, matching the spec and the portfolio guide's sample.",
    if_fail="The spec is wrong. Compare the printed `reviewStatuses` with the schema: fix the item enum, "
            "nullability, or array type. If the count doesn't match `documents`, fix the ReviewStatuses "
            "description too.",
    if_skip="Unverified live. The docs change rests on the backend source review only. The test account "
            "has no portfolio extraction. Run one (any portfolio gets reviewStatuses, with null entries "
            "when nothing needs review), then rerun.",
)
def test_review_statuses_is_array_per_document(api, specs):
    spec = specs["extraction"]
    review_schema = spec["components"]["schemas"]["ReviewStatuses"]

    # Claim 1: the spec documents an array.
    assert review_schema.get("type") == "array", "spec doesn't document ReviewStatuses as an array"

    print("\n=== test_review_statuses_is_array_per_document: ReviewStatuses is an array, "
          "one entry per portfolio document ===")
    # Every portfolio extraction has reviewStatuses: one entry per document, "NEEDS_REVIEW" or null
    # (backend src/api/extract/entity.ts:876). Don't filter by review_statuses: that would drop
    # portfolios whose entries are all null.
    portfolios, token = [], None
    for _ in range(5):
        query = {"limit": 100, **({"continuation_token": token} if token else {})}
        expect("HTTP 200 with a page of extractions. Portfolio extractions show `reviewStatuses` as an "
               "array such as [\"NEEDS_REVIEW\", null]; single-document extractions don't have it.")
        status, body = api.request("GET", "/extractions", query)
        assert status == 200, f"GET /extractions returned {status}: {body}"
        portfolios += [e for e in body.get("extractions", []) if "reviewStatuses" in e]
        token = body.get("continuation_token")
        if portfolios or not token:
            break
    if not portfolios:
        pytest.skip("The test account has no portfolio extractions in its recent history.")

    for summary in portfolios[:3]:
        # Claim 2: the list summary's reviewStatuses matches the documented schema.
        errors = schema_errors(spec, review_schema, summary["reviewStatuses"])
        assert errors == [], f"summary {summary['id']}: {errors}"

        # Claim 3: on retrieval, there's one status per document in the portfolio.
        expect("HTTP 200 with the full portfolio extraction. `reviewStatuses` has exactly as many "
               "entries as `documents`, each one APPROVED, NEEDS_REVIEW, REJECTED, or null.")
        status, full = api.request("GET", f"/documents/{summary['id']}")
        assert status == 200, f"GET /documents/{summary['id']} returned {status}"
        statuses = full.get("reviewStatuses")
        assert statuses is not None, f"{summary['id']}: retrieval has no reviewStatuses"
        assert schema_errors(spec, review_schema, statuses) == []
        assert len(statuses) == len(full.get("documents", [])), (
            f"{summary['id']}: {len(statuses)} statuses for {len(full.get('documents', []))} documents")


# ── cutoff_date removed from GET /extractions ────────────────────────────────

@pytest.mark.docs_impact(
    change="Removed the deprecated `cutoff_date` field from the response.",
    where="reference/openapi_extraction.json > components.schemas.ExtractionsResponseFiltered",
    pages="API reference: List extractions (ref:list-extractions)",
    if_pass="Correct as published. Production doesn't return `cutoff_date`, and every top-level field it "
            "does return is documented. No docs change needed.",
    if_fail="The spec is wrong. If `cutoff_date` came back, restore it in ExtractionsResponseFiltered. "
            "If the failure lists other undocumented top-level fields, document them there.",
    if_skip="Unverified: the API couldn't be reached with the test key. Check SENSIBLE_TEST_API_KEY and rerun.",
)
def test_list_extractions_has_no_cutoff_date(api, specs):
    spec = specs["extraction"]
    response_schema = spec["components"]["schemas"]["ExtractionsResponseFiltered"]

    # Claim 1: the spec no longer documents cutoff_date.
    assert "cutoff_date" not in response_schema["properties"]

    print("\n=== test_list_extractions_has_no_cutoff_date: GET /extractions no longer returns cutoff_date ===")
    expect("HTTP 200. Top-level fields are only `extractions`, `continuation_token`, and possibly "
           "`last_evaluated_creation_date`. No `cutoff_date` anywhere at the top level.")
    status, body = api.request("GET", "/extractions", {"limit": 5})
    assert status == 200, f"GET /extractions returned {status}: {body}"

    # Claim 2: the API doesn't return it.
    assert "cutoff_date" not in body

    # Claim 3: every top-level field the API returns is documented, and the body matches the schema.
    undocumented = sorted(set(body) - set(response_schema["properties"]))
    assert undocumented == [], f"undocumented top-level fields: {undocumented}"
    assert schema_errors(spec, response_schema, body) == []
