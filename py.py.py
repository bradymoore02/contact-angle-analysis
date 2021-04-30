import pandas as pd


directory = "../Pre-Processed_Images"
overview = pd.read_excel(f'{directory}/Overview.xlsx', header=0, usecols=[0,1,3,4,5,6], names=["Drop","Time","Material","Drop_Material","Image","Temp"], converters={5:(lambda x: round(float(x), 2))}) # the standard is a , with one space after such as .csv', usecols
print(overview)
#, header=0, usecols=[0,1,3,4,5,6], names=["Drop","Time","Material","Drop_Material","Image","Temp"], converters={6:lambda x: round(float(x), 2)}
