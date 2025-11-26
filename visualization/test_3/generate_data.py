import pandas as pd
from datetime import date, timedelta
from pathlib import Path

out = Path.cwd()
start = date(2024,1,1)
days = 200
rows = []

for d in range(days):
    dt = (start + timedelta(days=d)).isoformat()
    a = 100 + d % 50
    b = 100 + d % 40
    c = 100 + d % 60
    if d == 150:
        b += 10000
    rows.append({"date": dt, "A": a, "B": b, "C": c})

df = pd.DataFrame(rows)
df.to_csv(out / "timeseries.csv", index=False)
print("timeseries.csv generated. Expected series with largest single-day spike: B")