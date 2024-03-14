---
title: "Getting started with layout-based extractions"
hidden: false
---


In this tutorial, you'll learn to extract data out of a set of similar documents using a layout-based query language, SenseML. You'll write JSON to tell Sensible about which data to extract from an example document, using what you know about the layout of the document. SenseML uses a mix of techniques, including machine learning, heuristics, and rules, to extract your target information.

You can then save your descriptions as a "config." Publish your config to automate extracting from similar documents.   

Use this tutorial if you want a guided tour of SenseML concepts and the Sensible app. Or see the following links:

- SenseML is for advanced config authoring. For a simpler authoring experience, use Sensible Instruct. For more information about SenseML versus Sensible Instruct, see [Choosing extraction strategy](doc:author). For authoring in Sensible Instruct, see [Getting started](doc:getting-started-ai).

- If you instead want to explore without much explanation, then [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app tutorials in the `sensible_instruct_basics` document type.
- If you want a quick "hello world" API response, see the [API quickstart](doc:quickstart).

Get structured data from an auto insurance quote
===

Let's get started with SenseML!


If you can write basic SQL queries, you can write SenseML queries. SenseML shields you from the underlying complexities of PDFs, so you can  write queries that are visually and logically clear to a human programmer.

 In this tutorial, you'll:

- [Write a collection of queries ( a "config")](doc:getting-started#create-a-config) to [extract structured data](doc:getting-started#extract-data) from an example auto insurance document 
- [Learn how the config works](doc:getting-started#how-it-works), including key concepts like lines, anchors, and methods
- [Test the config](doc:getting-started#test-the-config) by running your config against a second, similar auto insurance document
- [Use the API](doc:getting-started#integrate-with-your-application) to integrate your Sensible config with your application
- [Validate extractions in production](doc:getting-started#validate-extractions-in-production) by using JsonLogic to define expected extracted values and flag unexpected values as warnings or errors

Get an account
====

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

Configure the extraction
====

1. In the [**Document Types**](https://app.sensible.so/document-types/) tab, Click **New document type**  to create a new document type and name  it "auto_insurance_quote." Leave the defaults and click **Create**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_doc_type.png)

2. To upload an example document for your document type, take the following steps:

   1. Download the following document:

   | Example document | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
   | --------------------------- | ------------------------------------------------------------ |
   2. As the following screenshot shows, click the **auto_insurance_quote** document type you created,  click the **Reference documents** tab, and click **Upload document**:
      ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_upload_doc.png) 

   3. In the file upload dialog, choose the generic car insurance quote you downloaded in a previous step.


2. To create a configuration for your document type, take the following steps:
   1. In your **auto_insurance_quote** document type, click the **Configurations** tab. 

   2. On the tab, click **Create configuration**, name  it "anyco" (for the fictional company providing the quote), and click **Create**.

3. To edit your  **anyco** configuration, click it. When the configuration opens, you see an empty config pane on the left, the document in the middle, and an empty output pane on the right:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_blank_config.png)

Extract data
====


For this tutorial, you'll extract these fields:

- a couple of premiums
- the policy number
- the policy period

1. Paste this config into the left pane in the editor to extract the data:

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            /* ask a free-text question.
           You can author LLM-powered queries in Sensible Instruct
           instead of in JSON */
            "id": "bodily_injury_premium",
            "description": "bodily injury premium",
            "type": "currency"
          },
          {
            "id": "customer_service_phone",
            "description": "insurer's customer service phone number",
          }
        ]
      }
    },
    {
      /* ID for target data */
      "id": "policy_period",
      /* search for target data 
      near text "policy period" in doc*/
      "anchor": "policy period",
      "method": {
        /* target to extract is a single line 
        near anchor line ("policy period") */
        "id": "label",
        /* target data is to right of anchor line */
        "position": "right"
      }
    },
    {
      /* target data is near text "comprehensive" */
      "id": "comprehensive_premium",
      "anchor": "comprehensive",
      /* target data is a currency, else return null */
      "type": "currency",
      "method": {
        /* target to extract is in a row */
        "id": "row",
        /* target is to right of anchor ("comprehensive") in row */
        "position": "right",
        /* grab 2nd row cell (right of anchor) */
        "tiebreaker": "second"
      }
    },
    /* target data is text in a box
    with anchor "policy number" */
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
    }
  ]
}
```

The following image shows this example in the Sensible app:


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_after_paste.png)



You should see the following extracted data in the right pane:

```json
{
  "bodily_injury_premium": {
    "source": "$100",
    "value": 100,
    "unit": "$",
    "type": "currency",
    "confidenceSignal": "confident_answer"
  },
  "customer_service_phone": {
    "value": "1800 123 4567",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "policy_period": {
    "type": "string",
    "value": "April 14, 2021 - Oct 14, 2021"
  },
  "comprehensive_premium": {
    "source": "$150",
    "value": 150,
    "unit": "$",
    "type": "currency"
  },
  "policy_number": {
    "type": "string",
    "value": "123456789"
  }
}
```

Congratulations! You created your first config and extracted your first document data. If you want to process car insurance quotes generated by a different company, you can create a new config and upload a new reference document. 

- For a deep dive on how the config works, see [the following section](doc:getting-started#how-it-works).

- If you want to skip ahead and try out the API, see [Integrate with your application](doc:getting-started#integrate-with-your-application). 

How layout-based extraction works
====

This guide focuses on layout-based document extraction, which works as follows:

- Each "field" is a basic query unit in Sensible.  Each field outputs a piece of data from the document that you want to extract. Sensible uses the field `id` as the key in the key/value JSON output. For more information, see [Field](doc:field-query-object).

- Sensible searches first for a text "anchor" because it's a computationally quick way to narrow down the location of the target data to extract.  An anchor is text that always occurs close to your target text. Without it, Sensible wouldn't know which page to search in for your target text . For more information about defining complex anchors, see [Anchor](doc:anchor). 

- Then, Sensible uses a "method" to expand its search out from the anchor and extract the data you want. For more information about methods, see [Methods](doc:methods).

This config uses three types of layout-based methods:

  | Type of method | explanation                                                  | description                                       |
  | -------------- | ------------------------------------------------------------ | ------------------------------------------------- |
  | layout         | [How it works: label method](doc:getting-started#how-it-works-label-method) | Grab info immediately proximate to labeling text. |
  | layout         | [How it works: row method](doc:getting-started#how-it-works-row-method) | Grab info from a cell in a row.                   |
  | layout         | [How it works: box method](doc:getting-started#how-it-works-box-method) | Grab info from a box.                             |


This config also uses one natural-language, or AI-powered, method, to demonstrate that you can combine layout-based and natural-language methods in the same config:

| Type of method   | explanation                                                  | description                                                  |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Natural-language | [How it works: query group method](doc:getting-started#how-it-works-query-group-method) | Ask a free-text question about simple information in the document |

How it works: Query Group method
---

The easiest way to start extracting simple information is to ask a natural-language question, or query.

For example, to extract the bodily injury liability:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_question.png)



The config uses the [Query Group](doc:query-group) method to query for the  `bodily injury premium`. You can group together other queries if the answers are located within a page or two of each other in the document. For example, in the group, the config also queries for the  `insurer's customer service phone number`.  

```json
 {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            /* ask a free-text question.
           You can author LLM-powered queries in Sensible Instruct
           instead of in JSON */
            "id": "bodily_injury_premium",
            "description": "in the table, what's the bodily injury premium?",
            "type": "currency"
          },
          {
            "id": "customer_service_phone",
            "description": "insurer's customer service phone number",
          }
        ]
      }
    },
```

This config returns:

```json
{
  "bodily_injury_premium": {
    "source": "$100",
    "value": 100,
    "unit": "$",
    "type": "currency",
    "confidenceSignal": "confident_answer"
  },
  "customer_service_phone": {
    "value": "1800 123 4567",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
```

Try it out: change one of the questions to `"street address for the Anyco insurance company"` and see what you get.

You can write natural-language methods powered by large-language models (LLMs), such as the Query Group method, in SenseML, or in Sensible Instruct, Sensible's visual authoring tool. For more information about Sensible Instruct, see [Getting started](doc:getting-started-ai).

Natural-language methods can run up against limitations with complex document formatting. In such cases, combine natural-language methods with layout-based methods in the same document extraction configuration. 

Let's look next at several simple layout-based methods.

How it works: Label method
----

To extract the policy period from the document:
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_label_right.png)

