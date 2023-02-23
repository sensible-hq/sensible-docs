---
title: "Question"
hidden: true

---

Extracts the answer to a free-text question.  This method is a beta release. This method is powered by GPT-3.

[**Parameters**](doc:question#parameters)
[**Examples**](doc:question#examples)

Parameters
=====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| key                     | value      | description                                                  |
| :---------------------- | :--------- | :----------------------------------------------------------- |
| id (**required**)       | `question` | The Anchor parameter is optional for fields that use the Question method. If you specify an anchor, Sensible ignores it. TODO: true? |
| question (**required**) | string     | A free-text question about information in the document. For example, `"what's the policy period?"` or `"what's the client's first and last name?"`.  For more information about how to write questions (or "prompts"), see [GPT-3 Completions documentation](https://beta.openai.com/docs/guides/completion/introduction). |

Examples 
====

**Config**

```json

```

**Example document**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/question.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |



**Output**

```json

```



Notes
===

For an overview of how this method works, see the following steps:

- Since GPT-3 has an input character limit, Sensible splits the document into equal-sized, overlapping chunks that are under the character limit.
- Sensible scores each chunk by how well it matches the question you pose about the data you want to extract. To create the score, Sensible compares your question against each chunk using an OpenAPI embedding API. 
- Sensible selects a number of the top-scoring chunks and combines them.
- Sensible inputs the combined chunks to GPT-3 as one context, and instructs it to answer the question based on the context.