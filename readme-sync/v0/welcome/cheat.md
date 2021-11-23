---
title: "Cheat sheet"
hidden: true

---

If you landed on this page, you're probably looking for answers for our in-app tutorials. 

[Part 1](doc:cheat#part-1)



Part 1
===

Solution
---

After you've completed all the steps in the tutorial, the final config is:

```json
{
  "fields": [
    {
      "id": "your_first_extracted_field",
      "anchor": "use this anchor line",
      "method": {
        "id": "box",
        "position": "right"
      }
    }
  ]
}
```

Explanation
---

Here are some explanations of the effects of some of the steps you take in this tutorial:

**Change 1**

- change `"anchor": "welcome"` to `"anchor": "use this anchor line"`

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/cheat_1_1.png)

The line starting with "Use this anchor line" becomes the new anchor, as shown by the yellow box. The anchor serves as a label (`"id":"label"`) for the target line below the anchor (`"position":"below"`).   For more information, see [Label](doc:lable).

The blue box shows the target line to extract. 



**Change 3**

- change `"id": "label"` to  `"id": "box"`

Instead of treating the anchor as a label, Sensible searches outward from the anchor line to find dark box borders. Once Sensible recognizes the box, it grabs all the text inside the box except the anchor line itself. For more information, see [Box](doc:box).



Initial config
----

If you want to undo all your changes to the Part 1 config, paste the following config into the left pane of the SenseML editor:


```json
{
  "fields": [
    {
      "id": "your_first_extracted_field",
      "anchor": "welcome",
      "method": {
        "id": "label",
        "position": "below"
      }
    }
  ]
}
```



Part 2
===

Solution
---

After you've completed all the steps in the tutorial, the final config is:



Explanation
---

Initial config
---

```json
{
  "fields": [
    {
      "id": "second_most_popular_snack",
      "anchor": "second",
      "type": "string",
      "method": {
        "id": "row",
        "position": "left",
        "tiebreaker": "first"
      }
    },
    {
      "id": "table_with_specified_columns",
      "anchor": "tables and rows",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 7,
        "columns": [
          {
            "id": "column_in_table",
            "index": 1
          },
          {
            "id": "another_column",
            "index": 5,
            "type": "percentage"
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "mix it up"
        }
      }
    }
  ]
}

```

**Mix it up answers**

TBD explanations

```json
{
  "fields": [
    {
      "id": "second_most_popular_snack",
      "anchor": "second",
      "type": "string",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "first"
      }
    },
    {
      "id": "table_with_specified_columns",
      "anchor": "tables and rows",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 7,
        "columns": [
          {
            "id": "column_in_table",
            "index": 2
          },
          {
            "id": "another_column",
            "index": 5,
            "type": "phoneNumber"
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "mix it up"
        }
      }
    }
  ]
}

```

**Challenges solutions**

TBD explanations

```json
{
  "fields": [
    {
      "id": "second_most_popular_snack",
      "anchor": "second",
      "type": "currency",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": ">"
      }
    },
    {
      "id": "table_with_specified_columns",
      "anchor": "mix it up",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 3,
        "columns": [
          {
            "id": "column_in_table",
            "index": 0
          },
          {
            "id": "another_column",
            "index": 2,
            "type": "string"
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "challenges"
        }
      }
    }
  ]
}

```



Part 3
====

Starting state
---

**TBD explanation**

```json
{
  "fields": [
    {
      "id": "preference_monday_fruit",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "monday"
          },
          {
            "type": "includes",
            "text": "fruit"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "preference_wed_fruit",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "wednesday"
          },
          {
            "type": "includes",
            "text": "fruit"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "all_options_wednesday",
      "anchor": "wednesday",
      "method": {
        "id": "region",
        "start": "below",
        "width": 5,
        "height": 0.5,
        "offsetX": -0.5,
        "offsetY": 0
      }
    },
    {
      "id": "disclaimer_paragraph",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "please note"
        }
      },
      "method": {
        "id": "documentRange",
        "includeAnchor": true,
        "stop": {
          "type": "startsWith",
          "text": "try it"
        }
      },
      "type": "paragraph"
    }
  ]
}
```



After Try it Out
---

```json
{
  "fields": [
    {
      "id": "preference_tuesday_fruit",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "tuesday"
          },
          {
            "type": "includes",
            "text": "fruit"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "preference_wed_fruit",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "wednesday"
          },
          {
            "type": "includes",
            "text": "fruit"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "all_options_wednesday",
      "anchor": "wednesday",
      "method": {
        "id": "region",
        "start": "below",
        "width": 5,
        "height": 0.5,
        "offsetX": -0.5,
        "offsetY": 0
      }
    },
    {
      "id": "disclaimer_paragraph_and_try_it_out_section",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "please note"
        }
      },
      "method": {
        "id": "documentRange",
        "includeAnchor": true,
        "stop": {
          "type": "startsWith",
          "text": "challenges"
        }
      },
      "type": "paragraph"
    }
  ]
}
```

After Challenges
---



```json
{
  "fields": [
    {
      "id": "preference_tuesday_grits",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "grits",
        }
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "preference_wed_fruit",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "wednesday"
          },
          {
            "type": "includes",
            "text": "fruit"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "all_options_tues",
      "anchor": "tues",
      "method": {
        "id": "region",
        "start": "below",
        "width": 6,
        "height": 0.5,
        "offsetX": -0.5,
        "offsetY": 0
      }
    },
    {
      "id": "disclaimer_paragraph_and_try_it_out_section",
      "anchor": {
        "match": {
          "type": "includes",
          "text": "please note"
        }
      },
      "method": {
        "id": "documentRange",
        "includeAnchor": true,
        "stop": {
          "type": "startsWith",
          "text": "challenges"
        }
      },
      "type": "paragraph"
    }
  ]
}
```

Part 4
====



```json
{
  "fields": [
    {
      "id": "grand_total",
      "type": "currency",
      "anchor": "grand total",
      "method": {
        "id": "row",
        "tiebreaker": ">"
      }
    },
    {
      "id": "doc_date",
      "type": "date",
      "anchor": "document date",
      "method": {
        "id": "label",
        "position": "below",
        "textAlignment": "hangingIndent"
      }
    },
    {
      "id": "customer_address",
      "type": "address",
      "anchor": "prepared for",
      "method": {
        "id": "box"
      }
    },
    {
      "id": "reflective_finish",
      "anchor": "reflective",
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "terms_paragraphs",
      "anchor": "subject to",
      "type": "paragraph",
      "method": {
        "id": "documentRange"
      }
    }
  ]
}
```



OUTPUT:

TODO: add in?

