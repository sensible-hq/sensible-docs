---
title: "Field query object"
hidden: false
---

A field is the basic SenseML query unit for extracting a piece of document data. The output of a field is a JSON key-value pair that structures the extracted data. 

[**Parameters**](doc:field-query-object#parameters)
[**Examples**](doc:field-query-object#examples)
[**Notes**](doc:field-query-object#notes)

Here's a simple example of a field: 

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

| Parameter                                                    | Value                                              | Description                                                  |
| ------------------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------ |
| id (**required**)                                            | string                                             | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` object.<br/>To specify fallbacks, use the same ID in multiple fields. Succeeding fields act as fallbacks if the first returns null.<br/>For example, to capture differences in wording between document revisions, define two fields with the same ID, which anchor on synonymous text that 's present or absent in different document revisions. <br/>Or, specify an optional anchor anywhere in a document for an LLM-based field, and fall back to a different field if the anchor isn't present. <br/>Fallback fields can be of any kind. For example, you can fallback from a field, to a computed field, to a section group.<br/>**Limitations:**<br/>- Fallbacks don't work across nested structures. For example, you can't fall back from a parent section group's field to a child section group's field.<br/>- Fallbacks don't work within a query group. To specify fallbacks, define them in separate query groups. |
| anchor (**required**) except for fields that use [LLM-based methods](doc:llm-based-methods) | object                                             | The anchor identifies one or more lines of text in the document at which Sensible starts executing a method. Can be a string, Match object, or array of Match objects. For more information, see [Anchor object](doc:anchor) and [Match object](doc:match). |
| method (**required**)                                        | object                                             | The method describes how Sensible expands from the anchor and extracts the target data. For more information, see [Methods](doc:methods), [LLM-based methods](doc:llm-based-methods), and [Method object](doc:method). |
| type                                                         | see [Types](doc:types)                             | The data type to extract, for example, a currency, an address, or a custom type you define. This structured output includes the type information. If the field captures other data in addition to the data matching the type, Sensible suppresses the additional data from the output. For more information, see [Types](doc:types). |
| match                                                        | `first`,`last`,`all`, `allWithNull`,`mostFrequent` | If there are multiple anchors, specifies which one to use to extract output. <br/> <br/>- `first`  specifies the first anchor in the document that returns non-null output.<br/><br/>- `last` specifies the last anchor in the document that returns non-null output.<br/><br/>- `all` matches all anchors and returns non-null extracted output under a single key. For example, something like:  <br/>{<br/>  "name_of_output_key": [<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for first anchor match"<br/>    },<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for second anchor match"<br/>    } ]<br/>}<br/><br/><br/>- `allWithNull`  matches all anchors and returns extracted output, including null output, under a single key. For example, use this option if you're using the [Zip computed field method](doc:zip) to zip together parallel arrays, where array elements can be nulls. For an example, see [Zip](doc:zip#match-with-null-zip).<br/><br/>- `mostFrequent` matches all anchors, extracts the corresponding output, then returns the most frequently occurring non-null output. This is useful for OCR text, like poor-quality scans or photographs. For example, a scanned document repeats a box titled `1 Wages` four times with the same dollar value, `21850.20`. Due to OCR errors, the extracted outputs are `21050.20`, `21850.20`, `21850.20` and `21850.58`.  This option returns the most frequent, and therefore the mostly likely correct output,  `21850.20`. |

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




Next
===

The Field object contains:

- [Anchor object](doc:anchor)
- [Method object](doc:method)
