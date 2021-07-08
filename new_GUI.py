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

def cube_root(t,a,b,c):
    return a*(t-b)**(1/3)+c



class MainApp(tk.Tk):
    def __init__(self):
        '''
        Initializes the tkinter window and creates the layout and buttons.
        '''

        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.title("Wetting Plots")
#        self.find_data()
        # decide plotting shapes and colors
        self.shapes = ['s','o','d','*','p','^','v','h','.','o','<','>','1','2','3','4','8']
        self.s = 0

        self.colors = []
        n = 3000
        for i in range(n):
            self.colors.append('#%06X' % randint(0, 0xFFFFFF))
        self.c = 0

        # creates frames
        self.plotting_frame = tk.Frame()
        self.plotting_frame.grid(row=0, column=1,sticky="news")
        self.analysis_frame = tk.Frame()
        self.analysis_frame.grid(row=0, column=0,sticky="news")

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
        self.allbtn = ttk.Button(self.analysis_frame, text="All data",command=self.load_all)
        self.allbtn.grid(row=1, column=0, sticky="ew")
        self.clearbtn = ttk.Button(self.analysis_frame, text="Clear plot", command=self.clear)
        self.clearbtn.grid(row=4, column=0, sticky="ew")
        self.savebtn = ttk.Button(self.analysis_frame, text="Save", command=self.save)
        self.savebtn.grid(row=5, column=0, sticky="ew")

    def find_data(self):
        # creates a dictionary with all available data for plotting
        self.tests = {}
        print("hi")
        for path in os.walk(os.path.expanduser('~/Desktop/CPMI/Lithium_Wetting/GF-Wetting')):
            if "output_byDrop.csv" in path[-1]:
                try:
                    self.tests[path[0].split("GF-Wetting/")[1].split("/")[0]].append(f"{path[0]}/output_byDrop.csv")
                except KeyError:
                    self.tests[path[0].split("GF-Wetting/")[1].split("/")[0]] = [f"{path[0]}/output_byDrop.csv"]

    def load_all(self):
        '''
        Plots all of the saved data at one time.
        '''
        self.find_data()
        for mat in self.tests.keys():
            for path in self.tests[mat]:
                data = pd.read_csv(path)
                try:
                    date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
                except ValueError:
                    date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                self.ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"],
                yerr=data["Overall Std."],fmt=self.shapes[self.s],c=self.colors[self.c],
                linewidth = 2, capsize=3, label=f"{data['Stage Material'][0]} on {date}")
                self.c += 1
                print(self.c)
#               self.s += 1
        plt.legend()
        self.ax.set_ylim(0)
        self.ax.axhline(y=90, color='r', linestyle='--')
        plt.xlabel("Substrate Temperature [\u2103]")
        plt.ylabel("Average Contact Angle [Degrees]")
        self.canvas.draw()


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

        print(tel)
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
        print(tel)

        # creates String variable and sets up option menu for selecting the material
        self.material = tk.StringVar()
        self.material.set(list(tel.keys())[0])

        ttk.OptionMenu(win, self.material, self.material.get(), *tel.keys()).grid(row=0,column=1,sticky='ew')

        # add done button
        ttk.Button(win, text="Done", command=lambda: self.plot_mat(self.material)).grid(row=3,column=0,columnspan=2,sticky='ew')

    def plot_mat(self, material):

        # closes the "load data" window
        for widget in self.winfo_children():
            if widget.winfo_class() == 'Toplevel':
                widget.destroy()

        sorted_index = np.argsort([int("".join(i.split('/')[-2].split('_'))) for  i in self.tests[material.get()]])
        x = []
        y = []
        for i in sorted_index:
            path = self.tests[material.get()][i]
            data = pd.read_csv(path)
            try:
                date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
            except ValueError:
                date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
            self.ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"],
            yerr=data["Overall Std."],fmt=self.shapes[self.s], linewidth = 2, capsize=3, label=f"{data['Stage Material'][0]} on {date}", ms=7, color=self.colors[self.c])
            x.extend(data["Stage Temperature [C]"])
            y.extend(data["Overall Average"])


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
        self.ax.set_ylim(0)
        self.ax.axhline(y=90, color='r', linestyle='--', lw=3)
        plt.xlabel("Substrate Temperature [\u2103]")
        plt.ylabel("Average Contact Angle [Degrees]")
        plt.title(f'{self.material.get()} Wetting')
        self.canvas.draw()
        self.s += 1

    def plot(self, date):

        self.find_data()
        # closes the "load data" window
        for widget in self.winfo_children():
            if widget.winfo_class() == 'Toplevel':
                widget.destroy()
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
        self.ax.axhline(y=90, color='r', linestyle='--')
        plt.xlabel("Substrate Temperature [\u2103]")
        plt.ylabel("Average Contact Angle [Degrees]")
        plt.title(f'{data["Stage Material"][0]} Contact angle vs Temperature')
        self.canvas.draw()



    def clear(self):
        self.ax.clear()
        self.c = 0
        self.s = 0
        self.canvas.draw()


    def on_closing(self):
        '''
        Closes out of app.
        '''
        self.quit()
        self.destroy()


    def save(self):
        print(self.tests[self.material.get()][0].split('output_byDrop')[0][0:-15])
        plt.savefig(f"{self.tests[self.material.get()][0].split('output_byDrop')[0][0:-12]}/{self.material.get()}", dpi=300)


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
