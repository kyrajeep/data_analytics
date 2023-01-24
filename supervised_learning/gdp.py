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
data = pd.DataFrame(data = data)
#data = data.astype(int)
data.rename(columns = {'GDP, current prices (Billions of U.S. dollars)':'GDP (billions USD)'}, inplace = True)
#print(data.columns)

#Clean out the columns that have no information
data = data.drop([i for i in range (196, 230)], axis = 0)
data = data.T
data = data.rename({'GDP (billions USD)':'Year'}, axis = 0)
data =data.iloc[1:,:].astype(int)

print(data.head)


# Make a smaller dataset with Zimbabwe
#zimbabwe = data[data["GDP (billions USD)"] == "Zimbabwe"]
#print(zimbabwe.iloc[:, [i for i in range(5,19)]], "Zimbabwe recorded their first significant GDP in 1990 with 10.144 billion USD")
#data = data.set_index('Countries')
#vietnam = data[data["GDP (billions USD)"] == "Vietnam"]
print(data.iloc[:, 2])
plt.plot(data.iloc[:, 0], data.iloc[:, 5])
plt.show()
'''
# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
ax.plot(x, x, label='linear')  # Plot some data on the axes.
ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
ax.plot(x, x**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend();  # Add a legend.

'''


model = linear_model.LinearRegression()


