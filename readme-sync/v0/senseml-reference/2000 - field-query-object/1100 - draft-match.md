---
title: "Match object"
hidden: true

---

Matches are instructions for matching lines of text in a document. They're  valid elements in anchors and other objects. 



See the following sections for more information:

[**Match types**](doc:match#match-types)

- [Global parameters](doc:anchor#global-parameters)
- [Simple match](doc:anchor#simple-match)
- [Regex match](doc:anchor#regex-match)
- [First match](doc:anchor#first-match)
- [Any match](doc:match#any-match)

[**Examples**](doc:match#examples)

- [Match arrays](doc:match#match-arrays) 



Match types
===

Global parameters
----

The following parameters are available to most types of Match objects:


| key           | values                  | description                                                  |
| ------------- | ----------------------- | ------------------------------------------------------------ |
| minimumHeight | number                  | The minimum height of the matched line's boundaries, in inches. Not valid as a top-level parameter for an Any match, but valid for individual matches in the Any match. |
| maximumHeight | number                  | The maximum height of the matched line's boundaries, in inches.  Not valid as a top-level parameter for an Any match, but valid for individual matches in the Any match. |
| reverse       | boolean. default: false | Use with match arrays. Do not use with the first match in the array.<br/>  If true, searches for a match in lines that precede the previous match in the array. For example, in an array with matches A and B, if B is a First match with `"reverse":true`, then Sensible matches the first line that *precedes* the line matched by A. For a more detailed example, see [Reverse match](doc:match#reverse-match). |

Reverse match
---

Use the Reverse parameter in situations where an easy-to-match line follows a difficult target line. You can match the easy line, then set `"reverse:true"` to search preceding lines until you match the difficult line. 

**Config**

```json
{
  "fields": [
    {
      "id": "reverse_example",
      "anchor": {
        "match": [
          {
            "type": "startsWith",
            "text": "section header"
          },
          {
            "type": "startsWith",
            "text": "an unusual line"
          },
          {
            "type": "startsWith",
            "text": "a common line",
            "reverse": true
          }
        ]
      },
      "method": {
        "id": "label",
        "position": "below",
        "textAlignment": "hangingIndent"
      }
    }
  ]
}
```



**PDF**

The following image shows the example PDF used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/reverse_1.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/reverse.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "reverse_example": {
    "type": "string",
    "value": "Target data"
  }
}
```

**Notes**

Sensible searches for anchor candidates in sequence, and rules out overlapping candidates. In other words, after Sensible identifies an anchor candidate, it ignores that anchor line and its preceding lines when searching for the next candidate. The following image illustrates this behavior for the example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/reverse_2.png)
