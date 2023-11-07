---
title: "Typescript SDK reference"
hidden: true
---

## Installation

See [Typescript quickstart](doc:quickstart-typescript).

## Source files

[Typescript SDK repo](https://github.com/optimizely/python-sdk)

### Workflow

This SDK is a simplification of the [Sensible API](ref:choosing-an-endpoint) for document extraction and classification.

The document extraction workflow is as follows (TODO reword):

1. Instantiate an SDK object (`new SensibleSDK("apiKey")`).
2. Request a document extraction (`sensible.extract()`)
   1.  here we should explain that a file can be specified with an URL or by sending a blob of a local file.
   2. that we need to specify the document type(s), probably with links to where our docs explain what doctypes are, e.g. `sensible.extract(documentType:"auto_insurance")`.
   3. See following table for other options.
3. Wait for the result (`sensible.waitFor(request)`)
4. work with the output (optionally, generating an excel file)

## Extraction parameters

The following table shows You can configure the following parameters for extraction: TODO: better way to show these options than the internal definitions...?

```typescript
const request = await sensible.extract({
      file: blob,
      documentType: "tax_forms",
      environment: "development"
      documentName: "1040_john_doe.pdf",
      webhook: "YOUR_WEBHOOK_URL",
      generateExcel: true
    });
```

See the following table for more information:

| key               | value                                                        | description                                                  |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| file              | TODO -- string? or better description?                       | One of two options for submitting the document you want to extract data from.<br/> Pass the non-encoded document bytes.  You can extract document data from the following file formats:   PDF JPEG PNG TIFF.  For more information about file types, see  <https://docs.sensible.so/reference/extract-data-from-a-document>. |
| url               | string                                                       | One of two options for submitting the document you want to extract data from.<br/>URL that responds to a GET request with the bytes of the document you want to extract data from. This URL must be either publicly accessible, or presigned with a security token as part of the URL path. To check if the URL meets these criteria, open the URL with a web browser. The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication. |
| documentType      |                                                              | One of two options for specifying the document type or types.<br/>Type of document to extract from. Create your custom type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`). |
| documentTypes     |                                                              | One of two options for specifying the document type or types.<br/>Types of documents to extract from. Use this parameter to extract from multiple documents that are packaged into one PDF file (a PDF "portfolio").  This parameter specifies the document types contained in the PDF portfolio. Sensible then segments the PDF into documents using the specified document types (for example, 1099, w2, and bank_statement) and then runs extractions for each document. For more information, see [Multi-doc extraction](doc:portfolio). |
| generateExcel     | Boolean. default: false. TODO is it a boolean or extraction ID? | Converts the extracted document data from JSON format to Excel format. For more information, see [Get excel extraction](ref:get-excel-extraction). TODO: how to combine multiple extractions???? look at code but probably can't. |
| configurationName |                                                              | If specified, Sensible uses the specified config to extract data from the document instead of automatically choosing the best-scoring extraction in the document type.<br/>If unspecified, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type.<br/>Not applicable for PDF portfolios. TODO update API? |
| documentName      |                                                              | If you specify the filename of the document using this parameter, then Sensible returns the filename in the extraction response and populates the file name in the Sensible app's list of recent extractions TODO update API. |
| environment       | `production` or `development`. default: `production`         | If you specify `development`, extracts preferentially using config versions published to the development environment in the Sensible app. The extraction runs all configs in the doc type before picking the best fit. For each config, falls back to production version if no development version of the config exists. |
| webhook           |                                                              | Specifies to return extraction results to the defined webhook as soon as they're complete, so you don't have to poll for results status. Sensible also calls this webhook on error. For a tutorial about using webhooks with Sensible, see [Try a webhook](doc:api-tutorial-webhook). |

## Extraction schema

For the schema for extracted document data,  see <https://docs.sensible.so/reference/extract-data-from-a-document> and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

## Classification parameters

See the following table for classification parameters:

| key  | value                                  | description                                                  |
| ---- | -------------------------------------- | ------------------------------------------------------------ |
| file | TODO -- string? or better description? | Pass the non-encoded document bytes.  You can classify documents in the following file formats:   PDF JPEG PNG TIFF.  For more information about file types, see  <https://docs.sensible.so/reference/extract-data-from-a-document>. |

## Classification schema

For the schema for document classification, see https://docs.sensible.so/reference/classify-document-sync and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.