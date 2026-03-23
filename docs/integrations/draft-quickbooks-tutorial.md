---
title: QuickBooks tutorial
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: 'Extract invoices into QuickBooks Online as bills with Python and Sensible'
  robots: index
next:
  description: ''
---

This topic describes sending extracted data from vendor invoices into QuickBooks Online using Sensible's Zapier integration.

## Use cases

Vendor invoices often arrive as PDFs emailed by suppliers, downloaded from portals, or scanned from paper. Getting them into your accounting system accurately and quickly is a core accounts payable workflow. Here are a few scenarios where automating this with Sensible and QuickBooks Online is valuable:

- **AP automation for bookkeeping services.** You're a SaaS company that handles bookkeeping for small-business clients. Your clients forward vendor invoices to you as PDF documents, and you extract invoice data from the documents automatically and create bills in QBO.

- **Expense management for growing businesses.** You're a mid-size company receiving dozens of vendor invoices per month across multiple departments. Rather than routing paper invoices through an approval chain and then hand-entering them, you extract the data with Sensible and push it directly into QBO as bills ready for review and payment.

- **Financial ops tooling for vertical SaaS.** You're building a platform for a specific industry (for example, construction, healthcare, or logistics) where your customers receive high volumes of vendor invoices with industry-specific line items. You embed Sensible's extraction into your product and sync bills to your customers' QuickBooks Online accounts via the API.

In this tutorial, you'll set up the first scenario: extracting a vendor invoice with Sensible and creating a bill in QuickBooks Online using Zapier.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickbooks_0.png)

This Zap:

1. triggers every time that Sensible extracts from a document of the `invoices` document type, and
2. creates a new bill in QuickBooks Online from the extracted data.

## Create an example Sensible extraction

To configure Zapier, you'll use a recent example of a document extraction:

