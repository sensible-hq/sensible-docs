# QBO OAuth Auto-Auth Design

**Date:** 2026-03-23
**Scope:** `scripts/quickbooks_sensible/` — sample/educational integration between Sensible and QuickBooks Online
**Goal:** Users never manually handle tokens after first-time setup.

---

## Context

The existing flow in `scripts/quickbooks_sensible/` requires three manual steps on every token rotation:
1. Visit the Intuit OAuth Playground and copy an auth code
2. Run `qbo_get_tokens.py <code>` and copy tokens from stdout
3. Set `QBO_REFRESH_TOKEN` and `QBO_REALM_ID` in the environment

The new flow reduces this to a one-time browser click on first run. All subsequent runs are fully automatic.

**Out of scope:**
- `scripts/quickbooks-setup.py` — a separate, older script (sandbox, writes to `.env`, uses OAuth Playground redirect URI). Not part of `scripts/quickbooks_sensible/`. Left untouched.
- `docs/integrations/draft-quickbooks-tutorial.md` — describes a Zapier-based workflow; does not reference any `scripts/quickbooks_sensible/` files. Left untouched.

---

## Files

| File | Change |
|---|---|
| `scripts/quickbooks_sensible/qbo_auth.py` | New — shared auth module |
| `scripts/quickbooks_sensible/quickbooks-setup.py` | New — first-time setup runner |
| `scripts/quickbooks_sensible/import_sensible_to_quickbooks.py` | Updated — replace auth block with `get_qb_client()` |
| `scripts/quickbooks_sensible/qbo_get_tokens.py` | Deleted — confirmed no other files reference it (grep verified) |
| `scripts/quickbooks_sensible/.gitignore` | New — ignore `.qbo_tokens.json` |

---

## One-Time Manual Step

Add `http://localhost:8080/callback` as an allowed redirect URI in the Intuit developer console for the app. This is required once and never again. Document this in a comment at the top of `qbo_auth.py`.

---

## `qbo_auth.py`

The only public interface is `get_qb_client()`. Everything else is internal.

**Environment:**
Uses `environment="sandbox"` for both `AuthClient` and `QuickBooks` (educational/test integration — change to `"production"` for real use).

**Token storage:**

Default token file path: `Path(__file__).parent / ".qbo_tokens.json"` (i.e., `scripts/quickbooks_sensible/.qbo_tokens.json`).

Override: if the environment variable `QBO_TOKEN_FILE` is set, use `Path(os.environ["QBO_TOKEN_FILE"])` instead. A comment in the code should note: *"For production use, set QBO_TOKEN_FILE=~/.qbo_tokens.json (or any path outside the project directory)."*

