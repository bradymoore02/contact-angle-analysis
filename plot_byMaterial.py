'''
This file plots contact angle vs stage temperature for a given substrate.
'''
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import datetime
import numpy as np

directory = "../GF-Wetting/YttriaCoatedSlide"
for dir, subdirs, files in os.walk(directory):
    if dir == directory:
        for subdir in subdirs:
            print(subdir)
            try:
                try:
                    data = data.append(pd.read_csv(f"{directory}/{subdir}/output_byDrop.csv"))
                except NameError:
                    data = pd.read_csv(f"{directory}/{subdir}/output_byDrop.csv")
            except FileNotFoundError:
                print("not found")
                pass
data.reset_index(inplace=True)
data = data.drop(0)
print(data)
drop = data["Drop Material"][1]
subs = data["Stage Material"][1]
date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
data.sort_values("Stage Temperature [C]", inplace=True)
fig, ax = plt.subplots()
ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"], marker = "s",
    yerr=data["Overall Std."], fmt="o", linewidth = 2, capsize=3)
ax.set_ylim(0)
plt.xlabel("Substrate Temperature [C]")
plt.ylabel("Average Contact Angle [Degrees]")
plt.title(f"{drop} Drop on {subs} {date} ")
ax.axhline(y=90, color='r', linestyle='--')
z = np.polyfit(data["Stage Temperature [C]"], data["Overall Average"], 1)
fit = np.poly1d(z)
ax.plot(data["Stage Temperature [C]"], fit(data["Stage Temperature [C]"]))
z = np.polyfit(data["Stage Temperature [C]"], data["Overall Average"], 2)
fit = np.poly1d(z)
ax.plot(data["Stage Temperature [C]"], fit(data["Stage Temperature [C]"]))
plt.show()


#add axis labels xxx
#markers on each point (square or x) xxx
#increase line width xxx
#add y error bars - way too small to see xxx
#add a horizontal dashed line at 90 Degrees xxx
#scatter plot xxx
