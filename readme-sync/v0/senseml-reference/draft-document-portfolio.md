---
title: "Extracting from document portfolios"
hidden: true

---

Sometimes, multiple documents are packaged into one PDF file (a PDF "portfolio"). For example, a PDF might contain an invoice, a tax document, and a contract. 

In this case, it is best practice to add each document to the appropriate document type, rather than trying to fit them all into one document type (which would break any [validations](doc:validate-extractions) you write for the doc type). For example, if you already have a tax docs and an invoice doc type, define your new configs in these preexisting doc types.  In order for Sensible to handle the document inside the package, specify the following:

- In the config for each document in the package, use a fingerprint to define text matches for the starting and ending pages of the document, or for every page of the document. Sensible uses the fingerprint to find the page range in the package to which this config applies.
- When you make an asynchronous API call to extract data from the package, specify the multiple doc types that apply to the package. For example, `"types: ["insurance_quote", "insurance_loss_run"]`.  The return API response then includes additional metadata in the `parsed_documents` section to help you understand how Sensible parsed the package into separate documents, including the `document_type` and configuration used for a document ( `page_range`) in the package.

```json
{
    "id": "a2e39ca4-0a50-4be7-91b6-0e3b686e5cf9",
    "created": "2021-09-27T21:23:38.933Z",
    "status": "WAITING",
    "types": [
        "insurance_quote",
        "insurance_loss_run"
    ]
}
```

**TODO example**

talk about 'strong' fingerprints in an example

to be able to work with multidocuments your fingerprints should be "stronger" than the ones you use to discriminate between configs.

1.- they should be able to discriminate over a wider set of configs (not just the ones of the same doctype, but the ones on the other doctypes); 2.- if the bundles can have multiple copies of the same document, they should use the page: first/last so we can identify the end and start of different documents with the same type and config. for example, the multidoc from candor that we tested today included two documents, both of those were account summaries from the same bank, for two different periods. in a previous multidoc I've seen there were several 1040s. if you have two documents of the same type one after the other you need to be able to know where is the border between them. 

**TODO** add to OCR configuration setting that it's not honored for multidoc endpoints?  The main caveat is that at least for the moment we’re not honoring the MS/Google setting and you will always get MS OCR This is because we need to OCR the doc to detect what its doc type is and the OCR engine is set at the doc type level)

Example
----



**Fingerprint for car insurance quote**

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



