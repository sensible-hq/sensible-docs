---
title: "phone no"
hidden: true
---
TODO: add link  to field-query-object page

[Phone Number](doc:types#phone-number)



Phone Number
----

Returns phone numbers:

- Recognizes USA 10-digit phone numbers either with or without a country calling code. May be optionally formatted with parentheses, dashes, spaces, plus sign (+), or periods. 

- Recognizes international phone numbers only if prefixed by a country calling code (for example, +91 for India).

Examples: 

```
1-888-353-9578
+18883539578
888.353.9577
888 353 3264
888 353-3232
(207) 312-6767
+91 9999999999
+91 9999 999999
+91 9999-999999

```

Example output:


```json
{
    "type": "phoneNumber",
    "source": "(855) 786-3246",
    "value": "+18557863246"
}
```

This type does *not* recognize country calling codes formatted with 00, for example, 0091 or 001. 
