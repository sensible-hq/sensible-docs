---
title: XML postprocessor
excerpt: Transform extracted data into a custom XML output schema
deprecated: false
hidden: true
metadata:
  title: ''
  description: Transform extracted data into a custom XML output schema
  robots: index
next:
  description: ''
slug: draft-xml
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
  "postprocessorOutput": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><invoice><contract_date type=\"date\">2023-01-01T00:00:00.000Z</contract_date><customer_name type=\"string\">John Smith</customer_name></invoice>"
}
```

The following JsonLogic rule produces the preceding XML output:

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    /*
        In practice, you extract contract_date and customer_name from a document.
        This example uses constant fields to input hardcoded values
        so you can run it in the SenseML editor without a document.
      */
    {
      "id": "contract_date",
      "type": "date",
      "method": { "id": "constant", "value": "2023-01-01T00:00:00.000Z" }
    },
    {
      "id": "customer_name",
      "type": "string",
      "method": { "id": "constant", "value": "John Smith" }
    }
  ],
  "postprocessor": {
    "type": "xml",
    "declaration": true,
    "rule": {
      "eachKey": {
        /* builds an element object; its properties define the XML output */
        "tag": "invoice" /* root XML element name */,
        "content": [
          /* array. produces a sequence of child elements */
          {
            "eachKey": {
              "tag": "contract_date" /* XML element name */,
              "attrs": {
                /* key-value pairs that become XML attributes, e.g. type="date" */
                "eachKey": {
                  "type": { "var": "contract_date.type" }
                } /* "var" returns "date" from parsed_document */
              },
              "content": {
                "var": "contract_date.value"
              } /* extracted value, e.g. "2023-01-01T00:00:00.000Z", becomes
  text content */
            }
          },
          {
            "eachKey": {
              "tag": "customer_name" /* XML element name */,
              "attrs": {
                /* key-value pairs that become XML attributes, e.g. type="string" */
                "eachKey": {
                  "type": { "var": "customer_name.type" }
                } /* "var" returns "string" from parsed_document */
              },
              "content": {
                "var": "customer_name.value"
              } /* extracted value, e.g. "John Smith", becomes text content */
            }
          }
        ]
      }
    }
  }
}
```

Find postprocessor output in the `postprocessorOutput` string value in the API response and in the **Postprocessed** tab in the SenseML editor:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/ui_postprocessed_tab.png)

Postprocessor output isn't available in [Excel output](doc:excel-reference).

# Parameters

