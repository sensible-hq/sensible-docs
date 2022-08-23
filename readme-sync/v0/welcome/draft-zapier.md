---
title: "Zapier to airtable integration tutorial"
hidden: true

---

TODO: rewrite for preexisting geico example??? 



Getting your document data into a variety of destinations is easy  with Sensible's Zapier integration. This tutorial describes getting data from an example document into the Airtable database from Sensible using Zapier. 

Go from documents like this:

![image-20220815094925837](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815094925837.png)

To a database like this:

TODO screenshot with MULTIPLE records.



Prerequisites
---

We'll be working with some mock car quotes and their extracted data. To configure their data extraction, you'll need to create an `auto_insurance_quote` doc type in the Sensible app. In the doc type, create a config named `zapier_test` and paste in the following config:

```
{
  "fingerprint": {
    "tests": [
      {
        "page": "first",
        "match": [
          {
            "text": "anyco auto insurance",
            "type": "startsWith"
          }
        ]
      },
      {
        "page": "last",
        "match": [
          {
            "text": "please be sure to review your contract for a full explanation of coverages",
            "type": "includes"
          }
        ]
      }
    ]
  },
  "fields": [
    {
      "id": "policy_number",
      "type": "string",
      "anchor": {
        "match": {
          "text": "policy number",
          "type": "startsWith"
        }
      },
      "method": {
        "id": "box"
      }
    },
    {
      "id": "name_insured",
      "anchor": "name of driver",
      "method": {
        "id": "label",
        "position": "below"
      }
    },
    {
      "id": "comprehensive_premium",
      "anchor": "comprehensive",
      "type": "currency",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "second"
      }
    },
    {
      "id": "property_liability_premium",
      "anchor": "property",
      "type": "currency",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "second"
      }
    },
    {
      "id": "_raw_policy_period",
      "anchor": "policy period",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
  ],
  "computed_fields": [
    {
      "id": "policy_start",
      "method": {
        "id": "split",
        "source_id": "_raw_policy_period",
        "separator": "-",
        "index": 0
      }
    },
    {
      "id": "policy_end",
      "method": {
        "id": "split",
        "source_id": "_raw_policy_period",
        "separator": "-",
        "index": 1
      }
    }
  ]
}
```

Select **Publish** and select **Production**: TODO reuse screenshot.

Test the extraction using the **quick extraction** dashboard so you'll have test data for the initial Zapier integration later.

TODO screenshots.

ALTERNATE PREREQ
----

Use the quick extract pane (link) to extract info from an example Geico page: https://github.com/sensible-hq/sensible-configuration-library/blob/main/auto_policy_declaration_pages/geico/geico_sample.pdf 

![image-20220823112424601](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220823112424601.png)





Make an empty destination database
----

In Airtable, make a new base and name it "Sensible test":

![image-20220815101632157](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815101632157.png)



In the base, create columns for the values from the document that you want to extract. Let's say we want to extract:

- Driver's name
- Policy number
- Policy start and end dates
- Dollar amount of comprehensive premium
- Dollar amount of property liability premium.

Create a table named **Anyco auto insrance quote** and create columns in the table that correspond to the previously listed values. **Optional**: Right-click a column heading to edit its type, for example, currency, date, or string. 

![image-20220815102002800](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815102002800.png)



Configure Zapier 
----

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











