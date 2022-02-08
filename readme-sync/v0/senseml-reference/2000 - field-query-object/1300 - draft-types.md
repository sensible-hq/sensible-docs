---
title: "Types"
hidden: true
---


Name
-----

You can define the Name type using concise syntax, `"type":"name"`, or you can use expanded syntax and configure the following parameters:

**Parameters**

| key               | value                                            | description                                                  |
| ----------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**) | `name`                                           |                                                              |
| capitalization    | `allCaps`, `firstLetter`. default: `firstLetter` | Recognize names in all uppercase, or names with the first letter capitalized. |



Returns one or more names. Doesn't recognize a list of names more than 6 lines long. 

Recognizes names of the formats below, and variant representations of these elements such as abbreviations. Configure the Capitalization parameter to recognize the following formats where all letters are uppercase:

\- First Last
\- First1 Last1 and First2 Last2
\- Last, First1 and First2
\- First1 and First2 Last



**Example input**

```json
John R. Smith Sr
JOHN R. SMITH SR
Richard & Ann Spangenberg
DuBois, Renee and Lois 
DUBOIS, RENEE AND LOIS



```

This type does **not** recognize text such as `Last1, Last2, & Last3`

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



