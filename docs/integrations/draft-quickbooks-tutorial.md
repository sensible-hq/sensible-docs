---
title: QuickBooks integration
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: Integrate with Quickbooks using Python
  description: Extract invoices into QuickBooks Online as bills with Python and Sensible
  robots: index
next:
  description: ''
---
This topic describes sending extracted data from vendor invoices into QuickBooks Online using Sensible and Python.

> **This is a proof-of-concept tutorial.** It is not intended for production use. The OAuth flow, token storage, and credential handling are intentionally simplified for local development. See the inline `PRODUCTION:` comments in `qbo_auth.py` for a summary of what would need to change before deploying this anywhere real.

```mermaid
flowchart LR
    A[Vendor invoice PDF] --> B["Sensible\n(invoices document type)"]
    B --> C["Python script"]
    C --> D["QuickBooks Online bill"]
```

## Use cases

Vendor invoices often arrive as PDFs emailed by suppliers, downloaded from portals, or scanned from paper. Getting them into your accounting system accurately and quickly is a core accounts payable workflow. Here are a few scenarios where automating this with Sensible and QuickBooks Online is valuable:

* **AP automation for bookkeeping services.** You're a SaaS company that handles bookkeeping for small-business clients. Your clients forward vendor invoices to you as PDF documents, and you extract invoice data from the documents automatically and create bills in QBO.

* **Expense management for growing businesses.** You're a mid-size company receiving dozens of vendor invoices per month across multiple departments. Rather than routing paper invoices through an approval chain and then hand-entering them, you extract the data with Sensible and push it directly into QBO as bills ready for review and payment.

* **Financial ops tooling for vertical SaaS.** You're building a platform for a specific industry (for example, construction, healthcare, or logistics) where your customers receive high volumes of vendor invoices with industry-specific line items. You embed Sensible's extraction into your product and sync bills to your customers' QuickBooks Online accounts via the API.

In this tutorial, you'll set up the first scenario: extracting a vendor invoice with Sensible and creating a bill in QuickBooks Online using Python.

The Python script:

1. Extracts a vendor invoice PDF using Sensible's `invoices` document type, and
2. Creates a new bill in QuickBooks Online from the extracted data.

## Add the invoices document type to your Sensible account

The script uses Sensible's `invoices` document type, which is available in the [Sensible configuration library](https://github.com/sensible-hq/sensible-configuration-library). To add it to your account:

1. In the Sensible app, click the **Template library** tab.
2. Search for **invoices** or browse by use case.
3. Click the **invoices** document type, then click **Clone to account**. Sensible adds the document type and its extraction configurations to your **Document types** tab.
4. Test the document type by uploading a sample invoice using the **Extract** tab.

## Set up a destination in QuickBooks Online

Before you can integrate Sensible with QuickBooks Online, you need an expense account in your Chart of Accounts to assign bill line items to, and a vendor to associate with the bill.

**Access a QuickBooks Online sandbox company**

If you're using a free Intuit Developer account for testing:

