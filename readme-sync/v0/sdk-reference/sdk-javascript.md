---
title: "Javascript SDK reference"
hidden: false
---

This SDK is a simplification of the [Sensible API](ref:choosing-an-endpoint) for document extraction and classification.

## Installation

See [Javascript quickstart](doc:quickstart-javascript).

## Source files

[Javascript SDK repo](https://github.com/optimizely/python-sdk)

## Workflows

### Extraction workflow

See the following steps for an overview of the SDK's workflow for extraction:

1. Instantiate an SDK object (`new SensibleSDK()`. 
2. Request a document extraction (`sensible.extract()` with the following parameters:
   1.  **(required)** Specify the document from which to extract data using the `url` or `file` parameter. 
   2.  **(required)** Specify the user-defined document type or types using the `documentType` or `documentTypes` parameter.
   3.  See the following section for optional parameters.
3. Poll for the results (`sensible.waitFor()` or get the results using a webhook.
4. Optionally convert the extracted JSON data to Excel using `generateExcel()`. 
5. Consume the data.


### Classification workflow

See the following steps for an overview of the SDK's workflow for classification:

1. Instantiate an SDK object (`new SensibleSDK()`.

2. Request a document classification (`sensible.classify()`.  Specify the document to classify using the `file` parameter.

3. Poll for the result (`sensible.waitFor()`.

4. Consume the data.


See the following sections for more information about the methods in these workflows.

## Extract method

### Description

Extract data from a document, as specified by the extraction configurations and document types defined in your Sensible account.

### Example

```type
const request = await sensible.extract({
      url: "https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library/main/balance_sheets/form_10k_balance_sheet/form_10k_balance_sheet_sample.pdf", //required
      documentType: "balance_sheets", //required
      environment: "development"
      documentName: "balance_sheet_acme_co.pdf",
      webhook: {
         url:"YOUR_WEBHOOK_URL",
         payload: "additional info",
    }});
```

### Parameters

See the following table for information about parameters:

| key               | value                                                      | description                                                  |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| file              | string                                                     | One of two required options for submitting the document you want to extract data from.<br/> Pass the non-encoded document bytes.  For more information about supported file types, see  [Extract data from a document](https://docs.sensible.so/reference/extract-data-from-a-document). |
| url               | string                                                     | One of two required options for submitting the document you want to extract data from.<br/>URL that responds to a GET request with the bytes of the document you want to extract data from. This URL must be either publicly accessible, or presigned with a security token as part of the URL path. To check if the URL meets these criteria, open the URL with a web browser. The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication. |
| documentType      | string                                                     | One of two required options for specifying the document type or types.<br/>Type of document to extract from. Create your custom type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`). |
| documentTypes     | array                                                      | One of two required options for specifying the document type or types.<br/>Types of documents to extract from. Use this parameter to extract from multiple documents that are packaged into one file (a "portfolio").  This parameter specifies the document types contained in the portfolio. Sensible then segments the portfolio into documents using the specified document types (for example, 1099, w2, and bank_statement) and then runs extractions for each document. For more information, see [Multi-doc extraction](doc:portfolio). |
| configurationName | string                                                     | If specified, Sensible uses the specified config to extract data from the document instead of automatically choosing the best-scoring extraction in the document type.<br/>If unspecified, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type.<br/>Not applicable for portfolios. |
| documentName      | string                                                     | If you specify the filename of the document using this parameter, then Sensible returns the filename in the extraction response and populates the file name in the Sensible app's list of recent extractions. |
| environment       | `"production"` or `"development"`. default: `"production"` | If you specify `development`, Sensible extracts preferentially using config versions published to the development environment in the Sensible app. The extraction runs all configs in the doc type before picking the best fit. For each config, falls back to production version if no development version of the config exists. |
| webhook           | object                                                     | Specifies to return extraction results to the specified webhook URL as soon as they're complete, so you don't have to poll for results status. Sensible also calls this webhook on error.<br/> The webhook object has the following parameters:<br/>`url`:  string. Webhook destination. Sensible will POST to this URL when the extraction is complete.<br/>`payload`: string, number, boolean, object, or array. Information additional to the API response, for example a UUID for verification. |

### Returns

Get results from this method by using a webhook or calling the Wait For method. For the schema for the results of an extraction request,  see [Extract data from a document](https://docs.sensible.so/reference/extract-data-from-a-document) and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

## Wait For method

### Description

Polls for completed status of an extraction or classification request.

### Example

The following code sample shows waiting for a document extraction:

```javascript
const results = await sensible.waitFor(request);
```

### Parameters

See the following table for information about parameters:

| key  | value  | description                                                  |
| ---- | ------ | ------------------------------------------------------------ |
| n/a  | object | Specify an extraction request object or a classification request object. Polls Sensible every 5 seconds before returning results. |

### Returns

This method returns the results of a classification or extraction request. For more information, see those methods.

## Generate Excel method

### Description

Get Excel files from documents. In more detail, this endpoint converts your JSON document extraction to an Excel spreadsheet.
To compile multiple documents into one Excel file, specify the results of extractions as an array.
For the best compiled spreadsheet results, configure your SenseML so that each document extraction outputs identically named fields. For more information about the conversion process, see [SenseML to spreadsheet reference](https://docs.sensible.so/docs/excel-reference).

### Example

```javascript
const excelDownloadURL = (await sensible.generateExcel(results)).url;
```

### Parameters

See the following table for information about parameters:

| key  | value                      | description                                                  |
| ---- | -------------------------- | ------------------------------------------------------------ |
| n/a  | object or array of objects | Specify the completed results from an extraction request, or an array of completed results. |

### Returns

Sensible converts the results to an Excel file and returns the link for downloading the file.

## Classify method

### Description

Classify a document by type, as specified by the document types defined in your Sensible account. For more information, see [Classifying documents by type](doc:classify).

### Example

```javascript
const blob = await fs.readFile("./YOUR_DOCUMENT.pdf");
const request = await sensible.classify({file: blob}); 
```

### Parameters

See the following table for classification parameters:

| key  | value  | description                                                  |
| ---- | ------ | ------------------------------------------------------------ |
| file | string | Pass the non-encoded document bytes.  You can classify documents in the following file formats:   For information about supported file types, see  [Extract data from a document](https://docs.sensible.so/reference/extract-data-from-a-document). |

### Returns

Get results from this method by calling the Wait For method. For the schema for the results of a classification request , see [Classify document by type (sync)](https://docs.sensible.so/reference/classify-document-sync) and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.
