---
title: "API quickstart"
hidden: false

---

Introduction
====
In this quickstart, use an example SenseML configuration and example document to get a quick "hello world" API response. 



- To get started with extracting from your custom documents, see [Getting Started](doc:getting-started-ai).




Extract example document data
=====

To run an API call and return extracted, structured data from a downloaded example document: 


1. Get an account at [sensible.so](https://app.sensible.so/register).

    **NOTE** In the Sensible app, don't rename the example doc type (**layout_basics**) or delete the **1_extract_your_first_data** config, or this example fails. 

1. Copy your API key from your [account page](https://app.sensible.so/account/).

2. Copy the following code example into a plain-text application and replace `*YOUR_API_KEY*` with your API key:


```shell
curl -L https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/1_extract_your_first_data.pdf --output 1_extract_your_first_data.pdf && curl --request POST --url "https://api.sensible.so/v0/extract/layout_basics" --header "Authorization: Bearer YOUR_API_KEY" --header "Content-Type: application/pdf" --data-binary "@1_extract_your_first_data.pdf"

```


3. Run the code sample in a command prompt. The code downloads an example document (`1_extract_your_first_data.pdf` ) and runs it against an example document type (`layout_basics`). The following excerpt of the API response shows the extracted document text in the `parsed_document` object: 

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

2. Navigate to the [first tutorial](https://app.sensible.so/editor/?d=layout_basics&c=1_extract_your_first_data&g=1_extract_your_first_data) config.
   
3. Visually examine the example document (middle pane), config (left pane), and extracted data (right pane) to better understand the API call you just ran:
   

![q](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quick_1.png) 



Next
===

- See the [API reference](https://docs.sensible.so/reference/choosing-an-endpoint) and [example code](https://github.com/sensible-hq/sensible-code-examples)
- If you're new to APIs, see [API tutorials](doc:api-tutorial)
- To get started with authoring extraction configurations, or configs, for your custom documents, see [Getting Started](doc:getting-started-ai).
