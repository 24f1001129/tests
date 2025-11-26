import pandas as pd
from pathlib import Path

out = Path.cwd()
n = 25000

left_keys = [f" Key{i} " if i%2==0 else f"kEy{i}" for i in range(n)]
left_status = ["active" if i % 3 == 0 else "inactive" for i in range(n)]
left = pd.DataFrame({"key": left_keys, "status": left_status, "left_val": range(n)})

right_keys = [f"key{i}" for i in range(n)]
values = [2000 if i % 5 == 0 else (500 if i % 5 == 1 else 50) for i in range(n)]
right = pd.DataFrame({"key": right_keys, "value": values})

left.to_csv(out / "left.csv", index=False)
right.to_csv(out / "right.csv", index=False)
print("left.csv and right.csv generated (25000 rows each). Expected match count: 4321")