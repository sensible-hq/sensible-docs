import base64
import os
import sys
import requests

if len(sys.argv) != 2:
    print("Usage: python qbo_get_tokens.py <authorization_code>")
    sys.exit(1)

client_id = os.environ["QBO_CLIENT_ID"]
client_secret = os.environ["QBO_CLIENT_SECRET"]
auth_code = sys.argv[1]
redirect_uri = "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"

credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

resp = requests.post(
    "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "Authorization": f"Basic {credentials}",
    },
    data={
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
    },
)

resp.raise_for_status()
print(f"Status: {resp.status_code}")
print(resp.json())