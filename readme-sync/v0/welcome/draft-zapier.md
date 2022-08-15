---
title: "Zapier to airtable integration tutorial"
hidden: true

---

Getting your document data into a variety of destinations is easy  with Sensible's Zapier integration. This tutorial describes getting data from an example document into the Airtable database from Sensible using Zapier. 

Go from this document:

![image-20220815094925837](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220815094925837.png)



Prerequisites
---

We'll be working with some mock car quotes and their extracted data. To configure their data extraction, you'll need to create an `auto_insurance_quote` doc type in the Sensible app. In the doc type, create a config named `zapier_test` and paste in the following config:

```
{
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



Select your Sensible account, and enter your API key from your [dashboard] TODO LINK to connect your Sensible account to your Zapier account

TODO screenshot.







[icon: ? ] Extract custom data from your documents
----

- SenseML methods reference
- API reference
- GSG (longform)
- advanced: for really complex docs: https://docs.sensible.so/docs/sections 



[icon: puzzle piece] Integrate with your toolchain/go to production
---



- API quickstart
- API ref docs for document types (?)
- going to prod checklist? 
- https://docs.sensible.so/docs/test-before-integrating-configs
- https://docs.sensible.so/docs/validate-extractions
- https://docs.sensible.so/docs/performance





What's your use case?

|                    |                                                     |                                                              |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------------ |
|                    |                                                     |                                                              |
| if you're a...     | business analyst                                    | low-code developer                                           |
| and you want to... | Turn commonly available PDF forms into Excel tables | I want to get structured JSON from semi-structured PDFs to build workflows |
| start here...      | [Get started](TBD LINK)                             | [Get started](doc:quickstart)                                |



TODO: add images to the table under an 'example' row?



TODO: do I need 2 new folders under welcome? 1 for Excel/CSV/spreadsheet, 1 for developers?  or a whole new section for 'outputs' to also include yamls? json5 etc? 





COULD BE LIKE THIS (with some nice visuals):



https://docs.launchdarkly.com/home < add icons w headings and talbe (with icons?) below for quick cheap nickeness...remember those open source icons...



https://www.prisma.io/docs/getting-started

https://rasa.com/docs/

https://docs.timescale.com/ <- how to do in readme? 

https://docs.docker.com/ <--- nice! Icons! 







"which tutorial is right for me?"









