---
title: Fallback document type example
excerpt: >-
  Extract the pages of a portfolio that no fingerprint matches with a catch-all
  document type, instead of dropping them.
deprecated: false
hidden: true
metadata:
  title: ''
  description: >-
    Extract the pages of a portfolio that no fingerprint matches with a
    catch-all document type, instead of dropping them.
  robots: index
next:
  description: ''
---
In a portfolio extraction that segments documents with fingerprints, Sensible drops pages that no document type's fingerprints match. To extract those pages instead, name a fallback document type in the extraction request's `fallback_type` parameter. Sensible extracts each run of consecutive unmatched pages as one document of the fallback type.

The following example extends the [Fingerprint example](doc:portfolio#fingerprint-example) in Multi-document extractions. The portfolio contains a car insurance quote and a loss run from that example, interleaved with an invoice and a bank statement that no fingerprint matches. A third document type, `other_documents`, has an LLM-based config without a fingerprint that extracts basic facts from any document. The extraction request names `other_documents` as the fallback.

### Config

**_Document types 1 and 2_**

Create the `auto_insurance_quotes` and `loss_run_reports` document types and their configs as described in the [Fingerprint example](doc:portfolio#fingerprint-example).

**_Document type 3_**

- **doc type**: `other_documents`

- **config name**: `catch_all`

- **config content:**

```json
{
  /* no fingerprint: in a portfolio, this config runs only on pages
     that the fallback_type parameter routes to it, for example, the invoice on page 1 */
  "fields": [
    {
      "method": {
        "id": "queryGroup", /* LLM-based method, so the config works on documents with layouts you haven't seen, such as an invoice or a bank statement */
        "queries": [
          {
            "id": "document_type",
            "description": "what kind of document is this, for example invoice, lease, or bank statement?",
            "type": "string"
          },
          {
            "id": "issuer",
            "description": "the name of the company or organization that issued this document",
            "type": "string"
          },
          {
            "id": "document_date",
            "description": "the document's main date, such as its issue date or statement date",
            "type": "date"
          }
        ]
      }
    }
  ]
}
```

### Example document

The example portfolio has four one-page documents, in this order: an invoice, a car insurance quote, a bank statement, and a loss run.

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/portfolio_fallback.pdf) |
| ---------------- | ------------------------------------------------------------------------------------------------------------------ |

### Output

1. Make an extraction request that lists all three document types and names `other_documents` as the fallback:

```
curl --request POST 'https://api.sensible.so/v0/extract_from_url' \
  --header "Authorization: Bearer $SENSIBLE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data-raw '{"document_url":"https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/pdfs/portfolio_fallback.pdf","types":["auto_insurance_quotes","loss_run_reports","other_documents"],"segment_documents_with":"fingerprints","fallback_type":"other_documents"}'
```

2. This request returns an extraction ID. Use it to retrieve the extractions by replacing _YOUR_EXTRACTION_ID_ with the returned ID in the following example code:

```
curl --request GET 'https://api.sensible.so/v0/documents/YOUR_EXTRACTION_ID' \
--header "Authorization: Bearer $SENSIBLE_API_KEY"
```

The response contains four document extractions. The fingerprints match pages 2 and 4. Sensible extracts pages 1 and 3 using the fallback document type. The following excerpts show each document's `parsedDocument`. In the response, `startPage` and `endPage` are zero-based, so page 1 is `"startPage": 0`.

#### Page 1 | `other_documents` | `catch_all`

```json
{
  "document_type": {
    "value": "invoice",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "issuer": {
    "value": "Anyco inc",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "document_date": {
    "source": "06/21/21",
    "value": "2021-06-21T00:00:00.000Z",
    "type": "date",
    "confidenceSignal": "confident_answer"
  }
}
```

#### Page 2 | `auto_insurance_quotes` | `anyco`

```json
{
  "bodily_injury_premium": {
    "source": "$100",
    "value": 100,
    "unit": "$",
    "type": "currency",
    "confidenceSignal": "confident_answer"
  },
  "policy_number": {
    "type": "string",
    "value": "123456789"
  }
  /* etc */
}
```

#### Page 3 | `other_documents` | `catch_all`

```json
{
  "document_type": {
    "value": "bank statement",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "issuer": {
    "value": "First Best Bank",
    "type": "string",
    "confidenceSignal": "confident_answer"
  },
  "document_date": {
    "source": "March 31, 2023",
    "value": "2023-03-31T00:00:00.000Z",
    "type": "date",
    "confidenceSignal": "confident_answer"
  }
}
```

#### Page 4 | `loss_run_reports` | `acme`

```json
{
  "total_unprocessed_claims": {
    "source": "5",
    "value": 5,
    "type": "number"
  }
  /* etc */
}
```

If you leave out `fallback_type`, the response contains only the two documents on pages 2 and 4. In the response's `errors` array, Sensible reports that `other_documents` has no fingerprints, so it can't match any page.
