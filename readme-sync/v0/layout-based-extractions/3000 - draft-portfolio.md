---
title: "Multi-document extractions"
hidden: true
---

Sensible supports extracting multiple documents from a single file (a "portfolio"). For example, for a portfolio file containing two invoices, a 1040 tax document, and a contract, Sensible can segment out each document and return its extracted data separately. 

Sensible recommends extracting each document in a portfolio using its own document type, so you can write [validations](doc:validate-extractions)  for each type. For example, use an "income tax" doc type and an "invoice" doc type for the portfolio file in the previous example, rather than creating a "combined_tax_and_invoice" doc type.

To extract from a portfolio,  you have the following options:

|                     | LLM-based                                                    | Text-based ("fingerprints")                                  |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Segmentation method | Sensible prompts an LLM to segment the documents based on user-provided descriptions of the documents and their contents. | Sensible finds user-configured text matches ("fingerprints") on first and last pages to segment documents |
| Granularity         | at the document type level                                   | at the config level                                          |

Other tradeoffs between LLM and layout-based methods apply. For more tradeoffs see [Choosing an extraction approach](doc:author).

## Extracting from a portfolio

To extract from a portfolio, take the following steps:

- Configure how Sensible segments the portfolio into documents with one of the following alternatives: 
  -  **LLM mode**: In the document type's **Settings** tab, describe the document type in the **LLM portfolio description** field. For examples, see TODO link to descriptions topic.
  -  **Fingerprint mode**: In the document type's  **Settings** tab, specify **Fingerprint mode**. Specify [fingerprints](doc:fingerprint) in each config. Fingerprints test for text matches on first pages, last pages, and other page types. For an example of fingerprints, see [Fingerprint example](doc:portfolio#fingerprint-example).

- Create an extraction request by taking the following steps:

  - **Sensible app**: 
    
    - Click the **Portfolio** button on the **Extract** tab.  
    
    - Specify either **fingerprint mode** or **LLM mode**.
    
    - Select the document types contained in the portfolio file.
    
    - Upload the portfolio file and click **Extract**.
    
  - **API or SDK**:     
  
    - In a portfolio extraction API endpoint, specify the segmentation method and doc types, for example:
  
      ```json
      curl --location 'https://api.sensible.so/dev/extract_from_url?environment=production&document_name=portfolio_llm_filename_test' \
      --header 'Content-Type: application/json' \
      --header 'Authorization: ••••••' \
      --data '{
          "document_url":"https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/portfolio_bank_paystub_tax.pdf",
          "types": [
                "bank_statements",
                "tax_forms",
                "pay_stubs"
                
           ],
           "segment_documents_with": "llm"
           
      }'
      ```
  
      For information about extracting from portfolios using the SDKs, see the [SDK documentation](doc:sdk-guides)  
  

- The extraction response includes document extractions and their page ranges in the portfolio.  In the Sensible app, you can navigate through the portfolio's extractions using the dropdown:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/portfolio_nav.png) 

# Examples

## LLM example

The following example shows extracting three documents from a portfolio using LLMs to segment the documents. The portfolio contains a bank statement, a paystub, and a tax form. To try out the example, take the following steps:

1. Follow the steps in [Out-of-the-box extractions](doc:library-quickstart)  to add support for the **bank statements**, **tax forms**, and **pay stubs** document types to your account.

2. In the Sensible app, click the **Document types** tab. Click each document type to edit its settings. In the **Settings** tab, enter the following descriptions for each type in the **LLM portfolio description** field:

   | document type   | description                                                  |
   | --------------- | ------------------------------------------------------------ |
   | bank statements | this is a bank statement document type. Each document contains the name of the bank on the first page. |
   | pay stubs       | this is a pay stub document type.                            |
   | tax forms       | this is a tax form document type. Each page in each document contains the form number in the bottom right corner of the page. |

3. Download the following example document:

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/portfolio_bank_paystub_tax.pdf) |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |


4. In the **Extract** tab:
   - TODO left off do a screenshot once it's in place showing the doc types selected (re-clone them to avoid 'described') 

