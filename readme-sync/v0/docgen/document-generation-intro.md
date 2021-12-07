---
title: "Document generation introduction"
hidden: true
---

 You can programmatically fill in templated forms with structured data using Sensible. As an overview, if you create a fillable form, either PDF or HTML, and add unique identifier to fillable elements, like this: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/docgen-1.png)

then you can use Sensible's generation API to feed in data to the fillable elements:

```json
{

  "customer": {
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "06/24/1979"
  },

  "addresses":[
      {
          "street_address": "111 Center Street",
          "zip_code": "78123"
      },
      {
          "street_address": "123 Main Street",
          "zip_code": "78125"
      }
  ],
  "contract": {
    "start_date": "01/01/2022",  
  },
}


```

and return a filled document, like this:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/docgen-2.png)

Complete these setup tasks for each fillable form:

1. Email the fillable form to Sensible customer support at support@sensible.so.
2. Write a mapping between the IDs in the fillable form to the json keys you submit to the generation API and email it to Sensible customer support. For example:

```json
[
  {
    "document": {
      "type": "pdf",
      "name": "customer_contract"
    },
    "mapping": {
     "customerName": {
        "method": "concat",
        "sources": ["customer.first_name", "customer.last_name"]
      },
      "customerDob": "customer.birth_date",  
      "customerStrAdr": "addresses.1.street_address",
      "contractStart": "contract.start_date",

    }
  }
]

```

Notes
---


Sensible currently supports filling text fields, not boolean form elements like checkboxes or radio buttons.
