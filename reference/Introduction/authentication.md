---
title: Authentication
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
Sensible uses API keys to authenticate requests. Create and manage your API key on your [Account page](https://app.sensible.so/account/) in the Sensible app. You can create keys at different levels of security, including nonrecoverable keys or keys recoverable with an account password. Keep your API keys secure and do not share them in publicly accessible areas such as GitHub, client-side code, etc. 

To authenticate, provide your API key as the bearer authentication value. For example:

```
curl --request POST \
       --url "https://api.sensible.so/v0/extract/<TYPE>" \
       --header "Authorization: Bearer <YOUR_API_KEY>" \
       --header "Content-Type: application/pdf" \
       --data-binary "@your_doc.pdf" \
```