#!/bin/bash
# Expects: 404 — processor does not exist.
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/error_get_nonexistent_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
  "https://api.sensible.so/v0/processors/email/nonexistent_processor_xyz" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
