'''
This file plots contact angle vs stage temperature for a given substrate.
'''
import matplotlib.pyplot as plt
from os import listdir, walk
import pandas as pd


directory = "../glass_slide"
for dir,subdirs,files in walk(directory):
    if dir == directory:
        for subdir in subdirs:
            try:
                try:
                    data = data.append(pd.read_csv(f"{directory}/{subdir}/output_byDrop.csv"))
                except NameError:
                    data = pd.read_csv(f"{directory}/{subdir}/output_byDrop.csv")
            except FileNotFoundError:
                pass

print(data)
data.sort_values("Stage Temperature [C]", inplace=True)
fig, ax = plt.subplots()
ax.scatter(data["Stage Temperature [C]"], data["Overall Average"])
ax.set_ylim(0)
plt.show()

#add axis labels
#markers on each point (square or x)
#increase line width
#add y error bars
#add a horizontal dashed line at 90 Degrees
#scatter plot
