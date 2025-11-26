import pandas as pd
import numpy as np
from pathlib import Path

out = Path.cwd()
np.random.seed(3)
n = 20000
vals = np.random.normal(loc=55.1234, scale=10, size=n)
svals = []

for i, v in enumerate(vals):
    if i % 50 == 0:
        svals.append(f"{v:,.2f}")
    elif i % 37 == 0:
        svals.append("")
    else:
        svals.append(str(v))

df = pd.DataFrame({"id": range(n), "measurement": svals})
df.to_csv(out / "mixed_types.csv", index=False)
print("mixed_types.csv generated (20000 rows). Expected trimmed mean: 55.1234")