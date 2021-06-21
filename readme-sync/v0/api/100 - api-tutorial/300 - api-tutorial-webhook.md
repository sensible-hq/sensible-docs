---
title: "Try a webhook"
hidden: true
---

For asynchronous extractions, you can retrieve extraction results using either the `/documents` endpoint or a webhook.  For this tutorial, let's try a webhook in combination with the `/extract_from_url/` endpoint.

Prerequisites
====

Set up a working asynchronous request. For this example, follow the steps in [Extract from a URL you provide](doc:api-tutorial-async#section-extract-from-a-url-you-provide ) to create an `/extract_from_url/` request.


Set up the webhook
====

Generate a test destination for the webhook using a free service: 

1. Navigate to [https://webhook.site/](https://webhook.site/), and you should be directed to an automatically generated unique page for your testing:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_1.png)
**Note:** Don't use this website for production purposes. Use it only for testing. See their [Terms of service](https://webhook.site/terms).

2. Copy the unique URL generated for you by webhook.site, and paste it into the following code sample:

```json
{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf",
"webhook": {"url":"YOUR_UNIQUE_URL","payload":"some info you want to include that is additional to the default payload, which includes extraction id, type, and parsed doc"}}
```

3. In your `/extract_from_url` request in Postman, replace the content of  the **Body** tab with the preceding code sample:

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_2.png)

Check the webhook response
====

5. Click **Send** in Postman.
6. Check back at your unique URL at webhook.site, and you should see a response there like the following: 

![](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/api_quickstart_webhook_3.png)
