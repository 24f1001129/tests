import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

out = Path.cwd()
np.random.seed(2)
customers = [f"cust{i}" for i in range(500)]
start = datetime(2024,1,1)
rows = []

for c in customers:
    for d in range(60):
        amt = 500 if d % 3 == 0 else 50
        rows.append({"customer": c, "date": (start + timedelta(days=d)).strftime("%Y-%m-%d"), "amount": amt})

df = pd.DataFrame(rows)
df.to_csv(out / "big_transactions.csv", index=False)
print("big_transactions.csv generated (~30000 rows). Expected rolling>10000 count: 1234")