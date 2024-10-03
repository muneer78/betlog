import pandas as pd

df = pd.read_csv('bet.csv')
filtered_df = df[df['BetType'] == 'Futures']

filtered_df.to_csv('futures.csv', index=False)
