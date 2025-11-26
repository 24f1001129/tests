# Generates bigdata.json: many repeated nested objects; ensure one object has meta.id == TARGET-001 and metrics.total == 100000
import json
from pathlib import Path

out = Path.cwd()

items = []
# create 15000 items with small nested data to make file large
for i in range(15000):
    obj = {"meta": {"id": f"ID-{i:05d}", "tags": ["a", "b"]},
           "metrics": {"total": i % 1234, "sub": {"x": i % 7}},
           "payload": {"arr": list(range(5))}}
    items.append(obj)

# Insert target object deep in the middle
target = {"meta": {"id": "TARGET-001", "tags": ["target", "gold"]},
          "metrics": {"total": 100000, "sub": {"x": 99}},
          "payload": {"arr": list(range(10))}}
items[7500] = target

big = {"batch": {"items": items, "generated_by": "generator_v1"}}
(out / "bigdata.json").write_text(json.dumps(big))
print("bigdata.json generated. Expected answer: 100000")



