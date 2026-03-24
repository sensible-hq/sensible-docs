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
