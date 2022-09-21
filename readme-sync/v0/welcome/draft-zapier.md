---
title: "Zapier to airtable integration tutorial"
hidden: true

---

Send your document data to a variety of destinations using Sensible's Zapier integration. This topic describes getting data from an example document into the Airtable database from Sensible using Zapier. 



TODO:

- so it's easy to COPY base so I'm set there. 

- copying a zap isn't as pre-configured as I'd like??  https://zapier.com/shared/sensible-to-airtable/b328ec83630c9ad8bc1e7f5db237def212ba204b  ... TODO: YES do senseml_basics, maybe the B&B menu since json tables don't translate well?? or even just hello_world.



Introduction
----

With Sensible's Zapier integration, you can transform data in PDFs and other documents, for example the adjusted gross income numbers in 1040 tax forms: 



Into a spreadsheet, email, database, or other supported Zapier destinations. This tutorial shows transforming 1040 tax data into a database, for example:



TODO PICTURE



Create an empty destination database
----



Before you can integrate Sensible with Airtable, you need to set up a destination in Airtable for Sensible's extracted document data. Take the following steps:

1. Sign in or create an [Airtable account](https://airtable.com/).
2. Navigate to the [Sensible test base](https://airtable.com/shrJOFW1mdUdaSMiV/tblpjJbsekvE6wEwr/viw4FaqsAD3uXBAmh?blocks=hide ), and click **Copy base**.  

The example base contains a record, or column, for each piece of document data to extract.  Zapier adds a row for each new document you extract from.

Create an example Sensible extraction
----

To configure Zapier, you'll use a recent example of a document extraction. Follow the steps in [PDF to Excel quickstart](doc:excel-quickstart) to create an example JSON extraction.

Configure Zapier
----

Take the following steps to connect Sensible to Airtable using Zapier:

1. Sign in or create a [Zapier account](https://zapier.com/).
2. Navigate to the [Sensible example Zap](https://zapier.com/shared/sensible-to-airtable/b328ec83630c9ad8bc1e7f5db237def212ba204b), and click **Try this Zap**.
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

8. Follow the prompts to test the action. You should see the extracted data from the [1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf) as a row in Airtable:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_4.png)

9. Follow the prompts to publish your Zap. 

(Optional) Add more document data to Airtable 
---

Congratulations, your integration is up and running! Take the following steps to continue building a database from your documents:

1. Navigate to the Sensible [quick extraction tab](https://app.sensible.so/quick-extraction/).
2. Upload and run extractions for the following example 1040 documents:
   - [2018 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2018/1040_2018_sample.pdf)
   - [2019 1040 example document](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2019/1040_2019_sample.pdf)


3. Verify the extractions show up in Airtable. You may have to wait up to 15 minutes. To avoid waiting, manually run the Zap in the Zap list.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/zapier_5.png)




TODO DELETE:

Click **Create Zap**. In the search bar, type **Sensible** and select the Sensible app:

![image-20220815102814832](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815102814832.png)

In the **Event** dropdown, select the **New Document Extraction** trigger.

![image-20220815102933162](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815102933162.png)



Follow the prompts to select your Sensible account, and enter your API key from your [dashboard] TODO LINK to connect your Sensible account to your Zapier account

TODO screenshot.



Select **Test trigger** (TODO: will nahual fix the 'reduce scope to specified doc type?'). Select the recent extraction that used the `zpaier_test` config you created in the **Prerequisites** section. If you can't find it, re-extract using the quick extraction pane and wait for Zapier to pull in the extraction (this make take a few minutes). Click  **Continue**.

![image-20220815104719300](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815104719300.png)



In the Action dropdown, select **Airtable**. In the **Event** dropdown, select **Create new record**. Click **Continue**

![image-20220815104925851](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815104925851.png)

Follow the prompts to connect your Zapier and Airtable accounts.

In the **Set up action** pane:

- Select your **Sensible test** base.
- Select your **Anyco auto insurance quote** table.
- For the columns you created, select the corresponding extracted value. For example, for the `driver_name` column, select the `name_insured` extracted field. Zapier displays test values from the recent extraction.  ![image-20220815105309097](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815105309097.png)
- When complete, the **Set up action** pane looks like the following image:
- ![image-20220815105523183](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815105523183.png)

Click **test and continue**, then check in airtable that the record was created. This may take a few minutes:











