# Question: Can we predict the GDP of Zimbabwe in 2023 
# given the GDP of neighboring countries?
# Are they correlated? 
# How about for Canada and the US?

# Can try with data from the 1980's to predict 1990's.
from sklearn import linear_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('World GDP Dataset.csv')
data.rename(columns = {'GDP, current prices (Billions of U.S. dollars)':'GDP (billions USD)'}, inplace = True)
#print(data.columns)

#Clean out the columns that have no information
data = data.drop([i for i in range (196, 230)], axis = 0)
#print(data.head)

# Plot for all countries
plt.figure(); data.plot(style='k--', label='Series'); plt.legend()
plt.show()

# Make a smaller dataset with Zimbabwe
zimbabwe = data[data["GDP (billions USD)"] == "Zimbabwe"]
print(zimbabwe.iloc[:, [i for i in range(5,19)]], "Zimbabwe recorded their first significant GDP in 1990 with 10.144 billion USD")

model = linear_model.LinearRegression()


