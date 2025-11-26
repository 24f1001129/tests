import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

out = Path.cwd()
rows = []
user_count = 2000
base = datetime(2024,1,1)

for u in range(user_count):
    num_events = 3 if u % 10 == 0 else (5 + (u % 10))
    start = base + timedelta(seconds=u*10)
    for e in range(num_events):
        ts = start + timedelta(seconds=e * (10 if u%7 else 3600))
        rows.append({"userid": f"user{u}", "event": f"e{e}", "timestamp": ts.isoformat()})

df = pd.DataFrame(rows)
df.to_csv(out / "events.csv", index=False)
print("events.csv generated. Expected 95th percentile session length (sec): 3600")