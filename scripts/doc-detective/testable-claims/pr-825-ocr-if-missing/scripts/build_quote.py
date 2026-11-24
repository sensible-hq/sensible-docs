"""Build two versions of a CGL quote letter: premium table as digital text (A) or as a pasted screenshot (B)."""
import sys, fitz

OUT = sys.argv[1]
W, H = 612, 792
M = 54
NAVY = (0.12, 0.2, 0.38)
GRAY = (0.35, 0.35, 0.35)

PREMIUM_ROWS = [
    ("General Liability Premium", "$4,812.00"),
    ("Products/Completed Operations", "$1,236.00"),
    ("Terrorism (TRIA)", "$61.00"),
    ("Total Premium", "$6,109.00"),
    ("Policy Fee", "$150.00"),
    ("Surplus Lines Tax & Stamping Fee", "$218.72"),
    ("Total Due", "$6,477.72"),
]

def lines(page, y, rows, size=10, color=(0, 0, 0), x=M, lead=14):
    for r in rows:
        page.insert_text((x, y), r, fontsize=size, fontname="helv", color=color)
        y += lead
    return y

def letterhead(page, n):
    page.draw_rect(fitz.Rect(0, 0, W, 64), color=None, fill=NAVY)
    page.insert_text((M, 34), "Harborview Insurance Agency", fontsize=16, fontname="hebo", color=(1, 1, 1))
    page.insert_text((M, 52), "1200 Example Avenue, Suite 400  |  Springfield, ST 00000  |  (555) 010-0199",
                     fontsize=8.5, fontname="helv", color=(1, 1, 1))
    page.insert_text((M, H - 30), f"Quote No. HIA-CGL-20481  |  Page {n} of 2", fontsize=8, fontname="helv", color=GRAY)
    page.insert_text((W - M - 180, H - 30), "Quotes are valid for 30 days from issue.", fontsize=8, fontname="helv", color=GRAY)

def heading(page, y, text):
    page.insert_text((M, y), text, fontsize=12, fontname="hebo", color=NAVY)
    page.draw_line((M, y + 4), (W - M, y + 4), color=NAVY, width=0.7)
    return y + 22

def premium_table_digital(page, y):
    """Premium summary drawn as real embedded text."""
    x2 = W - M - 10
    for label, amt in PREMIUM_ROWS:
        bold = label in ("Total Premium", "Total Due")
        f = "hebo" if bold else "helv"
        page.insert_text((M + 10, y), label, fontsize=10, fontname=f)
        tw = fitz.get_text_length(amt, fontname=f, fontsize=10)
        page.insert_text((x2 - tw, y), amt, fontsize=10, fontname=f)
        if label in ("Terrorism (TRIA)", "Total Premium"):
            page.draw_line((M + 10, y + 5), (x2, y + 5), color=GRAY, width=0.5)
        y += 18
    return y + 4

def premium_table_screenshot(page, y):
    """Render the carrier-portal table on a scratch page, rasterize it, paste it as an image only."""
    sw, sh = 504, 190
    scratch = fitz.open()
    sp = scratch.new_page(width=sw, height=sh)
    sp.draw_rect(fitz.Rect(0, 0, sw, sh), color=(0.75, 0.75, 0.75), fill=(0.97, 0.97, 0.98), width=1)
    sp.draw_rect(fitz.Rect(0, 0, sw, 26), color=None, fill=(0.0, 0.42, 0.45))
    sp.insert_text((10, 17), "Northfield Mutual  |  Agent Portal  >  Quote 77-410392  >  Premium Detail",
                   fontsize=9, fontname="helv", color=(1, 1, 1))
    yy = 46
    for label, amt in PREMIUM_ROWS:
        bold = label in ("Total Premium", "Total Due")
        f = "hebo" if bold else "helv"
        sp.insert_text((14, yy), label, fontsize=10, fontname=f, color=(0.15, 0.15, 0.15))
        tw = fitz.get_text_length(amt, fontname=f, fontsize=10)
        sp.insert_text((sw - 14 - tw, yy), amt, fontsize=10, fontname=f, color=(0.15, 0.15, 0.15))
        yy += 20
    pix = sp.get_pixmap(dpi=150)
    rect = fitz.Rect(M, y - 10, M + sw, y - 10 + sh)
    page.insert_image(rect, stream=pix.tobytes("png"))
    return rect.y1 + 16

