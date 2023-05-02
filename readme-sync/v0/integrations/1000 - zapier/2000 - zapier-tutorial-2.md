---
title: "Advanced Zapier tutorial"
hidden: true

---

TODOO ON PUBLISH:



- publish the zaps  https://zapier.com/app/zaps/folder/1370975 and update links to them! 
- notes about mult-file extractions
- add overview screenshots to slides and to the docs





This topic describes an example two-Zap workflow for Zapier:

1. Zap 1: Every time you receive an email in Gmail with a 1040 document attached, Zapier triggers Sensible to 1. extract data from it and 2. output the extraction as a spreadsheet.
2. Zap 2: Every time Sensible extracts a document, Zapier checks that it's a 1040. If so, Zapier uploads the spreadsheet of the extracted data to a folder in Google drive.

Prerequisite: Configure 1040 extractions in Sensible
----

Follow the steps in [Getting started with out-of-the-box extractions](doc:excel-quickstart) to configure extracting data from a 1040 tax form. 

Prerequisite: Configure Google accounts
----

1. Choose a Gmail account for the Zaps. Send a test email to it with an [example 1040](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf)  attached and make sure the subject line includes the text `1040`.
2. Create an empty Google Drive folder as a destination for the spreadsheets of extracted data that Sensible will create for each 1040 PDF you receive as an email.
3. (Optional) In the Google Drive folder, create a spreadsheet named `Zapier-Sensible Extractions`. Create columns to record information about each extraction, for example, `Extraction ID` , `Extraction Date` , `Email subject`, and `Extraction link`.

First Zap: Extract emailed 1040 doc with Sensible
---



[block:html]
{
  "html": "<div style=\"position: relative; padding-bottom: calc(87.19723183391004% + 10px); height: 0;\"><iframe src=\"https://docs.google.com/presentation/d/e/2PACX-1vTFlT9rc8mGJVz1cCs4RJEww7u1I3X857_jikiWxwJoBJfbU-ITFe9h4U1HkVuGFQUlT44EwVmlJECP/embed?start=false&loop=false&delayms=5000\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"
}
[/block]

Second Zap: Upload extraction as spreadsheet to Google drive, if it's a 1040
---



[block:html]
{
  "html": "<div style=\"position: relative; padding-bottom: calc(87.19723183391004% + 10px); height: 0;\"><iframe src=\"https://docs.google.com/presentation/d/e/2PACX-1vTMJ5faM9JKFRzEVNym81e1PNuC0sLBi5fBLfJyj1HGIvbgCI8YbWpuPuKZWFABgBRPgun4ziZeUigX/embed?start=false&loop=false&delayms=5000\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"
}
[/block]



(Optional) Test your integration
---

Congratulations, your integration is now published and running! Take the following steps to continue populating a Google folder from example documents:

1. Email the following example 1040 documents to the Gmail account, ensuring that they match the search criteria you created in Zapier:
   - [2018 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2018)
   - [2019 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2019)
   - [2020 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2020)

2. Verify the extractions show up in your Google Drive folder as spreadsheets.

Notes
---

To combine the output of multiple extractions into a single spreadsheet, use 