1. Follow the steps in [Getting started with out-of-the-box extractions](https://docs.sensible.so/docs/library-quickstart) to create support for the `invoices` document type.

2. Download an [example invoice](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Invoices/refdocs) from the Sensible library.

3. In the Sensible app, click the **Extract** tab. Upload the example document, select the `invoices` document type, and run an extraction.

## Set up a destination in QuickBooks Online

Before you can integrate Sensible with QuickBooks Online, you need an expense account in your Chart of Accounts to assign bill line items to, and a vendor to associate with the bill.

**Access a QuickBooks Online sandbox company**

If you're using a free Intuit Developer account for testing:

1. Sign in to [developer.intuit.com](https://developer.intuit.com/) and navigate to your workspace.
2. On the **Apps** tab, click the **+** button to create a new app.
3. Name your app (for example, "Sensible Integration Test") and verify that **QuickBooks Online** is the platform. 
   1. TODO: .auth scope?  com.intuit.quickbooks.accouting and/or .payment?
   2. copy the credentials?

4. Click **Open app** to open the app you created.
5. In the upper-right corner, click **My Hub**, then select **Sandboxes** to access a sandbox company that Quickbooks created by default for your account.
6. In the **Sandbox companies** list, click the name of your sandbox company to *launch it in QuickBooks Online|open it*. Sandbox companies come preloaded with sample vendors, accounts, and other data.

**Verify your Chart of Accounts and vendors**

1. In the sandbox company, navigate to **Accounting > Chart of Accounts** TODO PROPER STYLE? and verify that an expense account (for example,  "Office Supplies" or "Cost of Goods Sold") exists: In the **ACCOUNT TYPE** filter, verify at least one account of type **Expenses** exists. If not, create a test expense account: click **New account** in the upper right corner. In the dialog, select **Expenses** in the **Account type** dropdown, populate the remaining fields with test data, and click **Save**. 
3. In the sandbox company, navigate to **Expenses > Vendors** and verify that at least one vendor exists. If not, create a test vendor: click **Create vendor** , complete the dialog with test data, and click **Save**. In production, you'd match extracted vendor names to existing QBO vendors or create new ones automatically.

## Integrate with Python

You can use Sensible's Python SDK and the `python-quickbooks` library to extract invoices and create bills in QuickBooks Online in a single script. This approach gives you full control over the data transformation — especially for handling variable numbers of line items — and is suitable for batch processing or server-side automation.

### Prerequisites

Install the required libraries:

```bash
pip install sensibleapi python-quickbooks intuit-oauth
```

Set the following environment variables:

| Variable | Description |
| --- | --- |
| `SENSIBLE_API_KEY` | Your Sensible API key, available on your [account page](https://app.sensible.so/account/). |
| `QBO_CLIENT_ID` | Your QuickBooks app's client ID, available in the [Intuit Developer Portal](https://developer.intuit.com/). |
| `QBO_CLIENT_SECRET` | Your QuickBooks app's client secret. |
| `QBO_REFRESH_TOKEN` | A valid OAuth 2.0 refresh token for your QuickBooks Online company. |
| `QBO_REALM_ID` | Your QuickBooks Online company ID (also called Realm ID). |
| `QBO_EXPENSE_ACCOUNT_ID` | The default QuickBooks expense account ID for bill line items. Find it under **Accounting > Chart of Accounts**. |

**Note:** To obtain a refresh token, complete the OAuth 2.0 authorization flow once using the Intuit Developer Portal's OAuth Playground or your app's auth endpoint. The script uses the refresh token to generate access tokens automatically on each run.



TODO: add intro here

| QuickBooks Online field  | Sensible field             | Description                                                  |
| ------------------------ | -------------------------- | ------------------------------------------------------------ |
| **Vendor**               | `vendor_name`              | The vendor who issued the invoice. Select a matching vendor from QBO, or use Zapier's lookup feature to match dynamically. |
| **Transaction Date**     | `invoice_date`             | The date on the invoice.                                     |
| **Due Date**             | `due_date`                 | The payment due date.                                        |
| **Ref No.**              | `invoice_number`           | The vendor's invoice number, for cross-referencing.          |
| **Line 1 - Description** | `line_items.0.description` | The description of the first line item.                      |
| **Line 1 - Amount**      | `line_items.0.amount`      | The amount for the first line item.                          |
| **Line 1 - Account**     | *(select from QBO)*        | The expense account to categorize this line item under (for example, "Office Supplies"). |



### Script

```python
import os
from sensibleapi import SensibleSDK
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.bill import Bill, BillLine, AccountBasedExpenseLineDetail
from quickbooks.objects.vendor import Vendor
from quickbooks.objects.base import Ref

# ── Sensible extraction ────────────────────────────────────────────────────────

sensible = SensibleSDK(os.environ["SENSIBLE_API_KEY"])

request = sensible.extract(
    path="./vendor_invoice.pdf",   # replace with your file path
    document_type="invoices",
    environment="production",
)
result = sensible.wait_for(request)

parsed = result["parsed_document"]

# Extract the fields we need using the actual Sensible field IDs.
# Field IDs contain spaces and mixed casing — use the exact IDs from your config.
invoice_date   = (parsed.get("Invoice date")            or {}).get("value")
due_date       = (parsed.get("Invoice due date")        or {}).get("value")
invoice_number = (parsed.get("Invoice number")          or {}).get("value")
vendor_name    = (parsed.get("Vendor name")             or {}).get("value")
total_amount   = (parsed.get("Total amount of invoice") or {}).get("value")
line_items     = parsed.get("line_items", [])

# Vendor name may be null for some invoices. Fall back to a placeholder
# so the bill is still created and can be reassigned during review.
DEFAULT_VENDOR = "Unmatched - Review Required"
if not vendor_name:
    print(f"Warning: Vendor name not found in extraction. Using default: {DEFAULT_VENDOR}")
    vendor_name = DEFAULT_VENDOR

# ── QuickBooks Online auth ─────────────────────────────────────────────────────

auth_client = AuthClient(
    client_id=os.environ["QBO_CLIENT_ID"],
    client_secret=os.environ["QBO_CLIENT_SECRET"],
    redirect_uri="https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl",
    environment="production",
)
auth_client.refresh(refresh_token=os.environ["QBO_REFRESH_TOKEN"])

qb_client = QuickBooks(
    auth_client=auth_client,
    refresh_token=os.environ["QBO_REFRESH_TOKEN"],
    company_id=os.environ["QBO_REALM_ID"],
)

# ── Find or create vendor ──────────────────────────────────────────────────────

vendors = Vendor.filter(DisplayName=vendor_name, qb=qb_client)
if vendors:
    vendor_ref = Ref()
    vendor_ref.value = vendors[0].Id
    vendor_ref.name = vendors[0].DisplayName
else:
    new_vendor = Vendor()
    new_vendor.DisplayName = vendor_name
    new_vendor.save(qb=qb_client)
    vendor_ref = Ref()
    vendor_ref.value = new_vendor.Id
    vendor_ref.name = new_vendor.DisplayName

# ── Build bill ─────────────────────────────────────────────────────────────────

bill = Bill()
bill.TxnDate = str(invoice_date) if invoice_date else None
bill.DueDate = str(due_date) if due_date else None
bill.DocNumber = str(invoice_number) if invoice_number else None
bill.VendorRef = vendor_ref

expense_account_ref = Ref()
expense_account_ref.value = os.environ["QBO_EXPENSE_ACCOUNT_ID"]

# Line items are always variable-length. Loop through all extracted items.
# The extraction uses field IDs like "item_description", "item_total", etc.
if not line_items:
    # If no line items were extracted, fall back to a single line using the total.
    line = BillLine()
    line.Amount = abs(float(total_amount)) if total_amount else 0
    line.Description = "Invoice total (line items not extracted)"
    line.DetailType = "AccountBasedExpenseLineDetail"
    detail = AccountBasedExpenseLineDetail()
    detail.AccountRef = expense_account_ref
    line.AccountBasedExpenseLineDetail = detail
    bill.Line.append(line)
else:
    for item in line_items:
        detail = AccountBasedExpenseLineDetail()
        detail.AccountRef = expense_account_ref

        # item_total is extracted as a string (e.g. "20475").
        # Clean commas and parse to float.
        raw_total = (item.get("item_total") or {}).get("value", "0")
        amount = float(str(raw_total).replace(",", ""))

        description = (item.get("item_description") or {}).get("value", "")

        line = BillLine()
        line.Amount = abs(amount)
        line.Description = description
        line.DetailType = "AccountBasedExpenseLineDetail"
        line.AccountBasedExpenseLineDetail = detail
        bill.Line.append(line)

saved = bill.save(qb=qb_client)
print(f"Bill created: ID {saved.Id}, vendor {vendor_name}, date {saved.TxnDate}")
```

## (Optional) Test your integration

1. TODO

## (Optional) Scale up

You can extract from more invoices automatically by building a more complex Zap so that you can trigger Sensible extractions with file actions in Google Drive, email, or other Zapier-supported apps. Then send the extraction to QuickBooks Online or another destination with a Sensible action. For more information, see [Advanced Zapier tutorial](https://docs.sensible.so/docs/zapier-tutorial-2).

**Note:** Sensible offers native support for automatically extracting from email attachments. Since vendor invoices commonly arrive as email attachments, this is a natural fit. Instead of using Zapier for emails, see [Getting started with email extractions](https://docs.sensible.so/docs/getting-started-email).

# Notes

**QuickBooks Online limitations**

* For production use, consider adding logic to match extracted vendor names to existing QBO vendors to avoid creating duplicates. The Python script above includes basic vendor matching.