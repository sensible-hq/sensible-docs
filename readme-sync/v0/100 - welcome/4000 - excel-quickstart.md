---
title: "Getting started with out-of-the-box extractions"
hidden: false
---

If you want to extract from any of the following document types:

- auto policy declaration pages
- balance sheets
- bank statements
- closing disclosures
- credit card statements
- driers licenses
- explanation of benefits
- loss runs
- pay stubs
- resumes
- tax forms
- ....and more

Then you can get started in minutes using the [Sensible configuration library](https://github.com/sensible-hq/sensible-configuration-library), which provides out-of-the-box support for common business forms.

In this quickstart, extract data from an example tax form PDF and convert the document data to a spreadsheet using the configuration library. 

- If you instead want a guided tour for extracting data from your own custom documents, see [Overview](doc:overview) for choosing an extraction strategy.

Copy pre-built extraction configuration
----

1. Get an account at [sensible.so](https://app.sensible.so/register).

2. Navigate to Sensible's [open-source configuration library](https://app.sensible.so/library/) to choose an example document type. For this tutorial, select **Tax forms**.

3. Select **Clone to account** to copy example tax forms and associated configurations for extracting data from those forms to your account.

Extract from sample document
----

4. Download the following example tax form: 

   | Example PDF | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf) |
   | ----------- | ------------------------------------------------------------ |

5. Navigate to the [quick extraction](https://app.sensible.so/quick-extraction/) tab.

6. Upload the document you downloaded in the previous step.

7. Select **tax_forms** in the **Document type** dropdown and click **Run extraction**.

   ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_excel_1.png)

   Sensible extracts data from the document using the pre-built config you copied in a previous step. 

(Optional) Convert to spreadsheet
----


11. Sensible displays the extracted data as JSON in the right pane. Click the **Download excel** to convert the extracted document data to Excel:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_excel_2.png)

  The following spreadsheet shows the example output. 



[block:html]
{
  "html": "<div><iframe class=\"spreadsheet\"  src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vQZEvCIXgC5QbJ5-XnV61GjyVSJsdLbLqogiS9b1HIz4T0DwbcfEDsSseHuE1sfzjliKlBWTkbm9ITI/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n<style>.spreadsheet{width:100%;height:200px}</style>"
}
[/block]

11. (**Optional**) View the document and its configuration in the Sensible app at https://app.sensible.so/editor/?d=tax_forms&c=1040_2021&g=1040_2021_sample to explore or tweak the SenseML rules for extracting data from this tax form.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_excel_3.png)



12. (**Optional**) Upload a second example document and run an extraction to see how the extracted output changes. 

   | Example PDF | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/senior_1040_2021_sample.pdf) |
   | ----------- | ------------------------------------------------------------ |


Next
----

To get started with authoring extraction configurations, or configs, for your custom documents, see [Overview](doc:overview).

