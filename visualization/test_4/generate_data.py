import matplotlib.pyplot as plt
from pathlib import Path

out = Path.cwd()
labels = ['Alpha','Beta','Gamma','Theta','Delta']
sizes = [30,25,20,12,13]
plt.pie(sizes, labels=labels, autopct='%1.0f%%')
plt.savefig(out / "image_chart.png")
print("image_chart.png generated. Expected Theta label: 12%")