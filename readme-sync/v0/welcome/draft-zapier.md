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







Prerequisites
===



Create an empty destination database
----

Before you can integrate Sensible with Airtable, you need to set up a destination in Airtable for Sensible's extracted document data. This tutorial uses example data from 1040 tax forms. Take the following steps:

1. Sign in or create an [Airtable account](https://airtable.com/).
2. In the [Sensible test base](https://airtable.com/shrJOFW1mdUdaSMiV/tblpjJbsekvE6wEwr/viw4FaqsAD3uXBAmh?blocks=hide ), click **Copy base**. 

 The example base contains a record, or column, for each piece of document data to extract. When you extract from a document, Zapier adds a row that document.

Configure Sensible extraction
----

This tutorial uses open-source [SenseML configurations](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms/1040) for 1040 tax forms. To copy the configurations into your Sensible account:

1. 



 let's extract the following pieces of information available in that configuration: 

- tax year (`year`)

- taxpayer name (`name`)

- taxable income ()`taxable_income`)

- overpaid amout (`overpaid_amount`)

- total tax owed (`total_tax`)

  

Create a table named **Anyco auto insrance quote** and create columns in the table that correspond to the previously listed values. **Optional**: Right-click a column heading to edit its type, for example, currency, date, or string. 

![image-20220815102002800](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815102002800.png)

Create a test Sensible extraction
----

In Zapier, you need access to a recent document extraction as an example for configuring the integration. Take the following steps to create an extraction:

1. Get an account at [sensible.so](https://app.sensible.so/register).

2. Navigate to Sensible's [open-source configuration library](https://app.sensible.so/library/) to choose an example document type. For this tutorial, select **Tax forms**.

3. Select **Clone to account** to copy example tax forms and associated configurations for extracting data from those forms to your account.

4. Navigate to the [quick extraction](https://app.sensible.so/library/) tab.

5. Select **tax_forms / Auto select** from the dropdown in the upper left corner:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_excel_1.png)

7. Download the following example tax form. 

   | Example PDF | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/tax_forms/1040/2021/1040_2021_sample.pdf) |
   | ----------- | ------------------------------------------------------------ |

8. Select **Upload Document** and upload the document you downloaded in the previous step.

9. Sensible extracts data from the document and displays it as JSON in the **Extraction** pane. You'll use this example extraction in the following steps.



Configure Zapier using the test extraction
====

In Zapier:

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











