import base64
import pandas as pd
from pathlib import Path

out = Path.cwd()
size = 30000
rows = []

for i in range(size):
    if i < 100:
        val = 70
        enc = base64.b64encode(str(val).encode()).decode()
    elif i % 500 == 0:
        enc = "!!!corrupt!!!"
    else:
        enc = base64.b64encode(str(i % 123).encode()).decode()
    rows.append({"id": i, "encoded": enc})

df = pd.DataFrame(rows)
df.to_csv(out / "trans.csv", index=False)
print("trans.csv generated (30000 rows). Expected sum of decoded ints divisible by 7: 7000")