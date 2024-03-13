---
title: "Regex"
hidden: false
---
Extracts lines matching a regular expression. Often, you use a capturing group in this method to narrow down text you matched in an anchor. 

[**Parameters**](doc:regex#parameters)
[**Examples**](doc:regex#examples)
[**Notes**](doc:regex#notes)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.


| key                    | value                                                 | description                                                  |
| ---------------------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `regex`                                               | Specifies to include the anchor line in the method's output. |
| pattern (**required**) | Javascript-flavored regex                             | Returns the first capturing group. To capture more than one group, you can use one field for each group, then concatenate them with the [Concatenate](doc:concatenate) computed field method. <br/>Double escape special characters since the regex is in a JSON object. For example, `\\s`, not `\s` , to represent a whitespace character.<br/>Sensible throws an error if you specify a pattern that can match an empty string, for example, `.*`. |
| flags                  | Javascript-flavored regex flags. default: none        | Flags to apply to the regex. For example, "i" for case-insensitive. |
| stop                   | Match object or array of match objects. default: none | Stops extraction at the matched line. Matched line isn't included in the method output. If unspecified, matches to the end of the document. |

Examples
====

The following example narrows down text matched by an anchor line by using the Regex method. The Regex method extracts the last four digits in a customer ID.

**Config**

```json
{
  "fields": [
    {
      "id": "last_4_digits_customer_id",
      "type": "number",
      "anchor": {
        "match": [
          {
            "type": "startsWith",
            "text": "customer id"
          },
          {
            "type": "regex",
            "pattern": "^[A-Z]{4}\\d{4}$",
          }
        ]
      },
      "method": {
        "id": "regex",
        "pattern": "\\d{4}$"
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/regex.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/regex.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
{
  "last_4_digits_customer_id": {
    "source": "7890",
    "value": 7890,
    "type": "number"
  }
}
```



Notes
====

Alternatives to this method include the [Passthrough method](doc:passthrough) with a custom type. For example, for the preceding example document, the following config returns similar output:

```json
{
  "fields": [
     {
      "id": "last_4_digits_customer_id",
      "anchor": {
        "match": [
          // find an 8-character ID that follows the line
          // 'customer id'
          {
            "type": "startsWith",
            "text": "customer id"
          },
          {
            "type": "regex",
            "pattern": "^[A-Z]{4}\\d{4}$",
          }
        ]
      },
      // custom type outputs last 4 digits of the id
      "type": {
        "id": "custom",
        "pattern": "^[A-Z]{4}(\\d{4})$",
        "type": "last_4_digits"
      },
      "method": {
        "id": "passthrough"
      }
    }
    ]
}
```

The preceding config returns:

```json
{
  "last_4_digits_customer_id": {
    "source": "ABCD7890",
    "value": "7890",
    "type": "last_4_digits"
  }
}
```