The config uses the [Label method](doc:label):

```json
      {
        "id": "policy_period",
        "anchor": "policy period:",
        "method": {
          "id": "label",
          "position": "right"
        }
      }
```

This describes the layout of the data to extract relative to the anchor:

- The anchor (`"policy period"`) is text that's pretty close to the text to extract, so it can serve as a "label" for that text  (`"id": "label"`). 
- The text to extract is to the right of the anchor (`"position": "right"`).  

This config returns:

```json
    "policy_period": {
      "type": "string",
      "value": " April 14, 2021 - Oct 14, 2021"
     }   
```

You can extract text to the right, left, above, or below a label. For example, how would you use a label to extract the driver's name? Try it out.

Key concept: lines
----

See those gray boxes around the text in the following image?

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_concept_1.png)

Each gray box shows the boundaries for a "line." Sensible recognizes lines using whitespaces and other factors, so "lines" can occupy the same height on the page.

The Label method can operate in a single line, or on consecutive lines. Here's a question: for the preceding image, can you use the Label method to anchor on  "Bodily injury"  and return "$25,000 each"? Try it out:

    {
        "id": "doesnt_work_returns_null",
        "anchor": "bodily injury",
        "method": {
            "id": "label",
            "position": "right"
        }
    }

This returns null, because the Label method works for text in the same line or in proximate lines. In this case, the problem is that the gap between the two lines of text is more than 0.2 inches:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_concept_2.png)

 Take a look instead at a purpose-built Row method instead to extract text in a table. 

