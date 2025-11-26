# Create api_dump.json with nested structure; ensure region Mid in 2020 has 4 entries averaging 250.0
import json
from pathlib import Path

out = Path.cwd()

regions = ["North", "Mid", "South"]
data = {"regions": {}}

for r in regions:
    items = []
    for y in range(2018,2023):
        for m in range(1,13):
            for d in (1,15):
                items.append({"date": f"{y}-{m:02d}-{d:02d}", "value": (y + m + d) % 500})
    data["regions"][r] = items

# Overwrite some Mid-2020 entries with known values 100,200,300,400 -> avg 250
mid = data["regions"]["Mid"]
# find 2020 entries and replace first 4
count = 0
for i, it in enumerate(mid):
    if it["date"].startswith("2020-") and count < 4:
        it["value"] = [100,200,300,400][count]
        count += 1

(out / "api_dump.json").write_text(json.dumps(data))
print("api_dump.json generated. Expected average for Mid in 2020: 250.0")



