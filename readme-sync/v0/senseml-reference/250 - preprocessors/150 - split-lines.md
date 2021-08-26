---
title: "Split lines"
hidden: false
---

Use this preprocessor to split lines. This preprocessor is most useful for typewriter-style documents where whitespaces are used for formatting. 


Parameters
====

| key                   | value        | description                                                  |
| --------------------- | ------------ | ------------------------------------------------------------ |
| `type` (**required**) | `splitLines` |                                                              |
| minSpaces             | number       | The number of consecutive space characters (`&#x20;`) at or above which to split lines. |

Examples
====

The following image shows a "typewritten" style PDF in which the Split Lines preprocessor preserves columns and rows that are formatted with spaces:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/split_lines_example.png)

Without this preprocessor, the lines are merged too aggressively:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/split_lines_example_2.png)

Try out this example in the Sensible app using the following PDF and config:

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split_lines_example.pdf) |
| --------------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "preprocessors": [
    {
      "type": "splitLines",
      "minSpaces": 3
    }
  ],
  "fields": [
    {
      "id": "policy_number",
      "method": {
        "id": "row",
      },
      "anchor": "policy number",
    }
  ]
}
```



**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods).
