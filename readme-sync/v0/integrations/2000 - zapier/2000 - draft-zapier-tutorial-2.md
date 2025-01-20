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

Every time you receive an email in Gmail with a 1040 document attached, Zapier triggers Sensible to extract data from it.

Zap 2
---

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action_2.png)

Every time Sensible extracts a document, Zapier checks that it's a 1040 document. If so, Zapier triggers Sensible to create a spreadsheet of the extracted data, and uploads the spreadsheet to a folder in Google drive.

Take the following steps to run these Zaps with example data, then modify them for your needs.

Prerequisite: Configure 1040 extractions in Sensible
----

Follow the steps in [Getting started with out-of-the-box extractions](doc:library-quickstart) to clone the `1040s`  document type to your account. 

Prerequisite: Configure Google accounts
----

1. Choose a Gmail account for the Zaps. Send a test email to it with an [example 1040 document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/templates/Tax%20Forms/1040s/refdocs/1040_2021_sample.pdf)  attached and make sure the subject line includes the text `1040`.
2. Create an empty Google Drive folder as a destination for the spreadsheets of extracted data. Name it `1040s_extracted`.
3. (Optional) In the Google Drive folder, create a spreadsheet named `Zapier-Sensible Extractions Logs` to log each time the Zaps run. Create columns to record information about each extraction, for example, `Extraction ID` , `Extraction Date` , `Email link`, and `Extraction link`.

Zap 1: Extract emailed 1040 doc with Sensible
---

See the following steps to configure Zap 1:

1. Create a new Zap.

2. For the trigger, take the following steps:
   1. Setup:
      1. **App**: Gmail
      2. **Trigger event**: New Attachment
      3. **Account**: Your Google account.
   2. Configure:
      1. **Label or mailbox**: Inbox and all labels
      2. **Search keywords**: `subject:1040` (This triggers on each attachment if the email's subject contains "1040")
   3. Test:
      1. Before you click **Test trigger**, send an email to yourself with an attached 1040 document and the subject "1040".
      2.  Select the email attachment you sent.

3. For the action, take the following steps: 

   1. Setup:
      1. Search for and select `Sensible`.
      2. **Action event**: Extract document
      3. **Account**: Select your Sensible account.


   2. Configure:
      1. **Document type**: 1040s
      2. **Environment**: Production
      3. **Document**: `Attachment (Exists but not shown)`.  This specify to extract from the email attachment.
      4. **Reference**: `Attachment (Exists but not shown)`. If you were working in Google Drive, you'd input "File".
   3. Test:
      1. Click test, then verify that the extraction is in `WAITING` status
      2. Click **Publish**.



Zap 2: Upload extraction as spreadsheet to Google drive, if it's a 1040
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
       	4. **Create Excel output**: True. This creates an Excel [spreadsheet](doc:excel-reference) from the extracted document data.
   	3. Test:
       	1. Click **Test trigger**.
                	1. Select the extraction you triggered in the previous Zap. Verify its status is now `COMPLETE` and that the `parsed_document` object contains extracted data from the example document you emailed in a previous step. For example, `Parsed Document Year Value` is `2021`.

3. For the action, take the following steps:
   1. Filter:
      1. Search for **Filter** and select Filter conditions.
      2. **Only continue if**: Webhook Payload Reference 1
      3. **Condition**: Exists. This ensures that you take action on the same extraction that was created in the previous Zap.

   2. Setup:
      1. Search for and select `Google Drive`.
      2. **Action event**: Upload file. This will upload the Excel file of extracted document data you created in the previous Zap.
      3. **Account**: Select your Google account.

   3. Configure:
      1. **Drive**: Select your Google drive
      2. **Folder**: Select the `1040s_extracted` folder you created in a previous step.
      3. **File**: Select `New Document Extraction in Sensible`, then select `Excel Output` to select the Excel file you created in a previous Zap, which Sensible outputs to a URL.
      4. **Convert to Document**: True
      5. **File Name**: Choose `New Document Extraction in Sensible`,  then select `ID` to name the uploaded file after the Sensible extraction ID.

   4. Test:

      1. Click **Test Step**.

      2. Navigate to the `1040s_extracted` Google Drive folder you created in a previous step and verify it now contains a spreadsheet with extracted document data, for example:

         ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_spreadsheet.png) 

4. (Optional): Log zapier actions

    To log when Zap 1 and Zap 2 run, take the following actions:   

    1. Setup:

       	1. Click **Edit Zap** to edit the Zap 2.

       1. Click **Add step**

       1. Search for and select `Google Sheets`.

   1. 

(Optional) Test your integration
---

Congratulations, your integration is now published and running! Take the following steps to continue populating a Google folder from example documents:

1. Download example 1040 documents from the Sensible [library](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Tax%20Forms/1040s/refdocs).

2. Email the example 1040 documents to the Gmail account, ensuring that they match the search criteria you created in Zapier:

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

- If you select **New file in folder**  event in Google drive folder as the trigger for the Sensible action, Zapier ignores uploaded files whose create or modified date is older than 4 days. 
- When setting up the Sensible action, run an extraction on the same file you intend to use for your Zapier sample setup a minute or so before you start configuring the Zap in order to get sample data. Otherwise, Zapier returns an incomplete extraction during configuration.