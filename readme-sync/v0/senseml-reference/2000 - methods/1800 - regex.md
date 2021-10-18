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


| key                    | value                                          | description                                                  |
| ---------------------- | ---------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `regex`                                        | The anchor line is included in this method's output.        |
| pattern (**required**) | Javascript-flavored regex                      | If the regular expression has capturing groups (for example, `([0-9])([a-z])`, Sensible returns the contents of the **first** capturing group (in the preceding example, a single numeric character). Otherwise, Sensible returns the full contents of the matched line. Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s` not `\s` to represent a whitespace character). |
| flags                  | Javascript-flavored regex flags. default: none | Flags to apply to the regex. For example, "i" for case-insensitive. |
| stop                   | Match object. default: none                    | A Match object to stop extraction. Not included in the method output. If unspecified, matches to the end of the document. |

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

**PDF**
The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/regex.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/regex.pdf) |
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

- Regular expressions are also supported in **anchor** matches. For an example, see the [Passthrough method](doc:passthrough).

- If the target data contains separator characters (for example, whitespaces in a credit card number) then you can use the  [Split method](doc:split) as an alternative to the Regex method.

  