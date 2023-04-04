---
title: "Developer quickstart"
hidden: false

---

Introduction
====
In this quickstart, use an example SenseML configuration and example PDF to get a quick "hello world" API response. 



- To get started with extracting from your custom documents, see [Overview](doc:overview).




Extract example document data
=====

To run an API call and return extracted, structured data from a downloaded example document: 



TODO: update 1_extract_your_first_data config to a sensible instruct config.

1. Get an account at [sensible.so](https://app.sensible.so/register).

    **NOTE** In the Sensible app, don't rename of the default doc type (**senseml_basics**) or delete the **1_extract_your_first_data** config, or this example fails. 

1. Copy your API key from your [account page](https://app.sensible.so/account/).

2. Copy the following code example into a plain-text application and replace <YOUR_API_TOKEN> with your API key:

[block:code]
{
  "codes": [
    {
      "code": "curl -L https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/1_extract_your_first_data.pdf \\\n  --output 1_extract_your_first_data.pdf && \\\ncurl --request POST \\\n  --url \"https://api.sensible.so/v0/extract/senseml_basics\" \\\n  --header \"Authorization: Bearer <YOUR_API_TOKEN>\" \\\n  --header \"Content-Type: application/pdf\" \\\n  --data-binary \"@1_extract_your_first_data.pdf\" \n",
      "language": "shell",
      "name": "Linux/Mac"
    },
    {
      "code": "curl -L https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/1_extract_your_first_data.pdf ^\n  --output 1_extract_your_first_data.pdf && ^\ncurl --request POST ^\n  --url \"https://api.sensible.so/v0/extract/senseml_basics\" ^\n  --header \"Authorization: Bearer <YOUR_API_TOKEN>\" ^\n  --header \"Content-Type: application/pdf\" ^\n  --data-binary \"@1_extract_your_first_data.pdf\" \n",
      "language": "shell",
      "name": "Windows"
    }
  ]
}
[/block]

3. Run the code sample in a command prompt. The code downloads an example PDF (`1_extract_your_first_data.pdf` ) and runs it against an example document type (`senseml_basics`). The following excerpt of the API response shows the extracted document text in the `parsed_document` object: 

```json
{
   "parsed_document":{
      "your_first_extracted_field":{
         "type":"string",
         "value":"Welcome to your first document"
      }
   }
}
```

 

(Optional) See how it works in the Sensible app
=====

To see this example in the Sensible app:

1. Log into the [Sensible app](https://app.sensible.so/signin/).

2. Navigate to the [first tutorial](https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data) config.
   
3. Visually examine the example PDF (middle pane), config (left pane), and extracted data (right pane) to better understand the API call you just ran:
   

![q](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quick_1.png) 



Next
===

TODO update links?

- Learn concepts with more detailed examples in the [Getting started with SenseML](doc:getting-started)
- Check out the [SenseML method reference docs](doc:methods) to write your own extractions
- See the [API reference](https://docs.sensible.so/reference/choosing-an-endpoint) and [example code](https://github.com/sensible-hq/sensible-code-examples)
