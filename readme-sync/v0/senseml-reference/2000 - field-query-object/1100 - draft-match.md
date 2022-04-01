---
title: "Match object"
hidden: true

---





Simple match
-------



**Parameters**

| *key*                                                        | *values*                                                | *description*                                                |
| ------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------------------------------------ |
| *text  (**required**)*                                       | *string*                                                | *The string to match*                                        |
| *type (**required**)*                                        | *`equals`, `startsWith`, `endsWith`, `includes`*        | *`equals`: The matching line must equal the string<br/>`startsWith`: Match at beginning of line<br/>`endsWIth`: Match at end of line<br/>`includes`: Match anywhere in line* |
| **editDistance** **TODO: verify not compatible with includes??** | integer. the number of allowed edits for a fuzzy match. | Configure this parameter to allow *fuzzy*, or approximate, string matching. This is useful for OCR text, like poor-quality scans or handwriting. For example, if you configure 3, then Sensible matches `kitten` in the document for `sitting` in the Text parameter.  Sensible implements fuzzy matching using [Levenshtien distance](https://en.wikipedia.org/wiki/Levenshtein_distance). Levenshtien distance is case sensitive, so even if you set `"isCaseSensitive":false`, the case of the string in the Text parameter can affect whether Sensible finds the match. <br/>Sensible recommends avoiding setting this parameter on short matches, like "A:" or "Sub", because an edit distance as low as 2 on a short match can result in a large number of of line matches and impact performance. |



**Example**

The following example shows setting the Edit Distance parameter for a poor-quality photographed document, so that the anchor  `6 City state and ZIP code` matches the incorrect OCR output of  `6 Chi state and ZIP code`. 



**Config**

```json
{
  "fields": [
    {
      "id": "simple_anchor",
      "anchor": {
        "match": {
          "editDistance": 3,
          "type": "startsWith",
          "text": "6 City state and ZIP code"
        }
      },
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/edit_distance.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/edit_distance_.pdf) |
| ----------- | ------------------------------------------------------------ |



**Output**

```json
{
  "simple_anchor": {
    "type": "string",
    "value": "SomeCity, NJ, $70101"
  }
}
```

