#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post processing for contact angle analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # unused
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

tk.Tk().withdraw()
while True:
    directory = filedialog.askdirectory(initialdir=os.path.expanduser('~/Desktop/Lithium_Wetting/GF-Wetting'))
    try:
        droplets = pd.read_csv(f'{directory}/Results.csv', header=0, usecols=[1,6,7,14], names=["name", "left", "right", "area"])
        overview = pd.read_excel(f'{directory}/Overview.xlsx', header=0, usecols=[0,1,3,4,5,6], names=["Drop", "Time", "Material", "Drop_Material", "Image", "Temp"], converters={5:lambda x: round(float(x), 2)})
        break
    except FileNotFoundError:
        if messagebox.askquestion('No Data Found',
                                  'No data was found. '
                                  'Would you like to try another directory?') == 'no':
            sys.exit()




#correct the contact angles which are supplementary to the correct angle
droplets.right = 180 - droplets.right
droplets.left = 180 - droplets.left

#cleans up the file names by only keeping the image number
array = []
for cap in droplets.name:
    cap = str(cap).split('.')[0].split('-')[0].split('_')[-1]
    num = ""
    for i in cap: # you can also just put this straight in for n, cap in enumerate(droplets.name):
        if i.isnumeric(): # droplets.loc[n,'name'] = num
            num += i
    array.append(int(num))
droplets.name = array

#creates a new dataframe to store data in terms of each drop
by_image = pd.DataFrame(columns=["Image Number", "Drop #", "Stage Temperature [C]", "Stage Material", "Drop Material", "Left angle", "Right angle", "Area", "Time"])
#make image number first
for ind in range(len(overview)):
    for idx in range(len(droplets)):
        try:
            if overview.loc[ind, "Image"] <= droplets.loc[idx, "name"] and overview.loc[ind+1, "Image"] > droplets.loc[idx, "name"]:
                array = [droplets.loc[idx,"name"],overview.loc[ind,"Drop"],overview.loc[ind,"Temp"],overview.loc[ind,"Material"],overview.loc[ind,"Drop_Material"],droplets.loc[idx,"left"],droplets.loc[idx,"right"],droplets.loc[idx,"area"],overview.loc[ind,"Time"]]
                by_image.loc[idx] = array # .loc[ind] =
        except KeyError:
            if overview.Image[ind] <= droplets.name[idx]:
                array = [droplets.loc[idx,"name"],overview.loc[ind,"Drop"],overview.loc[ind,"Temp"], overview.loc[ind,"Material"], overview.loc[ind,"Drop_Material"], droplets.loc[idx,"left"], droplets.loc[idx,"right"],droplets.loc[idx,"area"],overview.loc[ind,"Time"]]
                by_image.loc[idx] = array
by_image.sort_values("Image Number", inplace=True)
by_image.to_csv(f"{directory}/output_byImage.csv", index=False)

by_drop = pd.DataFrame(columns=["Drop #", "Stage Temperature [C]", "Stage Material", "Drop Material", "Left Average", "Right Average", "Overall Average", "Area Average", "Left Std.", "Right std.","Overall Std.", "Area std", "Time"])
# dtypes to make output cleaner^^
for ind in overview.index:
    angles = []
    left = []
    right = []
    area = []
    for idx in droplets.index:
        try:
            if overview.loc[ind, "Image"] <= droplets.loc[idx, "name"] and overview.loc[ind+1, "Image"] > droplets.loc[idx, "name"]:
                angles.append(droplets.left[idx])
                angles.append(droplets.right[idx])
                left.append(droplets.left[idx])
                right.append(droplets.right[idx])
                area.append(droplets.area[idx])
        except KeyError:
            if overview.Image[ind] <= droplets.name[idx]:
                angles.append(droplets.left[idx])
                angles.append(droplets.right[idx])
                left.append(droplets.left[idx])
                right.append(droplets.right[idx])
                area.append(droplets.area[idx])
    array = [overview.Drop[ind],overview.Temp[ind],overview.loc[ind,"Material"],overview.loc[ind,"Drop_Material"],np.mean(left), np.mean(right), np.mean(angles), np.mean(area), np.std(left),np.std(right),np.std(angles),np.std(area)] # np.mean(angles) can be np.mean(left.extend(right)) and you don't need angles anymore
    array2 = []
    for x in array:
        date = overview.loc[ind,"Time"]
        try:
            x = round(float(x), 2)
            array2.append(x)
        except:
            array2.append(x)
    array2.append(date)
    by_drop.loc[len(by_drop.index)] = array2

by_drop[["Drop #"]] = by_drop[["Drop #"]].astype(int)
by_drop.to_csv(f"{directory}/output_byDrop.csv", index=False)
