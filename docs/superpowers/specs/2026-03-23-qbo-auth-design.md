# QBO OAuth Auto-Auth Design

**Date:** 2026-03-23
**Scope:** `scripts/temp/` — sample/educational integration between Sensible and QuickBooks Online
**Goal:** Users never manually handle tokens after first-time setup.

---

## Context

The existing flow requires three manual steps on every token rotation:
1. Visit the Intuit OAuth Playground and copy an auth code
2. Run `qbo_get_tokens.py <code>` and copy tokens from stdout
3. Set `QBO_REFRESH_TOKEN` and `QBO_REALM_ID` in the environment

The new flow reduces this to a one-time browser click on first run. All subsequent runs are fully automatic.

---

## Files

| File | Change |
|---|---|
| `scripts/temp/qbo_auth.py` | New — shared auth module |
| `scripts/temp/quickbooks-setup.py` | New — first-time setup runner |
| `scripts/temp/import_sensible_to_quickbooks.py` | Updated — replace auth block with `get_qb_client()` |
| `scripts/temp/qbo_get_tokens.py` | Deleted — replaced entirely |

---

## One-Time Manual Step

Add `http://localhost:8080/callback` as an allowed redirect URI in the Intuit developer console for the app. This is required once and never again.

---

## `qbo_auth.py`

The only public interface is `get_qb_client()`. Everything else is internal.

**Token storage:**
`scripts/temp/.qbo_tokens.json` — stores `access_token`, `refresh_token`, and `realm_id`. File permissions set to 600 on write. A comment in the code notes that production use should store this at `~/.qbo_tokens.json` or equivalent.

**Environment variables (still required):**
`QBO_CLIENT_ID` and `QBO_CLIENT_SECRET` — app credentials, appropriate to keep in env. `QBO_REFRESH_TOKEN` and `QBO_REALM_ID` are no longer needed in the environment.

**Internal functions:**

- `_load_tokens()` — reads token file, returns `{}` if missing
- `_save_tokens(tokens)` — writes token file, sets permissions to 600
- `_browser_flow()` — builds the QBO authorization URL via `intuitlib.AuthClient`, opens it in the default browser, starts a one-shot `HTTPServer` on `localhost:8080` to receive the OAuth redirect, exchanges the auth code for tokens via `AuthClient.get_bearer_token()`, returns token dict

**`get_qb_client()` logic:**

1. Load tokens from file
2. If `refresh_token` present → call `auth_client.refresh()`, save updated tokens
3. If no tokens or refresh raises → run `_browser_flow()`, save tokens
4. Construct and return `QuickBooks` client

---

## `quickbooks-setup.py`

Thin entry point for first-time setup. Calls `get_qb_client()` (which triggers the browser flow when no token file exists) and prints a success message. No logic of its own — `qbo_auth.py` handles everything.

---

## `import_sensible_to_quickbooks.py`

The ~10-line auth block is replaced with:

```python
from qbo_auth import get_qb_client

print("\n[3/6] Authenticating with QuickBooks Online ...")
qb_client = get_qb_client()
print("  ✓ Connected.")
```

No other changes.

---

## Error Handling

- If the browser flow fails (user closes window, port 8080 in use, etc.) — the `HTTPServer` call blocks; if the redirect never arrives the script hangs. Acceptable for an educational script; a comment notes this limitation.
- If `refresh()` raises a `QuickbooksException` (expired/revoked token) → fall through to `_browser_flow()` automatically.
