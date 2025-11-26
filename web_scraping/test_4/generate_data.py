# Create 5 pages each with 200 rows; on each page we'll include 20 rows with category "X" with values 50 each.
from pathlib import Path

out = Path.cwd()

rows_per_page = 200
x_count_per_page = 20
x_value = 50

# Expected sum = 5 pages * 20 rows/page * 50 = 5000

for p in range(1, 6):
    rows = []
    # create rows, insert x_count_per_page occurrences of category "X"
    for i in range(rows_per_page):
        cat = "X" if i < x_count_per_page else f"C{i%5}"
        val = x_value if i < x_count_per_page else (i % 100)
        rows.append(f"<tr><td>{cat}</td><td>{val}</td></tr>")
    
    body = "<table><tr><th>category</th><th>value</th></tr>" + "".join(rows) + "</table>"
    nav = ""
    if p < 5:
        nav = f'<a href="./page{p+1}.html">Next</a>'
    
    page = f"<!DOCTYPE html><html><head><title>Page {p}</title></head><body><h2>Page {p}</h2>{body}{nav}</body></html>"
    (out / f"page{p}.html").write_text(page)

print("page1..page5.html generated. Expected sum for category X: 5000")



