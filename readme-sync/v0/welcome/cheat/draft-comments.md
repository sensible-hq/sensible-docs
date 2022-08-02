---
title: "comments drafts"
hidden: true

---



GETTING STARTED -> 

TODO: UPDATED SOURCE OF TRUTH (position for rows) from this + update PDFs

https://dev.sensible.so/editor/?d=auto_insurance_quote&c=anyco&g=auto_insurance_anyco_golden

```json
{
  "fields": [
    {
      /* ID for target data (policy period) */
      "id": "policy_period",
      /* search for target data 
      near text "policy period" in doc*/
      "anchor": "policy period",
      "method": {
        /* target to extract is a single line 
        near anchor line ("policy period") */
        "id": "label",
        /* target data is to right of anchor line */              
        "position": "right"
      }
    },
    {
      /* target data is near text "comprehensive" */
      "id": "comprehensive_premium",
      "anchor": "comprehensive",
      /* target data is a currency, else return null */
      "type": "currency",
      "method": {
        /* target to extract is in a row */ 
        "id": "row",
        /* target is to right of anchor ("comprehensive") in row */
        "position": "right",
        /* grab 2nd cell (right of anchor) */
        "tiebreaker": "second"
      }
    },
    {
      /* target data is a currency in a row, 
      in the 2nd cell right of text "property"*/  
      "id": "property_liability_premium",
      "anchor": "property",
      "type": "currency",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "second"
      }
    },
    /* target data is all the text in box
    with anchor "policy number" */  
    {
      "id": "policy_number",
      "type": "string",
      "anchor": {
        "match": {
          "text": "policy number",
          "type": "startsWith" 
        }
      },
      "method": {
        "id": "box" 
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
        "anchor": "name of driver", //search for target data near "name of driver" text in doc
        "method": {
          "id": "label", //target to extract is a single line near anchor line
          "position": "below" //target is below anchor line
        }
    }],
    "computed_fields": [{ //target data is a transformation of already-extracted data
            "id": "driver_name_last", //ID for transformed target data
            "method": {
                "source_id": "_driver_name_raw", //already-extracted data to transform
                "id": "split", //target data is substring in already-extracted data 
                "separator": ", ", //use commas to split the already-extracted data into substring array 
                "index": 1 //target is 2nd element in substring array
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

