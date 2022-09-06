---
title: "excel examples"
hidden: true
---

This topic describes how Sensible converts documents such as PDFs into Excel sheets. To get output from a document structured as an Excel file with labeled columns, you must first:

- Configure extractions for a document type, either using Sensible's using [SenseML](doc:senseml-reference-introduction) or using Sensible's [open-source configuration library](app.sensible.com/library). TODO UPDATE LINK. 
- Run an extraction on a target document that belongs to your document type using the [Sensible app](app.sensible.com/quick-extract) or the [Sensible API](https://docs.sensible.so/reference/choosing-an-endpoint). Both these options then allow you to download an Excel file of the extraction results.

Sensible transforms its JSON API extraction output using the following rules:

`fields` sheet
====

The `fields` sheet lists fields and their values as key-value dictionary, with the field ID as the column heading and value as the row. Sensible outputs a field to this sheet if the field:

- outputs a single `value`. For example, the [Box](doc:box), [Label](doc:label), [Row](doc:row) and [Region](doc:region) methods each output a single value.

- outputs a predictably short array of values that can easily be stringified in a single cell. Typically this is the result of a [Type](doc:types) configuration, for example, the [Name](doc:types#name) type always outputs an array.

**Example** 

Sensible converts the following extraction output from the [auto_insurance_anyco](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) example described in the [Getting started guide](doc:getting-started):

  ```json
  {
    "policy_period": {
      "type": "string",
      "value": "April 14, 2021 - Oct 14, 2021"
    },
    "comprehensive_premium": {
      "source": "$150",
      "value": 150,
      "unit": "$",
      "type": "currency"
    },
    "property_liability_premium": {
      "source": "$10",
      "value": 10,
      "unit": "$",
      "type": "currency"
    },
    "policy_number": {
      "value": "123456789",
      "type": "string"
    }
  }
  ```


to the  following Excel sheet:

<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRJO_nwPRVe84ZdAi-gc6mny0zhRO9iz4nclfEKSBFQWHotARcgUkwfcinpGJTzPM4GIoIvf6PcN7zv/pubhtml?widget=true&amp;headers=false"></iframe>

`<field_id>` sheets
====

Each  `<field_id>` sheet lists the output of a single field. Sensible outputs a field to this sheet if the field outputs multiple values. For example: 

- the Table methods, [sections](doc:sections), and other methods that output nested JSON objects. For more information about sections output, see the following section.
- methods that output arrays of unpredictable length, for example, fields with `"match":"all"` configured.

**Examples**

Sensible converts the following output from the [example PDF]() listed in the [Table](doc:table) method:

```json
{
  "agile_risks_table_updates_monthly": {
    "columns": [
      {
        "id": "col1_risk_description",
        "values": [
          {
            "value": "Poor task point estimation",
            "type": "string"
          },
          {
            "value": "Poor epic scope definition",
            "type": "string"
          },
          {
            "value": "Inadequate scrum master training",
            "type": "string"
          }
        ]
      },
      {
        "id": "rank_this_month",
        "values": [
          {
            "source": "3",
            "value": 3,
            "type": "number"
          },
          {
            "source": "1",
            "value": 1,
            "type": "number"
          },
          {
            "source": "2",
            "value": 2,
            "type": "number"
          }
        ]
      }
    ]
  }
}
```

To the following Excel output:

<iframe src="https://docs.google.com/spreadsheets/d/e/2PACX-1vRU-wjC2m6F0ACgU1Ry_W1zggeb7-oM_tZZ7XAsadz8m7uzZos1TY7B0XLpGW79_7rgltqpj8eCB262/pubhtml?widget=true&amp;headers=false"></iframe>

The preceding example shows that the `fields` sheet refers to sheets containing complex output. In this case, you must click on the `agile_risks_table_updates_monthly` sheet to view the table output.



- sections sheets - Sections have the same patterns as previously mentioned methods, with indexes to handle repeating output. For example, a sheet name can be: `section_group_id.*section_index*.child_group_id.*child_index*.field_id` 



Simple extracted values
---

Fields with a single value convert to a "fields" sheet.  For example, Sensible outputs these fields from [Getting started](doc:getting-started)

```json
{
  "fields": [
    {
      "id": "policy_period",
      "anchor": "policy period",
      "method": {
        "id": "label",
        "position": "right"
      }
    },
    {
      "id": "comprehensive_premium",
      "anchor": "comprehensive",
      "type": "currency",
      "method": {
        "id": "row",
        "tiebreaker": "second"
      }
    }
 }      
```

 to the following CSV:

![image-20220614102120649](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220614102120649.png)

Examples of methods that output single-value output include the following methods where match-all or other array params are disabled:

TODO convert to table, some have examples, some don't??? 

- Box

- Checkbox

- (document range?? passthrough?)

- Intersection

- Invoice `metadata` output

- Label

- Nearest Checkbox

- Regex

- Region

- Row(?)

- **computed**

- Concatenate

- Constant

- Mapper

- (pick values?)

- Split

  

For more examples, see the following: 

| simple fields    | TODO: use when adding docs to topics                         |                                                              |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| anyco            | https://docs.google.com/spreadsheets/d/1S5W9NO-5W51xxif29Aws6sojBiitONUpb-g4-6ANtaA/edit?usp=sharing | [Getting started][getting-started](doc:getting-started#csv-output) |
| invoice metadata | https://docs.google.com/spreadsheets/d/1vIiiFGwLYjT6CLx9BHBZdur9PdZ50lY-G3ae2CoPf9w/edit#gid=0 | [Invoice][doc:invoice#csv-output]                            |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |

