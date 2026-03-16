---
title: January 2025
slug: january-2025
date: 2025-01-02
---

In the last month, Sensible released a powerful new feature for chaining large language model (LLM) prompts together, enabled "magic links" for reviewing extracted document data without a Sensible account, and made UX improvements.

## New feature: Chain LLM prompts for the Query Group method

With the Query Group's new [Source IDs](doc:query-group#parameters)  parameter, you can prompt a large language model (LLM) to extract or transform data from another field's extracted output. For example, if you extract a field `_checking_transactions` and specify it in the Query Group's Source IDs parameter, then Sensible searches for the answer to `what is the largest transaction?` in `_checking_transactions`, rather than searching the whole document to locate the [context](doc:prompt#notes).

Using the Source IDs parameter, you can prompt an LLM to:

* Reformat or otherwise transform the outputs of other fields.
* Compute or generate new data from the output of other fields.
* Narrow down the context for your prompts to a specific part of the document.
* Troubleshoot or simplify complex prompts that aren't performing reliably. Break the prompt into several simpler parts, and chain them together using successive Source ID parameters in the fields array.

The Query Group's Source IDs parameter deprecates the [Summarizer](doc:deprecated-summarizer) method.

## New feature: Review extracted data via magic links without a Sensible account

By implementing a new [Auth Token](ref:account-auth-tokens) endpoint, you can provide "magic links" to your reviewers to review, edit, approve, or reject extracted document data without logging into a Sensible account. This feature enables you to implement easier human-in-the-loop flows for your document processing. For example, if you're a proptech company processing mortgage application documents, you might have a UI for your employees to perform mortgage-related tasks. Now you can add a link in that UI to each document extraction that failed the quality criteria you configured in Sensible. Your employees can click each link, review, and correct the extracted data without logging into a Sensible account, then be redirected back to your UI via a callback URL when they approve or reject the extraction. 

For a detailed implementation tutorial, see [How to automate human-in-the-loop review for document processing](https://www.sensible.so/blog/human-review-document-processing). 

## Improvement: Extract 100-page lists

You can now extract lists up to 100 pages from documents using the new Long value for the LLM Engine parameter on the [List](doc:list#parameters)  method. If you set this value, then Sensible can output lists extracted from up to 100 potentially nonconsecutive, 1-page source chunks. Otherwise Sensible by default extracts from 20 1-page chunks. If the list in the document is longer than the number of source chunks, Sensible truncates the list. 

## UX improvement: Boolean type for LLM-based methods in visual editor

 You can now specify the [Boolean](doc:types#boolean)  type for LLM-based fields in the visual editor, in addition to specifying this and other types in the JSON editor. Note the JSON editor offers a superset of the functionality in the visual editor.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/changelog_jan2025_boolean.png)
