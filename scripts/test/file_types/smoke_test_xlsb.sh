#!/bin/bash
# smoke_test_xlsb.sh
#
# Checks whether the Sensible API accepts XLSB (Excel binary workbook) files.
# XLSB content type: application/vnd.ms-excel.sheet.binary.macroenabled.12
# Added for sensible-hq/sensible#3474 (engine) and sensible-hq/sensible-app#1882 (app).
# Bug write-up: .claude/sessions/xlsb/eng-bug-report.md
#
# The script prints each curl command before running it, then the response,
# then what to expect. There's no automatic pass/fail: compare GOT with EXPECTED.
#
# Usage, from anywhere:  bash scripts/test/file_types/smoke_test_xlsb.sh
# Needs SENSIBLE_API_KEY. Uses the "cells" document type.
# Cost: checks 3, 11, 12 and 13 each run one extraction.
#
# Results on 2026-10-12:
#   1  POST /classify, XLSB                       FAIL  400 Missing request body
#   2  POST /classify/async, XLSB                 FAIL  400 Missing request body (2b skipped)
#   3  POST /extract, XLSB                        FAIL  400 Missing request body or body.document
#   4  Reference document upload, XLSB            PASS
#   5  POST /classify, XLSX (control)             PASS  reaches the engine
#   6  POST /classify, XLSM (control)             FAIL  400 Missing request body
#   7  POST /classify, XLSB bytes sent as XLSX    PASS  reaches the engine
#   8  POST /classify, XLS (control)              FAIL  400 Missing request body
#   9  POST /classify, XLSB with capital E        FAIL  415
#   10 POST /classify, CSV                        FAIL  400 Missing request body
#   11 POST /extract, CSV                         PASS
#   12 generate_upload_url, XLSB                  PASS  workaround
#   13 POST /extract, XLSB as base64 JSON         PASS  workaround

cd "$(dirname "$0")/../../.." || exit 1   # run from the repo root
mkdir -p scripts/test/file_types/outputs
exec > >(tee "scripts/test/file_types/outputs/smoke_test_xlsb_$(date +%Y-%m-%d_%H-%M-%S).log") 2>&1

# Prints a command, then runs it in this shell (so variables it sets are kept).
run() {
  local cmd
  cmd=$(cat)
  echo "\$ $cmd"
  echo "--- GOT:"
  eval "$cmd"
  echo
}

section() {
  echo
  echo "=================================================================="
  echo "$1"
  echo "EXPECTED today:     $2"
  echo "EXPECTED after fix: $3"
  echo "=================================================================="
}


section "1. POST /classify with an XLSB file" \
  "400 Missing request body" \
  "anything except 'Missing request body' or 415 (this sample gets 'No match found')"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/classify?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.ms-excel.sheet.binary.macroenabled.12" \
  --data-binary @scripts/test/assets/xlsb_sample.xlsb
CMD


section "2. POST /classify/async with an XLSB file" \
  "2a: 400 Missing request body; 2b: skipped" \
  "2a: HTTP 200 with an id and download_link; 2b: HTTP 200 {\"error\":\"No match found for document\"} (this sample matches no type)"
echo "2a. Send the file. Like /classify, the async endpoint takes the file bytes in the"
echo "    request body. It returns right away with a download_link to poll."
run <<'CMD'
ASYNC=$(curl -s -w "\nHTTP %{http_code}" -X POST \
  "https://api.sensible.so/v0/classify/async?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.ms-excel.sheet.binary.macroenabled.12" \
  --data-binary @scripts/test/assets/xlsb_sample.xlsb)
echo "$ASYNC"
CMD
echo "2b. Wait 15 seconds, then fetch the download_link (skipped if 2a returned none)"
run <<'CMD'
DOWNLOAD_LINK=$(echo "$ASYNC" | head -n -1 | jq -r '.download_link // empty' 2>/dev/null)
if [ -z "$DOWNLOAD_LINK" ]; then
  echo "skipped: no download_link"
else
  sleep 15
  curl -s -w "\nHTTP %{http_code}\n" "$DOWNLOAD_LINK"
fi
CMD


section "3. POST /extract/cells with an XLSB file" \
  "400 Missing request body or body.document" \
  "HTTP 200, status COMPLETE"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/extract/cells" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.ms-excel.sheet.binary.macroenabled.12" \
  --data-binary @scripts/test/assets/xlsb_sample.xlsb
CMD


section "4. Upload an XLSB reference document to the cells document type, then delete it" \
  "every step succeeds; step 4d shows error null and a converted_url" \
  "same"
echo "4a. Look up the cells document type's id"
run <<'CMD'
TYPE_ID=$(curl -s "https://api.sensible.so/v0/document_types" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" |
  jq -r '.[] | select(.name == "cells") | .id')
echo "TYPE_ID=$TYPE_ID"
CMD
echo "4b. Create the reference document. The response includes an upload_url."
run <<'CMD'
GOLDEN=$(curl -s -X POST \
  "https://api.sensible.so/v0/document_types/$TYPE_ID/goldens" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "xlsb_smoke_test_delete_me", "content_type": "application/vnd.ms-excel.sheet.binary.macroenabled.12"}')
