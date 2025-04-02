---
title: "Advanced Zapier tutorial"
hidden: true

---





LEFT OFF: OK. it seems that if i give a link to https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/blog_salesforce/blog_lease_1.pdf and say download raw file, I actually get something w/ today's create/modified date. sooooo... that could work??



This topic describes how to configure an example two-Zap workflow for Zapier. The example workflow extracts data from documents uploaded to a Slack channel and uploads them as spreadsheets to another Google Drive folder. 

Sensible supports two-step Zapier workflows as follows:

- The first Zap extracts the document and returns a `WAITING` extraction status.
- The second Zap triggers when the extraction status is `COMPLETE` and takes action on the extraction.

You can use the example Zaps in this topic as templates. For example, modify this workflow to trigger extractions based on other file actions in Zapier-support apps. Or, output to different destinations (for example, a database record instead of spreadsheet files in Google Drive).

Zap 1
---

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action_1_slack.png)





Every time you add a new file to a specified Google Drive folder, Zapier triggers Sensible to start extracting data from it.

Zap 2
---

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action_2.png)

Every time Sensible completes extracting from a document, Zapier checks if the extraction was triggered by Zap 1. If it is, Zapier triggers Sensible to create a spreadsheet of the extracted data, and uploads the spreadsheet to a folder in Google Drive.

Take the following steps to run these Zaps with example data, then modify them for your needs.

Prerequisite: Configure 1040 extractions in Sensible
----

Follow the steps in [Getting started with out-of-the-box extractions](doc:library-quickstart) to clone the `1040s`  document type to your account. 

Prerequisite: Configure accounts
----

1. Create a test Slack channel. Name it `1040s_uploads`. Upload an [example 1040 document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/templates/Tax%20Forms/1040s/refdocs/1040_2021_sample.pdf) to the channel.
2. Create an empty Google Drive folder as a destination for the spreadsheets of extracted data. Name it `1040s_extracted`.
3. (Optional) In the `1040s_extracted` folder, create a spreadsheet named `Zapier-Sensible Extractions Logs` to log each time the Zaps run. Create columns to record information about each extraction, for example, `Extraction ID` , `Extraction Date` , and `Extraction link`.

Zap 1: Extract new file in Slack with Sensible
---

See the following steps to configure Zap 1:

1. Create a new Zap.

2. For the trigger, take the following steps:
   1. Setup:
      1. **App**: Slack
      2. **Trigger event**: New File
      3. **Account**: Your Slack account.
   2. Configure:
      1. **Channel**: Select the test `1040s_uploads` channel you created in the Prerequisites steps.
      2. **User Name**: Leave unselected
      3. **Shared**: Select **True**.
   3. Test:
      1. Before you click **Test trigger**, ensure you've uploaded a 1040 document to the `1040s_uploads` Slack channel.
      2.  Select the document you uploaded.
   
3. For the action, take the following steps: 

   1. Setup:
      1. Search for and select `Sensible`.
      2. **Action event**: Extract document
      3. **Account**: Select your Sensible account.


   2. Configure:
      1. **Document type**: 1040s
      2. **Environment**: Production
      3. **Document**: `File (Exists but not shown)`.  This specifies to extract from the document uploaded to Slack.
      4. **Reference**: `File (Exists but not shown)`.  You'll use this reference to connect Zap 1 and Zap 2 in a succeeding step.
      5. (Optional): You can specify additional references to log additional information in succeeding steps.
   3. Test:
      1. Click test, then verify that the extraction is in `WAITING` status
      2. Click **Publish**.



Zap 2: Upload extraction as spreadsheet to Google drive
---

See the following steps to configure Zap 2.

1. Create a new Zap.