How it works: Row method
----

To extract the comprehensive premium of $150:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_row.png)

The config uses the [Row method](doc:row):

```json
      {
          "id": "comprehensive_premium",
          "anchor": "comprehensive",
          "type": "currency",
          "method": {
              "id": "row",
              "tiebreaker": "second",
          }
      }
```

This describes the data to extract:

- The anchor text (`"comprehensive"`) is part of a row of lines (`"id": "row"`).
- The returned value is a currency (`"type": "currency"`). For other data types you can define, see [Field query object](doc:field-query-object).
- The text to extract is the second line in the row after the anchor  (`"tiebreaker": "second"`).  Use tiebreakers to select lines in rows, for example maximum and minimum values (`<` and `>`).
- By default, the Row method extracts values to the right of the anchor. You can override the default by specifying (`"position":"left"`). 

This returns: 

```json
    "comprehensive_premium": {
      "source": "$150",
      "value": 150,
      "unit": "$",
      "type": "currency"
    }
```

But wait! Why didn't `"tiebreaker": "second"` select $250 instead of $150, since $250 is the second line after the anchor (the first line is `............`)? 

The reason is that `"tiebreaker": "second"` evaluates *after* the data type specified in the field, `"type": "currency"`. Instead of looking for the second line after the anchor in general, Sensible looks for the second line *that contains a currency*.  Convenient, right?

Key concept: visualize anchors and matches
----

In the app, you can visually inspect anchors and methods by looking at their color coding:

- Orange boxes show lines matched by the Anchor object.
- Blue boxes show lines matched by the Method object.
- Dotted blue boxes show lines discarded by the Method object. Seeing the entire method match in the app can help you troubleshoot unexpected output.

