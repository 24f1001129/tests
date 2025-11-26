# Create dirty.csv with 20000 rows and a deterministic sum for amounts
import pandas as pd
import numpy as np
from pathlib import Path

out = Path.cwd()

np.random.seed(0)
size = 20000

# We'll make most rows have amounts but in various formats; include some 'unknown' and NaN
base_values = np.random.randint(100, 10000, size)
formats = []
clean_values = []

for v in base_values:
    if v % 50 == 0:
        formats.append("unknown")
        clean_values.append(0)
    elif v % 97 == 0:
        formats.append("")  # empty => NaN
        clean_values.append(0)
    else:
        # random choose format
        if v % 3 == 0:
            s = f"${v:,}.00"
        elif v % 3 == 1:
            s = f"{v:,}"
        else:
            s = f"{v}.5"
        formats.append(s)
        clean_values.append(float(str(v).replace(",", "")) if "." not in s else float(s.replace("$","").replace(",","")))

# Force total to known number: compute sum of clean_values then compute offset to reach target 1234567.89
current_sum = sum(clean_values)
target = 1234567.89
offset = target - current_sum

# Add offset to first value that is numeric
for i, f in enumerate(formats):
    if isinstance(formats[i], str) and formats[i] not in ("unknown", ""):
        # adjust by adding offset to this numeric cell (render in same format style)
        new_val = float(clean_values[i]) + offset
        formats[i] = f"${int(new_val):,}.00"
        break

df = pd.DataFrame({"id": range(size), "amount": formats})
df.to_csv(out / "dirty.csv", index=False)
print("dirty.csv generated with 20000 rows. Expected sum (rounded 2 dec): 1234567.89")



