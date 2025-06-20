---
"title": "Getting started with email extraction"
"hidden": true
---

## Introduction

You can automatically extract structured data from email bodies and attachments by forwarding them to Sensible.

The following image shows an overview of  email extraction:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email_overview.png)

## Implementation overview

To implement this workflow, take the following general steps:

- **Determine email filters**

  1. Determine a set of similar emails from which you want to extract data. For example, you're in PropTech and you want to extract data from residential lease applications.


  1. Determine email filtering criteria for the set of emails. In a succeeding step, you'll use the filters to automatically forward these emails to a Sensible address.


- **Configure data extraction**
  1. In the Sensible app, define a [document type](doc:document-type-settings) for each email attachment in the lease application emails from which you want to extract data. You can optionally define a document type for the email body. For example, `driverse_licenses`, `paystubs`, `leases`, and `email_body_lease_applications`.


- **(Optional) Configure data destination**
  1. By default, view the extracted data in the Sensible app. Optionally you can also define a webhook to receive the extracted data.

- **Create email processor**
  1. When you've completed the preceding steps, contact Sensible to create an *email processor*. An email processor contains the specified document types, webhook URLs, and forwarding email aliases. You can now start forwarding lease application emails to the processor and receive extracted data.

**Email processor overview**

When an email processor receives an email, it takes the following steps:

1.  Extracts data from the email body using the document type you specify, for example, `lease_application_email_bodies`.
2.  For each attachment, [classifies](doc:classify) it as one of the document types you specify, for example, `paystubs` or `drivers_licenses`, then extracts data from the attachment.


![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email_processor.png)


The following sections provide an implementation example.

## Getting started

Let's walk through an example email data extraction. In this example, you're in PropTech and you want to extract data from lease applications addressed to the property manager "Sensible Property".  Lease application emails to this property manager typically include the following attachments:

- paystub
- drivers license
- signed lease

The following image shows an example email:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email_sample.png)

Let's walk through extracting data from these emails.

## Determine email filters

1. Determine your filtering criteria for forwarding Sensible Property lease applications. For example, you filter by emails addressed to `applications@sensibleproperty.com`.

## Configure data classification and extraction

To configure email data classification and extraction in your Sensible account, take the following steps.

#### Create out-of-the-box document types

Create document types to [classify](doc:classify) and extract from the paystub, drivers license, and signed lease attachments:
1. Follow the steps in [Out-of-the-box extractions](doc:library-quickstart) to add extraction support for the following document types to your account:
   1. **driver_license** document type
   2. **pay_stubs** document type

Each document type contains [_configs_](doc:config-settings), or collections of [SenseML](doc:senseml-reference-introduction) extraction queries. Configs handle variations in a document type. For example, each config in the `pay_stubs` document type handles a different paystub software vendor, such as Gusto, ADP, or Paylocity.

#### (Optional) Create custom document types

Sensible doesn't provide out-of-the-box extraction support for lease applications. To create support in your account, take the following steps:

   1. Create a document type for **leases**. In the **Document Types** tab, Click **New document type**. In the dialog, take the following steps:
      1. Name the document type `leases`.
      2. Upload the following example document:

       | Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/email_lease.pdf) |
         | ---------------- | ------------------------------------------------------------ |

      3. Name the config `sensibleproperties`  for the fictional property management company in this example.
      4. After you create the document type, edit the config you created. Paste the following code into the left pane:

         ```json
         {
           "fields": [
             {
               "method": {
                 "id": "queryGroup",
                 "queries": [
                   {
                     "id": "tenancy_terms_start",
                     "description": "tenancy terms start date",
                     "type": "date"
                   },
                   {
                     "id": "tenancy_terms_end",
                     "description": "tenancy terms end date",
                     "type": "date"
                   },
                   {
                     "id": "monthly_rents_dollars",
                     "description": "monthly rents in dollars",
                     "type": "currency"
                   }
                 ]
               }
             }
           ]
         }
         ```

1. (Optional) Create a document type for **lease application email bodies**:
   1. Follow the preceding steps to create a document type named `email_body_lease_applications` with a config named `sensibleproperties`. Upload the following example document:
   | Example document | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/email_body_lease.pdf) |
   | ---------------- | ------------------------------------------------------------ |
   **Note**: This example document is a PDF exported from an email body for testing. In production, Sensible automatically converts email bodies to PDFs.

   2. In the config, paste the following code:

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

## (Optional) Configure data destination

To receive extracted email data, you have the following options:

- By default, view and download the extracted data in the Sensible app on the **Extraction history** tab:

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email_history_ui.png)

- Implement a webhook as a destination for the extracted data. You'll provide Sensible with its URL in a succeeding step.

## Specify email processor

In the preceding steps, you configured the necessary prerequisites for an *email processor* that can handle lease applications. Contact Sensible to implement the email processor. Provide the following details:

- the names of the document types you created in your account (`driver_license`, `pay_stubs`, `leases`, and `email_body_lease_applications`.)
- (optional) the URL of the webhook you implemented.

After implementing the email processor, Sensible provides you with the  email alias for the processor, for example, `87237966-5965-4019-97f2-66436947ccbb@app.sensible.so`. Forward your lease application emails to this address.

## (Optional) Send a test email

Send a test email with attachments to the processor you created. You can download example documents from the following locations:

| document        | link                                                         |
| --------------- | ------------------------------------------------------------ |
| Drivers license | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/email_drivers_license_sample.pdf) |
| Pay stub        | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/email_gusto_sample.pdf) |
| Lease           | [Download link](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/pdfs/email_lease.pdf) |

 For the body, use the following text:


> Dear Anita Patel,
>
> I hope you’re doing well. I’m writing to formally submit my application for the rental unit at 123 Sample St unit #3. I am very interested in leasing this apartment and have attached all the necessary documents for your review.
>
> Please find attached:
>
> - Signed lease agreement
> - Proof of income (recent pay stub)
> - Copy of my ID (driver’s license)
>
> Please let me know if you need any additional information or if there are any next steps in the approval process.
>
> Thank you for your time and consideration. I look forward to your response.
>
> Best regards,
> Brenda Sample
> (505) 123 4567
> brenda.sample@gmail.com




You should get back an extraction response for each attachment at the webhook you specified.

In the Sensible app, click each extraction to view its data. For example, the paystub extraction includes the extracted fields `employer_name: Delta Airlines` and `employee_name: Brenda Sample`:



![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/main/readme-sync/assets/v0/images/final/email_details_ui.png)