| key                 | value                     | description                                                                                                                                                                                                                                                                                                          |
| :------------------ | :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type (**required**) | `xml`                     | Transform extracted data into an XML output.                                                                                                                                                                                                                                                                         |
| rule (**required**) | JsonLogic object          | Define the XML output using a [JsonLogic](doc:jsonlogic) rule. See [Defining XML output](#defining-xml-output) for the rule syntax. The rule must evaluate to a root element object.                                                                                                                                 |
| declaration         | boolean. default: `false` | If true, Sensible prepends an XML declaration (`<?xml version="1.0" encoding="UTF-8"?>`) to the output.                                                                                                                                                                                                              |
| selfCloseEmptyTags  | boolean. default: `true`  | If true, Sensible renders elements with no content as self-closing tags (for example, `<tag/>`). If false, Sensible renders them as an open-and-close tag pair (for example, `<tag></tag>`). Null fields appear as empty elements, for example, `<null_field/>` when true or `<null_field></null_field>` when false. |
| keepParsedDocument  | boolean. default: `true`  | If false, Sensible suppresses the `parsed_document` object in the output and disables [Excel](doc:excel-reference) output and [human review](doc:human-review). Set to false to reduce the size of large output when you only need the postprocessor output.                                                         |

# Defining XML output

In the `rule` parameter, define your XML output using [JsonLogic](doc:jsonlogic). A minimal rule looks like this:

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    /*
      In practice, you extract total from a document.
      This example uses a constant field to input a hardcoded value
      so you can run it in the SenseML editor without a document.
    */
    {
      "id": "total",
      "type": "currency",
      "method": { "id": "constant", "value": "4500" }
    }
  ],
  "postprocessor": {
    "type": "xml",
    "rule": {
      "eachKey": { /* builds an element object; its properties define the XML output */
        "tag": "invoice", /* XML root element name */
        "attrs": { /* key-value pairs that become XML attributes */
          "eachKey": {
            "currency": "USD" /* hardcoded attribute value */
          }
        },
        "content": [ /* array — produces a sequence of child elements */
          {
            "eachKey": {
              "tag": "total", /* XML element name */
              "content": { "var": "total.value" } /* extracted value becomes text content */
            }
          }
        ]
      }
    }
  }
}
```

This produces:

```json
{
  "postprocessorOutput": "<invoice currency=\"USD\"><total>4500</total></invoice>"
}
```

Each element object you define in the rule has the following properties:

| property           | value                                                                             | description                                                                                                                                                                                      |
| :----------------- | :-------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tag (**required**) | string                                                                            | The XML element name.                                                                                                                                                                            |
| attrs              | JsonLogic object                                                                  | Key-value pairs that become XML attributes on the element. Use the [Each Key](doc:jsonlogic#each-key) operation to build the object. Values must be scalars (string, number, boolean, or null).  |
| content            | scalar, JsonLogic object that evaluates to XML element object, or array of either | The element's content. A scalar value (string, number, boolean, or null) becomes text content. An element object becomes a nested child element. An array produces a sequence of child elements. |

If you specify a string value for the Attrs or Content parameter, Sensible automatically escapes reserved XML characters (`<`, `>`, `&`, `"`, `'`). For example, `"content": "1 < 2 & 3 > 0"` renders as `"1 &lt; 2 &amp; 3 &gt; 0"`.

### Dynamic field mapping

