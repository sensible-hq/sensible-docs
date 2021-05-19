---
title: "Field query object"
hidden: false
---

A field is the basic unit for writing a SenseML query to extract data from a PDF. The output of a field is a JSON key-value pair that structures the extracted data.  

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

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/images/v0/basic_field.png)

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
| id (**required**)     | string                                                       | The ID is the name of the field, which SenseML uses as the key in the structured key/value output. |
| anchor (**required**) | object                                                       | The anchor identifies one or more lines of *text* in the document where we start method execution. Can be a string, [Match object](doc:anchor#section-match-object) or array of Match objects. |
| method (**required**) | object                                                       | The method describes how we want to expand from that anchor and grab your target data. |
| type                  | `accountingCurrency`, `address`, `boolean`, `currency`, `date`, `distance`, `images`, `name`, `number`, `paragraph`, `percentage`, `string`, `table`, `weight` | The type of data we want to extract. This type is also specified in the structured output. |
| match                 | `first`,`last`,`all`                                         | If there are multiple matches for the anchor, which one to use.  <br/>`all` returns an array of values for each match, under a single output key.  For example something like:  <br/>{<br/>  "name_of_output_key": [<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for first match"<br/>    },<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for second match"<br/>    } ]<br/>} |



Example
----
The following field example uses all the top-level parameters:

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





