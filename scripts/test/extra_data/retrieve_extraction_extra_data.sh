#!/bin/bash
# Usage: bash retrieve_extraction_extra_data.sh <extraction_id>
# Tests that extra_data is echoed in GET /documents/{id}.
# Run extract_from_url_extra_data.sh or generate_upload_url_extra_data.sh first
# to get an extraction ID.
EXTRACTION_ID=${1:?Usage: bash retrieve_extraction_extra_data.sh <extraction_id>}
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/retrieve_extraction_extra_data_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
  "https://api.sensible.so/v0/documents/${EXTRACTION_ID}" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}")
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
echo ""
echo "extra_data in response: $(echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('extra_data','(not found)'))" 2>/dev/null)"