To generate one XML element per extracted field without naming each field individually in the rule, use the [Map Object](doc:jsonlogic#map-object) operation with `{"var": ""}` to iterate over the entire `parsed_document`. Because the rule must output a well-formed XML document, nest [Map Object](doc:jsonlogic#map-object) inside the `content` property of a root element:

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    /*
      In practice, you extract load_id and rate from a document.
      This example uses constant fields to input hardcoded values
      so you can run it in the SenseML editor without a document.
    */
    {
      "id": "load_id",
      "type": "number",
      "method": { "id": "constant", "value": "328298459" }
    },
    {
      "id": "rate",
      "type": "number",
      "method": { "id": "constant", "value": "4500" }
    }
  ],
  "postprocessor": {
    "type": "xml",
    "rule": {
      "eachKey": {
        "tag": "document", /* root element wrapping all fields */
        "content": {
          "mapObject": [ /* iterates over each field in parsed_document and operates on its key and value */
            { "var": "" }, /* current context: the entire parsed_document */
            {
              "eachKey": { /* builds an element object for each field */
                "tag": { "var": "key" }, /* current field's ID becomes the XML element name */
                "content": { "var": "value.value" } /* current field's extracted value becomes text content */
              }
            }
          ]
        }
      }
    }
  }
}
```

This produces:

```json
{
  "postprocessorOutput": "<document><load_id>328298459</load_id><rate>4500</rate></document>"
}
```

Any field you add to the config automatically appears in the XML output without updating the postprocessor rule. See [JsonLogic](doc:jsonlogic) for Sensible's full operator reference.

# Examples

## Example 1

**Config**

```json
/* Sensible uses JSON5 to support in-line comments*/
{
  "fields": [
    {
      "id": "load_id", /* user-friendly ID for extracted target data */
      "type": "number", /* Sensible formats extracted data as this data type, or returns null if it doesn't recognize extracted data as the specified type */
      "method": { "id": "passthrough" },
      "anchor": { /* an anchor is text that always occurs in the same position relative to your target data. */
        "match": [ /* array of Match objects. Sensible matches the last element
                      if each element matches a successive line in the document */
          {
            "text": "confirmation - #", /* string to match */
            "type": "includes" /* match anywhere in line. */
          }
        ]
      }
    },
    {
      "id": "_trailer_type_raw", /* user-friendly ID for extracted target data */
      "method": {
        "id": "row", /* target data to extract is distributed on same horizontal line as anchor */
        "position": "right", /* default: right. target data is to left or right of anchor. enums: left | right. */
        "tiebreaker": "first"
      },
      "anchor": { /* an anchor is text that always occurs in the same position relative to your target data. */
        "match": [ /* array of Match objects. Sensible matches the last element
                      if each element matches a successive line in the document */
          {
            "text": "Equipment:", /* string to match */
            "type": "startsWith" /* line must start with the match */
          }
        ]
      }
    },
    {
      "id": "trailer_type", /* user-friendly ID for extracted target data */
      "method": {
        "id": "split",
        "separator": " - ",
        "source_id": "_trailer_type_raw",
        "index": 0
      }
    },
    {
      "id": "hide_fields", /* user-friendly ID for extracted target data */
      "method": { "id": "suppressOutput", "source_ids": ["_trailer_type_raw"] }
    },
    {
      "id": "test_field_xml_escapes_&_<stuff>", /* user-friendly ID for extracted target data */
      "method": {
        "id": "constant",
        "value": "blah 'blah' \"blah\" & <blah></blah>"
      }
    },
    {
      "id": "test_field_null", /* user-friendly ID for extracted target data */
      "method": { "id": "constant", "value": "" }
    }
  ],
  "postprocessor": {
    "type": "xml",
    "declaration": true,
    "selfCloseEmptyTags": false,
    "rule": {
      "eachKey": { /* builds an element object; its properties define the XML output */
        "tag": "DOCUMENTS", /* XML element name */
        "content": [ /* array — produces a sequence of child elements */
          {
            "eachKey": {
              "tag": "DOCUMENT", /* XML element name */
              "content": [
                {
                  "eachKey": {
                    "tag": "FORM", /* XML element name */
                    "content": "AU Tax Invoice Precise" /* hardcoded text content */
                  }
                },
                {
                  "eachKey": {
                    "tag": "FIELDS", /* XML element name */
                    "content": {
                      "mapObject": [ /* iterates over each field in parsed_document and operates on its key and value */
                        { "var": "" }, /* current context: the entire parsed_document */
                        {
                          "eachKey": { /* builds an element object for each field */
                            "tag": "FIELD", /* XML element name */
                            "attrs": { /* key-value pairs that become XML attributes, e.g. name="load_id" type="number" */
                              "eachKey": {
                                "name": { "var": "key" }, /* current field's ID becomes the attribute value */
                                "type": { "var": "value.type" } /* current field's data type becomes the attribute value */
                              }
                            },
                            "content": { "var": "value.value" } /* current field's extracted value becomes text content */
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

**Example document**<br />The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/postprocessor_xml_rate_confirmation.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/postprocessor_xml_rate_confirmation.pdf) |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------- |

**Output**

```json
/* POSTPROCESSED OUTPUT */
/* postprocessorOutput is a JSON string; see below for formatted XML */

{
  "postprocessorOutput": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>..."
}
```

```xml
<!-- postprocessorOutput value, formatted for readability -->

<DOCUMENTS><DOCUMENT><FORM>AU Tax Invoice Precise</FORM><FIELDS><FIELD name=\"load_id\" type=\"number\">123456789</FIELD><FIELD name=\"trailer_type\" type=\"string\">Van</FIELD><FIELD name=\"test_field_xml_escapes_&amp;_&lt;stuff&gt;\" type=\"string\">blah 'blah' \"blah\" &amp; &lt;blah&gt;&lt;/blah&gt;</FIELD><FIELD name=\"test_field_null\" type=\"\"></FIELD></FIELDS></DOCUMENT></DOCUMENTS>
```

```json
{
  "load_id": {
    "source": "123456789",
    "value": 123456789,
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
