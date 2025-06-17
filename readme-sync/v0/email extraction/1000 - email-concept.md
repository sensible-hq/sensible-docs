---
"title": "Email data extraction"
"hidden": true
---

## Introduction

You can automatically extract structured data from email bodies and attachments by forwarding them to Sensible. Define [document types](doc:document-type-settings) in the Sensible app to handle the extractions.

The following image shows an overview of  email extraction:



![image-20250617131007756](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20250617131007756.png)

TODO: add image here (email_overview.png)

## Implementation overview

To implement this workflow, take the following general steps:

**Configure email**

1. Determine a set of similar emails that you want to extract from. For example, you're in PropTech and you want to extract data from residential lease applications.
2. Define a Sensible forwarding email address for the set of emails. For example, `residential-lease-applications@sensible.so`.
3. Set up your email filters so your lease application emails automatically forward to the Sensible address.

**Configure data extraction**

1. In the Sensible app, define [document types](doc:document-type-settings) for each email attachment in the similar emails that you want to extract from and optionally one for the email body. For example, `driverse_licenses` and `paystubs` and `email_body_lease_applications`.

**Configure data destination**

1. Define a webhook to receive the extracted data, or view the extracted data in the Sensible app

The following sections provide more implementation detail.

## Getting started

Let's walk through an example scenario of extracting data from emails. In this example, you're in PropTech and you want to extract data from lease applications. 

This example uses the manager *Sensible Property*.  Lease application emails to this property manager typically include the following attachments:

- paystub
- drivers license
- signed lease
- email body that includes the applicant's name

Let's walk through extracting data from these email documents.

## Configure email

1. Determine your filtering criteria for forwarding lease applications for Sensible Property for extraction. For example, you filter on emails addressed to `applications@sensibleproperty.com`. 
2. Determine the name for the Sensible  email address to which you want to forward this set of emails. The email must be at the Sensible domain, for example, `residential-lease-applications@sensible.so`. You'll provide Sensible with this email address in a later step.

## Configure data classification and extraction

To configure email data classification and extraction in your Sensible account, take the following steps.

#### Create out-of-the-box document types

Create document types to handle the paystub, drivers license, and signed lease attachments:
1. Follow the steps in [Out-of-the-box extractions](doc:library-quickstart) to add extraction support for the following document types to your account: 
   1. **driver_license** document type
   2. **pay_stubs** document type  
      Each document type contains _configs_, or collections of SenseML extraction queries. Configs handle variations in a document type; for example TODO more definition.

#### (Optional) Create custom document types

The Sensible prebuilt config library doesn't support rental property lease applications. To support it, take the following steps:

   1. In the **Document Types** tab, Click **New document type** and name it `leases`. In the dialog, take the following steps:
      1. Upload the example document from TODO LINK QUERY GROUP.
      2. Name the config `sensibleproperties`  for the fictional property management company in this example. 
      3. After you create the document type, edit the config you created. Paste the example from TODOQUERY GROUP into the empty config and publish it.

1. (Optional) To support extracting from the email body:
   1. Follow the preceding steps to create a document type named`email_body_lease_applications`:
      1. Upload the following example document:

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/email_lease.pdf) |
| ---------------- | ------------------------------------------------------------ |

**Note**: this example is a PDF export of an email body.  When you need to configure extraction support, it's a one-time setup process to convert or print the email body to a supported file type (TODO LINK) so you can test your extraction queries on it.

b. For the configuration, paste in the following code:

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "queries": [
          {
            "id": "applicant_name",
            "description": "What is the name of the applicant?",
            "type": "string"
          },
          {
            "id": "date_sent",
            "description": "What is the date the email was sent?",
            // this type formats the extracted data as a ISO 8601 date
            "type": "date"
          },
          {
            "id": "attachment_count",
            "description": "How many attachments are included in the email?",
            "type": "string"
          }
        ]
      }
    }
  ]
}
```

When you forward an email to Senislbe automatically classifies documents as paystubs, drivers licenses, signed leases, or email bodies of lease applications, and extracts data from them.



## Configure data destination

To recieve extracted email data, you have the following options:

	1. View and download the extracted data in the Sensible app on the **Extraction history** tab.
	1. Implement a webhook as a destination for the extracted data. You'll provide Sensible with its URL in a later step.



## Configure email processor

So far, you've created all the necessary prerequisites for an *email processor* that can handle lease applications. The last step is to contact Sensible to implement the email processor. Provide the following details:

- the name of your Sensible email forwarding address  (TODO: specify it here or say 'see earlier steps')
- the names of the document types you created in your account (TODO: specify it here)
- (optional) the URL of your webhook (TODO: specify it here)

## (Optional) Send a test email

Send a test email to the processor you created. You can download  the example documents for attachments from the following locations:

- GH location
- GH location 



 For the body, you can use the following text:

```
TODO: CHANGE THIS TEXT
Dear Anita Patel,

I hope you’re doing well. I’m writing to formally submit my application for the rental unit at  123 Sample St unit #3. I am very interested in leasing this apartment and have attached all the necessary documents for your review.

Please find attached:

Signed lease agreement
Proof of income (recent pay stub)
Copy of my ID ( driver’s license)
Please let me know if you need any additional information or if there are any next steps in the approval process.

Thank you for your time and consideration. I look forward to your response.


Best regards,
Brenda Sample
(505) 123 4567
brenda.sample@gmail.com

```

You should get back an extraction response for each attachment at the webhook.

You can also view the extractions in the Sensible app's **Extraction history** tab:





TODO: DELETE:

```
---
config:
  layout: dagre
---
flowchart TD
    A["User receives email"] --> B["User fowards email to Sensible"]
    B --> C["Classify attachments"]
    C --> D["Extract data"]
    D --> E["User gets extracted data with webhook"]
    style A fill:#fafaf8,stroke:#000,stroke-width:1px
    style B fill:#fafaf8,stroke:#000,stroke-width:1px
    style C fill:#fafaf8,stroke:#000,stroke-width:1px
    style D fill:#fafaf8,stroke:#000,stroke-width:1px

```





