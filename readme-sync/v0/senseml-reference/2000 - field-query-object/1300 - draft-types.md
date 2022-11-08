---
title: types
hidden: true
---

Custom
====

Defines a custom type using regular expressions. For example, define types for zip codes, time durations, customer IDs, and order numbers.

**Example syntax**

```
"type":
  {
    "id": "custom",
    "pattern": "Time\\:\\s*([0-9][0-9]:[0-9][0-9])",
    "type": "time_24_hr_military"
  }
```

**Example output**

This type outputs strings. For example:

```json
{
    "source": "Time: 14:01",
    "value": "14:01",
    "type": "time_24_hr_military"
  }
```

**Parameters**

| key                    | value                    | description                                                  |
| ---------------------- | ------------------------ | ------------------------------------------------------------ |
| id (**required**)      | `custom`                 |                                                              |
| pattern (**required**) | Valid JS regex           | Javascript-flavored regular expression. Returns the first capturing group. To capture more than one group, you can use one field for each group, then concatenate them with the [Concatenate](doc:concatenate) computed field method.<br/>Double escape special characters since the regex is in a JSON object. For example, `\\s`, not `\s` , to represent a whitespace character.<br/>Sensible doesn't validate regular expressions for custom types. |
| flags                  | JS-flavored regex flags. | Flags to apply to the regex. for example: "i" for case-insensitive. |
| matchMultipleLines     | Boolean. default: false  | If true, matches regular expressions that span multiple lines. To enable this behavior, Sensible joins the lines returned by the method using whitespaces as the separators, and runs the regular expression on the joined text.<br/>  `^` matches the start of the first line returned by the method, and `$` matches the end of the last line. For example,  `^[0-9 ]+$` matches all the joined text returned by the method, if all the characters are digits or whitespaces. |