To continue the Row method example from the previous section, in the following image the orange box shows that "Comprehensive" is the anchor line:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_concept_3.png)

The dotted blue boxes show you that the Row method matches *all* the lines  in the row after the anchor, but then narrows down the actual output to $150 using `"tiebreaker": "second"`. 

How it works: Box method
----

To extract the policy number from this document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_box.png)

The config uses the [Box method](doc:box):

```json
{
      "id": "policy_number",
      "type": "string",
      "anchor": {
        "match": 
          {
            "text": "policy number",
            "type": "startsWith"
          }  
      },
      "method": {
        "id": "box"
      }
    }
```

 This describes the data to extract:

- The anchor is inside a box (`"id": "box"`).
- The anchor text  is `policy number`.
- The anchor line is a little more complex than previous examples, because it also defines a match type (`"type": "startsWith"`). You can write a simpler string anchor as `"anchor":"policy number"`, or you can expand to complex anchors. For more information, see [Anchor object](doc:anchor).

 This returns: 

```json
  "policy_number": {
    "value": "123456789",
    "type": "string"
  }
```

**Note:** Sensible extracts the box contents, but not the anchor itself.  By default, Sensible returns method results, not anchor results.

Advanced layout-based queries
----

You can get more advanced with this auto insurance config. For example:

- The limits listed in the table are tricky for the Row method to capture since they can be a variable number of lines. Row methods depend on strict horizontal alignment of lines, so Sensible extracts the first line. Instead, use the [NLP Table method](doc:nlp-table) to more reliably capture the data in each cell of the whole table. 
- What if the document listed emails, and you wanted to capture all those emails? You could use a regular expression (regex) in a `"match":"all"` anchor coupled with a [Passthrough method](doc:passthrough), or the [Regex method](doc:regex).
- You can split the policy period into two dates, either by using the [Split computed field method](doc:split), or by setting the [Date](doc:types#date) type on the field and using a tiebreaker.

To check out other methods, see [Methods](doc:methods).

Test the config
====

Before integrating the config with an application and writing [validation tests](doc:validate-extractions) against it, double check the config by uploading another quote.

1. Repeat the steps in the previous section to upload a second generic car insurance quote:

   | auto_insurance_anyco_2 | [Download link](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_2.pdf) |
   | ----------------------------- | ------------------------------------------------------------ |

2. Click the **anyco** config, select the "auto_insurance_anyco_2" document, and look at the output. Unlike the first document, the policy period takes up two lines, so Sensible misses the end year (2021):

   ```json
   {
     "policy_period": {
       "type": "string",
       "value": "May 20, 2021 - Nov 20,"
     }
   ```

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_error_1.png)

That seems like sloppy document formatting, but let's work with it. There are several options for capturing the policy period reliably, including:  

- Document Range method
- Region method

**Alternative 1: Document Range method**

You can use the [Document Range](doc:document-range) method to extract the policy period. This method extracts succeeding lines of text after an anchor. You need to configure some optional parameters, because the Document Range method by default discards anchor lines. Since the date range is part of the anchor line (the line containing `"policy period"`), you need to specify to:

- include the anchor with `"includeAnchor": true`
- filter out unwanted text in the anchor (the words "Policy period") with a Word Filters parameter.

Try it out by replacing your existing `policy_period` field with this example:

```
   {
      "id": "policy_period",
      "anchor": "policy period",
      "method": {
        "id": "documentRange",
        "includeAnchor": true,
        "wordFilters": [
          "policy period"
        ],
        "stop": {
          "text": "for customer",
          "type": "startsWith"
        },
      }
    }
```

**Alternative 2: Region method**

You can use the [Region method](doc:region) to extract the policy period. A region is a rectangular space defined by coordinates relative to the anchor. 

Replace the existing `policy_period` field with the following field in the Sensible app:

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
        "offsetX": -0.2,
        "offsetY": -0.1,
        "width": 3.6,
        "height": 0.45,
        "start": "left",
        "wordFilters": [
          "policy period",
        ]
      }
    },
