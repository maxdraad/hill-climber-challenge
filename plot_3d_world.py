import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd

data = pd.read_csv("hillclimber.csv")

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_trisurf(data['x'], data['y'], data['z'], cmap=cm.coolwarm, linewidth=0, antialiased=False)
plt.show()