'''
File for processing the raw data output from the MCATS application.
This results in the 'Overview.xlsx' file that is needed for the
'post_processing.py' file.
'''

import os
import sys
import pickle
import datetime as dt
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d


def interpTC(location, time, pins, locs=[22, 66, 110]):
    '''
    Interpolate the stage temperature at drop location
    using linear interpolation/extrapolation
    '''
    vals = []
    for pin in pins:
        vals.append(data[pin]['data'][abs(data[pin]['time'] -
                                          (time-appstartdt).total_seconds()).argmin()])
    interp = interp1d(locs, vals, fill_value='extrapolate')
    return interp(location)

# Open Tkinter window and withdraw it so it doesn't appear on screen.
# Ask user to select directory and check whether data files are present.
# If not, prompt user to try again or end the program
tk.Tk().withdraw()
while True:
    directory = filedialog.askdirectory(initialdir=os.path.expanduser('~'))
    try:
        with open(f'{directory}/data-0.pkl', 'rb') as f:
            pickle.load(f)
        break
    except FileNotFoundError:
        if messagebox.askquestion('No Data Found',
                                  'No data was found. '
                                  'Would you like to try another directory?') == 'no':
            sys.exit()

# Read in all the data files in directory
Data = []
i = 0
while True:
    try:
        with open(f'{directory}/data-{i}.pkl', 'rb') as f:
            while True:
                try:
                    Data.append(pickle.load(f))
                except EOFError:
                    i += 1
                    break
    except FileNotFoundError:
        break

# Make a dictionary to combine all data files and
# give it all the appropriate keys
data = {}
for entry in Data:
    for key in entry.keys():
        if key not in data.keys():
            data[key] = {}
            data[key]['time'] = []
            data[key]['data'] = []
            data[key]['nickname'] = []
            data[key]['equation'] = []

# Add all the data to the data dictionary
for entry in Data:
    for key in entry:
        data[key]['time'].extend(entry[key]['time'])
        data[key]['data'].extend(entry[key]['data'])
        data[key]['nickname'].append(entry[key]['nickname'])
        data[key]['equation'].append(entry[key]['equation'])

# Read in log file and determine the start time of the application
with open(f'{directory}/log.log', 'r') as f:
    loglines = f.readlines()

for line in loglines:
    if 'Application Started' in line:
        appstart = float(line.split(' ')[-1])
        appstartdt = dt.datetime.strptime(line.split(' - ')[0], '%Y-%m-%d %H:%M:%S,%f')

# Convert data to appropriate data types and warning the user of issues
for key, value in data.items():
    value['time'] = np.array(value['time']) - appstart
    value['data'] = np.array(value['data'])
    if len(set(value['nickname'])) == 1:
        value['nickname'] = value['nickname'][-1]
    else:
        messagebox.showwarning('Multiple Names', f'{key} had '
                               'multiple names assigned in the data files.')
        value['nickname'] = value['nickname'][-1]
    if len(set(value['equation'])) == 1:
        value['equation'] = value['equation'][-1]
    else:
        messagebox.showwarning('Multiple Names', f'{key} had '
                               'multiple equations assigned in the data files.')
        value['equation'] = value['equation'][-1]

# Determine which LabJack pins were used for the pressure,
# stage temperature, and injector tip
stagePins = []
for key, value in data.items():
    if value['equation'] == 'FullRange':
        pressurePin = key
    if (value['equation'] == 'ToC') and ('Inj Tip' in value['nickname']):
        tipPin = key
    if (value['equation'] == 'ToC') and ('Stage' in value['nickname']):
        stagePins.append(key)

# Grab the info about each droplet from the log file.
#
# In order: droplet number, time of droplet placement,
# location of droplet, substrate material, droplet material
# image number starting images of droplet, stage temperature
# interpolated from location, injector tip temperature,
# chamber pressure
dropInfo = []
for line in loglines:
    if 'drop' in line:
        number = line.split('drop number ')[1].split(' ')[0]
        time = dt.datetime.strptime(line.split(' - ')[0], '%Y-%m-%d %H:%M:%S,%f')
        location = line.split('at ')[1].split(' mm')[0]
        substrate = line.split('on ')[1].split(' at')[0]
        dropMaterial = line.split(' INFO - ')[1].split(' drop')[0]
        imageStart = line.split('starting at ')[1].split(' and')[0]
        interpTemp = interpTC(int(location), time, stagePins)
        tipTemp = data[tipPin]['data'][abs(data[tipPin]['time'] -
                                           (time - appstartdt).total_seconds()).argmin()]
        pressure = data[pressurePin]['data'][abs(data[pressurePin]['time'] -
                                                 (time - appstartdt).total_seconds()).argmin()]
        try:
            dropInfo.append([int(number), time, int(location), substrate,
                         dropMaterial, int(imageStart), round(float(interpTemp), 2),
                         round(tipTemp, 2), float('{:.2e}'.format(pressure)),"None"])
        except ValueError:
            dropInfo.append([int(number), time, int(location), substrate,
                         dropMaterial, int(imageStart[0:5]), round(float(interpTemp), 2),
                         round(tipTemp, 2), float('{:.2e}'.format(pressure)),imageStart[21:-2]])


# Convert the droplet info into a Pandas DataFrame and write to Excel file
Drops = pd.DataFrame(dropInfo, columns=['Drop Number', 'Time', 'Drop Location',
                                        'Substrate Material', 'Drop Material',
                                        'Starting Image Number', 'Stage Temperature (degC)',
                                        'Injector Tip Temperature (degC)', 'Pressure (Torr)', 'Comments'])

Drops.to_excel(f'{os.path.split(directory)[0]}/Overview.xlsx', index=False)
