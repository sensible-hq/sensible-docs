---
title: XML postprocessor
excerpt: Transform extracted data into a custom XML output schema
deprecated: false
hidden: false
metadata:
  title: ''
  description: Transform extracted data into a custom XML output schema
  robots: index
next:
  description: ''
---
Define your own XML output with a [JsonLogic](doc:jsonlogic)-based postprocessor. For example, use a postprocessor if your app or API consumes data using an XML schema, and you don't want to integrate using Sensible's output schema.

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

Using a postprocessor, you can transform the extracted data into an XML output, for example:

```json
{
  "postprocessorOutput": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<invoice>\n  <contract_date type=\"date\">2023-01-01T00:00:00.000Z</contract_date>\n  <customer_name type=\"string\">John Smith</customer_name>\n</invoice>"
}
```

The following rule produces that output:

```json
{
  "eachKey": {
    "tag": "invoice",
    "content": [
      {
        "eachKey": {
          "tag": "contract_date",
          "attrs": { "eachKey": { "type": { "var": "contract_date.type" } } },
          "content": { "var": "contract_date.value" }
        }
      },
      {
        "eachKey": {
          "tag": "customer_name",
          "attrs": { "eachKey": { "type": { "var": "customer_name.type" } } },
          "content": { "var": "customer_name.value" }
        }
      }
    ]
  }
}
```

Find postprocessor output in the `postprocessorOutput` string value in the API response and in the **Postprocessed** tab in the SenseML editor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_postprocessed_tab.png)

Postprocessor output isn't available in [Excel output](doc:excel-reference).

# Parameters

