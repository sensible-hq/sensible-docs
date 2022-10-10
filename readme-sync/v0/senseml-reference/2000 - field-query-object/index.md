---
title: "Field query object"
hidden: false
---

A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. 

[**Parameters**](doc:field-query-object#parameters)
[**Examples**](doc:field-query-object#examples)
[**Notes**](doc:field-query-object#notes)

Here is a simple example of a field: 

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

The following image shows this example in the Sensible app:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/basic_field.png)

As the preceding image shows, this is the output of the example field: 

```json
{
  "name_of_output_key": {
    "type": "string",
    "value": "Below the matching anchor, this is the data to extract. The anchor is a label for this data."
  }
}
```

Parameters
====

The Field object has the following top-level parameters:

| Parameter             | Value                                               | Description                                                  |
| --------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)     | string                                              | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` section.<br/>To specify fallbacks, use the same ID in multiple fields. Succeeding fields act as fallbacks if the first returns null. For example, to capture differences in wording between document revisions, define two fields with the same ID, which anchor on synonymous text that may be present or absent in different document revisions. Fallback fields can be of any kind. For example, you can fallback from a field, to a computed field, to a section group. Fallbacks don't work across nested structures. For example, you can't fall back from a parent section group's field to a child section group's field. |
| anchor (**required**) | object                                              | The anchor identifies one or more lines of text in the document at which Sensible starts executing a method. Can be a string, Match object, or array of Match objects. For more information, see [Anchor object](doc:anchor) and [Match object](doc:match). |
| method (**required**) | object                                              | The method describes how Sensible expands from the anchor and extracts the target data. For more information, see [Methods](doc:methods) and [Method object](doc:method). |
| type                  | see [Types](doc:types)                              | The data type to extract, for example, a currency, an address, or a custom type you define. This structured output includes the type information. If the field captures other data in addition to the data matching the type, Sensible suppresses the additional data from the output. For more information, see [Types](doc:types). |
| match                 | `first`,`last`,`all`, `allWithNulls`,`mostFrequent` | If there are multiple matches for the anchor, specifies which one to use. <br/> <br/>- `all` matches all anchors and returns non-null extracted values under a single key. For example, something like:  <br/>{<br/>  "name_of_output_key": [<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for first anchor match"<br/>    },<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for second anchor match"<br/>    } ]<br/>}<br/><br/><br/>- `allWithNulls`  matches all anchors and returns extracted values, including null values, under a single key. For example, use this option if you're using the [Zip computed field method](doc:zip) to zip together parallel arrays, where array elements can be nulls. For an example, see the Examples section.<br/><br/>- `mostFrequent` matches all anchors, extracts the corresponding values, then returns the most frequently occurring value. This is useful for OCR text, like poor-quality scans or photographs. For example, a scanned document repeats a box titled `1 Wages` four times with the same dollar value, `21850.20`. Due to OCR errors, the extracted values are `21050.20`, `21850.20`, `21850.20` and `21850.58`.  This option returns the most frequent, and therefore the mostly likely correct value,  `21850.20`. |

Examples
====

Example 1
-----


The following example shows all the top-level parameters of the Field object:

```json
{
  "fields": [
    {
      "id": "name_of_output_key",
      "anchor": "text to match",        
      "type":"accountingCurrency",
      "match":"last",
      "method": {
        "id": "row",
        "position": "right",
      }
    }
  ],
}
```

Example 2
----

The following example shows using `"match":"allWithNull"` to return parallel arrays of phones and last names. If you used `"match":"all"`, the missing phone number for claimant Badawi would result in that claimant's omission from the zipped `name_and_phone` array.



**Config**

```json
{
  "preprocessors": [
    {
      "type": "splitLines",
      "minSpaces": 3
    }
  ],
  "fields": [
    {
      /* using `allWithNull` creates a 5-element array
         with one null element (phone for Badawi).
         Using `all  would create a 4-element array  */
      "id": "phone_number",
      "match": "allWithNull",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "phone number"
        }
      },
      "method": {
        "id": "row"
      }
    },
    {
      /* 5 element array results from either `all` or 
         `allWithNull`, because no last 
         names are missing in doc */
      "id": "last_name",
      "match": "allWithNull",
      "anchor": {
        "match": {
          "type": "startsWith",
          "text": "claimant last name"
        }
      },
      "method": {
        "id": "label",
        "position": "right"
      }
    }
  ],
  "computed_fields": [
    {
      /* if you used `all` instead of `allWithNull`,
         `name_and_phone` zipped output
         would omit claimant Bawadi, because Zip 
         method joins arrays up to 
         their maximum shared length. */
      "id": "name_and_phone",
      "method": {
        "id": "zip",
        "source_ids": [
          "phone_number",
          "last_name"
        ]
      }
    },
    {
      "id": "hide_unzipped_fields",
      "method": {
        "id": "suppressOutput",
        "source_ids": [
          "phone_number",
          "last_name"
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/all_with_null.png)

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/all_with_null.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

```json
{
  "name_and_phone": [
    {
      "phone_number": {
        "type": "string",
        "value": "512 409 8765"
      },
      "last_name": {
        "type": "string",
        "value": ": Diaz"
      }
    },
    {
      "phone_number": null,
      "last_name": {
        "type": "string",
        "value": ": Badawi"
      }
    },
    {
      "phone_number": {
        "type": "string",
        "value": "505 238 8765"
      },
      "last_name": {
        "type": "string",
        "value": ": Levy"
      }
    },
    {
      "phone_number": {
        "type": "string",
        "value": "860 231 8344"
      },
      "last_name": {
        "type": "string",
        "value": ": Zenfell"
      }
    },
    {
      "phone_number": {
        "type": "string",
        "value": "312 242 9856"
      },
      "last_name": {
        "type": "string",
        "value": ": Smith"
      }
    }
  ]
}
```

Next
===

The Field object contains:

- [Anchor object](doc:anchor)
- [Method object](doc:method)
