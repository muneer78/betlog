import pandas as pd
import numpy as np
import math

df = pd.read_csv('bet.csv')
cols = ['Amount', 'Odds']
df[cols] = df[cols].astype('float').fillna(0)
df['Date'] = pd.to_datetime(arg=df['Date'],format='%m/%d/%Y')


df['CleanedOdds'] = df['Odds'].abs()

df['Winnings'] = np.where(df['Odds'] > 0, ((df['CleanedOdds']/100)*df['Amount']), (100/(df['CleanedOdds'])*df['Amount'])).round(2)

cols2 = ['Winnings','CleanedOdds']
df[cols2] = df[cols2].apply(pd.to_numeric, errors='coerce', axis=1)

df['PotentialPayout'] = df['Winnings'] + df['Amount'].apply(pd.to_numeric, errors='coerce')
df['PotentialPayout'] = df['PotentialPayout'].round(2)

df['BreakEvenPercentage'] = np.where(df['Odds'] > 0, ((100 / (100 + df['CleanedOdds']))), ((df['CleanedOdds'])/(100+(df['CleanedOdds'])))).round(2)
df['BreakEvenPercentage'] = df['BreakEvenPercentage'].apply(pd.to_numeric, errors='coerce')

df['Expected Value'] = np.ceil(df['BreakEvenPercentage'] * df['Amount']) - ((1 - df['BreakEvenPercentage']) * df['Amount'])
df['Expected Value'] = df['Expected Value'].apply(pd.to_numeric, errors='coerce')
df['Expected Value'] = df['Expected Value'].round(2)

df['ActualPayout'] = np.nan
df['ActualPayout'] = df['ActualPayout'].astype('float')

for i, row in df.iterrows():
    if row['Result'] == 'L' and row['FreeBet'] == 'N':
        df.at[i, 'ActualPayout'] = 0 - row['Amount']
    elif row['Result'] == 'L' and row['FreeBet'] == 'Y':
        df.at[i, 'ActualPayout'] = 0
    elif row['Result'] == 'W' and row['FreeBet'] == 'Y':
        df.at[i, 'ActualPayout'] = row['Winnings']
    elif row['Result'] == 'W' and row['FreeBet'] == 'N':
        df.at[i, 'ActualPayout'] = row['PotentialPayout']
    elif row['Result'] == 'Pe':
        df.at[i, 'ActualPayout'] = 0
    elif row['Result'] == 'P':
        df.at[i, 'ActualPayout'] = row['PushAmount']

df3 = df.groupby(['Sportsbook'])['ActualPayout'].sum().reset_index()
df4 = df.groupby(['Sport'])['ActualPayout'].sum().reset_index()
df5 = df.groupby(['System'])['ActualPayout'].sum().reset_index()
df6 = df.groupby(['BetType'])['ActualPayout'].sum().reset_index()
df7 = df.groupby(df['Date'].dt.strftime('%B %Y'))['ActualPayout'].sum().sort_values()

print(df.head)

print(df3)
print(df4)
print(df5)
print(df6)
print(df7)

df.to_csv('betlog.csv')