import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


fig, ax = plt.subplots()
# creates a dictionary with all available data for plotting
tests = {}
for path in os.walk(os.path.expanduser('~/Desktop/CPMI/Lithium_Wetting/GF-Wetting')):
    if "output_byDrop.csv" in path[-1]:
        try:
            tests[path[0].split("GF-Wetting/")[1].split("/")[0]].append(f"{path[0]}/output_byDrop.csv")
        except KeyError:
            tests[path[0].split("GF-Wetting/")[1].split("/")[0]] = [f"{path[0]}/output_byDrop.csv"]
materials = tests.keys()
print(tests['304SS'])
for i in range(len(tests['304SS'])):
    data = pd.read_csv(tests['304SS'][i])
    try:
        date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    except ValueError:
        date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"],
                yerr=data["Overall Std."], fmt="x",linewidth = 2, capsize=3, label=f"Test {i+1} ({date})")
for i in range(len(tests['80Grit304SS'])):
    data = pd.read_csv(tests['304SS'][i])
    try:
        date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
    except ValueError:
        date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
    ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"],
                yerr=data["Overall Std."], fmt="x",linewidth = 2, capsize=3, label=f"Test {i+1} ({date})")
#fmt and c
ax.plot()
ax.hlines(90,0,450, linestyles="dashed", color="black")
plt.xlim(195,450)
plt.ylim(0)
plt.legend()
plt.title("304 Stainless Steel Wetting")
plt.show()
