# Converting Dates to proper datetime format
    # This script uses the Nat_Gas CSV file with 'Dates' and 'Prices' columns.

import pandas as pd

# Reload the CSV file
file_path = "JPMC Tasks/Nat_Gas.csv"
df = pd.read_csv(file_path)
df['Dates'] = pd.to_datetime(df['Dates'], format="%m/%d/%y")


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


#Extroplating data
    # Using linear regression model (oct 2024 - sept 2025)

from sklearn.linear_model import LinearRegression

#Preparing data
X = df[['DateNum']] #input = actual # of days since first date (2D)
y = df[['Prices']]

model = LinearRegression()
model.fit(X,y) # model can now predict gas proces based on a day Number

# prediction of next year
last_date = df['Dates'].max() # finds last date -> stores
future_dates = pd.date_range(
    start = last_date + pd.Timedelta(days=1), # starts in Oct 1 , 2024
    periods=365 #makes 365 future dates
)

# converting numbers for prediction
future_date_nums = (future_dates - df['Dates'].min()).days.values.reshape(-1,1)




# testing
test_dates = ["2021-03-15", "2022-07-10", "2023-12-01"]

for date in test_dates:
    price = estimate_price_interpolated(date)
    print(f"Estimated price on {date}: ${price:.2f}")