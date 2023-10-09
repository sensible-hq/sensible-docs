---
title: "Getting started"
hidden: false
---

Overview
---

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. It's highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large-language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful document primitives.



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/platform.png)

See the following list for an overview of going live with Sensible:

- **Learn** to extract data, or use out-of-the-box supported document types
- [**Integrate**](doc:integrate) using our API,  quick-extract UI, or other tools
- [**Quality control**](doc:validate-extractions) extracted data
-  [**Monitor**](doc:metrics) extracted data in production 

This guide gets you started with the first step in the preceding list.

# Learn to extract data

Let's get started with extracting document data from an example bank statement. We'll use a large-language model (LLM) prompt to extract a checking account number in minutes.

 In this guide, you'll:

- Extract data from an example PDF using a natural-language description of your target data 
- Publish your prompt as part of a "config".
- Test your config against a second, similar PDF to ensure it extracts the same target data.

# Get an account

1. Get an account at [sensible.so](https://app.sensible.so/register).  If you don't have an account, you can still read along to get a rough idea of how things work.

2. Log into the [Sensible app](https://app.sensible.so/signin/).

# Configure the extraction

1. To view an example bank statement PDF extraction, navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement>. 

   You'll see a "config", or list of prompts for extracting from the example document (in the left pane), and extracted data in the right pane.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_1.png)

Take the following steps to edit the config to extract more data from the document.

## Extract an account number from a bank statement

1. To extract a single data point from the document, click **Query**.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_2.png)

2. Edit the query as shown in the following screenshot by entering `checking account number (not savings)` in the query field. Give the query an ID, `account_num_checking`, then click the **Send** icon:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_3.png)

- You should see the extracted account number, `8347-3248`, populate in the **Extracted data** section.
- Click **Back to fields**.

Congratulations! You extracted the checking account number from the bank statement.

# Publish the prompt

Now let's publish the prompt you created so you can use it to extract checking account numbers from other bank statement documents. You'll be publishing the "config" that contains your prompt, including its other example prompts.

To publish your config, click **Publish**, click **Production**, then click **Publish to production**:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_10.png)

# Extract from a second document

Let's find out if the config containing your prompt works with other bank statements. To test the config against a second example document, take the following steps:

1. Navigate to <https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement_2>. Notice that the document in the left pane changed, to a statement for a different customer.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_8.png)

2. In the right pane, scroll down to the fields you authored in previous steps. Verify that the extracted information automatically updated to reflect the second example document. For example, the account number updated from `8347-3248` to `9876-12345`: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_instruct_9.png)

It looks like your prompt was successful at extracting the checking account number from another document. Great! 

# (Optional) Extract more data

Try extracting other pieces of information using what you learned in previous steps, such as:

- The customer's address
- The Spanish-speaking customer service phone number
- The time period for each account. **Hint:** Use the [List method](doc:list). For example, in this config, the `accounts_list` uses the List method.

When you're done making changes, publish the config to save your changes.

## Next

**Learn more about extracting**

- Explore extracting lists, tables, and single data points with interactive examples: 
  - [Bank statement](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=bank_statement&g=bank_statement)
  - [Resume](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=resume&g=resume&v=)
  - [Purchase contract](https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=contract&g=contract&v=)

- For advanced extraction strategies, see [Choosing an extraction approach](doc:author)

**Integrate**

- [Integrating](doc:integrate)



