---
title: "Developer quickstart"
hidden: false

---

Introduction
====
Sensible extracts structured data from document such as PDFs using SenseML, a JSON-formatted query language.

In this quickstart, use an example SenseML configuration and example PDF to get a quick "hello world" API response. 

- If you instead want a guided tour of SenseML concepts, see [Getting started](doc:getting-started).

- If you instead want to explore SenseML without much explanation, then [sign up](https://app.sensible.so/register) for an account and check out our interactive in-app tutorials: [extract_your_first_data](https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data), [tables and rows](https://app.sensible.so/editor/?d=senseml_basics&c=2_tables_and_rows&g=2_tables_and_rows), [checkboxes, paragraphs, and regions](https://app.sensible.so/editor/?d=senseml_basics&c=3_checkboxes_paragraphs_and_regions&g=3_checkboxes_paragraphs_and_regions), and a [blank-slate challenge](https://app.sensible.so/editor/?d=senseml_basics&c=4_extract_from_scratch&g=4_extract_from_scratch).


Extract example document data
=====

To run an API call and return extracted, structured data from a downloaded example document: 

1. Get an account at [sensible.so](https://app.sensible.so/register).

    **NOTE** In the Sensible app, don't rename of the default doc type (**senseml_basics**) or delete the **1_extract_your_first_data** config, or this example fails. 

2. Copy the following code example:

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

3. Replace `<YOUR_API_TOKEN>` with your API key in the preceding code example. Find your key on your [account page](https://app.sensible.so/account/).

4. Run the code sample in a command prompt. The API returns a `parsed_document` object with the extracted data, as well as metadata about the extraction, in a response like the following:

```json
{
   "id":"153753e0-5673-466f-aa61-5175200c210d",
   "created":"2022-02-02T21:30:01.981Z",
   "status":"COMPLETE",
   "type":"senseml_basics",
   "configuration":"1_extract_your_first_data",
   "parsed_document":{
      "your_first_extracted_field":{
         "type":"string",
         "value":"Welcome to your first document"
      }
   },
   "validations":[
      
   ],
   "validation_summary":{
      "fields":1,
      "fields_present":1,
      "errors":0,
      "warnings":0,
      "skipped":0
   },
   "classification_summary":[
      {
         "configuration":"1_extract_your_first_data",
         "score":{
            "value":1,
            "fields_present":1,
            "penalties":0
         }
      },
      {
         "configuration":"2_tables_and_rows",
         "score":{
            "value":0,
            "fields_present":0,
            "penalties":0
         }
      },
      {
         "configuration":"3_checkboxes_paragraphs_and_regions",
         "score":{
            "value":0,
            "fields_present":0,
            "penalties":0
         }
      },
      {
         "configuration":"4_extract_from_scratch",
         "score":{
            "value":0,
            "fields_present":0,
            "penalties":0
         }
      }
   ],
   "errors":[
      
   ]
}
```

 

(Optional) See how it works in the Sensible app
=====

To see this example in the Sensible app:

1. Log into the [Sensible app](https://app.sensible.so/signin/).

2. Navigate to the [first tutorial](https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data) config.
   
3. Visually examine the example PDF (middle pane), config (left pane), and extracted data (right pane) to better understand the API call you just ran:
   

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quick_1.png) 



Next
===

- Learn concepts with more detailed examples in the [Getting Started Guide](doc:getting-started)
- Check out the [SenseML method reference docs](doc:methods) to write your own extractions
- See the [API reference](https://docs.sensible.so/reference/choosing-an-endpoint) and [example code](https://github.com/sensible-hq/sensible-code-examples)
