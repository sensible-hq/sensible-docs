---
title: "Rotate page"
hidden: true
---

Rotates page so that a matched anchor becomes horizontal. Use this when Sensible's default rotation handling behavior fails to rotate a page, usually because the page contains a mix of horizontally and vertically oriented text.  If the page is both rotated and skewed, use the Deskew preprocessor.

Parameters
====

| key                 | value                                  | description                                                  |
| ------------------- | -------------------------------------- | ------------------------------------------------------------ |
| type (**required**) | `rotatePage`                           | Rotates page by up to 90 degrees. TODO more,, what if it's not quite at 90? |
| match               | Match object or array of Match objects | See [Match object](doc:match)                                |
| matchAll            | boolean                                | If true, rotates all pages containing the line specified by the Match parameter. |

Examples
====

The following image shows that without the Rotate page preprocessor, extraction from a rotated PDF fails. The Label method returns null, because the targeted text  isn't in the expected position (`right` ):

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_1.png)

To solve this problem, define a text match that you want to be horiztonal, and Sensible rotates the page accordingly:

**Config**

```json
{
  "preprocessors": [
    {
      "type": "rotatePage",
      "match": "first dog ID card"
    }
  ],
  "fields": [
    {
      "id":"pet_name",
      "anchor": "name:",
      "method":
      {
        "id":"label",
        "position":"right"
      }
    }
  ]
}
```

**Example document**

The following images show the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/rotate_page_2.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/rotate_page.pdf) |
| ------------------------------------------ | ------------------------------------------------------------ |

**Output**

```json
{
  "pet_name": {
    "type": "string",
    "value": "Pushinka"
  }
}
```

Notes
----

- 