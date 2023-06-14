---
title: "NLP"
hidden: true
---

TODO: do I want to link to the NLP preprocessor from the Question method? AND! 

Parameters
====

| key            | value            | description                                                  |
| -------------- | ---------------- | ------------------------------------------------------------ |
|                |                  |                                                              |
|                |                  |                                                              |
| pageHinting    | boolean.         | Turn on or off metadata about each page. So if you ask `What is the medical paid value on the last claim of the first page?` the LLM ignores the "first page" part(?) TODO: it removes the "page metadata" at each chunk<br/> DEFAULT HINTING: each chunk has info like `The excerpt starts at the top of page 1 and ends at the bottom of page 1.` |
| queryPrompt    | string. default: | Overwrites the default prepending to your prompt. default: `Answer the question as truthfully and concisely as possible using the provided context, and if the answer is not contained within the text below, say "I don\'t know."\n\nContext:\n\n'`<br/> For example:  `"Answer the question as truthfully and concisely as possible using the provided context, and if the answer is not contained within the text below, say \"Fblthp\"",`<br/>**Note** Sensible returns null for a field if the phrase `I don't know` is in the retured field value. If you alter this phrase, for example like `unknown` then you'll get that string back instead of null. TODO REWORD, add to each Prefix param? |
| listPrompt     | string           | Overwrites the default prepending to your prompt. default: `"Using the provided context fill out the table below. If the context doesn't contain any of the described items, leave it empty.\n\nContext:\n\n"` <br/>For example:<br/>`"Using the provided context fill out the table below. If the context doesn't contain any of the described items, just fill the table with four entries that say \"Cucumber.\""` |
| nlpTablePrompt | string           | Overwrites the default. the default instructions are: `Below is a sample table. Please transform the data from the sample table into the target table where the target table's column headers are provided. Please do not modify the target table's headers. If cells in the sample table don't contain data, leave the corresponding cell of the new table blank. Finally return the transformed table without the header and header seperator line.\n\n`<br/> For example, overwrite with:`"Below is a sample table. Please transform the data from the sample table into the target table where the target table's column headers are provided. Please do not modify the target table's headers. If cells in the sample table don't contain data, put the word \"Hippopotamus\" in those cells. Finally return the transformed table without the header and header seperator line."` |


Examples
====

Example 1
---

The following example shows using the NLP preprocessor to describe the context for each field in the config.

**Config**

```json
{
  "preprocessors": [
    {
      "type": "nlp",
      "contextDescription": "the following context is an excerpt from an ID card for a presidential pet."
    }
  ],
  "fields": [
    {
      "id": "pet_name",
      "method": {
        "id": "question",
        "question": "pet's name"
      },
      "type": "string"
    },
    {
      "id": "pet_owner",
      "method": {
        "id": "question",
        "question": "usa president who owned this pet"
      },
      "type": "string"
    },
    {
      "id": "tenure",
      "method": {
        "id": "question",
        "question": "for what date range was this pet in the white house"
      },
      "type": "string"
    }
  ],
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/nlp.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/nlp.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "pet_name": {
    "type": "string",
    "value": "Fala"
  },
  "pet_owner": {
    "type": "string",
    "value": "Franklin D Roosevelt"
  },
  "tenure": {
    "type": "string",
    "value": "1940 - 1945"
  }
}
```



