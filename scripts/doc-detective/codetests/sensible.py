"""The Sensible API calls code tests make, in one client.

Code tests run in a temporary document type (settings.DOC_TYPE) in the docs test account. Each
config is uploaded as written, as configuration <testId>, published to development. Deleting the
document type removes its configs; extraction history stays in the app.
"""

import json
import time

from . import settings
from .errors import CONFIG_INVALID, EXTRACTION_ERROR, CodeTestError


class SensibleClient:
    def __init__(self, key):
        self.key = key
        self._type_id = None

    def _api(self, method, path, **kwargs):
        import requests

        return requests.request(method, f"{settings.API}{path}", headers={"Authorization": f"Bearer {self.key}"}, timeout=60, **kwargs)

    def document_status(self, url):
        """The HTTP status of the example document's link (200 when it resolves)."""
        import requests

        return requests.head(url, allow_redirects=True, timeout=30).status_code

    def _doc_type_id(self):
        response = self._api("GET", "/document_types")
        response.raise_for_status()
        return next((d["id"] for d in response.json() if d["name"] == settings.DOC_TYPE), None)

    def ensure_doc_type(self):
        if self._type_id:
            return self._type_id
        self._type_id = self._doc_type_id()
        if not self._type_id:
            response = self._api("POST", "/document_types", json={"name": settings.DOC_TYPE, "schema": {"fingerprint_mode": "fallback_to_all"}})
            response.raise_for_status()
            self._type_id = response.json()["id"]
        return self._type_id

    def delete_doc_type(self):
        """Delete the temporary document type. Returns whether there was one."""
        type_id = self._doc_type_id()
        self._type_id = None
        if not type_id:
            return False
        self._api("DELETE", f"/document_types/{type_id}").raise_for_status()
        return True

    def upload_config(self, name, config_text):
        """Upload the config as the doc shows it, comments and all: Sensible accepts JSON5-style configs."""
        type_id = self.ensure_doc_type()
        body = {"configuration": config_text, "publish_as": settings.ENVIRONMENT}
        if self._api("GET", f"/document_types/{type_id}/configurations/{name}").status_code == 404:
            response = self._api("POST", f"/document_types/{type_id}/configurations", json={"name": name, **body})
        else:
            response = self._api("PUT", f"/document_types/{type_id}/configurations/{name}", json=body)
        if not response.ok:
            raise CodeTestError(CONFIG_INVALID, f"config upload returned {response.status_code}: {response.text[:500]}")

    def delete_config(self, name):
        """Delete a configuration, so the next code test's extraction can't pick it instead of its own."""
        type_id = self.ensure_doc_type()
        response = self._api("DELETE", f"/document_types/{type_id}/configurations/{name}")
        if response.status_code not in (200, 204, 404):
            response.raise_for_status()

    def extract(self, url, config_name, document_name):
        """Extract from a document URL with a configuration and wait. Returns parsed_document.

        In the development environment Sensible runs every config in the document type and picks
        the best fit, so this checks the extraction used `config_name`."""
        from sensibleapi import SensibleSDK

        sdk = SensibleSDK(self.key)
        result = sdk.wait_for(sdk.extract(
            url=url, document_type=settings.DOC_TYPE, configuration_name=config_name,
            environment=settings.ENVIRONMENT, document_name=document_name,
        ))
        if result.get("status") != "COMPLETE":
            raise CodeTestError(EXTRACTION_ERROR, f"status {result.get('status')}: {json.dumps(result.get('errors'))[:500]}")
        if result.get("configuration") != config_name:
            raise CodeTestError(EXTRACTION_ERROR, f"Sensible used configuration {result.get('configuration')!r}, not {config_name!r}")
        return result.get("parsed_document") or {}

    # -- Fixtures and portfolio extractions (fingerprint claims) --

    def ensure_fixture(self, doctype_file, config_file):
        """Make sure the fixture's doc type exists and its config is published, as committed.

        Fixture doc types are persistent: they're created or republished here when missing or
        different, and never deleted. Returns (doc type name, config name)."""
        import os

        with open(doctype_file, encoding="utf-8") as f:
            doctype = json.load(f)
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)
        name = doctype["name"]
        config_name = os.path.basename(config_file)[len(name) + 1:-len(".config.json")]
        response = self._api("GET", "/document_types")
        response.raise_for_status()
        type_id = next((d["id"] for d in response.json() if d["name"] == name), None)
        if not type_id:
            response = self._api("POST", "/document_types", json=doctype)
            if not response.ok:
                raise CodeTestError(CONFIG_INVALID, f"creating fixture doc type {name} returned {response.status_code}: {response.text[:300]}")
            type_id = response.json()["id"]
        published = self._published_config(type_id, config_name)
        if published != config:
            body = {"configuration": json.dumps(config), "publish_as": settings.FIXTURE_ENVIRONMENT}
            if published is None:
                response = self._api("POST", f"/document_types/{type_id}/configurations", json={"name": config_name, **body})
            else:
                response = self._api("PUT", f"/document_types/{type_id}/configurations/{config_name}", json=body)
            if not response.ok:
                raise CodeTestError(CONFIG_INVALID, f"publishing fixture config {name}/{config_name} returned {response.status_code}: {response.text[:300]}")
        return name, config_name

    def _published_config(self, type_id, config_name):
        """The config published to the fixture environment, parsed, or None if there isn't one."""
        response = self._api("GET", f"/document_types/{type_id}/configurations/{config_name}/versions")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        versions = response.json()
        versions = versions if isinstance(versions, list) else versions.get("versions", [])
        version = next((v["version_id"] for v in versions if settings.FIXTURE_ENVIRONMENT in (v.get("environments") or [])), None)
        if not version:
            return None
        response = self._api("GET", f"/document_types/{type_id}/configurations/{config_name}/{version}")
        response.raise_for_status()
        config = response.json()["configuration"]
        return json.loads(config) if isinstance(config, str) else config

    def extract_portfolio(self, url, doc_types, document_name, timeout=600):
        """Run a fingerprint-segmented portfolio extraction and wait. Returns (extraction ID, documents)."""
        response = self._api(
            "POST", f"/extract_from_url?environment={settings.FIXTURE_ENVIRONMENT}&document_name={document_name}",
            json={"document_url": url, "types": doc_types, "segment_documents_with": "fingerprints"},
        )
        if not response.ok:
            raise CodeTestError(EXTRACTION_ERROR, f"portfolio extraction request returned {response.status_code}: {response.text[:300]}")
        extraction_id = response.json()["id"]
        deadline = time.time() + timeout
        while True:
            result = self._api("GET", f"/documents/{extraction_id}").json()
            if result.get("status") in ("COMPLETE", "FAILED"):
                break
            if time.time() > deadline:
                raise CodeTestError(EXTRACTION_ERROR, f"extraction {extraction_id} didn't finish within {timeout} seconds")
            time.sleep(5)
        if result.get("status") != "COMPLETE":
            raise CodeTestError(EXTRACTION_ERROR, f"extraction {extraction_id}: status {result.get('status')}: {json.dumps(result.get('errors'))[:300]}")
        return extraction_id, result.get("documents") or []
