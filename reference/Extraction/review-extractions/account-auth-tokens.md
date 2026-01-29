---
title: Get token for review link
excerpt: "Use this endpoint to provide a [reviewer](doc:human-review) with a \"magic\
  \ link\" they can use to \napprove, reject, and edit extracted document data without\
  \ logging into a Sensible account. \nThis endpoint's response includes an authorization\
  \ token you can use to compose the magic link. \nFor information about implementing\
  \ human review, see [Human review implementation](doc:human-review-implementation).\n\
  For example, for an extraction id `b84bd1c8-113e-4e1e-8462-379f0dde2abf`, make the\
  \ following request:\n\n```curl\ncurl --location 'https://api.sensible.so/v0/account/auth_tokens'\
  \ \\\n--header 'Content-Type: application/json' \\\n--header 'Authorization: Bearer\
  \ YOUR_API_KEY' \\\n--data '{\n    \"grants\": [\n        {\n            \"route\"\
  : \"/documents/{id}\",\n            \"method\": \"GET\",\n            \"path\":\
  \ {\n                \"id\": \"b84bd1c8-113e-4e1e-8462-379f0dde2abf\"\n        \
  \    }\n        },\n        {\n            \"route\": \"/extractions/{id}\",\n \
  \           \"method\": \"PUT\",\n            \"path\": {\n                \"id\"\
  : \"b84bd1c8-113e-4e1e-8462-379f0dde2abf\"\n            }\n        }\n    ],\n \
  \   \"expires\": \"2025-01-15T22:14:35.720Z\"\n}'\n\n```\n"
api:
  file: openapi_extraction.json
  operationId: account-auth-tokens
hidden: false
metadata:
  description: 'null'
---
