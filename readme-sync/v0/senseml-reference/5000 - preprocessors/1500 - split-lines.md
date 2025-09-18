---
title: "Split lines"
hidden: false
---

Splits lines distributed along a horizontal axis. This preprocessor is most useful for typewriter-style documents that use whitespaces for formatting. 

Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| key                      | value                                                 | description                                                  |
| ------------------------ | ----------------------------------------------------- | ------------------------------------------------------------ |
| type (**required**)      | `splitLines`                                          | splits lines distributed along a horizontal axis.            |
| minSpaces (**required**) | number                                                | The number of consecutive whitespace characters (`&#x20;`) at or above which to split lines. |
| separator                | string                                                | Modifies the Min Spaces parameter to split on the specified character, for example "-", instead of the default whitespace character. For example, if you specify `"-"` for this parameter and `2` for the Min Spaces parameter, then Sensible splits lines when it finds `--`. |
| match                    | A [Match](doc:match) object or array of Match objects | If specified, Sensible runs the Split Lines preprocessor on pages containing the matched text and ignores all other pages. For example, use this parameter to target typewritten pages in a document that otherwise contains pages with digital fonts. |

Examples
====

The following example shows solving undersplit lines in a "typewritten" style document. The Split Lines preprocessor preserves columns and rows in this document.

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

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/split_lines.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/split_lines.pdf) |
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

