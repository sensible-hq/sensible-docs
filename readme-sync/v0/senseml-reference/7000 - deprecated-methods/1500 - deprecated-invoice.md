---
title: "(Deprecated) Invoice"
hidden: true
---
## Deprecated

This method is deprecated. [LLM-based methods](doc:instruct) replace this method.

## Description

This method is identical to the [(Deprecated) Table method](doc:deprecated-table), and also returns detected invoice metadata. This method accepts one invoice per document file. If the document contains multiple tables, the Invoice method returns the data for the table that is the best invoice candidate.

It's a best practice to create a single, flexible config that works for a variety of invoice formats. This is because invoices typically come from such a wide variety of vendors that it would be unmanageable to create a config for each vendor. Create a flexible config by using synonymous terms to identify invoice elements. For more information, see the [Examples section](doc:invoice#examples). 

[**Parameters**](doc:invoice#parameters)
[**Examples**](doc:invoice#examples)

Parameters
====
**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method#global-parameters-for-methods). The following table shows parameters most relevant to or specific to this method.


| key                  | value     | description                                                  |
| :------------------- | :-------- | :----------------------------------------------------------- |
| id (**required**)    | `invoice` | When you specify this method, you must also specify `"type": "table"` in the field's parameters. |
| columns **required** | array     | An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output. <br/> -`terms` (**required**): An array of terms to score positively during column recognition. For more information about scoring, see [bag of words](doc:bag-of-words) scoring. Usually, you include column heading terms in this array. <br/> -`stopTerms`: An array of terms to score negatively during column recognition. For more information about scoring, see [bag of words](doc:bag-of-words).<br/> -`type`: The table cell's type. For more information about types, see [Field query object](doc:field-query-object). <br/>  -`isRequired` (default false): If true, Sensible omits a row if its cell is empty in this column. If false, Sensible returns nulls for empty cells in the row. Note that if you set this parameter to true for one column, Sensible omits the row for *all* columns, even if the row had content under other columns. |


Examples
====

The following example shows using the Invoice method:

- It extracts the invoice table from a document that contains multiple tables.
- It extracts other invoice metadata from header and footer information in the invoice.
- This example uses a large number of synonymous terms for each invoice column, so it can parse invoices from a variety of vendors. 

**Config**


```json
{
  "fields": [
    {
      "id": "invoice",
      "type": "table",
      "method": {
        "id": "invoice",
        "columns": [
          {
            "id": "quantity",
            "terms": [
              "qty",
              "quantity",
              "ordered",
              "shipped",
              "ord"
            ],
            "isRequired": true
          },
          {
            "id": "sku",
            "terms": [
              "sku",
              "item number",
              "item no.",
              "item code",
              "product number",
              "product no.",
              "product code",
              "p.o.s."
            ],
            "isRequired": true
          },
          {
            "id": "description",
            "terms": [
              "description",
              "product",
              "material description",
              "product description"
            ],
            "isRequired": true
          },
          {
            "id": "unit_price",
            "terms": [
              "price",
              "unit price",
              "list",
              "sale",
              "pricing",
              "rate"
            ],
            "stopTerms": [
              "ext",
              "extendsion",
              "extd",
              "final",
              "total"
            ],
            "isRequired": true
          },
          {
            "id": "total_price",
            "terms": [
              "amount",
              "total",
              "extension",
              "final price",
              "extended amount",
              "extended",
              "ext price",
              "net extended",
              "extd. price",
              "sales amount",
              "total price",
              "sub total"
            ],
            "isRequired": true
          }
        ]
      },
      "anchor": {
        "match": {
          "type": "first"
        }
      }
    }
  ]
}
```

**Example document**
The following image shows the example document used with this example config:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main//readme-sync/assets/v0/images/final/invoice.png)

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/invoice.pdf) |
| ----------------------- | ------------------------------------------------------------ |

**Output**

```json
{
  "invoice": {
    "metadata": {
      "billing_address_recipient": {
        "value": "Cash sales-Anytown",
        "type": "string"
      },
      "customer_name": {
        "value": "Acme Inc",
        "type": "string"
      },
      "invoice_date": {
        "source": "06/21/21",
        "value": "2021-06-21T00:00:00.000Z",
        "type": "date"
      },
      "invoice_id": {
        "value": "19288685",
        "type": "string"
      },
      "invoice_total": {
        "source": "7,061.48",
        "value": 7061.48,
        "unit": "$",
        "type": "currency"
      },
      "items": {
        "value": "",
        "type": "string"
      },
      "shipping_address": null,
      "shipping_address_recipient": {
        "value": "Acme Inc",
        "type": "string"
      },
      "sub_total": {
        "source": "$6306.93",
        "value": 6306.93,
        "unit": "$",
        "type": "currency"
      },
      "total_tax": {
        "source": "450.00",
        "value": 450,
        "unit": "$",
        "type": "currency"
      }
    },
    "columns": [
      {
        "id": "quantity",
        "values": [
          {
            "value": "1x",
            "type": "string"
          },
          {
            "value": "4x",
            "type": "string"
          },
          {
            "value": "2x",
            "type": "string"
          }
        ]
      },
      {
        "id": "sku",
        "values": [
          {
            "value": "987654321",
            "type": "string"
          },
          {
            "value": "123456789",
            "type": "string"
          },
          {
            "value": "192837465",
            "type": "string"
          }
        ]
      },
      {
        "id": "description",
        "values": [
          {
            "value": "Standing desk",
            "type": "string"
          },
          {
            "value": "Office chair (gray)",
            "type": "string"
          },
          {
            "value": "Conference table (beige)",
            "type": "string"
          }
        ]
      },
      {
        "id": "unit_price",
        "values": [
          {
            "value": "$1,100.99",
            "type": "string"
          },
          {
            "value": "$550.99",
            "type": "string"
          },
          {
            "value": "$1,500.99",
            "type": "string"
          }
        ]
      },
      {
        "id": "total_price",
        "values": [
          {
            "value": "$1,100.99",
            "type": "string"
          },
          {
            "value": "$2,203.96",
            "type": "string"
          },
          {
            "value": "$3,001.98",
            "type": "string"
          }
        ]
      }
    ]
  }
}
```

