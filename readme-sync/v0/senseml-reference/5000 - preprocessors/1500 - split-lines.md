---
title: "Split lines"
hidden: false
---

Splits lines. This preprocessor is most useful for typewriter-style documents that use whitespaces for formatting. 

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                   | value        | description                                                  |
| --------------------- | ------------ | ------------------------------------------------------------ |
| `type` (**required**) | `splitLines` |                                                              |
| minSpaces             | number       | The number of consecutive space characters (`&#x20;`) at or above which to split lines. |

Examples
====

The following example shows solving undersplit lines in a "typewritten" style PDF. The Split Lines preprocessor preserves columns and rows in this document.

**PROBLEM**

Without the Split Lines preprocessor, Sensible merges the lines too aggressively:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/split_lines_2.png)

**SOLUTION**

**Config**

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

**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/split_lines.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split_lines.pdf) |
| --------------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "policy_number": {
    "type": "string",
    "value": "18-376-190"
  }
}
```

