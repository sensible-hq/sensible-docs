---
title: "excel examples"
hidden: true
---

This topic describes how Sensible converts documents such as PDFs into Excel spreadsheets. To get output from a document structured as a spreadsheet with labeled columns, you must first:

- Configure extractions for a document type, either using Sensible's using [SenseML](doc:senseml-reference-introduction) or using Sensible's [open-source configuration library](app.sensible.com/library). TODO UPDATE LINK. 
- Run an extraction on a target document that belongs to your document type using the [Sensible app](app.sensible.com/quick-extract) or the [Sensible API](https://docs.sensible.so/reference/choosing-an-endpoint). Both these options then allow you to download a spreadsheet of the extraction results.

Sensible transforms its JSON API extraction output using the following rules:

- Each document transforms into one Excel file. In the file;
- the `fields` sheet lists each piece of document data that can be represented as a single cell value. For example, an extracted total monthly mortgage dollar amount.
- `<field_id>` sheets hold more complex pieces of document data. For example, an extracted table.
- `<field_id>.<index>` sheets hold complex repeating document data. For example, an extracted claims loss run.
- TBD TODO: invoices?

For more information, see the following sections.

`fields` sheet
====

The `fields` sheet lists fields and their values as key-value dictionary, with the field ID as the column heading and value as the row. Sensible outputs a field to this sheet if the field:

- outputs a single `value`. For example, the [Box](doc:box), [Label](doc:label), [Row](doc:row) and [Region](doc:region) methods each output a single value.

- outputs a predictably short array of values that can easily be stringified in a single cell. Typically this is the result of a [Type](doc:types) configuration, for example, the [Name](doc:types#name) type always outputs an array.

Example
-----

Sensible converts the JSON extraction output from the [auto_insurance_anyco](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) example described in the [Getting started guide](doc:getting-started) to the following spreadsheet:

**Spreadsheet output**

[block:html]
{
  "html": "<div><iframe src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vRJO_nwPRVe84ZdAi-gc6mny0zhRO9iz4nclfEKSBFQWHotARcgUkwfcinpGJTzPM4GIoIvf6PcN7zv/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n\n<style></style>"
}
[/block]



**Example document**

The preceding spreadsheet contains data from the following example document:

| Example PDF | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco.pdf) |
| ----------- | ------------------------------------------------------------ |

**Example configuration**

See the [Getting started guide](doc:getting-started)  for the SenseML configuration for this example.

**JSON output**

The following JSON document extraction output is the source for this spreadsheet:

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





`<field_id>` sheets
====

Each  `<field_id>` sheet lists the output of a single field. Sensible outputs a field to this sheet if the field outputs multiple values. For example: 

- the Table methods, invoices, and other methods that output nested JSON objects.
- methods that output arrays of unpredictable length, for example, fields with `"match":"all"` configured.

Example
-----

Sensible converts the example JSON output from the [example PDF](TODO) described in the [Table](doc:table#examples) method to the following spreadsheet:

[block:html]
{
  "html": "<div><iframe src=\"https://docs.google.com/spreadsheets/d/e/2PACX-1vRU-wjC2m6F0ACgU1Ry_W1zggeb7-oM_tZZ7XAsadz8m7uzZos1TY7B0XLpGW79_7rgltqpj8eCB262/pubhtml?widget=true&amp;headers=false\"></iframe></div>\n\n<style></style>"
}
[/block]

The preceding example shows that the `fields` sheet lists the corresponding sheets for fields that have complex output.  In this case, you must click on the `agile_risks_table_updates_monthly` sheet to view the table output.

**Example document**

The preceding spreadsheet contains data from the following example document: 

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/table_dynamic.pdf) |
| ----------- | ------------------------------------------------------------ |



**Example configuration**

See the [Table method](doc:table#examples)  for the SenseML configuration for this example.



**JSON output**

The following JSON extraction output is the source for this spreadsheet:

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



`<field_id>.<index>` sheets
====

Each  `<field_id>.<index>` sheet lists the output of a single field that contains complex repeating data. This is the case for [Sections](doc:sections) output.







`section_group_id.*section_index*.child_group_id.*child_index*.field_id` 


invoices
====



