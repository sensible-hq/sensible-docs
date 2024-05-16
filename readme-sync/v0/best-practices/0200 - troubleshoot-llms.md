---
title: "Troubleshooting LLM extractions"
hidden: false
---

See the following tips for troubleshooting situations in which large language model (LLM)-based extraction methods return inaccurate responses, nulls, or errors.

### Fix error messages

**Error message**

```
ConfigurationError: LLM response format is invalid
```

**Notes**

Reword the prompt in simpler terms, and avoid specifying a format in the prompt for the extracted data. Or, add a fallback field to bypass the error if the original query is working for most documents and you're only seeing the error intermittently. See the following section for more information about fallbacks.

Background: Sensible returns this error when the LLM doesn't return its response in the JSON format that Sensible specifies in the backend for [full prompts](doc:prompt). This can occur when your `description` parameters prompt the LLM to return data in a specific format that conflicts with the expected JSON format.

### Interpret confidence signals

Confidence signals are an alternative to confidence scores and to error messages. For information about troubleshooting LLM confidence signals, such as `multiple_possible_answers` or `answer_maybe_be_incomplete`, see [Qualifying LLM accuracy](doc:confidence).

### Create fallbacks for null responses or false positives

Sometimes an LLM prompt works for the majority of documents in a document type, but returns null or an inaccurate response (a "false positive") for a minority of documents. Rather than rewrite the prompt, which can cause regressions, create fallbacks targeted at the failing documents.

### Trace source context

Tracing the document's source text, or [context](doc:prompt#notes), for an LLM's answer can help you determine if the LLM is misinterpreting the correct text, or targeting the wrong text.

You can view the source text for an LLM's answer highlighted in the document for the Query Group method:

- In the Sensible Instruct editor, click the **Location** button in the output of a query field to view its source text in the document.  For more information about how location highlighting works and its limitations, see [Location highlighting](doc:query-group#notes).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/location.png)

- In the SenseML editor, Sensible displays location highlighting by outline the context with [blue boxes](doc:color). 

### Specify source context

Sometimes, an LLM fails to locate the relevant portion of the document that contains the answers to your prompts. To troubleshoot locating [context](doc:prompt#notes) in the document:

- For the Query Group method, add more prompts to the group that target information in the context, even if you don't care about the answer. For the List and NLP Table methods, add prompts to extract each item in the list or column in the table, respectively. 

- If the context occurs consistently in a page range in the document, use the Page Hinting or Page Range parameters to narrow down the context's possible location. For more  information about these parameters, see [Advanced prompt configuration](doc:prompt).  

