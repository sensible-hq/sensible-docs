---
title: "Field query object"
hidden: false
---

A field is the basic *SenseML* query unit for extracting a piece of document data. SenseML is a query language that lets you extract structured data from documents, for example, from PDFs.  The output of a field is a JSON key-value pair that structures the extracted data. 

A field uses a *method* to extract data.  SenseML contains *layout-based* and *large language model (LLM)-based* methods. 

Here's a simple example of a layout-based field and its output:

#### Field query

```json
{
 "fields": [
   {
     /* find the first box in the document 
         containing the text 'rents'
        and return all the other text in the box */
     "anchor": "rents",
     "id": "rents_income",
     "method": {
       "id": "box",
     }
   }
 ]
}
```

#### Extracted field output

```json
{
  "rents_income": {
    "type": "string",
    "value": "$ 4,200"
  }
}
```

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/box_1099.png)



The following example shows the syntax for all the top-level parameters of the Field object:

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

For more information, see the following sections.

[**Parameters**](doc:field-query-object#parameters)
[**Examples**](doc:field-query-object#examples)
[**Notes**](doc:field-query-object#notes)

Parameters
====

The Field query object has the following top-level parameters:

| Parameter             | Value                                                        | Description for layout-based methods                         | Description for LLM-based methods                            |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| id (**required**)     | string                                                       | Sensible uses the ID as the key in the structured key/value output. In the API response, this output is in the `parsed_document` object.<br/><br/>If a field fails and returns null, you can specify a backup, or fallback field to target the same data with a different method. To specify fallbacks between fields, specify consecutive fields that use the same ID. For more information, see [Fallback fields](doc:fallbacks). | Same                                                         |
| anchor                | string, [Match object](doc:match), or array of Match objects | **Required**<br/> Matched text that narrows down the location of the target data to extract. <br/> For more information, see [Anchor object](doc:anchor). | **Optional** <br/>If the matched text is present anywhere in the document, Sensible runs the method on the whole document, otherwise it returns `null`.   For more information, see [Anchor object](doc:anchor). |
| method (**required**) | object                                                       | Defines how to spatially expand out from the anchor and extract the target data. Use for documents that have a relatively consistent spatial layout. For example, 1040 forms have relatively consistent layout. For more information, see [Layout-based methods](doc:layout-based-methods). | Describes the contents of the target data to extract in natural-language prompts for an LLM. Use for documents that have a relatively inconsistent spatial layout, for example, legal contracts. For more information, see [LLM-based methods](doc:llm-based-methods). |
| type                  | see [Types](doc:types)                                       | The data type to extract, for example, a currency, an address, or a custom type you define. This structured output includes the type information. If the field captures other data in addition to the data matching the type, Sensible suppresses the additional data from the output. For more information, see [Types](doc:types). | same                                                         |
| match                 | `first`,`last`,`all`, `allWithNull`,`mostFrequent`           | If there are multiple anchors, specifies which one to use to extract output for layout-based methods. <br/> <br/>- `first`  specifies the first anchor in the document that returns non-null output.<br/><br/>- `last` specifies the last anchor in the document that returns non-null output.<br/><br/>- `all` matches all anchors and returns non-null extracted output under a single key. For example, something like:  <br/>{<br/>  "name_of_output_key": [<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for first anchor match"<br/>    },<br/>    {<br/>      "type": "string",<br/>      "value": "extracted data for second anchor match"<br/>    } ]<br/>}<br/><br/><br/>- `allWithNull`  matches all anchors and returns extracted output, including null output, under a single key. For example, use this option if you're using the [Zip computed field method](doc:zip) to zip together parallel arrays, where array elements can be nulls. For an example, see [Zip](doc:zip#match-with-null-zip).<br/><br/>- `mostFrequent` matches all anchors, extracts the corresponding output, then returns the most frequently occurring non-null output. This is useful for OCR text, like poor-quality scans or photographs. For example, a scanned document repeats a box titled `1 Wages` four times with the same dollar value, `21850.20`. Due to OCR errors, the extracted outputs are `21050.20`, `21850.20`, `21850.20` and `21850.58`.  This option returns the most frequent, and therefore the mostly likely correct output,  `21850.20`. | not applicable                                               |

Examples
====

## Example 1

The following example shows a layout-based field and an LLM-based field.

**Config**

```json
{
  "fields": [
    {
      /* LAYOUT-BASED EXAMPLE */
      "id": "name_of_output_key",
      /* an anchor is some text to match. define complex anchors using match
         arrays 
      */
      "anchor": "here's an anchor",
      /* this method uses spatial information 
         to locate the target data relative to the anchor 
      */
      "method": {
        "id": "label",
        /* target data is below the anchor */
        "position": "below"
      }
    },
    /* LLM-BASED EXAMPLE */
    {
      "id": "overview_table",
      "method": {
        /* this method uses LLMs to search
           for your target data based on your prompts ("descriptions") 
        */
        "id": "nlpTable",
        "description": "table describing SenseML",
        "columns": [
          {
            "id": "attribute",
            "description": "attribute of SenseML",
          },
          {
            "id": "description",
            "description": "description ",
          }
        ]
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/basic_field.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/basic_field.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "name_of_output_key": {
    "type": "string",
    "value": "Below the matching anchor, this is the data to extract. The anchor is a label for this data."
  },
  "overview_table": {
    "columns": [
      {
        "id": "attribute",
        "values": [
          {
            "value": "key concepts",
            "type": "string"
          },
          {
            "value": "key method categories",
            "type": "string"
          }
        ]
      },
      {
        "id": "description",
        "values": [
          {
            "value": "Fields, anchors, and methods",
            "type": "string"
          },
          {
            "value": "LLM-based, layout-based, and computed",
            "type": "string"
          }
        ]
      }
    ],
    "title": {
      "type": "string",
      "value": "SenseML overview"
    }
  }
}
```




Next
===

The Field object contains:

- [Anchor object](doc:anchor)
- [Method object](doc:method)
