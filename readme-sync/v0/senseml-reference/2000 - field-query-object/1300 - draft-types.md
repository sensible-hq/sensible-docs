---
title: "Types"
hidden: true
---


Name
-----

You can define the Name type using concise syntax, `"type":"name"`, or you can use expanded syntax and configure the following parameters:

**Parameters**

| key               | value                                           | description                                                  |
| ----------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| id (**required**) | `name`                                          |                                                              |
| capitalization    | `allCaps`, `firstLetter`. default: `firstLeter` | Recognize names in all uppercase, or names with the first letter capitalized. |



Returns one or more names. Doesn't recognize a list of names more than 6 lines long. 

Recognizes names of the formats below, and variant representations of these elements such as abbreviations. Configure the Capitalization parameter to recognize the following formats where all letters are uppercase:

\- First Last
\- First1 Last1 and First2 Last2
\- Last, First1 and First2
\- First1 and First2 Last



**Example input**

```json
John R. Smith
JOHN R. SMITH
Richard & Ann Spangenberg
DuBois, Renee and Lois 



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



**Example input**

The following are examples of date formats that Sensible recognizes by default:

```
5/17/2018
november 30, 1955
Feb 1, 21
June 7th, 2021
Jan 9th, 09

```

**Example output**

```json
{
    "source": "Feb 1, 21",
    "value": "2021-02-01T00:00:00.000Z",
    "type": "date"
}

```

