"""Make two_images.pdf: cgl_quote_screenshot.pdf plus a pasted image on page 1 that reads
"Agency Reference: HIA-REF-4417", so both pages have text that's only in an image.

  python3 add_page1_image.py <dir with cgl_quote_screenshot.pdf>
"""
import sys
import fitz

d = sys.argv[1]
doc = fitz.open(f"{d}/cgl_quote_screenshot.pdf")
page = doc[0]
used = max(b[3] for b in page.get_text("blocks") if b[3] < 740)  # last text above the footer
scratch = fitz.open()
sp = scratch.new_page(width=300, height=40)
sp.draw_rect(fitz.Rect(0, 0, 300, 40), color=(0.7, 0.7, 0.7), fill=(0.96, 0.96, 0.97))
sp.insert_text((10, 26), "Agency Reference: HIA-REF-4417", fontsize=12, fontname="hebo")
y = used + 24
page.insert_image(fitz.Rect(54, y, 354, y + 40), stream=sp.get_pixmap(dpi=200).tobytes("png"))
doc.save(f"{d}/two_images.pdf")
