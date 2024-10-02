---
title: "Multi-document extractions"
hidden: false
---

Sensible supports extracting multiple documents from a single file (a "portfolio"). For example, for a portfolio PDF file containing two invoices, a 1040 tax document, and a contract, Sensible can segment out each document and return its extracted data separately. 

Sensible recommends extracting each document in a portfolio using its own document type, so you can write [validations](doc:validate-extractions)  for each type. For example, use an "income tax" doc type and an "invoice" doc type, rather than creating a "combined_tax_and_invoice" doc type.

To extract from a portfolio, take the following steps:

- Specify [fingerprints](doc:fingerprint) to configure how Sensible segments the portfolio into documents. Fingerprints test for text matches on first pages, last pages, and other page types.
- Create an extraction request by taking the following steps:

  - Indicate the file is a portfolio:
    - Sensible app: Click the **Portfolio** button on the **Extract** tab.
    - SDKs: Specify the Document Types parameter in the Extract method.
    - API:  Use one of the Portfolio extraction endpoints. 


  - In the request, specify the doc types that exist in the portfolio. For example, using the API, `"types": ["insurance_quote", "insurance_loss_run"]`. The extraction response includes document extractions and their page ranges in the portfolio.


Examples
===


The following example shows extracting three one-page documents from a portfolio using fingerprints to segment the documents. The portfolio contains two car insurance quotes and one loss run.

### Config


***Document type 1***

- **doc type**: "auto_insurance_quotes"

- **config name**: "anyco"

- **config content:**

To the config in [Getting started with layout-based extractions](doc:getting-started), append the following fingerprint:

```json
"fingerprint": {
    "tests": [
      {
        /* all these matches are unique to the first page. If a first page sometimes omits a match, specify alternatives
           in the match array using the`any` match type. */
        "page": "first",
        "match": [         
          {
            "text": "outline",
            "type": "startsWith"
          },
          {
            "text": "anycocarinsurance.com",
            "type": "startsWith"
          }
        ]
      }
    ]
  },
```

***Document type 2***

- **doc type**: "loss_run_reports"

- **config name**: "acme"

- **config content:**

To the config in the [Example loss run](doc:sections-example-loss-run) topic, append the following fingerprint:

```json
"fingerprint": {
    "tests": [
      {
        /* all these matches are unique to the first page. If a first page sometimes omits a match, specify alternatives
           in the match array using the`any` match type. */
        "page": "first",
        "match": [
          {
            "text": "any unprocessed claim",
            "type": "startsWith"
          }
        ]
      }
    ]
  },
```

### Example document


| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/portfolio.pdf) |
| ----------- | ------------------------------------------------------------ |

### Output


For the preceding configurations, doc types, and example document portfolio, the following asynchronous request returns a list of document extractions:

1. Make an extraction request. For example, through the API:

```
curl --request POST 'https://api.sensible.so/v0/extract_from_url/' \
--header 'Authorization: Bearer YOUR_API_KEY' \
--header 'Content-Type: application/json' \
--data-raw '{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/portfolio.pdf",
"types":["auto_insurance_quotes","loss_run_reports"]}'
```
2. This request returns an extraction ID. Use it to retrieve the extractions by replacing *YOUR_EXTRACTION_ID* with the returned ID in the following example code:
```
curl --request GET 'https://api.sensible.so/v0/documents/YOUR_EXTRACTION_ID' \
--header 'Authorization: Bearer YOUR_API_KEY'
```

The response contains extractions from three documents:

