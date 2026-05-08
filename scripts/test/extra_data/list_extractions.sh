#!/bin/bash
# Usage: bash list_extractions.sh
# Calls GET /extractions and prints the extra_data field from each extraction
# in the response to verify it echoes back on the list endpoint.
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/list_extractions_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
  "https://api.sensible.so/v0/extractions" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
echo ""
echo "=== extra_data per extraction ==="
echo "$BODY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
for e in d.get('extractions', []):
    print(f\"{e.get('id','?')} | extra_data: {e.get('extra_data')}\")
" 2>/dev/null
