# Generates page1.html and page2.html with a hidden meta token.
from pathlib import Path

out = Path.cwd()

# page1 links to page2
page1 = """<!DOCTYPE html><html><head><title>Page1</title></head><body>
<h2>Page 1</h2>
<a id="to2" href="./page2.html">Go to Page 2</a>
</body></html>"""

# page2 contains the hidden token in a meta tag and visible hint
page2 = """<!DOCTYPE html><html><head><title>Page2</title>
<meta name="secret-token" content="TOKEN-12345">
</head><body>
<h2>Page 2</h2>
<p>Look at meta name="secret-token"</p>
</body></html>"""

(out / "page1.html").write_text(page1)
(out / "page2.html").write_text(page2)
print("page1.html and page2.html generated. Expected token: TOKEN-12345")



