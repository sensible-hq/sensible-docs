"""The Sensible API calls code tests make, in one client.

Code tests run in a temporary document type (settings.DOC_TYPE) in the docs test account. Each
config is uploaded as written, as configuration <testId>, published to development. Deleting the
document type removes its configs; extraction history stays in the app.
"""

import json

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
