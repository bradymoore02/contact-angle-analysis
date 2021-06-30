import os
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline as spline
import matplotlib.pyplot as plt
import math
# creates a dictionary with all available data for plotting
tests = {}
b =1
for path in os.walk(os.path.expanduser('~/Desktop/Lithium_Wetting/GF-Wetting')):
    if "output_byDrop.csv" in path[-1]:
        try:
            tests[path[0].split("GF-Wetting/")[1].split("/")[0]].append(f"{path[0]}/output_byDrop.csv")
        except KeyError:
            tests[path[0].split("GF-Wetting/")[1].split("/")[0]] = [f"{path[0]}/output_byDrop.csv"]
print(tests[list(tests.keys())[0]])

with open("/Users/bradymoore/Desktop/LaTex_file.tex",'w') as f:
    f.write(
    '''
    \documentclass{article}
    \\begin{document}
    \\begin{center}
    \\begin{tabular}{|c|c|}
    '''
    )
    f.write(
    f'''
    \hline
    Material & Average Contact Angle (195-355)\\\\
    \hline
    '''
    )
    for material in tests.keys():
        data = pd.DataFrame(columns=["Stage Temperature [C]","Stage Material","Overall Average","Overall Std."])
        for date in tests[material]:
            temp = pd.read_csv(date, usecols=[1,3,7,10])
            data = data.append(temp, ignore_index=True)
        for i in range(len(data["Stage Material"])):
            try:
                if math.isnan(data["Overall Average"][i]):
                    data.drop(i, inplace=True)
                    data.reset_index(inplace=True)
            except:
                pass
        x = []
        y = []
        for i in range(len(data["Overall Average"])):
            if data["Stage Temperature [C]"][i] < 355:
                print(data["Overall Average"][i])
                print(".")
                x.append(data["Stage Temperature [C]"][i])
                y.append(data["Overall Average"][i])
            else:
                print(x)

        plt.scatter(x,y)
        mean = np.mean(y)
        f.write(f'''
        {material} & {round(mean,1)} \\\\
        '''
        )


        plt.hlines(90,xmin=0,xmax=550,linestyles="dashed")
        plt.hlines(mean,xmin=0,xmax=550)
        plt.ylim(0,150)
        plt.xlim(0,500)
        plt.title(material)
        plt.show()
        


    f.write(
    '''
    \\hline
    \\end{tabular}
    \\end{center}
    \\end{document}
    '''
    )

os.chdir("../..")
os.system("pdflatex LaTex_file.tex")
os.system("open LaTex_file.pdf")
