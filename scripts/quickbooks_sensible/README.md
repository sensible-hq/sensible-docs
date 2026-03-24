# Sensible → QuickBooks Online Integration

Extracts data from a vendor invoice PDF using Sensible, then creates a bill in QuickBooks Online.

---

## Prerequisites

### 1. Install dependencies

```bash
pip install sensible-sdk python-quickbooks intuitlib requests
```

### 2. Set environment variables

```bash
export SENSIBLE_API_KEY=your_sensible_api_key
export QBO_CLIENT_ID=your_intuit_app_client_id
export QBO_CLIENT_SECRET=your_intuit_app_client_secret
```

### 3. Add the localhost callback to your Intuit app (one-time)

1. Go to [developer.intuit.com](https://developer.intuit.com/) and sign in.
2. Click **Dashboard** in the top nav, then select your app. If you don't have one yet, click **+ Create an app**, choose **QuickBooks Online and Payments**, and give it a name.
3. In your app, go to the **Settings** tab.
4. Under **Redirect URIs**, click **Add URI**.
5. Enter `http://localhost:8080/callback` and click **Save**.

That's it — this redirect URI is what lets the setup script catch the OAuth callback automatically instead of requiring you to copy a code manually.

---

## First-time setup

Run the setup script to authorize the app and save your QuickBooks tokens:

```bash
cd scripts/quickbooks_sensible
python quickbooks-setup.py
```

This opens a browser window asking you to sign in to QuickBooks Online and authorize the app. Once you click **Connect**, the tokens are saved to `.qbo_tokens.json` in this directory and you're done. You won't need to do this again unless the refresh token expires (after 100 days of inactivity).

---

## Run the integration

```bash
python import_sensible_to_quickbooks.py
```

This will:

1. Download the sample invoice PDF (skipped if already present)
2. Extract invoice data using Sensible (`invoices` document type)
3. Authenticate with QuickBooks using saved tokens (auto-refreshes silently)
4. Find or create an expense account
5. Find or create a vendor
6. Create a bill in QuickBooks with the extracted line items

---

## Token storage

Tokens are saved to `scripts/quickbooks_sensible/.qbo_tokens.json` (git-ignored). To store them elsewhere — recommended for any real use — set:

```bash
export QBO_TOKEN_FILE=~/.qbo_tokens.json
```

---

## Re-authorizing

If your tokens expire or are revoked, just run setup again:

```bash
python quickbooks-setup.py
```

The browser flow will trigger automatically.
