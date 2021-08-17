---
title: "Passthrough"
hidden: false
---
Use the Passthrough method to grab a line or lines of text using an anchor, and return the match or matches directly. This can be useful when you want to match using regular expressions, and you don’t want to take any additional steps after finding your matches. 

[**Parameters**](doc:passthrough#section-parameters)
[**Examples**](doc:passthrough#section-examples)
[**Notes**](doc:passthrough#section-notes)

Examples
====

The following example config uses regular expressions to grab a list of forms that are all identified by four digits (i.e., "Form 1099") in a W-9 form. It defines a range to look in with  `start` and `stop` text. Since the data we were looking for is already matched by the anchor, we don't need a Method object. To ignore the Method object, we set the method id to  `"passthrough"`. 

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

The following image shows this example in the Sensible app:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/passthrough_regex.png)

Parameters
====

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.

| id                | value         | description                                           |
| ----------------- | ------------- | ----------------------------------------------------- |
| id (**required**) | `passthrough` | bypass the Method object, and return an anchor. <br/> |

Notes
-----

Often, you use the Passthrough method in conjunction with an anchor that matches using regular expressions. Because anchor matches do not support regex capturing groups, the Passthrough method returns the full contents of the matched line. If you want instead to use a capturing group to return only part of a matching line, see the [Regex method](doc:regex).