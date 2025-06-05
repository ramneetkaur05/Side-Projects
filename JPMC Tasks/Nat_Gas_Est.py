# Converting Dates to proper datetime format and plotting natural gas prices
# This script uses the Nat_Gas CSV file with 'Dates' and 'Prices' columns.

import pandas as pd
import matplotlib.pyplot as plt  # this is the graphing tool

# Reload the CSV file
file_path = "JPMC Tasks/Nat_Gas.csv"
df = pd.read_csv(file_path)

df['Dates'] = pd.to_datetime(df['Dates'], format="%m/%d/%y")

plt.figure(figsize=(10, 5))  # make the plot big
plt.plot(df['Dates'], df['Prices'], marker='o')  # draw the line with dots on each point
plt.title("Natural Gas Prices Over Time")  # add a title
plt.xlabel("Date")  # label the X-axis
plt.ylabel("Price")  # label the Y-axis
plt.grid(True)  # add gridlines to help see the values
plt.show()  # show the graph

#INterpolating data

from scipy.interpolate import interp1d
import numpy as np

# Step 1: Convert dates to numerical values (number of days since the first date)
df['DateNum'] = (df['Dates'] - df['Dates'].min()).dt.days

# Step 2: Create interpolation function
interpolator = interp1d(df['DateNum'], df['Prices'], kind='linear', fill_value="extrapolate")

# Step 3: Define a function to estimate price on any given date (within known range)
def estimate_price_interpolated(date_str):
    date = pd.to_datetime(date_str)
    date_num = (date - df['Dates'].min()).days
    return float(interpolator(date_num))