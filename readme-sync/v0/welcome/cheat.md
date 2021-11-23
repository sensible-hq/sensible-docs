---
title: "Cheat sheet"
hidden: true

---

If you landed on this page, you're probably looking for answers for our in-app tutorials. 

[Part 1](doc:cheat#part-1)

[Part 2](doc:cheat#part-2)

[Part 3](doc:cheat#part-3)

[Part 4](doc:cheat#part-4)



Part 1
===

**Solution**

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

**Learn more**

To learn more about the steps you took in the tutorial, see:

| Link                      | Notes                                                        |
| ------------------------- | ------------------------------------------------------------ |
| [Anchor](doc:anchor)      | Fundamental concepts such as anchors and methods.            |
| [Label](doc:label)        | The label method is a frequently used extraction method.     |
| [Box](doc:box)            | The box method is a frequently used extraction method.       |
| [Color coding](doc:color) | Explains the yellow, blue, or green boxes you see overlaid on the PDF in the Sensible app. |

**Initial config**

To undo all your changes in Part 1, paste the following config into the left pane of the SenseML editor:


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

**Solution: Mix it up**

After you've completed all the Mix it up steps in the tutorial, the final config is:

```
{
  "fields": [
    {
      "id": "second_most_popular_snack",
      "anchor": "second",
      "type": "string",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "last"
      }
    },
    {
      "id": "snack_table",
      "anchor": "tables and rows",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 7,
        "columns": [
          {
            "id": "second_column",
            "index": 2
          },
          {
            "id": "sixth_column",
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

**Solution: Challenges**

After you've completed all the Challenges steps in the tutorial, the final config is:

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



**Learn more**

To learn more about the steps you took in the tutorial, see:

| Link               | Notes |
| ------------------ | ----- |
| [Row](doc:row)     |       |
| [Table](doc:table) |       |
| [Types](doc:types) |       |

**Initial config**

To undo all your changes in Part 2, paste the following config into the left pane of the SenseML editor:

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
      "id": "snack_table",
      "anchor": "tables and rows",
      "type": "table",
      "method": {
        "id": "fixedTable",
        "columnCount": 7,
        "columns": [
          {
            "id": "second_column",
            "index": 1
          },
          {
            "id": "sixth_column",
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



Part 3
====

**Initial config**

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

**Solution: Mix it up**

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

**Solution: Challenges**

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

