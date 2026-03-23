import os
import requests
from pathlib import Path

from sensibleapi import SensibleSDK
from quickbooks.objects.account import Account
from quickbooks.objects.bill import Bill
from quickbooks.objects.detailline import (
    AccountBasedExpenseLine,
    AccountBasedExpenseLineDetail,
)
from quickbooks.objects.vendor import Vendor
from quickbooks.objects.base import Ref
from qbo_auth import get_qb_client

# ── Constants ──────────────────────────────────────────────────────────────────

SAMPLE_PDF_URL = (
    "https://raw.githubusercontent.com/sensible-hq/sensible-configuration-library"
    "/main/templates/Utilities%20%26%20Invoices/Invoices/refdocs/llm_invoices_template.pdf"
)

DEFAULT_VENDOR = "Unmatched - Review Required"

PREFERRED_ACCOUNT_NAMES = [
    "Uncategorized Expense",
    "Miscellaneous",
    "Miscellaneous Expense",
    "Ask My Accountant",
    "Other Miscellaneous Expense",
]

FALLBACK_ACCOUNT_NAME = "Invoice Imports - Needs Review"

# ── Helpers ────────────────────────────────────────────────────────────────────


def get_field(parsed, key):
    return (parsed.get(key) or {}).get("value")


def make_ref(id, name):
    ref = Ref()
    ref.value = id
    ref.name = name
    return ref


def parse_amount(value):
    return float(str(value).replace(",", "")) if value else 0.0


def get_default_expense_account(qb_client):
    accounts = Account.filter(AccountType="Expense", qb=qb_client)
    accounts += Account.filter(AccountType="Other Expense", qb=qb_client)

    by_name = {a.Name.lower(): a for a in accounts}

    for name in PREFERRED_ACCOUNT_NAMES:
        match = by_name.get(name.lower())
        if match:
            print(f"  ✓ Using existing account: {match.Name!r} (ID {match.Id})")
            return make_ref(match.Id, match.Name)

    new_acct = Account()
    new_acct.Name = FALLBACK_ACCOUNT_NAME
    new_acct.AccountType = "Expense"
    new_acct.AccountSubType = "OtherMiscellaneousServiceCost"
    new_acct.save(qb=qb_client)

    print(f"  ✓ Created new account: {new_acct.Name!r} (ID {new_acct.Id})")
    return make_ref(new_acct.Id, new_acct.Name)


# ── Download sample invoice ────────────────────────────────────────────────────

script_dir = Path(__file__).resolve().parent
invoice_path = script_dir / "llm_invoices_template.pdf"

print("\n[1/6] Downloading sample invoice ...")
if not invoice_path.exists():
    resp = requests.get(SAMPLE_PDF_URL)
    resp.raise_for_status()
    invoice_path.write_bytes(resp.content)
    print(f"  ✓ Saved to {invoice_path}")
else:
    print(f"  ✓ Already exists at {invoice_path}, skipping download.")

# ── Sensible extraction ────────────────────────────────────────────────────────

print("\n[2/6] Extracting invoice with Sensible ...")
sensible = SensibleSDK(os.environ["SENSIBLE_API_KEY"])

request = sensible.extract(
    path=str(invoice_path),
    document_type="invoices",
    environment="production",
)
result = sensible.wait_for(request)

parsed = result["parsed_document"]

invoice_date   = get_field(parsed, "Invoice date")
due_date       = get_field(parsed, "Invoice due date")
invoice_number = get_field(parsed, "Invoice number")
vendor_name    = get_field(parsed, "Vendor name")
total_amount   = get_field(parsed, "Total amount of invoice")
line_items     = parsed.get("line_items", [])

print(f"  ✓ Vendor: {vendor_name or '(not found)'}")
print(f"  ✓ Invoice #: {invoice_number or '(not found)'}")
print(f"  ✓ Total: {total_amount or '(not found)'}")
print(f"  ✓ Line items: {len(line_items)}")

if not vendor_name:
    print(f"  ⚠ Vendor name not found. Using default: {DEFAULT_VENDOR}")
    vendor_name = DEFAULT_VENDOR

# ── QuickBooks Online auth ─────────────────────────────────────────────────────

print("\n[3/6] Authenticating with QuickBooks Online ...")
qb_client = get_qb_client()
print("  ✓ Connected.")

# ── Find or create a default expense account ──────────────────────────────────

print("\n[4/6] Resolving expense account ...")
expense_account_ref = get_default_expense_account(qb_client)

# ── Find or create vendor ──────────────────────────────────────────────────────

print("\n[5/6] Resolving vendor ...")
vendors = Vendor.filter(DisplayName=vendor_name, qb=qb_client)
if vendors:
    vendor_ref = make_ref(vendors[0].Id, vendors[0].DisplayName)
    print(f"  ✓ Found existing vendor: {vendor_ref.name} (ID {vendor_ref.value})")
else:
    new_vendor = Vendor()
    new_vendor.DisplayName = vendor_name
    new_vendor.save(qb=qb_client)
    vendor_ref = make_ref(new_vendor.Id, new_vendor.DisplayName)
    print(f"  ✓ Created new vendor: {vendor_ref.name} (ID {vendor_ref.value})")

# ── Build bill ─────────────────────────────────────────────────────────────────

print("\n[6/6] Creating bill in QuickBooks ...")

bill = Bill()
bill.TxnDate = str(invoice_date) if invoice_date else None
bill.DueDate = str(due_date) if due_date else None
bill.DocNumber = str(invoice_number) if invoice_number else None
bill.VendorRef = vendor_ref
bill.Line = []

if not line_items:
    detail = AccountBasedExpenseLineDetail()
    detail.AccountRef = expense_account_ref

    line = AccountBasedExpenseLine()
    line.Amount = parse_amount(total_amount)
    line.Description = "Invoice total (line items not extracted)"
    line.AccountBasedExpenseLineDetail = detail
    bill.Line.append(line)
    print(f"  • 1 summary line (no line items extracted): ${line.Amount:,.2f}")
else:
    for i, item in enumerate(line_items, 1):
        detail = AccountBasedExpenseLineDetail()
        detail.AccountRef = expense_account_ref

        amount = parse_amount((item.get("item_total") or {}).get("value"))
        description = (item.get("item_description") or {}).get("value", "")

        line = AccountBasedExpenseLine()
        line.Amount = amount
        line.Description = description
        line.AccountBasedExpenseLineDetail = detail
        bill.Line.append(line)
        print(f"  • Line {i}: {description or '(no description)'} — ${amount:,.2f}")

saved = bill.save(qb=qb_client)
print(f"\n{'='*60}")
print(f"  ✓ Bill created successfully!")
print(f"    ID:     {saved.Id}")
print(f"    Vendor: {vendor_ref.name}")
print(f"    Date:   {saved.TxnDate}")
print(f"    Lines:  {len(bill.Line)}")
print(f"    View:   https://app.sandbox.qbo.intuit.com/app/bill?txnId={saved.Id}")
print(f"{'='*60}")
