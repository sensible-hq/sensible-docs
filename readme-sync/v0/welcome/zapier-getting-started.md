---
title: "Zapier to Airtable tutorial"
hidden: true

---

This topic describes sending data from example documents into an Airtable database from Sensible using Zapier. 

Create an example Sensible extraction
----

To configure Zapier, you'll use a recent example of a document extraction. Follow the steps in [PDF to Excel quickstart](doc:excel-quickstart) to create an example JSON extraction.

Create an empty destination database
----

Before you can integrate Sensible with Airtable, you need to set up a destination in Airtable for the extracted data Sensible creates. Take the following steps:

1. Sign in or create an [Airtable account](https://airtable.com/).
2. Navigate to the example [Sensible test base](https://airtable.com/shrJOFW1mdUdaSMiV/tblpjJbsekvE6wEwr/viw4FaqsAD3uXBAmh?blocks=hide ), and click **Copy base**.  

The example base contains a field, or column, for each piece of document data to extract.  Zapier adds a row for each new document you extract from.

3. (Optional) examine the example extraction you created in the previous step. To add more data from the extraction to Airtable, create corresponding columns. For example, create a `Total taxes owed` column.

Configure Zapier
----

Take the following steps to connect Sensible to Airtable using Zapier:

1. Sign in or create a [Zapier account](https://zapier.com/).
2. Navigate to the [Sensible example Zap](https://zapier.com/shared/cb6b2637ef466ddf140ed14c3be66a5969acef29), and click **Try this Zap**.
3. Take the following steps to connect your Sensible account to Zapier:
   1. Click to expand the **Trigger** section.
   2. Click to expand the **Choose account** section, then follow the prompts to enter your Sensible [API key](https://app.sensible.so/account/).
4. In the **Set up trigger** section, select the **tax_forms** document type you created in the previous steps, select the **Production** environment, and select the **Complete** status. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_1.png)

5. Continue to the **Test trigger** section and follow the prompts to test. Verify that the recent document extraction you created in previous steps is selected:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_2.png)

6. Continue to the **Action** section and follow the prompts to connect your **Airtable** account to Zapier.
7. In the **Set up action** section, map Sensible field names to the corresponding Airtable record names. Zapier displays the data from the recent document extraction as examples. Use the following screenshot to complete the configuration:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_3.png)

8. (Optional) If you created extra columns in the database, map each one.

9. Follow the prompts to test the action. You should see the extracted data from the [1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf) as a row in Airtable:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_4.png)

9. Follow the prompts to publish your Zap. 

(Optional) Add more document data to Airtable 
---

Congratulations, your integration is up and running! Take the following steps to continue building a database from example documents:

1. Navigate to the Sensible [quick extraction tab](https://app.sensible.so/quick-extraction/).
2. Upload and run extractions for the following example 1040 documents:
   - [2018 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2018/1040_2018_sample.pdf)
   - [2019 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2019/1040_2019_sample.pdf)
   - [2020 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2019/1040_2020_sample.pdf)

3. Verify the extractions show up in Airtable: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_5.png)

Zapier polls Sensible every 1-15 minutes. To avoid waiting, manually run the Zap in the Zap list.











