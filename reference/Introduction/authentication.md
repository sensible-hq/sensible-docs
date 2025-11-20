---
title: Authentication
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: noindex
next:
  description: ''
---
Sensible uses API keys to authenticate requests. Find your API key on your [Account page](https://app.sensible.so/account/) in the Sensible app. If you're having trouble with your current key, please reach out to support@sensible.so. Keep your API keys secure and do not share them publicly accessible areas such as GitHub, client-side code, etc. 

Authentication to the API is performed via Bearer Authentication. Provide your API key as the bearer auth value, for example:
```
curl --request POST \
       --url "https://api.sensible.so/v0/extract/<TYPE>" \
       --header "Authorization: Bearer <YOUR_API_KEY>" \
       --header "Content-Type: application/pdf" \
       --data-binary "@your_doc.pdf" \
```