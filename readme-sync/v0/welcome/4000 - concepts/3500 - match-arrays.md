---
title: "Match arrays"
hidden: false
---

**Note:** If you're familiar with Sensible, this detailed topic is for you. If you're new to Sensible, see [match](doc:match).



Sensible creates an anchor using the last element in a Match array if:

- The other array elements precede the last element in order.
- Each array element targets a separate successive line.

This example creates an Anchor line using the last element in the array:

```json
{
  "fields": [
    {
      "id": "match_array",
      "anchor": {
        "start": "My section heading to start matching on",
        "end": "My footer text to stop matching on",
        "includeEnd": true,
        "match": 
          [
            {
              "type": "includes",
              "text": "finds anchor if you match this string in a line",
            },
            {
              "type": "startsWith",
              "pattern": "followed by the first occurrence of this string in another line",
            },
                          {
              "type": "regex",
              "text": ".*create an Anchor line out of this last match",
            },
          ]      
      },
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}
```

Reverse match arrays
---

Use the Reverse parameter when a difficult target line precedes an easy-to-match line. You can match the easy line, then set `"reverse:true"` to search preceding lines until you match the difficult line. 

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

Sensible searches for anchor candidates in sequence, and rules out overlapping match arrays. The following image illustrates this behavior for the example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/reverse_2.png)

