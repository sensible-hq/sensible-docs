---
title: "Welcome"
hidden: true
---

Welcome to Sensible's documentation! Sensible extracts structured data from documents, for example PDFs of business forms.

Check out the following use cases and roles for where to get started.

Use cases
====

| extract from these documents                                 | topics                                                       | notes                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Common business documents, including:<br/><br/>- home, renters, and auto insurance declarations<br/>- pay stubs<br/>explanations of benefits<br/>-  tax forms | [Extract sample data](doc:excel-quickstart)                  | Choose from our library of pre-built parsers to extract data from an example 1040 tax form. |
| Excel documents                                              | [Convert to spreadsheet](doc:excel-quickstart#convert-to-spreadsheet) | Convert extracted document data to Excel as tables, labeled columns, and linked sheets. |
| Free-text documents, for example contracts or research documents | [How to use GPT-3 to parse free-text documents](https://www.sensible.so/blog/how-to-use-gpt-3-to-parse-free-text-documents)<br/><br/>[Summarizer method](doc:summarizer) | Walk through a guided tutorial on extracting key info from a lease, or take a look at  the reference docs. |



Roles
===

Non-developer
-----

| goals                                            | topics                                          | notes                                                        |
| ------------------------------------------------ | ----------------------------------------------- | ------------------------------------------------------------ |
| Extract document data using the Sensible web app | [Sensible walkthrough](doc:ui)                  | Tour of the Sensible  web app.                               |
| Convert PDF docs into Excel spreadsheets         | [Quickstart PDF to Excel](doc:excel-quickstart) | Get started in minutes using pre-built parsers for common business documents. |
| Make minor edits to extraction configurations    | [Getting started guide](doc:getting-started)    | Get started learning SenseML concepts                        |
| Set up low-code workflows                        | [Zapier overview](doc:zapier)                   | Automate sending document data to other destinations, such as emails or databases |




Developer
-----

| goals                                              | topics                                                       | notes                                                        |
| -------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Test the API                                       | [Developer Quickstart](doc:quickstart)                       | Hello world                                                  |
| Explore the API                                    | [API reference](reference:choosing-an-endpoint)              | Interactive API reference and Postman collection.            |
| Extract from custom doc types                      | [extract_your_first_data](https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data)<br/>[tables and rows](https://app.sensible.so/editor/?d=senseml_basics&c=2_tables_and_rows&g=2_tables_and_rows)<br/> [checkboxes, paragraphs, and regions](https://app.sensible.so/editor/?d=senseml_basics&c=3_checkboxes_paragraphs_and_regions&g=3_checkboxes_paragraphs_and_regions)<br/>  [blank-slate challenge](https://app.sensible.so/editor/?d=senseml_basics&c=4_extract_from_scratch&g=4_extract_from_scratch) | Learn SenseML with interactive tutorials                     |
| Tweak existing extraction configs                  | [SenseML reference introduction](doc:senseml-reference-introduction) | Explore the full SenseML reference                           |
| Test in dev                                        | [Test before integrating](doc:test-before-integrating-configs) | Test extraction configurations before going live             |
| Integrate with your toolchain and go to production | [Zapier overview](doc:zapier)<br/>[Code examples](doc:examples) | Integrate using Zapier,  or leverage code samples to integrate with your codebase |


QA and testing
----

| Goal                      | topics                                               | notes                                                        |
| ------------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| Validate extractions      | [Validate extractions](doc:validate-extractions)     | Trigger errors about incorrectly extracted data by writing rules. |
| Troubleshoot API response | [Troubleshoot](doc:troubleshoot)                     | Get verbose API output.                                      |
| Performance tips          | [Optimizing extraction performance](doc:performance) | Speed up extraction.                                         |



