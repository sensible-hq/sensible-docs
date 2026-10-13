"""Live checks for the request and response field changes in sensible-docs#744.

Each test reads the claim from the spec in reference/ (not a hard-coded copy),
then checks it against the live API using the test account:

- POST /account/auth_tokens: `expires` is a documented, required request field.
- ReviewStatuses: an array with one status (or null) per portfolio document.
- GET /extractions: the response no longer includes `cutoff_date`.

Run:
  SENSIBLE_TEST_API_KEY=... python -m pytest scripts/test/probe_endpoints/contract -v

Side effect: test_auth_token_expires creates one auth token that expires 15
minutes later. Error-code changes in the same PR (404, 415) aren't tested here.
"""

from datetime import datetime, timedelta, timezone

import pytest

from conftest import schema_errors


def _first_extraction_id(api) -> str:
    status, body = api.request("GET", "/extractions", {"limit": 1})
    assert status == 200, f"GET /extractions returned {status}: {body}"
    if not body.get("extractions"):
        pytest.skip("The test account has no extractions to grant access to.")
    return body["extractions"][0]["id"]


# ── expires on POST /account/auth_tokens ─────────────────────────────────────

def test_auth_token_expires(api, specs):
    spec = specs["extraction"]
    request_schema = spec["paths"]["/account/auth_tokens"]["post"]["requestBody"]["content"][
        "application/json"]["schema"]
    response_schema = spec["components"]["schemas"]["AuthTokenResponse"]

    # Claim 1: the spec documents `expires` and marks it required.
    assert "expires" in request_schema["properties"], "spec doesn't document `expires`"
    assert "expires" in request_schema.get("required", []), "spec doesn't mark `expires` required"

    extraction_id = _first_extraction_id(api)
    grants = [{"route": "/documents/{id}", "method": "GET", "path": {"id": extraction_id}}]
    expires = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat(timespec="milliseconds")
    expires = expires.replace("+00:00", "Z")

    # Claim 2: a body with `expires` matches the documented request schema and succeeds.
    body = {"grants": grants, "expires": expires}
    assert schema_errors(spec, request_schema, body) == []
    status, resp = api.request("POST", "/account/auth_tokens", body=body)
    assert status == 200, f"POST with expires returned {status}: {resp}"
    assert schema_errors(spec, response_schema, resp) == [], "response doesn't match AuthTokenResponse"
    assert "expires" in resp

    # Claim 3: the API rejects a body without `expires`, as the spec's `required` says.
    status, resp = api.request("POST", "/account/auth_tokens", body={"grants": grants})
    assert status == 400, f"POST without expires returned {status}, expected 400: {resp}"


# ── ReviewStatuses is an array, one entry per portfolio document ─────────────

def test_review_statuses_is_array_per_document(api, specs):
    spec = specs["extraction"]
    review_schema = spec["components"]["schemas"]["ReviewStatuses"]

    # Claim 1: the spec documents an array.
    assert review_schema.get("type") == "array", "spec doesn't document ReviewStatuses as an array"

    status, body = api.request(
        "GET", "/extractions", {"review_statuses": "APPROVED,NEEDS_REVIEW,REJECTED", "limit": 20})
    assert status == 200, f"GET /extractions returned {status}: {body}"
    portfolios = [e for e in body.get("extractions", []) if "reviewStatuses" in e]
    if not portfolios:
        pytest.skip(
            "The test account has no portfolio extraction with review statuses. "
            "Add a fixture: a portfolio document type with review triggers.")

    for summary in portfolios[:3]:
        # Claim 2: the list summary's reviewStatuses matches the documented schema.
        errors = schema_errors(spec, review_schema, summary["reviewStatuses"])
        assert errors == [], f"summary {summary['id']}: {errors}"

        # Claim 3: on retrieval, there's one status per document in the portfolio.
        status, full = api.request("GET", f"/documents/{summary['id']}")
        assert status == 200, f"GET /documents/{summary['id']} returned {status}"
        statuses = full.get("reviewStatuses")
        assert statuses is not None, f"{summary['id']}: retrieval has no reviewStatuses"
        assert schema_errors(spec, review_schema, statuses) == []
        assert len(statuses) == len(full.get("documents", [])), (
            f"{summary['id']}: {len(statuses)} statuses for {len(full.get('documents', []))} documents")


# ── cutoff_date removed from GET /extractions ────────────────────────────────

def test_list_extractions_has_no_cutoff_date(api, specs):
    spec = specs["extraction"]
    response_schema = spec["components"]["schemas"]["ExtractionsResponseFiltered"]

    # Claim 1: the spec no longer documents cutoff_date.
    assert "cutoff_date" not in response_schema["properties"]

    status, body = api.request("GET", "/extractions", {"limit": 5})
    assert status == 200, f"GET /extractions returned {status}: {body}"

    # Claim 2: the API doesn't return it.
    assert "cutoff_date" not in body

    # Claim 3: every top-level field the API returns is documented, and the body matches the schema.
    undocumented = sorted(set(body) - set(response_schema["properties"]))
    assert undocumented == [], f"undocumented top-level fields: {undocumented}"
    assert schema_errors(spec, response_schema, body) == []
