---
title: "Quick extraction"
hidden: false

---

After you've configured extractions for your [custom documents](doc:getting-started-ai) or for out-of-the-box [supported documents](doc:excel-quickstart), you can upload documents to the Sensible app and download the extracted data as Excel files.

**Note:** A bulk file upload feature is coming soon.

 In this tutorial you'll learn to:

- upload bank statements to the Sensible app's **Quick extraction** tab
- automatically extract from the statements using a pre-existing document type and config
- download the extracted data as Excel.

Take the following steps:

1. Download the following PDF document:

| Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/bank_3.pdf) |
| ----------- | ------------------------------------------------------------ |

1. Navigate to the [Quick Extraction](https://app.sensible.so/quick-extraction/) tab.
   1. In the **Document type** dropdown in the right pane, select `sensible_instruct_basics / Auto select` . This document type, `sensible_instruct_basics`, contains interactive example configs for bank statements, resumes, and contracts.  If you specify `Auto select`,  Sensible automatically detects the best-fitting extraction configuration, or "config", for the document you upload.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_11.png)

2. Click **Upload document** and select the document you downloaded in a previous step.

3. Click **Run Extraction**.

4. Sensible displays the extracted data as JSON in the right pane. Click the **Download excel** to convert the extracted document data to Excel:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_12.png)

  The following spreadsheet shows the example output. The first tab contains fields with single values, for example the start date field, and succeeding tabs contain fields with table output, for example, the account list table. 

[block:html]
{
  "html": "<div><iframe class=\"spreadsheet\" src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vTwZYVB1DHgb-RrlCzqAMvnE0yUausiTp4CtEVIVeVVoTLyi8rFBmSyzfiznfPrbmbFnnifXAWZZPx6/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n<style>.spreadsheet{width:100%;height:200px}</style>"
}
[/block]

**Note** Each downloaded Excel file contains the data from one document. To combine extracted documents into one Excel file, use the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction).

##  Next

- For more information about how Sensible converts JSON document extractions to Excel, see [SenseML to spreadsheet reference](https://docs.sensible.so/docs/excel-reference).
