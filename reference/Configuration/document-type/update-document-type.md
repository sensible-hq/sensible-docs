---
title: Update document type
excerpt: >-
  Update an existing document type with new information. For example, use this
  endpoint to add validations:


  ```curl

  curl --location --request PUT
  'https://api.sensible.so/v0/document_types/<TYPE_ID>' \

  --header 'Authorization: Bearer YOUR_API_KEY' \

  --header 'Content-Type: application/json' \

  --data-raw '{"schema":{"validations":[{"description":"example validation to
  test broker email
  format","condition":{"match":[{"var":"broker\\.email.value"},"^\\S+\\@\\S+$"]},"severity":"warning","fields":["test"]}]}}
  '

  ```
api:
  file: configuration-4.json
  operationId: update-document-type
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---