---
title: "Getting started layout-powered extractions"
hidden: false
---

In this tutorial, you'll learn to extract data out of a collection of similar documents using a layout-based query language, SenseML. You'll write JSON to tell Sensible about which data to extract from a set of similar documents, using what you know about the layouts of the documents in the set. SenseML uses a mix of techniques, including machine learning, heuristics, and rules, to extract your target information.

You can then save your descriptions as a "config." Publish your config as an API endpoint, and use the endpoint to automate extracting from similar documents.   

Note that you can mix and match SenseML methods with Sensible Instruct methods. SenseML is a a JSON-formatted, layout-based query language, and Sensible Instruct is an AI-powered subset of SenseML that you can author in the app, no JSON required. Use SenseML for advanced document extraction, for example, for complex document layouts. For simpler document extraction, author AI-powered extraction configurations using Sensible Instruct. 

Use this tutorial if you want a guided tour of SenseML concepts and the Sensible app. Or see the following links:

- For more information about SenseML versus Sensible Instruct, see [Choosing extraction strategy](doc:author). For authoring in Sensible Instruct, see [Get started with AI-powered extraction](doc:getting-started-ai).

- If you instead want to explore without much explanation, then [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app tutorials: [extract_your_first_data](https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data), [tables and rows](https://app.sensible.so/editor/?d=senseml_basics&c=2_tables_and_rows&g=2_tables_and_rows), [checkboxes, paragraphs, and regions](https://app.sensible.so/editor/?d=senseml_basics&c=3_checkboxes_paragraphs_and_regions&g=3_checkboxes_paragraphs_and_regions), and a [blank-slate challenge](https://app.sensible.so/editor/?d=senseml_basics&c=4_extract_from_scratch&g=4_extract_from_scratch).
- If you to get want a quick "hello world" API response, see the [quickstart](doc:quickstart).

Get structured data from an auto insurance quote
===

Let's get started with SenseML!


If you can write basic SQL queries, you can write SenseML queries. SenseML shields you from the underlying complexities of PDFs, so you can  write queries that are visually and logically clear to a human programmer.

 In this tutorial, you'll:

- [Write a collection of queries ( a "config")](doc:getting-started#create-a-config) to [extract structured data](doc:getting-started#extract-data) from an example auto insurance PDF 
- [Learn how the config works](doc:getting-started#how-it-works), including key concepts like lines, anchors, and methods
- [Test the config](doc:getting-started#test-the-config) by running your config against a second, similar auto insurance PDF
- [Use the API](doc:getting-started#integrate-with-your-application) to integrate your Sensible config with your application
- [Validate extractions in production](doc:getting-started#validate-extractions-in-production) by using JsonLogic to define expected extracted values and flag unexpected values as warnings or errors

Get an account
====

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

Configure the extraction
====

1. Click **New document type**  to create a new document type and name  it "auto_insurance_quote." Leave the defaults and click **Create**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_doc_type.png)

2. To upload an example document for your document type, take the following steps:

   1. Download the following PDF document:

   | Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
   | --------------------------- | ------------------------------------------------------------ |
   2. As the following screenshot shows, click the **auto_insurance_quote** document type you just created,  click the **Reference documents** tab, and click **Upload document**:
      ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_upload_doc.png) 

   3. In the file upload dialog, choose the generic car insurance quote you just downloaded.


2. To create a configuration for your document type, take the following steps:
   1. In your **auto_insurance_quote** document type, click the **Configurations** tab. 

   2. On the tab, click **Create configuration**, name  it "anyco" (for the fictional company providing the quote), and click **Create**.

3. To edit your  **anyco** configuration, click it. When the configuration opens, you see an empty config pane on the left, the PDF in the middle, and an empty output pane on the right:

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
      /* ID for target data */
      "id": "bodily_liability_premium",
      /* search for target data 
      on page containing this anchor line*/
      "method": {
        "id": "question",
        /* ask a free-text question, get an answer powered by AI.
          best suited to simple questions
          that have one label and one answer 
          in the document.  You can also author this field in Sensible Instruct
          instead of in JSON */
        "question": "in the table, what's the bodily injury premium?"
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
    /* target data is all the text in box
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
  "bodily_liability_premium": {
    "source": "$100",
    "value": 100,
    "unit": "$",
    "type": "currency"
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

Congratulations! You created your first config and extracted your first document data. If you want to process car insurance quotes generated by a different company, you can create a new config and upload a new reference PDF. 

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


This config also uses one natural-language, or AI-powered, method, in order to show that you can combine layout-based and natural-language methods in the same config:

| Type of method   | explanation                                                  | description                                                  |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Natural-language | [How it works: question method](doc:getting-started#how-it-works-question-method) | Ask a free-text question about simple information in the document |

How it works: Question method
---

The easiest way to start extracting simple information is to ask a natural-language question, as you would ask a chatbot.

For example, to extract the bodily injury liability:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_question.png)



The config uses the [Question](doc:question) method to ask, `in the table, what's the bolidy injury premium?`:  

```
{
      /* ID for target data */
      "id": "bodily_liability_premium",
      /* search for target data 
      on page containing this text*/
      "anchor": "anyco auto insurance",
      "method": {
        "id": "question",
        /* ask a free-text question.
          best suited to simple questions
          that have one label and one answer 
          in the document. */
        "question": "in the table, what's the bodily injury premium?"
      }
    
```

This config returns:

```json
  "bodily_liability_premium": {
    "type": "string",
    "value": "$100"
```

Try it out: change the question to `"what's the street address for the Anyco insurance company?"` and see what you get.

You can also natural-language methods such as Question in JSON, or in Sensible Instruct, Sensible's visual authoring tool. For more information about Sensible Instruct, see [Get started with AI-powered extractions](doc:getting-started-ai).

Natural-language methods, such as Sensible's Question method or GPT-3 powered Table method, can run up against limitations with highly complex document formatting, or layouts. In such cases, combine natural-language methods with layout-based methods in the same document extraction configuration. 

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

Advanced queries
----

You can get more advanced with this auto insurance config. For example:

- You can use a [Column method](doc:column) to return all the listed premiums ($90, $15, $130).
- The limits listed in the table are tricky for the Row method to capture since they can be a variable number of lines. Row methods depend on strict horizontal alignment of lines, so Sensible extracts the first line. Instead, use the [Table method](doc:table) to more reliably capture the data in each cell of the whole table. Or, use an `xRangeFilter` parameter in the [Document Range method](doc:document-range) to capture the limits.  
- What if the document listed emails, and you just wanted to capture all those emails? You could use a regular expression (regex) in a `"match":"all"` anchor coupled with a [Passthrough method](doc:passthrough), or the [Regex method](doc:regex).
- You can split the policy period into two dates, either by using the [Split computed field method](doc:split), or by setting the [Date](doc:types#date) type on the field and using a tiebreaker.

To check out other methods, see [Methods](doc:methods).

Test the config
====

Before integrating the config with an application and writing [validation tests](doc:validate-extractions) against it, double check the config by uploading another quote.

1. Repeat the steps in the previous section to upload a second generic car insurance quote:

   | auto_insurance_anyco_2 | [Download link](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_2.pdf) |
   | ----------------------------- | ------------------------------------------------------------ |

2. Click the **anyco** config, select the "auto_insurance_anyco_2" PDF, and look at the output. Unlike the first document, the policy period takes up two lines, so Sensible misses the end year (2021):

   ```json
   {
     "policy_period": {
       "type": "string",
       "value": "May 20, 2021 - Nov 20,"
     }
   ```

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_error_1.png)

That seems like sloppy PDF formatting, but let's work with it. There are several options for capturing the policy period reliably, including:  

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

Let's double check that this region also works with the first PDF:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_error_4.png)

Yes, it works too.

3. Click **Publish** and choose **Production** to save your changes to the config.

In a production scenario, continue testing PDFs until you have confidence your configs work with the PDF document type you've defined.  Then, write tests to validate the extractions in production.

Integrate with your application
====

When you're ready to integrate with your application, enable using the config with the Sensible API by taking the following steps:

1. Click **Publish**.  The config is still a work in progress, so click **Development**.  Now you can use the query parameter `env=development`  to test the integration before you go to production:![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_publish_config.png).
2.  use the [Sensible API](https://docs.sensible.so/reference) to integrate with your application. If you're new to APIs, then see [Try asynchronous extraction from your URL](doc:api-tutorial-async-1) for a tutorial. 

Validate extractions in production 
====

In a previous section, you tested a couple of PDFs manually. Now it's time to scale up and quality control the extractions by writing tests that run for all API extractions in a doc type.

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



5. To test the validations with a PDF that's missing information, [try out an API call](doc:api-tutorial-async-1) with the following example PDF that has these errors:

   -  the policy number is missing
   -  the property damage liability premium is $200 more than the comprehensive premium

| auto_insurance_anyco_3 | [Download link](https://github.com/sensible-hq/sensible-docs/blob/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_3.pdf) |
| ----------------------------- | ------------------------------------------------------------ |

You should receive a response with errors and warnings in the Validations array, as show in the following API response excerpt:

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
