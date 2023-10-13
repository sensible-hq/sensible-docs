---
title: "Typescript SDK quickstart"
hidden: true
---

## Overview

Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. It's highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large-language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful document primitives.

This quickstart provides an overview of the Sensible Typescript SDK. Use this SDK to extract structured data from your custom documents. You configure the extractions for a set of similar documents, or *document type*, in the Sensible app or Sensible API, then you run extractions for documents of the type with this SDK. TODO: links to configuring SenseML

Sensible offers



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sdk.svg)



TODO: make sure beginners are comfy by talking about test directory and test `index.ts` file instructions + navigating dirs/files and running commands at right dirs.

## Install

In an environment where you have Node/Typescript installed (TODO reword?), install the dependencies using (npm/yarn/what?)

```shell
npm install SensibleSDK
```

Import Sensible and other dependencies to your project

```node
import { promises as fs } from "fs";
import { SensibleSDK } from "../src/index";
```

## Initialize

Get an account at [sensible.so](https://app.sensible.so/register) if you don't have one already.

Initialize the dependency using your API key TODO linke to the part of account with the key.  Replace `apiKey` with your API key in your project's `index.ts` file:

```node
const sensible = new SensibleSDK(apiKey);
```

**Note** In production ensure your API key is properly secured, for example as a Github secret.

## Extract document data

Extract data from a sample document that you can download from (TODO LINK TO GH in docs repo) to your project in the same directory as `index.ts`:

1. copy the following into an `index.ts` file in your project

```node
const blob = await fs.readFile("./contract.pdf");
const request = await sensible.extract({
      file: blob,
      documentType: "senseml_instruct_basics",
    });
const results = await sensible.waitFor(request);
console.log(results);
```

The code runs an example PDF (`contract.pdf`) against an example document type (`senseml_instruct_basics`). 

or, to extract directly from the URL without downloading the file locally, replace the preceding code with the following code:

```
const request = await sensible.extract({
      url: "TODO_URL.pdf",
      documentType: "senseml_instruct_basics",
    });
const results = await sensible.waitFor(request);
console.log(results);
```

2. Run the script in a command prompt: `ts-node index.ts`.

## Results

The following excerpt of the results shows the extracted document text in the `parsed_document` object:

```
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

For more information about the response body, see <https://docs.sensible.so/reference/extract-data-from-a-document> and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

### Optional: understand extraction configuration

See how the extraction you just ran works in the Sensible app:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sdk_typescript_1png)



## Source files

- [Typescript SDK repo](https://github.com/optimizely/python-sdk)
- changelog <-- todo maintain a changelog in the repo???

## Extraction Parameters

You can configure the following options for extraction:

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

See the following table for more information

| key               | value                                                | description                                                  |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| file              | blob                                                 | One of two options for submitting the document you want to extract data from.<br/> Pass the non-encoded document bytes.  You can extract document data from the following file formats:   PDF JPEG PNG TIFF.  For more information about file types, see  <https://docs.sensible.so/reference/extract-data-from-a-document>.<br/>TODO how to word: Using this option automatically uploads the file to a `download_url` URL that Sensible generates. You'll get the `download_url` in the response. |
| url               | string                                               | One of two options for submitting the document you want to extract data from.<br/>URL that responds to a GET request with the bytes of the document you want to extract data from. This URL must be either publicly accessible, or presigned with a security token as part of the URL path. To check if the URL meets these criteria, open the URL with a web browser. The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication. |
| documentType      |                                                      | Type of document to extract from. Create your custom type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`).<br/>As a convenience, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type.<br/>For example, if you create an `auto_insurance_quotes` document type, you can add `carrier 1`, `carrier 2`, and `carrier 3` configs to the document type in the Sensible app. Then, you can extract data from all these carriers using the same document type, without specifying the carrier in the API request. |
| documentTypes     |                                                      | Use this parameter to extract from multiple documents that are packaged into one PDF file (a PDF "portfolio").  This parameter specifies the document types contained in the PDF portfolio. Sensible then segments the PDF into documents using the specified document types (for example, 1099, w2, and bank_statement) and then runs extractions for each document. |
| configurationName |                                                      | use with the Document Type parameter.  If specified, Sensible uses the specified config to extract data from the document instead of automatically choosing the best-scoring extraction in the document type. |
| documentName      |                                                      | why is this snake case? raise it if you see it in the PR TODO |
| environment       | `production` or `development`. default: `production` | If you specify `development`, extracts preferentially using config versions published to the development environment in the Sensible app. The extraction runs all configs in the doc type before picking the best fit. For each config, falls back to production version if no development version of the config exists. |
| webhook           |                                                      | Specifies to return extraction results to the defined webhook as soon as they're complete, so you don't have to poll for results status. Sensible also calls this webhook on error. For a tutorial about using webhooks with Sensible, see [Try a webhook](doc:api-tutorial-webhook). |

