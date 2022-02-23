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
----

The Field object has the following top-level parameters:

| Parameter             | Value                                                        | Description                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                       | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` section.<br/>To specify fallbacks, use the same ID in multiple fields. Succeeding fields act as fallbacks if the first returns null. For example, to capture differences in wording between document revisions, define two fields with the same ID, which anchor on synonymous text that may be present or absent in different document revisions. |
| anchor (**required**) | object                                                       | The anchor identifies one or more lines of text in the document at which Sensible starts executing a method. Can be a string, Match object, or array of Match objects. For more information, see [Anchor object](doc:anchor) and [Match object](doc:match). |
| method (**required**) | object                                                       | The method describes how Sensible expands from the anchor and extracts the target data. For more information, see [Methods](doc:methods) and [Method object](doc:method). |
| type                  | `accountingCurrency`,<br/> `address`,<br/> `boolean`,<br/> `currency`,<br/>`custom`<br/> `date`,<br/> `distance`,<br/> `images`,<br/> `name`,<br/> `number`,<br/> `paragraph`, <br/>`percentage`,<br/>`phoneNumber`,<br/> `string`,<br/> `table`,<br/> `weight` | The data type to extract. This structured output includes the type information. If the field captures other data in addition to the data matching the type, Sensible suppresses the additional data from the output. For more information, see [Types](doc:types). |
| match                 | `first`,`last`,`all`                                         | If there are multiple matches for the anchor, specifies which one to use. This parameter applies to the anchor's Match parameter, not to the Start or Stop parameters.<br/>`all` returns an array of matched values under a single key. For example, something like:  <br/>{<br/>  "name_of_output_key": [<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for first match"<br/>    },<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for second match"<br/>    } ]<br/>} |

Examples
----

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
