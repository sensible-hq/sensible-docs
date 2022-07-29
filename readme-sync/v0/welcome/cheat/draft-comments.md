---
title: "comments drafts"
hidden: true

---



[Part 1: Extract your first data](doc:cheat-1)

TODO doublecheck senseml

```json
{
  "fields": [
    {
      "id": "your_first_extracted_field", //ID for extracted target data
      "anchor": "hello world", //search for target data near line containing "hello world" in doc
      "method": {
        "id": "label", //target to extract is a single line near anchor line
        "position": "below" //target is below anchor line
      }
    }
  ]
}
```



[Part 2: Tables and rows](doc:cheat-2)



TODO doublecheck senseml. and update for zero-index tiebrearker

```json
{
  "fields": [
    {
      "id": "second_most_popular_snack", //ID for extracted target data
      "anchor": "second", //search for target data near anchor line containing "second"
      "type": "string",
      "method": {
        "id": "row", //target to extract is in a row
        "position": "left", //target is to left of anchor in row
        "tiebreaker": 0 // target is 1st row cell (left of anchor)
      }
    },
    {
      "id": "snack_table", //ID for extracted target data
      "anchor": "snack", //search for target data near anchor line containing "snack"  
      "type": "table",
      "method": {
        "id": "fixedTable", //target is in table below anchor with fixed column count
        "columnCount": 6,
        "columns": [
          {
            "id": "ranking", //ID for extracted table column
            "index": 1 //extract cells in table's 2nd column
          },
          {
            "id": "liked_by", //ID for extracted table column
            "index": 5, //extract cells in table's 6th column...
            "type": "percentage", // ...if cell is percentage...
            "isRequired": true // ...else omit row containing cell from all extracted columns in table
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

TODO doublecheck senseml

```json
{
  "fields": [
    {
      "id": "preference_monday_fruit", //ID for extracted target data
      "anchor": {
        "match": [
          {
            "type": "includes", //search for target data near anchor line...
            "text": "monday"
          },
          {
            "type": "includes",
            "text": "fruit" //...including 'fruit' and preceded by line including 'monday'
          }
        ]
      },
      "method": {
        "id": "checkbox", //target to extract is a checkbox
        "position": "left" //target is to left of anchor line
      }
    },
    {
      "id": "preference_wed_fruit", //ID for extracted target data
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
      "id": "tuesday_all_options", //ID for extracted target data
      "anchor": "tuesday",
      "method": {
        "id": "region", //target data is all the text in a rectangular region
        "start": "below", //region is below anchor with following inch coordinates...
        "width": 9.0, //...for example, watch the green-outlined region resize as you change the "width" number
        "height": 0.5,
        "offsetX": -0.5,
        "offsetY": 0
      }
    },
    {
      "id": "disclaimer_paragraph", //ID for extracted target data
      "anchor": {
        "match": {
          "type": "startsWith", //anchor line *starts* with "please note"
          "text": "please note" 
        }
      },
      "method": {
        "id": "documentRange", //target data is paragraph-like
        "includeAnchor": true, //extract anchor line along with target data
        "stop": {
          "type": "startsWith",
          "text": "in part 2"//target ends before line starting with this string
        }
      }
    }
  ]
}
```



GETTING STARTED -> 

TODO: UPDATED SOURCE OF TRUTH (position for rows) from this + update PDFs

https://dev.sensible.so/editor/?d=auto_insurance_quote&c=anyco&g=auto_insurance_anyco_golden

```json
{
  "fields": [
    {
      "id": "policy_period", //ID for extracted target data
      "anchor": "policy period", //search for target data near line containing "policy period" in doc
      "method": {
        "id": "label", //target to extract is a single line near anchor line
        "position": "right" //target is to right of anchor line
      }
    },
    {
      "id": "comprehensive_premium", //ID for extracted target data
      "anchor": "comprehensive", //anchor line contains "comprehensive"
      "type": "currency", //target is a currency
      "method": {
        "id": "row", //target is in a row
        "position": "right", //target is to right of anchor in row
        "tiebreaker": "second" //target is 2nd row cell (right of anchor)
      }
    },
    {
      "id": "property_liability_premium", //ID for extracted target data
      "anchor": "property",
      "type": "currency",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "second"
      }
    },
    {
      "id": "policy_number", //ID for extracted target data
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



SENSEML INTRO

https://docs.sensible.so/docs/senseml-reference-introduction



```json
{
    "fingerprint": { //preferentially run this config if doc contains the test strings
        "tests": [ 
            "anyco",
            "quoted coverage changes"
        ]
    },
    "preprocessors": [{
        "type": "pageRange", //cuts out irrelevant doc pages before extraction
        "startPage": 0,
        "endPage": 2
    }],
    "fields": [{
        "id": "_driver_name_raw", //ID for extracted target data
        "anchor": "name of driver", //search for target data near line containing "name of driver" in doc
        "method": {
          "id": "label", //target to extract is a single line near anchor line
          "position": "below" //target is below anchor line
        }
    }],
    "computed_fields": [{
            "id": "driver_name_last", //ID for extracted target data
            "method": {
                "source_id": "_driver_name_raw", //target data is transformed from this already-extracted data
                "id": "split", //target data is substring in already-extracted data 
                "separator": ", ", //split the target on commas into substring array 
                "index": 1 // target is 2nd element in substring array
            }
        }

    ]
}
```



SenseML concepts



https://docs.sensible.so/docs/senseml

```json
{

  "fields": [
    {
      "id": "name_of_output_key",
      "anchor": "an anchor is some text to match. An anchor can be an array of matches",
      "method": {
        "id": "label",
         "position": "below"
      }
    },
  ]
}
```