def build(screenshot):
    doc = fitz.open()
    p1 = doc.new_page(width=W, height=H)
    letterhead(p1, 1)
    y = 96
    y = lines(p1, y, ["November 10, 2026", "", "Greenline Landscaping LLC", "Attn: Owner",
                      "450 Sample Road", "Springfield, ST 00000"])
    y += 8
    y = lines(p1, y, ["Re: Commercial General Liability Quote, Effective 12/01/2026 to 12/01/2027"], size=10.5)
    y += 8
    y = lines(p1, y, [
        "Thank you for the opportunity to quote your commercial general liability coverage. We marketed your",
        "account to four carriers and recommend the attached quote from Northfield Mutual Insurance Company,",
        "rated A (Excellent) by AM Best. The quote is based on the underwriting information you provided on",
        "your application dated October 22, 2026, including annual gross receipts of $1,850,000 and a payroll",
        "of $640,000 for landscaping and lawn care operations. Please review the coverage summary below and",
        "the premium summary on page 2. If any of the underlying information has changed, let us know before",
        "binding, because changes can affect the premium and terms.",
    ])
    y += 10
    y = heading(p1, y, "Coverage Summary")
    cov = [
        ("Carrier", "Northfield Mutual Insurance Company"),
        ("Policy Form", "Occurrence"),
        ("Each Occurrence", "$1,000,000"),
        ("General Aggregate", "$2,000,000"),
        ("Products/Completed Operations Aggregate", "$2,000,000"),
        ("Personal & Advertising Injury", "$1,000,000"),
        ("Damage to Premises Rented to You", "$100,000"),
        ("Medical Expense (Any One Person)", "$5,000"),
        ("Deductible", "$1,000 per claim, property damage"),
        ("Additional Insured", "Blanket, where required by written contract"),
        ("Waiver of Subrogation", "Blanket, where required by written contract"),
        ("Primary & Non-Contributory", "Included"),
    ]
    for k, v in cov:
        p1.insert_text((M + 10, y), k, fontsize=10, fontname="helv")
        p1.insert_text((M + 260, y), v, fontsize=10, fontname="helv")
        y += 15
    y += 10
    y = heading(p1, y, "Notable Exclusions")
    y = lines(p1, y, [
        "- Pesticide and herbicide application, unless performed by a licensed applicator",
        "- Snow and ice removal operations",
        "- Tree trimming above 15 feet",
        "- Professional liability and errors & omissions",
        "- Employment practices liability",
    ], x=M + 10)

    p2 = doc.new_page(width=W, height=H)
    letterhead(p2, 2)
    y = 100
    y = heading(p2, y, "Premium Summary")
    y = lines(p2, y, ["Premium shown is annual and fully earned at 25% upon binding. Taxes and fees are non-refundable."])
    y += 14
    y = premium_table_screenshot(p2, y) if screenshot else premium_table_digital(p2, y)
    y += 8
    y = heading(p2, y, "Payment Options")
    y = lines(p2, y, [
        "- Paid in full at binding",
        "- 25% down, then 9 monthly installments (a $10 installment fee applies to each installment)",
        "- Premium financing is available through our finance partner on request",
    ], x=M + 10)
    y += 10
    y = heading(p2, y, "Subjectivities")
    y = lines(p2, y, [
        "Before binding, the carrier requires the following:",
        "1. Signed and dated application (ACORD 125 and ACORD 126)",
        "2. Currently valued loss runs for the past 5 years from all prior carriers",
        "3. Signed surplus lines disclosure form",
        "4. Copy of the applicator license for any pesticide or herbicide work",
    ], x=M + 10)
    y += 10
    y = heading(p2, y, "Important Notice")
    lines(p2, y, [
        "This quote is an indication of coverage only and does not bind coverage. Coverage is subject to",
        "the terms, conditions, and exclusions of the policy as issued. The quote is valid for 30 days from",
        "the date of this letter. To bind coverage, sign below and return this letter with the items listed",
        "under Subjectivities and your down payment.",
        "",
        "Accepted by: ______________________________    Date: ______________",
        "",
        "Sincerely,",
        "Jordan Example, CIC",
        "Commercial Lines Account Manager, Harborview Insurance Agency",
    ])
    return doc

for name, shot in (("cgl_quote_digital", False), ("cgl_quote_screenshot", True)):
    d = build(shot)
    d.set_metadata({"title": "Commercial General Liability Quote", "producer": "Harborview Agency System"})
    d.save(f"{OUT}/{name}.pdf")
    print("wrote", name)
