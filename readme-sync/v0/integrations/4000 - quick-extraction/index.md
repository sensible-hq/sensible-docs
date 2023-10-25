---
title: "Quick extraction"
hidden: false

---

After you've configured extractions for your [custom documents](doc:getting-started-ai) or for out-of-the-box [supported documents](doc:library-quickstart), you can upload documents to the Sensible app and download the extracted data as Excel files.

**Note:** A bulk file upload feature is coming soon.

 In this tutorial you'll learn to:

- upload documents to the Sensible app's **Quick extraction** tab
- automatically extract from the documents using pre-existing document types and configs
- download the extracted data as Excel.

Take the following steps:

1. Navigate to the [Quick Extraction](https://app.sensible.so/quick-extraction/) tab.

2. In the **Document type** dropdown in the right pane, select your document type.

   If you haven't created your own document type, select `sensible_instruct_basics / Auto select` . The `sensible_instruct_basics` document type contains interactive examples for bank statements, resumes, and contracts.  If you specify `Auto select`,  Sensible automatically detects the best-fitting extraction configuration, or "config", for the document you upload.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_11.png)

3. Click **Upload document** and select your example document. For document file formats other than PDFs, use other integration methods such as the API. Note that Sensible automatically OCRs documents for you, except in [advanced cases](doc:ocr).

​       If you don't have an example document, use the following PDF document with the `sensible_instruct_basics` document type :

| Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/bank_3.pdf) |
| ----------- | ------------------------------------------------------------ |

3. Click **Run Extraction**.

4. Sensible displays the extracted data as JSON in the right pane. Click the **Download excel** to convert the extracted document data to Excel:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_12.png)

 The following spreadsheet shows output for the example bank statement PDF. The first tab contains fields with single values, for example the start date field. Succeeding tabs contain fields with table output, for example, the accounts list table. 

[block:html]
{
  "html": "<div><iframe class=\"spreadsheet\" src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vTwZYVB1DHgb-RrlCzqAMvnE0yUausiTp4CtEVIVeVVoTLyi8rFBmSyzfiznfPrbmbFnnifXAWZZPx6/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n<style>.spreadsheet{width:100%;height:200px}</style>"
}
[/block]

**Note** Each downloaded Excel file contains the data from one document. To combine extracted documents into one Excel file, use the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction).

##  Next

For more information about how Sensible converts JSON document extractions to Excel, see [SenseML to spreadsheet reference](https://docs.sensible.so/docs/excel-reference).
