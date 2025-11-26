import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

out = Path.cwd()
np.random.seed(4)
x = np.random.normal(size=50000)
y = np.random.normal(size=50000)
plt.hexbin(x,y,gridsize=100, cmap='inferno', vmin=0, vmax=1)
cb = plt.colorbar()
cb.set_label("intensity")
cb.set_ticks([0, 0.5, 1.0])
plt.savefig(out / "complex_plot.png")
print("complex_plot.png generated. Expected colorbar max label: 1.0")