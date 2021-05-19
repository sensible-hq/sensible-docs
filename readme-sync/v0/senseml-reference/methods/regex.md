---
title: "Regex"
hidden: false
---
Returns lines matching a regular expression. 

Parameters
-----

**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key                    | value                                  | description                                                  |
| ---------------------- | -------------------------------------- | ------------------------------------------------------------ |
| id (**required**)      | `regex`                                |                                                              |
| pattern (**required**) | Javascript-flavored regular expression | If the regular expression has capturing groups (for example, `([0-9])([a-z])`, Sensible return the contents of the **first** capturing group (in the preceding example, a single numeric character). Otherwise, Sensible returns the full contents of the matched line.  Note you have to double escape characters, since the regex is contained in a JSON object (for example, `\\s` not `\s` to represent a whitespace character). |
| flags                  | JS-flavored regex flags, default: none | Flags to apply to the regex. for example: "i" for case-insensitive, "g", "m", etc. |
| stop                   | Match object. default: none            | A Match object to stop extraction. Not included in the method output.  If unspecified, matches to end of document. |



Notes
---

Regular expressions are also supported in **anchor** matches.  For an example, see the [Passthrough method](doc:passthrough).