```

This field defines a region in inches relative to the anchor. Since the region overlaps the anchor, specify a Word Filters parameter to remove the anchor text in the output. See the green box representing the region in the editor? This box dynamically resizes as you adjust the region parameters (such as the Height and Start parameters), so you can visually tweak the region till you're satisfied. 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_error_3.png)

Let's double check that this region also works with the first document:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_error_4.png)

Yes, it works too.

3. Click **Publish configuration** and choose **Production** to save your changes to the config.

In a production scenario, continue testing documents until you have confidence your configs work with the document type you've defined.  Then, write tests to validate the extractions in production.

Integrate with your application
====

When you're ready to integrate with your application, enable using the config with the Sensible SDKs or API by taking the following steps:

1. Click **Publish configuration**.  The config is still a work in progress, so click **Development**.  Now you can use the query parameter `env=development`  to test the integration before you go to production:![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_publish_config.png).
2. Use the Sensible SDKs or API to integrate with your application.

Validate extractions in production 
====

In a previous section, you tested a couple of documents manually. Now it's time to scale up and quality control the extractions by writing tests that run for all API extractions in a doc type.

Use JsonLogic to validate that the extracted information makes sense for the car insurance document:

- Test that the property damage liability premium is cheaper than the comprehensive premium:
  -  `{"<":[{"var":"property_liability_premium.value"},{"var":"comprehensive_premium.value"}]}`
- Test that the policy number is a nine-digit number:
  - `{"match":[{"var":"policy_number.value"},"\\d{9}"]}`

To add these tests:

1. In the **auto_insurance_quote** document type, click **Create validation**. Add the following input to the dialog:
   - Set the **Severity** to **Warning**
   - Set the **Description** to "prop. damage is less than comprehensive"
   - Set the **Condition** to:

```json
{"<":
 [
     {"var":"property_liability_premium.value"},
     {"var":"comprehensive_premium.value"}
 ]
}
```

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_validation.png)

3. Click **Create**.
4. Repeat the previous steps to create another validation with the following settings:
   -  Set the **Severity** to **Error**
   -  Set the **Description** to "policy number is a nine-digit number"
   -  Set the **Condition** to:

```json
{"match":
  [
      {"var":"policy_number.value"},"\\d{9}"
  ]
}
```



5. To test the validations with a document that's missing information, [try out an API call](doc:api-tutorial-async-1) with the following example document that has these errors:

   -  the policy number is missing
   -  the property damage liability premium is $200 more than the comprehensive premium

| auto_insurance_anyco_3 | [Download link](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_3.pdf) |
| ----------------------------- | ------------------------------------------------------------ |

You should receive a response with errors and warnings in the Validations array, as shown in the following API response excerpt:

```json
{
    "id": "11404335-1ea4-4414-a5ca-1ccef568ebec",
    "created": "2021-09-21T17:36:56.339Z",
    "status": "COMPLETE",
    "type": "auto_insurance_quote",
    "configuration": "anyco",
    "parsed_document": {
        "policy_period": null,
        "comprehensive_premium": {
            "source": "$100",
            "value": 100,
            "unit": "$",
            "type": "currency"
        },
        "property_liability_premium": {
            "source": "$300",
            "value": 300,
            "unit": "$",
            "type": "currency"
        },
        "policy_number": null
    },
    "validations": [
        {
            "description": "prop. damage less than comprehensive",
            "severity": "warning"
        },
        {
            "description": "policy number is a nine-digit number",
            "severity": "error"
        }
    ],
    "validation_summary": {
        "fields": 4,
        "fields_present": 2,
        "errors": 1,
        "warnings": 1,
        "skipped": 0
    }
}
```


Next
====

- Check out the [SenseML method reference docs](doc:methods) to write your own extractions
- Learn more about [validations](doc:validate-extractions) to test the quality of your extractions in production
