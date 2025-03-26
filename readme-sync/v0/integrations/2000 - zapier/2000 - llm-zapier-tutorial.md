---
title: "Advanced Zapier tutorial"
hidden: true
---

This topic describes how to configure an example two-Zap workflow for Zapier. The example workflow extracts data from emailed documents and uploads them as spreadsheets to Google Drive. 

Sensible supports two-step Zapier workflows as follows:

- The first Zap extracts the document and returns a `WAITING` extraction status.
- The second Zap triggers when the extraction status is `COMPLETE` and takes action on the extraction.

You can use the example Zaps in this topic as templates. For example, modify this workflow to trigger extractions based on other file actions in Zapier-support apps (for example, a new document uploaded to Google Drive instead of a new email in Gmail). Or, output to different destinations (for example, a database record instead of spreadsheet files in Google Drive).

Zap 1
---

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action_1.png)

Every time a new file is added to a specific Google Drive folder, Zapier triggers Sensible to start extracting data from it.

Zap 2
---

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action_2.png)

Every time Sensible completes extracting from a document, Zapier checks if the extraction was triggered by Zap 1. If it is, Zapier triggers Sensible to create a spreadsheet of the extracted data, and uploads the spreadsheet to a folder in Google Drive.

Take the following steps to run these Zaps with example data, then modify them for your needs.

Prerequisite: Configure 1040 extractions in Sensible
----

Follow the steps in [Getting started with out-of-the-box extractions](doc:library-quickstart) to clone the `1040s` document type to your account. 

Prerequisite: Configure Google accounts
----

1. Choose a Google Drive account for the Zaps. 
2. Create an empty Google Drive folder as a destination for the uploaded 1040 documents. Name it `1040s_uploads`.
3. Create another empty Google Drive folder as a destination for the spreadsheets of extracted data. Name it `1040s_extracted`.
4. (Optional) In the `1040s_extracted` Google Drive folder, create a spreadsheet named `Zapier-Sensible Extractions Logs` to log each time the Zaps run. Create columns to record information about each extraction, for example, `Extraction ID`, `Extraction Date`, and `Extraction link`.

Zap 1: Extract new file in Google Drive with Sensible
---

See the following steps to configure Zap 1:

1. Create a new Zap.

2. For the trigger, take the following steps:
   1. Setup:
      1. **App**: Google Drive
      2. **Trigger event**: New File in Folder
      3. **Account**: Your Google account.
   2. Configure:
      1. **Drive**: Select your Google Drive.
      2. **Folder**: Select the `1040s_uploads` folder you created.
   3. Test:
      1. Before you click **Test trigger**, ensure you've uploaded a 1040 document to the `1040s_uploads` folder.

3. For the action, take the following steps: 

   1. Setup:
      1. Search for and select `Sensible`.
      2. **Action event**: Extract document.
      3. **Account**: Select your Sensible account.

   2. Configure:
      1. **Document type**: 1040s
      2. **Environment**: Production
      3. **Document**: `File (Exists but not shown)`. This specifies to extract from the uploaded file.
      4. **Reference**: `File (Exists but not shown)`. You'll use this reference to connect Zap 1 and Zap 2 in a succeeding step.
   3. Test:
      1. Click test, then verify that the extraction is in `WAITING` status.
      2. Click **Publish**.

Zap 2: Upload extraction as spreadsheet to Google Drive
---

See the following steps to configure Zap 2.

1. Create a new Zap.

2. For the trigger, take the following steps:

   1. Setup:
      1. Search for and select `Sensible`.
      2. **Trigger event**: New Document Extraction.
      3. **Account**: Select your Sensible account.

   2. Configure:
      1. **Document type**: 1040s
      2. **Environment**: Production
      3. **Status**: Complete
      4. **Create Excel output**: True. This creates an Excel [spreadsheet](doc:excel-reference) from the extracted document data and stores it at a URL.

   3. Test:
      1. Click **Test trigger** and verify the extracted data.

3. For the action, take the following steps:
   1. Filter:
      1. Search for **Filter** and select Filter conditions.
      2. **Only continue if**: Webhook Payload Reference 1
      3. **Condition**: Exists.

   2. Setup:
      1. Search for and select `Google Drive`.
      2. **Action event**: Upload file.
      3. **Account**: Select your Google account.

   3. Configure:
      1. **Drive**: Select your Google Drive.
      2. **Folder**: Select the `1040s_extracted` folder.
      3. **File**: Select `New Document Extraction in Sensible`, then select `Excel Output`.
      4. **Convert to Document**: True.
      5. **File Name**: Choose `New Document Extraction in Sensible`, then select `ID`.

   4. Test:
      1. Click **Test Step**.
      2. Navigate to the `1040s_extracted` folder and verify it now contains a spreadsheet.

(Optional) Test your integration
---

Congratulations, your integration is now published and running! Take the following steps:

1. Upload example 1040 documents to the `1040s_uploads` folder.
2. Zapier can take up to 15 minutes to pull data from Sensible. To avoid waiting, manually run the Zaps.
3. Verify the extracted spreadsheets appear in your `1040s_extracted` Google Drive folder.

Notes
---

**General Limitations**

- You can configure single-value field output with the Sensible-Zapier integration. For multi-value output such as tables and sections, use Sensible’s API.
- You can extract from single-document files with Zapier. For portfolio files (documents containing multiple documents), use Sensible’s API or SDK.

**Sensible action limitations**

- If you select **New File in Folder** in Google Drive as the trigger, Zapier ignores uploaded files whose creation or modified date is older than 4 days.
- Run an extraction on the file you intend to use for your Zapier sample setup a minute or so before configuring Zap 2. Otherwise, Zapier can return an incomplete example extraction.
