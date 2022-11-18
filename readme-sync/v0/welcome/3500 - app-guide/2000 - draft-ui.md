---
title: "App overview"
hidden: true
---







Extracting from a new document
===

A brief overview of extracting information from an example bank statement doc type:

Configure the app
-----

1. Click **+ New** in the left pane to create a new document type, for example, "bank statements".
2. Click the new document type in the left pane.
3. Click **Create configuration** and name it, for example, "anyco_bank".
4. Click **Reference documents** and click **Upload document** to upload a reference PDF, for example, a typical bank statement from Anyco Bank.
   - (Optional) In the **Upload reference document** dialog, select the configuration you created. Now the Sensible app always displays this PDF by default when you edit the config.
7. For each company or format of bank statement you want to extract from, create another configuration. 

Write the extraction
-----

7. Click a new configuration to edit the SenseML and extract structured data from the PDF. For a tutorial, see [Getting Started](doc:getting-started).
8. (Optional) Click the **Validations** tab and write [validations](doc:validate-extractions).

View extractions
-----

9. Extract data from other bank statements using the [Sensible API](https://docs.sensible.so/reference), then check the extraction results in the app:
  - To view extractions for a document type, select the document type, then select the **Extractions** tab.
  - To view extractions for all document types, select **Recent extractions** in the left pane.

