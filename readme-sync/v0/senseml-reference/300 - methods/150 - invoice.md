---
title: "Invoice"
hidden: false
---
Identical to the [Table method](doc:table), but also returns detected invoice metadata.

Parameters
====
**Note:** For the full list of parameters available for this method, see [Global parameters for methods](doc:method-object#section-global-parameters-for-methods). The following table only shows parameters most relevant to or specific to this method.


| key     | value                                                        | description                                                  |
| :------ | :----------------------------------------------------------- | :----------------------------------------------------------- |
| id      | `invoice`                                                    |                                                              |
| columns |                                                              | TODO: An array of objects with the following parameters: An array of objects with the following parameters: <br/> -`id` (**required**): The id for the column in the extraction output <br/> - `index` (**required**): A zero-based column index <br/>-`type` : The type of the value in the table cell. See a list of possible types in [Field query object](doc:field-query-object)) <br/> -`isRequired` (default: false): If true, the extraction does not return rows where a value is not present in this column. |
| stop    | [Matcher](https://unpublished-sandbox.readme.io/docs/matcher) | optional, default: none. A [Matcher](https://unpublished-sandbox.readme.io/docs/matcher) to stop extraction. With `stop` defined, the engine selectively OCR the pages from the starting anchor to the page with the stop match. Otherwise the engine OCR all pages. |

Examples
====

The following image shows extracting two invoices for 2 items that have variably formatted invoices

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/invoice_example.png)


You can try out this example yourself in the Sensible app using the following downloadable PDF and config:

| Example PDF for invoice | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/example_invoice.pdf) |
| ----------------------- | ------------------------------------------------------------ |

This example uses the following config:

```json
{
  "fields": [
    {
      "id": "invoice_item_1",
      "type": "table",
      "anchor": "item 1",
      "method": {
        "id": "invoice",
        "columns": [
          {
            "id": "quantity",
            "terms": [
              "quantity",
              "ordered",
            ],
            "isRequired": true
          },
          {
            "id": "sku",
            "terms": [
              "sku",
              "item code",
            ],
            "isRequired": true
          },
          {
            "id": "unit_price",
            "terms": [
              "unit price",
            ],
            "stopTerms": [
              "total"
            ],
            "type": "currency",
          },
          {
            "id": "description",
            "terms": [
              "description",
              "material description",
            ],
            "isRequired": true
          },
          {
            "id": "total_price",
            "terms": [
              "final price",
              "total price"
            ],
            "type": "currency",
            "isRequired": true
          }
        ]
      }
    },
    {
      "id": "invoice_item_2",
      "type": "table",
      "anchor": "item 2",
      "method": {
        "id": "invoice",
        "columns": [
          {
            "id": "quantity",
            "terms": [
              "quantity",
              "ordered",
            ],
            "isRequired": true
          },
          {
            "id": "sku",
            "terms": [
              "sku",
              "item code",
            ],
            "isRequired": true
          },
          {
            "id": "unit_price",
            "terms": [
              "unit price",
            ],
            "stopTerms": [
              "total"
            ],
            "type": "currency",
          },
          {
            "id": "description",
            "terms": [
              "description",
              "material description",
            ],
            "isRequired": true
          },
          {
            "id": "total_price",
            "terms": [
              "final price",
              "total price"
            ],
            "isRequired": true
          }
        ]
      }
    },
  ]
}
```

And the example output is the following:

```json
{
  "invoice_item_1": {
    "metadata": {
      "items": {
        "value": "",
        "type": "string"
      }
    },
    "columns": [
      {
        "id": "quantity",
        "values": [
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
          }
        ]
      },
      {
        "id": "description",
        "values": [
          {
            "value": "Rubber boots (blue)",
            "type": "string"
          }
        ]
      },
      {
        "id": "unit_price",
        "values": [
          {
            "source": "$10.99",
            "value": 10.99,
            "unit": "$",
            "type": "currency"
          }
        ]
      },
      {
        "id": "total_price",
        "values": [
          {
            "source": "$21.98",
            "value": 21.98,
            "unit": "$",
            "type": "currency"
          }
        ]
      }
    ]
  },
  "invoice_item_2": {
    "metadata": {
      "items": {
        "value": "",
        "type": "string"
      }
    },
    "columns": [
      {
        "id": "quantity",
        "values": [
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
          }
        ]
      },
      {
        "id": "description",
        "values": [
          {
            "value": "Rubber boots (blue)",
            "type": "string"
          }
        ]
      },
      {
        "id": "unit_price",
        "values": [
          {
            "source": "$10.99",
            "value": 10.99,
            "unit": "$",
            "type": "currency"
          }
        ]
      },
      {
        "id": "total_price",
        "values": [
          {
            "value": "$21.98",
            "type": "string"
          }
        ]
      }
    ]
  }
}
```

