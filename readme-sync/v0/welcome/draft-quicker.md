---
title: "Quicker start"
hidden: true

---

Extract example document data
=====

To run an API call and return extracted data from an example document: 

1. Get an account at [sensible.so](https://app.sensible.so/register).

    **NOTE** In the Sensible app,don't modify the name of the default doc type (**senseml_basics**) or delete the **1_extract_your_first_data1** config, or this example fails. 

2. Copy the following code example:

    ```curl
    curl -L https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/1_extract_your_first_data.pdf  --output 1_extract_your_first_data.pdf && \
    curl --request POST \
      --url "https://api.sensible.so/v0/extract/senseml_basics" \
      --header "Authorization: Bearer e08b909f931072f8ba45ad7fd512a0b4e48ac59c4a03278dc1ebe062dfa0d98f90eff12a5b61fdc55e6102d7cf06e33aa8de5e90c6ea33a56b001210255c2d8d" \
      --header "Content-Type: application/pdf" \
      --data-binary "@1_extract_your_first_data.pdf" \
    | json_pp
    
    ```

    

2. Replace `<YOUR_API_TOKEN>` with your API key in the preceding code example. Find it on your [account page][https://app.sensible.so/account/].

4. Run the code sample: In a **Linux** or **Mac** command line, paste in the code example. (For **Windows** command prompt, modify the code by replacing multiline indicators (\) with backticks (`) ).


You should see an API response like the following:



```json
{
   "configuration" : "1_extract_your_first_data",
   "created" : "2022-01-18T19:44:48.967Z",
   "errors" : [],
   "id" : "7b675925-a7d8-487e-bc20-61f2c8e6c635",
   "parsed_document" : {
      "your_first_extracted_field" : {
         "type" : "string",
         "value" : "Welcome to your first document"
      }
   },
   "status" : "COMPLETE",
   "type" : "senseml_basics",
   "validation_summary" : {
      "errors" : 0,
      "fields" : 1,
      "fields_present" : 1,
      "skipped" : 0,
      "warnings" : 0
   },
   "validations" : []
}
```

 

(Optional) See how it works in the Sensible app
=====

   To see this example in the Sensible app:

   1. Log into the [Sensible app](https://app.sensible.so/signin/).
      2. Navigate to [https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data](https://app.sensible.so/editor/?d=senseml_basics&c=1_extract_your_first_data&g=1_extract_your_first_data).
      
      3. Visually examine the example PDF (middle pane), config (left pane), and extracted data (right pane) to better understand the API call you just ran:
      
         ![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/quick_1.png) 



Next
===

- Learn more concepts with [Getting Started](doc:quickstart)

- Check out the [SenseML method reference docs](doc:methods) to write your own extractions

