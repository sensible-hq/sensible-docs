---
title: "Quick extract"
hidden: false

---



The following tutorial shows you how to use "quick extract" to upload documents for extraction to Sensible.

**Note:** Bulk uploads are coming soon.

# Quick extractions

Let's use example documents to show how to quickly extract data.

**Coming soon:** Bulk upload for quick extractions

 In this tutorial you'll learn to:

- upload new bank statements to the Sensible app
- automatically extract from them using the config
- download the extracted data as Excel.

Take the following steps:

1. Download the following PDF document:

| Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/bank_3.pdf) |
| ----------- | ------------------------------------------------------------ |

1. Navigate to the [Quick Extraction](https://app.sensible.so/quick-extraction/) tab.
   1. In the dropdown in the right pane, select `sensible_instruct_basics / Auto select` . The document type, `sensible_instruct_basics`, contains configs for bank statements and other document types such as resumes and contracts.  When you specify `Auto select`,  Sensible automatically chooses the bank config when you upload a bank statement.

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

**NOTE:** Bulk upload for documents is coming soon. TO DO WORD BETTER

##  Next

- For more information about how Sensible converts JSON document extractions to Excel, see [SenseML to spreadsheet reference](https://docs.sensible.so/docs/excel-reference).
