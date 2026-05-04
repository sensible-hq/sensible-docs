#!/bin/bash
# Usage: bash get_email_processor.sh <processor_name>
PROCESSOR_NAME=${1:-test1}
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/get_email_processor_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "https://api.sensible.so/v0/processors/email/${PROCESSOR_NAME}" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
