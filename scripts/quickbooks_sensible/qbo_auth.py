"""
Shared QuickBooks Online auth helper.

One-time setup required:
  Add http://localhost:8080/callback as an allowed redirect URI in your
  Intuit Developer app at https://developer.intuit.com/

Environment variables:
  Required: QBO_CLIENT_ID, QBO_CLIENT_SECRET
  Optional: QBO_TOKEN_FILE — override token storage path.
            For production use, set QBO_TOKEN_FILE=~/.qbo_tokens.json
            (or any path outside the project directory).
"""

import json
import os
import socket
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from intuitlib.exceptions import AuthClientError
from quickbooks import QuickBooks
from quickbooks.exceptions import QuickbooksException

_REDIRECT_URI = "http://localhost:8080/callback"


def token_path() -> Path:
    """Return the resolved token file path (public — useful for callers that need to display or check the path)."""
    if "QBO_TOKEN_FILE" in os.environ:
        return Path(os.environ["QBO_TOKEN_FILE"])
    return Path(__file__).parent / ".qbo_tokens.json"


def _load_tokens(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _save_tokens(path: Path, tokens: dict) -> None:
    path.write_text(json.dumps(tokens, indent=2))
    os.chmod(path, 0o600)


def _browser_flow(auth_client: AuthClient) -> dict:
    result = {}

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            params = parse_qs(urlparse(self.path).query)
            result["code"] = params.get("code", [None])[0]
            result["realm_id"] = params.get("realmId", [None])[0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Authorized! You can close this tab.</h1>")

        def log_message(self, format, *args):
            pass  # suppress request logs

    try:
        server = HTTPServer(("localhost", 8080), _Handler)
    except OSError:
        print("Error: port 8080 is in use. Stop the other process and try again.")
        sys.exit(1)

    server.socket.settimeout(120)
    auth_url = auth_client.get_authorization_url([Scopes.ACCOUNTING])
    print(f"\n  Open this URL in your browser to authorize:\n\n  {auth_url}\n")
    print("  Waiting for authorization (120s timeout)...")

    try:
        server.handle_request()
    except socket.timeout:
        print("Error: no callback received within 120 seconds. Did you authorize in the browser?")
        sys.exit(1)

    auth_client.get_bearer_token(result["code"], realm_id=result["realm_id"])
    return {
        "access_token": auth_client.access_token,
        "refresh_token": auth_client.refresh_token,
        "realm_id": result["realm_id"],
    }


def get_qb_client() -> QuickBooks:
    """Return an authenticated QuickBooks client, handling all token management.

    On first run: opens a browser for OAuth authorization and saves tokens.
    On subsequent runs: refreshes the access token silently from the saved file.
    If the refresh token is expired or revoked: re-runs the browser flow.
    """
    path = token_path()
    auth_client = AuthClient(
        client_id=os.environ["QBO_CLIENT_ID"],
        client_secret=os.environ["QBO_CLIENT_SECRET"],
        redirect_uri=_REDIRECT_URI,
        environment="sandbox",
    )

    tokens = _load_tokens(path)

    if tokens.get("refresh_token"):
        try:
            auth_client.refresh(refresh_token=tokens["refresh_token"])
            tokens["access_token"] = auth_client.access_token
            tokens["refresh_token"] = auth_client.refresh_token
            _save_tokens(path, tokens)
        except (AuthClientError, QuickbooksException):
            print("  Warning: saved tokens are invalid or expired. Re-authorizing...")
            tokens = {}

    if not tokens:
        tokens = _browser_flow(auth_client)
        _save_tokens(path, tokens)

    return QuickBooks(
        auth_client=auth_client,
        refresh_token=auth_client.refresh_token,
        company_id=tokens["realm_id"],
        minorversion=75,
        environment="sandbox",
    )
