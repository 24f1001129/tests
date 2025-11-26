# Generate a 7-page PDF containing a table split across pages and ensure score mean == 50.0
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path

out = Path.cwd()

scores = [50] * 700  # 700 rows, all score 50 -> mean 50.0
c = canvas.Canvas(str(out / "mixed_layout.pdf"), pagesize=letter)

r = 0
for p in range(1, 8):
    y = 700
    c.drawString(40, y+20, f"Page {p}")
    # Put 100 rows per page
    for i in range(100):
        if r >= len(scores):
            break
        # sometimes render with commas (though 50 has none), but we'll render as string intentionally inconsistent
        score_str = f"{scores[r]}" if r % 10 else f"{scores[r]:,}"
        c.drawString(40, y, f"row{r},score,{score_str}")
        y -= 10
        r += 1
    c.showPage()

c.save()
print("mixed_layout.pdf generated (7 pages). Expected mean score: 50.000")



