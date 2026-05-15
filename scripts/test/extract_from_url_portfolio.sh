#!/bin/bash

mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/extract_from_url_portfolio_$(date +%Y-%m-%d_%H-%M-%S).json"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "https://api.sensible.so/v0/extract_from_url?environment=production&document_name=portfolio_bank_paystub_tax" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "document_url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/portfolio_bank_paystub_tax.pdf",
    "types": [
      "bank_statements",
      "pay_stubs",
      "1040s"
    ],
    "segment_documents_with": "llm"
  }')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
