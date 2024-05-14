---
title: "Troubleshoot LLM extractions"
hidden: true
---

See the following tips for troubleshooting situations in which large language model (LLM)-based extraction methods return inaccurate responses, nulls, or errors.

### Fix error messages

**Error message**

```
ConfigurationError: LLM response format is invalid
```

**Notes**

Reword the description in simpler terms, and refrain from including the word "return" in your prompts, if possible. Or, add a fallback query to bypass the error if the original query is working for some documents and you're only seeing the error intermittently. See the following section for more information.

Background: Sensible returns this error when the LLM doesn't return its response in the JSON format that Sensible specifies in [full prompts](doc:prompt). This can occur when your `description` parameters prompt the LLM to return data in a specific format that conflicts with the expected JSON format.

### Interpret confidence signals

Confidence signals are an alternative to confidence scores and to error messages. For information about troubleshooting LLM confidence signals, such as `multiple_possible_answers` or `answer_maybe_be_incomplete`, see [Qualifying LLM accuracy](doc:confidence).

### Create fallbacks for null responses

Sometimes an LLM prompt works for the majority of documents in a document type, but returns null for a minority of documents. Rather than rewrite the prompt, create fallback prompts targeted at the failing documents.

To create fallback prompts:

TODO

### Locate source text

Locating the source text, or [context](doc:prompt#notes), for an LLM's answer can help you determine if the LLM is misinterpreting the correct text, or targeting the wrong text.

To view the source text for an LLM's answer:

- You can view the source text for an LLM's answer highlighted in the document for the Query Group method. In the Sensible Instruct editor, click the **Location** button in the output of a query field to view its source text in the document. For more information about how location highlighting works and its limitations, see [Location highlighting](doc:query-group#notes).

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/location.png)

- To troubleshoot locating a group's context in the document, ensure that the Page Hinting parameter is enabled, then add location information to a prompt in a group. For more information about the Page Hinting parameter, see [Advanced prompt configuration](doc:prompt).

  **Location relative to page number and position on page**

  - "address in the **top left of the first page** of the document"

  - "What is the medical paid value on the **last claim of the second page**?"

  - "consumer electronics device with highest sales mentioned **near end of document**"

    **Location relative to content in document**

  - "total amount **in the expense table**"

  - "phone number after **section 2**"
