---
title: "Getting started"
hidden: false
---

# Introduction

Welcome! Sensible extracts structured data from documents, for example,  business forms in PDF format. 

Sensible uses an collection of prompts, or "config",  to extract data from a collection of similar documents that you send to Sensible, either through our app or through our API.

Sensible offers a platform for document data extraction:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform.png)

In this getting started guide, we'll look at using an LLM method to extract data from a bank statement. 

# Get data from a bank statement

Let's get started with Sensible Instruct! Sensible Instruct makes it easy to specify the data you want to extract from documents.

 In this guide, you'll:

- Extract data from an example PDF by prompting an LLM. 
- Publish your prompt.
- Test your prompt against a second, similar PDF to ensure it extracts the same target data.

# Get an account

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

# Configure the extraction

1. To view an example bank statement PDF extraction, navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement>. 

   You'll see a "config", or list of prompts for extracting from the example document (in the left pane), and extracted data in the right pane.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_1.png)

2. Take the following steps to edit the config to extract more data from the document.

## Extract an account number from a bank statement

3. To extract a single data point from the document, click **Query**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

- Edit the query as shown in the following screenshot by entering `checking account number (not savings)` in the query field. Give the query an ID, `account_num_checking` then click the **Send** icon:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_3.png)

- You should see the extracted account number, `8347-3248`, populate in the **Extracted data** section.
- Click **Back to fields**.

Congratulations! You extracted the checking account number from the bank statement.

# Publish the extraction configuration TODO: or test the prompt?

Now let's publish the prompt you created so you can use it to extract checking account numbers from other bank statement documents. You'll be publishing the "config" that contains your prompt, as well as other example prompts.

To publish your config, click **Publish**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

# Test the prompt TODO: Test the extraction configuration?

Let's find out if the config containing your prompt works with other bank statements. To test the config against a second example document, take the following steps:

1. Navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement_2>. Notice that the document in the left pane changed, to a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)

2. In the right pane, scroll down to the fields you authored in previous steps. Verify that the extracted information automatically updated to reflect the second example document. For example, the account number updated from `8347-3248` to `987612345`: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_9.png)

It looks like your prompt was successful at extracting the checking account number from another document. Great! 

Now it's time to integrate and eventually scale up to extracting from many document using the same config. 

## Next

TODO: link to "integrating" topic.

## Out-of-the-box extractions

Evaluate if the documents you're interested in are already in our config library. if so move onto integrating. If not, see creating your own prompts. TODO: where does extraction approach fit into this? 

- Integrate
