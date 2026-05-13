#!/bin/bash
# Usage: SENSIBLE_API_KEY=<key> bash test_extra_data_prod.sh <doc_type>
# Runs the extra-data.md example against the GEICO PDF in prod.
# Poll with: curl -s "https://api.sensible.so/v0/documents/<id>" -H "Authorization: Bearer ${SENSIBLE_API_KEY}"
DOC_TYPE="${1:-extra_data}"
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/test_extra_data_prod_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.sensible.so/v0/extract_from_url/${DOC_TYPE}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  --data '{
    "document_url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/extra_data.pdf",
    "extra_data": {
      "expected_collision_deductible": 500,
      "expected_comprehensive_deductible": 300,
      "expected_insured_vehicle": "NISSAN ROGUE 2010"
    }
  }')
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
echo "$BODY" | python3 -m json.tool 2>/dev/null > "$OUTFILE"
echo ""
echo "Extraction ID: $(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','(not found)'))" 2>/dev/null)"
