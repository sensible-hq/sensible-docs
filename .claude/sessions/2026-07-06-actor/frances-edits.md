# Frances's edits — actor field session (2026-07-06)

Branch: `fe_actor_docs`  
File touched: `reference/openapi_extraction.json`

---

## Frances's stated reason

End users don't know what "Cognito" is. The description should be written from the user's perspective (how they made the extraction) rather than from the backend's perspective (which auth system handled it).

---

## Changes by file

### `reference/openapi_extraction.json` — `Actor` schema description

**From:**
> "Best-effort label identifying the user or credential that initiated the extraction. For Cognito users, this is the bare email address (for example, `user@example.com`). For API keys, this is `api_key: <key name>` if the key has a name, or `api_key` if unnamed. For auth tokens, this is `auth_token: <creator>` if a creator is recorded, or `auth_token` if not. For legacy credentials, this is `legacy: <account>`. Sensible omits this field for system-initiated extractions (for example, email pipeline or reprocessing)."

**To:**
> "Best-effort label identifying the user or credential that initiated the extraction. For extractions you initiate in the Sensible app, this is your account's email address. For extractions you initiate by using your API key, this is `api_key: <key name>` if the key has a name, or `api_key` if unnamed. For extractions you initiate using an authorization token, this is `auth_token: <creator>` if a creator is recorded, or `auth_token` if not. For extractions you initiate in the Sensible app while logged in with legacy credentials, this is `legacy: <account>`. Sensible omits this field for system-initiated extractions that lack authentication info (for example, extractions you make with email processors)."

---

## Speculated reasons (beyond stated)

**"Cognito users" → "extractions you initiate in the Sensible app"** — "Cognito" is an AWS implementation detail invisible to end users. The user-facing concept is "I logged into the Sensible app with my email." Replacing it with the scenario keeps the description grounded in the user's experience.

**"email pipeline or reprocessing" → "extractions you make with email processors"** — "reprocessing" is also internal terminology. "Email processors" is the published Sensible product name for the email extraction feature, so it's meaningful to customers. The reprocessing case (system re-running an extraction after a config update) is omitted from the example since it has no customer-visible name and the example only needs one representative case to be illustrative.

**"auth tokens" → "authorization tokens"** — "auth token" is ambiguous (authentication vs. authorization). Changed to "authorization token" pending eng confirmation. Flag for Horacio to verify before publishing.

**"system-initiated extractions" kept, but qualified with "that lack authentication info"** — the longer phrase is more precise and avoids implying that all system paths always omit `actor` (future paths could set auth).

---

## Edit 2 — Remove auth_token case from Actor description

**Reviewer feedback:** "at this time we only use auth tokens for human review (so they won't ever end up as actors in extractions)"

**Frances's stated reason:** The previous description didn't reason through backend capabilities vs. front-end capabilities. Auth tokens are used only for the human review flow (granting a reviewer a magic link via `/account/auth_tokens`), so they cannot produce an `actor` value in an extraction response. Including the `auth_token: <creator>` case in the Actor description was factually wrong for the extraction API context.

### `reference/openapi_extraction.json` — `Actor` schema description

**Removed sentence:**
> "For extractions you initiate using an authorization token, this is `auth_token: <creator>` if a creator is recorded, or `auth_token` if not."

**Result:** The description now covers only the cases that can actually appear as actors in extraction responses: Sensible app (email), API key, legacy credentials, and the system-omitted case.

---

## Edit 3 — "the value is" + quote string values in Actor description

**Branch:** `v0` (committed directly)  
**Commit:** `7ee7f7912`

**Frances's stated reason:** "this is" was ambiguous and the values are strings, so they should be in quotes — the edit is more accurate and precise.

### `reference/openapi_extraction.json` — `Actor` schema description

**Pattern changed throughout:** `this is <value>` → `the value is "<value>"` (quoted)

- `this is your account's email address` → `the value is your account's email address` (email left unquoted — it's not a fixed string)
- `` this is `api_key: <key name>` `` → `` the value is `"api_key: <key name>"` ``
- `` this is `api_key` `` → `` the value is `"api_key"` ``
- `` this is `legacy: <account>` `` → `` the value is `"legacy: <account>"` ``
