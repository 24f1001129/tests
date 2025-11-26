# Build nested-huge.json with many users; alpha_agent will have deterministic order amounts summing to 98765
import json
from pathlib import Path

out = Path.cwd()

users = []
# make 5000 users
for i in range(5000):
    uname = f"user{i:05d}"
    # many orders but small amounts
    orders = [{"id": f"O{i}-{j}", "amount": (j * 3) % 1000} for j in range(10)]
    users.append({"username": uname, "orders": orders})

# Create alpha_agent with orders that sum to 98765
alpha_orders = [{"id": f"A-{i}", "amount": a} for i, a in enumerate([10000,20000,30000,38765])]
users[2500] = {"username": "alpha_agent", "orders": alpha_orders}

big = {"meta": {"count": len(users)}, "users": users}
(out / "nested-huge.json").write_text(json.dumps(big))
print("nested-huge.json generated. Expected sum for alpha_agent: 98765")



