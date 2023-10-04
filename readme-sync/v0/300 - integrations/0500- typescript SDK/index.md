---
title: "SDK introduction"
hidden: true
---

This topic gives an overview and links to the Sensible Typescript SDK.

Overview
---

Use Sensible's Typescript SDK to extract structured data from documents.

**Quick example: Extraction**

The following example shows extraction code and the data it delivers:

```typescript
blah blah
```

Which returns the following from an example PDF:

```json
{some quick policy period or something}
```

TODO: image of PDF with extracted data highlighted.

These 3 lines of code perform the following before delivering the structured data:

- upload the document 
- use an existing config to extract the document. You've got to write the config yourself
- send the info to a webhook or back to you



Similarly, you can also classify documents with the Sensible SDK [TODO LINK] 






This reference guide describes how to use the Sensible Typescript SDK.

### VersionThis topic gives an overview and links to the Optimizely Python SDK.

[Suggest Edits](https://docs.developers.optimizely.com/full-stack-experimentation/edit/python-sdk)

This reference guide describes how to use the Optimizely Python SDK.

### Version

For the current version number of this SDK, see [SDK Compatibility Matrix](https://docs.developers.optimizely.com/full-stack-experimentation/docs/sdk-feature-compatibility#current-sdk-versions).

### Quickstart

To get up and running quickly, see the [API quickstart](https://docs.developers.optimizely.com/full-stack-experimentation/docs/python-quickstart).

### Reference

For reference docs, see the left-hand navigation, or start off with [Install SDK](https://docs.developers.optimizely.com/full-stack-experimentation/docs/install-sdk-python).

### Source files

- [Python SDK repo](https://github.com/optimizely/python-sdk)
- [changelog](https://github.com/optimizely/python-sdk/blob/master/CHANGELOG.md)



# Install SDK

```typescript
npm install -g sensible-sdk
```

In a terminal, set your `CLOUDINARY_URL` environment variable.

Replace `CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME` with the **API environment variable** copied from your product environment credentials:

- On Mac or Linux:

  

  ```
  export CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
  ```

- On Windows:

  

  ```
  set CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
  ```


Important



- When writing your own applications, follow your organization's policy on storing secrets and don't expose your API secret.
- If you use a method that involves writing your environment variable to a file (e.g. `dotenv`), the file should be excluded from your version control system, so as not to expose it publicly.



# Example Usage (for typescript extract)

```
const sensible = new Sensible(apiKey);
const result = await sensible.waitFor(await sensible.extract({file: blob, documentType: "blabla"}));
```

Or a use that would work with existing docs:

In a new file called `test.ts`

```typescript
// TODO: understand this 'new' langauge versus 'require' again..
/* find your api key at account. */
const sensible = new Sensible(apiKey);
/* use an example 'contract' document type and example contract doc for this to work. */
const result = await sensible.waitFor(await sensible.extract({url: github_storage_for_contract, documentType: "contract"}));
```

OTHER EXAMPLES:

- portfolio extraction
- extract at your URL + webhook?

This gets you back a JSON payload that includes a `parsed_document` with the following fields:

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

TODO: mimic the structure of the 'developer quickstart'?

For more information about the returned payload response, see https://docs.sensible.so/reference/extract-data-from-a-document and expand both 200 responses to see the model and an example.

## Extract function

### Description

This method extracts structured data from a document. It's constructed like this:

```
declare class Sensible {
  constructor(apikey: string);
  extract(
    options: ({ url: string } | { file: Blob }) &
      (
        | { documentType: string; configurationName?: string }
        | { documentTypes: string[] }
      ) & {
        webhook?: Webhook;
        document_name?: string;
        environment?: string;
      }
  ): Promise<ExtractionRequest>;
  waitFor(task: ExtractionRequest): Promise<ExtractionResult;

}
type Webhook = ...; // sync with api types
type ExtractionRequest = {
  type: "extraction";
  id: string;
};
```





### Parameters



| key               | value                                                | description                                                  |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------------------ |
| file              | blob                                                 | One of two options for submitting the document you want to extract data from.<br/> Pass the non-encoded document bytes.  You can extract document data from the following file formats:   PDF JPEG PNG TIFF.  For more information about file types, see  https://docs.sensible.so/reference/extract-data-from-a-document.<br/>TODO how to word: Using this option automatically uploads the file to a `download_url` URL that Sensible generates. You'll get the `download_url` in the response. |
| url               | string                                               | One of two options for submitting the document you want to extract data from.<br/>URL that responds to a GET request with the bytes of the document you want to extract data from. This URL must be either publicly accessible, or presigned with a security token as part of the URL path. To check if the URL meets these criteria, open the URL with a web browser. The browser must either render the document as a full-page view with no other data, or download the document, without prompting for authentication. |
| documentType      |                                                      | Type of document to extract from. Create your custom type in the Sensible app (for example, `rate_confirmation`, `certificate_of_insurance`, or `home_inspection_report`).<br/>As a convenience, Sensible automatically detects the best-fit extraction from among the extraction queries ("configs") in the document type.<br/>For example, if you create an `auto_insurance_quotes` document type, you can add `carrier 1`, `carrier 2`, and `carrier 3` configs to the document type in the Sensible app. Then, you can extract data from all these carriers using the same document type, without specifying the carrier in the API request. |
| configurationName |                                                      | use with the Document Type parameter.  If specified, Sensible uses the specified config to extract data from the document instead of automatically choosing the best-scoring extraction in the document type. |
| documentTypes     |                                                      | Use this parameter with multiple documents that are packaged into one PDF file (a PDF "portfolio"), to specify the document types contained in the PDF portfolio. Sensible then segments the PDF into documents using the specified document types (for example, 1099, w2, and bank_statement) and then runs extractions for each document. |
| document_name     |                                                      | why is this snake case? raise it if you see it in the PR TODO |
| environment       | `production` or `development`. default: `production` | If you specify `development`, extracts preferentially using config versions published to the development environment in the Sensible app. The extraction runs all configs in the doc type before picking the best fit. For each config, falls back to production version if no development version of the config exists. |
| webhook???        |                                                      | Specifies to return extraction results to the defined webhook as soon as they're complete, so you don't have to poll for results status. Sensible also calls this webhook on error. TODO: how does this interact w the MVP poller? |

### Response

 `waitfor` only takes one request and returns one promise so we "folks can use the standard promise machinery to deal with multiple parallel requests" as Josh proposed.For the MVP we could generate a poller for each `waitFor` call, in the future we can create the "smart poller" that Jay proposed without having to change the API.

Once the promise 'resolves' (TODO correct wording),  this function returns structured data extracted from the document. For more information, see https://docs.sensible.so/reference/extract-data-from-a-document and expand the 200 responses in the middle pane and the right pane to see the model and an example, respectively.

