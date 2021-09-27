---
title: "API tute screenshot sources"
hidden: true
---

**TUTE SYNC**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quickstart_postman_import.png)

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/source/quickstart_postman_import.png)

```
curl --request POST \
  --url https://api.sensible.so/v0/extract/auto_insurance_quote \
  --header 'Authorization: Bearer 123abc' \
  --header 'Content-Type: application/pdf' \
  --data-binary '@/PATH_TO_DOWNLOADED_PDF/auto_insurance_anyco_golden.pdf'
```



---



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_1.png)

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/source/api_quickstart_postman_1.png)

```json
curl --request POST 'https://api.sensible.so/v0/extract_from_url/auto_insurance_quote' \
--header 'Authorization: Bearer 123abc' \
--header 'Content-Type: application/json' \
--data-raw '{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf"}'
```

-----

**_2**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_2.png)

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/source/api_quickstart_postman_2.png)

```json
curl --request GET 'https://api.sensible.so/v0/documents/14d82783-c12b-4e70-b0ae-ca1ce35a9836' \
--header 'Authorization: Bearer 123abc'
```

----

**_3**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_3.png)
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/source/api_quickstart_postman_3.png)

```
curl --request POST 'https://api.sensible.so/v0/generate_upload_url/auto_insurance_quote' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer 123abc'
```

**_4**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_postman_4.png)
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/source/api_quickstart_postman_4.png)

```
curl --request PUT 'https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/fc3484c5-3f35-4129-bb29-0ad1291ee9f8/EXTRACTION/14d82783-c12b-4e70-b0ae-ca1ce35a9836.pdf?AWSAccessKeyId=ASIAR355P7ASRMWOLX6W&Expires=1623790786&Signature=REDACTED-amz-security-token=REDACTED' \
--data-binary '@/PATH_TO_DOWNLOADED_PDF/auto_insurance_anyco_golden.pdf'
```



WEBHOOK

**webhook_2**

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/api_quickstart_webhook_2.png)
![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/source/api_quickstart_webhook_2.png)

```json
{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/auto_insurance_anyco_golden.pdf",
"webhook": {"url":"https://webhook.site/b37c53a3-fb75-48d6-df696ebd1388","payload":"some info you want to include that is additional to the default payload, which includes extraction id, type, and parsed doc"}}
```

