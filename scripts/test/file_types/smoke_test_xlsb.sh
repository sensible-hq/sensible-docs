#!/bin/bash
# smoke_test_xlsb.sh
# Asserts the OpenAPI spec claims that the API accepts XLSB (Excel binary workbook)
# files, content type application/vnd.ms-excel.sheet.binary.macroenabled.12.
# Added for sensible-hq/sensible#3474 and sensible-hq/sensible-app#1882.
#
# Spec claims, binary request body (SupportedFileTypes / extraction request body):
#   [1] POST /classify
#   [2] POST /classify/async
#   [3] POST /extract/{document_type}
#
# Spec claims, configuration API (PostGolden.content_type):
#   [4] POST /document_types/{id}/goldens with the XLSB content_type, PUT the file
#       to upload_url, then GET shows the reference document processed without error.
#       The script deletes the reference document afterward.
#
# Controls, to tell an XLSB problem from a general one:
#   [5] XLSX bytes sent as XLSX to /classify (should reach the engine)
#   [6] XLSX bytes sent as XLSM to /classify (XLSM is the other macroenabled type)
#   [7] XLSB bytes sent as XLSX to /classify (proves the engine reads the XLSB file)
#
# "Reaches the engine" means the response isn't "Missing request body" (body dropped
# before the engine) or HTTP 415 (content type rejected). /classify answers "No match
# found" for this sample, which counts as reaching the engine.
#
# Known result on 2026-10-12: [4], [5] and [7] pass. [1], [2], [3] and [6] fail with
# "Missing request body" for both macroenabled types, so the gateway likely drops
# those binary bodies. Re-run after a fix.
#
# Usage: SENSIBLE_API_KEY=<key> bash smoke_test_xlsb.sh [document_type]
# document_type defaults to "cells". It's used for [3] and [4].

DOCUMENT_TYPE=${1:-cells}
CLASSIFY_TYPES="invoices,bank_statements"
API_BASE="https://api.sensible.so/v0"
SCRIPT_DIR="$(dirname "$0")"
XLSB_FILE="$SCRIPT_DIR/../assets/xlsb_sample.xlsb"
XLSX_FILE="$SCRIPT_DIR/../../../assets/pdfs/cell_rows.xlsx"
GOLDEN_NAME="xlsb_smoke_test_delete_me"
OUTDIR="$SCRIPT_DIR/outputs"
OUTFILE="$OUTDIR/smoke_test_xlsb_$(date +%Y-%m-%d_%H-%M-%S).log"
AUTH="Authorization: Bearer ${SENSIBLE_API_KEY:?Set SENSIBLE_API_KEY}"

CT_XLSB="application/vnd.ms-excel.sheet.binary.macroenabled.12"
CT_XLSM="application/vnd.ms-excel.sheet.macroenabled.12"
CT_XLSX="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

PASS=0
FAIL=0
mkdir -p "$OUTDIR"
exec > >(tee "$OUTFILE") 2>&1

pass() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

# Posts a file as a binary body and asserts the request reached the engine.
assert_body_reaches_engine() {
  local label=$1 url=$2 content_type=$3 file=$4
  local response code body
  response=$(curl -s -w "\n%{http_code}" -X POST "$url" -H "$AUTH" \
    -H "Content-Type: $content_type" --data-binary @"$file")
  code=$(echo "$response" | tail -1)
  body=$(echo "$response" | head -n -1)
  if [ "$code" = "415" ] || echo "$body" | grep -q "^Missing request body"; then
    fail "$label → HTTP $code: ${body:0:120}"
  else
    pass "$label → HTTP $code: ${body:0:120}"
  fi
}

echo "== Binary request body endpoints"
assert_body_reaches_engine "[1] POST /classify, XLSB" \
  "$API_BASE/classify?document_types=$CLASSIFY_TYPES" "$CT_XLSB" "$XLSB_FILE"
assert_body_reaches_engine "[2] POST /classify/async, XLSB" \
  "$API_BASE/classify/async?document_types=$CLASSIFY_TYPES" "$CT_XLSB" "$XLSB_FILE"
assert_body_reaches_engine "[3] POST /extract/$DOCUMENT_TYPE, XLSB" \
  "$API_BASE/extract/$DOCUMENT_TYPE" "$CT_XLSB" "$XLSB_FILE"

echo "== Reference document upload"
TYPE_ID=$(curl -s "$API_BASE/document_types" -H "$AUTH" |
  python3 -c "import sys,json; print(next((t['id'] for t in json.load(sys.stdin) if t['name']=='$DOCUMENT_TYPE'),''))")
if [ -z "$TYPE_ID" ]; then
  fail "[4] document type '$DOCUMENT_TYPE' not found"
else
  trap 'curl -s -o /dev/null -X DELETE "$API_BASE/document_types/$TYPE_ID/goldens/$GOLDEN_NAME" -H "$AUTH"' EXIT
  UPLOAD_URL=$(curl -s -X POST "$API_BASE/document_types/$TYPE_ID/goldens" -H "$AUTH" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$GOLDEN_NAME\",\"content_type\":\"$CT_XLSB\"}" |
    python3 -c "import sys,json; print(json.load(sys.stdin).get('upload_url',''))" 2>/dev/null)
  if [ -z "$UPLOAD_URL" ]; then
    fail "[4] POST goldens returned no upload_url"
  else
    PUT_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$UPLOAD_URL" \
      -H "Content-Type: $CT_XLSB" --data-binary @"$XLSB_FILE")
    STATE=""
    for _ in $(seq 1 20); do
      STATE=$(curl -s "$API_BASE/document_types/$TYPE_ID/goldens/$GOLDEN_NAME" -H "$AUTH" |
        python3 -c "
import sys, json
d = json.load(sys.stdin)
print('error: ' + str(d['error']) if d.get('error') else ('ok' if d.get('converted_url') else 'pending'))")
      [ "$STATE" != "pending" ] && break
      sleep 3
    done
    [ "$PUT_CODE" = "200" ] && [ "$STATE" = "ok" ] &&
      pass "[4] reference document upload → processed" ||
      fail "[4] reference document upload → PUT HTTP $PUT_CODE, state: $STATE"
  fi
fi

echo "== Controls"
assert_body_reaches_engine "[5] POST /classify, XLSX bytes as XLSX" \
  "$API_BASE/classify?document_types=$CLASSIFY_TYPES" "$CT_XLSX" "$XLSX_FILE"
assert_body_reaches_engine "[6] POST /classify, XLSX bytes as XLSM" \
  "$API_BASE/classify?document_types=$CLASSIFY_TYPES" "$CT_XLSM" "$XLSX_FILE"
assert_body_reaches_engine "[7] POST /classify, XLSB bytes as XLSX" \
  "$API_BASE/classify?document_types=$CLASSIFY_TYPES" "$CT_XLSX" "$XLSB_FILE"

echo
echo "Results: $PASS passed, $FAIL failed. Log: $OUTFILE"
[ "$FAIL" -eq 0 ]
