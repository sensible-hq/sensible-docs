---
title: "Zapier overview"
hidden: false

---

With Sensible's beta Zapier integration, you can transform data in PDFs and other documents into emails, databases, Google sheets, and other supported Zapier destinations.

For example, you can extract data in 1040 tax forms: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_6.png)

And send the data to spreadsheets, emails, databases, or other supported Zapier destinations. The following image shows how Zapier can add extracted data from each document as a record, or row, in an Airtable database: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_5.png)

When creating a Zapier integration, you can either:

- Run extractions and then act on the data with a **Sensible trigger**.
- Trigger extractions automatically outside of Sensible, then act on the data with a **Sensible action**.

Sensible trigger
---


Every time you run an extraction using the Sensible [app](https://app.sensible.so/quick-extraction) or [API](ref:choosing-an-endpoint), you can automatically send the data to a destination, for example an email or database, using a **Sensible trigger**: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_trigger.png)

For more information, see the [Zapier getting started guide](doc:zapier-getting-started) or [example Zap](https://zapier.com/shared/cb6b2637ef466ddf140ed14c3be66a5969acef29).

Sensible action
---

You can bypass the Sensible app or API and instead trigger Sensible extractions with file actions in Google drive, email, or other supported Zapier apps. Then send the extraction to the destination of your choice with a **Sensible action**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action.png)

For more information, see [Advanced Zapier tutorial](zapier-tutorial-2) and two example Zaps. 

Notes
===

**General Limitations**

- You can configure single-value field output with these integrations. For multi-value output such as tables and sections, you can compile document extractions into a spreadsheet or CSV file using Sensible's API. For more information, see [SenseML to Excel reference](doc:excel-reference).
- You can extract from single-document files with Zapier. If you want to extract from portfolio PDFs (documents that contain multiple documents, for example, insurance bundles), use the Sensible API. 

**Sensible action limitations**

- If you select **New file in folder**  event in Google drive folder as the trigger for the Sensible action, Zapier ignores uploaded files whose create or modified date is older than 4 days. 
- The Sensible action can't filter extraction status, so Zapier can send incomplete or failed extractions to the data destination. To avoid this, add a Zapier delay in your Zap.
- When setting up the Sensible action, run an extraction on the same file you intend to use for your Zapier sample setup a minute or so before you start configuring the Zap in order to get sample data. Otherwise, Zapier returns an incomplete extraction during configuration.



