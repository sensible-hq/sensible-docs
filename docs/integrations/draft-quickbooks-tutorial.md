---
title: QuickBooks tutorial
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

TODO: mermaid diagram here?

TODO: make sure there's disclaimer language around this being a POC/tutorial, don't use scripts in production

## Use cases

Vendor invoices often arrive as PDFs emailed by suppliers, downloaded from portals, or scanned from paper. Getting them into your accounting system accurately and quickly is a core accounts payable workflow. Here are a few scenarios where automating this with Sensible and QuickBooks Online is valuable:

* **AP automation for bookkeeping services.** You're a SaaS company that handles bookkeeping for small-business clients. Your clients forward vendor invoices to you as PDF documents, and you extract invoice data from the documents automatically and create bills in QBO.

* **Expense management for growing businesses.** You're a mid-size company receiving dozens of vendor invoices per month across multiple departments. Rather than routing paper invoices through an approval chain and then hand-entering them, you extract the data with Sensible and push it directly into QBO as bills ready for review and payment.

* **Financial ops tooling for vertical SaaS.** You're building a platform for a specific industry (for example, construction, healthcare, or logistics) where your customers receive high volumes of vendor invoices with industry-specific line items. You embed Sensible's extraction into your product and sync bills to your customers' QuickBooks Online accounts via the API.

In this tutorial, you'll set up the first scenario: extracting a vendor invoice with Sensible and creating a bill in QuickBooks Online using Python.

These Python scripts:

1. TODO: figure out how to do that in python trigger (and/or in email type of sitch/filtering?)! triggers every time that Sensible extracts from a document of the `invoices` document type, and
2. creates a new bill in QuickBooks Online from the extracted data.

## Set up a destination in QuickBooks Online

Before you can integrate Sensible with QuickBooks Online, you need an expense account in your Chart of Accounts to assign bill line items to, and a vendor to associate with the bill.

**Access a QuickBooks Online sandbox company**

If you're using a free Intuit Developer account for testing:

