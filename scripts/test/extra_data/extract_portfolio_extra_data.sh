#!/bin/bash
# Usage: bash extract_portfolio_extra_data.sh
# Tests that extra_data is accepted in POST /extract_from_url (portfolio) and
# threads to every document in the portfolio. Pass the returned ID to
# retrieve_extraction_extra_data.sh to verify extra_data echoes in the response.
#
# Example:
#   SENSIBLE_API_KEY=your_key bash extract_portfolio_extra_data.sh
mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/extract_portfolio_extra_data_$(date +%Y-%m-%d_%H-%M-%S).json"
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.sensible.so/v0/extract_from_url" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "document_url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/portfolio.pdf",
    "types": ["1040s", "auto_policy_declaration", "bank_statements"],
    "segment_documents_with": "llm",
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
