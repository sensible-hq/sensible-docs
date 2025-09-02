---
title: "Email rough draft"
hidden: true
---



# See readme dash v5





*You can extract data from email bodies and attachments by emailing them to Sensible.*

*The following image shows an overview for the email extraction workflow:*



```
graph TD;
    A[User receives email] --> B[User sends email to Sensible]
    B --> C[Email is classified into an email type]
    C -->|If there are attachments| D[Documents classified and extracted]
    C --> E[Email is extracted]
    D --> F[Extracted data is sent and appears in the extractions history]
    E --> F
```







*![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email.png)*

*How to set up email integration: TODO: probably easier with a fictional example and screenshots in Gmail. TODO: should the fictional example include a couple attachments of different doc types?*

1. *Create a document type (link to instructions) for the emails you want to extract from.*
2. *In the document type, create a dedicated email address for receiving the emails to extract from, i.e.,  `UUID@forwarding.sensible.so`.*
3. *Use filtering rules in your email provider to filter the emails you want to extract from that match the document type you created.    For example, filter emails from a certain domain or those containing specific keywords or specific attachment types.*
4. *Set up automatic forwarding with your email service provider to send your filtered emails to Sensible.*

## *Configuring attachment extractions*

*Not all attachments in an email will need to be extracted. To prevent triggering an extraction on irrelevant documents, we should allow users to configure the criteria for documents that need to be extracted. These filters should include:*

- *Classification score slider (ex. if the highest score returned is <x, don’t extract the document)*
- *File name (ex. only extract files that contain “1040” in the title)*
- *File types (ex. only extract PDFs)*



## *Notes*

- *TODO:  "We need to be transparent and clear with the security implications of the data they’re forwarding and how it’s protected" <-- how much of this is on the docs, how much on the UI, how much on just linking to AWS infra docs??*
- *For email size limitations, see [Supported file formats] TODO --> link + include the info there*



## from dash

`https://www.notion.so/sensiblehq/Support-for-extracting-emails-e62a33d18726446dadd2d46ad1d07b9a`

TODO:

- how to cross link btwn this and an EMAIL INTEGRATION topic; what's the distinction here? I think the GSG topic need to emphasize webhook implementation; maybe also practical concerns like filtering in your host email, and the integrations topic focuses a little more on how it works...??

<br />

POTENTIAL DIAGRAM:

1. user enables forwarding to a Sensible email processor alias
2. User configures email forwarding filters from their email client/platform
3. Filtered email is forward to the alias
4. Email extracted based on auto-selected configuration in each _document type_

## Introduction

You can extract structured data from email bodies and attachments by emailing them to Sensible. Define document types (TODO link) to handle the extractions. 

The following image shows an overview for the email extraction workflow: 

```
 graph TD;
    style A fill:#fafaf8,stroke:#000,stroke-width:1px;
    style B fill:#fafaf8,stroke:#000,stroke-width:1px;
    style C fill:#fafaf8,stroke:#000,stroke-width:1px;
    style D fill:#fafaf8,stroke:#000,stroke-width:1px;

    
    A[User receives email] --> B[ User fowards email to Sensible]
    B --> C[Classification and extraction from documents and attachments ]
    C --> D[User gets extracted data with webhook ]
```

