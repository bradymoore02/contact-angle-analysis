import os
import sys

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime
import numpy as np
from random import randint
from scipy.interpolate import UnivariateSpline as spline
import math
from scipy.optimize import curve_fit as cf
from scipy.signal import savgol_filter

'''
This file creates a GUI that enables the user to plot different combinations
of the wetting data saved to this computer.
'''
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 18}
matplotlib.rc('font', **font)


class MainApp(tk.Tk):
    def __init__(self):
        '''
        Initializes the tkinter window and creates the layout and buttons.
        '''

        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.title("Wetting Plots")
        self.colors = ["blue", "green","red","cyan","magenta","yellow","black","white"]
        self.c=0
        self.shapes = {"Square":'s',"Circle":'o',"Diamond":'d',"Star":'*',"Pentagon":'p',"Upwards Triangle":'^',"Downwards Triangle":'v'}
        #,'h','.','o','<','>','1','2','3','4','8'
        self.s = 0
        self.data_on_plot = False

        # creates frames
        self.plotting_frame = tk.Frame()
        self.plotting_frame.grid(row=0, column=1,sticky="news")
        self.analysis_frame = tk.Frame()
        self.analysis_frame.grid(row=0, column=0,sticky="news")
        self.style_frame = tk.Frame()
        self.style_frame.grid(row=0, column=2, sticky="news")

        # sets up plotting frame
        self.fig, self.ax = plt.subplots(1,figsize=[8,6])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotting_frame)
        self.canvas.draw()
        self.ax.clear()
        self.canvas.get_tk_widget().pack(expand=1, fill=tk.BOTH)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plotting_frame)
        self.toolbar.update()

        # label for directions
        ttk.Label(self.analysis_frame, text="Choose which data to plot:", anchor="center").grid(row=0,column=0)
        # buttons to choose data to plot
        self.matbtn = ttk.Button(self.analysis_frame,text="One material",command=self.load_mat)
        self.matbtn.grid(row=3, column=0,sticky="ew")
        self.daybtn = ttk.Button(self.analysis_frame,text="One day",command=self.load_day)
        self.daybtn.grid(row=2, column=0, sticky="ew")

        self.clearbtn = ttk.Button(self.analysis_frame, text="Clear plot", command=self.clear)
        self.clearbtn.grid(row=20, column=0, sticky="ew")
        self.savebtn = ttk.Button(self.analysis_frame, text="Save", command=self.save_window)
        self.savebtn.grid(row=21, column=0, sticky="ew")
        self.newdatabtn = ttk.Button(self.analysis_frame, text="New data", command=self.new_data)
        self.newdatabtn.grid(row=22, column=0, sticky="ew")

        ttk.Label(self.style_frame, text="Plot Title:", anchor="center").grid(row=0, column=0)
        self.title1 = tk.StringVar()
        self.title1.set("Untitled")
        ttk.Entry(self.style_frame, textvariable=self.title1, width=30).grid(row=1, column=0, sticky="ew")
        self.titlebtn = ttk.Button(self.style_frame, text="Update title", command=self.update_title)
        self.titlebtn.grid(row=2,column=0, sticky="ew")

    def new_data(self):
        os.system("python3 pre_processing.py")
        os.system("python3 post_processing.py")


    def find_data(self):
        # creates a dictionary with all available data for plotting
        self.tests = {}
        for path in os.walk(os.path.expanduser('~/Desktop/CPMI/Lithium_Wetting/GF-Wetting')):
            if "output_byDrop.csv" in path[-1]:
                try:
                    self.tests[path[0].split("GF-Wetting/")[1].split("/")[0]].append(f"{path[0]}/output_byDrop.csv")
                except KeyError:
                    self.tests[path[0].split("GF-Wetting/")[1].split("/")[0]] = [f"{path[0]}/output_byDrop.csv"]

    def load_day(self):
        '''
        Loads the data from one specific day of Testing.
        '''
        self.find_data()

        # create new selection window
        win = tk.Toplevel()
        win.geometry("400x150")
        win.title("Plot by Day")

        # add labels
        ttk.Label(win, text="Select Material: ").grid(row=0, column=0, sticky='ew')
        ttk.Label(win, text="Select Date(s): ").grid(row=1, column=0,sticky='ew')
        # creates a local variable so og dictionary is unchanged
        tel = self.tests

        # creates String variable and sets up option menu for selecting the material
        self.material = tk.StringVar()
        self.material.set(list(tel.keys())[0])
        self.material.trace('w', self.update_options)

        ttk.OptionMenu(win, self.material, self.material.get(), *tel.keys()).grid(row=0,column=1,sticky='ew')

        # creates a list of dates for the initial material
        self.dates = tel[self.material.get()]
        for i in range(len(self.dates)):
            self.dates[i] = self.dates[i].split('/output')[0].split('/')[-1]
        self.date = tk.StringVar()
        self.date.set(self.dates[0])
        self.datemenu = ttk.OptionMenu(win, self.date, self.date.get(), *self.dates)
        self.datemenu.grid(row=1,column=1,sticky='ew')

        # add done button
        ttk.Button(win, text="Done", command =lambda: self.plot(self.date)).grid(row=3,column=0,columnspan=2,sticky='ew')

    def update_options(self, *args):
        '''
        Updates the dates available for plotting when material selection changes.
        '''
        tel = self.tests

        try:
            self.dates = tel[self.material.get()]
            for i in range(len(self.dates)):
                self.dates[i] = self.dates[i].split('/output')[0].split('/')[-1]
            self.date.set(self.dates[0])
            self.datemenu.set_menu(self.date.get(), *self.dates)

        except:
            pass

    def load_mat(self):
        self.find_data()

        # create new selection window
        win = tk.Toplevel()
        win.geometry("400x150")
        win.title("Plot by Material")

        # add labels
        ttk.Label(win, text="Select Material: ").grid(row=0, column=0, sticky='ew')
        # creates a local variable so og dictionary is unchanged
        tel = self.tests
        ttk.Label(win, text="Legend entry: ").grid(row=3, column=0, sticky='ew')
        self.leg = tk.StringVar()
        ttk.Entry(win, textvariable=self.leg).grid(row=3, column=1, sticky='ew')
        # creates String variable and sets up option menu for selecting the material
        self.material = tk.StringVar()
        self.material.set(list(tel.keys())[0])
        self.material.trace('w', self.leg_set)
        ttk.OptionMenu(win, self.material, self.material.get(), *tel.keys()).grid(row=0,column=1,sticky='ew')

        # Sets up color and shape selection
        ttk.Label(win, text="Select color: ").grid(row=1, column=0, sticky='ew')
        self.color = tk.StringVar()
        self.color.set(self.colors[0])
        ttk.OptionMenu(win, self.color, self.color.get(), *self.colors).grid(row=1, column=1, sticky='ew')

        ttk.Label(win, text="Select shape: ").grid(row=2, column=0, sticky='ew')
        self.shape = tk.StringVar()
        self.shape.set(list(self.shapes.keys())[0])
        ttk.OptionMenu(win, self.shape, self.shape.get(), *self.shapes.keys()).grid(row=2, column=1, sticky='ew')

        # add done button
        ttk.Button(win, text="Done", command=lambda: self.plot_mat(self.material)).grid(row=4,column=0,columnspan=2,sticky='ew')


    def leg_set(self, *args):
        self.leg.set(self.material.get())


    def plot_mat(self, material):

        # closes the "load data" window
        self.exit_window()

        sorted_index = np.argsort([int("".join(i.split('/')[-2].split('_'))) for  i in self.tests[material.get()]])
        x = []
        y = []
        for i in sorted_index:
            path = self.tests[material.get()][i]
            try:
                data = data.append(pd.read_csv(path))
            except:
                data = pd.read_csv(path)
        data.reset_index(inplace=True)
        self.ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"],
        yerr=data["Overall Std."],fmt=self.shapes[self.shape.get()], c=self.color.get(),linewidth = 2, capsize=3, label=self.leg.get(), ms=6)
        x.extend(data["Stage Temperature [C]"])
        y.extend(data["Overall Average"])

        self.data_on_plot = True
        self.c += 1

        '''
        x = []
        y = []
        for line in self.ax.get_lines()[0:-1:3]:
            x.extend(line.get_xdata())
            y.extend(line.get_ydata())
        '''
        '''
        indices = np.argsort(x)
        x = np.array(x)[indices]
        y = np.array(y)[indices]
        angles = savgol_filter(y, 5, 2)
        self.ax.errorbar(x, angles)
        '''
        '''
        z = spline(x,y,k=2,s=1000)
        self.ax.plot(x, z(x))
        '''
        plt.legend()
        self.ax.set_ylim(0,141)
        self.ax.set_xlim(195,360)
        self.ax.axhline(y=90, color='k', linestyle='--', lw=3)
        plt.xlabel("Substrate Temperature [\u2103]")
        plt.ylabel("Average Contact Angle [Degrees]")
        self.update_title()
        self.canvas.draw()
        self.s += 1

    def plot(self, date):

        self.find_data()
        # closes the "load data" window
        self.exit_window()
        tests = self.tests
        for key in tests.keys():
            for path in tests[key]:
                if self.date.get() in path:
                    data = pd.read_csv(path)
                    try:
                        date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
                    except ValueError:
                        date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                    self.ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"],
                    yerr=data["Overall Std."],fmt='s', linewidth = 2, capsize=3, label=f"{data['Stage Material'][0]} on {date}")
        plt.legend()
        self.ax.set_ylim(0)
        self.ax.relim()
        self.ax.axhline(y=90, color='k', linestyle='--')
        plt.xlabel("Substrate Temperature [\u2103]")
        plt.ylabel("Average Contact Angle [Degrees]")
        plt.title(f'{data["Stage Material"][0]} Contact angle vs Temperature')
        self.canvas.draw()


    def update_title(self):
        plt.title(self.title1.get())
        self.canvas.draw()
    def clear(self):
        self.ax.clear()
        self.c = 0
        self.s = 0
        self.canvas.draw()
        self.data_on_plot = False


    def save_window(self):
        if self.data_on_plot:
            win = tk.Toplevel()
            win.geometry("500x150")
            win.title("Save")

            # Entry box for file name
            ttk.Label(win, text="Figure name:").grid(row=0, column=0, sticky='ew')
            self.name = tk.StringVar()
            self.name.set(self.tests[self.material.get()][0].split('/')[-3])
            ttk.Entry(win, textvariable=self.name).grid(row=0,column=1, columnspan=3,sticky="ew")

            # Entry box for file path
            ttk.Label(win, text="Select path:").grid(row=1, column=0, sticky='ew')
            self.save_path = tk.StringVar()
            self.save_path.set('/Users/bradymoore/Desktop/CPMI/Lithium_Wetting/GF-Wetting/')
            ttk.Entry(win, textvariable=self.save_path, width=60).grid(row=1, column=1)

            # Button to confirm choices
            self.save_final = ttk.Button(win, text="Save as", command=self.save)
            self.save_final.grid(row=2,column=0,sticky="ew")

            '''
            self.save_final["state"] = tk.DISABLED
            if self.name.get() != "" and self.save_path.get() != "":
                self.save_final["state"] = tk.NORMAL
            '''
        else:
            # Creates window letting user know that no data is plotted
            win = tk.Toplevel()
            win.geometry("200x75")
            win.title("No Data")
            ttk.Label(win, text="There is no data plotted").grid(row=0, column=0, sticky='ew')
            ttk.Button(win, text="Ok", command=self.exit_window).grid(row=1, column=0, sticky='ew')


    def save(self):
        # get rid of save as window
        self.exit_window()

        # save data to user-specified location
        plt.savefig(f'{self.save_path.get()}{self.name.get()}', dpi=300)


    def exit_window(self):
        for widget in self.winfo_children():
            if widget.winfo_class() == 'Toplevel':
                widget.destroy()


    def on_closing(self):
        '''
        Closes out of app.
        '''
        self.quit()
        self.destroy()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
