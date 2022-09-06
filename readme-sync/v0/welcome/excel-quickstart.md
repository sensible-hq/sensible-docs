---
title: "PDF to Excel quickstart"
hidden: true
---



If you're trying to convert a PDF into an Excel spreadsheet, you'll often find tools that simply visually map the PDF layout onto a spreadsheet, with no meaningful relationship between the extracted text and the underlying cells. In contrast, Sensible structures document data into meaningfully labeled column/row pairs and linked sheets, so you can convert document tables, checkboxes, paragraphs, and even complex repeating section layouts into spreadsheets.

In this quickstart, convert an example tax form to a spreadsheet using an existing SenseML configuration. 

Convert document data to Excel spreadsheet
----

1. Get an account at [sensible.so](https://app.sensible.so/register).

2. Navigate to Sensible's [open-source configuration library](https://app.sensible.so/library/) to choose an example document type. For this quickstart, select **Tax forms**.

3. Select **Clone to account** to copy example tax forms and associated configurations for extracting data from those forms to your account.

4. Navigate to the [quick extraction](https://app.sensible.so/library/) tab.

5. Select **tax_forms / Auto select** from the dropdown in the upper left corner:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/excel_quickstart_1.png)

7. Download the following example tax form. 

   | Example PDF | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf) |
   | ----------- | ------------------------------------------------------------ |

8. Select **Upload Document** and upload the document you downloaded in the previous step.

9. Sensible extracts data from the document and displays it as JSON in the **Extraction** pane. Select **Download Excel** to view the document data converted to Excel.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/excel_quickstart_2.png)

  The following spreadsheet shows the example output:

[block:html]
{
  "html": "<div><iframe src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vQZEvCIXgC5QbJ5-XnV61GjyVSJsdLbLqogiS9b1HIz4T0DwbcfEDsSseHuE1sfzjliKlBWTkbm9ITI/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n\n<style></style>"
}
[/block]



11. (**Optional**) View the document and its configuration in the Sensible app at https://app.sensible.so/editor/?d=tax_forms&c=1040_2021&g=1040_2021_sample to explore or tweak the SenseML rules for extracting data from this tax form.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/excel_quickstart_3.png)

Next
----

- For more information about how Sensible converts JSON document extractions to Excel, see [SenseML to spreadsheet reference](doc:excel-reference).
- See the [Getting started guide](doc:getting-started) to learn how to extract from your custom documents or tweak Sensible's [open-source configuration library](https://app.sensible.so/library/).





