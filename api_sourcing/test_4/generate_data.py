# Build massive.json by repeating blocks; ensure last 'role' == 'target' has token == 'END-TOKEN-77'
import json
from pathlib import Path

out = Path.cwd()

blocks = []
for i in range(20000):
    role = "target" if i == 19999 else ("normal" if i % 50 else "other")
    tok = f"TOKEN-{i}" if role != "target" else "END-TOKEN-77"
    blocks.append({"meta": {"idx": i, "role": role}, "session": {"token": tok, "info": {"i": i}}})

data = {"blocks": blocks}
(out / "massive.json").write_text(json.dumps(data))
print("massive.json generated. Expected token for last target: END-TOKEN-77")



