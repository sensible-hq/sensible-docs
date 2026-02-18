#!/usr/bin/env python3
"""
Redact and replace text in a PDF using PyMuPDF.

Each replacement whites out the matched text and inserts the replacement
at the same position, preserving the original font size.

Usage:
    python scripts/redact_pdf.py \\
        --input  <path/to/input.pdf> \\
        --output <path/to/output.pdf> \\
        --replacements '[{"find": "Real Name", "replace": "Fake Name"}, ...]'

Replacement object fields:
    find        (required) Text to search for.
    replace     (required) Replacement text.
    bold        (optional, default false) Use bold (Helvetica-Bold) instead of
                regular (Helvetica) for the replacement text.
    page        (optional) Zero-indexed page number to restrict the search to.
                Omit to search all pages.
    fontsize    (optional) Font size for the replacement. Defaults to the size
                of the first matched span, or 10 if not detectable.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)


def detect_fontsize(page: fitz.Page, text: str) -> float:
    """Return the font size of the first span containing `text`, or 10."""
    for block in page.get_text("dict")["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if text in span["text"]:
                    return span["size"]
    return 10.0


def apply_replacement(doc: fitz.Document, find: str, replace: str,
                      bold: bool, page_idx: int | None, fontsize: float | None) -> int:
    """Apply one find/replace across the document (or a single page). Returns match count."""
    pages = [doc[page_idx]] if page_idx is not None else list(doc)
    count = 0
    fontname = "hebo" if bold else "helv"  # hebo = Helvetica-Bold

    for page in pages:
        rects = page.search_for(find)
        if not rects:
            continue
        size = fontsize or detect_fontsize(page, find)
        for rect in rects:
            page.add_redact_annot(
                rect,
                text=replace,
                fontname=fontname,
                fontsize=size,
                fill=(1, 1, 1),
                text_color=(0, 0, 0),
                align=0,
            )
            count += 1
        page.apply_redactions()

    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Redact and replace text in a PDF."
    )
    parser.add_argument("--input",        required=True, type=Path, help="Input PDF path")
    parser.add_argument("--output",       required=True, type=Path, help="Output PDF path")
    parser.add_argument("--replacements", required=True,
                        help='JSON array of replacement objects: [{"find":..., "replace":...}]')
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        replacements = json.loads(args.replacements)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON in --replacements: {e}", file=sys.stderr)
        sys.exit(1)

    doc = fitz.open(str(args.input))

    for r in replacements:
        find     = r["find"]
        replace  = r["replace"]
        bold     = r.get("bold", False)
        page_idx = r.get("page")        # None = all pages
        fontsize = r.get("fontsize")

        count = apply_replacement(doc, find, replace, bold, page_idx, fontsize)
        if count == 0:
            print(f"  WARNING: no match found for {repr(find)}")
        else:
            print(f"  {repr(find)} → {repr(replace)} ({count} replacement{'s' if count > 1 else ''})")

    doc.save(str(args.output))
    doc.close()
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
