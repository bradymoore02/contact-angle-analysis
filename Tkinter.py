import tkinter as tk
import matplotlib.pyplot as plt
import os
from tkinter import filedialog
import sys
import pandas as pd
from datetime import datetime
import numpy as np

window = tk.Tk()
directory = ""
def choose_dir():
    directory = filedialog.askdirectory(initialdir=os.path.expanduser('~/Desktop/Lithium_Wetting'))

window.geometry('1000x700')
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)
window.columnconfigure(4, weight=1)


label = tk.Label(text="Contact Angle Graphing Interface", width=30, height=4, font=("Arial", 25))
label.grid(row = 0,columnspan=5, rowspan=2, sticky="N")


words = tk.Label(text="Have Fun Graphing!")
words.grid(column=0, row=1, columnspan=5)

#determines axes and other parameters from user input
def graph():
    words = tk.Label(text="Have Fun Graphing!")
    words.grid_remove()
    x = x_axis.get()
    y = y_axis.get()
    f = fit.get()
    m = material.get()
    if x != "" and y != "" and format.get() != "" and m!= "":
        if format.get() == "By_Image.csv":
            form = "By Image"
        else:
            form = "By Drop"
        words = tk.Label(text=f"Graphing {y} vs {x} {form} with a fit of degree {f}", width=100)
        words.grid(column=0, row=0, columnspan=4,rowspan=4)
        plot_it(x, y, form, f, m)
    else:
        words = tk.Label(text="Please choose an option from each column")
        words.grid(column=0, row=0, columnspan=4,rowspan=4)

#actually plots
def plot_it(x_ax, y_ax, by_, deg, subs):
    #load the data into a pandas dataframe
    print(os.walk(directory))
    try:
        for dir, subdirs, fil in os.walk(directory):
            if dir == directory:
                print(dir)
                for subdir in subdirs:
                    print(f"-{subdir}")
                    for dir2, subdirs2, files in ox.walk(f"directory/dubdir"):
                        for sub2 in subdirs2:
                            try:
                                try:
                                    data = data.append(pd.read_csv(f"{directory}/{subdir}/{sub2}/{by_}"))
                                except NameError:
                                    data = pd.read_csv(f"{directory}/{subdir}/{sub2}/{by_}")
                            except FileNotFoundError:
                                pass
    except FileNotFoundError:
        if messagebox.askquestion('No Data Found',
                                  'No data was found. '
                                  'Would you like to try another directory?') == 'no':
                                  sys.exit()
    #clean up the data a bit
    data.reset_index(inplace=True)
    data = data.drop(0)
    data.sort_values("Stage Temperature [C]", inplace=True)

    #plotting
    fig, ax = plt.subplots()
    if y_ax.contains("Average"):
        ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"], marker = "s",
            yerr=data["Overall Std."], fmt="o", linewidth = 2, capsize=3)
    ax.set_ylim(0)
    plt.xlabel(x_ax)
    plt.ylabel(y_ax)
    plt.title(f"Lithium Drops on {subs}")
    ax.axhline(y=90, color='r', linestyle='--')
    z = np.polyfit(data[x_ax], data[y_ax], f)
    fit = np.poly1d(z)
    ax.plot(data[x_ax], fit(data[y_ax]))
    plt.show()


#options for graphing below
#x axis options
axes1 = tk.Label(text="Choose x axis:",font=("Arial", 15))
x_axis = tk.StringVar()
r1 = tk.Radiobutton(window, text="Left Angle", value="Left Average", variable=x_axis)
r2 = tk.Radiobutton(window, text="Right Angle", value="Right Average", variable=x_axis)
r3 = tk.Radiobutton(window, text="Average Angle", value="Overall Average", variable=x_axis)
r4 = tk.Radiobutton(window, text="Temperature", value="Stage Temperature [C]", variable=x_axis)
r5 = tk.Radiobutton(window, text="Left Standard Deviation", value="Left std.", variable=x_axis)
r6 = tk.Radiobutton(window, text="Right Standard Deviation", value="Right std.", variable=x_axis)

#y axis options
axes2 = tk.Label(text="Choose y axis:",font=("Arial", 15))
y_axis = tk.StringVar()
r11 = tk.Radiobutton(window, text="Left Angle", value="Left Average", variable=y_axis)
r12 = tk.Radiobutton(window, text="Right Angle", value="Right Average", variable=y_axis)
r13 = tk.Radiobutton(window, text="Average Angle", value="Overall Average", variable=y_axis)
r14 = tk.Radiobutton(window, text="Temperature", value="Stage Temperature [C]", variable=y_axis)
r15 = tk.Radiobutton(window, text="Left Standard Deviation", value="Left std.", variable=y_axis)
r16 = tk.Radiobutton(window, text="Right Standard Deviation", value="Right std.", variable=y_axis)

#format options
formatlabel = tk.Label(text="Choose format:",font=("Arial", 15))
format = tk.StringVar()
r21 = tk.Radiobutton(window, text="By Image", value="By_Image.csv", variable=format)
r22 = tk.Radiobutton(window, text="By Drop", value="By_Drop.csv", variable=format)

#degree of fit
fitlabel = tk.Label(text="Degree of fit:",font=("Arial", 15))
fit = tk.StringVar()
degree_input = tk.Entry(window, width=5, textvariable=fit)

#Material
matlabel = tk.Label(text="Stage Material:",font=("Arial", 15))
material = tk.StringVar()
m1 = tk.Radiobutton(window, text="Bare Microscope Slide", value="BareMicroscopeSlide", variable=material)
m2 = tk.Radiobutton(window, text="Yttria", value="Yttria", variable=material)
m3 = tk.Radiobutton(window, text="All Materials", value="BareMircroscopeSlide/Yttria", variable=material)

#Put widgets in the window
axes1.grid(column=2, row=2)
r1.grid(column=2, sticky="W")
r2.grid(column=2, sticky="W")
r3.grid(column=2, sticky="W")
r4.grid(column=2, sticky="W")
r5.grid(column=2, sticky="W")
r6.grid(column=2, sticky="W")

axes2.grid(column=3, row=2)
r11.grid(column=3, row=3, sticky="W")
r12.grid(column=3, row=4, sticky="W")
r13.grid(column=3, row=5, sticky="W")
r14.grid(column=3, row=6, sticky="W")
r15.grid(column=3, row=7, sticky="W")
r16.grid(column=3, row=8, sticky="W")

formatlabel.grid(column=1, row=2)
r21.grid(column=1, row=3, sticky="W")
r22.grid(column=1, row=4, sticky="W")

fitlabel.grid(column=4, row=2)
degree_input.grid(column=4, row=3)

matlabel.grid(column=0, row=2)
m1.grid(column=0, row=3, sticky="W")
m2.grid(column=0, row=4, sticky="W")
m3.grid(column=0, row=5, sticky="W")
#choose a directory to find the data
button = tk.Button(
    command=choose_dir,
    text="Choose",
    width=25,
    height=3,
    fg="black"
)
button.grid(column=3,row=9)
#button widget to confirm choices and create graph
button = tk.Button(
    command=graph,
    text="Graph",
    width=25,
    height=5,
    fg="black"
)
button.grid(column=0, columnspan=5, row=10)
window.mainloop()
