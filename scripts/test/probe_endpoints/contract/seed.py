#!/usr/bin/env python3
"""Create or update the contract tests' fixtures in the test account.

Reads fixtures/manifest.json and, through the documented configuration API:
  1. creates each document type, or updates its settings if they differ
  2. creates each config and publishes it, or republishes it if it differs
  3. creates each reference document and uploads its PDF; updates its config
     association if that differs

Safe to rerun: everything is matched by name, and unchanged items are left alone.

Usage (from the repo root):
  python3 scripts/test/probe_endpoints/contract/seed.py           # apply
  python3 scripts/test/probe_endpoints/contract/seed.py --check   # report only, no writes

Uses SENSIBLE_TEST_API_KEY only (environment, else the repo-root .env). Exits 1
if --check finds differences or anything fails.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from conftest import KEY_ENV, REPO_ROOT, Api, _read_key  # noqa: E402

FIXTURES = HERE / "fixtures"


class Seeder:
    def __init__(self, api: Api, check: bool):
        self.api, self.check, self.problems, self.changes = api, check, 0, 0

    def log(self, status: str, what: str, detail: str = "") -> None:
        print(f"  {status:10} {what}{f'  ({detail})' if detail else ''}")
        if status in ("MISSING", "DIFFERS", "FAILED"):
            self.problems += 1

    def call(self, method, path, **kw):
        status, body = self.api.request(method, path, quiet=True, **kw)
        if status >= 400 and not (method == "GET" and status == 404):
            raise RuntimeError(f"{method} {path} returned {status}: {body}")
        return status, body

    # ── document types ──
    def document_type(self, spec: dict, existing: dict) -> str | None:
        name = spec["name"]
        live = existing.get(name)
        if live is None:
            if self.check:
                self.log("MISSING", f"document type {name}")
                return None
            _, created = self.call("POST", "/document_types", body=spec)
            self.changes += 1
            self.log("CREATED", f"document type {name}")
            return created["id"]
        wanted = spec.get("schema", {})
        live_schema = live.get("schema") or {}
        diffs = sorted(k for k, v in wanted.items() if live_schema.get(k) != v)
        if not diffs:
            self.log("OK", f"document type {name}")
        elif self.check:
            self.log("DIFFERS", f"document type {name}", f"settings: {', '.join(diffs)}")
        else:
            self.call("PUT", f"/document_types/{live['id']}", body={"schema": {**live_schema, **wanted}})
            self.changes += 1
            self.log("UPDATED", f"document type {name}", f"settings: {', '.join(diffs)}")
        return live["id"]

    # ── configs ──
    def config(self, type_id: str | None, type_name: str, cfg: dict) -> None:
        name, env = cfg["name"], cfg["publish_as"]
        wanted = json.loads((FIXTURES / cfg["file"]).read_text())
        what = f"config {type_name}/{name} ({env})"
        if type_id is None:
            self.log("MISSING", what)
            return
        status, live = self.call("GET", f"/document_types/{type_id}/configurations/{name}")
        payload = {"configuration": json.dumps(wanted), "publish_as": env}
        if status == 404:
            if self.check:
                self.log("MISSING", what)
            else:
                self.call("POST", f"/document_types/{type_id}/configurations", body={"name": name, **payload})
                self.changes += 1
                self.log("CREATED", what)
            return
        # The top-level version_id/configuration is the latest draft, which may not be what's
        # published. Compare the version that's actually published to `env`.
        published = next((v for v in live.get("versions") or []
                          if env in (v.get("environments") or []) and not v.get("draft")), None)
        if published is None:
            reason = f"nothing published to {env}"
        else:
            _, version = self.call(
                "GET", f"/document_types/{type_id}/configurations/{name}/{published['version_id']}")
            reason = None if _parse(version.get("configuration")) == wanted else f"version published to {env} differs"
        if reason is None:
            self.log("OK", what, f"published version {published['version_id']}")
        elif self.check:
            self.log("DIFFERS", what, reason)
        else:
            self.call("PUT", f"/document_types/{type_id}/configurations/{name}", body=payload)
            self.changes += 1
            self.log("UPDATED", what, f"{reason}; published fixture to {env}")

    # ── reference documents ──
    def reference(self, type_id: str | None, type_name: str, ref: dict) -> None:
        name, pdf = ref["name"], REPO_ROOT / ref["pdf"]
        what = f"reference {type_name}/{name} ({ref['pdf']})"
        if type_id is None:
            self.log("MISSING", what)
            return
        status, live = self.call("GET", f"/document_types/{type_id}/goldens/{name}")
        if status == 404:
            if self.check:
                self.log("MISSING", what)
                return
            _, created = self.call("POST", f"/document_types/{type_id}/goldens",
                                   body={"name": name, "configuration": ref["configuration"],
                                         "content_type": "application/pdf"})
            put = _put(created["upload_url"], pdf)
            if put != 200:
                self.log("FAILED", what, f"PDF upload returned {put}")
            else:
                self.changes += 1
                self.log("CREATED", what)
            return
        if live.get("configuration") == ref["configuration"]:
            self.log("OK", what)
        elif self.check:
            self.log("DIFFERS", what, f"associated config is {live.get('configuration')!r}")
        else:
            self.call("PUT", f"/document_types/{type_id}/goldens/{name}",
                      body={"configuration": ref["configuration"]})
            self.changes += 1
            self.log("UPDATED", what, "config association")


def _parse(text):
    try:
        return json.loads(text) if isinstance(text, str) else text
    except json.JSONDecodeError:
        return None


def _put(upload_url: str, path: Path) -> int:
    """PUT a PDF to a pre-signed URL without printing the URL (it contains credentials)."""
    import urllib.error
    import urllib.request
    req = urllib.request.Request(upload_url, data=path.read_bytes(),
                                 headers={"Content-Type": "application/pdf"}, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code


def main() -> int:
    check = "--check" in sys.argv[1:]
    key = _read_key()
    if not key:
        print(f"{KEY_ENV} isn't set (environment or repo-root .env). Refusing to run without the test key.")
        return 1
    seeder = Seeder(Api(key), check)
    manifest = json.loads((FIXTURES / "manifest.json").read_text())
    print(f"{'Checking' if check else 'Seeding'} test account fixtures from {FIXTURES.relative_to(REPO_ROOT)}/manifest.json")
    try:
        _, types = seeder.call("GET", "/document_types")
        existing = {t["name"]: t for t in types}
        for entry in manifest["document_types"]:
            spec = json.loads((FIXTURES / entry["doctype"]).read_text())
            print(f"\n{spec['name']}")
            type_id = seeder.document_type(spec, existing)
            for cfg in entry.get("configs", []):
                seeder.config(type_id, spec["name"], cfg)
            for ref in entry.get("references", []):
                seeder.reference(type_id, spec["name"], ref)
    except RuntimeError as e:
        print(f"\nFAILED: {e}")
        return 1
    if seeder.problems:
        print(f"\n{seeder.problems} item(s) missing, different, or failed.")
    elif seeder.changes:
        print(f"\nApplied {seeder.changes} change(s). Rerun with --check to confirm.")
    else:
        print("\nNo differences.")
    return 1 if seeder.problems else 0


if __name__ == "__main__":
    sys.exit(main())