Token file shape:
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "realm_id": "..."
}
```

`realm_id` is captured from the OAuth callback query parameter `realmId` (not from the token response). All other fields come from the `AuthClient` after calling `get_bearer_token()`.

On write: call `os.chmod(path, 0o600)` after writing. This sets permissions explicitly; it does not rely on umask.

If the token file exists but contains malformed JSON, `json.JSONDecodeError` propagates — no special handling.

**Environment variables:**

Required: `QBO_CLIENT_ID`, `QBO_CLIENT_SECRET`. If either is missing, `os.environ[key]` raises `KeyError` — acceptable failure mode for an educational script.

No longer required: `QBO_REFRESH_TOKEN`, `QBO_REALM_ID`.

Optional: `QBO_TOKEN_FILE` (path override for token storage).

**Internal functions:**

`_load_tokens(path)` — reads and JSON-parses the token file at `path`; returns `{}` if the file does not exist.

`_save_tokens(path, tokens)` — writes token dict as JSON to `path`, then calls `os.chmod(path, 0o600)`.

`_browser_flow(auth_client)` — takes an `AuthClient` instance. **Important:** this function calls `auth_client.get_bearer_token()` on the passed-in instance, which sets `auth_client.access_token` and `auth_client.refresh_token` as side effects. The caller (`get_qb_client`) relies on these side effects being present after `_browser_flow` returns.

Steps:
1. Attempt `HTTPServer(("localhost", 8080), ...)` construction. If this raises `OSError` (port in use), print `"Error: port 8080 is in use. Stop the other process and try again."` and call `sys.exit(1)`. **This must happen before opening the browser** so the user is not sent to a URL that will never receive a callback. If `get_authorization_url` subsequently raises, the server socket is not explicitly closed — acceptable for an educational script.
2. Build handler: a `BaseHTTPRequestHandler` subclass that parses `code` and `realmId` from the GET query string, responds `200 OK` with `<h1>Authorized! You can close this tab.</h1>`, and stores results in a shared `result` dict.
3. Set `server.socket.settimeout(120)`. (`socket.timeout` is an alias for `OSError` on Python 3.3+ and a subclass of `TimeoutError` on 3.11+; catching `socket.timeout` works on all supported versions.)
4. Call `auth_client.get_authorization_url([Scopes.ACCOUNTING])` to get the auth URL.
5. Open the URL with `webbrowser.open()`.
6. Print `"  Waiting for browser authorization (120s timeout)..."`.
7. Call `server.handle_request()`. If it raises `socket.timeout`, print `"Error: no callback received within 120 seconds. Did you authorize in the browser?"` and call `sys.exit(1)`.
8. Call `auth_client.get_bearer_token(result["code"], realm_id=result["realm_id"])`.
9. Return `{"access_token": auth_client.access_token, "refresh_token": auth_client.refresh_token, "realm_id": result["realm_id"]}`.

**`get_qb_client()` logic:**

1. Resolve token file path: `Path(os.environ["QBO_TOKEN_FILE"]) if "QBO_TOKEN_FILE" in os.environ else Path(__file__).parent / ".qbo_tokens.json"`.
2. Read `QBO_CLIENT_ID` and `QBO_CLIENT_SECRET` from env; construct `AuthClient(client_id=..., client_secret=..., redirect_uri="http://localhost:8080/callback", environment="production")`.
3. Load tokens from file.
4. If `refresh_token` present in loaded tokens:
   - Call `auth_client.refresh(refresh_token=tokens["refresh_token"])`.
   - On success: update `tokens["access_token"] = auth_client.access_token` and `tokens["refresh_token"] = auth_client.refresh_token` (preserving `realm_id`), call `_save_tokens()`, proceed to step 6.
   - On `AuthClientError` or `QuickbooksException` (auth-specific failures indicating the token is invalid): print a warning that tokens are invalid and re-authorization is needed, set `tokens = {}`, fall through to step 5. All other exceptions propagate.
5. If `tokens` is empty: call `_browser_flow(auth_client)`, assign the returned dict to `tokens`, call `_save_tokens()`. After this step, `auth_client.refresh_token == tokens["refresh_token"]` is guaranteed (both were set by `get_bearer_token()` inside `_browser_flow`).
6. Construct and return:
   ```python
   QuickBooks(
       auth_client=auth_client,
       refresh_token=auth_client.refresh_token,
       company_id=tokens["realm_id"],
       minorversion=75,
   )
   ```

---

## `quickbooks-setup.py`

Imports `get_qb_client` from `qbo_auth`. Calls it (triggers browser flow on first run), prints `"Setup complete. Tokens saved to <path>."` on success. No try/except — `qbo_auth` calls `sys.exit(1)` on all recoverable failures; unrecoverable exceptions (missing env vars, network errors) propagate as Python tracebacks, acceptable for an educational script.

---

## `import_sensible_to_quickbooks.py`

The existing auth block (constructing `AuthClient` and `QuickBooks` manually) is replaced with:

```python
from qbo_auth import get_qb_client

print("\n[3/6] Authenticating with QuickBooks Online ...")
qb_client = get_qb_client()
print("  ✓ Connected.")
```

`[3/6]` is correct — the script has 6 steps and auth is step 3. No other changes to the file.

---

## `scripts/quickbooks_sensible/.gitignore`

Create with:
```
.qbo_tokens.json
```

---

## Acceptance Criteria

1. Running `python quickbooks-setup.py` with `QBO_CLIENT_ID` and `QBO_CLIENT_SECRET` set opens a browser, completes the OAuth flow, and creates `scripts/quickbooks_sensible/.qbo_tokens.json` with permissions `600`.
2. Running `python quickbooks-setup.py` a second time (token file already present) refreshes the access token and updates the file without opening a browser.
3. Running `python import_sensible_to_quickbooks.py` completes the full Sensible → QBO flow without the user setting `QBO_REFRESH_TOKEN` or `QBO_REALM_ID`.
4. Deleting `.qbo_tokens.json` and re-running either script triggers the browser flow again.
5. Running with port 8080 occupied prints the port-in-use error and exits with code 1.
6. Setting `QBO_TOKEN_FILE=/tmp/test_tokens.json` and running `python quickbooks-setup.py` creates the token file at `/tmp/test_tokens.json`, not at `scripts/quickbooks_sensible/.qbo_tokens.json`.
