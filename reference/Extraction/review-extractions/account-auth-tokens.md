---
title: Get token for review link
excerpt: >-
  Use this endpoint to provide a [reviewer](doc:human-review) with a "magic
  link" they can use to 

  approve, reject, and edit extracted document data without logging into a
  Sensible account. 

  This endpoint's response includes an authorization token you can use to
  compose the magic link. 

  For information about implementing human review, see [Human review
  implementation](doc:human-review-implementation).

  For example, for an extraction id `b84bd1c8-113e-4e1e-8462-379f0dde2abf`, make
  the following request:


  ```curl

  curl --location 'https://api.sensible.so/v0/account/auth_tokens' \

  --header 'Content-Type: application/json' \

  --header 'Authorization: Bearer YOUR_API_KEY' \

  --data '{
      "grants": [
          {
              "route": "/documents/{id}",
              "method": "GET",
              "path": {
                  "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf"
              }
          },
          {
              "route": "/extractions/{id}",
              "method": "PUT",
              "path": {
                  "id": "b84bd1c8-113e-4e1e-8462-379f0dde2abf"
              }
          }
      ],
      "expires": "2025-01-15T22:14:35.720Z"
  }'


  ```
api:
  file: extraction.json
  operationId: account-auth-tokens
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---