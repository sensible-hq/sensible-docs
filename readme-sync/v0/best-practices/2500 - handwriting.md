---
title: "Extracting handwriting"
hidden: true

---



```
{
    "id": "7c269ef2-f9f1-4271-82e0-79b60887f45a",
    "created": "2021-09-29T17:03:06.058Z",
    "status": "COMPLETE",
    "types": [
        "auto_insurance_quote",
        "loss_run"
    ],
    "documents": [
        {
            "documentType": "auto_insurance_quote",
            "configuration": "anyco_quote",
            "startPage": 0,
            "endPage": 0,
            "output": {
                "parsedDocument": {
                    "policy_period": {
                        "type": "string",
                        "value": "April 14, 2021 - Oct 14, 2021"
                    },
                    "comprehensive_premium": {
                        "source": "$150",
                        "value": 150,
                        "unit": "$",
                        "type": "currency"
                    },
                    "property_liability_premium": {
                        "source": "$10",
                        "value": 10,
                        "unit": "$",
                        "type": "currency"
                    },
                    "policy_number": {
                        "value": "123456789",
                        "type": "string"
                    }
                },
                "configuration": "anyco_claims",
                "validations": [],
                "validation_summary": {
                    "fields": 4,
                    "fields_present": 4,
                    "errors": 0,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        },
        {
            "documentType": "auto_insurance_quote",
            "configuration": "anyco_quote",
            "startPage": 1,
            "endPage": 1,
            "output": {
                "parsedDocument": {
                    "policy_period": {
                        "type": "string",
                        "value": "May 20, 2021 - Nov 20,"
                    },---
title: "Extracting handwriting"
hidden: true

---

This topic contains tips and tricks for extracting handwriting:

- **Choosing an OCR engine** Google OCR instead of Microsoft OCR. To configure OCR, click the gear icon for the Document Type and select **Google**: 

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/merge_lines_ocr_1.png)

  

- **Defining regions** can occupy an unpredictable region or even overlap other lines. Rather than attempting to draw a large region to encapsulate the handwriting, it's sometimes better to draw a box with a small height and long width that runs through the middle of the handwriting, as the following image shows:

  ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/handwriting_1.png) 

  For more information about how Sensible determines whether to extract a line that partially overlaps a region, see [Region](doc:region).

- **Correcting for vertical misalignment** jitter in the vertical positions of handwritten lines can cause Sensible to incorrectly sort lines that a human reader interprets as following left to right. The Sort Lines parameter corrects this problem by sorting lines by their likely reading order. For more information, see [the Sort Lines example](doc:method#sort-line-example).







