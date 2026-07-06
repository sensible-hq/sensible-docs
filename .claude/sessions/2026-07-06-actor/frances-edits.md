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
> "Best-effort label identifying the user or credential that initiated the extraction. For extractions you initiate in the Sensible app, this is your account's email address. For extractions you initiate by using your API key, this is `api_key: <key name>` if the key has a name, or `api_key` if unnamed. For extractions you initiate using auth tokens, this is `auth_token: <creator>` if a creator is recorded, or `auth_token` if not. For extractions you initiate in the Sensible app while logged in with legacy credentials, this is `legacy: <account>`. Sensible omits this field for system-initiated extractions that lack authentication info (for example, extractions you make with email processors)."

---

## Speculated reasons (beyond stated)

**"Cognito users" → "extractions you initiate in the Sensible app"** — "Cognito" is an AWS implementation detail invisible to end users. The user-facing concept is "I logged into the Sensible app with my email." Replacing it with the scenario keeps the description grounded in the user's experience.

**"email pipeline or reprocessing" → "extractions you make with email processors"** — "reprocessing" is also internal terminology. "Email processors" is the published Sensible product name for the email extraction feature, so it's meaningful to customers. The reprocessing case (system re-running an extraction after a config update) is omitted from the example since it has no customer-visible name and the example only needs one representative case to be illustrative.

**"system-initiated extractions" kept, but qualified with "that lack authentication info"** — the longer phrase is more precise and avoids implying that all system paths always omit `actor` (future paths could set auth).
