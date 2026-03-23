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
   2. TODO: copy the credentials? YES! you'll need them for auth later; turn this into a real step

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
| `QBO_REFRESH_TOKEN` | A valid OAuth 2.0 refresh token for your QuickBooks Online company. To obtain this, see following steps. |
| `QBO_REALM_ID` | Your QuickBooks Online company ID (also called Realm ID). To obtain this, see following steps. TODO: is this really necessary |

### One-time oauth2 authorization

To obtain a refresh token and realm ID, complete the OAuth 2.0 authorization flow once:

1. In the Intuit Developer Portal's [OAuth Playground](https://developer.intuit.com/app/developer/playground), select your workspace and app in the dropdowns.

1. Select the `com.intuit.quickbooks.accounting` scope.

1. Click **Get authorization code** and follow the prompts. After you authorize, the playground receives the authorization code automatically via its own redirect URL. TODO: are steps 3 and 4 correct?

1. Click **Get tokens**. The playground displays the authorization code  and realm ID.

1. Exchange the authorization code for access and refresh tokens by running the following python script:

1. 

1. TODO: add steps about saving this to about installing dependencies, saving the script to file, running it in a command line

   ```python
   """
   qbo_get_tokens.py
   
   Exchange a QuickBooks Online authorization code for access and refresh tokens.
   This is a one-time setup utility. Run it once to get a refresh token, then use
   that refresh token in the main integration script.
   
   Prerequisites:
     - A QuickBooks app created at https://developer.intuit.com
     - The redirect URI https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl
       registered in your app's Keys & OAuth settings
     - pip install requests
   
   Environment variables:
     QBO_CLIENT_ID      Your app's client ID (from Keys & OAuth in the Intuit Developer Portal)
     QBO_CLIENT_SECRET   Your app's client secret
   
   Usage:
     1. Go to https://developer.intuit.com/app/developer/playground
     2. Select your app, choose scopes (at minimum com.intuit.quickbooks.accounting),
        and connect to your QuickBooks company or sandbox
     3. Copy the authorization code
     4. Run immediately (codes expire within minutes):
   
        python qbo_get_tokens.py <authorization_code>
   
     5. Copy the refresh_token from the response and set it as your
        QBO_REFRESH_TOKEN environment variable for the main integration script
   
   Notes:
     - Authorization codes expire within a few minutes. Get a fresh one right
       before running this script.
     - Refresh tokens are valid for ~101 days (x_refresh_token_expires_in).
     - Each time you use a refresh token, the response includes a new one
       that replaces the old one.
   """
   
   import base64
   import os
   import sys
   import requests
   
   if len(sys.argv) != 2:
       print("Usage: python qbo_get_tokens.py <authorization_code>")
       sys.exit(1)
   
   client_id = os.environ["QBO_CLIENT_ID"]
   client_secret = os.environ["QBO_CLIENT_SECRET"]
   auth_code = sys.argv[1]
   redirect_uri = "https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl"
   
   credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
   
   resp = requests.post(
       "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
       headers={
           "Content-Type": "application/x-www-form-urlencoded",
           "Accept": "application/json",
           "Authorization": f"Basic {credentials}",
       },
       data={
           "grant_type": "authorization_code",
           "code": auth_code,
           "redirect_uri": redirect_uri,
       },
   )
   
   print(f"Status: {resp.status_code}")
   print(resp.json())
   ```

   Replace `<client_id>`, `<client_secret>`, and `<authorization_code>` with your Quickbook Online values.

   You should see a response like the following:

   ```json
   {'x_refresh_token_expires_in': 8726400, 'refresh_token': '<REDACTED>', 'access_token': '<REDACTED', 'token_type': 'bearer', 'expires_in': 3600}
   ```

   

   6. Copy the `refresh_token` from the JSON response and set it as your `QBO_REFRESH_TOKEN` environment variable.

   Refresh tokens are valid for 100 days. The following script uses the refresh token to generate short-lived access tokens automatically on each run. For production use, store the refresh token securely and handle token rotation — each refresh call returns a new refresh token that replaces the previous one.

   ### Script

   TODO: explain this table and update as necessary given the actual JSON payload.

   The `parsed_document` object you're expecting from Sensible's extraction API looks something like this (TODO REWORD)

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

   

   ### 

TODO: add steps about saving this to a file, running it in a command line, and the sort of output to expect AND a description of what the script does (downloads an example file, etc) NOTE TO SELF: save this file in docs assets so it never breaks







