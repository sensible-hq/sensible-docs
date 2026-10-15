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

    def fixture_drift(self, doctype_file, config_file, references=()):
        """Compare a fixture with the test account, without changing anything.

        Returns a dict: name, config_name, type_id (None if the doc type is missing), and `drift`, a
        list of readable differences between the committed files and the test account (the doc type's
        settings, and the config published to settings.FIXTURE_ENVIRONMENT). `draft` is True when there's
        an unpublished edit whose content differs from the published config. It doesn't affect tests."""
        import os

        with open(doctype_file, encoding="utf-8") as f:
            doctype = json.load(f)
        with open(config_file, encoding="utf-8") as f:
            config = json.load(f)
        name = doctype["name"]
        config_name = os.path.basename(config_file)[len(name) + 1:-len(".config.json")]
        state = {"name": name, "config_name": config_name, "doctype": doctype, "config": config, "type_id": None, "drift": [], "draft": False,
                 "references": list(references), "missing_refs": [], "relinked_refs": []}
        response = self._api("GET", "/document_types")
        response.raise_for_status()
        live_type = next((d for d in response.json() if d["name"] == name), None)
        if not live_type:
            state["drift"].append(f"doc type {name} is missing from the test account")
            state["missing_refs"] = list(references)
            return state
        state["type_id"] = live_type["id"]
        state["drift"] += [f"doc type {name} settings: {d}" for d in json_diff(doctype.get("schema") or {}, live_type.get("schema") or {})]
        published, state["draft"] = self._published_config(live_type["id"], config_name)
        if published is None:
            state["drift"].append(f"config {name}/{config_name} isn't published to {settings.FIXTURE_ENVIRONMENT}")
        else:
            state["drift"] += [f"config {name}/{config_name}: {d}" for d in json_diff(config, published)]
        state["published"] = published
        for ref in references:
            response = self._api("GET", f"/document_types/{live_type['id']}/goldens/{ref['name']}")
            if response.status_code == 404:
                state["drift"].append(f"reference document {name}/{ref['name']} is missing")
                state["missing_refs"].append(ref)
                continue
            response.raise_for_status()
            linked = response.json().get("configuration")
            if linked != ref["configuration"]:
                state["drift"].append(f"reference document {name}/{ref['name']}: linked to config {linked!r}, committed {ref['configuration']!r}")
                state["relinked_refs"].append(ref)
        return state

    def ensure_fixture(self, doctype_file, config_file, references=()):
        """Make sure the fixture's doc type and published config match the committed files, restoring
        them if they don't. Fixture doc types are persistent: created when missing, never deleted.

        Returns (doc type name, config name, warnings). Each warning describes something the runner
        restored, for example a config someone edited and published in the app."""
        state = self.fixture_drift(doctype_file, config_file, references)
        name, config_name, type_id = state["name"], state["config_name"], state["type_id"]
        if not state["drift"]:
            return name, config_name, []
        if not type_id:
            response = self._api("POST", "/document_types", json=state["doctype"])
            if not response.ok:
                raise CodeTestError(CONFIG_INVALID, f"creating fixture doc type {name} returned {response.status_code}: {response.text[:300]}")
            type_id = response.json()["id"]
            state["published"] = None
        elif any(d.startswith(f"doc type {name} settings") for d in state["drift"]):
            response = self._api("PUT", f"/document_types/{type_id}", json={"name": name, "schema": state["doctype"].get("schema") or {}})
            if not response.ok:
                raise CodeTestError(CONFIG_INVALID, f"restoring fixture doc type {name} settings returned {response.status_code}: {response.text[:300]}")
        if state.get("published") != state["config"]:
            body = {"configuration": json.dumps(state["config"]), "publish_as": settings.FIXTURE_ENVIRONMENT}
            exists = self._api("GET", f"/document_types/{type_id}/configurations/{config_name}").status_code != 404
            if exists:
                response = self._api("PUT", f"/document_types/{type_id}/configurations/{config_name}", json=body)
            else:
                response = self._api("POST", f"/document_types/{type_id}/configurations", json={"name": config_name, **body})
            if not response.ok:
                raise CodeTestError(CONFIG_INVALID, f"publishing fixture config {name}/{config_name} returned {response.status_code}: {response.text[:300]}")
        for ref in state["missing_refs"]:
            self._upload_reference(type_id, ref)
        for ref in state["relinked_refs"]:
            response = self._api("PUT", f"/document_types/{type_id}/goldens/{ref['name']}", json={"configuration": ref["configuration"]})
            if not response.ok:
                raise CodeTestError(CONFIG_INVALID, f"relinking reference document {name}/{ref['name']} returned {response.status_code}: {response.text[:300]}")
        warnings = [f"restored fixture from the committed files ({d})" for d in state["drift"]]
        return name, config_name, warnings

    def _upload_reference(self, type_id, ref):
        """Create a reference document and upload its PDF from the repo."""
        import os

        import requests

        response = self._api("POST", f"/document_types/{type_id}/goldens",
                             json={"name": ref["name"], "configuration": ref["configuration"], "content_type": "application/pdf"})
        if not response.ok:
            raise CodeTestError(CONFIG_INVALID, f"creating reference document {ref['name']} returned {response.status_code}: {response.text[:300]}")
        with open(os.path.join(settings.REPO_ROOT, ref["pdf"]), "rb") as f:
            put = requests.put(response.json()["upload_url"], data=f, headers={"Content-Type": "application/pdf"}, timeout=120)
        if put.status_code != 200:
            raise CodeTestError(CONFIG_INVALID, f"uploading reference document {ref['name']} ({ref['pdf']}) returned {put.status_code}")

    def _published_config(self, type_id, config_name):
        """(The config published to the fixture environment, parsed, or None; whether a newer unpublished version exists)."""
        response = self._api("GET", f"/document_types/{type_id}/configurations/{config_name}/versions")
        if response.status_code == 404:
            return None, False
        response.raise_for_status()
        versions = response.json()
        versions = versions if isinstance(versions, list) else versions.get("versions", [])
        version = next((v["version_id"] for v in versions if settings.FIXTURE_ENVIRONMENT in (v.get("environments") or [])), None)
        if not version:
            return None, False
        published = self._config_version(type_id, config_name, version)
        # An unpublished edit in the app. The editor autosaves a draft just from opening a config, so
        # only a draft whose content differs from the published config counts.
        published_at = next((v.get("datetime", "") for v in versions if v["version_id"] == version), "")
        drafts = sorted((v for v in versions if v.get("draft") and v.get("datetime", "") > published_at), key=lambda v: v.get("datetime", ""))
        draft = bool(drafts) and self._config_version(type_id, config_name, drafts[-1]["version_id"]) != published
        return published, draft

    def _config_version(self, type_id, config_name, version):
        response = self._api("GET", f"/document_types/{type_id}/configurations/{config_name}/{version}")
        response.raise_for_status()
        config = response.json()["configuration"]
        try:
            return json.loads(config) if isinstance(config, str) else config
        except json.JSONDecodeError:
            return config  # a draft with comments or a syntax error still counts as different

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


def json_diff(committed, live, path="$"):
    """Readable differences between a committed fixture value and the test account's value."""
    if isinstance(committed, dict) and isinstance(live, dict):
        out = []
        for key in sorted(set(committed) | set(live), key=str):
            if key not in live:
                out.append(f"{path}.{key} is missing in the test account (committed {json.dumps(committed[key])[:80]})")
            elif key not in committed:
                out.append(f"{path}.{key} was added in the test account ({json.dumps(live[key])[:80]})")
            else:
                out += json_diff(committed[key], live[key], f"{path}.{key}")
        return out
    if isinstance(committed, list) and isinstance(live, list) and len(committed) == len(live):
        return [d for i, (a, b) in enumerate(zip(committed, live)) for d in json_diff(a, b, f"{path}[{i}]")]
    if committed != live:
        return [f"{path}: committed {json.dumps(committed)[:80]}, test account {json.dumps(live)[:80]}"]
    return []
