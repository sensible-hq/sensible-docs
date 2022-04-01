---
title: "Scale"
hidden: true
---



Parameters
====

| key                 | value            | description                                                  |
| ------------------- | ---------------- | ------------------------------------------------------------ |
| type (**required**) | `scale`          | For an example, see the Examples section.                    |
| samples             | array of objects | Array of example objects containing font heights for text matches in 100% scaled documents. Sensible compares the actual size of each match against the examples, then take an average of the ratios and use that to rescale the whole document. Sensible recommends the following text match practices:<br>- Choose matches for which the font height does not vary.<br/>- Choose text that appears on each page, such as headers or footers.<br/>Each example object has the following parameters:<br/> `match`: a [Match](doc:match) object<br/>`targetHeight`: the number in inches of the match at 100% scale. |
| perPage             | boolean          | If true, Sensible rescales each page individually against the Target Height parameter, taking the average of  all matches' heights on that page rather than in the whole document. For example, if a tax return contains multiple W-2 forms, but each W-2 can be scanned at an unpredictable scale, then you can set this parameter to true and match on text such as the `"Wage and Tax"` and the `W-2` titles in the W-2 form. |

Examples
====

The following example shows using the Per Page parameter to scale an ID card that has a different size on each page, where the second page contains the target scale.

**Config**

```json
{
  "preprocessors": [
    {
      "type": "scale",
      "perPage": true,
      "samples": [
        {
          "match": {
            "type": "includes",
            "text": "First",
            "isCaseSensitive": true
          },
          "targetHeight": 0.22
        }
      ]
    }
  ],
  "fields": [
    
    {
      "id": "white_house_tenure",
      "anchor": "tenure",
      "match": "all",
      "method": {
        "id": "region",
        "start": "below",
        "offsetX": -1.7,
        "offsetY": 0,
        "width": 1.5,
        "height": 0.6
      }
    }
  ]
}
```

**Example document**

The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/scale.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/scale.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json
{
  "white_house_tenure": [
    {
      "type": "string",
      "value": "1940-1945"
    },
    {
      "type": "string",
      "value": "1940-1945"
    },
    {
      "type": "string",
      "value": "1940-1945"
    }
  ]
}
```

