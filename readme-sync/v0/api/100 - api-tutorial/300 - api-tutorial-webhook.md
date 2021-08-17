---
title: "Try a webhook"
hidden: false
---

For asynchronous extractions, you can retrieve extraction results using either API endpoints or a webhook.  A webhook allows you to receive the extraction as a push, rather than waiting for responses from API endpoints.  

For this tutorial, let's try a webhook in combination with the `/extract_from_url/` endpoint.

Prerequisites
====

Set up a working asynchronous request. For this example, follow the steps in [Extract from a URL you provide](doc:api-tutorial-async#section-extract-from-a-url-you-provide ) to create an `/extract_from_url/` request in Postman.


Configure the webhook
====

1. Generate a destination for the webhook: navigate to [https://webhook.site/](https://webhook.site/) to automatically create a unique test page:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_1.png)
**Note:** Use this website [only for testing](https://webhook.site/terms). In production, implement your own destination for the webhook payload.

2. Copy the following code sample, and replace `YOUR_UNIQUE_URL` with your uniquely generated webhook.site URL:

```json
{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf",
"webhook": {"url":"YOUR_UNIQUE_URL","payload":"some info you want to include that is additional to the default payload, which includes extraction id, type, and parsed doc"}}
```

3. In your `/extract_from_url` request in Postman, replace the content of  the **Body** tab with the preceding code sample:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_2.png)

Check the webhook response
====

5. Click **Send** in Postman.
6. Visit your unique URL at webhook.site to verify there is a response like the following: 

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_3.png)
