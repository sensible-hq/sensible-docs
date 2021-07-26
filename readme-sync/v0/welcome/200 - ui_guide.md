---
title: "UI guide"
hidden: true
---

The Sensible app helps you understand your SenseML queries using visual symbols. This topic explains the symbols.

Anchors and matches
====

Yellow boxes represent anchors. For more information about anchors, see [Anchors](doc:anchor-object).

Blue boxes represent matches. For more information about matches, see [Match object](doc:match-object).

For example, the following image shows:

- an anchor line outlined in yellow ("Here is a good candidate..")
- a matched line outlined in blue ("And here's the text below..")

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/ui_anchor_method_1.png)

The query used to capture this anchor line is:

```json
{
  "fields": [
    {
      "id": "simple_label",
      "anchor": "Here is a good candidate",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}    
```

Discarded data
====

The Sensible app represents discarded data to help you troubleshoot your queries. 

Discarded anchor data
---

Sensible anchors filter out captured text depending on parameters you set in the field, the anchor, and the method. Common parameters resulting in filtering include:

-  the field's data type (currency, date, address, etc)
-  the field's match method (first, last, all)
- the anchor's start and end
- the method's id (for example, a Label method filters out all lines that are not closely proximate to other lines)

Light yellow boxes represent filtered-out anchor data.

For example, in the following image:

- There is one filtered out "languages" anchor surrounded by a light yellow box. It is filtered out because the field's Match paramter specifies to match the last instance of this word.

- There are two filtered out "python" anchors surrounded by light yellow boxes. They are filtered out because they do not meet the Label method's proximitey requirements.  If this query specified a Row method instead, the first "python" instance would successfully match, and would become outlined in darker yellow. 

  

```json
{
  "fields": [
    {
      "id": "filtered_by_match",
      "anchor": "languages",
      "match": "last",
      "method": {
        "id": "label",
        "position": "right"
      }
    }
    {
      "id": "filtered_by_method",
      "anchor": "python",
      "match": "first",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
  ]
}
```





Discarded method data
---

Sensible methods filter out captured data depending on parameters you set in the field, the anchor, and the method. Common parameters resulting in filtering include:

- the field's data type (currency, date, address, etc)
- the method's stop
- the method's tiebreaker

Light blue boxes represent filtered-out method data. For example, in the following image, a Row method captures everything to the right of the text "Python", but a tiebreaker selects 11.87% and discards +2.75%:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/ui_filtered_method_row.png)

The query used in the following image is:

```json
{
  "fields": [
    {
      "id": "python_change_in_TIBOE_rating",
      "method": {
        "id": "row",
        "tiebreaker": "second"
      },
      "anchor": {
        "match": [
          {
            "text": "Languages ranked by search engine",
            "type": "startsWith"
          },
          {
            "text": "Python",
            "type": "startsWith"
          }
        ]
      }
    }
  ]
}
```





Points and positions
====



![image-20210525092225165](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210525092225165.png)

Line details
====

