# Creates dynamic-data.json with the reveal number and also a small script that simulates many items
import json
from pathlib import Path

out = Path.cwd()

# Build a JSON > ~1KB to make it non-trivial; reveal key present
data = {"meta": {"source": "test"}, "items": [{"i": i, "v": i*i % 1000} for i in range(1000)], "reveal": 314159}

(out / "dynamic-data.json").write_text(json.dumps(data))
print("dynamic-data.json generated. Expected reveal value: 314159")



