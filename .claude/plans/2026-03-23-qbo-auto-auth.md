# QBO Auto-Auth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace manual token handling in the QuickBooks/Sensible integration with a browser-based OAuth flow that auto-refreshes tokens on every run.

**Architecture:** A new shared module `qbo_auth.py` owns all token logic (browser OAuth flow, token file persistence, auto-refresh). Public interface: `get_qb_client()` and `token_path()`. Two scripts consume it: `quickbooks-setup.py` (first-time setup runner) and `import_sensible_to_quickbooks.py` (updated to call `get_qb_client()` instead of manually constructing auth).

**Tech Stack:** Python 3, `intuitlib`, `python-quickbooks`, `http.server` (stdlib), `webbrowser` (stdlib)

**Spec:** `scripts/quickbooks_sensible/2026-03-23-qbo-auth-design.md`

---

## File Map

| File | Action |
|---|---|
| `scripts/quickbooks_sensible/qbo_auth.py` | Create |
| `scripts/quickbooks_sensible/quickbooks-setup.py` | Replace (old manual script → new thin runner) |
| `scripts/quickbooks_sensible/import_sensible_to_quickbooks.py` | Update auth block only |
| `scripts/quickbooks_sensible/.gitignore` | Create |

---

## Task 1: Create `.gitignore`

**Files:**
- Create: `scripts/quickbooks_sensible/.gitignore`

- [ ] **Step 1: Create the file**

```
.qbo_tokens.json
```

- [ ] **Step 2: Commit**

```bash
git add scripts/quickbooks_sensible/.gitignore
git commit -m "chore: add .gitignore for qbo token file"
```

---

## Task 2: Create `qbo_auth.py`

**Files:**
- Create: `scripts/quickbooks_sensible/qbo_auth.py`

- [ ] **Step 1: Write the file**

```python
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
import webbrowser
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
    webbrowser.open(auth_url)
    print("  Waiting for browser authorization (120s timeout)...")

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
        environment="production",
    )

    tokens = _load_tokens(path)

    if tokens.get("refresh_token"):
        try:
            auth_client.refresh(refresh_token=tokens["refresh_token"])
            tokens["access_token"] = auth_client.access_token
            tokens["refresh_token"] = auth_client.refresh_token
            _save_tokens(path, tokens)
        except (AuthClientError, QuickbooksException):
            print("  ⚠ Saved tokens are invalid or expired. Re-authorizing...")
            tokens = {}

    if not tokens:
        tokens = _browser_flow(auth_client)
        _save_tokens(path, tokens)

    return QuickBooks(
        auth_client=auth_client,
        refresh_token=auth_client.refresh_token,
        company_id=tokens["realm_id"],
        minorversion=75,
    )
```

- [ ] **Step 2: Commit**

```bash
git add scripts/quickbooks_sensible/qbo_auth.py
git commit -m "feat: add qbo_auth.py with browser OAuth flow and token persistence"
```

---

## Task 3: Replace `quickbooks-setup.py`

**Files:**
- Modify: `scripts/quickbooks_sensible/quickbooks-setup.py`

- [ ] **Step 1: Replace the file contents**

```python
"""
First-time QuickBooks Online setup.

Run this once to authorize the app and save tokens:
    python quickbooks-setup.py

Required env vars: QBO_CLIENT_ID, QBO_CLIENT_SECRET
One-time Intuit console step: add http://localhost:8080/callback as a redirect URI.
"""

from qbo_auth import get_qb_client, token_path

print("Connecting to QuickBooks Online...")
get_qb_client()
print(f"Setup complete. Tokens saved to {token_path()}")
```

- [ ] **Step 2: Commit**

```bash
git add scripts/quickbooks_sensible/quickbooks-setup.py
git commit -m "feat: replace quickbooks-setup.py with browser OAuth runner"
```

---

## Task 4: Update `import_sensible_to_quickbooks.py`

**Files:**
- Modify: `scripts/quickbooks_sensible/import_sensible_to_quickbooks.py`

- [ ] **Step 1: Replace the auth block**

Remove lines 5–6 (the `AuthClient` and `QuickBooks` imports) and the auth block at lines 120–137:

```python
# Remove these imports:
from intuitlib.client import AuthClient
from quickbooks import QuickBooks

# Remove this block (lines 120–137):
# ── QuickBooks Online auth ─────────────────────────────────────────────────────
print("\n[3/6] Authenticating with QuickBooks Online ...")
auth_client = AuthClient(
    client_id=os.environ["QBO_CLIENT_ID"],
    ...
)
...
print("  ✓ Connected.")
```

Replace with:

```python
# New import (add alongside existing imports at top of file):
from qbo_auth import get_qb_client

# New auth block (replace the removed block):
# ── QuickBooks Online auth ─────────────────────────────────────────────────────
print("\n[3/6] Authenticating with QuickBooks Online ...")
qb_client = get_qb_client()
print("  ✓ Connected.")
```

- [ ] **Step 2: Verify the file still imports only what it uses**

After editing, the imports at the top of the file should be:

```python
import os
import requests
from pathlib import Path

from sensibleapi import SensibleSDK
from quickbooks.objects.account import Account
from quickbooks.objects.bill import Bill
from quickbooks.objects.detailline import (
    AccountBasedExpenseLine,
    AccountBasedExpenseLineDetail,
)
from quickbooks.objects.vendor import Vendor
from quickbooks.objects.base import Ref
from qbo_auth import get_qb_client
```

- [ ] **Step 3: Commit**

```bash
git add scripts/quickbooks_sensible/import_sensible_to_quickbooks.py
git commit -m "feat: replace manual auth block with get_qb_client()"
```

---

## Manual Verification

After all tasks are complete, verify against the acceptance criteria from the spec:

- [ ] **AC1:** `python quickbooks-setup.py` (no token file) opens a browser, completes OAuth, creates `.qbo_tokens.json` with permissions `600`
- [ ] **AC2:** `python quickbooks-setup.py` (token file present) refreshes silently, no browser
- [ ] **AC3:** `python import_sensible_to_quickbooks.py` completes without `QBO_REFRESH_TOKEN` or `QBO_REALM_ID` set
- [ ] **AC4:** Delete `.qbo_tokens.json`, re-run — browser flow triggers again
- [ ] **AC5:** With port 8080 occupied: prints port-in-use error, exits 1
- [ ] **AC6:** `QBO_TOKEN_FILE=/tmp/test_tokens.json python quickbooks-setup.py` creates token at `/tmp/test_tokens.json`
