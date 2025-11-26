import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

out = Path.cwd()
size = 20000
rows = []
start = datetime(2024, 1, 1)

for i in range(size):
    d = start + timedelta(days=(i % 366))
    if i % 3 == 0:
        s = d.strftime("%Y/%m/%d")
    elif i % 3 == 1:
        s = d.strftime("%d-%m-%Y")
    else:
        excel_serial = (d - datetime(1899,12,31)).days
        s = str(excel_serial)
    rows.append({"idx": i, "date": s})

df = pd.DataFrame(rows)
df.to_csv(out / "dates.csv", index=False)
print("dates.csv generated (20000 rows). Expected Mondays in 2024: 3387")