```json
{
    "id": "56a27285-9465-4781-82d1-3010bd5c589f",
    "created": "2024-09-26T19:26:13.492Z",
    "completed": "2024-09-26T19:26:21.691Z",
    "status": "COMPLETE",
    "types": [
        "auto_insurance_quotes",
        "loss_run_reports"
    ],
    "environment": "production",
    "documents": [
        {
            "documentType": "auto_insurance_quotes",
            "configuration": "anyco",
            "startPage": 0,
            "endPage": 0,
            "output": {
                "parsedDocument": {
                    "bodily_injury_premium": {
                        "source": "$100",
                        "value": 100,
                        "unit": "$",
                        "type": "currency",
                        "confidenceSignal": "confident_answer"
                    },
                    "customer_service_phone": {
                        "value": "18001234567",
                        "type": "string",
                        "confidenceSignal": "confident_answer"
                    },
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
                    "policy_number": {
                        "type": "string",
                        "value": "123456789"
                    }
                },
                "configuration": "anyco",
                "validations": [],
                "coverage": 1,
                "fileMetadata": {
                    "info": {
                        "modification_date": "2021-09-29T10:51:49.000-07:00"
                    }
                },
                "errors": [],
                "needsReview": false,
                "classificationSummary": [
                    {
                        "configuration": "anyco",
                        "score": {
                            "score": 5,
                            "coverage": 1,
                            "fieldsPresent": 5,
                            "penalties": 0
                        }
                    }
                ],
                "validation_summary": {
                    "fields": 5,
                    "fields_present": 5,
                    "errors": 0,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        },
        {
            "documentType": "auto_insurance_quotes",
            "configuration": "anyco",
            "startPage": 1,
            "endPage": 1,
            "output": {
                "parsedDocument": {
                    "bodily_injury_premium": {
                        "source": "$90",
                        "value": 90,
                        "unit": "$",
                        "type": "currency",
                        "confidenceSignal": "confident_answer"
                    },
                    "customer_service_phone": {
                        "value": "18001234567",
                        "type": "string",
                        "confidenceSignal": "confident_answer"
                    },
                    "policy_period": {
                        "type": "string",
                        "value": "May 20, 2021 - Nov 20,"
                    },
                    "comprehensive_premium": {
                        "source": "$130",
                        "value": 130,
                        "unit": "$",
                        "type": "currency"
                    },
                    "policy_number": {
                        "type": "string",
                        "value": "987654321"
                    }
                },
                "configuration": "anyco",
                "validations": [],
                "coverage": 1,
                "fileMetadata": {
                    "info": {
                        "modification_date": "2021-09-29T10:51:49.000-07:00"
                    }
                },
                "errors": [],
                "needsReview": false,
                "classificationSummary": [
                    {
                        "configuration": "anyco",
                        "score": {
                            "score": 5,
                            "coverage": 1,
                            "fieldsPresent": 5,
                            "penalties": 0
                        }
                    }
                ],
                "validation_summary": {
                    "fields": 5,
                    "fields_present": 5,
                    "errors": 0,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        },
        {
            "documentType": "loss_run_reports",
            "configuration": "acme",
            "startPage": 2,
            "endPage": 2,
            "output": {
                "parsedDocument": {
                    "total_unprocessed_claims": {
                        "source": "5",
                        "value": 5,
                        "type": "number"
                    },
                    "monthly_total_unprocessed_claims": [
                        {
                            "type": "string",
                            "value": "Sept unprocessed claims: 2"
                        },
                        {
                            "type": "string",
                            "value": "Oct unprocessed claims: 1"
                        },
                        {
                            "type": "string",
                            "value": "Nov unprocessed claims: 2"
                        }
                    ],
                    "unprocessed_sept_oct_claims_sections": [
                        {
                            "claim_number": {
                                "source": "1223456789",
                                "value": 1223456789,
                                "type": "number"
                            },
                            "phone_number": {
                                "type": "phoneNumber",
                                "source": "512 409 8765",
                                "value": "+15124098765"
                            },
                            "_everything_in_this_section": {
                                "type": "string",
                                "value": "Claim number: 1223456789 Claimant last name: Diaz Date of claim 09/15/2021 Phone number 512 409 8765"
                            }
                        },
                        {
                            "claim_number": {
                                "source": "9876543211",
                                "value": 9876543211,
                                "type": "number"
                            },
                            "phone_number": null,
                            "_everything_in_this_section": {
                                "type": "string",
                                "value": "Claim number: 9876543211 Claimant last name: Badawi Date of claim 09/08/2021 Phone number"
                            }
                        },
                        {
                            "claim_number": {
                                "source": "6785439210",
                                "value": 6785439210,
                                "type": "number"
                            },
                            "phone_number": {
                                "type": "phoneNumber",
                                "source": "505 238 8765",
                                "value": "+15052388765"
                            },
                            "_everything_in_this_section": {
                                "type": "string",
                                "value": "Claim number: 6785439210 Claimant last name: Levy Date of claim 10/03/2021 Phone number 505 238 8765"
                            }
                        }
                    ]
                },
                "configuration": "acme",
                "validations": [],
                "coverage": 0.9090909090909091,
                "fileMetadata": {
                    "info": {
                        "modification_date": "2021-09-29T10:51:49.000-07:00"
                    }
                },
                "errors": [],
                "needsReview": false,
                "classificationSummary": [
                    {
                        "configuration": "acme",
                        "score": {
                            "score": 10,
                            "coverage": 0.9090909090909091,
                            "fieldsPresent": 10,
                            "penalties": 0
                        }
                    }
                ],
                "validation_summary": {
                    "fields": 7,
                    "fields_present": 7,
                    "errors": 0,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        }
    ],
    "page_count": 3,
    "validation_summary": {
        "fields": 17,
        "fields_present": 17,
        "errors": 0,
        "warnings": 0,
        "skipped": 0
    },
    "download_url": "REDACTED",
    "coverage": 0.9696969696969697,
    "charged": 3,
    "version_id": "2ZjsLpUxhkv4SqiHxugHKXNhbV_S1jah",
    "reviewStatuses": [
        null,
        null,
        null
    ]
}
```