2. For the trigger, take the following steps:

   1. Setup:
      1. Search for and select `Sensible`.
      2. **Trigger event**: New Document Extraction
      3. **Account**: Select your Sensible account.

   2. Configure:
       	1. **Document type**: 1040s
       	2. **Environment**: Production
       	3. **Status**: Complete
       	4. **Create Excel output**: True. This creates an Excel [spreadsheet](doc:excel-reference) from the extracted document data and stores it at URL.
   3. Test:
        1. Click **Test trigger**.
        2. Select the extraction you triggered in the previous Zap. Verify its status is now `COMPLETE` and that the `parsed_document` object contains extracted data from the example document you uploaded in a previous step. For example, `Parsed Document Year Value` is `2021`.

3. For the action, take the following steps:
   1. Filter:
      1. Search for **Filter** and select Filter conditions.
      2. **Only continue if**: Webhook Payload Reference 1 (Exists but not shown)
      3. **Condition**: Exists. This ensures that you take action on the same extraction that was triggered in the previous Zap.

   2. Setup:
      1. Search for and select `Google Drive`.
      2. **Action event**: Upload file. This will upload the Excel file of extracted document data you created in the previous Zap.
      3. **Account**: Select your Google account.

   3. Configure:
      1. **Drive**: Select your Google drive
      2. **Folder**: Select the `1040s_extracted` folder you created in a previous step.
      3. **File**: Select `New Document Extraction in Sensible`, then select `Excel Output` to select the Excel file you created in a previous Zap.
      4. **Convert to Document**: True
      5. **File Name**: Choose `New Document Extraction in Sensible`,  then select `ID` to name the uploaded file after the Sensible extraction ID.

   4. Test:

      1. Click **Test Step**.

      2. Navigate to the `1040s_extracted` Google Drive folder you created in a previous step and verify it now contains a spreadsheet with extracted document data, for example:

         ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_spreadsheet.png) 

4. (Optional): To log when Zap 1 and Zap 2 run, take the following actions:

   1. Setup: 
       1. Click **Edit Zap** to edit the Zap 2.
       2. Click **Add step**
       3. Search for and select `Google Sheets`.
       4. **Event**: Create Spreadsheet Row
       5. **Account**: Select your Google account.

   2. Configure:
       1. **Drive**: Select your Google Drive.
       2. **Spreadsheet**: Select the `Zapier-Sensible Extractions Logs` spreadsheet you created in a previous step.
       3. **Worksheet**: Select the sheet in which you created column headings in a previous step.
       4. For each column heading you created, select the corresponding extraction information. For example:
           1. **extraction id**: ID
           2. **extraction date**: Completed
           3. **Extraction link**: Embed Link
           4. (Optional) Use additional references and webhook payloads to log more information from Zap 1.


(Optional) Test your integration
---

Congratulations, your integration is now published and running! Take the following steps to continue populating a Google folder from example documents:

1. Download example 1040 documents from the Sensible [library](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Tax%20Forms/1040s/refdocs).

2. Upload them to the Google Drive folder you created.

3. Zapier can take up to 15 minutes to pull data from Sensible. To avoid waiting, navigate to the **Zaps** tab in Zapier, right-click the Zap's ellipsis (...) icon and click **Run**.

4. Wait a few minutes, then verify the extractions show up in your Google Drive folder as spreadsheets:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action_3.png)

5. Verify the extractions show up in your optionally configured logs:

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action_4.png)

Notes
---

**General Limitations**

- You can configure single-value field output with the Sensible-Zapier integration. For multi-value output such as tables and sections, you can compile document extractions into a spreadsheet or CSV file using Sensible's API. For more information, see [SenseML to Excel reference](doc:excel-reference).
- You can extract from single-document files with Zapier. If you want to extract from portfolio files (documents that contain multiple documents, for example, insurance application bundles), use the Sensible app, API, or SDK. 

**Sensible action limitations**

- If you select **New file in folder**  event in Google Drive folder as the trigger for the Sensible action, Zapier ignores uploaded files whose create or modified date is older than 4 days. 
- Run an extraction on the file you intend to use for your Zapier sample setup a minute or so before you start configuring Zap 2. Otherwise, Zapier can return an incomplete example extraction.