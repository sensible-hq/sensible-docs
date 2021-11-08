---
title: "Cheat sheet"
hidden: true

---

THIS IS A DRAFT, needs polish! 

TODO: add TOC

If you landed on this page, you got a bit stumped by our in-app tutorial at <TBD URL..linking possible?>.

Part 2
===


Check out the answers and explanations:

**Starting state**

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
      "id": "preference_monday_oatmeal",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "monday"
          },
          {
            "type": "includes",
            "text": "oatmeal"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "preference_wed_oatmeal",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "wednesday"
          },
          {
            "type": "includes",
            "text": "oatmeal"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
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
          "text": "try it out"
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
      "id": "preference_monday_oatmeal",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "monday"
          },
          {
            "type": "includes",
            "text": "oatmeal"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
      }
    },
    {
      "id": "preference_wed_oatmeal",
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "tuesday"
          },
          {
            "type": "includes",
            "text": "oatmeal"
          }
        ]
      },
      "method": {
        "id": "checkbox",
        "position": "left"
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
          "text": "challenges"
        }
      },
      "type": "paragraph"
    }
  ]
}
```



{

 "fields": [

  {

   "id": "my_data_439",

   "anchor": {

​    "match": {

​     "type": "includes",

​     "text": "please note"

​    }

   },

   "method": {

​    "id": "region",

​    "height": 1,

​    "offsetX": 0,

​    "offsetY": -1,

​    "start": "below"

   }

  }

 ]

}
