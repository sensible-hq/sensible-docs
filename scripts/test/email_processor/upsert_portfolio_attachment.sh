#!/bin/bash
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/upsert_portfolio_attachment_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
  "https://api.sensible.so/v0/processors/email/test3" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "attachmentSpecs": [
      {
        "kind": "portfolio",
        "docTypeIds": [
          "37674511-20cd-49a2-87dc-8e8b070ff43a"
        ],
        "segmentDocumentsWith": "llm"
      }
    ],
    "webhooks": [
      {
        "url": "https://webhook.site/b9dad6da-5902-43d8-bca9-423347f000f0"
      }
    ]
  }')
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