| key                 | value                   | description                                                                                                                                                                                                         |
| :------------------ | :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| type (**required**) | `xml`                   | Transform extracted data into an XML output.                                                                                                                                                                        |
| rule (**required**) | JsonLogic object        | Define the XML output using a [JsonLogic](doc:jsonlogic) rule. See [JSON to XML mapping](#json-to-xml-mapping) for the rule syntax.                                                                                 |
| declaration         | Boolean. Default: false | If true, Sensible prepends an XML declaration (`<?xml version="1.0" encoding="UTF-8"?>`) to the output.                                                                                                             |
| selfCloseEmptyTags  | Boolean. Default: true  | If true, Sensible renders elements with no content as self-closing tags (for example, `<tag/>`). If false, Sensible renders them as an open-and-close tag pair (for example, `<tag></tag>`).                        |
| keepParsedDocument  | Boolean. Default: true  | If false, Sensible suppresses the `parsed_document` object in the output. Set to false to reduce the size of large output when you only need the postprocessor output. Setting to false disables [Excel](doc:excel-reference) output and [human review](doc:human-review). |

# JSON to XML mapping

The `rule` parameter takes a [JsonLogic](doc:jsonlogic) rule that must evaluate to an element object. A minimal rule looks like this:

```json
{
  "eachKey": {
    "tag": "invoice",
    "attrs": {
      "eachKey": {
        "currency": "USD"
      }
    },
    "content": [
      {
        "eachKey": {
          "tag": "total",
          "content": { "var": "total.value" }
        }
      }
    ]
  }
}
```

This produces:

```json
{
  "postprocessorOutput": "<invoice currency=\"USD\">\n  <total>4500</total>\n</invoice>"
}
```

The element object has the following properties:

| property            | value                                              | description                                                                                                                                                                                       |
| :------------------ | :------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| tag (**required**)  | string                                             | The XML element name.                                                                                                                                                                             |
| attrs               | object                                             | Key-value pairs that become XML attributes on the element. Use the [Each Key](doc:jsonlogic#each-key) operation to build the object. Values must be scalars (string, number, boolean, or null).   |
| content             | scalar, element object, or array of either         | The element's content. A scalar value (string, number, boolean, or null) becomes text content. An element object becomes a nested child element. An array produces a sequence of child elements. |

Sensible automatically escapes reserved XML characters (`<`, `>`, `&`, `"`, `'`) in text content and attribute values. For example, `"content": "1 < 2 & 3 > 0"` renders as `1 &lt; 2 &amp; 3 &gt; 0`.

**Dynamic Field Mapping with [mapObject](doc:jsonlogic#map-object)**

To generate one XML element per extracted field without naming each field individually in the rule, use the [mapObject](doc:jsonlogic#map-object) operation with `{"var": ""}` to iterate over the entire `parsed_document`:

```json
{
  "mapObject": [
    { "var": "" },
    {
      "eachKey": {
        "tag": { "var": "key" },
        "content": { "var": "value.value" }
      }
    }
  ]
}
```

If `parsed_document` contains `load_id` and `rate` fields, this produces:

```json
{
  "postprocessorOutput": "<load_id>328298459</load_id>\n<rate>4500</rate>"
}
```

Any field you add to the config automatically appears in the XML output without updating the postprocessor rule. See [JsonLogic](doc:jsonlogic) for Sensible's full operator reference.

# Examples

## Example 1

**Config**

```json
{
  "fields": [
    {
      "id": "load_id",
      "type": "number",
      "method": { "id": "passthrough" },
      "anchor": {
        "match": [{ "text": "confirmation - #", "type": "includes" }]
      }
    },
    {
      "id": "_trailer_type_raw",
      "method": { "id": "row", "position": "right", "tiebreaker": "first" },
      "anchor": { "match": [{ "text": "Equipment:", "type": "startsWith" }] }
    },
    {
      "id": "trailer_type",
      "method": {
        "id": "split",
        "separator": " - ",
        "source_id": "_trailer_type_raw",
        "index": 0
      }
    },
    {
      "id": "hide_fields",
      "method": { "id": "suppressOutput", "source_ids": ["_trailer_type_raw"] }
    },
    {
      "id": "test_field_xml_escapes_&_<stuff>",
      "method": {
        "id": "constant",
        "value": "blah 'blah' \"blah\" & <blah></blah>"
      }
    },
    { "id": "test_field_null", "method": { "id": "constant", "value": "" } }
  ],
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
                  "eachKey": {
                    "tag": "FORM",
                    "content": "AU Tax Invoice Precise"
                  }
                },
                {
                  "eachKey": {
                    "tag": "FIELDS",
                    "content": {
                      "mapObject": [
                        { "var": "" },
                        {
                          "eachKey": {
                            "tag": "FIELD",
                            "attrs": {
                              "eachKey": { "name": { "var": "key" } }
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
  }
}
```

**Example document**\
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/postprocessor_xml.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/postprocessor_xml.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |

**Output**

```json
// POSTPROCESSED OUTPUT

{
  "postprocessorOutput": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><DOCUMENTS><DOCUMENT><FORM>AU Tax Invoice Precise</FORM><FIELDS><FIELD name=\"load_id\">328298459</FIELD><FIELD name=\"trailer_type\">Van</FIELD><FIELD name=\"test_field_xml_escapes_&amp;_&lt;stuff&gt;\">blah 'blah' \"blah\" &amp; &lt;blah&gt;&lt;/blah&gt;</FIELD><FIELD name=\"test_field_null\"></FIELD></FIELDS></DOCUMENT></DOCUMENTS>"
}
```

```json
// PARSED DOCUMENT OUTPUT

{
  "load_id": {
    "source": "328298459",
    "value": 328298459,
    "type": "number"
  },
  "trailer_type": {
    "value": "Van",
    "type": "string"
  },
  "test_field_xml_escapes_&_<stuff>": {
    "value": "blah 'blah' \"blah\" & <blah></blah>",
    "type": "string"
  },
  "test_field_null": null
}
```

# Notes

- **Null fields**: Fields that return null appear as empty elements. With `selfCloseEmptyTags: true` (the default), they render as `<TAG/>`. With `selfCloseEmptyTags: false`, they render as `<TAG></TAG>`.
