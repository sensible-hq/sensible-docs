---
title: "Multi-document extractions"
hidden: true
---

Sensible supports extracting multiple documents from a single file (a "portfolio"). For example, for a portfolio file containing two invoices, a 1040 tax document, and a contract, Sensible can segment out each document and return its extracted data separately. 

Sensible recommends extracting each document in a portfolio using its own document type, so you can write [validations](doc:validate-extractions)  for each type. For example, use an "income tax" doc type and an "invoice" doc type for the portfolio file in the previous example, rather than creating a "combined_tax_and_invoice" doc type.

To extract from a portfolio,  you have the following options:

|                              | LLM-based                                                    | Text matching ("fingerprints")                               |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Segmentation method          | Sensible prompts an LLM to segment the documents based on user-provided descriptions of the documents and their first and last page contents. | Sensible finds user-configured text matches to segment documents |
| Document variability         | Suited to documents that are unstructured or that have a large number of layout variations or revisions. | Suited to structured documents with a finite number of variations, where you know the layout of the document in advance. |
| Deterministic                | No                                                           | Yes. Find the information in the document using anchoring text and layout data. |
| Technical expertise required | For nontechnical users. Describe what you want to extract in a prompt to an LLM. For example, "the policy period" or "total amount invoiced". | Offers powerful extraction configuration for technical users based on spatial layout. For example, grab the text in a rectangular region relative to the word "Addendums" |
| Performance                  | Data extraction takes a few seconds for each LLM-based method. | Offers faster performance in general. For more information, see [Optimizing extraction performance](https://docs.sensible.so/docs/performance). |
| Specificity                  | at the document type level                                   | at the config level                                          |





To extract from a portfolio, take the following steps:

- Configure how Sensible segments the portfolio into documents with one of the following alternatives:
  - **LLM mode**: In the document type's  **Settings** tab, specify **LLM mode**. Provide a natural-language description of the document type, especially first and last page contents. For example: TODO image or text
  - **Fingerprint mode**  - In the document type's  **Settings** tab, specify **Fingerprint mode**. Specify [fingerprints](doc:fingerprint) in each config. Fingerprints test for text matches on first pages, last pages, and other page types.
- Create an extraction request by taking the following steps:

  - Indicate the file is a portfolio:
    - Sensible app: Click the **Portfolio** button on the **Extract** tab.
    - SDKs: Specify the Document Types parameter in the Extract method.
    - API:  Use one of the Portfolio extraction endpoints. 


  - In the request, specify the doc types that exist in the portfolio. For example, using the API, `"types": ["insurance_quotes_auto", "insurance_quotes_home"]`. The extraction response includes document extractions and their page ranges in the portfolio.


# Examples

## LLM example

TODO



## Fingerprint example



The following example shows extracting three one-page documents from a portfolio. The portfolio contains two car insurance quotes and one loss run.

### Config


***Document type 1***

- **doc type**: "auto_insurance_quote"

- **config name**: "anyco_quote"

- **config content:**

The config is the same as the one used in the [Getting started with layout-based extractions](doc:getting-started), with the addition of the following fingerprint:

```json
"fingerprint": {
    "tests": [
      {
        /* all these matches are unique to the first page. If a first page sometimes omits a match, specify alternatives
           in the match array. */
        "page": "first",
        "match": [         
          {
            "text": "outline of quoted coverage changes",
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

- **doc type**: "loss_run"

- **config name**: "anyco_claims"

- **config content:**

The config is the same as the one used in the [Sections](doc:sections) topic, with the addition of the following fingerprint:

```json
"fingerprint": {
    "tests": [
      {
        /* all these matches are unique to the first page. If a first page sometimes omits a match, specify alternatives
           in the match array. */
        "page": "first",
        "match": [
          {
            "text": "any unprocessed claim number must be processed within 90",
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
"types":["auto_insurance_quote","loss_run"]}'
```
2. This request returns an extraction ID. Use it to retrieve the extractions by replacing `*YOUR_EXTRACTION_ID* with the returned ID in the following example code:
```
curl --request GET 'https://api.sensible.so/v0/documents/YOUR_EXTRACTION_ID' \
--header 'Authorization: Bearer YOUR_API_KEY'
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
                    "errors": 0,
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
    "page_count": 3,
    "download_url": "https://sensible-so-document-type-bucket-prod-us-west-2.s3.us-west-2.amazonaws.com/sensible/MULTIDOC_EXTRACTION/7c269ef2-f9f1-4271-82e0-79b60887f45a.pdf?AWSAccessKeyId=REDACTED"
}
```



