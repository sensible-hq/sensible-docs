---
title: "Zapier tutorial"
hidden: false

---

This topic describes sending extracted data from example documents into an Airtable database using Sensible's Zapier integration. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_0.png)

Create an example Sensible extraction
----

To configure Zapier, you'll use a recent example of a document extraction. Follow the steps in [Getting started with out-of-the-box extractions](doc:library-quickstart) to create a JSON extraction from an example 1040 tax form. 

**Note** Ensure your example extraction contains non-null values for all fields you intend to configure in Zapier.

Create an empty destination database
----

Before you can integrate Sensible with Airtable, you need to set up a destination in Airtable to hold the extracted data Sensible creates. Take the following steps:

1. Sign in or create an [Airtable account](https://airtable.com/).
2. Create a destination Airtable base using the following image as a guide, with **extraction id**, **adjusted gross income**, and **taxpayer name**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_7.png)

The base contains a field (displayed as a column), for each piece of document data to extract.  Zapier adds a record (displayed as a row), for each new document you extract from.

3. (Optional) examine the [example extraction](https://app.sensible.so/quick-extraction/) you created in the previous section. To add more data from the extraction, create corresponding Airtable fields. For example, create a `Total taxes owed` field.

Configure Zapier
----

Take the following steps to connect Sensible to Airtable using Zapier:

1. Sign in or create a [Zapier account](https://zapier.com/).

2. Create a new Zap. For your trigger, search for and select **Sensible**.

3. Take the following steps to connect your Sensible account to Zapier:
   1. Click to expand the **Trigger** section.
   2. Click to expand the **Choose account** section, then follow the prompts to connect your Sensible account.

4. In the **Set up trigger** section:

   1. Select the **tax_forms** document type you created in the previous steps.

   2. Select the **Production** environment.

   3. Select the **Complete** status. 

   4. Leave the default for the **Create Excel output** option. 

      **Note:** that if you select true for this option, you can access the extracted document data [converted](doc:excel-reference) to an Excel file in succeeding Zapier actions. For an example of using this option, see [Advanced Zapier tutorial](doc:zapier-tutorial-2).


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_1.png)

5. Continue to the **Test trigger** section and follow the prompts to test. Verify that the recent document extraction you created in previous steps is selected:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_2.png)

6. Continue to the **Action** section, search for and select **Airtable**:
   1. For the **Event**, choose **Create records (With Line Item Support)** 
   2. Follow the prompts to connect your Airtable account to Zapier. 

7. In the **Set up action** section, map Sensible extracted field ids to the corresponding Airtable field names. Zapier displays the data from the recent document extraction as examples. Use the following screenshot to complete the configuration:

 ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_3.png)

8. (Optional) If you created extra fields in the database, map each one.

9. Follow the prompts to test the action. You should see the extracted data from the [1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf) as a row in Airtable:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_4.png)

9. Follow the prompts to publish your Zap. 

(Optional) Test your integration
---

Congratulations, your integration is now published and running! Take the following steps to continue building a database from example documents:

1. Navigate to the Sensible [Extract tab](https://app.sensible.so/quick-extraction/).
2. Upload and run extractions for the following example 1040 documents:
   - [2018 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2018)
   - [2019 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2019)
   - [2020 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040/2020)

3. Zapier can take up to 15 minutes to pull data from Sensible. To avoid waiting, navigate to the **Zaps** tab in Zapier, right-click the Zap's ellipsis (...) icon and click **Run**.

4. Verify the extractions show up in Airtable: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_5.png)



(Optional) Scale up
---

You can extract from more documents automatically by building a more complex Zap so that you can trigger Sensible extractions with file actions in Google drive, email, or other supported Zapier apps.
Then send the extraction to the destination of your choice with a Sensible action.  For more information, see [Advanced Zapier tutorial](doc:zapier-tutorial-2).![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_action.png)



Notes
===

**Limitations**

- By default, you can configure single-value field output with the Sensible-Zapier integration. To handle multi-value output such as tables and sections in Zapier, you can first compile document extractions into a spreadsheet or CSV file using the Create Spreadsheet Row in Zapier's Google Sheets integrations. For more information about Sensible's Excel exports, see [SenseML to Excel reference](doc:excel-reference).
- You can extract from single-document files with Zapier. If you want to extract from portfolio files (files that contain multiple documents, for example, insurance application bundles), use the Sensible API or SDKs. 







