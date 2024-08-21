---
title: "Passthrough"
hidden: false
---
Use the Passthrough method to match text using an anchor, and return the anchor match or matches directly. For example, this can be useful when you want to match using regular expressions, and you don’t want to take more extraction steps after finding the matches. 

[**Parameters**](doc:passthrough#parameters)
[**Examples**](doc:passthrough#examples)
[**Notes**](doc:passthrough#notes)


Parameters
====

**Note:** For additional parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.

| id                | value         | description                                                  |
| ----------------- | ------------- | ------------------------------------------------------------ |
| id (**required**) | `passthrough` | bypass the Method object, and return the output of the anchor's Match parameter. <br/> |

Examples
====

The following example uses regular expressions to extract a list of forms with four-digits identifiers (for example, "Form 1099") in a W-9 form. It defines a range to look in with  `start` and `stop` text. Since the anchor already matches the target data, further extraction steps using a Method object are unnecessary. To ignore the Method object, set the method id to  `"passthrough"`. 

**Config**

```json
{
  "fields": [
    {
      "id": "forms_with_4_numbers",
      "match": "all",
      "anchor": {
        "start": {
          "type": "startsWith",
          "text": "General Instructions",
          "isCaseSensitive": true
        },
        "match": {
          "type": "regex",
          "pattern": "Form [0-9]{4}"
        },
        "end": "Rev. 10-2018"
      },
      "method": {
        "id": "passthrough"
      }
    }
  ]
}
```

**Example document**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/passthrough.png)

| Example document | [Download link](https://www.irs.gov/pub/irs-pdf/fw9.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**
```json
{
  "forms_with_4_numbers": [
    {
      "type": "string",
      "value": "• Form 1099-DIV (dividends, including those from stocks or mutual"
    },
    {
      "type": "string",
      "value": "• Form 1099-MISC (various types of income, prizes, awards, or gross"
    },
    {
      "type": "string",
      "value": "• Form 1099-B (stock or mutual fund sales and certain other"
    },
    {
      "type": "string",
      "value": "• Form 1099-S (proceeds from real estate transactions)"
    },
    {
      "type": "string",
      "value": "• Form 1099-K (merchant card and third party network transactions)"
    },
    {
      "type": "string",
      "value": "• Form 1098 (home mortgage interest), 1098-E (student loan interest),"
    },
    {
      "type": "string",
      "value": "• Form 1099-C (canceled debt)"
    },
    {
      "type": "string",
      "value": "• Form 1099-A (acquisition or abandonment of secured property)"
    },
    {
      "type": "string",
      "value": "• Form 1099-INT (interest earned or paid)"
    }
  ]
}
```




Notes
===

Often, you use the Passthrough method in combination with regular expressions. Because anchors don't support regex capturing groups, the Passthrough method returns the full contents of the matched line. If you want instead to use a capturing group to return part of a matched line, see the [Regex method](doc:regex).