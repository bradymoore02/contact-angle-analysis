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
    Material & Critical Wetting Temperature \\\\
    \hline
    '''
    )

    for material in tests.keys():
        data = pd.DataFrame(columns=["Stage Temperature [C]","Stage Material","Overall Average","Overall Std."])
        for date in tests[material]:
            temp = pd.read_csv(date, usecols=[1,3,7,10])
            data = data.append(temp, ignore_index=True)
        for i in range(len(data["Stage Material"])):
            print(data["Overall Average"][i])
            if math.isnan(data["Overall Average"][i]):
                data.drop(i, inplace=True)
                print("here")
        x = data["Stage Temperature [C]"]
        y = data["Overall Average"]
        indices = np.argsort(x)
        x = np.array(x)[indices]
        y = np.array(y)[indices]
        z = spline(x,y,k=2,s=1000)
        domain = np.linspace(x[0],x[-1],100)
        fit_y = z(domain)
        plt.scatter(x,y)
        plt.plot(domain,z(domain))
        if abs(fit_y[np.argmin(abs(fit_y-90))]-90) < 1:
            wet_temp = np.argmin(abs(fit_y-90))
            plt.vlines(domain[wet_temp],ymin=0,ymax=200)
            print(domain[wet_temp])
            f.write(f'''
            {material} & {domain[wet_temp]} \\\\
            '''
            )
        else:
            f.write(f'''
            {material} & {"Not Wet Yet"} \\\\
            '''
            )

        plt.hlines(90,xmin=0,xmax=400)
        plt.ylim(0)

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