![](https://files.readme.io/e13afe72089d634b0f2b304cc9923134c870ed8ce579dc1b2d8ff7ce0fd4ffa6-image.png)

In this tutorial, you'll learn to extract data from a set of similar emails. For this tutorial, we'll use  lease application emails like the following, and you'll learn to extract stuff like:

- TBD LIST DATA POINTS like address, rent price, paystub income, dirvers license..

![](https://files.readme.io/c1a738873e5c5c023ef4f4e8230b9b6172aa88dc8cc2f617a6bfafbbbc705723-image.png)

<br />

## Setup

<br />

Say you want to parse lease application emails that typically include the following attachments:

- paystub
- drivers license
- signed lease

There are two big setup steps:

1. Configure Sensible to handle the lease application extractions
2. Configure your email client to filter and forward the lease applciations to Sensible.

Let's take a look:

## Configure Sensible app to extract from lease emails

To create extraction support in your Sensible account for the attachments in typical lease emails, such as driver licenses, take the following steps:

1. Create document types to handle the attachments:
   1. Follow the steps in [Out-of-the-box extractions](doc:library-quickstart) to add extraction support for the following document types to your account: 
      1. **driver_license** document type
      2. **pay_stubs** document type  
         Each document type contains _configs_, or collections of SenseML extraction queries. Configs handle variations in a document type; for example TODO more definition.
   2. (Optional) The Sensible prebuilt config library doesn't support rental property lease applications. To support it, take the following steps:
      1. In the Document Types tab, Click New document type named `leases` to create a new document type:
         1. Upload the example document from TODO LINK QUERY GROUP.
         2. Name the config `sensibleproperties`  for the fictional property management company in this example. 
         3. After you create the document type, edit the config you created. Paste the example from TODOQUERY GROUP into the empty config and publish it.
2. (Optional) To support extracting from the email body:
   1. Follow the preceding steps to create a document type named `email_body_leases`:
      1. Upload the following example document:

<br />

| Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/email_lease.pdf) |
| ---------------- | ------------------------------------------------------------ |

Note: this example is a PDF print-out of an email body.  When you need to configure extraction support, it's a one-time setup process to convert or print out the email body to a supported file type (TODO LINK) so you can test your extraction queries on it.

b. For the configuration, paste in the following code:

```json
{
  "fields": [
    {
      "method": {
        "id": "queryGroup",
        "searchBySummarization": "page",
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

## Configure Sensible email alias and webhook

To create a Sensible email alias that will automatically initiate extracting from these attachments every time you forward a lease application email to it, take the following steps:

<br />

1. Create an email processor.
   1. Click Email processors in the left pane of the Sensible app.
   2. Click **New email processor**.
      1. give it a name, for example, `lease_applications_sensibleproperties`.
      2. For the  **body document type**, select the `email_body_leases` document type you optionally created a previous step.
      3. For teh **attachments document types**, select the following types:
         1. `leases`
         2. `drivers_license`
         3. `pay_stubs`
      4. Create an email alias. For example, TBD
      5. Create a webhook that you implement. For example, TBD. (TODO: run thr
      6. Click **Create**.

## Send a test email

Send a test email to the processor you created. You can download  the example documents for attachments from the following locations:

- GH location
- GH location 

<br />

 For the body, you can use the following text:

```
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

<br />

You should get back an extraction response for each attachment at the webhook.

You can also view the extractions in the Sensible app's **Extraction history** tab.

![](https://files.readme.io/454d9a658fa78a8a7879606279f043ba4e75d330f76fddf3f4900e5c691d5e3c-image.png)

Click each extraction to view its individual results. For example, the paystub extraction extracted the `employer_name: Delta Airlines` and `employee_name: Brenda Sample` fields:

![](https://files.readme.io/ac3b4ce5588d073d5a0bcfa99d95d1c06a741abaf7515bdb236f6e16bc07ac22-image.png)

<br />

<br />

## Old:

1. 1. Define a document type for the email body, and define a document type for  each of the possible attachments. TODO LINK TO DOCUMENT TYPE DEFINITION (maybe in doctype settings??)   TODO give a real world example quickly here.
   2. In each document type, configure the extraction using SenseML query configs.  
      1. , then upload it to the document type. From there, write your SenseML query configs.
2. <br />
3. Test the processor

<br />

<br />

<br />

1. (Your email client) Decide what emails you want to extract from and how you want to filter and forward them. 
2. (sensible app) Configure the email data extraction. You'll need to define a document type for the body and for each of the possible attachments types. For example, TODO
3. (sensible app) Create an email processor that lists the document types and defines an @sensible email and that points to a webhook you will implement. When you send emails to this address, Sensible extracts data from the email and its attachments using the document types you configured. For example, TODO.

<br />

### Set up your email alias

<br />

<br />

<br />

<br />

### Filter and forward your email set

<br />

In Gmail, your filtering and forwarding rules might look something like the following:

![](https://files.readme.io/147ab62e3d24847d225b85d96985e837986cf0b70d8b534cc240269c4e7aa9ef-image.png)

And forward:

![](https://files.readme.io/6ef10ad24c1343c115054c3ec378efda01ebb8454b30f294289afd28790725ca-image.png)

<br />

<br />

<br />

<br />

<br />

<br />

## Extraction

Use the webhook to get notified when Sensible finishes an extraction. You can also view the extraction in the Sensible app. TODO screenshot?

<br />

<br />

How it works is as follows:

EMAIL SAMPLE in my gmail: **Application for Rental Lease**

![](https://files.readme.io/811e14dda7991171f41f4feea42e68975eb8086e7c25366519168e80af2e77bd-image.png)

<br />

<br />

The way this flow looks like visually is as follows:

<br />

TODO: I'll want a diagram here I believe! maybe one w/ a real-world use case example email type?
