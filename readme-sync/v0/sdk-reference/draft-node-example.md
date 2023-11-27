---
title: "draft sdk code"
hidden: true
---

# Sensible Node SDK

The open-source Sensible Node SDK offers convenient access to the [Sensible API](https://docs.sensible.so/reference/choosing-an-endpoint). Use the Sensible Node SDK to:

- [Extract](#extract-document-data): Extract structured data from your custom documents. Configure the extractions for a set of similar documents, or *document type*, in the Sensible app or Sensible API, then you run extractions for documents of the type with this SDK.
- [Classify](#classify): Classify documents by the types you define, for example, bank statements or tax forms. Use classification to determine which documents to extract prior to calling a Sensible extraction endpoint, or route each document in a system of record.

## Documentation

For configuration options, see [Node SDK reference](https://docs.sensible.so/docs/sdk-node).

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
      environment: "development" // see Node SDK reference for full list of configuration options
    });
const results = await sensible.waitFor(request); // waitFor is optional if you configure a webhook
console.log(results); // see Node SDK reference to convert results from JSON to Excel
```

2. Replace `YOUR_API_KEY` with your [API key](https://app.sensible.so/account/):
3. In a command prompt in the same directory as your `index.mjs` file, run the code with the following command:

```shell
node index.mjs
```

The code extracts data from an example document (`contract.pdf`) using an example document type (`sensible_instruct_basics`) and an example extraction configuration.

### Results

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

#### 



## Workflows

### Extraction workflow

See the following steps for an overview of the SDK's workflow for document data extraction. Every method returns a chainable promise:

1. Instantiate an SDK object (`new SensibleSDK()`. 
2. Request a document extraction (`sensible.extract()` with the following required parameters:
   1.  **(required)** Specify the document from which to extract data using the `url`, `path`, or `file` parameter. 
   2.  **(required)** Specify the user-defined document type or types using the `documentType` or `documentTypes` parameter.
3. Wait for the result. Use (`sensible.waitFor()`,  or use a webhook.
4. Optionally convert the result or results to Excel using `generateExcel()`.
5. Consume the data.

For a complete example, see TBD/TODO: [link to the bank statements example?] 

### Classification workflow

See the following steps for an overview of the SDK's workflow for classification. Every method returns a chainable promise:

1. Instantiate an SDK object (`new SensibleSDK("YOUR_API_KEY")`.

2. Request a document classification (`sensible.classify()`.  Specify the document to classify using the `file` parameter. See the Classify method for more information.

3. Consume the data.

   ```node
   import { SensibleSDK } from "sensible-api"
   
   const sensible = new SensibleSDK(YOUR_API_KEY);
   const request = await sensible.classify({path: "./YOUR_DOCUMENT.pdf"}); 
   const result = await sensible.waitFor(request);
   console.log(results);
   ```


## Usage: Extract document data

#### Extract from a local file

To extract from a local file:

1. Download the following example file and save it in the same directory as your `index.mjs` file:

| Example document | [Download link](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/contract.pdf) |
| ---------------- | ------------------------------------------------------------ |

2. Paste the following code into an empty `index.mjs` file, then run it according to the steps in the previous option:


```node
import { SensibleSDK } from "sensible-api"

const sensible = new SensibleSDK(YOUR_API_KEY);
const request = await sensible.extract({
      path: ("./contract.pdf"),
      documentType: "sensible_instruct_basics",
    });
const results = await sensible.waitFor(request); // waitFor is optional if you configure  a webhook
console.log(results); // see Node SDK reference to convert results from JSON to Excel
```

This code extracts data from a local file (`contract.pdf`) using an example document type (`sensible_instruct_basics`) and an example extraction configuration.

#### Check results

The following excerpt of the results shows the extracted document text in the `parsed_document` object:

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

For more information about the response body schema, see [Extract data from a document](https://docs.sensible.so/reference/extract-data-from-a-document) and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

#### Code example: Extract from PDFs in directory and convert to Excel

See the following code for a complete example of how to use the SDK for document extraction in your own app.

The example:

1. Filters a directory to find the PDF files.
2. Extracts data from the PDF files using the extraction configurations in a  `bank_statements` document type.
3. Writes the extractions into an Excel file.

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
    const file = await fs.readFile(`${dir}/${filename}`);
    return sensible.extract({
      file,
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

## Classify

You can classify a document by its similarity to each document type you define in your Sensible account. For example, if you define a [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/bank_statements) type and a [tax_forms](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms) type in your account, you can classify 1040 forms, 1099 forms, Bank of America statements, Chase statements, and other documents, into those two types.

See the following code example for classifying a document.

```node
import { SensibleSDK } from "sensible-api"

const sensible = new SensibleSDK(YOUR_API_KEY);
const request = await sensible.classify({path:"./boa_sample.pdf"});
const results = await sensible.waitFor(request);
console.log(results);
```

To classify an example document, take the following steps:

1. Follow the steps in the preceding sections to install the SDK.
2. Paste the preceding code into your `index.mjs` file. Ensure you replaced`YOUR_API_KEY` with your [API key](https://app.sensible.so/account/).
3. Follow the steps in [Out-of-the-box extractions](https://docs.sensible.so/reference/choosing-an-endpoint/library-quickstart) to add support for bank statements to your account.
4. Download the following example file and save it in the same directory as your `index.mjs` file:

| Example document | [Download link](https://github.com/sensible-hq/sensible-configuration-library/raw/main/bank_statements/bank_of_america/boa_sample.pdf) |
| ---------------- | ------------------------------------------------------------ |

5. In a command prompt in the same directory as your `index.mjs` file, run the code with the following command:

```shell
node index.mjs
```

#### Check results

The following excerpt of the results shows that Sensible classifies the example document as a bank statement, and most probably as a Bank of America statement:

```json
{
  "document_type": {
    "id": "22666f4f-b8d6-4cb5-ad52-d00996989729",
    "name": "bank_statements",
    "score": 0.8922476745112722
  },
  "reference_documents": [
    {
      "id": "c82ac28e-7725-4e42-b77c-e74551684caa",
      "name": "boa_sample",
      "score": 0.9999980536061833
    },
    {
      "id": "f80424a0-58f8-40e7-814a-eb49b199221e",
      "name": "wells_fargo_checking_sample",
      "score": 0.8946129923339182
    },
    {
      "id": "cf17daf8-7e8b-4b44-bc4b-7cdd6518d963",
      "name": "chase_consolidated_balance_summary_sample",
      "score": 0.8677569417649393
    }
  ]
}
```

### 

