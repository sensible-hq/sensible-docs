---
title: "Quickstart"
hidden: true
---



DRAFT: UNPUBLISHED
-----


this is a draft version that is not yet included in the table of contents.



Get structured data from an auto insurance quote
===

Let's get started with SenseML! In this quickstart, you'll write a custom config to extract structured data from auto insurance quote PDFs and integrate Sensible with your application.

Create the config
----

1. You'll need an account.  Get one at [Sensible.so](https://www.sensible.so/get-early-access).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the Sensible app at [app.sensible.so](app.sensible.so).
3. Click **Create document type** and name  it "auto_insurance_quote". Leave the defaults and click **Create**.

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_doc_type.png)

3. Click **Upload document**  and choose this [generic car insurance quote](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/pdfs/auto_insurance_anyco_golden.pdf).

4. Click **Create configuration**, name  it "anyco" (for the fictional company providing the quote), and click **Create**.

5. Click the configuration name to edit the configuration.

6. For this quickstart, let's extract only a few pieces of information:

   - the policy number
   - the policy period
   - the premium for comprehensive insurance.
   
7. Paste in this config in the left pane in the editor to extract the data:
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

  - To grab the policy number, the config uses the "box" method. This tells SenseML that the anchor (`"Policy number"`) is inside of a box, and SenseML should grab the box contents except for the anchor itself.

    For this box:
  
    ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_box.png)
  
    The config uses this Field query:
  
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
  
    Which returns:

    ```json
    {
    "policy_number": {
    "type": "string",
    "value": "123456789"
    }
    ```
    
  - To grab the policy period, the config uses the "label" method. This tells SenseML that the anchor (`"policy period"`) is text that is pretty close to some other text, and SenseML should grab the nearest text to the label in the position specified (`right`).  (The "closeness" of lines is something you can configure with a preprocessor.)
  
    For this text:
    ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_label_right.png)
    The config uses this Field query:
  
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
  
    This returns:
  
    ```json
      "policy_period": {
        "type": "string",
        "value": " April 14, 2021 - Oct 14, 2021"
      
    ```
  
    
  
    You can grab text to the right, left, above, or below a label. For example, how would you use a label to grab the driver's name? Try it out.
  
  - To grab the comprehensive coverage premium, the config uses the "row" method. This tells SenseML that the anchor (`"comprehensive"`) is part of a row in a table, and to grab some text in that row.
  
    To grab this premium of $150:
  
    ![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_row.png)
    The config uses this Field query:
    
    ```json
        {
          "id": "comprehensive_premium",
          "anchor": "comprehensive",
          "type": "currency",
          "method": {
            "id": "row",
            "tiebreaker": "second"
          }
    ```
    
    This returns: 
    
    ```json
      "comprehensive_premium": {
        "source": "$150",
        "value": 150,
        "unit": "$",
        "type": "currency"
      }
    ```
    
    The tiebreaker lets you select which element in the row you want and can include maximums and miniums (`<` and `>`). You can also select elements to the right or left of the anchor using `position`.  (not shown).

**Key concepts: lines**
 You might ask yourself, "why can't I just use a label in the table? Why can't I set a label for "bodily injury liability" and then grab the line starting with "$25,00" to the right of it, like this: 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_concept_1.png)

```json
    {
      "id": "injury_liability",
      "anchor": "bodily injury",
      "method": {
        "id": "label",
        "position": "right"
      }

```

The reason this query doesn't work is that SenseML operates on "lines". See those gray boxes around the text in the preceding image? Each gray box is a line. Lines are defined by whitespace, so multiple "lines" can occupy the same x-axis. Since the Label method works only for closely proximate lines (sensitive to spacing and font size), this config uses the purpose-built "row" method instead.

**Advanced queries**

You can get more advanced with this auto insurance config. For example:

- You can use a Computed Field method to return the sum of all the listed premiums, which is $260 ($100 + $10 + $150).
- The limits listed in the table are tricky since they can be a variable number of lines. You can use an xRangeFilter set in the Document Range method to capture them. 

We'll save these and other techniques for a later tutorial! 

Sanity test the config
----

Before integrating the config with an application and writing tests against it, let's sanity test the config by simply uploading another quote.

1.  Repeat the steps in the previous section to upload this [generic car insurance quote](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/pdfs/auto_insurance_anyco_golden_2.pdf).

2. Click the **anyco** config and look at the output.

   Uh oh! It looks like this policy period spills over onto the next line. That's some yucky PDF formatting, but we can't do anything about it. So we miss the end year (2021):

How can we capture the policy period reliably? AS you become more familiar with SenseML, you might guess you'd use a Document Range method, which grabs multiple lines of text, like paragraphs, after an anchor. But nope, this sloppily formatted PDF doesn't fit neatly into that method, because the first line we want is also part of the anchor, so it doesn't get included in the output:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/quickstart_error_1.png)

Fortunately, there are almost always multiple ways to tackle a problem in SenseML. 





```json
    {
      "id": "policy_period",
      "anchor": {
        "match": [
          {
            "text": "policy period",
            "type": "startsWith"
          }
        ]
      },
      "method": {
        "id": "region",
        "offsetX": -0.1,
        "offsetY": -0.1,
        "width": 3.5,
        "height": 0.45,
        "start": "left",
        "wordFilters": [
          "policy period",
        ]
      }
    },
```







TODO:

- talk about Integrating w/ your app (API calls + how you'd use the above app stuff to test out configs before doing the API calls...also talk about seeing your extraction run history in the app (sort alike logging?)