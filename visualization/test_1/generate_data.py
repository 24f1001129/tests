import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

out = Path.cwd()
cats = ["A","B","C","D"]
rows = []

for i in range(20000):
    cat = cats[i % 4]
    val = 100 if cat == "A" else (200 if cat=="B" else (700 if cat=="C" else 300))
    rows.append({"id": i, "category": cat, "value": val})

df = pd.DataFrame(rows)
df.to_csv(out / "chart_data.csv", index=False)
agg = df.groupby("category").value.sum()
agg.plot(kind="bar")
plt.title("Category aggregate")
plt.savefig(out / "chart.png")
print("chart_data.csv and chart.png generated. Expected value for category C: 700")