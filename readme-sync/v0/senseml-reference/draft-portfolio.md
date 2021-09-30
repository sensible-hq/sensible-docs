---
title: "Extracting from document portfolios"
hidden: true

---

Sometimes, multiple documents are packaged into one PDF file (a PDF "portfolio"). For example, a PDF might contain an invoice, a tax document, and a contract. 

In this case, it is best practice to extract each document using its appropriate document type, rather than trying to fit them all into one document type (which would break any [validations](doc:validate-extractions) you write for the doc type). For example, use an "income tax" doc type and an "invoice doc" type, rather than creating a "combined_tax_and_invoice" doc type.  In order for Sensible to handle the portfolio in one API extraction request, specify the following:

- In the config for each document in the portfolio, use a fingerprint to define text matches for the starting and ending pages of the document, or for every page of the document. Sensible uses the fingerprint to find the page range of each document in the package to which this config applies.
- Use https://docs.sensible.so/reference?showHidden=4007a#generate-an-upload-url-for-a-pdf-portfolio or https://docs.sensible.so/reference?showHidden=4007a#provide-a-download-url-for-a-pdf-portfolio (TODO: update links when go-live) to extract data from the portfolio. Specify the multiple doc types that apply to the portfolio. For example, `"types: ["insurance_quote", "insurance_loss_run"]`.  The return API response then includes multiple  `parsed_documents` sections, as well as information to help you understand how Sensible parsed the portfolio into separate documents, including the `document_type` and configuration used for a document ( `page_range`) in the package.

Example
----

The following example shows extracting three 1-page documents from a portfolio (two car insurance quotes and one loss run).

**Config**

***Document 1***

**doc type**: "auto_insurance_quote"

**config name**: "anyco_quote"

**config content:**

The config is the same as the one used in the [Getting started guide](doc:quickstart), with the addition of the following fingerprint:

```
  "fingerprint": {
    "tests": [
      {
        "page": "first",
        "match": [
          {
            "text": "anyco auto insurance",
            "type": "startsWith"
          }
        ]
      },
      {
        "page": "last",
        "match": [
          {
            "text": "please be sure to review your contract for a full explanation of coverages",
            "type": "includes"
          }
        ]
      }
    ]
  },
```

***Document 2***

**doc type**: "loss_run"

**config name**: "anyco_claims"

**config content:**

The config is the same as the one used in the Sections topic (TODO LINK), with the addition of the following fingerprint:

```

  "fingerprint": {
    "tests": [
      {
        "page": "first",
        "match": [
          {
            "text": "any unprocessed claim number must be processed within 90",
            "type": "startsWith"
          }
        ]
      },
      {
        "page": "last",
        "match": [
          {
            "text": "Total unprocesssed claims",
            "type": "startsWith",
            "isCaseSensitive": true
          }
        ]
      }
    ]
  },
```

**PDF**

| Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/portfolio.pdf) |
| ----------- | ------------------------------------------------------------ |

**Output**

For the preceding configurations, doc types, and example PDF portfolio, the following asynchronous extraction requests return a response with multiple extractions:

1. Submit an async request:

```
curl --request POST 'https://api.sensible.so/v0/extract_from_url/' \
--header 'Authorization: Bearer {API_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{"document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/portfolio.pdf",
"types":["auto_insurance_quote","loss_run"]}'
```
2. This request returns an EXTRACTION_ID. Use it to retrieve the extraction:
```
curl --request GET 'https://api.sensible.so/v0/documents/{EXTRACTION_ID}' \
--header 'Authorization: Bearer {API_TOKEN}'
```

The response contains extractions from three documents:

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
                    "errors": 1,
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
                    },
                    "comprehensive_premium": {
                        "source": "$130",
                        "value": 130,
                        "unit": "$",
                        "type": "currency"
                    },
                    "property_liability_premium": {
                        "source": "$15",
                        "value": 15,
                        "unit": "$",
                        "type": "currency"
                    },
                    "policy_number": {
                        "value": "987654321",
                        "type": "string"
                    }
                },
                "configuration": "anyco_multidoc",
                "validations": [],
                "validation_summary": {
                    "fields": 4,
                    "fields_present": 4,
                    "errors": 1,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        },
        {
            "documentType": "loss_run",
            "configuration": "anyco_claims",
            "startPage": 2,
            "endPage": 2,
            "output": {
                "parsedDocument": {
                    "total_unprocessed_claims": {
                        "source": "5",
                        "value": 5,
                        "type": "number"
                    },
                    "monthly_number_unprocessed_claims": [
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
                    "unprocessed_sept_oct_claims": [
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
                            }
                        },
                        {
                            "claim_number": {
                                "source": "9876543211",
                                "value": 9876543211,
                                "type": "number"
                            },
                            "phone_number": null
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
                            }
                        }
                    ]
                },
                "configuration": "sections",
                "validations": [],
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
    "download_url": "https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/MULTIDOC_EXTRACTION/7c269ef2-f9f1-4271-82e0-79b60887f45a.pdf?AWSAccessKeyId=REDACTED"
}
```



