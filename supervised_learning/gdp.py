#cd import sklearn
import numpy as np
import pandas as pd

data = pd.read_csv('World GDP Dataset.csv')
data.rename(columns = {'GDP, current prices (Billions of U.S. dollars)':'GDP (billions USD)'}, inplace = True)
print(data.columns)

data1 = data.drop([i for i in range (196, 230)], axis = 0)
print(data1.head)
# a smaller dataset with Zimbabwe
zimbabwe = data1[data1["GDP (billions USD)"] == "Zimbabwe"]
print(zimbabwe.iloc[:, [i for i in range(5,19)]], "Zimbabwe recorded their first significant GDP in 1990 with 10.144 billion USD")
