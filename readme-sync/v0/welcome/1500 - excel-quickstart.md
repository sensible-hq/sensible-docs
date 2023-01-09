---
title: "Quickstart PDF to Excel"
hidden: false
---

In this quickstart, extract data from an example tax form PDF and convert the document data to a spreadsheet with no coding involved.

- If you instead want a guided tour of SenseML concepts so you extract data from your own custom documents, see [Getting started](doc:getting-started).

Introduction
----

If you're trying to convert a PDF into an Excel spreadsheet, you'll often find tools that visually map the PDF layout onto a spreadsheet, with no meaningful relationship between the extracted text and the underlying cells. 

In contrast, this tutorial shows you how to use Sensible to convert document tables, checkboxes, paragraphs, and even complex repeating section layouts into meaningfully labeled column/row pairs and linked sheets. You can convert documents formatted as PDFs, PNGs, TIFFs, and JPEGs.

Extract sample document data
----

1. Get an account at [sensible.so](https://app.sensible.so/register).
2. Navigate to Sensible's [open-source configuration library](https://app.sensible.so/library/) to choose an example document type. For this tutorial, select **Tax forms**.
3. Select **Clone to account** to copy example tax forms and associated configurations for extracting data from those forms to your account.

7. Download the following example tax form: 

   | Example PDF | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf) |
   | ----------- | ------------------------------------------------------------ |

8. Navigate to the [quick extraction](https://app.sensible.so/library/) tab.

9. Upload the document you downloaded in the previous step.

7. Select **tax_forms** in the **Document type** dropdown and click **Run extraction**.

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_excel_1.png)

   Sensible extracts data from the document and displays it as JSON in the **Extraction** pane. 

Convert to spreadsheet
----


11. Select **Download Excel** to convert the extracted document data to Excel.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_excel_2.png)

  The following spreadsheet shows the example output:



[block:html]
{
  "html": "<div><iframe class=\"spreadsheet\" src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vQZEvCIXgC5QbJ5-XnV61GjyVSJsdLbLqogiS9b1HIz4T0DwbcfEDsSseHuE1sfzjliKlBWTkbm9ITI/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n<style>.spreadsheet{width:100%;height:200px}</style>"
}
[/block]

11. (**Optional**) View the document and its configuration in the Sensible app at https://app.sensible.so/editor/?d=tax_forms&c=1040_2021&g=1040_2021_sample to explore or tweak the SenseML rules for extracting data from this tax form.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_excel_3.png)



Compile PDFs into one spreadsheet
----

To combine multiple PDFs  into one multi-document spreadsheet, use the [Sensible API](https://docs.sensible.so/reference/get-excel-extraction).


Next
----

- For more information about how Sensible converts JSON document extractions to Excel and combines multiple documents into one spreadsheet, see [SenseML to spreadsheet reference](doc:excel-reference).
- See the [Getting started guide](doc:getting-started) to learn how to extract from your custom documents or tweak Sensible's [open-source configuration library](https://app.sensible.so/library/).





