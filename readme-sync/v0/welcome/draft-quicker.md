---
title: "Quicker start"
hidden: true

---

Extract data from an example document
=====



TODOs:

- add a link to this quickstart from the last cheatsheet?? 

- add a link to this quickstart at the top of the getting started explaining this is quick vs the GSG is conceptual.

- fix all links

  

  

1. Get an account at [sensible.so](https://www.sensible.so/get-early-access).
2. Clone a code sample in your preferred language:
  - [Python](https://github.com/fscelliott/sens-code-example) TODO: take the code sample below and put in dir and verify it works.
  - other languages TBD  


2. Add your api key to the code sample. For example, in the Python example, replace `"YOUR_API_KEY"` with your key. Find your API key in the dashboard at [TBD LINK TO ACCOUNT PAGE].

  

  ```python
  #!/usr/local/bin/python
  
  '''
  This script asynchronously extracts structured data from the specified PDF.
  For more information, see https://docs.sensible.so/docs/api-tutorial-async-1.
  '''
  
  import time
  import json
  import requests
  
  # The name of a document type in Sensible, e.g., auto_insurance_quote
  DOCUMENT_TYPE = "tutorials"
  # The URL of the PDF you'd like to extract from
  DOCUMENT_URL = "https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/walkthrough_1.pdf"
  # Your Sensible API key
  API_KEY = "YOUR_API_KEY"
  
  
  def extract_from_doc_url():
      headers = {
          'Authorization': 'Bearer {}'.format(API_KEY),  'Content-Type': 'application/json'
      }
      body = json.dumps({"document_url": DOCUMENT_URL})
      response = requests.request(
          "POST",
          "https://api.sensible.so/v0/extract_from_url/{}".format(
              DOCUMENT_TYPE),
          headers=headers,
          data=body)
      try:
          response.raise_for_status()
      except requests.RequestException:
          print(response.text)
      else:
          document_extraction = response.json()
          poll_count = 0
          # In production you'd use a webhook to avoid polling
          while document_extraction["status"] == "WAITING":
              # Wait a few seconds before each poll until the extraction completes
              time.sleep(3)
              poll_count += 1
              response = requests.request(
                  "GET",
                  "https://api.sensible.so/v0/documents/{}".format(document_extraction['id']),
                  headers=headers)
              try:
                  response.raise_for_status()
              except requests.RequestException:
                  print(response.text)
                  break
              else:
                  document_extraction = response.json()
                  print("Poll attempt: {}, status: {}".format(
                      poll_count, document_extraction["status"]))
          print(json.dumps(document_extraction, indent=2))
  
  
  if __name__ == '__main__':
      extract_from_doc_url()
  ```



  

4. Run the code sample. In the command line in the cloned directory, run `python extract_example_doc.py`.




You should see a response like the following:



```json
{
    "id": "1b86d404-6dc5-4878-a495-6fce40c7ea06",
    "created": "2022-01-05T17:02:02.283Z",
    "status": "COMPLETE",
    "type": "auto_insurance_quote",
    "configuration": "anyco_multidoc",
    "parsed_document": {
  "your_first_extracted_field": {
    "type": "string",
    "value": "Welcome to your first document"
  }
},
    "validations": [],
    "validation_summary": {
        "fields": 1,
        "fields_present": 1,
        "errors": 0,
        "warnings": 0,
        "skipped": 0
    }
}
```

 

Optional: see how it works in the Sensible app
=====

   To see this example in the Sensible app:

   1. Log into the Sensible app at [app.sensible.so](https://app.sensible.so/) using your API key.
      2. Navigate to https://dev.sensible.so/editor/?d=senseml_basics&c=walkthrough_1&g=walkthrough_1.
      3.  Visually examine the PDF (middle pane), config (left pane), and extracted data (right pane) you just ran in the previous code sample:
         ![image-20220105100032719](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20220105100032719.png)



Next
===

- Learn more with [Getting Started](doc:quickstart)

- Check out the [SenseML method reference docs](doc:methods) to write your own extractions

  
