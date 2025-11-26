# Generates login.html (a page that echoes POST data and links to secret.html for correct creds)
from pathlib import Path

out = Path.cwd()

# login.html explains expected credentials and provides link if posted correctly.
login = """<!DOCTYPE html><html><head><title>Login</title></head><body>
<h2>Login Handler</h2>
<p>This test server expects credentials: username=agent, password=letmein</p>
<!-- In a real test, server would check POST. For this static repo, provide an anchor with the secret -->
<a href="./secret.html">If credentials correct, go to secret</a>
</body></html>"""

secret = """<!DOCTYPE html><html><head><title>Secret</title></head><body>
<h2>Secret Page</h2>
<p>The secret code for this test is: <strong>WS-300</strong></p>
</body></html>"""

(out / "login.html").write_text(login)
(out / "secret.html").write_text(secret)
print("login.html and secret.html generated. Expected secret: WS-300")



