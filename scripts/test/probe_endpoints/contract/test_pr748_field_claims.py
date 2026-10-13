"""Live checks for the request and response field changes in sensible-docs#748.

Each test reads the claim from the spec in reference/ (not a hard-coded copy),
then checks it against the live API using the test account:

- POST /account/auth_tokens: `expires` is a documented, required request field.
- ReviewStatuses: an array with one status (or null) per portfolio document.
- GET /extractions: the response no longer includes `cutoff_date`.

Run from the repo root (-s shows each request, its response, and what to expect):
  python3 -m pytest scripts/test/probe_endpoints/contract -v -s --report-chars=s
To check #748's specs before it merges, point CONTRACT_SPEC_DIR at its reference/ folder.
The key comes from SENSIBLE_TEST_API_KEY in the environment, or from the
gitignored .env at the repo root (see conftest.py).

Side effects: test_auth_token_expires creates one auth token that expires 15
minutes later. test_review_statuses_is_array_per_document runs one portfolio
extraction of assets/pdfs/portfolio.pdf. Error-code changes in the same PR (404, 415) aren't tested here.
"""

import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

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

PORTFOLIO_PDF = Path(__file__).resolve().parents[4] / "assets" / "pdfs" / "portfolio.pdf"
PORTFOLIO_TYPES = ["auto_insurance_quotes", "loss_run_reports"]  # docs/document extraction/portfolio.md


@pytest.mark.docs_impact(
    change="Changed ReviewStatuses from a string to an array of nullable strings.",
    where="reference/openapi_extraction.json > components.schemas.ReviewStatuses "
          "(used by MultiExtractionSummaryResponse and ExtractionPortfolioRetrievalResponse)",
    pages="API reference: List extractions (ref:list-extractions) and Retrieve extraction "
          "(ref:retrieving-results); guide sample in docs/document extraction/portfolio.md, "
          "which already shows an array",
    if_pass="Correct as published. A live portfolio extraction returns an array with one status per "
            "document, matching the spec and the portfolio guide's sample.",
    if_fail="The spec is wrong. Compare the printed `reviewStatuses` with the schema: fix the item enum, "
            "nullability, or array type. If the count doesn't match `documents`, fix the ReviewStatuses "
            "description too.",
    if_skip="Unverified live. The test account is missing the portfolio document types. Create them from "
            "scripts/test/probe_endpoints/contract/fixtures/portfolio/, then rerun.",
)
def test_review_statuses_is_array_per_document(api, specs):
    spec = specs["extraction"]
    review_schema = spec["components"]["schemas"]["ReviewStatuses"]

    # Claim 1: the spec documents an array.
    assert review_schema.get("type") == "array", "spec doesn't document ReviewStatuses as an array"

    # Every portfolio extraction has reviewStatuses: one entry per document, "NEEDS_REVIEW" or null
    # (backend src/api/extract/entity.ts:876). The loss_run_reports fixture has a coverage review
    # trigger, so this portfolio should return a mix of null and "NEEDS_REVIEW".
    expect("HTTP 200 with an extraction `id` and an `upload_url` (its signed query is redacted here). "
           f"A 400 means the test account lacks one of {PORTFOLIO_TYPES}; the test then skips.")
    status, created = api.request("POST", "/generate_upload_url",
                                  query={"document_name": "contract_test_portfolio"},
                                  body={"types": PORTFOLIO_TYPES, "content_type": "application/pdf"})
    if status == 400:
        pytest.skip(f"The test account can't run this portfolio: {created}")
    assert status == 200, f"POST /generate_upload_url returned {status}: {created}"

    expect(f"HTTP 200. Uploads {PORTFOLIO_PDF.name} from this repo's assets/pdfs.")
    assert api.upload(created["upload_url"], PORTFOLIO_PDF, "application/pdf") == 200

    expect("Polls GET /documents/{id} quietly until the extraction is COMPLETE (up to 3 minutes), then "
           "prints the final response. It contains `documents` (two auto_insurance_quotes and one "
           "loss_run_reports) and `reviewStatuses` with one entry per document: null for the quotes, "
           "\"NEEDS_REVIEW\" for the loss run.")
    for _ in range(36):
        status, full = api.request("GET", f"/documents/{created['id']}", quiet=True)
        if status == 200 and full.get("status") in ("COMPLETE", "FAILED"):
            break
        time.sleep(5)
    status, full = api.request("GET", f"/documents/{created['id']}")
    assert full.get("status") == "COMPLETE", f"extraction didn't complete: {full.get('status')}"

    # Claim 2: on retrieval, reviewStatuses matches the schema, with one entry per document.
    statuses = full.get("reviewStatuses")
    assert statuses is not None, "retrieval has no reviewStatuses"
    assert schema_errors(spec, review_schema, statuses) == []
    assert len(statuses) == len(full.get("documents", [])), (
        f"{len(statuses)} statuses for {len(full.get('documents', []))} documents")

    # Claim 3: the List extractions summary for the same extraction has the same shape.
    expect("HTTP 200. The newest extraction in the list is this portfolio, with the same `reviewStatuses`.")
    status, page = api.request("GET", "/extractions", {"limit": 5})
    assert status == 200
    summary = next((e for e in page.get("extractions", []) if e["id"] == created["id"]), None)
    assert summary is not None, "the new portfolio extraction isn't in the first page of List extractions"
    assert schema_errors(spec, review_schema, summary.get("reviewStatuses")) == []
    assert summary["reviewStatuses"] == statuses


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
