#!/bin/bash
# Usage: bash retrieve.sh <extraction_id>
EXTRACTION_ID="${1:?Usage: bash retrieve.sh <extraction_id>}"
curl -s "https://api.sensible.so/v0/documents/${EXTRACTION_ID}" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" | python3 -m json.tool
