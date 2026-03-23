"""
If you used the Intuit OAuth 2.0 Playground to get an authorization code,
run this immediately to exchange it for tokens. Auth codes expire quickly.

Usage:
    python exchange_tokens.py <auth_code> <realm_id>
"""

import sys
import os
from intuitlib.client import AuthClient

if len(sys.argv) != 3:
    sys.exit("Usage: python exchange_tokens.py <auth_code> <realm_id>")

auth_code = sys.argv[1]
realm_id  = sys.argv[2]

auth_client = AuthClient(
    client_id=os.environ["QBO_CLIENT_ID"],
    client_secret=os.environ["QBO_CLIENT_SECRET"],
    # Must match exactly what's configured in your Intuit Developer app.
    redirect_uri="https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl",
    environment="sandbox",  # change to "production" when ready
)

auth_client.get_bearer_token(auth_code, realm_id=realm_id)

env_path = os.path.join(os.path.dirname(__file__), ".env")
with open(env_path, "w") as f:
    f.write(f'QBO_CLIENT_ID="{os.environ["QBO_CLIENT_ID"]}"\n')
    f.write(f'QBO_CLIENT_SECRET="{os.environ["QBO_CLIENT_SECRET"]}"\n')
    f.write(f'QBO_REFRESH_TOKEN="{auth_client.refresh_token}"\n')
    f.write(f'QBO_REALM_ID="{realm_id}"\n')

print(f"Tokens written to {env_path}")
print(f"  Realm ID:       {realm_id}")
print(f"  Refresh token:  {auth_client.refresh_token[:20]}...")
