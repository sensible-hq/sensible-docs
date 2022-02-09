---
title: "Types"
hidden: true
---


Name
-----

You can define the Name type using concise syntax, `"type":"name"`, or you can use expanded syntax and configure the following parameters:

**Parameters**

| key               | value                                                        | description                                                  |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**) | `name`                                                       |                                                              |
| capitalization    | `allCaps`, `firstLetter`. default: no change to source capitalization | Formats the output in all uppercase, or with only the first letter of each word capitalized. |



Returns one or more names. Doesn't recognize a list of names more than 6 lines long. 

Recognizes names of the formats below, and variant representations of these elements such as abbreviations. 

\- first last
\- first1 last1 and first2 last2
\- last, first1 and first2
\- first1 and first2 last



**Example input**

```json
John R. Smith Sr
Richard & Ann Spangenberg
DuBois, Renee and Lois 
```

This type does **not** recognize lists of three or more names such as `last1, last2, & last3`

Example output:

```json
{
  "source": "Richard & Ann Spangenberg",
  "type": "name",
  "value": [
      "Richard Spangenberg",
      "Ann Spangenberg"
}
```



