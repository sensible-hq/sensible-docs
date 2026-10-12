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
#   [8] XLSX bytes sent as XLS (application/vnd.ms-excel) to /classify
#
# Related checks:
#   [9]  XLSB content type with IANA casing (macroEnabled) to /classify. Media types are
#        case-insensitive, and Python's mimetypes module sends this casing.
#   [10] Real CSV to /classify. Compare with [11].
#   [11] Real CSV to /extract/{document_type}
#   [12] XLSB through POST /generate_upload_url/{document_type}, PUT the file, then
#        poll GET /documents/{id} for COMPLETE. This is the workaround while [1]–[3] fail.
#
# "Reaches the engine" means the response isn't "Missing request body" (body dropped
# before the engine) or HTTP 415 (content type rejected). /classify answers "No match
# found" for this sample, which counts as reaching the engine.
#
# Known result on 2026-10-12: [4], [5], [7], [11] and [12] pass. [1], [2], [3], [6] and
# [8] fail with "Missing request body": the API Gateway binaryMediaTypes list in
# packages/infra-stage-ephemeral/infra/gatewayV1.ts (sensible-hq/sensible) omits XLS,
# XLSM and XLSB. [9] fails with HTTP 415 (case-sensitive content type check). [10] fails
# because the classify handler reads only binary bodies. Re-run after a fix.
#
# Cost: [3], [11] and [12] each run an extraction.
#
# Usage: SENSIBLE_API_KEY=<key> bash smoke_test_xlsb.sh [document_type]
# document_type defaults to "cells". It's used for [3] and [4].

DOCUMENT_TYPE=${1:-cells}
CLASSIFY_TYPES="invoices,bank_statements"
API_BASE="https://api.sensible.so/v0"
SCRIPT_DIR="$(dirname "$0")"
XLSB_FILE="$SCRIPT_DIR/../assets/xlsb_sample.xlsb"
XLSX_FILE="$SCRIPT_DIR/../../../assets/pdfs/cell_rows.xlsx"
CSV_FILE="$(mktemp --suffix=.csv)"
printf 'name,amount\nhello,1\nand this,2\n' > "$CSV_FILE"
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
assert_body_reaches_engine "[8] POST /classify, XLSX bytes as XLS" \
  "$API_BASE/classify?document_types=$CLASSIFY_TYPES" "application/vnd.ms-excel" "$XLSX_FILE"

echo "== Related checks"
assert_body_reaches_engine "[9] POST /classify, XLSB as macroEnabled (IANA casing)" \
  "$API_BASE/classify?document_types=$CLASSIFY_TYPES" \
  "application/vnd.ms-excel.sheet.binary.macroEnabled.12" "$XLSB_FILE"
assert_body_reaches_engine "[10] POST /classify, real CSV" \
  "$API_BASE/classify?document_types=$CLASSIFY_TYPES" "text/csv" "$CSV_FILE"
assert_body_reaches_engine "[11] POST /extract/$DOCUMENT_TYPE, real CSV" \
  "$API_BASE/extract/$DOCUMENT_TYPE" "text/csv" "$CSV_FILE"

GEN=$(curl -s -X POST "$API_BASE/generate_upload_url/$DOCUMENT_TYPE" -H "$AUTH" \
  -H "Content-Type: application/json" -d "{\"content_type\":\"$CT_XLSB\"}")
DOC_ID=$(echo "$GEN" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
GEN_URL=$(echo "$GEN" | python3 -c "import sys,json; print(json.load(sys.stdin).get('upload_url',''))" 2>/dev/null)
if [ -z "$GEN_URL" ]; then
  fail "[12] generate_upload_url returned no upload_url: ${GEN:0:120}"
else
  curl -s -o /dev/null -X PUT "$GEN_URL" -H "Content-Type: $CT_XLSB" --data-binary @"$XLSB_FILE"
  DOC_STATUS=""
  for _ in $(seq 1 30); do
    DOC_STATUS=$(curl -s "$API_BASE/documents/$DOC_ID" -H "$AUTH" |
      python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null)
    case "$DOC_STATUS" in COMPLETE|FAILED) break ;; esac
    sleep 3
  done
  [ "$DOC_STATUS" = "COMPLETE" ] &&
    pass "[12] generate_upload_url + PUT, XLSB → COMPLETE" ||
    fail "[12] generate_upload_url + PUT, XLSB → status: $DOC_STATUS"
fi
rm -f "$CSV_FILE"

echo
echo "Results: $PASS passed, $FAIL failed. Log: $OUTFILE"
[ "$FAIL" -eq 0 ]
