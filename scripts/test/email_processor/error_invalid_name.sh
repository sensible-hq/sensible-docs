#!/bin/bash
# Expects: 400 — processor name contains invalid characters (uppercase, special chars).
# Valid names must match ^[a-z0-9_]+$.
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/error_invalid_name_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  "https://api.sensible.so/v0/processors/email/Test!_3%23%24" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "webhooks": [
      {
        "url": "https://webhook.site/f3a2b1c4-d5e6-7890-abcd-1234567890ab"
      }
    ],
    "bodySpec": {
      "kind": "doctype",
      "docTypeId": "1a2b3c4d-5e6f-7890-a1b2-c3d4e5f67890"
    }
  }')
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
