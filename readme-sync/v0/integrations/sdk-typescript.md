---
title: "Typescript SDK reference"
hidden: true
---

## Installation

See TODO LINK Typescript quickstart.

## Source files

- [Typescript SDK repo](https://github.com/optimizely/python-sdk)
- changelog <-- todo maintain a changelog in the repo???

## Extraction parameters

You can configure the following parameters for extraction:

```
type FileDefinition = { file: Buffer } | { url: string };
type DocumentType =
  | { documentType: string; configurationName?: string }
  | { documentTypes: string[] };
type Options = {
  webhook?: Webhook;
  documentName?: string;
  environment?: string;
};
type ExtractParams = FileDefinition & DocumentType & Options;
```

See the following table for more information:

| key                 | value                                                | description                                                  |
| ------------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| file                | TODO -- string? or better description?               | One of two options for submitting the document you want to extract data from.<br/> Pass the non-encoded document bytes.  You can extract document data from the following file formats:   PDF JPEG PNG TIFF.  For more information about file types, see  <https://docs.sensible.so/reference/extract-data-from-a-document>.<br/>TODO how to word: Using this option automatically uploads the file to a `download_url` URL that Sensible generates. You'll get the `download_url` in the response. |
| url                 | string                                               | One of two options for submitting the document you want to extract data from.<br/>URL that responds to a GET request with the bytes of the document you want to extract data from. This URL must be either publicly accessible, or presigned with a security token as part of the URL path. To check if the URL meets these criteria, open the URL with a web browser. The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication. |
| documentType        |                                                      | Type of document to extract from. Create your custom type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`).<br/>As a convenience, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type.<br/>For example, if you create an `auto_insurance_quotes` document type, you can add `carrier 1`, `carrier 2`, and `carrier 3` configs to the document type in the Sensible app. Then, you can extract data from all these carriers using the same document type, without specifying the carrier in the API request. |
| documentTypes       |                                                      | Use this parameter to extract from multiple documents that are packaged into one PDF file (a PDF "portfolio").  This parameter specifies the document types contained in the PDF portfolio. Sensible then segments the PDF into documents using the specified document types (for example, 1099, w2, and bank_statement) and then runs extractions for each document. |
| configurationName   |                                                      | use with the Document Type parameter.  If specified, Sensible uses the specified config to extract data from the document instead of automatically choosing the best-scoring extraction in the document type. |
| documentName        |                                                      | TODO                                                         |
| environment         | `production` or `development`. default: `production` | If you specify `development`, extracts preferentially using config versions published to the development environment in the Sensible app. The extraction runs all configs in the doc type before picking the best fit. For each config, falls back to production version if no development version of the config exists. |
| webhook             |                                                      | Specifies to return extraction results to the defined webhook as soon as they're complete, so you don't have to poll for results status. Sensible also calls this webhook on error. For a tutorial about using webhooks with Sensible, see [Try a webhook](doc:api-tutorial-webhook). |
| convertExcelTBDNAME |                                                      | TBD/TODO                                                     |

## Extraction schema

For the schema for extracted document data,  see <https://docs.sensible.so/reference/extract-data-from-a-document> and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

## Classification parameters

See the following table for classification parameters:

| key  | value                                  | description                                                  |
| ---- | -------------------------------------- | ------------------------------------------------------------ |
| file | TODO -- string? or better description? | Pass the non-encoded document bytes.  You can classify documents in the following file formats:   PDF JPEG PNG TIFF.  For more information about file types, see  <https://docs.sensible.so/reference/extract-data-from-a-document>. |

## Classification schema

For the schema for document classification, see https://docs.sensible.so/reference/classify-document-sync and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.