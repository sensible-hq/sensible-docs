#!/bin/bash
# ==============================================================================
# TEMPLATE — copy and adapt for each endpoint script
#
# Placeholders to replace:
#   SCRIPT_BASENAME   — snake_case name matching the operationId, e.g. get_email_processor
#   HTTP_METHOD       — GET | POST | PUT | DELETE (uppercase)
#   ENDPOINT_PATH     — full path, e.g. /processors/email/${PROCESSOR_NAME}
#   REQUEST_BODY      — JSON body string for PUT/POST; omit the -d block for GET/DELETE
#   PATH_PARAM_BLOCK  — see patterns below; omit if no path params
#
# Path param patterns:
#   Optional (GET):   PROCESSOR_NAME=${1:-default_value}
#   Required (DELETE): PROCESSOR_NAME=${1:?Usage: bash SCRIPT_BASENAME.sh <processor_name>}
#
# For endpoints with no request body (GET, DELETE): remove the -H "Content-Type" and -d lines.
# For endpoints with a 204 No Content response: BODY will be empty — the script handles this.
# ==============================================================================

# --- PATH PARAM BLOCK (if needed) ---
# PROCESSOR_NAME=${1:-my_processor}

mkdir -p "$(dirname "$0")/outputs"
OUTFILE="$(dirname "$0")/outputs/SCRIPT_BASENAME_$(date +%Y-%m-%d_%H-%M-%S).json"

RESPONSE=$(curl -s -w "\n%{http_code}" -X HTTP_METHOD \
  "https://api.sensible.so/v0/ENDPOINT_PATH" \
  -H "Authorization: Bearer ${SENSIBLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d 'REQUEST_BODY')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)
echo "HTTP $HTTP_CODE"
OUTPUT=$(echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY")
echo "$OUTPUT" | tee "$OUTFILE"
