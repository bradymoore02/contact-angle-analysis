import os
import sys

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime
import numpy as np

'''
This file creates a GUI that enables the user to plot different combinations
of the wetting data saved to this computer.
'''

class MainApp(tk.Tk):
    def __init__(self):
        '''
        Initializes the tkinter window and creates the layout and buttons.
        '''
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.title("Wetting Plots")

        # creates frames
        self.plotting_frame = tk.Frame()
        self.plotting_frame.grid(row=0, column=1,sticky="news")
        self.analysis_frame = tk.Frame()
        self.analysis_frame.grid(row=0, column=0,sticky="news")

        # sets up plotting frame
        self.fig, self.ax = plt.subplots(1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plotting_frame)
        self.canvas.draw()
        self.ax.clear()
        self.canvas.get_tk_widget().pack(expand=1, fill=tk.BOTH)

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

    def find_data(self):
        # creates a dictionary with all available data for plotting
        self.tests = {}
        for path in os.walk(os.path.expanduser('~/Desktop/Lithium_Wetting/GF-Wetting')):
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
            print(mat)
            for path in self.tests[mat]:
                print(f'-{path}')
                data = pd.read_csv(path)
                try:
                    date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S.%f').strftime('%m/%d/%Y')
                except ValueError:
                    date = datetime.strptime(data["Time"][1], '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%Y')
                self.ax.errorbar(data["Stage Temperature [C]"], data["Overall Average"],
                yerr=data["Overall Std."],fmt='s', linewidth = 2, capsize=3, label=f"{data['Stage Material'][0]} on {date}")
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
        # disable analysis buttons
        self.matbtn["state"] = tk.DISABLED
        self.daybtn["state"] = tk.DISABLED
        self.allbtn["state"] = tk.DISABLED

        # create new selection window
        win = tk.Toplevel()
        win.geometry("400x150")
        win.title("Plot by Day")

        # add labels
        ttk.Label(win, text="Select Material: ").grid(row=0, column=0, sticky='ew')
        ttk.Label(win, text="Select Date(s): ").grid(row=1, column=0,sticky='ew')
        # creates a local variable so og dictionary is unchanged
        tel = self.tests
        print(f'0{self.tests}')

        # creates String variable and sets up option menu for selecting the material
        self.material = tk.StringVar()
        self.material.set(list(tel.keys())[0])
        self.material.trace('w', self.update_options)

        ttk.OptionMenu(win, self.material, self.material.get(), *tel.keys()).grid(row=0,column=1,sticky='ew')
        print(f'1{self.tests}')

        # creates a list of dates for the initial material
        self.dates = tel[self.material.get()]
        for i in range(len(self.dates)):
            self.dates[i] = self.dates[i].split('/output')[0].split('/')[-1]
        self.date = tk.StringVar()
        self.date.set(self.dates[0])
        self.datemenu = ttk.OptionMenu(win, self.date, self.date.get(), *self.dates)
        self.datemenu.grid(row=1,column=1,sticky='ew')
        print(f'2{self.tests}')

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
            print(f'3{self.tests}')
            self.date.set(self.dates[0])
            self.datemenu.set_menu(self.date.get(), *self.dates)

        except:
            pass

    def load_mat(self):
        pass

    def plot(self, date):
        # enable analysis buttons
        self.matbtn["state"] = tk.NORMAL
        self.daybtn["state"] = tk.NORMAL
        self.allbtn["state"] = tk.NORMAL

        self.find_data()
        # closes the "load data" window
        for widget in self.winfo_children():
            if widget.winfo_class() == 'Toplevel':
                widget.destroy()
        print(self.tests)
        tests = self.tests
        for key in tests.keys():
            print(key)
            for path in tests[key]:
                print(path)
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
        self.ax.axhline(y=90, color='r', linestyle='--')
        plt.xlabel("Substrate Temperature [\u2103]")
        plt.ylabel("Average Contact Angle [Degrees]")
        self.canvas.draw()



    def clear(self):
        self.ax.clear()
        self.canvas.draw()
        # enable analysis buttons
        self.matbtn["state"] = tk.NORMAL
        self.daybtn["state"] = tk.NORMAL
        self.allbtn["state"] = tk.NORMAL

    def on_closing(self):
        '''
        Closes out of app.
        '''
        self.quit()
        self.destroy()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
