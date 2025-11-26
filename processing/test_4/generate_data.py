import json, base64
from pathlib import Path

out = Path.cwd()
records = []
values = [100.0, 125.0, 123.5] * 7

for i, v in enumerate(values):
    payload = {"metrics": {"x": f"{int(v):,}" if i%2==0 else v}}
    enc = base64.b64encode(json.dumps(payload).encode()).decode()
    records.append({"id": i, "payload": enc})

for i in range(1000):
    records.append({"id": 100 + i, "payload": "!!!corrupt!!!"})

(out / "encoded_dataset.json").write_text(json.dumps({"records": records}))
print("encoded_dataset.json generated. Expected median: 123.5")