---
title: XML postprocessor
excerpt: Transform extracted data into an XML document
deprecated: false
hidden: false
metadata:
  title: ''
  description: 'Transform extracted data into an XML document'
  robots: index
next:
  description: ''
---
Use the XML postprocessor to transform Sensible's `parsed_document` output into an XML document. For example, use this postprocessor if your downstream system expects XML — such as a legacy system, EDI pipeline, or SOAP API.

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
}
```

Using the XML postprocessor, you define the shape of an XML document with a [JsonLogic](doc:jsonlogic) rule that constructs an element tree. Sensible evaluates the rule against the extracted data and serializes the result as an XML string.

Postprocessor output is available in the `postprocessorOutput` object in the API response and in the **Postprocessed** tab in the SenseML editor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_postprocessed_tab.png)

Postprocessor output isn't available in [Excel output](doc:excel-reference).

# Parameters

| key                  | value                   | description                                                                                                                                                                                                                                                                                                                                                        |
| :------------------- | :---------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type (**required**)  | `xml`                   | Identifies this postprocessor as an XML postprocessor.                                                                                                                                                                                                                                                                                                             |
| rule (**required**)  | JsonLogic object        | A [JsonLogic](doc:jsonlogic) rule that evaluates to an `XmlSpecNode` — an object with a `tag` (string, required), optional `attrs` (key-value pairs of attribute names to scalar values), and optional `content` (a scalar value, a nested `XmlSpecNode`, or an array of either). Sensible escapes reserved XML characters (`<`, `>`, `&`, `"`, `'`) in text content and attribute values automatically. |
| declaration          | Boolean. Default: false | If true, Sensible prepends an XML declaration (`<?xml version="1.0" encoding="UTF-8"?>`) to the output.                                                                                                                                                                                                                                                             |
| selfCloseEmptyTags   | Boolean. Default: true  | If true, Sensible renders elements with no content as self-closing tags (for example, `<tag/>`). If false, Sensible renders them as an open-and-close tag pair (for example, `<tag></tag>`).                                                                                                                                                                        |
| keepParsedDocument   | Boolean. Default: true  | If false, Sensible suppresses the `parsed_document` object in the output. Set to false to reduce the size of large output when you only need the postprocessor output. Setting to false disables [Excel](doc:excel-reference) output and [human review](doc:human-review).                                                                                          |

# Examples

## Example 1

The following example extracts fields from a CH Robinson rate confirmation and outputs them as XML, mapping each extracted field to a `<FIELD name="...">` element. The `mapObject` operator iterates over all fields in `parsed_document` and generates the child elements dynamically — so any field you add to the config appears in the XML output without updating the postprocessor rule.

**Config**

```json
{
  "postprocessor": {
    "type": "xml",
    "declaration": true,
    "selfCloseEmptyTags": false,
    "rule": {
      "eachKey": {
        "tag": "DOCUMENTS",
        "content": [
          {
            "eachKey": {
              "tag": "DOCUMENT",
              "content": [
                {
                  /* hardcoded element: document type name */
                  "eachKey": {
                    "tag": "FORM",
                    "content": "CH Robinson Rate Confirmation"
                  }
                },
                {
                  /* dynamic elements: one <FIELD name="id"> per extracted field */
                  "eachKey": {
                    "tag": "FIELDS",
                    "content": {
                      "mapObject": [
                        { "var": "" },
                        {
                          "eachKey": {
                            "tag": "FIELD",
                            "attrs": {
                              "eachKey": {
                                "name": { "var": "key" }
                              }
                            },
                            "content": { "var": "value.value" }
                          }
                        }
                      ]
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }
  },
  "fields": [
    {
      "id": "load_id",
      "method": {
        "id": "label",
        "position": "right"
      },
      "anchor": {
        "match": [
          {
            "text": "confirmation - #",
            "type": "includes"
          }
        ]
      }
    },
    {
      "id": "rate",
      "type": "currency",
      "method": {
        "id": "row",
        "position": "right",
        "tiebreaker": "first"
      },
      "anchor": {
        "start": [
          {
            "text": "service for load",
            "type": "startsWith"
          }
        ],
        "match": [
          {
            "text": "total",
            "type": "startsWith"
          }
        ]
      }
    },
    {
      "id": "broker_contact_name",
      "method": {
        "id": "regex",
        "pattern": "was booked with (.+), [+(]",
        "flags": "i"
      },
      "anchor": {
        "match": [
          {
            "pattern": "load was booked with",
            "type": "regex",
            "flags": "i"
          }
        ]
      }
    },
    {
      "id": "trailer_type",
      "method": {
        "id": "split",
        "separator": " - ",
        "source_id": "_trailer_raw",
        "index": 0
      }
    },
    {
      "id": "weight",
      "method": {
        "id": "label",
        "position": "below"
      },
      "anchor": {
        "match": [
          {
            "text": "Commodity",
            "type": "equals"
          },
          {
            "text": "Est wgt",
            "type": "equals"
          }
        ]
      }
    }
  ]
}
```

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/postprocessor_xml.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/postprocessor_xml.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |

**Output**

```xml
<!-- POSTPROCESSED OUTPUT -->

<?xml version="1.0" encoding="UTF-8"?>
<DOCUMENTS>
  <DOCUMENT>
    <FORM>CH Robinson Rate Confirmation</FORM>
    <FIELDS>
      <FIELD name="load_id">328298459</FIELD>
      <FIELD name="rate">4500</FIELD>
      <FIELD name="broker_contact_name">Sue Maske</FIELD>
      <FIELD name="trailer_type">Van</FIELD>
      <FIELD name="weight">7,000</FIELD>
    </FIELDS>
  </DOCUMENT>
</DOCUMENTS>
```

```json
// PARSED DOCUMENT OUTPUT

{
  "load_id": {
    "type": "string",
    "value": "328298459"
  },
  "rate": {
    "source": "$4,500.00",
    "type": "currency",
    "unit": "$",
    "value": 4500
  },
  "broker_contact_name": {
    "type": "string",
    "value": "Sue Maske"
  },
  "trailer_type": {
    "type": "string",
    "value": "Van"
  },
  "weight": {
    "type": "string",
    "value": "7,000"
  }
}
```

# Notes

- **XML character escaping**: Sensible automatically escapes reserved XML characters (`<`, `>`, `&`, `"`, `'`) in element content and attribute values.
- **Null fields**: Fields that return null appear as empty elements. With `selfCloseEmptyTags: true` (the default), they render as `<TAG/>`. With `selfCloseEmptyTags: false`, they render as `<TAG></TAG>`.
- **Dynamic field mapping**: The `mapObject` operator (a Sensible extension to JsonLogic) iterates over the key-value pairs of an object. Combined with `{"var": ""}` to reference the entire parsed document, it generates one XML element per extracted field without requiring you to name each field individually in the postprocessor rule. See [JsonLogic](doc:jsonlogic) for Sensible's full operator reference.