You should see results like the following (in the UI, page through the results TODO how to describe? TODO test these updated descriptions:

```json
{
    "id": "cdbc284f-2681-4681-ad6e-cfb0108d546c",
    "created": "2024-09-24T16:11:55.684Z",
    "completed": "2024-09-24T16:13:48.809Z",
    "status": "COMPLETE",
    "types": [
        "tax_forms",
        "pay_stubs",
        "bank_statements"
    ],
    "environment": "production",
    "document_name": "portfolio_llm_filename_test",
    "documents": [
        {
            "documentType": "tax_forms",
            "configuration": "1040_2019",
            "startPage": 0,
            "endPage": 1,
            "output": {
                "parsedDocument": {
                    "year": {
                        "type": "string",
                        "value": "2020"
                    },
                    "filing_status.single": {
                        "type": "boolean",
                        "value": false
                    },
                    "filing_status.marrid_filing_jointly": {
                        "type": "boolean",
                        "value": true
                    },
                    "filing_status.marrid_filing_separately": {
                        "type": "boolean",
                        "value": false
                    },
                    "filing_status.head_of_household": {
                        "type": "boolean",
                        "value": false
                    },
                    "filing_status.qualifying_widow": {
                        "type": "boolean",
                        "value": false
                    },
                    "name": {
                        "type": "string",
                        "value": "Kevin Finnerty"
                    },
                    "ssn": {
                        "type": "string",
                        "value": "091-30-1116"
                    },
                    "spouse_name": {
                        "type": "string",
                        "value": "Carmella Finnerty"
                    },
                    "spouse_ssn": {
                        "type": "string",
                        "value": "772-98-1129"
                    },
                    "home_street_address": {
                        "type": "string",
                        "value": "4880 Combe Street"
                    },
                    "home_apartment_number": null,
                    "home_city_state_zipcode": {
                        "type": "string",
                        "value": "Newark, New Jersey 99033"
                    },
                    "wages_salaries_tips": {
                        "source": "502,213",
                        "value": 502213,
                        "type": "number"
                    },
                    "tax_exempt_interest": null,
                    "taxable_interest": {
                        "source": "2,049",
                        "value": 2049,
                        "type": "number"
                    },
                    "qualified_dividends": {
                        "source": "25",
                        "value": 25,
                        "type": "number"
                    },
                    "ordinary_dividends": {
                        "source": "69",
                        "value": 69,
                        "type": "number"
                    },
                    "ira_distributions": null,
                    "ira_distributions_taxable_amount": null,
                    "pensions_and_annuities": null,
                    "pensions_and_annuities_taxable_amount": null,
                    "social_security_benefits": null,
                    "social_security_benefits_taxable_amount": null,
                    "capital_gain_or_loss": {
                        "source": "7",
                        "value": 7,
                        "type": "number"
                    },
                    "other_income": {
                        "source": "0",
                        "value": 0,
                        "type": "number"
                    },
                    "total_income": {
                        "source": "504,331",
                        "value": 504331,
                        "type": "number"
                    },
                    "adjustments_to_income": null,
                    "adjusted_gross_income": {
                        "source": "504,331",
                        "value": 504331,
                        "type": "number"
                    },
                    "standard_deduction": {
                        "source": "24,800",
                        "value": 24800,
                        "type": "number"
                    },
                    "qualified_business_deduction": {
                        "source": "13",
                        "value": 13,
                        "type": "number"
                    },
                    "taxable_income": {
                        "source": "479,531",
                        "value": 479531,
                        "type": "number"
                    },
                    "tax": null,
                    "child_tax_credit": {
                        "source": "19",
                        "value": 19,
                        "type": "number"
                    },
                    "other_tax_including_self_employment": {
                        "source": "0",
                        "value": 0,
                        "type": "number"
                    },
                    "total_tax": {
                        "source": "32",
                        "value": 32,
                        "type": "number"
                    },
                    "federal_income_tax_withheld": null,
                    "earned_income_credit": {
                        "source": "27",
                        "value": 27,
                        "type": "number"
                    },
                    "additional_child_tax_credit": {
                        "source": "28",
                        "value": 28,
                        "type": "number"
                    },
                    "american_opportunity_credit": {
                        "source": "29",
                        "value": 29,
                        "type": "number"
                    },
                    "total_other_payments": {
                        "source": "32",
                        "value": 32,
                        "type": "number"
                    },
                    "total_payments": {
                        "source": "500",
                        "value": 500,
                        "type": "number"
                    },
                    "overpaid_amount": {
                        "source": "468",
                        "value": 468,
                        "type": "number"
                    },
                    "overpaid_refund_amount": {
                        "source": "0",
                        "value": 0,
                        "type": "number"
                    },
                    "routing_number": {
                        "type": "string",
                        "value": "X X X X X X X X X"
                    },
                    "account_type.checking": {
                        "type": "boolean",
                        "value": true
                    },
                    "account_type.savings": {
                        "type": "boolean",
                        "value": false
                    },
                    "account_number": {
                        "type": "string",
                        "value": "X X X X X X X X X X X X X X X X X"
                    },
                    "amount_you_owe": null,
                    "estimated_tax_penalty": {
                        "source": "38",
                        "value": 38,
                        "type": "number"
                    },
                    "signed": {
                        "type": "boolean",
                        "value": false
                    },
                    "signed_date": null,
                    "spouse_signed": {
                        "type": "boolean",
                        "value": false
                    },
                    "spouse_signed_date": null
                },
                "configuration": "1040_2019",
                "validations": [],
                "coverage": 0.7407407407407407,
                "fileMetadata": {
                    "info": {
                        "modification_date": "2023-11-27T12:43:54.000-07:00"
                    }
                },
                "errors": [],
                "needsReview": false,
                "classificationSummary": [
                    {
                        "configuration": "1040_2018",
                        "score": {
                            "score": 33,
                            "coverage": 0.6111111111111112,
                            "fieldsPresent": 33,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "1040_2019",
                        "score": {
                            "score": 40,
                            "coverage": 0.7407407407407407,
                            "fieldsPresent": 40,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "1040_2020",
                        "score": {
                            "score": 33,
                            "coverage": 0.6111111111111112,
                            "fieldsPresent": 33,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "1040_2021",
                        "score": {
                            "score": 34,
                            "coverage": 0.6296296296296297,
                            "fieldsPresent": 34,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "4868_2021",
                        "score": {
                            "score": 0,
                            "coverage": 0,
                            "fieldsPresent": 0,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "4868_2022",
                        "score": {
                            "score": 0,
                            "coverage": 0,
                            "fieldsPresent": 0,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "941_2022",
                        "score": {
                            "score": 3,
                            "coverage": 0.03225806451612903,
                            "fieldsPresent": 3,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "senior_1040_2021",
                        "score": {
                            "score": 33,
                            "coverage": 0.6111111111111112,
                            "fieldsPresent": 33,
                            "penalties": 0
                        }
                    }
                ],
                "validation_summary": {
                    "fields": 54,
                    "fields_present": 40,
                    "errors": 0,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        },
        {
            "documentType": "bank_statements",
            "configuration": "wells_fargo_checking",
            "startPage": 2,
            "endPage": 6,
            "output": {
                "parsedDocument": {
                    "start_date": {
                        "source": "07/14/2021",
                        "value": "2021-07-14T00:00:00.000Z",
                        "type": "date"
                    },
                    "end_date": {
                        "source": "08/11/2021",
                        "value": "2021-08-11T00:00:00.000Z",
                        "type": "date"
                    },
                    "customer_name": {
                        "type": "string",
                        "value": "DOMINIC BOGDAN"
                    },
                    "customer_address": {
                        "value": "111 LAKES RD\nSAN DEGO CA 11111",
                        "type": "address"
                    },
                    "account_summary_table": null,
                    "accounts": [
                        {
                            "account_type": {
                                "type": "string",
                                "value": "Essential Checking"
                            },
                            "account_number": null,
                            "beginning_balance": {
                                "source": "3,082.80",
                                "value": 3082.8,
                                "unit": "$",
                                "type": "currency"
                            },
                            "deposits": {
                                "source": "24,163.03",
                                "value": 24163.03,
                                "unit": "$",
                                "type": "currency"
                            },
                            "withdrawals": {
                                "source": "26,557.01",
                                "value": 26557.01,
                                "unit": "$",
                                "type": "currency"
                            },
                            "end_balance": {
                                "source": "688.82",
                                "value": 688.82,
                                "unit": "$",
                                "type": "currency"
                            },
                            "deposits_table": [
                                {
                                    "date": {
                                        "value": "7/15",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "167.00",
                                        "value": 167,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "3,764.53",
                                        "value": 3764.53,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/23",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "7,189.15",
                                        "value": 7189.15,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/23",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "123.45",
                                        "value": 123.45,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/27",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "s",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "4,961.00",
                                        "value": 4961,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/29",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "2.69",
                                        "value": 2.69,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/30",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "3,772.62",
                                        "value": 3772.62,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "1,300.00",
                                        "value": 1300,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/4",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "75.00",
                                        "value": 75,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/5",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "194.36",
                                        "value": 194.36,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/6",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "2,613.23",
                                        "value": 2613.23,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                }
                            ],
                            "withdrawals_table": [
                                {
                                    "date": {
                                        "value": "7/14",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "10.00",
                                        "value": 10,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/14",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "11.77",
                                        "value": 11.77,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/15",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "n",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "3.45",
                                        "value": 3.45,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/15",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "co",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "70.66",
                                        "value": 70.66,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/15",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "44.24",
                                        "value": 44.24,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/15",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "101.93",
                                        "value": 101.93,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/15",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "1,400.00",
                                        "value": 1400,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "14.99",
                                        "value": 14.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "11.88",
                                        "value": 11.88,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "58.26",
                                        "value": 58.26,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "5.00",
                                        "value": 5,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "1,300.00",
                                        "value": 1300,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "8.80",
                                        "value": 8.8,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/16",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "167.00",
                                        "value": 167,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "2.99",
                                        "value": 2.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "212.83",
                                        "value": 212.83,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "39.99",
                                        "value": 39.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "198.59",
                                        "value": 198.59,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "295.82",
                                        "value": 295.82,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "4.00",
                                        "value": 4,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "55.84",
                                        "value": 55.84,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "10.00",
                                        "value": 10,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "65.00",
                                        "value": 65,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "35.26",
                                        "value": 35.26,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "k",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "1,300.00",
                                        "value": 1300,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "149.11",
                                        "value": 149.11,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "150.00",
                                        "value": 150,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/19",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "250.00",
                                        "value": 250,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/20",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "8.86",
                                        "value": 8.86,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/20",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "A",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "19.88",
                                        "value": 19.88,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/20",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "Check",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "399.14",
                                        "value": 399.14,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/21",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "29.18",
                                        "value": 29.18,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/22",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "e",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "36.00",
                                        "value": 36,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/22",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "33.48",
                                        "value": 33.48,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/22",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "17.02",
                                        "value": 17.02,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/23",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "8.00",
                                        "value": 8,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": {
                                        "value": "8",
                                        "type": "string"
                                    },
                                    "amount": {
                                        "source": "195.28",
                                        "value": 195.28,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "93.98",
                                        "value": 93.98,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "18.44",
                                        "value": 18.44,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "113.68",
                                        "value": 113.68,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "219.93",
                                        "value": 219.93,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "10.00",
                                        "value": 10,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "250.00",
                                        "value": 250,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "400.00",
                                        "value": 400,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/26",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "2,500.00",
                                        "value": 2500,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/27",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "45.85",
                                        "value": 45.85,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/27",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "600.00",
                                        "value": 600,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/27",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "3,123.43",
                                        "value": 3123.43,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/28",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "11.99",
                                        "value": 11.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/30",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "54.99",
                                        "value": 54.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "7/30",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "10.89",
                                        "value": 10.89,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "98.09",
                                        "value": 98.09,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "18.99",
                                        "value": 18.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "82.12",
                                        "value": 82.12,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "56.40",
                                        "value": 56.4,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "255.25",
                                        "value": 255.25,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "102.20",
                                        "value": 102.2,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "145.37",
                                        "value": 145.37,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "10.00",
                                        "value": 10,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "53.56",
                                        "value": 53.56,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "35.00",
                                        "value": 35,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "2.18",
                                        "value": 2.18,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "11.06",
                                        "value": 11.06,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "800.00",
                                        "value": 800,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "215.62",
                                        "value": 215.62,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "250.00",
                                        "value": 250,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/2",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "1,500.00",
                                        "value": 1500,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/3",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "15.99",
                                        "value": 15.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/5",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "7.99",
                                        "value": 7.99,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/5",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "250.00",
                                        "value": 250,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/5",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "20.00",
                                        "value": 20,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/6",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "3.00",
                                        "value": 3,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/6",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "83.00",
                                        "value": 83,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/6",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "4,961.98",
                                        "value": 4961.98,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "176.66",
                                        "value": 176.66,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "146.82",
                                        "value": 146.82,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "13.87",
                                        "value": 13.87,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "88.00",
                                        "value": 88,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "25.96",
                                        "value": 25.96,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "16.86",
                                        "value": 16.86,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "35.53",
                                        "value": 35.53,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "42.19",
                                        "value": 42.19,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "7.00",
                                        "value": 7,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "74.19",
                                        "value": 74.19,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "150.00",
                                        "value": 150,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "810.00",
                                        "value": 810,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/9",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "1,300.00",
                                        "value": 1300,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/10",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "161.45",
                                        "value": 161.45,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/10",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "100.00",
                                        "value": 100,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/10",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "250.00",
                                        "value": 250,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                },
                                {
                                    "date": {
                                        "value": "8/11",
                                        "type": "string"
                                    },
                                    "description": null,
                                    "amount": {
                                        "source": "3.25",
                                        "value": 3.25,
                                        "unit": "$",
                                        "type": "currency"
                                    }
                                }
                            ],
                            "transaction_table": null
                        }
                    ]
                },
                "configuration": "wells_fargo_checking",
                "validations": [],
                "coverage": 0.6949685534591195,
                "fileMetadata": {
                    "info": {
                        "modification_date": "2023-11-27T12:43:54.000-07:00"
                    }
                },
                "errors": [],
                "needsReview": false,
                "classificationSummary": [
                    {
                        "configuration": "ally_combined_customer_statement",
                        "score": {
                            "score": 0,
                            "coverage": 0,
                            "fieldsPresent": 0,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "any_single_account_bank_statement",
                        "score": {
                            "score": 20,
                            "coverage": 0.7407407407407407,
                            "fieldsPresent": 20,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "boa",
                        "score": {
                            "score": 0,
                            "coverage": 0,
                            "fieldsPresent": 0,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "chase_consolidated_balance_summary",
                        "score": {
                            "score": 0,
                            "coverage": 0,
                            "fieldsPresent": 0,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "wells_fargo_checking",
                        "score": {
                            "score": 221,
                            "coverage": 0.6949685534591195,
                            "fieldsPresent": 221,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "wells_fargo_combined_statement_of_accounts",
                        "score": {
                            "score": 4,
                            "coverage": 0.6666666666666666,
                            "fieldsPresent": 4,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "wells_fargo_savings",
                        "score": {
                            "score": 221,
                            "coverage": 0.6949685534591195,
                            "fieldsPresent": 221,
                            "penalties": 0
                        }
                    }
                ],
                "validation_summary": {
                    "fields": 6,
                    "fields_present": 5,
                    "errors": 0,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        },
        {
            "documentType": "pay_stubs",
            "configuration": "pay_stubs",
            "startPage": 7,
            "endPage": 7,
            "output": {
                "parsedDocument": {
                    "employer_name": {
                        "value": "Delta Airlines",
                        "type": "string",
                        "confidenceSignal": "confident_answer"
                    },
                    "employee_name": {
                        "value": "Clyde Drexler",
                        "type": "string",
                        "confidenceSignal": "confident_answer"
                    },
                    "employee_address": {
                        "value": "1123 Drive street",
                        "type": "string",
                        "confidenceSignal": "confident_answer"
                    },
                    "pay_date": null,
                    "pay_period_start_date": null,
                    "pay_period_end_date": null,
                    "net_pay": {
                        "source": "$2,076.28",
                        "value": 2076.28,
                        "unit": "$",
                        "type": "currency",
                        "confidenceSignal": "confident_answer"
                    },
                    "earnings": [
                        {
                            "earnings_type": {
                                "value": "Regular Hours I Salaried",
                                "type": "string"
                            },
                            "rate": {
                                "value": "$74.52",
                                "type": "string"
                            },
                            "hours": {
                                "value": "40.0",
                                "type": "string"
                            },
                            "amount": {
                                "value": "$2,980.77",
                                "type": "string"
                            },
                            "ytd": {
                                "value": "$17,288.47",
                                "type": "string"
                            }
                        },
                        {
                            "earnings_type": {
                                "value": "Total Hours Worked",
                                "type": "string"
                            },
                            "rate": null,
                            "hours": {
                                "value": "40.0",
                                "type": "string"
                            },
                            "amount": null,
                            "ytd": null
                        },
                        {
                            "earnings_type": {
                                "value": "Paid Holidays",
                                "type": "string"
                            },
                            "rate": null,
                            "hours": null,
                            "amount": null,
                            "ytd": {
                                "value": "$596.15",
                                "type": "string"
                            }
                        },
                        {
                            "earnings_type": {
                                "value": "Commission",
                                "type": "string"
                            },
                            "rate": null,
                            "hours": null,
                            "amount": {
                                "value": "$0.00",
                                "type": "string"
                            },
                            "ytd": {
                                "value": "$33,591.83",
                                "type": "string"
                            }
                        },
                        {
                            "earnings_type": {
                                "value": "Gross Earnings",
                                "type": "string"
                            },
                            "rate": null,
                            "hours": null,
                            "amount": {
                                "value": "$2,980.77",
                                "type": "string"
                            },
                            "ytd": {
                                "value": "$51,476.45",
                                "type": "string"
                            }
                        }
                    ],
                    "deductions": [
                        {
                            "deduction": {
                                "value": "Employee Vision Insurance",
                                "type": "string"
                            },
                            "this_period": {
                                "value": "$0.02",
                                "type": "string"
                            },
                            "ytd": {
                                "value": "$0.14",
                                "type": "string"
                            }
                        },
                        {
                            "deduction": {
                                "value": "Employee Dental Insurance",
                                "type": "string"
                            },
                            "this_period": {
                                "value": "$0.15",
                                "type": "string"
                            },
                            "ytd": {
                                "value": "$1.07",
                                "type": "string"
                            }
                        },
                        {
                            "deduction": {
                                "value": "Employee Medical Insurance",
                                "type": "string"
                            },
                            "this_period": {
                                "value": "$1.12",
                                "type": "string"
                            },
                            "ytd": {
                                "value": "$6.72",
                                "type": "string"
                            }
                        },
                        {
                            "deduction": {
                                "value": "Dependents Medical Insurance",
                                "type": "string"
                            },
                            "this_period": {
                                "value": "$1.11",
                                "type": "string"
                            },
                            "ytd": {
                                "value": "$6.66",
                                "type": "string"
                            }
                        }
                    ]
                },
                "configuration": "pay_stubs",
                "validations": [],
                "coverage": 0.7045454545454546,
                "fileMetadata": {
                    "info": {
                        "modification_date": "2023-11-27T12:43:54.000-07:00"
                    }
                },
                "errors": [],
                "needsReview": false,
                "classificationSummary": [
                    {
                        "configuration": "adp",
                        "score": {
                            "score": 4,
                            "coverage": 0.2,
                            "fieldsPresent": 4,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "gusto",
                        "score": {
                            "score": 10,
                            "coverage": 0.47619047619047616,
                            "fieldsPresent": 10,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "pay_stubs",
                        "score": {
                            "score": 31,
                            "coverage": 0.7045454545454546,
                            "fieldsPresent": 31,
                            "penalties": 0
                        }
                    },
                    {
                        "configuration": "paylocity",
                        "score": {
                            "score": 1,
                            "coverage": 0.05,
                            "fieldsPresent": 1,
                            "penalties": 0
                        }
                    }
                ],
                "validation_summary": {
                    "fields": 16,
                    "fields_present": 13,
                    "errors": 0,
                    "warnings": 0,
                    "skipped": 0
                }
            }
        }
    ],
    "page_count": 8,
    "validation_summary": {
        "fields": 76,
        "fields_present": 58,
        "errors": 0,
        "warnings": 0,
        "skipped": 0
    },
    "download_url": "https://sensible-so-document-type-bucket-dev-us-west-2.s3.us-west-2.amazonaws.com/c024cd1c-5f33-4a82-b2ea-2c807e44988b/MULTIDOC_EXTRACTION/cdbc284f-2681-4681-ad6e-cfb0108d546c.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAR355P7ASS36YVB52%2F20240924%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20240924T161349Z&X-Amz-Expires=900&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJ%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQC%2FhsviH7McR4SqqKyegBpXSrK5XHEOLMmPD1aJT8dzGAIhAK6qW3O2MTzJFlw7lCyYvPvefZsBOaWlwFguk1Lc4Z1sKpQDCNj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQAhoMMTI4NzA5NTU2MjYxIgzs6oTDT9ISsiENbqkq6AKPyGaxlwtg7hzJB2uzU10XQWN%2Fn52MfjpyD8%2FTT7fw%2BH66qJ6vItiktBb2YCuVqoWTK0ViKSoP4rRGr9ccgtBhpyRBXjgcK8zC8f2JgbPdLcBOm0Rb9xIHKSSZErtFzHnsypx2w9N5AK%2BPans66ORzXZsFzNK%2F06bybDAAqAD5ve4Ghy9ryUqHsoxPEgRq0aQGIvp1reAc2dbJUdjKxtnwHbBx2OGhGkF5shtKg%2Bp62QRRV530ki87Ub6MiwhdOt%2BOYREapd3krRYTp5eprsCyVpcj1w7MRwAP9TuBinrn4Utib8QkLGDeh8cFoX1%2FZD6NQJDVIPlAht7rkuAG9ub4u25W41Ikbvhkv8NlOAvba0HgY%2FphipYp0Lcqf5I%2Bqn%2Fp%2BYT7Xj%2FACkMb5rDiUjZfSa3us%2BaQOzdyhHl3ZoUclNiqU%2FcBpkxgSg%2BcbMDnBdzHigyGmoXegvIJAMIymFRNR7oc39o6D6gw9KbLtwY6nAFDrMzClFRTheORjP4btj%2BmhKx7phlY6esYQfPbk5kqDNTMA4aUWCa8GjMW8aBZj448muHl89feN1SLl4csDRbYBrOXwe8EIxybl%2FvfJ9TIXVxWALO2baX4qSf7ThzXQLPOzgE5FDrL4pHKxaNGhWT%2FUSS34WMjo88hmZyKiEHgIUxeUNuEQJjYZI4u9aFnk2U%2BayWXfIDWZEODKuI%3D&X-Amz-Signature=e28cc057947a95f97ae2a27a4d01c92af5ae40d6e8f70ea99242e3557e1e2544&X-Amz-SignedHeaders=host&x-id=GetObject",
    "coverage": 0.7134182495817716,
    "charged": 3,
    "version_id": "DkxGjnwpLR0xqiO13PTtTTJflQ8vhvBd",
    "reviewStatuses": [
        null,
        null,
        null
    ]
}
```



## Fingerprint example



The following example shows extracting three one-page documents from a portfolio using fingerprints to segment the documents. The portfolio contains two car insurance quotes and one loss run.

### Config


***Document type 1***

- **doc type**: "auto_insurance_quote"

- **config name**: "anyco_quote"

- **config content:**

To the config in [Getting started with layout-based extractions](doc:getting-started), append the following fingerprint:

```json
"fingerprint": {
    "tests": [
      {
        /* all these matches are unique to the first page. If a first page sometimes omits a match, specify alternatives
           in the match array. */
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

- **doc type**: "loss_run"

- **config name**: "anyco_claims"

- **config content:**

To the config in the [Sections](doc:sections) topic, append the following fingerprint:

```json
"fingerprint": {
    "tests": [
      {
        /* all these matches are unique to the first page. If a first page sometimes omits a match, specify alternatives
           in the match array. */
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



