---
title: "Document packages"
hidden: true

---

Sometimes, multiple documents are packaged into one PDF. For example, a PDF might contain an invoice, a tax document, and a contract. 

In this case, it is best practice to add each document to the appropriate document type, rather than trying to fit them all into one document type (which would break any [validations](doc:validate-extractions) you write for the doc type). For example, if you already have a tax docs and an invoice doc type, define your new configs in these preexisting doc types.  In order for Sensible to handle the document inside the package, specify the following:

- In the config for each document that is part of a package, use the Page parameter in a fingerprint to define text matches for the starting and ending pages of the document. Sensible uses the fingerprint to find the page range in the package to which this config applies.
- When you make an API call to extract data from the package, specify the multiple doc types in which you wrote your configs using the Document Type body parameter. For example, `"document_types": ["rate_confirmation", "bill_of_lading"]`.  The return API response then includes additional metadata in the `parsed_documents` section to help you understand how Sensible parsed the package into separate documents, including the `document_type` and configuation used for a `page_range` in the package.

**TODO: talk OCR behavior (update OCR docs too??**

**TODO: add to API sample response at some point to the reference...**

```json
{
  "id": "dda0b2a6-2b2e-4848-b314-d7e65ed75159",
  "created": "2021-08-23T20:56:58.265Z",
  "status": "COMPLETE",
  "document_types": ["rate_confirmation", "bill_of_lading"],
  "parsed_documents": [
    {
      "document_type": "rate_confirmation",
      "configuration": "uber_freight",
      "page_range": [0, 3],
      "parsed_document": { ...current single document API parsed_document field...},
      "validations": [...],
      "validation_summary": {...}
    },
    ...
  ]
}
```

**TODO example**

talk about 'strong' fingerprints in an example

to be able to work with multidocuments your fingerprints should be "stronger" than the ones you use to discriminate between configs.

1.- they should be able to discriminate over a wider set of configs (not just the ones of the same doctype, but the ones on the other doctypes); 2.- if the bundles can have multiple copies of the same document, they should use the page: first/last so we can identify the end and start of different documents with the same type and config. for example, the multidoc from candor that we tested today included two documents, both of those were account summaries from the same bank, for two different periods. in a previous multidoc I've seen there were several 1040s. if you have two documents of the same type one after the other you need to be able to know where is the border between them. 

