---
title: "Zapier tutorial"
hidden: true

---

This topic describes an example two-Zap workflow for Zapier:

1. Every time you receive an email in Gmail with a 1040 document attached, trigger Sensible to extract data from it and output the extraction as a spreadsheet.
2. Every time Sensible extracts a document, check that it's a 1040. If so, upload the extracted spreadsheet to a folder in Google drive.

Prerequisite: Create an example Sensible extraction
----

To configure Zapier, you'll use a recent example of a document extraction. Follow the steps in [PDF to Excel quickstart](doc:excel-quickstart) to create a JSON extraction from an example 1040 tax form. 

Prerequisite: Create a Gmail filter and Google Drive folder
----

1. Set up a Gmail filter that automatically applies the label "1040" to any email you receive that has an attached 1040 document in PDF format. For example, filter on `subject:1040`.
2. Create an empty Google Drive folder as a destination for the spreadsheets of extracted data that Sensible will create for each 1040 PDF you receive as an email.

First Zap: Extract emailed 1040 doc with Sensible
---



[block:html]
{
  "html": "<div style=\"position: relative; padding-bottom: calc(87.19723183391004% + 41px); height: 0;\"><iframe src=\"https://docs.google.com/presentation/d/e/2PACX-1vTFlT9rc8mGJVz1cCs4RJEww7u1I3X857_jikiWxwJoBJfbU-ITFe9h4U1HkVuGFQUlT44EwVmlJECP/embed?start=false&loop=false&delayms=5000\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"
}
[/block]

Second Zap: Upload extraction as spreadsheet to Google drive, if it's a 1040
---



[block:html]
{
  "html": "<div style=\"position: relative; padding-bottom: calc(87.19723183391004% + 41px); height: 0;\"><iframe src=\"https://docs.google.com/presentation/d/e/2PACX-1vTMJ5faM9JKFRzEVNym81e1PNuC0sLBi5fBLfJyj1HGIvbgCI8YbWpuPuKZWFABgBRPgun4ziZeUigX/embed?start=false&loop=false&delayms=5000\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"
}
[/block]



(Optional) Test your integration
---

Congratulations, your integration is now published and running! Take the following steps to continue populating a Google folder from example documents:

1. Navigate to the Sensible [quick extraction tab](https://app.sensible.so/quick-extraction/).
2. Upload and run extractions for the following example 1040 documents:
   - [2018 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2018)
   - [2019 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2019)
   - [2020 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2020)

3. Verify the extractions show up in your Google Drive folder as spreadsheets.


