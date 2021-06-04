---
title: "Regex"
hidden: false
---
Returns lines matching a regular expression. Often, you use a capturing group in this method to narrow down some text in a line you matched in an anchor. 

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                    | value                                  | description                                                  |
| ---------------------- | -------------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `regex`                                | The anchor line is included in this method's match.          |
| pattern (**required**) | Javascript-flavored regular expression | If the regular expression has capturing groups (for example, `([0-9])([a-z])`, Sensible return the contents of the **first** capturing group (in the preceding example, a single numeric character). Otherwise, Sensible returns the full contents of the matched line.  Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s` not `\s` to represent a whitespace character). |
| flags                  | JS-flavored regex flags, default: none | Flags to apply to the regex. for example: "i" for case-insensitive, "g", "m", etc. |
| stop                   | Match object. default: none            | A Match object to stop extraction. Not included in the method output.  If unspecified, matches to end of document. |

Examples
====

The following example narrows down text that's matched in an anchor line (since capturing groups are supported only in the Regex method, not in anchors):



![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/regex_example.png)




```json
{
  "fields": [
    {
      "anchor": {
        "match": {
          "pattern": "^(19|20)\\d{2}$",
          "type": "regex",
          "minimumHeight": 0.2
        }
      },
      "id": "document_year",
      "type": "number",
      "method": {
        "id": "regex",
        "pattern": "^((19|20)\\d{2})$"
      },
    },
  ]
}
```



Notes
====

Regular expressions are also supported in **anchor** matches.  For an example, see the [Passthrough method](doc:passthrough).