echo "$GOLDEN" | jq '{id, name, upload_url: (.upload_url[0:60] + "...")}'
CMD
echo "4c. Upload the XLSB file to the upload_url"
run <<'CMD'
curl -s -w "HTTP %{http_code}\n" -X PUT "$(echo "$GOLDEN" | jq -r .upload_url)" \
  -H "Content-Type: application/vnd.ms-excel.sheet.binary.macroenabled.12" \
  --data-binary @scripts/test/assets/xlsb_sample.xlsb
CMD
echo "4d. Wait 15 seconds, then check that Sensible processed it"
run <<'CMD'
sleep 15
curl -s "https://api.sensible.so/v0/document_types/$TYPE_ID/goldens/xlsb_smoke_test_delete_me" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" |
  jq '{name, error, has_converted_url: (.converted_url != null)}'
CMD
echo "4e. Delete the test reference document (expect HTTP 204)"
run <<'CMD'
curl -s -w "HTTP %{http_code}\n" -X DELETE \
  "https://api.sensible.so/v0/document_types/$TYPE_ID/goldens/xlsb_smoke_test_delete_me" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY"
CMD


section "5. Control: POST /classify with an XLSX file" \
  "400 No match found for document (reached the engine)" \
  "same"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/classify?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  --data-binary @assets/pdfs/cell_rows.xlsx
CMD


section "6. Control: POST /classify with the XLSX file sent as XLSM" \
  "400 Missing request body (XLSM is broken too, so the bug predates XLSB)" \
  "400 No match found for document"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/classify?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.ms-excel.sheet.macroenabled.12" \
  --data-binary @assets/pdfs/cell_rows.xlsx
CMD


section "7. Control: POST /classify with the XLSB file sent as XLSX" \
  "400 No match found for document (the engine reads XLSB fine)" \
  "same"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/classify?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  --data-binary @scripts/test/assets/xlsb_sample.xlsb
CMD


section "8. Control: POST /classify with the XLSX file sent as XLS" \
  "400 Missing request body (XLS is broken too)" \
  "anything except 'Missing request body' or 415"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/classify?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.ms-excel" \
  --data-binary @assets/pdfs/cell_rows.xlsx
CMD


section "9. POST /classify with XLSB, content type spelled macroEnabled (capital E)" \
  "415 Content-Type must be ... (the check is case-sensitive)" \
  "same result as check 1 after its fix"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/classify?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/vnd.ms-excel.sheet.binary.macroEnabled.12" \
  --data-binary @scripts/test/assets/xlsb_sample.xlsb
CMD


echo
echo "Making a small CSV file for checks 10 and 11"
run <<'CMD'
CSV_FILE=$(mktemp --suffix=.csv)
printf 'name,amount\nhello,1\nand this,2\n' > "$CSV_FILE"
cat "$CSV_FILE"
CMD


section "10. POST /classify with a CSV file" \
  "400 Missing request body (classify doesn't read text bodies)" \
  "400 No match found for document"
run <<'CMD'
curl -s -w "\nHTTP %{http_code}\n" -X POST \
  "https://api.sensible.so/v0/classify?document_types=invoices,bank_statements" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: text/csv" \
  --data-binary @"$CSV_FILE"
CMD


section "11. POST /extract/cells with the same CSV file (compare with 10)" \
  "HTTP 200, status COMPLETE" \
  "same"
run <<'CMD'
curl -s -X POST "https://api.sensible.so/v0/extract/cells" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: text/csv" \
  --data-binary @"$CSV_FILE" |
  jq '{status, content_type, page_count, errors}'
CMD
rm -f "$CSV_FILE"


section "12. Workaround: extract XLSB through generate_upload_url" \
  "step 12c shows status COMPLETE and the XLSB content_type" \
  "same"
echo "12a. Get an upload URL for the cells document type"
run <<'CMD'
UPLOAD=$(curl -s -X POST "https://api.sensible.so/v0/generate_upload_url/cells" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content_type": "application/vnd.ms-excel.sheet.binary.macroenabled.12"}')
echo "$UPLOAD" | jq '{id, upload_url: (.upload_url[0:60] + "...")}'
CMD
echo "12b. Upload the XLSB file to the upload_url"
run <<'CMD'
curl -s -w "HTTP %{http_code}\n" -X PUT "$(echo "$UPLOAD" | jq -r .upload_url)" \
  -H "Content-Type: application/vnd.ms-excel.sheet.binary.macroenabled.12" \
  --data-binary @scripts/test/assets/xlsb_sample.xlsb
CMD
echo "12c. Wait 20 seconds, then retrieve the extraction"
run <<'CMD'
sleep 20
curl -s "https://api.sensible.so/v0/documents/$(echo "$UPLOAD" | jq -r .id)" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" |
  jq '{status, content_type, page_count, errors}'
CMD


section "13. Workaround: POST /extract/cells with XLSB as base64 in a JSON body" \
  "status COMPLETE and the XLSB content_type" \
  "same"
run <<'CMD'
jq -n \
  --arg doc "$(base64 -w0 scripts/test/assets/xlsb_sample.xlsb)" \
  '{document: $doc, content_type: "application/vnd.ms-excel.sheet.binary.macroenabled.12"}' |
curl -s -X POST "https://api.sensible.so/v0/extract/cells" \
  -H "Authorization: Bearer $SENSIBLE_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- |
  jq '{status, content_type, page_count, errors}'
CMD
