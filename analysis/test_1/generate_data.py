import pandas as pd
import numpy as np
from pathlib import Path

out = Path.cwd()
np.random.seed(1)
n = 25000
regions = ["North", "South", "East", "West"]
region_col = np.random.choice(regions, n)
scores = np.random.randint(10, 90, n)
weights = np.random.randint(1, 10, n)

df = pd.DataFrame({"region": region_col, "score": scores, "weight": weights})
north_idx = df[df.region == "North"].index
for j, idx in enumerate(north_idx):
    df.at[idx, "score"] = 42 if j % 2 == 0 else 43

df.to_csv(out / "sales_big.csv", index=False)
print("sales_big.csv generated (25000 rows). Expected weighted avg for North: 42.500")