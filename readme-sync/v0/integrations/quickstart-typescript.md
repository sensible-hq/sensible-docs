---
title: "Typescript SDK quickstart"
hidden: true
---

## Overview

BLURB FOR GITHUB README (if public repo)>>>>Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. It's highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large-language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful document primitives.<<<<

TODO: Simplify this image background?

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intro_sdk.png)

This quickstart provides an overview of the Sensible Typescript SDK. Use this SDK to:

- [extract](doc:quickstart-typescript#extract-document-data): extract structured data from your custom documents. You configure the extractions for a set of similar documents, or *document type*, in the Sensible app or Sensible API, then you run extractions for documents of the type with this SDK. TODO: links to configuring SenseML
- [classify](doc:quickstart-typescript#classify): classify documents by the types you define. For example, use classification to determine which documents to extract prior to calling a Sensible extraction endpoint, or route each document or to label each document in a system of record.

## Install

In an environment in which you've installed Typescript, create a test project and install the dependencies:    TODO/TBD: options will we offer? yarn etc?

```shell
npm install sensible-sdk
```

To import Sensible and other dependencies to your project, navigate to your test project directory, create an `index.ts` file, and add the following lines to the file:

```typescript
import { promises as fs } from "fs";
import { SensibleSdk } from "sensible-sdk";
```

## Initialize

Get an account at [sensible.so](https://app.sensible.so/register) if you don't have one already.

To initialize the dependency using your [API key](https://app.sensible.so/account/?t=api_keys), replace `apiKey` with your API key in your `index.ts` file:

```typescript
const sensible = new sensibleSdk(apiKey);
```

**Note** In production ensure your API key is properly secured, for example as a Github secret.

## Extract document data

#### Option 1

To extract data from a sample document at a URL:

1. add the following lines to your `index.ts` file:

```typescript
const request = await sensible.extract({
      url: "TODO_URL.pdf",
      documentType: "senseml_instruct_basics",
      environment: "development" // see Typescript SDK reference for configuration options
    });
const results = await sensible.waitFor(request);
console.log(results);


```

2. In a command prompt in the same directory as your `index.ts` file, run the extraction with the following command: `ts-node index.ts`.

The code extracts data from an example PDF (`contract.pdf`) using an example document type (`senseml_instruct_basics`). 

#### Option 2

To extract from a local file: 

1.  Download the following example file and save it in the same directory as your `index.ts` file: 

2. | Example PDF | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/contract.pdf) |
   | ----------- | ------------------------------------------------------------ |

3. Replace the preceding code with the following code, then run it according to the steps in the previous option:

```typescript
const blob = await fs.readFile("./contract.pdf");
const request = await sensible.extract({
      file: blob,
      documentType: "senseml_instruct_basics",
      environment: "development" // see Typescript SDK reference for configuration options
    });
const results = await sensible.waitFor(request);
console.log(results);
```

This code uploads your local file to a Sensible-hosted URL and extracts data from an example PDF (`contract.pdf`) using an example document type (`senseml_instruct_basics`). 

#### Check results

The following excerpt of the results shows the extracted document text in the `parsed_document` object:

```typescript
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

For more information about the response body schema, see <https://docs.sensible.so/reference/extract-data-from-a-document> and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

#### Optional: understand extraction

Navigate to https://app.sensible.so/editor/instruct/?d=sensible_instruct_basics&c=contract&g=contract to see how the extraction you just ran works in the Sensible app. You can add more field queries to extract more data:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sdk_typescript_1.png)

#### Complete code example

Here's a complete example of how to use the SDK in your own app. TODO: decide if complete code example should have download URL or local file?

```typescript
import { promises as fs } from "fs";
import { SensibleSdk } from "sensible-sdk"

const sensible = new SensibleSDK(apiKey);
const blob = await fs.readFile("./contract.pdf");
const request = await sensible.extract({
      file: blob,
      documentType: "senseml_instruct_basics",
      environment: "development" // see Typescript SDK reference for configuration options
    });
const results = await sensible.waitFor(request);
console.log(results);
```



## Classify

You can classify a document by its similarity to each document type you define in your Sensible account. For example, if you define a [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/bank_statements) type and a [tax_forms](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms) type in your account, you can classify 1040 forms, 1099 forms, Bank of America statements, Chase statements, and other documents, into those two types.

See the following complete code example for classifying a document.

```typescript
import { promises as fs } from "fs";
import { SensibleSdk } from "sensible-sdk"

const sensible = new SensibleSDK(apiKey);
const blob = await fs.readFile("./contract.pdf");
const request = await sensible.classify({file: blob});
const result = await sensible.waitFor(request);
```



## Next

To configure options for extraction and classification, see [Typescript SDK reference](doc:sdk-typescript).



BLURB FOR GITHUB README: >>>> To learn more about Sensible's developer platform, see [Sensible documentation](https://docs.sensible.so/docs/). <<<