1. Sign in to [developer.intuit.com](https://developer.intuit.com/) and navigate to your workspace.

2. On the **Apps** tab, click the **+** button to create a new app.

3. Name your app (for example, "Sensible Integration Test"), select **QuickBooks Online and Payments** as the platform, and select **com.intuit.quickbooks.accounting** as the OAuth scope.

4. After creating the app, go to the **Keys & credentials** tab and copy the **Client ID** and **Client Secret**. You'll use these as environment variables in a later step.

5. Click **Open app** to open the app you created.

6. In the upper-right corner, click **My Hub**, then select **Sandboxes** to access a sandbox company that Quickbooks created by default for your account.

7. In the **Sandbox companies** list, click the name of your sandbox company to open it. Sandbox companies come preloaded with sample vendors, accounts, and other data.

The script automatically resolves both the expense account and vendor at runtime:

- **Expense account**: the script checks for common account names (such as "Uncategorized Expense" or "Miscellaneous") in your Chart of Accounts. If none are found, it creates an account called "Invoice Imports - Needs Review".
- **Vendor**: the script searches for a vendor matching the extracted vendor name, and creates one if no match is found.

No manual setup of accounts or vendors is required.

## Integrate with Python

You can use Sensible's Python SDK and the `python-quickbooks` library to extract invoices and create bills in QuickBooks Online in a single script. This approach gives you full control over the data transformation — especially for handling variable numbers of line items — and is suitable for batch processing or server-side automation.

### Get the scripts

Download the scripts from GitHub:

```bash
git clone https://github.com/sensible-hq/sensible-quickbooks-py.git
cd sensible-quickbooks-py
```

### Prerequisites

Install the required libraries:

```bash
pip install sensible-sdk python-quickbooks intuitlib 
```

Set the following environment variables:

| Variable            | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `SENSIBLE_API_KEY`  | Your Sensible API key, available on your [account page](https://app.sensible.so/account/). |
| `QBO_CLIENT_ID`     | Your QuickBooks app's client ID. In the [Intuit Developer Portal](https://developer.intuit.com/), open your app and go to **Keys & credentials**. |
| `QBO_CLIENT_SECRET` | Your QuickBooks app's client secret, on the same **Keys & credentials** tab. |

### One-time setup

Before running the integration for the first time, complete two setup steps.

**Add a redirect URI to your Intuit app**

The authorization script uses a local HTTP server to catch the OAuth callback automatically. To enable this:

1. Go to [developer.intuit.com](https://developer.intuit.com/) and open your app.
2. Go to the **Settings** tab.
3. Under **Redirect URIs**, click **Add URI**, enter `http://localhost:8080/callback`, and click **Save**.

**Authorize the app**

Run the setup script in a regular terminal (not in an AI coding tool) once to authorize and save your tokens:

```bash
python quickbooks-setup.py
```

The script prints an authorization URL. Copy it, open it in your browser, and click **Connect**. Once you authorize, the script saves your tokens automatically. You won't need to repeat this unless the refresh token expires (after 100 days of inactivity).

### Run the integration

Run the integration script in a regular terminal (not in an AI coding tool):

```bash
python invoice_to_quickbooks.py
```

### What the script does

The script runs five steps:

1. Extracts invoice data using Sensible's `invoices` document type from a local PDF (`invoice_sample.pdf`).
2. Authenticates with QuickBooks Online using your saved tokens (auto-refreshes silently).
3. Finds a matching expense account in your Chart of Accounts (checking for common names like "Uncategorized Expense" and "Miscellaneous"), or creates one called "Invoice Imports - Needs Review" if none exist.
4. Finds or creates a vendor matching the extracted vendor name.
5. Creates a bill in QuickBooks with the extracted line items.

### Field mapping

The extraction response from Sensible api includes a `parsed_document` object containing the extracted document data:

TODO: update this to the actual sample_invoice.pdf results (claude probably can't do this for me)

```json
{
    "id": "04d60717-8e11-43d1-8a76-e773954bffb0",
    "created": "2026-03-23T21:00:42.274Z",
    "completed": "2026-03-23T21:01:55.999Z",
    "status": "COMPLETE",
    "type": "invoices",
    "document_name": "invoice_sample",
    "configuration": "llm_invoices_template",
    "configuration_version": "g2miCFA52OW1ABhCtzoEU17oFPFcFzyz",
    "environment": "production",
    "page_count": 1,
    "parsed_document": {
        "Vendor name": {
            "value": "Sample, Inc.",
            "type": "string",
            "confidenceSignal": "confident_answer"
        },
        "Vendor address": {
            "value": "PO Box 11111, Charlotte, NC 28233",
            "type": "string",
            "confidenceSignal": "confident_answer"
        },
        "Customer name": {
            "value": "Sample Group",
            "type": "string",
            "confidenceSignal": "confident_answer"
        },
        // abridged response...
        "line_items": [
            {
                "item_number": {
                    "value": "A075NN8WT2F 019.75MS",
                    "type": "string"
                },
                "item_description": {
                    "value": "VITRA CHARGED FILAMENT",
                    "type": "string"
                },
                "item_boxes": null,
                "item_unit_quantity": {
                    "source": "178,200",
                    "value": 178200,
                    "type": "number"
                },
                "item__uom": {
                    "value": "Feet",
                    "type": "string"
                },
                "item__unit_price": {
                    "value": "0.194",
                    "type": "string"
                },
                "item__box_price": null,
                "item_total": {
                    "value": "34570.80",
                    "type": "string"
                }
            },
            {
                "item_number": {
                    "value": "FREIGHTSURCHARGE",
                    "type": "string"
                },
                "item_description": {
                    "value": "Freight Surcharge on A075NN8WT2F 019.75MS",
                    "type": "string"
                },
                "item_boxes": null,
                "item_unit_quantity": {
                    "source": "178,200",
                    "value": 178200,
                    "type": "number"
                },
                "item__uom": {
                    "value": "Each",
                    "type": "string"
                },
                "item__unit_price": {
                    "value": "0.02224",
                    "type": "string"
                },
                "item__box_price": null,
                "item_total": {
                    "value": "3963.17",
                    "type": "string"
                }
            }
            // abridged resposne
        ]
    },
    "validations": [],
    "validation_summary": {
        "fields": 27,
        "fields_present": 20,
        "errors": 0,
        "warnings": 0,
        "skipped": 0
    },
    "classification_summary": [
        {
            "configuration": "llm_invoices_template",
            "score": {
                "value": 50,
                "fields_present": 50,
                "penalties": 0
            }
        }
    ],
    "errors": [],
    "download_url": ""<redacted>"",
    "content_type": "application/pdf",
    "file_metadata": {
        "info": {
            "creator": "Atalasoft, Inc.",
            "producer": "DotImage PDF Encoder",
            "creation_date": "2022-03-31T12:03:17.000Z",
            "modification_date": "2024-08-20T15:02:03.000-07:00"
        },
        "metadata": {
            "xmp:createdate": "2022-03-31T12:03:17Z",
            "xmp:creatortool": "Atalasoft, Inc.",
            "xmp:modifydate": "2024-08-20T15:02:03-07:00",
            "xmp:metadatadate": "2024-08-20T15:02:03-07:00",
            "pdf:producer": "DotImage PDF Encoder",
            "xmpmm:documentid": "xmp.d",
            "xmpmm:instanceid": "uuid:55c99e98-c153-fd43-b002-569b012c7eab",
            "xmpmm:history": "editedScannedDoc2024-08-20T15:02:03-07:00Page:1",
            "dc:format": "application/pdf"
        }
    },
    "coverage": 0.7246376811594203,
    "charged": 1,
    "version_id": "bV7R07dGkanm.la93_Cb70NuHd1WkWWx"
}
```

The script reads fields from the `parsed_document` object in the Sensible API response and maps them to QuickBooks Online bill fields:

| QuickBooks Online field       | Sensible field                   | Notes                                                                                                                     |
| ----------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Vendor**                    | `Vendor name`                    | The script searches for an existing QBO vendor with a matching `DisplayName`, or creates a new vendor if none is found.   |
| **Transaction Date**          | `Invoice date`                   | The date on the invoice.                                                                                                  |
| **Due Date**                  | `Invoice due date`               | The payment due date, if present on the invoice.                                                                          |
| **Ref No.**                   | `Invoice number`                 | The vendor's invoice number, for cross-referencing.                                                                       |
| **Line 1 - Description**      | `line_items[0].item_description` | The description of the first line item.                                                                                   |
| **Line 1 - Amount**           | `line_items[0].item_total`       | The amount of the first line item.                                                                                        |
| **Line 2 - Description**      | `line_items[1].item_description` | The description of the second line item.                                                                                  |
| **Line 2 - Amount**           | `line_items[1].item_total`       | The amount of the second line item.                                                                                       |
| **Line n - Description**      | `line_items[n].item_description` | The script iterates the full `line_items` array and creates one QBO bill line per entry.                                  |
| **Line n - Amount**           | `line_items[n].item_total`       |                                                                                                                           |
| **Line - Account**            | _(resolved automatically)_       | All lines use the same expense account, resolved as described in [What the script does](#what-the-script-does).           |

### Expected output

Running the script produces output like the following:

```bash
python invoice_to_quickbooks.py

[1/5] Extracting invoice with Sensible ...
  ✓ Vendor: Fictional Horticulture Vendor
  ✓ Invoice #: 39
  ✓ Total: 28.215
  ✓ Line items: 4

[2/5] Authenticating with QuickBooks Online ...
  ✓ Connected.

[3/5] Resolving expense account ...
  ✓ Using existing account: 'Uncategorized Expense' (ID 31)

[4/5] Resolving vendor ...
  ✓ Created new vendor: Fictional Horticulture Vendor (ID 59)

[5/5] Creating bill in QuickBooks ...
  • Line 1: Leather Leaf — $20,475.00
  • Line 2: Leather Leaf — $4,620.00
  • Line 3: Leather Leaf — $1,200.00
  • Line 4: Leather Leaf — $1,920.00

============================================================
  ✓ Bill created successfully!
    ID:     149
    Vendor: Fictional Horticulture Vendor
    Date:   2023-04-02
    Lines:  4
    View:   https://app.sandbox.qbo.intuit.com/app/bill?txnId=149
============================================================
```

Follow the link to view the created bill:

TODO: create screenshot, claude can't help w/ this

![](https://files.readme.io/59e96373d2797785bffff67932fdb3656cfe1f6d9e14bd781fd707196a6c8aed-image.png)

Compare it to the sample invoice to see how the document data was extracted:

![](https://files.readme.io/d867b30fbd2180419370474e9d516552131b1718a11a212adfd012f4ac06c863-image.png)

TODO: create screenshot, claude code can't help

## (Optional) Scale up

This tutorial processes a single local PDF. Here are a few directions for going further.

**Process a batch of invoices**

To extract multiple invoices in one run, loop over a directory of PDFs and call `sensible.extract()` for each file. Add error handling to log failures without stopping the batch.

**Trigger extraction automatically**

Sensible supports automatic extraction via its [email processor](https://docs.sensible.so/docs/getting-started-email): forward invoices to a Sensible-generated address, and Sensible extracts them and POSTs the `parsed_document` to your webhook endpoint. Replace the `sensible.extract()` call in the script with a webhook handler on your server.

**Extract other document types**

The same pattern works for any document type in the [Sensible configuration library](https://docs.sensible.so/docs/library-quickstart) — purchase orders, receipts, expense reports, and more. Swap the `document_type` parameter in the `extract()` call and update the field mapping to match the new document type's fields.

**Production considerations**

Before deploying this integration in production, review the `PRODUCTION:` comments throughout `qbo_auth.py`. Key changes include:

* Storing OAuth tokens in a secrets manager (such as AWS Secrets Manager) rather than a local file
* Replacing the browser-based OAuth flow with a proper web redirect flow
* Switching `environment="sandbox"` to `environment="production"` in both the `AuthClient` and `QuickBooks` constructors
* Adding per-account token storage if your service connects to multiple QuickBooks Online companies

<br />

<br />
