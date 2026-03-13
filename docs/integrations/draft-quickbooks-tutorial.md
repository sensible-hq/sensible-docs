---
title: QuickBooks tutorial
excerpt: ''
deprecated: false
hidden: true
metadata:
  title: ''
  description: 'extract bank statements into QuickBooks Online'
  robots: index
next:
  description: ''
---
This topic describes sending extracted data from bank statements into QuickBooks Online using Sensible's Zapier integration.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickbooks_0.png)

This Zap:

1. triggers every time that Sensible extracts from a document of the `bank_statements` document type, and
2. creates a new journal entry in QuickBooks Online from the extracted data.

## Create an example Sensible extraction

To configure Zapier, you'll use a recent example of a document extraction:

1. Follow the steps in [Getting started with out-of-the-box extractions](https://docs.sensible.so/docs/library-quickstart) to create support for the `bank_statements` document type.

2. Download an [example bank statement](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Bank%20Statements/refdocs) from the Sensible library.

3. In the Sensible app, click the **Extract** tab. Upload the example document, select the `bank_statements` document type, and run an extraction.

## Set up a destination in QuickBooks Online

Before you can integrate Sensible with QuickBooks Online, you need a bank account in your Chart of Accounts to post journal entries to. Take the following steps:

1. Sign in or create a [QuickBooks Online](https://quickbooks.intuit.com/) account.

2. Navigate to **Accounting** > **Chart of Accounts** and verify that a bank account exists. If not, click **New**, set the **Account Type** to **Bank**, and save.

## Configure Zapier

Take the following steps to connect Sensible to QuickBooks Online using Zapier:

1. Sign in or create a [Zapier account](https://zapier.com/).

2. Create a new Zap. For your trigger, search for and select **Sensible**.

3. Take the following steps to connect your Sensible account to Zapier:
   1. Click to expand the **Trigger** section.
   2. Click to expand the **Choose account** section, then follow the prompts to connect your Sensible account.

4. In the **Set up trigger** section:

   1. Select the **bank_statements** document type you created in the previous steps.

   2. Select the **Production** environment.

   3. Select the **Complete** status.

   4. Leave the default for the **Create Excel output** option.

      **Note:** If you select true for this option, you can access the extracted document data [converted](https://docs.sensible.so/docs/excel-reference) to an Excel file in succeeding Zapier actions. This is useful for accessing multi-value fields such as `transactions` and `checks`. For an example of using this option, see [Advanced Zapier tutorial](https://docs.sensible.so/docs/zapier-tutorial-2).

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickbooks_1.png)

5. Continue to the **Test trigger** section and follow the prompts to test. Verify that the recent document extraction you created in previous steps is selected.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickbooks_2.png)

6. Continue to the **Action** section, search for and select **QuickBooks Online**:
   1. For the **Event**, choose **Create Journal Entry**.
   2. Follow the prompts to connect your QuickBooks Online account to Zapier.

7. In the **Set up action** section, map Sensible extracted field IDs to the corresponding QuickBooks Online fields. Zapier displays the data from the recent document extraction as examples. Use the following mappings as a guide:

   1. **Transaction Date**: Select `end_date`.
   2. **Private Note**: Select `customer_name` to record the account holder name.
   3. **Line 1 Amount**: Select `ending_balance`.
   4. **Line 1 Account**: Select the bank account from your Chart of Accounts.

   (Optional) To include the beginning balance and statement period, map `beginning_balance` and `start_date` to additional line items or memo fields.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickbooks_3.png)

8. Follow the prompts to test the action. You should see a new journal entry in QuickBooks Online containing the bank statement data.

![Click to enlarge](https://raw.githubusercontent.com/sensible-hq/sensible-docs/v0/assets/images/final/quickbooks_4.png)

9. Follow the prompts to publish your Zap.

## (Optional) Test your integration

Congratulations, your integration is now published and running! Take the following steps to continue populating QuickBooks Online from example documents:

1. Download additional example bank statements from the Sensible [library](https://github.com/sensible-hq/sensible-configuration-library/tree/main/templates/Financial%20Services/Bank%20Statements/refdocs).

2. Use the Sensible app's **Extract** tab to run extractions for the example documents.

3. Zapier can take up to 15 minutes to pull data from Sensible. To avoid waiting, navigate to the **Zaps** tab in Zapier, right-click the Zap's ellipsis (...) icon and click **Run**.

4. Verify the journal entries appear in QuickBooks Online under **Accounting** > **Chart of Accounts** > **View register** for the bank account you selected.

## (Optional) Scale up

You can extract from more bank statements automatically by building a more complex Zap so that you can trigger Sensible extractions with file actions in Google Drive, email, or other Zapier-supported apps. Then send the extraction to QuickBooks Online or another destination with a Sensible action. For more information, see [Advanced Zapier tutorial](https://docs.sensible.so/docs/zapier-tutorial-2).

**Note:** Sensible offers native support for automatically extracting from email attachments. Instead of using Zapier for emails, see [Getting started with email extractions](https://docs.sensible.so/docs/getting-started-email).



## (Optional) Automate with Python

As an alternative to Zapier, you can use Sensible's Python SDK and the `python-quickbooks` library to extract bank statements and post journal entries to QuickBooks Online in a single script. This approach gives you full control over the data transformation and is suitable for batch processing or server-side automation.

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
| `QBO_BANK_ACCOUNT_ID` | The QuickBooks account ID for the bank account to debit. Find it under **Accounting** > **Chart of Accounts**. |
| `QBO_EQUITY_ACCOUNT_ID` | The QuickBooks account ID for the offsetting equity account (for example, Opening Balance Equity). |

**Note:** To obtain a refresh token, complete the OAuth 2.0 authorization flow once using the Intuit Developer Portal's OAuth Playground or your app's auth endpoint. The script uses the refresh token to generate access tokens automatically on each run.

### Script

```python
import os
from sensibleapi import SensibleSDK
from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects.journalentry import JournalEntry, JournalEntryLine, JournalEntryLineDetail
from quickbooks.objects.base import Ref

# ── Sensible extraction ────────────────────────────────────────────────────────

sensible = SensibleSDK(os.environ["SENSIBLE_API_KEY"])

request = sensible.extract(
    path="./bank_statement.pdf",   # replace with your file path
    document_type="bank_statements",
    environment="production",
)
result = sensible.wait_for(request)

parsed = result["parsed_document"]

# Extract the fields we need; .get() returns None if a field wasn't extracted
end_date         = (parsed.get("end_date")          or {}).get("value")
customer_name    = (parsed.get("customer_name")     or {}).get("value")
ending_balance   = (parsed.get("ending_balance")    or {}).get("value")
beginning_balance = (parsed.get("beginning_balance") or {}).get("value")

if ending_balance is None or beginning_balance is None:
    raise ValueError("Required balance fields not found in extraction. Check the document or config.")

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

# ── Build journal entry ────────────────────────────────────────────────────────
# Journal entries must balance: total debits == total credits.
# Here we debit the bank account by the ending balance and credit
# an equity account by the same amount as a reconciliation entry.

def make_line(amount, posting_type, account_id):
    detail = JournalEntryLineDetail()
    detail.PostingType = posting_type
    account_ref = Ref()
    account_ref.value = account_id
    detail.AccountRef = account_ref

    line = JournalEntryLine()
    line.Amount = abs(float(amount))
    line.DetailType = "JournalEntryLineDetail"
    line.JournalEntryLineDetail = detail
    return line

journal_entry = JournalEntry()
journal_entry.TxnDate = str(end_date) if end_date else None
journal_entry.PrivateNote = (
    f"Bank statement reconciliation — {customer_name}. "
    f"Beginning balance: {beginning_balance}"
)

journal_entry.Line.append(
    make_line(ending_balance, "Debit",  os.environ["QBO_BANK_ACCOUNT_ID"])
)
journal_entry.Line.append(
    make_line(ending_balance, "Credit", os.environ["QBO_EQUITY_ACCOUNT_ID"])
)

saved = journal_entry.save(qb=qb_client)
print(f"Journal entry created: ID {saved.Id}, date {saved.TxnDate}")
```

# Notes

**Limitations**

* You can configure single-value field output with the Sensible-Zapier integration. Bank statements include `transactions` and `checks` fields that output data objects (tables). To handle these in Zapier, enable the **Excel output** option on the Sensible trigger. Then access the extracted tables as rows using Zapier's spreadsheet integrations, for example Google Sheets. For more information, see [SenseML to Excel reference](https://docs.sensible.so/docs/excel-reference).
* You can extract from single-document files with Zapier. If you want to extract from portfolio files (files that contain multiple documents), use the Sensible API or SDKs.

**QuickBooks Online limitations**

* This integration supports QuickBooks Online only. QuickBooks Desktop is not supported via Zapier.
* Journal entries created via Zapier appear as unreviewed in QuickBooks Online. Review and approve entries in QuickBooks before using them for reconciliation.
* Zapier ignores uploaded files in Google Drive whose create or modified date is older than 4 days when using **New file in folder** as the Sensible action trigger.

