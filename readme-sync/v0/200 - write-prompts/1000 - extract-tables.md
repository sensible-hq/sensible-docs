---
title: "Writing prompts"
hidden: false
---

In this tutorial, you'll learn to extract data from a set of similar documents using an AI-powered visual authoring tool, Sensible Instruct. You'll write natural-language prompts to extract:

- tables
- lists
- single data points.

Sensible uses large-language models (LLMs) such as GPT-4 to extract your target information.

You can then save your descriptions as an extraction configuration, or "config." Publish your config to automate extracting from similar documents.  

Use this tutorial if you want a guided tour of configuring AI-powered document extractions in the Sensible app. Or see the following links:

- TODO REWRITE THIS STUFF? You can mix and match Sensible Instruct methods with SenseML methods for advanced config authoring. SenseML is a superset of Sensible Instruct. For more information about SenseML versus Sensible Instruct, see [Choosing extraction approach](doc:author). For authoring in SenseML, see [Getting started with SenseML](doc:getting-started).
- If you want to explore without much explanation, [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app example extractions. For links to the examples, see [AI-powered resources](doc:no-code).

## Extract a table

To extract a table from an example document, take the following steps:

REWRITE: NAVIGATE TO TODOLINK

1. Click  **Table**.

2. Configure the table extraction using the following screenshot and instructions:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_4.png)

| Field name                  | Method | Overall table description     | Column IDs and descriptions                                                                              |
| --------------------------- | ------ | ----------------------------- | -------------------------------------------------------------------------------------------------------- |
| savings_transaction_history | Table  | "savings transaction history" | **date** - "date"<br/><br/>**description** - "description without totals"<br/><br/>**amount** - "amount" |

Click the **Send** icon for each column.

3. To verify the extracted data, scroll down in the right pane and compare the **Extracted data** section to the document in the left pane:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_5.png)

4. (**Optional**) To standardize the representation of the extracted dates and dollar amounts, configure `date` and `currency` types as shown in the following screenshots:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_6.png)

   You should see that the formatting of the extracted data changes according to the types you specified. For example, Sensible reformats the date `04/11/23` to a standardized output format, `2023-04-11`:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_7.png)

# TODO: add LIST method

# TODO: add an advanced param??

# (Optional) Extract more data

Try extracting other pieces of information using what you learned in previous steps, such as:

- The bank address or customer address
- The Spanish-speaking customer service phone number
- The time period for each account. **Hint:** To extract repeating data that isn't in table format, use the [List method](doc:list). For example, in this config, the `accounts_list` uses the List method.

When you're done making changes, publish the config to save your changes.

WHAT"S NEXT?

# Extract using our library

(lil plug or config library and for SenseML)

# Extract from your own documents

TODO: does 'author your own configs' belong in 'extras' and I link out to it??

Congratulations! You've created a reusable extraction prompt, or "config", and extracted your first example document data. 

- Or, create a new config for your custom documents:

  - In the [**Document Types**](https://app.sensible.so/document-types/) tab, Click **New document type**  to create a new document type and name  it. Leave the defaults and click **Create**.

  - In the document type's **Reference documents** tab, upload an example of the type of PDF document you want to extract from.

  - In the document type's **Configurations** tab, create a new test configuration, and click the configuration you created to edit it.

  - Click **Sensible Instruct** and create fields to extract data using what you've learned in this guide.

### Author your own configs

TODO: should HAVE some sort of guidance about creating document types --> look at the sensible config library and list some types??