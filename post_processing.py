#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 08:05:11 2021

@author: bradymoore
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # unused

directory = ".."
#read in the overview file and save as a data frame
overview = pd.read_csv(f'{directory}/Overview.csv',header=0,usecols=[0,1,3,4,5,6], names=["Drop","Time","Material","Drop_Material","Image","Temp"],converters={6:lambda x: round(float(x), 2)}) # the standard is a , with one space after such as .csv', usecols
#read in the results file from FIJI and save as a data frame
droplets = pd.read_csv(f'{directory}/Results_combined.csv',header=0,usecols=[1,6,7,14], names=["name","left","right","area"])

#correct the contact angles which are supplementary to the correct angle
droplets.right = 180 - droplets.right
droplets.left = 180 - droplets.left

#assumes that all drops in the file have same properties
Drop_Material = overview.loc[1, "Drop_Material"]  # This assumption should be fine but is it really needed
Material = overview.loc[1, "Material"] # note you are actually taking the second element not the first
Time = str(overview.loc[1, "Time"]) # are you just trying to make it not a datetime object?
Date = Time.split(" ")[0]

#cleans up the file names by only keeping the image number
array = []
for cap in droplets.name:
    cap = cap.split('.')[0] # this fails with 'Image0243-1.tif' that occurs when doing multiple rounds in ImageJ
    num = "" # why not cap = cap.split('.')[0].split('-')[0]
    for i in cap: # you can also just put this straight in for n, cap in enumerate(droplets.name):
        if i.isnumeric(): # droplets.loc[n,'name'] = num
            num += i
    array.append(int(num))
droplets.name = array

#creates a new dataframe to store data in terms of each drop
drop_overview = pd.DataFrame(columns=["Drop #", "Image Number", "Stage Temperature [C]", "Left angle", "Right angle", "Area"])
#make image number first
for ind in overview.index: # probably change to in range(len(overview))
    for idx in droplets.index:
        try:
            if overview.loc[ind, "Image"] <= droplets.loc[idx, "name"] and overview.loc[ind+1, "Image"] > droplets.loc[idx, "name"]:
                array = [overview.loc[ind,"Drop"],droplets.loc[idx,"name"],overview.loc[ind,"Temp"],droplets.loc[idx,"left"], droplets.loc[idx,"right"],droplets.loc[idx,"area"]]
                drop_overview.loc[len(drop_overview.index)] = array # .loc[ind] = 
        except KeyError:
            if overview.Image[ind] <= droplets.name[idx]:
                array = [overview.loc[ind,"Drop"],droplets.loc[idx,"name"],overview.loc[ind,"Temp"],droplets.loc[idx,"left"], droplets.loc[idx,"right"],droplets.loc[idx,"area"]] # It may be better to write a function that grabs this info because it is confusing to the reader
                drop_overview.loc[len(drop_overview.index)] = array
drop_overview.to_csv(f"{directory}/output_byPicture.csv")

by_drop = pd.DataFrame(columns=["Drop #", "Stage Temperature [C]", "Left Average", "Right Average", "Overall Average", "Area Average", "Left Std.", "Right std.","Overall Std.", "Area std"])
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
    array = [overview.Drop[ind],overview.Temp[ind],np.mean(left), np.mean(right), np.mean(angles), np.mean(area), np.std(left),np.std(right),np.std(angles),np.std(area)] # np.mean(angles) can be np.mean(left.extend(right)) and you don't need angles anymore
    array2 = []
    for x in array:
        x = round(float(x), 2)
        array2.append(x)
    by_drop.loc[len(by_drop.index)] = array2
by_drop[["Drop #"]] = by_drop[["Drop #"]].astype(int)
by_drop.to_csv(f"{directory}/output_byDrop.csv")
print(by_drop)
#out.plot.scatter("Stage Temperature [K]", "Mean angle [Degrees]",yerr="Std. angle",title=f"{Drop_Material} Drop on {Material} Stage on {Date}  ")
