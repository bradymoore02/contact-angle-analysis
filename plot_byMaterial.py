'''
This file plots contact angle vs stage temperature for a given substrate.
'''
import matplotlib.pyplot as plt
from os import listdir, walk
import pandas as pd
from datetime import datetime

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

print(data.head())
drop = data["Drop Material"][0]
subs = data["Stage Material"][0]
date = datetime.strptime(data["Time"][0], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
data.sort_values("Stage Temperature [C]", inplace=True)
fig, ax = plt.subplots()
ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"], marker = "x",
    yerr=data["Overall Std."], fmt="o", linewidth = 2)
ax.set_ylim(0)
plt.xlabel("Substrate Temperature [C]")
plt.ylabel("Average Contact Angle [Degrees]")
plt.title(f"{drop} Drop on {subs} {date} ")
ax.axhline(y=90, color='r', linestyle='--')
plt.show()


#add axis labels xxx
#markers on each point (square or x) xxx
#increase line width xxx
#add y error bars - way too small to see xxx
#add a horizontal dashed line at 90 Degrees xxx
#scatter plot xxx
