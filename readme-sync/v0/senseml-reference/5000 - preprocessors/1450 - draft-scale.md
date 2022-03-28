---
title: "Scale"
hidden: true
---



Parameters
====

| key                 | value            | description                                                  |
| ------------------- | ---------------- | ------------------------------------------------------------ |
| type (**required**) | `scale`          | For an example, see the Examples section.                    |
| samples             | array of objects | Array of example objects containing font heights for text matches in 100% scaled documents. Sensible compares the actual size of each match against the examples, then take an average of the ratios and use that to rescale the whole document. Sensible recommends choosing text matches for which the font height does not vary or that are unique in the document.<br/>Each example object has the following parameters:<br/> `match`: a [Match](doc:match) object<br/>`targetHeight`: the number in inches of the match at 100% scale. |
| perPage             | boolean          | If true, Sensible rescales each match found on each page individually against the Target Height parameter, rather than taking an average of all matches' heights. For example, if a tax return contains multiple W-2 forms, but each W-2 can unpredictably be scanned at a different scale, then you can set this parameter to true and match on large-font text such as the `"Wage and Tax"` title in the W-2 form. |

Examples
====

The following example shows:

- A repeating header with an incrementing page number. Sensible removes this from the direct text extraction.

  

  

**Config**

```json

```

**Example document**

TODO add in pic

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/scale.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json

```