```python
import os
import urllib.request
from pathlib import Path

from sensibleapi import SensibleSDK
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.account import Account
from quickbooks.objects.bill import Bill, BillLine, AccountBasedExpenseLineDetail
from quickbooks.objects.vendor import Vendor
from quickbooks.objects.base import Ref

# ── Download sample invoice ────────────────────────────────────────────────────

SAMPLE_PDF_URL = (
    "https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library"
    "/main/templates/Utilities%20%26%20Invoices/Invoices/refdocs/llm_invoices_template.pdf"
)

script_dir = Path(__file__).resolve().parent
invoice_path = script_dir / "llm_invoices_template.pdf"

if not invoice_path.exists():
    print(f"Downloading sample invoice to {invoice_path} ...")
    urllib.request.urlretrieve(SAMPLE_PDF_URL, invoice_path)
    print("Download complete.")
else:
    print(f"Sample invoice already exists at {invoice_path}, skipping download.")

# ── Sensible extraction ────────────────────────────────────────────────────────

sensible = SensibleSDK(os.environ["SENSIBLE_API_KEY"])

request = sensible.extract(
    path=str(invoice_path),
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

# ── Find or create a default expense account ──────────────────────────────────

# Ordered by likelihood of already existing in a real QBO company.
# "Uncategorized Expense" and "Ask My Accountant" are seeded by default
# in many regions, so this usually finds one on the first try.
PREFERRED_ACCOUNT_NAMES = [
    "Uncategorized Expense",
    "Miscellaneous",
    "Miscellaneous Expense",
    "Ask My Accountant",
    "Other Miscellaneous Expense",
]

# Deliberately ugly and specific — screams "come reclassify me" to a bookkeeper.
FALLBACK_ACCOUNT_NAME = "Invoice Imports - Needs Review"


def get_default_expense_account(qb_client):
    """
    Walk the Chart of Accounts looking for a sensible default expense account.

    Strategy:
      1. Query all Expense-type accounts once (QBO caps at 1 000,
         well beyond any real CoA).
      2. Check for preferred names (case-insensitive, in priority order).
      3. If nothing matches, create a new Expense account called
         "Invoice Imports - Needs Review" so the bookkeeper knows to reclassify.

    Returns a Ref suitable for AccountBasedExpenseLineDetail.AccountRef.
    """
    accounts = Account.filter(AccountType="Expense", qb=qb_client)
    # QBO treats "Other Expense" as a separate type, so grab those too.
    accounts += Account.filter(AccountType="Other Expense", qb=qb_client)

    by_name = {a.Name.lower(): a for a in accounts}

    for name in PREFERRED_ACCOUNT_NAMES:
        match = by_name.get(name.lower())
        if match:
            print(f"Using existing expense account: {match.Name!r} (ID {match.Id})")
            ref = Ref()
            ref.value = match.Id
            ref.name = match.Name
            return ref

    # None of our preferred names exist — create the fallback.
    new_acct = Account()
    new_acct.Name = FALLBACK_ACCOUNT_NAME
    new_acct.AccountType = "Expense"
    new_acct.AccountSubType = "OtherMiscellaneousServiceCost"
    new_acct.save(qb=qb_client)

    print(f"Created new expense account: {new_acct.Name!r} (ID {new_acct.Id})")
    ref = Ref()
    ref.value = new_acct.Id
    ref.name = new_acct.Name
    return ref


expense_account_ref = get_default_expense_account(qb_client)

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

# Some versions of python-quickbooks initialize Line as None, not [].
bill.Line = bill.Line or []

if not line_items:
    # No line items extracted — fall back to a single line using the total.
    line = BillLine()
    # NOTE: We preserve the sign here. A negative value likely means a credit
    # memo or discount, and silently flipping it would create an incorrect bill.
    line.Amount = float(total_amount) if total_amount else 0
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

        # item_total comes back as a string (e.g. "34570.80") in this config,
        # but other configs/fields may return a bare number. Coerce to str
        # first so .replace() is always safe. Sign is preserved — a negative
        # value from the extraction is meaningful (credit/discount).
        raw_total = (item.get("item_total") or {}).get("value", "0")
        amount = float(str(raw_total).replace(",", ""))

        description = (item.get("item_description") or {}).get("value", "")

        line = BillLine()
        line.Amount = amount
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