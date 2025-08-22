import pandas as pd
from scipy.interpolate import interp1d

# Assuming you have the data in a DataFrame called 'df'
data = {
    "Posted Spread": [
        2.5,
        3,
        2.5,
        3,
        2.5,
        3,
        3,
        3,
        3.5,
        3,
        3.5,
        3,
        3.5,
        7,
        6.5,
        7,
        6.5,
        7,
        7.5,
        7,
    ],
    "Bet Price": [
        -115,
        105,
        -120,
        100,
        -125,
        -105,
        -110,
        -115,
        105,
        -120,
        100,
        -125,
        -105,
        100,
        -115,
        -105,
        -120,
        -110,
        100,
        -115,
    ],
    "Implicit Spread": [
        2.625,
        2.625,
        2.75,
        2.75,
        2.875,
        2.875,
        3,
        3.125,
        3.125,
        3.25,
        3.25,
        3.375,
        3.375,
        6.75,
        6.75,
        6.875,
        6.875,
        7,
        7.25,
        7.375,
    ],
}

df = pd.DataFrame(data)

# Create a linear interpolation function based on the data
implicit_spread_interp = interp1d(
    df["Bet Price"], df["Implicit Spread"], kind="linear", fill_value="extrapolate"
)


# Function to calculate implicit spread for any spread and bet price
def calculate_implicit_spread(posted_spread, bet_price):
    implicit_spread = implicit_spread_interp(bet_price)
    return implicit_spread


# Example usage:
posted_spread = float(input("Enter the Posted Spread: "))
bet_price = float(input("Enter the Bet Price: "))
implicit_spread = calculate_implicit_spread(posted_spread, bet_price)

print(
    f"Implicit Spread for Posted Spread {posted_spread} and Bet Price {bet_price}: {implicit_spread}"
)