1. Sign in to [developer.intuit.com](https://developer.intuit.com/) and navigate to your workspace.

2. On the **Apps** tab, click the **+** button to create a new app.

3. Name your app (for example, "Sensible Integration Test") and verify that **QuickBooks Online** is the platform.
   1. TODO: .auth scope?  com.intuit.quickbooks.accouting and/or .payment?
   2. TODO: copy the credentials? YES! you'll need them for auth later; turn this into a real step

4. Click **Open app** to open the app you created.

5. In the upper-right corner, click **My Hub**, then select **Sandboxes** to access a sandbox company that Quickbooks created by default for your account.

6. In the **Sandbox companies** list, click the name of your sandbox company to _launch it in QuickBooks Online|open it_. Sandbox companies come preloaded with sample vendors, accounts, and other data.

**Verify your Chart of Accounts and vendors**

1. In the sandbox company, navigate to **Accounting > Chart of Accounts** TODO PROPER STYLE? and verify that an expense account (for example,  "Office Supplies" or "Cost of Goods Sold") exists: In the **ACCOUNT TYPE** filter, verify at least one account of type **Expenses** exists. If not, create a test expense account: click **New account** in the upper right corner. In the dialog, select **Expenses** in the **Account type** dropdown, populate the remaining fields with test data, and click **Save**.
2. In the sandbox company, navigate to **Expenses > Vendors** and verify that at least one vendor exists. If not, create a test vendor: click **Create vendor** , complete the dialog with test data, and click **Save**. In production, you'd match extracted vendor names to existing QBO vendors or create new ones automatically.

## Integrate with Python

You can use Sensible's Python SDK and the `python-quickbooks` TODO rename library to extract invoices and create bills in QuickBooks Online in a single script. This approach gives you full control over the data transformation — especially for handling variable numbers of line items — and is suitable for batch processing or server-side automation.

### Get the scripts

Download the scripts from GitHub:

```bash
git clone https://github.com/sensible-hq/sensible-quickbooks-py.git
cd sensible-docs/scripts/sensible-quickbooks-py
```

Or browse the GitHub directory directly: [https://github.com/sensible-hq/sensible-quickbooks-py](https://github.com/sensible-hq/sensible-quickbooks-py). TODO: good as LLM alternative?

### Prerequisites

Install the required libraries:

```bash
pip install sensible-sdk python-quickbooks intuitlib 
```

Set the following environment variables:

| Variable            | Description                                                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `SENSIBLE_API_KEY`  | Your Sensible API key, available on your [account page](https://app.sensible.so/account/).                                        |
| `QBO_CLIENT_ID`     | Your QuickBooks app's client ID, available in the [Intuit Developer Portal](https://developer.intuit.com/). TODO be more specific |
| `QBO_CLIENT_SECRET` | Your QuickBooks app's client secret. TODO same specific advice                                                                    |

### One-time setup

Before running the integration for the first time, complete two setup steps.

**Add a redirect URI to your Intuit app**

The authorization script uses a local HTTP server to catch the OAuth callback automatically. To enable this:

1. Go to [developer.intuit.com](https://developer.intuit.com/) and open your app.
2. Go to the **Settings** tab.
3. Under **Redirect URIs**, click **Add URI**, enter `http://localhost:8080/callback`, and click **Save**.

**Authorize the app**

Run the setup script once to authorize and save your tokens:

```bash
python quickbooks-setup.py
```

The script prints an authorization URL. Copy it, open it in your browser, and click **Connect**. Once you authorize, the script saves your tokens automatically. You won't need to repeat this unless the refresh token expires (after 100 days of inactivity).

### Run the integration

TODO: rename script

TODO: update with `! python` alternative for running interactively in claude code

```bash
python import_sensible_to_quickbooks.py
```

### What the script does

The script runs six steps: TODO update script has changed

1. Downloads a sample invoice PDF from the Sensible configuration library (skipped if already present)
2. Extracts invoice data using Sensible's `invoices` document type
3. Authenticates with QuickBooks Online using your saved tokens (auto-refreshes silently)
4. Finds an appropriate expense account (TODO: attempts to match, right?) in your Chart of Accounts, or creates one called "Invoice Imports - Needs Review" if none of the expected accounts exist
5. Finds or creates a vendor matching the extracted vendor name
6. Creates a bill in QuickBooks with the extracted line items

### Field mapping

The extraction response from Sensible api includes a `parsed_document` object containing the extracted document data:

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

TODO: add intro here about mapping that API response to the Quickbook entities.

AND: table is inaccruate, udpate

| QuickBooks Online field  | Sensible field             | Description                                                                                                                |
| ------------------------ | -------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Vendor**               | `vendor_name`              | The vendor who issued the invoice. Select a matching vendor from QBO, or use Zapier's lookup feature to match dynamically. |
| **Transaction Date**     | `invoice_date`             | The date on the invoice.                                                                                                   |
| **Due Date**             | `due_date`                 | The payment due date.                                                                                                      |
| **Ref No.**              | `invoice_number`           | The vendor's invoice number, for cross-referencing.                                                                        |
| **Line 1 - Description** | `line_items.0.description` | The description of the first line item.                                                                                    |
| **Line 1 - Amount**      | `line_items.0.amount`      | The amount for the first line item.                                                                                        |
| **Line 1 - Account**     | _(select from QBO)_        | The expense account to categorize this line item under (for example, "Office Supplies").                                   |

### Expected output

Running the script produces output like the following:

```
python invoice_to_quickbooks.py

[1/5] Extracting invoice with Sensible ...
  ✓ Vendor: (not found)
  ✓ Invoice #: 39
  ✓ Total: 28.215
  ✓ Line items: 4
  ⚠ Vendor name not found. Using default: Unmatched - Review Required

[2/5] Authenticating with QuickBooks Online ...
  ✓ Connected.

[3/5] Resolving expense account ...
  ✓ Using existing account: 'Uncategorized Expense' (ID 31)

[4/5] Resolving vendor ...
  ✓ Found existing vendor: Unmatched - Review Required (ID 58)

[5/5] Creating bill in QuickBooks ...
  • Line 1: Leather Leaf — $20,475.00
  • Line 2: Leather Leaf — $4,620.00
  • Line 3: Leather Leaf — $1,200.00
  • Line 4: Leather Leaf — $1,920.00

============================================================
  ✓ Bill created successfully!
    ID:     147
    Vendor: Unmatched - Review Required
    Date:   2023-04-02
    Lines:  4
    View:   https://app.sandbox.qbo.intuit.com/app/bill?txnId=147
```

Follow the link to view the created bill:

TODO: create screenshot,

![](https://files.readme.io/59e96373d2797785bffff67932fdb3656cfe1f6d9e14bd781fd707196a6c8aed-image.png)

Compare it to the sample invoice to see how the document data was extracted:

![](https://files.readme.io/d867b30fbd2180419370474e9d516552131b1718a11a212adfd012f4ac06c863-image.png)

<br />

## (Optional) Test your integration

1. TODO

## (Optional) Scale up

TODO... talk about extracting multiple files? webhooks? etc?

talk about production considerations?

* oauth
* For production use, consider adding logic to match extracted vendor names to existing QBO vendors to avoid creating duplicates. The Python script above includes basic vendor matching.

# Notes

<br />
