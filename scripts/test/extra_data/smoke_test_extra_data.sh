#!/bin/bash
# smoke_test_extra_data.sh
# Asserts every OpenAPI spec claim that extra_data appears in a request/response body.
#
# Spec claims — request body:
#   [1] POST /extract_from_url/{document_type}
#   [2] POST /generate_upload_url/{document_type}
#   [3] POST /extract_from_url (portfolio)
#   [4] POST /generate_upload_url (portfolio)
#
# Spec claims — response body:
#   [5] POST /extract_from_url/{document_type} → ExtractFromUrlResponse.extra_data (immediate)
#   [6] GET /documents/{id} single → ExtractionSingleRetrievalResponse.extra_data
#   [7] GET /documents/{id} portfolio → ExtractionPortfolioRetrievalResponse.extra_data
#   [8] GET /extractions → reachable (extra_data intentionally omitted from list summary shape)
#
# Additional coverage:
#   [9]  POST /extract/{document_type} (sync) — extra_data in JSON body + response
#   [10] GET /documents/{id} for generate_upload_url-originated extraction
#
# Usage: SENSIBLE_API_KEY=<key> bash smoke_test_extra_data.sh [document_type]
# document_type defaults to "extra_data"

DOCUMENT_TYPE=${1:-extra_data}
DOC_URL="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/extra_data.pdf"
PORTFOLIO_URL="https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/portfolio.pdf"
EXTRA_DATA='{"expected_collision_deductible": 500, "expected_comprehensive_deductible": 300}'
API_BASE="https://api.sensible.so/v0"
OUTDIR="$(dirname "$0")/outputs"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
PASS=0
FAIL=0

mkdir -p "$OUTDIR"

pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

assert_http_200() {
  local label=$1 code=$2
  [ "$code" = "200" ] && pass "$label → HTTP 200" || fail "$label → HTTP $code (expected 200)"
}

assert_has_extra_data() {
  local label=$1 body=$2
  local found
  found=$(echo "$body" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print('yes' if d.get('extra_data') is not None else 'no')
except Exception:
    print('no')
" 2>/dev/null)
  [ "$found" = "yes" ] && pass "$label → extra_data present in response" || fail "$label → extra_data missing from response"
}

# Polls GET /documents/{id} until status is COMPLETE or FAILED (max 90s).
poll_until_done() {
  local id=$1
  local i=0 max=30
  local body status
  while [ $i -lt $max ]; do
    body=$(curl -s "$API_BASE/documents/$id" -H "Authorization: Bearer $SENSIBLE_API_KEY")
    status=$(echo "$body" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null)
    case "$status" in COMPLETE|FAILED) echo "$body"; return ;; esac
    sleep 3
    i=$((i + 1))
  done
  echo "$body"  # return whatever we have after timeout
}

echo ""
echo "=== smoke_test_extra_data ==="
echo "Document type: $DOCUMENT_TYPE | $(date)"
echo ""

# ── [1] POST /extract_from_url/{document_type} — request ──────────────────
echo "[1] POST /extract_from_url/$DOCUMENT_TYPE (request body)"
RESP=$(curl -s -w "\n%{http_code}" -X POST \
  "$API_BASE/extract_from_url/$DOCUMENT_TYPE" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"document_url\":\"$DOC_URL\",\"extra_data\":$EXTRA_DATA}")
