"""Shared fixtures for live contract tests against the Sensible API.

These tests call the real API with the dedicated test account. They read the
key from SENSIBLE_TEST_API_KEY only: from the environment if it's set there,
otherwise from the gitignored .env at the repo root (the same file the
getting-started Doc Detective tooling uses). They skip if neither has it, never
fall back to another key, and never print the key.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import jsonschema
import pytest

API_BASE = "https://api.sensible.so/v0"
KEY_ENV = "SENSIBLE_TEST_API_KEY"
REPO_ROOT = Path(__file__).resolve().parents[4]
REFERENCE_DIR = REPO_ROOT / "reference"
DOTENV = REPO_ROOT / ".env"


def _read_key() -> str | None:
    """SENSIBLE_TEST_API_KEY from the environment, else from the repo-root .env."""
    if os.environ.get(KEY_ENV):
        return os.environ[KEY_ENV]
    if not DOTENV.is_file():
        return None
    for line in DOTENV.read_text().splitlines():
        name, sep, value = line.strip().removeprefix("export ").partition("=")
        if sep and name.strip() == KEY_ENV:
            return value.split(" #")[0].strip().strip("'\"") or None
    return None


class Api:
    def __init__(self, key: str):
        self._key = key

    def request(self, method: str, path: str, query: dict | None = None, body=None):
        """Return (status, parsed JSON body or raw text). Never raises on HTTP errors.

        Prints the full request and response. Run pytest with -s to see them.
        The Authorization header is always printed redacted.
        """
        url = f"{API_BASE}{path}"
        if query:
            url += "?" + urllib.parse.urlencode(query)
        headers = {"Authorization": f"Bearer {self._key}"}
        data = None
        if body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        _print_request(method, url, headers, body)
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                status, raw, resp_headers = resp.status, resp.read(), dict(resp.headers)
        except urllib.error.HTTPError as e:
            status, raw, resp_headers = e.code, e.read(), dict(e.headers or {})
        text = raw.decode("utf-8", errors="replace")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            parsed = text
        _print_response(status, resp_headers, parsed)
        return status, parsed


def _pretty(value) -> str:
    return json.dumps(value, indent=2) if isinstance(value, (dict, list)) else str(value)


def _print_request(method: str, url: str, headers: dict, body) -> None:
    shown = {k: ("Bearer <redacted>" if k.lower() == "authorization" else v) for k, v in headers.items()}
    print(f"\n──── REQUEST ─────────────────────────────────────────\n{method} {url}")
    for k, v in shown.items():
        print(f"{k}: {v}")
    if body is not None:
        print(f"\n{_pretty(body)}")


def _print_response(status: int, headers: dict, body) -> None:
    print(f"\n──── RESPONSE ────────────────────────────────────────\nHTTP {status}")
    for k, v in headers.items():
        print(f"{k}: {v}")
    print(f"\n{_pretty(body)}")


@pytest.fixture(scope="session")
def api() -> Api:
    key = _read_key()
    if not key:
        pytest.skip(
            f"{KEY_ENV} isn't in the environment or {DOTENV}. "
            "These tests only run against the test account.")
    return Api(key)


@pytest.fixture(scope="session")
def specs() -> dict:
    return {
        name: json.loads((REFERENCE_DIR / f"openapi_{name}.json").read_text())
        for name in ("extraction", "configuration", "classification", "email")
    }


def to_json_schema(spec: dict, schema: dict, _seen: tuple = ()) -> dict:
    """Inline $refs and convert OpenAPI 3.0 `nullable` so jsonschema can validate.

    Validation follows the spec as written: it doesn't add additionalProperties.
    """
    if isinstance(schema, list):
        return [to_json_schema(spec, s, _seen) for s in schema]
    if not isinstance(schema, dict):
        return schema
    ref = schema.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/"):
        if ref in _seen:
            return {}  # recursive reference: don't descend again
        target = spec
        for part in ref[2:].split("/"):
            target = target[part]
        return to_json_schema(spec, target, _seen + (ref,))
    out = {}
    for key, value in schema.items():
        if key.startswith("x-") or key in ("example", "examples", "nullable"):
            continue
        out[key] = to_json_schema(spec, value, _seen)
    if schema.get("nullable"):
        t = out.get("type")
        if isinstance(t, str):
            out["type"] = [t, "null"]
        elif isinstance(t, list) and "null" not in t:
            out["type"] = t + ["null"]
    return out


def schema_errors(spec: dict, schema: dict, instance) -> list[str]:
    """Validate instance against an OpenAPI schema fragment; return readable errors."""
    validator = jsonschema.Draft7Validator(to_json_schema(spec, schema))
    return [
        f"{'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
        for e in validator.iter_errors(instance)
    ]
