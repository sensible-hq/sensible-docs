# Optimizing PDF extraction performance with Sensible

##  What we'll cover

  * What impacts Sensible performance?
  * Rewrite SenseML queries for faster performance
  * Preferentially run or skip collections of queries ("configs") based on key text in documents. 



## What impacts Sensible performance?

First, let's clarify what _doesn't_** __** impact performance: the number of documents you submit has virtually no effect on processing time. Each document gets its own worker in parallel, whether you submit one or 50,000 documents. Instead, you can optimize:

  * document performance
  * document type performance



### Document performance

In an ideal performance scenario, you extract data from digitally generated PDFs using only text-based or coordinate-based SenseML methods, such as Label, Row, Region, Text Table, and Document Range.  


In the real world, things are never that simple. In order of slowest to quickest, these factors add seconds to doc processing:

#### **Over 10 seconds per document**  

**Whole-document OCR (for scanned documents)**  

Sensible takes 10 seconds or more to OCR an entire document. You can speed OCR up for shorter documents (5 pages or fewer) by choosing Sensible's Google OCR option.

**Whole-document table recognition**

Avoid configuring Sensible to search a whole document for tables. For a tutorial, see the "Add a Stop" section in this post.  


#### **Under 5 seconds per document**

**Selective OCR**  

Some documents mix digital text with text images, for example by embedding scanned pages in a digital PDF. Speed this up by OCRing select pages, not the whole document. For more information, see the [docs](https://docs.sensible.so/docs/ocr).  


**Selective table recognition**

Sensible process tables that include a stop in less than 5 seconds. Or, convert to a faster method that skips table recognition. For a tutorial, see "Add a Stop" and "Convert to faster query" sections in this post. 

#### **Under 1 second per document**

Some SenseML methods use pixels, for example to recognize borders. However, pixel recognition requires rendering a PDF page, which can take a couple hundred milliseconds. To improve processing time, use coordinate-based alternatives to these methods. 

**Boxes**

To improve processing speed, convert the more flexible Box method to the strictly coordinate-based Region method.

**Signature, checkbox, image coordinate extraction**

There are no alternative methods for signatures, checkboxes, and images. However, see the following section for ways to avoid running these methods except when absolutely necessary. 

### Document type performance

By default, Sensible runs all the configs in a document type before choosing the best one for a given document.  If your document type contains many different configs with computationally expensive methods such as Table or Box, you can improve performance by selectively running and skipping configs. For a tutorial, see the Skip queries section later in this post.  


Enough overview! Let's dive into some real-world optimizing.   


## Prerequisites  


  * You’ll need an account for [Sensible](https://www.sensible.so/get-early-access).  Or, read along for a rough idea of how things work.


  * Upload the [**Example commercial insurance application**](https://github.com/sensible-hq/sensible-docs/raw/main/readme-sync/assets/v0/pdfs/acord_125_test.pdf) to the Sensible app in a document type named "acord_application_test". If you're unfamiliar with the Sensible app, follow the steps in [create a document type and config](https://docs.sensible.so/docs/quickstart#create-a-config). Then, paste the following SenseML into an "acord_125_test config" in the Sensible app to extract the data:


    
    
    {
     
        "fields": [
          {
            "id": "loss_history",
            "anchor": "enter all claims or losses",
            "type": "table",
            "method": {
              "id": "fixedTable",
              "columnCount": 8,
              "columns": [
                {
                  "id": "date_of_occurence",
                  "type": "date",
                  "index": 0,
                  "isRequired": true
                },
                {
                  "id": "line",
                  "index": 1
                },
                {
                  "id": "description",
                  "index": 2
                },
                {
                  "id": "date_of_claim",
                  "type": "date",
                  "index": 3
                },
                {
                  "id": "amount_paid",
                  "type": "currency",
                  "index": 4
                },
                {
                  "id": "amount_reserved",
                  "type": "currency",
                  "index": 5
                },
                {
                  "id": "claim_status_open",
                  "index": 6
                },
                {
                  "id": "claim_status_closed",
                  "index": 7
                }
              ],
            }
          }
        ]
      }

You should see that Sensible recognizes the table (green box):

And you should see the following data extracted from the "loss history" table in the output pane:
    
    
    {
      "loss_history": {
        "columns": [
          {
            "id": "date_of_occurence",
            "values": [
              {
                "source": "10/16/2020",
                "value": "2020-10-16T00:00:00.000Z",
                "type": "date"
              },
              {
                "source": "07/12/2019",
                "value": "2019-07-12T00:00:00.000Z",
                "type": "date"
              }
            ]
          },
          {
            "id": "line",
            "values": [
              {
                "value": "PROP",
                "type": "string"
              },
              {
                "value": "PROP",
                "type": "string"
              }
            ]
          },
          {
            "id": "description",
            "values": [
              {
                "value": "Fire damage, 2020.",
                "type": "string"
              },
              {
                "value": "Burglary loss, 2019",
                "type": "string"
              }
            ]
          },
          {
            "id": "date_of_claim",
            "values": [
              {
                "source": "10/17/2020",
                "value": "2020-10-17T00:00:00.000Z",
                "type": "date"
              },
              {
                "source": "07/13/2019",
                "value": "2019-07-13T00:00:00.000Z",
                "type": "date"
              }
            ]
          },
          {
            "id": "amount_paid",
            "values": [
              {
                "source": "$ 10,000",
                "value": 10000,
                "unit": "$",
                "type": "currency"
              },
              {
                "source": "$ 5,000",
                "value": 5000,
                "unit": "$",
                "type": "currency"
              }
            ]
          },
          {
            "id": "amount_reserved",
            "values": [
              null,
              null
            ]
          },
          {
            "id": "claim_status_open",
            "values": [
              {
                "value": "",
                "type": "string"
              },
              {
                "value": "",
                "type": "string"
              }
            ]
          },
          {
            "id": "claim_status_closed",
            "values": [
              {
                "value": "N",
                "type": "string"
              },
              {
                "value": "N",
                "type": "string"
              }
            ]
          }
        ]
      }
    }
    
    
    

‍
