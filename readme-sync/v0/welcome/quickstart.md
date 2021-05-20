---
title: "Quickstart"
hidden: true
---



DRAFT: UNPUBLISHED
-----


this is a draft version that is not yet included in the table of contents.



Make your first config: auto insurance quote
----

Let's get started with SenseML! In this quickstart, you'll write a custom config to extract structured data from auto insurance quote PDFs and integrate Sensible with your application.

**Create the config**

1. You'll need an account.  Get one at [Sensible.so](https://www.sensible.so/get-early-access).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the Sensible app at [app.sensible.so](app.sensible.so).
3. Click **Create document type** and name  it "auto_insurance_quote". Leave the defaults and click **Create**.

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_doc_type.png)

3. Click **Upload document**  and choose this [generic car insurance quote](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/pdfs/auto_insurance_anyco_golden.pdf).

4. Click **Create configuration**, name  it "anyco" (for the fictional company providing the quote), and click **Create**.

5. Click the configuration name to edit the configuration..

6. For this quickstart, let's extract only a few pieces of information:

   - the policy number
   - the policy period
   - the premium for comprehensive insurance.
   
7. Paste in this config to extract the data:
 ```json
 {
   "fields": [
     {
       "id": "policy_number",
       "anchor": {
         "match": [
           {
             "text": "policy number",
             "type": "startsWith"
           }
         ]
       },
       "method": {
         "id": "box",
         "position": "below"
       }
     },
     {
       "id": "policy_period",
       "anchor": "policy period:",
       "method": {
         "id": "label",
         "position": "right"
       }
     },
     {
       "id": "comprehensive_premium",
       "anchor": "comprehensive",
       "type": "currency",
       "method": {
         "id": "row",
         "tiebreaker": "second"
       }
     }
   ]
 }
 ```

   You should see the following extracted data as the output of the config:

   ```json
   {
     "policy_number": {
       "type": "string",
       "value": "123456789"
     },
     "policy_period": {
       "type": "string",
       "value": " April 14, 2021 - Oct 14, 2021"
     },
     "comprehensive_premium": {
       "source": "$150",
       "value": 150,
       "unit": "$",
       "type": "currency"
     }
   }
   ```

   The following image shows this example in the Sensible app:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_config_1.png)

Congratulations! You've just created your first config! 

**How it works**

- Each "field" is a basic query unit in SenseML, and the field ID is output as the key in the structured data. 

- SenseML searches first for a text "anchor" because it's a computationally quick and inexpensive way to narrow down the location in the document where you want to extract data. Then, SenseML uses a "method" to expand out from the anchor and grab the data you want. This config uses three types of methods:

  - To grab the policy number, the config uses the "box" method. This tells SenseML that the anchor (`"Policy number"`) is inside of a box, and SenseML should grab the box contents except for the anchor itself

    ```json
    {
          "id": "policy_number",
          "anchor": {
            "match": [
              {
                "text": "policy number",
                "type": "startsWith"
              }
            ]
          }
    ```

    ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_box.png)

This returns:

```json
{
  "policy_number": {
    "type": "string",
    "value": "123456789"
  },
```
  - To grab the policy period, the config uses the "label" method. This tells SenseML that the anchor (`"policy period"`) is text that is pretty close to some other text, and SenseML should grab the nearest line in the position specified.  (The "closeness" of lines is something you can configure with a preprocessor.)

    ```json
        {
          "id": "policy_period",
          "anchor": "policy period:",
          "method": {
            "id": "label",
            "position": "right"
          }
        },
    ```

    ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_label_right.png)

    This returns:

    ```json
      "policy_period": {
        "type": "string",
        "value": " April 14, 2021 - Oct 14, 2021"
      
    ```

    

    You can grab text to the right, left, above, or below a label. For example, how would you use a label to grab the driver's name? Try it out.

    **key concept**

    




TODO:

- talk about Integrating w/ your app (API calls + how you'd use the above app stuff to test out configs before doing the API calls...also talk about seeing your extraction run history in the app (sort alike logging?)