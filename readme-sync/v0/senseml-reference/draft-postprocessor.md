---
title: "Postprocessor LLM JsonSchema draft"
hidden: true
---



TODOS:

- experiment with descriptions. what if you make a validating description and the raw data doesn fit it?

- Reword the existing preprocessor to xlink/relate to this one

- new LLM postprocessors category?

- TODO: ask an LLM how it interfaces with Json Schema (+ test its answers in real life w/ chat/claude). like what does it do when raw data fails json schema specs:

  - <u>what are descriptions good for?</u> 

  - <u>what if an LLM can't recognize a speciied type compared to the source data?</u> 
  - <u>what does required do if the required extracted data isn't present?</u>



# rough draft:

Define your custom output [JSON schema](https://json-schema.org/learn) with an LLM-based postprocessor.  For example, use a postprocessor if your app or API consumes data using a pre-existing schema, and you don't want to integrate using Sensible's output schema.

In detail, Sensible's `parsed_document` API output schema represents extracted document data as typed [fields](doc:field-query-object):

```json
{
"parsed_document": {
        "contract_date": {
            "value": "2023-01-01T00:00:00.000Z",
            "type": "date"
        },
         "customer_name": {
                "type": "string",
                "value": "John Smith"
            }
}
```

Using a postprocessor, you can specify your target JSON schema, and then the LLM takes your extracted data and transforms it. T*ODO award, simply sentence.*  

For example, for the following  extracted data:

``` json
{
    "eobs": [
        {
            "allowedAmountTotal": {
                "source": "119.00",
                "value": 119,
                "unit": "$",
                "type": "currency"
            },
            "claimNumber": {
                "type": "string",
                "value": "20231111"
            }
        }
    ]
}
```

You can specify:

```json
{
    "postprocessor": {
        "type": "jsonSchema",
        "schema": {
            "type": "object",
            "properties": {
                "allowedAmountTotal": {
                    "type": "integer"
                },
                "claimNumber": {
                    "type": "string",
                    "description": "must always be 8 digits"
                }
            },
            "required": [
                "claimNumber"
            ]
        }
    }
}
```

And the LLM transforms the extracted data to fit your specified JSON schema:

```json
{
    "postprocessorOutput": {
            "allowedAmountTotal": 119,
            "claimNumber": "20231111"
        
    }
}
```

This postprocessor is a low-code, indeterminate alternative to the JsonLogic postprocessor TODO LINK.

Postprocessor output is available in the `postprocessorOutput` object in the API response and in the **postprocessed** tab in the JSON editor: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/ui_postprocessed_tab.png) 

Postprocessor output isn't available in [Excel output](doc:excel-reference).

# Parameters


| key                   | value        | description                                                  |
| :-------------------- | :----------- | :----------------------------------------------------------- |
| type (**required**)   | `jsonSchema` | Specify the target [JSON schema](https://json-schema.org/learn) into which to transform the existing extracted JSON data TDODO word better |
| schema (**required**) | Json  object | Define a custom JSON schema for the LLM to transform your existing extracted data.  TODOs -- update w guidance abt what might happen when raw data fails the json schema specs. |



# Examples

## Example 1

**Config**

```json

```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/TBD.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/TBD.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**



remember to do  // POSTPROCESSED OUTPUT and  // PARSED DOCUMENT OUTPUT 