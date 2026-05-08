#!/bin/bash
# Usage: bash generate_upload_url_extra_data.sh [document_type]
# Tests that extra_data is accepted in POST /generate_upload_url/{document_type}.
# Prints the upload URL and extraction ID — pass the ID to
# retrieve_extraction_extra_data.sh to verify extra_data echoes in the response.
DOCUMENT_TYPE=${1:-auto_policy_declaration}
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/generate_upload_url_extra_data_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.sensible.so/v0/generate_upload_url/${DOCUMENT_TYPE}" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "extra_data": {
      "expected_collision_deductible": 500,
      "expected_comprehensive_deductible": 300
    }
  }')
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
echo ""
echo "Extraction ID: $(echo "$BODY" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('id','(not found)'))" 2>/dev/null)"
