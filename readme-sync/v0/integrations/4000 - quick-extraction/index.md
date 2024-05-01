---
title: "Quick extraction"
hidden: false

---

After you've configured extractions for your [custom documents](doc:getting-started-ai) or for out-of-the-box [supported documents](doc:library-quickstart), you can upload documents to the Sensible app in bulk and download the extracted data as Excel files.

 In this tutorial you'll learn to:

- upload documents to the Sensible app's **Extract** tab
- automatically extract from the documents using pre-existing document types and configs
- download the extracted data as Excel.

## Extract from a file

Take the following steps:

1. Navigate to the [Extract](https://app.sensible.so/quick-extraction/) tab.

2. Select **Document** for single-document files or **Portfolio** for [documents bundled into a single file](doc:portfolio).

3. In the **Document type** dropdown in the right pane, select the category that describes your document, for example, `resumes` or `tax_forms`. For portfolios, select multiple types.

   If you haven't created your own document type, select `sensible_instruct_basics / Auto select` . The `sensible_instruct_basics` document type contains interactive examples for bank statements, resumes, and contracts.  If you specify `Auto select`,  Sensible automatically detects the best-fitting extraction configuration, or "config", for the document you upload.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_11.png)

3. Click **Upload document** and select your example document or documents. For a list of supported file types, see [Supported file types](doc:file-types). Note that Sensible automatically OCRs documents as needed, except in [advanced cases](doc:ocr-preprocessor).

​       If you don't have an example document, use the following document with the `sensible_instruct_basics` document type :

| Example document | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/bank_3.pdf) |
| ----------- | ------------------------------------------------------------ |

3. Click **Run Extraction**.

4. Sensible displays the extracted data as JSON in the right pane. Click **Download excel** to convert the extracted document data to Excel:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_12.png)

 The following spreadsheet shows output for the example bank statement. The first tab contains fields with single values, for example the start date field. Succeeding tabs contain fields with table output, for example, the accounts list table. 

[block:html]
{
  "html": "<div><iframe class=\"spreadsheet\" src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vTwZYVB1DHgb-RrlCzqAMvnE0yUausiTp4CtEVIVeVVoTLyi8rFBmSyzfiznfPrbmbFnnifXAWZZPx6/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n<style>.spreadsheet{width:100%;height:200px}</style>"
}
[/block]

**Note** Each downloaded Excel file contains the data from one document. To combine extracted documents into one Excel file, use the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction) or [Sensible SDKs](doc:sdk-guides).

## Extract from multiple files

To extract from multiple files in a batch, select and upload multiple files in step 3 in the preceding section:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quick_extract_bulk.png)

##  Next

For more information about how Sensible converts JSON document extractions to Excel, see [SenseML to spreadsheet reference](https://docs.sensible.so/docs/excel-reference).
