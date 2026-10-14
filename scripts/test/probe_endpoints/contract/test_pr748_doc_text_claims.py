"""Live checks for the descriptive text changes in sensible-docs#748.

- Get configuration returns the current draft, not necessarily the published
  version, and the documented way to get the published version works.
- The generate_upload_url Step 2 curl example, run as written, uploads the file.

Run from the repo root (-s shows each request, its response, and what to expect):
  python3 -m pytest scripts/test/probe_endpoints/contract -v -s --report-chars=s
To check #748's specs before it merges, point CONTRACT_SPEC_DIR at its reference/ folder.

Side effects: creates and then deletes one throwaway config (drift_probe_*) in
the auto_insurance_quotes fixture document type, and runs two single-document
extractions of assets/pdfs/auto_insurance_anyco.pdf.
"""

import json
import re
import shlex
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from conftest import REPO_ROOT

DOC_TYPE = "auto_insurance_quotes"  # fixture from fixtures/manifest.json; seed.py creates it
SAMPLE_PDF = REPO_ROOT / "assets" / "pdfs" / "auto_insurance_anyco.pdf"


def expect(text: str) -> None:
    print(f"\n>>> EXPECT: {text}")


def _doc_type_id(api) -> str:
    expect(f"HTTP 200 with the account's document types, including {DOC_TYPE}.")
    status, types = api.request("GET", "/document_types")
    assert status == 200
    match = next((t for t in types if t["name"] == DOC_TYPE), None)
    if match is None:
        pytest.skip(f"The test account has no {DOC_TYPE} document type. Run seed.py, then rerun.")
    return match["id"]


def _config(marker: str) -> dict:
    """A small valid config whose only field ID identifies which version came back."""
    return {"fields": [{"id": marker, "anchor": "policy period", "method": {"id": "label", "position": "right"}}]}


# ── Get configuration returns the draft ──────────────────────────────────────

@pytest.mark.docs_impact(
    change="Get configuration's description now says it returns the current draft (or the latest "
           "version if there's no draft), not necessarily the published version, and how to get the "
           "published one.",
    where="reference/openapi_configuration.json > paths./document_types/{type-id}/configurations/"
          "{config-name}.get.description",
    pages="API reference: Get configuration (ref:get-configuration)",
    if_pass="Correct as published. With a draft and a newer published version, the endpoint returns the "
            "draft, and the documented steps return the published version.",
    if_fail="The description is wrong. If the endpoint returned the published version, it doesn't prefer "
            "drafts: rewrite the description. If Get configuration by version returned something else, "
            "fix the steps for getting the published version.",
    if_skip="Unverified: the test account has no auto_insurance_quotes document type. Run seed.py.",
)
def test_get_configuration_returns_draft(api, specs):
    # Claim 0: the spec's description says Get configuration returns the current draft.
    description = specs["configuration"]["paths"]["/document_types/{type-id}/configurations/{config-name}"][
        "get"]["description"]
    assert "current draft" in description, "spec doesn't say Get configuration returns the current draft"

    type_id = _doc_type_id(api)
    name = f"drift_probe_{datetime.now(timezone.utc):%Y%m%d%H%M%S}"
    base = f"/document_types/{type_id}/configurations"
    draft, published = _config("draft_marker"), _config("published_marker")
    try:
        expect(f"HTTP 200. Creates throwaway config {name} with no `publish_as`, so its only version is a draft.")
        status, resp = api.request("POST", base, body={"name": name, "configuration": json.dumps(draft)})
        assert status == 200, f"create returned {status}: {resp}"

        time.sleep(2)  # version timestamps have 1-second granularity; keep the published version newer
        expect("HTTP 200. Adds a newer version and publishes it to development. The draft stays.")
        status, resp = api.request("PUT", f"{base}/{name}",
                                   body={"configuration": json.dumps(published), "publish_as": "development"})
        assert status == 200, f"publish returned {status}: {resp}"

        # Claim 1: Get configuration returns the draft, even though a newer version is published.
        expect("HTTP 200. `configuration` contains `draft_marker`, not `published_marker`. `versions` lists "
               "the draft first, then the version published to development.")
        status, got = api.request("GET", f"{base}/{name}")
        assert status == 200
        assert json.loads(got["configuration"]) == draft, "Get configuration didn't return the draft"

        # Claim 2: the documented way to get the published version works.
        version = next((v for v in got["versions"] if "development" in (v.get("environments") or [])), None)
        assert version is not None, "no version in `versions` lists development in `environments`"
        expect("HTTP 200. Get configuration by version, for the version whose `environments` lists "
               "development, returns `published_marker`.")
        status, by_version = api.request("GET", f"{base}/{name}/{version['version_id']}")
        assert status == 200
        assert json.loads(by_version["configuration"]) == published
    finally:
        expect(f"HTTP 200. Deletes throwaway config {name}.")
        api.request("DELETE", f"{base}/{name}")


