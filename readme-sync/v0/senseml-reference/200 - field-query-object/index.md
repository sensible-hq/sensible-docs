---
title: "Field query object"
hidden: false
---

A field is the basic unit for writing a SenseML query to extract data from a PDF. The output of a field is a JSON key-value pair that structures the extracted data.  

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

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/basic_field.png)

As the preceding image shows, this is the output of the example field: 

```json
{
  "name_of_output_key": {
    "type": "string",
    "value": "Below the matching anchor, this is the data to extract. The anchor is a label for this data."
  }
}
```

Field parameters
----

Top-level components for a Field object are as follows:

| Parameter             | Value                                                        | Description                                                  |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                       | The ID is the name of the field. Sensible uses the ID as the key in the structured key/value output (`parsed_document` in the API output). If two fields share the same ID, then the second field acts as a fallback if the first returns null. Use fallbacks when you want to use a single config to extract data from a document whose formatting can vary. For example, a certificate of insurance can vary in formatting when a new revision is released. To capture differences in wording between revisions, you could define two fields with the same ID, which anchor on synonymous text that may be present or absent in different revisions. |
| anchor (**required**) | object                                                       | The anchor identifies one or more lines of *text* in the document at which Sensible starts executing a method. Can be a string, Match object, or array of Match objects. For more information, see [Anchor object](doc:anchor-object) and [Match object](doc:match-object). |
| method (**required**) | object                                                       | The method describes how Sensible expands from the anchor and grab the target data. For more information, see [Methods](doc:methods) and [Method object](doc:method-object). |
| type                  | `accountingCurrency`,<br/> `address`,<br/> `boolean`,<br/> `currency`,<br/> `date`,<br/> `distance`,<br/> `images`,<br/> `name`,<br/> `number`,<br/> `paragraph`, <br/>`percentage`,<br/>`periodDelimitedCurrency`,<br/> `string`,<br/> `table`,<br/> `weight` | The type of data to extract. This type information is included in the structured output. |
| match                 | `first`,`last`,`all`                                         | If there are multiple matches for the anchor, which one to use.  This parameter applies to the Match parameter as a whole in the Anchor object. This parameter does not apply to the Start or Stop parameters in the Anchor object (those parameters simply define areas of the document in which to find an anchor).<br/>`all` returns an array of matched values under a single key.  For example something like:  <br/>{<br/>  "name_of_output_key": [<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for first match"<br/>    },<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for second match"<br/>    } ]<br/>} |

Examples
----

The following field example uses all  top-level parameters:

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

- [Anchor object](doc:anchor-object)
- [Method object](doc:method-object)
