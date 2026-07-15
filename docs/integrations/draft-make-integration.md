---
title: Make tutorial
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: 'extract documents and route data with Make'
  robots: index
next:
  description: ''
---
This topic describes how to configure a two-scenario Make workflow that extracts data from documents and adds the extracted data as rows in a Google Sheets spreadsheet using Sensible's API.

Make supports this workflow as follows:

* The first scenario receives a document URL from any source and calls the Sensible API to start extracting data.
* The second scenario triggers when Sensible completes the extraction and adds the structured data to Google Sheets.

## Prerequisite: Configure 1040 extractions in Sensible

Follow the steps in [Getting started with out-of-the-box extractions](doc:library-quickstart) to clone the `1040s` document type to your account.

## Prerequisite: Configure accounts

1. Sign in or create a [Make account](https://make.com/).

2. Create a Google Sheets spreadsheet as a destination for extracted data. Name it `1040s_extracted`. Add the following column headings to the first sheet: **extraction id**, **taxpayer name**, and **adjusted gross income**.

3. Copy your Sensible API key from your [account page](https://app.sensible.so/account/).

## Scenario 1: Receive document URL and start extraction

See the following steps to configure Scenario 1.

1. Create a new scenario in Make.

2. For the trigger, take the following steps:

   1. Setup:
      1. **App**: Webhooks
      2. **Module**: Custom Webhook
   2. Configure:
      1. Click **Add** to create a new webhook.
      2. Name the webhook `sensible-start-extraction`.
      3. Copy the generated webhook URL. You will use this URL to send document URLs to Make from any source — for example, a form submission, a Google Drive file event, or a manual API call.
   3. Test:
      1. Click **OK**.

3. Add an HTTP module to call the Sensible extraction API. Take the following steps:

   1. Setup:
      1. **App**: HTTP
      2. **Module**: Make a Request
   2. Configure:
      1. **URL**: `https://api.sensible.so/v0/extract_from_url/1040s`
      2. **Method**: POST
      3. **Headers**:
         
         1. Add a header with **Name**: `Authorization` and **Value**: `Bearer YOUR_API_KEY` (replace `YOUR_API_KEY` with your Sensible API key).
         2. Add a header with **Name**: `Content-Type` and **Value**: `application/json`.
      4. **Body type**: Raw
      5. **Content type**: JSON (application/json)
      6. **Request content**: Enter the following JSON, replacing `SCENARIO_2_WEBHOOK_URL` with the webhook URL you will generate in Scenario 2:
         
         ```json
         {
           "document_url": "{{1.document_url}}",
           "webhook": {
             "url": "SCENARIO_2_WEBHOOK_URL",
             "payload": "{{1.document_url}}"
           }
         }
         ```
         **Note:** `{{1.document_url}}` maps the `document_url` field from the incoming webhook payload. The `payload` field passes the source URL back to Scenario 2 so you can correlate the extraction with the original document.
      7. **Parse response**: Yes
   3. Test:
      1. Click **OK**.
      2. To test, send a POST request to the Scenario 1 webhook URL with the following JSON body:
         ```json
         {
           "document_url": "https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/1040_2021_sample.pdf"
         }
         ```
      3. Verify that Make received the request and that the HTTP module returned a `200` status with a `WAITING` extraction status in the response body.

4. Click **Save** and turn the scenario on.

## Scenario 2: Receive extraction results and add to Google Sheets

See the following steps to configure Scenario 2.

1. Create a new scenario in Make.

2. For the trigger, take the following steps:

   1. Setup:
      1. **App**: Webhooks
      2. **Module**: Custom Webhook
   2. Configure:
      1. Click **Add** to create a new webhook.
      2. Name the webhook `sensible-extraction-complete`.
      3. Copy the generated webhook URL.
      4. Return to Scenario 1 and replace `SCENARIO_2_WEBHOOK_URL` in the HTTP module request body with this URL.
   3. Test:
      1. Click **OK**.
      2. Run Scenario 1 once with the example document URL to send a test extraction to this webhook.
      3. Verify that Make received the webhook payload and detected the data structure, including the `parsed_document` object.

3. Add a Google Sheets module to write the extracted data. Take the following steps:

   1. Setup:
      1. **App**: Google Sheets
      2. **Module**: Add a Row
      3. **Connection**: Your Google account.
   2. Configure:
      1. **Spreadsheet ID**: Select the `1040s_extracted` spreadsheet you created in the Prerequisites steps.
      2. **Sheet Name**: Select the sheet with your column headings.
      3. For each column, map the corresponding value from the webhook payload:
         1. **extraction id**: `{{1.id}}`
         2. **taxpayer name**: `{{1.parsed_document.name.value}}`
         3. **adjusted gross income**: `{{1.parsed_document.adjusted_gross_income.value}}`
   3. Test:
      1. Click **Test Step** to verify that Make creates a row in your spreadsheet with the example extraction data.

4. Click **Save** and turn the scenario on.

## (Optional) Test your integration

Congratulations, your integration is now live! Take the following steps to continue populating a spreadsheet from example documents:

1. Download [another example 1040 document](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/1040_2022_sample.pdf) to test your integration.

2. For each document, send a POST request to the Scenario 1 webhook URL with the document's publicly accessible URL in the `document_url` field.

3. After Sensible completes the extraction (typically within a minute), verify that new rows appear in your `1040s_extracted` Google Sheets spreadsheet.

## (Optional) Scale up

You can automate document submission so that extractions start without manual API calls. For example, add a Google Drive trigger or a Gmail attachment trigger to Scenario 1 to detect new documents automatically. For documents in Google Drive, use the **Google Drive > Download a File** module to retrieve the file bytes, then change the HTTP module to POST to `https://api.sensible.so/v0/extract/1040s` with `Content-Type: application/pdf` and the file as the request body.

# Notes

**Limitations**

* Sensible returns extracted data as structured JSON. Simple single-value fields (strings, numbers, booleans) map directly to Google Sheets cells, as shown in this tutorial. To handle complex fields such as tables and sections, use Sensible's Excel export: make a GET request to `https://api.sensible.so/v0/generate_excel/{extraction_id}` in Scenario 2 and upload the resulting file to Google Drive or another destination.
* This tutorial extracts from single-document files. To extract from portfolio files (files that contain multiple documents, for example, insurance application bundles), use the Sensible API's portfolio extraction endpoints directly.

**Document URL requirements**

* Sensible's `extract_from_url` endpoint requires the document URL to be publicly accessible without authentication. Use direct download links from public storage (for example, Amazon S3 pre-signed URLs or GitHub raw URLs). Google Drive files must be shared as **Anyone with the link can view** and use a direct download URL rather than the viewer link.
* To avoid exposing documents publicly, use Make's **HTTP > Make a Request** module to download the file bytes first, then POST to `https://api.sensible.so/v0/extract/1040s` with `Content-Type: application/pdf` and the file bytes as the request body.

**Webhook timing**

* Sensible processes extractions asynchronously. Scenario 2's webhook fires when extraction reaches `COMPLETE` status, typically within a minute for standard documents.
* Make webhook triggers stay active as long as the scenario is turned on. Turn both scenarios on together to avoid missed webhook calls.