---
name: sensible-quickbooks
description: Walks a developer through the Sensible + QuickBooks Online integration from setup to a working bill. Invoke whenever the user wants to set up the QuickBooks integration, run or follow the QuickBooks tutorial, connect Sensible to QuickBooks Online, automate invoice extraction into QuickBooks, or create bills from vendor invoice PDFs using Python. Use this skill even if the user says they "already have credentials" or are "partway through" — it handles all starting points.
---

# Sensible + QuickBooks Online Integration

This skill sets up the Python integration that extracts a vendor invoice with Sensible and creates a bill in QuickBooks Online. Two steps require you to act in a browser — everything else runs automatically.

## Starting point check

Before doing anything else, ask the user:

> "Quick check before we start — have you already done any of these steps?
> 1. Added the `invoices` document type to your Sensible account
> 2. Created a QuickBooks developer app and have a Client ID + Secret
> 3. Cloned the sensible-quickbooks-py repo locally
> 4. Completed the OAuth authorization step
>
> Tell me which ones are done and I'll skip ahead."

Use their answer to skip completed phases. If they're starting from scratch, begin at Phase 1.

---

## Phase 1: Collect credentials (browser steps)

Gather everything before touching the terminal. This avoids interrupting the automated phases later.

### 1a. Sensible API key

If the user hasn't done this: direct them to sign in at https://app.sensible.so and navigate to the Template library tab. Search for **invoices**, click the result, and click **Clone to account**. This takes about 2 minutes.

Then ask: "Please paste your Sensible API key — you can find it at https://app.sensible.so/account/"

Save the value as `SENSIBLE_API_KEY`.

### 1b. QuickBooks developer credentials

If the user hasn't done this, walk them through the Intuit portal:

1. Sign in at https://developer.intuit.com and navigate to your workspace
2. On the **Apps** tab, click **+** to create a new app
3. Name it (e.g. "Sensible Integration Test"), select `com.intuit.quickbooks.accounting` as the scope, verify the API Product is QuickBooks Online
4. Click **View credentials** — or open the app and go to the **Keys and credentials** tab — to get the Client ID and Client Secret
5. Go to **Settings** → **Redirect URIs** → **Development** tab → **Add URI** → enter `http://localhost:8080/callback` → **Save**
6. Click **My Hub** (upper right) → **Sandboxes** → verify a default sandbox company exists (it should be there automatically)

Then ask: "Please paste your QBO Client ID and Client Secret."

Save as `QBO_CLIENT_ID` and `QBO_CLIENT_SECRET`.

---

## Phase 2: Set up the repo

Run these, skipping any already done:

```bash
git clone https://github.com/sensible-hq/sensible-quickbooks-py.git
cd sensible-quickbooks-py
pip install sensible-sdk python-quickbooks intuit-oauth
```

Write a `.env` file in the repo directory with the credentials from Phase 1:

```
SENSIBLE_API_KEY=<value>
QBO_CLIENT_ID=<value>
QBO_CLIENT_SECRET=<value>
```

Verify the file was written correctly before continuing.

---

## Phase 3: One-time OAuth consent

Skip this phase if a token file already exists in the repo directory (check for any `.json` file that looks like a token store — typically `tokens.json` or similar).

Run the setup script, loading credentials from `.env`:

```bash
cd sensible-quickbooks-py && set -a && source .env && set +a && python quickbooks-setup.py
```

The script prints an authorization URL. Capture it from the output and surface it to the user:

> "Please open this URL in your browser and complete the QuickBooks authorization:
> [URL]
>
> Once you've authorized, come back here and let me know."

Wait for the user to confirm. After they do, verify a token file now exists in the directory. If it doesn't, the authorization didn't complete — tell the user and ask them to try again.

---

## Phase 4: Run the integration

```bash
cd sensible-quickbooks-py && set -a && source .env && set +a && python invoice_to_quickbooks.py
```

Parse the output for:
- `✓ Bill created successfully` — success
- The bill ID (printed after "ID:")
- The sandbox URL (printed after "View:")

Report to the user:

> "Done. Bill created in your QuickBooks sandbox.
> - Bill ID: [ID]
> - View it here: [URL]"

If the script fails, surface the error message directly and suggest the most likely fix:
- Auth errors → tokens may have expired, rerun Phase 3
- Missing vendor/account errors → sandbox company may not be set up, check the Intuit portal
- Sensible errors → verify the API key is correct and the `invoices` document type is cloned
