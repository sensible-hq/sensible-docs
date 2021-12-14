---
title: "Document generation introduction"
hidden: true
---

 You can programmatically fill in templated forms with structured data using Sensible. First, create a fillable template document, either PDF or HTML, and add unique identifier to fillable field elements, like this: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/docgen-1.png)

then you can use Sensible's [generation API](https://docs.sensible.so/reference/fill-form) to specify the data you want to use to populate the fillable fields:

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

Get started
---

For each unique fillable template you create, email the following to Sensible customer support at support@sensible.so to get started with calling the API: 

- The fillable template document.

- A mapping you write between the field IDs you created in the fillable document template  and the JSON keys you submit to the generation API. See [Mappings](doc:document-generation-intro#mappings) for more information. 

- A name for the "generator" for this fillable form. A generator can contain multiple templates and mappings.  For example, if you submit a `6_month_customer_contract.pdf` template, Sensible can store it in a `customer_contracts` generator along with a `3_month_customer_contract.pdf` and other related templates and their mappings.

Mappings
----
The following example JSON maps the names of field IDs in a fillable PDF named `customer_contract_6_months` to JSON keys used in the API call (using JSON  dot notation):


```json
[
  {
    "template": {
      "type": "pdf",
      "name": "customer_contract_6_months"
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

- To fill the PDF field `customerName`, take the values of the JSON keys `customer.first_name`, `customer.last_name` in the API request and concatenate them. 
- To fill the PDF field `customerStrAdr`, get the second element in the addresses array in the API request, then get the value of the `street_address` key.
- To fill the PDF field `contractStart`, look for the JSON key `contract.start_date` in the API request. If Sensible doesn't find that key, then fallback to an alternative and synonymous key, `policy.start_date`.

Portfolio generation
----

You can generate a portfolio file containing multiple filled documents in one file.  For example, if you write a mapping like this:

```json
[
  {
    "template": {
      "type": "pdf",
      "name": "auto_policy_declaration"
    },
    "mapping": {
     "customerName": "customer.full_name",
     "totalPremium": "auto_policy.total_premium",  
    }
  },
  {
    "template": {
      "type": "pdf",
      "name": "umbrella_policy_declaration"
    },
    "mapping": {
     "customerName": "customer.full_name",
     "totalPremium": "umbrella_policy.total_premium",  
    }
  }, 
]
```

You can use one API request with one JSON payload to generate a portfolio file containing two separate filled out forms, an auto policy declaration and an umbrella policy declaration.

Notes
---

Sensible currently supports the following:

- fillable text fields, not for example checkboxes or radio buttons.
- PDF templates, not for example HTML.
- the concat method, not for example split or join.
