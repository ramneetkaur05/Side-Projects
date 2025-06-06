"""
Prices a gas storage contract using the estimated prices.

Params:
    - injection_dates, withdrawal_dates: lists of date strings e.g. ['2025-03-15']
    - injection_rate, withdrawal_rate: max gas volume per injection/withdrawal date
    - max_volume: max storage volume
    - storage_cost_per_unit: cost per unit volume stored per period

Returns:
    - total contract value (float)
"""
import pandas as pd
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from Nat_Gas_Est import estimate_price_interpolated

def price_storage_contract(
    injection_dates,
    withdrawal_dates,
    injection_rate,
    withdrawal_rate,
    max_volume,
    storage_cost_per_unit
):
    
    #combined sorted list of dates 
    all_dates = sorted(set(injection_dates + withdrawal_dates),key=lambda x: pd.to_datetime(x))

    current_volume = 0 # keeps track of how much gas is currently in te stprgae
    total_value = 0 #keeps track of total profit or loss so far

    for i, date_str in enumerate(all_dates):
        price = estimate_price_interpolated(date_str) #for the current date, the functn frind the price

        # if this is the date where you INJECT the gas
            #calc how much  can inject
            # inc stored gas vol.
            #subtract money from total_val
        if date_str in injection_dates:
            inject_volume = min(injection_rate, max_volume - current_volume)
            current_volume += inject_volume
            total_value -= inject_volume * price

        #if this is the date where you WITHDRAW gas
            #calc how much you can withdraw
            #dec. stored gas
            #add mney to totl val.
        if date_str in withdrawal_dates:
            withdraw_volume = min(withdrawal_rate, current_volume)
            current_volume -= withdraw_volume
            total_value += withdraw_volume * price

        if i < len(all_dates) - 1:
            total_value -= current_volume * storage_cost_per_unit
    return total_value



injection_dates = ['2025-03-15', '2025-07-10']
withdrawal_dates = ['2025-09-01']

contract_value = price_storage_contract(
    injection_dates,
    withdrawal_dates,
    injection_rate=100,
    withdrawal_rate=100,
    max_volume=200,
    storage_cost_per_unit=0.05
)

print(f"Estimated contract value: ${contract_value:.2f}")
