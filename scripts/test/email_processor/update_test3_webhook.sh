#!/bin/bash
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/update_test3_webhook_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  "https://api.sensible.so/v0/processors/email/test3" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "bodySpec": {
      "kind": "doctype",
      "docTypeId": "37674511-20cd-49a2-87dc-8e8b070ff43a"
    },
    "attachmentSpecs": [
      {
        "kind": "doctype",
        "docTypeId": "37674511-20cd-49a2-87dc-8e8b070ff43a"
      }
    ],
    "webhooks": [
      {
        "url": "https://webhook.site/1234"
      }
    ]
  }')
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
