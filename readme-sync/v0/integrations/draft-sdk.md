---
title: "Typescript SDK quickstart"
hidden: true
---

TODO: slug: quickstart-typescript? 

## Overview

FOR GITHUB README>>>>Welcome! Sensible is a developer-first platform for extracting structured data from documents, for example, business forms in PDF format. It's highly configurable: you can get simple data in minutes by leveraging GPT-4 and other large-language models (LLMs), or you can tackle complex and idiosyncratic document formatting with Sensible's powerful document primitives.<<<<

This quickstart provides an overview of the Sensible Typescript SDK. Use this SDK to:

- [extract doc:typescript-quickstart#extract-document-data): extract structured data from your custom documents. You configure the extractions for a set of similar documents, or *document type*, in the Sensible app or Sensible API, then you run extractions for documents of the type with this SDK. TODO: links to configuring SenseML
- [classify doc:typescript-quickstart#classify): classify documents by the types you define. For example, use classification to determine which documents to extract prior to calling a Sensible extraction endpoint, or route each document or to label each document in a system of record.



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/intro_sdk.png)

TODO: make sure beginners are comfy by talking about test directory and test `index.ts` file instructions + navigating dirs/files and running commands at right dirs.

## Install

In an environment where you have Node/Typescript installed (TODO reword?), install the dependencies using (npm/yarn/what options will we offer?)

```shell
npm install sensible-sdk
```

Import Sensible and other dependencies to your project

```typescript
import { promises as fs } from "fs";
import { SensibleSdk } from "sensible-sdk";
```

## Initialize

Get an account at [sensible.so](https://app.sensible.so/register) if you don't have one already.

Initialize the dependency using your API key TODO linke to the part of account with the key.  Replace `apiKey` with your API key in your project's `index.ts` file:

```typescript
const sensible = new sensibleSdk(apiKey);
```

**Note** In production ensure your API key is properly secured, for example as a Github secret.

## Extract document data

Extract data from a sample document that you can download from (TODO LINK TO GH in docs repo) to your project in the same directory as `index.ts`:

1. copy the following into an `index.ts` file in your project

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

The code runs an example PDF (`contract.pdf`) against an example document type (`senseml_instruct_basics`). 

or, to extract directly from the URL without downloading the file locally, replace the preceding code with the following code:

```typescript
const request = await sensible.extract({
      url: "TODO_URL.pdf",
      documentType: "senseml_instruct_basics",
      environment: "development" // see Typescript SDK reference for configuration options
    });
const results = await sensible.waitFor(request);
console.log(results);
```

2. Run the script in a command prompt: `ts-node index.ts`.

#### Check for success

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

For more information about the response body, see <https://docs.sensible.so/reference/extract-data-from-a-document> and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

#### Optional: understand extraction

See how the extraction you just ran works in the Sensible app:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/sdk_typescript_1.png)

#### Complete code example

Here's a complete example of how to use the SDK in your own app.

```typescript

import { promises as fs } from "fs";
import { SensibleSdk } from "sensible-sdk"

const sensible = new SensibleSDK(apiKey);
const request = await sensible.extract({
      url: "TODO_URL.pdf",
      documentType: "senseml_instruct_basics",
      environment: "development" // see Typescript SDK reference for configuration options
    });
const results = await sensible.waitFor(request);
console.log(results);
```



## Classify

You can classify a document by its similarity to each document type you define in your Sensible account. For example, if you define a [bank statements](https://github.com/sensible-hq/sensible-configuration-library/tree/main/bank_statements) type and a [tax_forms](https://github.com/sensible-hq/sensible-configuration-library/tree/main/tax_forms) type in your account, you can classify 1040 forms, 1099 forms, Bank of America statements, Chase statements, and other documents, into those two types. For example, use classification to determine which documents to extract prior to calling a Sensible extraction endpoint, or route each document or to label each document in a system of record.

```typescript
import { promises as fs } from "fs";
import { SensibleSDK } from "../src/index";

const sensible = new SensibleSDK(apiKey);
const blob = await fs.readFile("./contract.pdf");
const request = await sensible.classify({file: blob});
const result = await sensible.waitFor(request);
```





## Next

To configure options for extraction and classification, see [Typescript SDK reference](doc:sdk-typescript).

To learn more about Sensible's developer platform, see [Sensible documentation](https://docs.sensible.so/docs/).
