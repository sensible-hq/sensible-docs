---
title: "Document generation introduction"
hidden: true
---

 You can programmatically fill in templated forms with structured data using Sensible. As an overview, if you create a fillable form, either PDF or HTML, and add unique identifier to fillable elements, like this: 

![image-20211207124138972](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20211207124138972.png)

then you can use Sensible's generation API to feed in data to the fillable elements:

```json
{

  "customer": {
    "first_name": "John",
    "last_name": "Doe",
    "birth_date": "06/24/1979"
  },
  "contract": {
    "start_date": "01/01/2022",
  },
}


```

and return a completed document, like this:

![image-20211207124059598](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20211207124059598.png)

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
      "contractStartDate": "contract.start_date",
      "customerName": {
        "method": "concat",
        "sources": ["customer.first_name", "customer.last_name"]
      },
      "customerDob": "customer.birth_date"
    }
  }
]

```

Notes
---


Sensible currently supports filling text fields, not boolean form elements like checkboxes or radio buttons.
