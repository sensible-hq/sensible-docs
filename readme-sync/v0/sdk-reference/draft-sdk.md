---
title: "draft sdk code"
hidden: true
---

# Sensible Node SDK

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. use Sensible to build document-automation features into your SaaS products. Sensible is highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large-language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful document primitives.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intro_SDK_2.png)

This open-source Sensible SDK offers convenient access to the [Sensible API](https://docs.sensible.so/reference/choosing-an-endpoint). Use this SDK to:

- [Extract](#extract-document-data): Extract structured data from your custom documents. Configure the extractions for a set of similar documents, or *document type*, in the Sensible app or Sensible API, then run extractions for documents of the type with this SDK.
- [Classify](#classify): Classify documents by the types you define, for example, bank statements or tax forms. Use classification to determine which documents to extract prior to calling a Sensible extraction endpoint, or route each document in a system of record.

## Documentation

For configuration options, see [Node SDK reference](https://docs.sensible.so/docs/sdk-node). TODO: where to link to instead?? the Sensible API?

## Versions

- The latest version of this SDK is v0.
- The latest version of the Sensible API is v0.

## Node and Typescript support

- This SDK supports all non end-of-life Node versions.
- This SDK supports all non end-of-life Typescript versions.

## Install

In an environment in which you've installed Node, create a directory for a test project, open a command prompt in the directory, and install the dependencies:

```shell
npm install sensible-api
```

To import Sensible and other dependencies to your project,  create an `index.mjs` file in your test project, and add the following lines to the file:

```node
import { SensibleSDK } from "sensible-api";
```

## Initialize

Get an account at [sensible.so](https://app.sensible.so/register) if you don't have one already.

To initialize the dependency, paste the following code into your `index.mjs` file and replace `YOUR_API_KEY` with your [API key](https://app.sensible.so/account/):

```node
const sensible = new SensibleSDK(YOUR_API_KEY);
```

**Note** In production ensure you secure your API key, for example as a GitHub secret.

## Quickstart

To extract data from a sample document at a URL:

1. Install the Sensible SDK using the steps in the previous section.
2. Paste the following code into an empty `index.mjs` file:

```node
import { SensibleSDK } from "sensible-api"

const sensible = new SensibleSDK(YOUR_API_KEY); //replace with your API key
const request = await sensible.extract({
      url: "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/contract.pdf",
      documentType: "sensible_instruct_basics",
      environment: "development" // see Node SDK reference for full list of configuration options TODO reword
    });
const results = await sensible.waitFor(request); // polls every 5 seconds. Optional if you configure a webhook
console.log(results); // see Node SDK reference to convert results from JSON to Excel TODO change wording
```

2. Replace `YOUR_API_KEY` with your [API key](https://app.sensible.so/account/):
3. In a command prompt in the same directory as your `index.mjs` file, run the code with the following command:

```shell
node index.mjs
```

The code extracts data from an example document (`contract.pdf`) using an example document type (`sensible_instruct_basics`) and an example extraction configuration.

#### Results

You should see the following extracted document text in the `parsed_document` object in the logged response:

```json
{
  "purchase_price": {
    "source": "$400,000",
    "value": 400000,
    "unit": "$",
    "type": "currency"
  },
  "street_address": {
    "value": "1234 ABC COURT City of SALT LAKE CITY County of Salt Lake -\nState of Utah, Zip 84108",
    "type": "address"
  }
}
```

#### Optional: Understand extraction

Navigate to https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=contract&g=contract to see how the extraction you just ran works in the Sensible app. You can add more fields to the extraction configuration to extract more data:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sdk_node_1.png)

## Usage: Extract document data

You can extract data from a document, as specified by the extraction configurations and document types defined in your Sensible account.

### Overview

See the following steps for an overview of the SDK's workflow for document data extraction. Every method returns a chainable promise:

1. Instantiate an SDK object with `new SensibleSDK()`. 
2. Request a document extraction with `sensible.extract()` . Use the following required parameters:
   1.  **(required)** Specify the document from which to extract data using the `url`, `path`, or `file` parameter. 
   2.  **(required)** Specify the user-defined document type or types using the `documentType` or `documentTypes` parameter.
3. Wait for the result. Use `sensible.waitFor()`,  or use a webhook.
4. Optionally convert extractions to Excel file with `generateExcel()`.
5. Consume the data.

### Extraction configuration

 You can configure several options for document data extraction:


```node
import { SensibleSDK } from "sensible-api"

const sensible = new SensibleSDK(YOUR_API_KEY);
const request = await sensible.extract({
      path: ("./1040_john_doe.pdf"),
      documentType: "tax_forms",
      webhook: {
         url:"YOUR_WEBHOOK_URL",
         payload: "additional info, for example, a UUID for verification",
    });
```

See the following table for information about configuration options:

| key               | value                                                      | description                                                  |
| ----------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| path              | string                                                     | An option for submitting the document you want to extract data from.<br/> Pass the path to the document. For more information about supported file types, see  [Supported file types](doc:file-types). |
| file              | string                                                     | An option for submitting the document you want to extract data from.<br/> Pass the non-encoded document bytes. |
| url               | string                                                     | An option for submitting the document you want to extract data from.<br/>URL that responds to a GET request with the bytes of the document you want to extract data from. This URL must be either publicly accessible, or presigned with a security token as part of the URL path. To check if the URL meets these criteria, open the URL with a web browser. The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication. |
| documentType      | string                                                     | An option for specifying the document type or types.<br/>Type of document to extract from. Create your custom type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`). |
| documentTypes     | array                                                      | An option for specifying the document type or types.<br/>Types of documents to extract from. Use this parameter to extract from multiple documents that are packaged into one file (a "portfolio").  This parameter specifies the document types contained in the portfolio. Sensible then segments the portfolio into documents using the specified document types (for example, 1099, w2, and bank_statement) and then runs extractions for each document. For more information, see [Multi-doc extraction](doc:portfolio). |
| configurationName | string                                                     | If specified, Sensible uses the specified config to extract data from the document instead of automatically choosing the best-scoring extraction in the document type.<br/>If unspecified, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type.<br/>Not applicable for portfolios. |
| documentName      | string                                                     | If you specify the filename of the document using this parameter, then Sensible returns the filename in the extraction response and populates the file name in the Sensible app's list of recent extractions. |
| environment       | `"production"` or `"development"`. default: `"production"` | If you specify `development`, Sensible extracts preferentially using config versions published to the development environment in the Sensible app. The extraction runs all configs in the doc type before picking the best fit. For each config, falls back to production version if no development version of the config exists. |
| webhook           | object                                                     | Specifies to return extraction results to the specified webhook URL as soon as they're complete, so you don't have to poll for results status. Sensible also calls this webhook on error.<br/> The webhook object has the following parameters:<br/>`url`:  string. Webhook destination. Sensible will POST to this URL when the extraction is complete.<br/>`payload`: string, number, boolean, object, or array. Information additional to the API response, for example a UUID for verification. |

### Extraction results

Get extraction results by using a webhook or calling the Wait For method.

For the schema for the results of an extraction request,  see [Extract data from a document](https://docs.sensible.so/reference/extract-data-from-a-document) and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

### Example: Extract from PDFs in directory and output an Excel file

See the following code for a complete example of how to use the SDK for document extraction in your own app.

The example:

1. Filters a directory to find the PDF files.
2. Extracts data from the PDF files using the extraction configurations in a  `bank_statements` document type.
3. Writes the extractions to an Excel file. For more information about the conversion process, see [SenseML to spreadsheet reference](https://docs.sensible.so/docs/excel-reference).

```node
import { promises as fs } from "fs";
import { SensibleSDK } from "sensible-sdk";
import got from "got";
const apiKey = process.env.SENSIBLE_APIKEY;
const sensible = new SensibleSDK(apiKey);
const dir = process.argv[2];
const files = (await fs.readdir(dir)).filter((file) => file.match(/\.pdf$/));
const extractions = await Promise.all(
  files.map(async (filename) => {
    const path = `${dir}/${filename}`;
    return sensible.extract({
      path,
      documentType: "bank_statements",
    });
  })
);
await Promise.all(
  extractions.map((extraction) => sensible.waitFor(extraction))
);
const excel = await sensible.generateExcel(extractions);
console.log(excel);
const excelFile = await got(excel.url);
await fs.writeFile(`${dir}/output.xlsx`, excelFile.rawBody);
```



## Usage: Classify documents by type

You can classify a document by type, as specified by the document types defined in your Sensible account. For more information, see [Classifying documents by type](https://docs.sensible.so/docs/classify).

### Overview

See the following steps for an overview of the SDK's workflow for document classification. Every method returns a chainable promise:

1. Instantiate an SDK object (`new SensibleSDK()`.

2. Request a document classification (`sensible.classify()`.  Specify the document to classify using the `path` or  `file` parameter.

3. Poll for the result (`sensible.waitFor()`.

4. Consume the data.


### Classification configuration

You can configure options for document data extraction:

```node
import { SensibleSDK } from "sensible-api"

const sensible = new SensibleSDK(YOUR_API_KEY);
const request = await sensible.classify({
  path:"./boa_sample.pdf"
  });
const results = await sensible.waitFor(request);
console.log(results);
```

See the following table for information about configuration options:

| key  | value  | description                                                  |
| ---- | ------ | ------------------------------------------------------------ |
| path | string | An option for submitting the document you want to extract data from. Pass the path to the document. For more information about supported file types, see [Supported file types](https://docs.sensible.so/docs/file-types). |
| file | string | Pass the non-encoded document bytes. For information about supported file types, see [Supported file types](https://docs.sensible.so/docs/file-types). |

### Classification results

Get results from this method by calling the Wait For method. For the schema for the results of a classification request , see [Classify document by type (sync)](https://docs.sensible.so/reference/classify-document-sync) and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.



