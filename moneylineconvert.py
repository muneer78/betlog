import pandas as pd

# Create a DataFrame with the specified columns
df = pd.DataFrame(columns=['GameNumber', 'Moneyline', 'Risk', 'Win', 'Return', 'Profit', 'MLRolloverOdds'])

# Populate the 'GameNumber' column with values 1 through 7
df['GameNumber'] = range(1, 7)

# Populate the 'Moneyline' column with specified values
moneyline_values = [-1500, -400, -350, -250, -150, -125]
df['Moneyline'] = moneyline_values

# Initialize the initial investment
initial_investment = 2.59

# Calculate winnings, return, profit, and cumulative ML rollover odds
for index, row in df.iterrows():
    if index == 0:
        df.at[index, 'Risk'] = initial_investment
    else:
        df.at[index, 'Risk'] = df.at[index-1, 'Return']

    if row['Moneyline'] < 0:
        df.at[index, 'Win'] = abs(df.at[index, 'Risk'] / (row['Moneyline'] / 100))
    else:
        df.at[index, 'Win'] = df.at[index, 'Risk'] * (row['Moneyline'] / 100)

    df.at[index, 'Return'] = df.at[index, 'Risk'] + df.at[index, 'Win']
    df.at[index, 'Profit'] = df.at[index, 'Return'] - initial_investment
    df.at[index, 'MLRolloverOdds'] = (df.at[index, 'Profit'] / initial_investment)*100

# Display the DataFrame with calculated columns
print(df)

df.to_csv('moneylineodds.csv', index=False)
