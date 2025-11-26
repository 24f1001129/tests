# Generates a simple multi-page PDF with text on page 4 containing "XF-834".
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

out = Path.cwd()

c = canvas.Canvas(str(out / "messy.pdf"), pagesize=letter)

# Create 6 pages with scattered text
for p in range(1, 7):
    text = c.beginText(40, 700)
    text.textLine(f"Page {p} - Sample noisy content")
    # add noise
    for i in range(10):
        text.textLine(f"noise {p} {i} --- {p*i}")
    c.drawText(text)
    # Put the hidden code on page 4
    if p == 4:
        c.drawString(100, 400, "Important: The hidden code is XF-834.")
    c.showPage()

c.save()
print("messy.pdf generated (6 pages). Expected code on page 4: XF-834")



