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



Into a spreadsheet, email, database, or other supported Zapier destinations. This tutorial shows transforming the data into a database, for example:



TODO PICTURE



Create an empty destination database
----



Before you can integrate Sensible with Airtable, you need to set up a destination in Airtable for Sensible's extracted document data. This tutorial uses example data from 1040 tax forms. 

Follow the steps in [PDF to Excel quickstart](doc:excel-quickstart) to create an example extraction. You don't need to follow the last step of downloading an Excel sheet. 



Create an example Sensible extraction
----

Zapier needs access to a recent example of a document extraction so you can configure the Zapier integration. Follow steps 1-9 in [PDF to Excel quickstart](doc:excel-quickstart) to create an example extraction. 

Configure Zapier
----

Take the following steps to connect Sensible to Airtable using Zapier:

1. Sign in or create a [Zapier account](https://zapier.com/).



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











