---
title: "Document generation introduction"
hidden: true
---

 You can programmatically fill in templated forms with structured data using Sensible. As an overview, if you create a fillable form, either PDF or HTML, where you've added unique identifier to fillable elements, like this: 

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

To set this up, you have some initial configuration tasks for each fillable form:

1. Send the fillable form to Sensible. Contact customer support to do so.
2. To map the IDs in the fillable form to the json you submit to the generation API, send Sensible customer support a mapping configuration, like this:

```
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

