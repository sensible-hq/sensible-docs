---
title: "Cheat sheet"
hidden: true

---

THIS IS A DRAFT, needs polish! 



If you landed on this page, you got a bit stumped by our in-app tutorial at <TBD URL..linking possible?>.



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
        "columnCount": 6,
        "columns": [
          {
            "id": "column_in_table",
            "index": 1
          },
          {
            "id": "another_column",
            "index": 4,
            "type": "percentage"
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "try it out"
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
        "columnCount": 6,
        "columns": [
          {
            "id": "column_in_table",
            "index": 2
          },
          {
            "id": "another_column",
            "index": 4,
            "type": "phoneNumber"
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "try it out"
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
          "text": "try it out"
        }
      }
    }
  ]
}

```

