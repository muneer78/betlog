import pandas as pd

# Assuming you have the data in a DataFrame called 'df'
data = {
    'Posted Spread': [2.5, 3, 2.5, 3, 2.5, 3, 3, 3, 3.5, 3, 3.5, 3, 3.5, 7, 6.5, 7, 6.5, 7, 7.5, 7],
    'Bet Price': [-115, 105, -120, 100, -125, -105, -110, -115, 105, -120, 100, -125, -105, 100, -115, -105, -120, -110, 100, -115],
    'Implicit Spread': [2.625, 2.625, 2.75, 2.75, 2.875, 2.875, 3, 3.125, 3.125, 3.25, 3.25, 3.375, 3.375, 6.75, 6.75, 6.875, 6.875, 7, 7.25, 7.375]
}

df = pd.DataFrame(data)

def lookup_nearest_implicit_spread(posted_spread, bet_price):
    # Calculate the absolute differences between the user inputs and the DataFrame values
    df['Absolute Difference'] = abs(df['Posted Spread'] - posted_spread) + abs(df['Bet Price'] - bet_price)

    # Find the row with the smallest absolute difference
    nearest_row = df.loc[df['Absolute Difference'].idxmin()]

    implicit_spread = nearest_row['Implicit Spread']
    return implicit_spread

# Get user inputs
posted_spread = float(input("Enter the Posted Spread: "))
bet_price = float(input("Enter the Bet Price: "))

implicit_spread = lookup_nearest_implicit_spread(posted_spread, bet_price)

print(f"Nearest Implicit Spread for Posted Spread {posted_spread} and Bet Price {bet_price}: {implicit_spread}")
