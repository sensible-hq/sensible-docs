#!/usr/bin/env python3
"""Make the commission statement test spreadsheets (XLSX, XLS, XLSM) from commission_statement.csv,
with LibreOffice, so each one displays exactly like the CSV (money as #,##0.00, rates as 0%).
The XLSB is saved by hand from Excel: LibreOffice can read XLSB but not write it.

Needs LibreOffice Calc and its Python bridge (sudo apt install libreoffice-calc). Run with the system
python3, which has `uno`:  python3 make_spreadsheets.py commission_statement.csv
Check a file with: soffice --headless --convert-to 'csv:Text - txt - csv (StarCalc):44,34,76,1,,1033,false,true,true' FILE
"""
import os, subprocess, sys, time
import uno
from com.sun.star.beans import PropertyValue

def prop(name, value):
    p = PropertyValue(); p.Name, p.Value = name, value; return p

src = os.path.abspath(sys.argv[1]); base = os.path.splitext(src)[0]
office = subprocess.Popen(["soffice", "--headless", "--invisible", "--norestore",
                           "--accept=socket,host=localhost,port=2083;urp;"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    resolver = uno.getComponentContext().ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", uno.getComponentContext())
    for _ in range(60):
        try:
            ctx = resolver.resolve("uno:socket,host=localhost,port=2083;urp;StarOffice.ComponentContext"); break
        except Exception:
            time.sleep(0.5)
    desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(src), "_blank", 0,
                                       (prop("FilterName", "Text - txt - csv (StarCalc)"), prop("FilterOptions", "44,34,76,1"), prop("Hidden", True)))
    sheet = doc.Sheets.getByIndex(0)
    fmt = doc.NumberFormats.queryKey("#,##0.00", doc.CharLocale, False)
    if fmt == -1:
        fmt = doc.NumberFormats.addNew("#,##0.00", doc.CharLocale)
    for rng in ("D6:D7", "F6:F8", "B9"):
        sheet.getCellRangeByName(rng).NumberFormat = fmt
    percent = doc.NumberFormats.queryKey("0%", doc.CharLocale, False)
    sheet.getCellRangeByName("E6:E7").NumberFormat = percent if percent != -1 else doc.NumberFormats.addNew("0%", doc.CharLocale)
    for ext, filt in (("xlsx", "Calc Office Open XML"), ("xls", "MS Excel 97"), ("xlsm", "Calc MS Excel 2007 VBA XML")):
        doc.storeToURL(uno.systemPathToFileUrl(f"{base}.{ext}"), (prop("FilterName", filt), prop("Overwrite", True)))
        print(f"wrote {base}.{ext}")
    doc.close(True)
finally:
    try: desktop.terminate()
    except Exception: pass
    office.wait(timeout=30)