# ── The upload example uploads the file ──────────────────────────────────────

def _step2_curl(specs) -> str:
    """The Step 2 PUT command from the generate_upload_url/{document_type} description, as published."""
    desc = specs["extraction"]["paths"]["/generate_upload_url/{document_type}"]["post"]["description"]
    after = desc.split("Step 2", 1)[1]
    return re.search(r"```curl\n(.*?)```", after, re.S).group(1).strip()


def _run_extraction(api, curl_command: str) -> dict:
    """Get an upload URL, PUT with the given curl command, and poll until the extraction finishes."""
    status, created = api.request("POST", f"/generate_upload_url/{DOC_TYPE}",
                                  query={"document_name": "contract_test_upload_example"},
                                  body={"content_type": "application/pdf"})
    assert status == 200, f"generate_upload_url returned {status}: {created}"
    command = (curl_command.replace("\\\n", " ")
               .replace("'https://sensible-so-utility-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/REDACTED'",
                        shlex.quote(created["upload_url"]))
               .replace("YOUR_PATH_TO_DOCUMENT.pdf", str(SAMPLE_PDF)))
    assert created["upload_url"] in command, "couldn't substitute the upload URL into the documented command"
    print(f"\n──── RUN (upload URL redacted) ───────────────────────\n"
          f"{command.replace(shlex.quote(created['upload_url']), '<upload_url>')}")
    result = subprocess.run(shlex.split(command), capture_output=True, text=True, timeout=120)
    print(f"curl exit code {result.returncode}")
    assert result.returncode == 0, f"curl failed: {result.stderr[-500:]}"
    for _ in range(36):
        status, full = api.request("GET", f"/documents/{created['id']}", quiet=True)
        if status == 200 and full.get("status") in ("COMPLETE", "FAILED"):
            break
        time.sleep(5)
    status, full = api.request("GET", f"/documents/{created['id']}")
    return full


@pytest.mark.docs_impact(
    change="The generate_upload_url Step 2 curl example now uses `--data-binary '@YOUR_PATH_TO_DOCUMENT.pdf'` "
           "instead of `--data 'YOUR_PATH_TO_DOCUMENT.pdf'`. docs/api/batch-api.md has the same fix.",
    where="reference/openapi_extraction.json > paths./generate_upload_url/{document_type}.post.description "
          "(Step 2)",
    pages="API reference: Generate upload URL (ref:generate-an-upload-url); guide: docs/api/batch-api.md",
    if_pass="Correct as published. The documented command, run as written, uploads the file and the "
            "extraction completes. The old form fails, so the fix was needed.",
    if_fail="If the documented command's extraction didn't complete, the example still doesn't upload the "
            "file: fix the curl flags. If the old form also completed, the original example worked, and "
            "the change was unnecessary.",
    if_skip="Unverified: curl isn't installed, or the test account has no auto_insurance_quotes document "
            "type (run seed.py).",
)
def test_upload_example_uploads_the_file(api, specs):
    if not shutil.which("curl"):
        pytest.skip("curl isn't installed.")
    _doc_type_id(api)
    documented = _step2_curl(specs)
    assert "--data-binary '@YOUR_PATH_TO_DOCUMENT.pdf'" in documented, "the spec's example isn't the fixed form"

    # Claim 1: the documented command, as written, uploads the file.
    expect("The documented Step 2 command runs with the real upload URL and the sample PDF path substituted. "
           "curl exits 0, and the extraction finishes COMPLETE.")
    full = _run_extraction(api, documented)
    assert full.get("status") == "COMPLETE", f"documented example: extraction is {full.get('status')}"

    # Control: the old form uploads the path text, so the extraction fails.
    old = documented.replace("--data-binary '@YOUR_PATH_TO_DOCUMENT.pdf'", "--data 'YOUR_PATH_TO_DOCUMENT.pdf'")
    expect("Control: the old command (`--data 'path'`). S3 accepts the upload, but it's the path text, "
           "not a PDF, so the extraction finishes FAILED.")
    full = _run_extraction(api, old)
    assert full.get("status") == "FAILED", f"old example: extraction is {full.get('status')}, expected FAILED"