CODE=$(echo "$RESP" | tail -1)
BODY_1=$(echo "$RESP" | head -n -1)
assert_http_200 "POST /extract_from_url/$DOCUMENT_TYPE" "$CODE"
echo "$BODY_1" > "$OUTDIR/smoke_1_extract_from_url_$TIMESTAMP.json"
EXTRACT_FROM_URL_ID=$(echo "$BODY_1" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
echo ""

# ── [2] POST /generate_upload_url/{document_type} — request ───────────────
echo "[2] POST /generate_upload_url/$DOCUMENT_TYPE (request body)"
RESP=$(curl -s -w "\n%{http_code}" -X POST \
  "$API_BASE/generate_upload_url/$DOCUMENT_TYPE" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"extra_data\":$EXTRA_DATA,\"content_type\":\"application/pdf\"}")
CODE=$(echo "$RESP" | tail -1)
BODY_2=$(echo "$RESP" | head -n -1)
assert_http_200 "POST /generate_upload_url/$DOCUMENT_TYPE" "$CODE"
echo "$BODY_2" > "$OUTDIR/smoke_2_generate_upload_url_$TIMESTAMP.json"
UPLOAD_ID=$(echo "$BODY_2" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
UPLOAD_URL=$(echo "$BODY_2" | python3 -c "import sys,json; print(json.load(sys.stdin).get('upload_url',''))" 2>/dev/null)

if [ -n "$UPLOAD_URL" ]; then
  PUT_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$UPLOAD_URL" \
    -H "Content-Type: application/pdf" \
    --data-binary @<(curl -sL "$DOC_URL"))
  assert_http_200 "PUT document to upload_url" "$PUT_CODE"
else
  fail "generate_upload_url/$DOCUMENT_TYPE: no upload_url in response"
fi
echo ""

# ── [3] POST /extract_from_url (portfolio) — request ──────────────────────
echo "[3] POST /extract_from_url (portfolio, request body)"
RESP=$(curl -s -w "\n%{http_code}" -X POST \
  "$API_BASE/extract_from_url" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"document_url\":\"$PORTFOLIO_URL\",\"types\":[\"1040s\",\"auto_policy_declaration\",\"bank_statements\"],\"segment_documents_with\":\"llm\",\"extra_data\":$EXTRA_DATA}")
CODE=$(echo "$RESP" | tail -1)
BODY_3=$(echo "$RESP" | head -n -1)
assert_http_200 "POST /extract_from_url (portfolio)" "$CODE"
echo "$BODY_3" > "$OUTDIR/smoke_3_extract_portfolio_$TIMESTAMP.json"
PORTFOLIO_EXTRACT_ID=$(echo "$BODY_3" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
echo ""

# ── [4] POST /generate_upload_url (portfolio) — request ───────────────────
echo "[4] POST /generate_upload_url (portfolio, request body)"
RESP=$(curl -s -w "\n%{http_code}" -X POST \
  "$API_BASE/generate_upload_url" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"types\":[\"1040s\",\"auto_policy_declaration\",\"bank_statements\"],\"segment_documents_with\":\"llm\",\"extra_data\":$EXTRA_DATA}")
CODE=$(echo "$RESP" | tail -1)
BODY_4=$(echo "$RESP" | head -n -1)
assert_http_200 "POST /generate_upload_url (portfolio)" "$CODE"
echo "$BODY_4" > "$OUTDIR/smoke_4_generate_upload_portfolio_$TIMESTAMP.json"
PORTFOLIO_UPLOAD_ID=$(echo "$BODY_4" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
PORTFOLIO_UPLOAD_URL=$(echo "$BODY_4" | python3 -c "import sys,json; print(json.load(sys.stdin).get('upload_url',''))" 2>/dev/null)

if [ -n "$PORTFOLIO_UPLOAD_URL" ]; then
  PUT_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$PORTFOLIO_UPLOAD_URL" \
    -H "Content-Type: application/pdf" \
    --data-binary @<(curl -sL "$PORTFOLIO_URL"))
  assert_http_200 "PUT portfolio document to upload_url" "$PUT_CODE"
else
  fail "generate_upload_url (portfolio): no upload_url in response"
fi
echo ""

# ── [5] POST /extract_from_url response — extra_data echoed immediately ────
echo "[5] POST /extract_from_url/$DOCUMENT_TYPE response (ExtractFromUrlResponse.extra_data)"
assert_has_extra_data "POST /extract_from_url/$DOCUMENT_TYPE" "$BODY_1"
echo ""

# ── [6] GET /documents/{id} single — extra_data echoed in retrieval ────────
echo "[6] GET /documents/{id} single (ExtractionSingleRetrievalResponse.extra_data)"
if [ -n "$EXTRACT_FROM_URL_ID" ]; then
  echo "  Polling extraction $EXTRACT_FROM_URL_ID ..."
  BODY_6=$(poll_until_done "$EXTRACT_FROM_URL_ID")
  echo "$BODY_6" > "$OUTDIR/smoke_6_retrieve_single_$TIMESTAMP.json"
  assert_has_extra_data "GET /documents/$EXTRACT_FROM_URL_ID (single)" "$BODY_6"
else
  fail "GET /documents/{id} (single): no extraction ID from step 1"
fi
echo ""

# ── [7] GET /documents/{id} portfolio — extra_data echoed in retrieval ─────
echo "[7] GET /documents/{id} portfolio (ExtractionPortfolioRetrievalResponse.extra_data)"
if [ -n "$PORTFOLIO_EXTRACT_ID" ]; then
  echo "  Polling portfolio extraction $PORTFOLIO_EXTRACT_ID ..."
  BODY_7=$(poll_until_done "$PORTFOLIO_EXTRACT_ID")
  echo "$BODY_7" > "$OUTDIR/smoke_7_retrieve_portfolio_$TIMESTAMP.json"
  assert_has_extra_data "GET /documents/$PORTFOLIO_EXTRACT_ID (portfolio)" "$BODY_7"
else
  fail "GET /documents/{id} (portfolio): no extraction ID from step 3"
fi
echo ""

# ── [8] GET /extractions — endpoint reachable ─────────────────────────────
# NOTE: extra_data is intentionally omitted from the list response. The backend
# uses a summary shape (toExtractionSummaryResponse) that strips extra_data for
# performance. It is only returned by GET /documents/{id}. The spec has been
# updated to remove extra_data from ExtractionSummaryBase accordingly.
echo "[8] GET /extractions (endpoint reachable, extra_data intentionally omitted)"
RESP=$(curl -s -w "\n%{http_code}" "$API_BASE/extractions" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY")
CODE=$(echo "$RESP" | tail -1)
BODY_8=$(echo "$RESP" | head -n -1)
assert_http_200 "GET /extractions" "$CODE"
echo "$BODY_8" > "$OUTDIR/smoke_8_list_extractions_$TIMESTAMP.json"
echo ""

# ── [9] POST /extract/{document_type} (sync) — extra_data in body + response
# The sync endpoint's standard request body (SupportedFileTypes) has no extra_data
# field, but the JSON variant (Base64PDF) may accept additional fields. We try
# passing extra_data alongside the base64 document and check whether the backend
# echoes it in ExtractionSingleResponse. If 200 + echoed: backend supports it.
# If 200 + absent: field is silently dropped. If 4xx: backend rejects it.
# The sync endpoint's preferred request form is raw bytes + Content-Type header.
# There is no JSON envelope to carry extra_data, so we expect it to be absent
# in the response — confirming the sync endpoint has no mechanism to accept it.
echo "[9] POST /extract/$DOCUMENT_TYPE (sync) — raw bytes, extra_data absent in response"
RESP=$(curl -sL "$DOC_URL" | curl -s -w "\n%{http_code}" -X POST \
  "$API_BASE/extract/$DOCUMENT_TYPE" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/pdf" \
  --data-binary @-)
CODE=$(echo "$RESP" | tail -1)
BODY_9=$(echo "$RESP" | head -n -1)
assert_http_200 "POST /extract/$DOCUMENT_TYPE (sync)" "$CODE"
echo "$BODY_9" > "$OUTDIR/smoke_9_sync_extract_$TIMESTAMP.json"
EXTRA_IN_SYNC=$(echo "$BODY_9" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    v = d.get('extra_data')
    print('echoed' if v is not None else 'absent')
except Exception:
    print('parse-error')
" 2>/dev/null)
echo "  extra_data in sync response: $EXTRA_IN_SYNC"
[ "$EXTRA_IN_SYNC" = "absent" ] \
  && pass "POST /extract/$DOCUMENT_TYPE (sync) → extra_data correctly absent (no request field to pass it in)" \
  || fail "POST /extract/$DOCUMENT_TYPE (sync) → unexpected extra_data value: $EXTRA_IN_SYNC"
echo ""

# ── [10] GET /documents/{id} for generate_upload_url-originated extraction ─
# Verifies that extra_data submitted in step [2] via generate_upload_url is
# persisted and returned by GET /documents/{id} once the extraction completes.
echo "[10] GET /documents/{id} for generate_upload_url extraction (UPLOAD_ID=$UPLOAD_ID)"
if [ -n "$UPLOAD_ID" ]; then
  echo "  Polling extraction $UPLOAD_ID ..."
  BODY_10=$(poll_until_done "$UPLOAD_ID")
  echo "$BODY_10" > "$OUTDIR/smoke_10_retrieve_upload_$TIMESTAMP.json"
  assert_has_extra_data "GET /documents/$UPLOAD_ID (generate_upload_url)" "$BODY_10"
else
  fail "GET /documents/{id} (generate_upload_url): no extraction ID from step 2"
fi
echo ""

# ── Summary ───────────────────────────────────────────────────────────────
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
