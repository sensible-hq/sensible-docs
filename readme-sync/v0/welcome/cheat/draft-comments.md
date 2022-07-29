---
title: "Cheatsheets"
hidden: true

---

For answers to the Sensible in-app tutorials, see the following links:

[Part 1: Extract your first data](doc:cheat-1)

TODO I think this isn't source of turth

```json
{
  "fields": [
    {
      "id": "your_first_extracted_field", //output ID for target data
      "anchor": "hello world", //search for target data near line containing "hello world" in doc
      "method": {
        "id": "label", //target data is a single line near anchor line
        "position": "below" //target is below anchor line
      }
    }
  ]
}
```



[Part 2: Tables and rows](doc:cheat-2)



TODO I think this isn't source of turth but change tyruth to include zero-index tiebrearker

```json
{
  "fields": [
    {
      "id": "second_most_popular_snack", //output ID for target data
      "anchor": "second", //search for target data near anchor line containing "second"
      "type": "string",
      "method": {
        "id": "row", //target is a row
        "position": "left", //target is to left of anchor in row
        "tiebreaker": 0 // target is 1st row cell (left of anchor)
      }
    },
    {
      "id": "snack_table", //output ID for target data
      "anchor": "snack", //search for target data near anchor line containing "snack"  
      "type": "table",
      "method": {
        "id": "fixedTable", //target data is table below anchor with fixed column count
        "columnCount": 6,
        "columns": [
          {
            "id": "ranking", //output ID for table column
            "index": 1 //outputs cells in table's 2nd column
          },
          {
            "id": "liked_by",
            "index": 5, //outputs cells in table's 6th column...
            "type": "percentage", // ...if cell is percentage...
            "isRequired": true // ...else omit row containing cell from all outputted columns
          }
        ],
        "stop": {
          "type": "startsWith",
          "text": "in part 1" //for fast performance, stop table recognition before line containing "in part 1"
        }
      }
    }
  ]
}
```



[Part 3: Checkboxes, paragraphs, and regions](doc:cheat-3)

TODO I think this isn't source of turth

```json
{
  "fields": [
    {
      "id": "preference_monday_fruit", //output ID for target data
      "anchor": {
        "match": [
          {
            "type": "includes",
            "text": "monday"
          },
          {
            "type": "includes",
            "text": "fruit" //search for target data near anchor line including 'fruit' and preceded by line including 'monday'
          }
        ]
      },
      "method": {
        "id": "checkbox", //target data is a checkbox
        "position": "left" //target is to left of anchor line
      }
    },
    {
      "id": "preference_wed_fruit", //output ID for target data
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
      "id": "tuesday_all_options", //output ID for target data
      "anchor": "tuesday",
      "method": {
        "id": "region", //target data is all text in rectangular region
        "start": "below", //region is below anchor with following inch coordinates...
        "width": 9.0, //...for example, watch the green-outlined region resize as you change the "width" number
        "height": 0.5,
        "offsetX": -0.5,
        "offsetY": 0
      }
    },
    {
      "id": "disclaimer_paragraph", //output ID for target data
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "please note" //anchor line *starts* with this string
        }
      },
      "method": {
        "id": "documentRange", //target data is paragraph-like
        "includeAnchor": true, //includes anchor line in target data output
        "stop": {
          "type": "startsWith",
          "text": "in part 2"//target ends before line starting with this string
        }
      }
    }
  ]
}
```



GETTING STARTED -> **UPDATED SOURCE OF TRUTH**

https://dev.sensible.so/editor/?d=auto_insurance_quote&c=anyco&g=auto_insurance_anyco_golden

```json
{
  "fields": [
    {
      "id": "policy_period", //output ID for target data
      "anchor": "policy period", //search for target data near line containing "policy period" in doc
      "method": {
        "id": "label", //target data is a single line near anchor line
        "position": "right" //target is to right of anchor line
      }
    },
    {
      "id": "comprehensive_premium", //output ID for target data
      "anchor": "comprehensive", //anchor line contains "comprehensive"
      "type": "currency", //target is a currency
      "method": {
        "id": "row", //target is in a row
        "position": "right", //target is to right of anchor in row
        "tiebreaker": "second" //target is 2nd row cell (right of anchor)
      }
    },
    {
      "id": "property_liability_premium", //output ID for target data
      "anchor": "property",
      "type": "currency",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "second"
      }
    },
    {
      "id": "policy_number", //output ID for target data
      "type": "string",
      "anchor": {
        "match": {
          "text": "policy number",
          "type": "startsWith" //anchor line *starts* with "policy number"
        }
      },
      "method": {
        "id": "box" //anchor line is in a box. target is all other text in box.
      }
    }
  ]
}
```





