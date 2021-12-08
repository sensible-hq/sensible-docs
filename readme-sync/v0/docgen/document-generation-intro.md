---
title: "Document generation introduction"
hidden: true
---

 You can programmatically fill in templated forms with structured data using Sensible. First, create a fillable form, either PDF or HTML, and add unique identifier to fillable elements, like this: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/docgen-1.png)

then you can use Sensible's [generation API](https://docs.sensible.so/reference/fill-form) to populate the fillable elements with data:

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

Complete these setup tasks for each unique fillable form:

1. Email the fillable form you created to Sensible customer support at support@sensible.so. Sensible stores the form as a template for all subsequent API calls you make for that particular document.
2. Write a config to map between the IDs you created in the fillable form and the JSON keys you submit to the generation API,and email it to Sensible customer support. For example, the following JSON maps the fillable field ID `customerDob` in a fillable PDF named "customer_contract" to a JSON key used in the API call, `customer.birth_date` (using JSON  dot notation):

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
      "contractStart": ["contract.start_date", "policy.start_date" ]

    }
  }
]

```

This mapping specifies, for example:

- To fill the PDF field `customerName`, take the values of the json keys `customer.first_name`, `customer.last_name` in the API request and concatenate them. 
- To fill the PDF field `customerStrAdr`, get the second element in the addresses array in the API request, then get the value of the `street_address` key.
- To fill the PDF field `contractStart`, look for the json key `contract.start_date` in the API request. If Sensible doesn't find that key, then fallback to the alternative, `policy.start_date`.

TODO: what other methods do we provide except concat?  will we allow any other params except method and sources? 

**Notes (todo, put somewhere about fallbacks not just in the notes above)**







Portfolio generation
----

You can generate a portfolio file containing multiple documents in one file.  For example, if you write a config like this:

```json
[
  {
    "document": {
      "type": "pdf",
      "name": "auto_policy_declaration"
    },
    "mapping": {
     "customerName": "customer.full_name",
     "policyStart": "auto_policy.start_date",  
    }
  },
  {
    "document": {
      "type": "pdf",
      "name": "umbrella_policy_declaration"
    },
    "mapping": {
     "customerName": "customer.full_name",
     "policyStart": "umbrella_policy.start_date",  
    }
  }, 
]
```

You can use one API request with one JSON payload to generate a portfolio file containing two separate filled out forms, an auto policy declaration and an umbrella policy declaration.



Notes
---


Sensible currently supports filling text fields, not Boolean form elements like checkboxes or radio buttons.
