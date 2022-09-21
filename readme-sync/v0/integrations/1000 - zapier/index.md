---
title: "Zapier overview"
hidden: false

---

With Sensible's Zapier integration, you can transform data in PDFs and other documents into emails, databases, Google sheets, and other supported Zapier destinations.

For example, you can extract data in 1040 tax forms: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_6.png)

And send the data to spreadsheets, emails, databases, or other supported Zapier destinations. The following image shows data from 1040s, where each document is a record, or row, in an Airtable database: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_5.png)



Sensible trigger
---


Every time you run an extraction using the Sensible [app]((https://app.sensible.so/quick-extraction) or [API](ref:choosing-an-endpoint), you can automatically send the data to a destination, for example an email or database, using a **Sensible trigger**: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_trigger.png)

For more information, see the [Zapier getting started guide](doc:zapier-getting-started) or [example Zap](https://zapier.com/shared/cb6b2637ef466ddf140ed14c3be66a5969acef29).

Sensible action
---

You can bypass the Sensible app or API and instead trigger Sensible extractions with file actions in Google drive, email, or other supported Zapier apps. Then send the extraction to the destination of your choice with a **Sensible action**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action.png)

For more information, see an  [example Zap](https://zapier.com/shared/89bc08c43e753cae2483de6909dea250dbb47155).

**Multistep limitations**

- If you select **New file in folder**  event in Google drive folder, Zapier ignores uploaded files whose create or modified date is older than 4 days. 
- Sensible's Zapier action can't filter extraction status, so Zapier can send incomplete or failed extractions to the data destination.







