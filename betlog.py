import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()
import csv

df = pd.read_csv('bet.csv')
cols = ['Amount', 'Odds']
df[cols] = df[cols].astype('float').fillna(0)
df['Date'] = pd.to_datetime(arg=df['Date'],format='%m/%d/%Y')

df['CleanedOdds'] = df['Odds'].abs()

df['PotentialProfit'] = np.where(df['Odds'] > 0, ((df['CleanedOdds']/100)*df['Amount']), (100/(df['CleanedOdds'])*df['Amount'])).round(2)

cols2 = ['PotentialProfit','CleanedOdds']
df[cols2] = df[cols2].apply(pd.to_numeric, errors='coerce', axis=1)

df['PotentialPayout'] = df['PotentialProfit'] + df['Amount'].apply(pd.to_numeric, errors='coerce')
df['PotentialPayout'] = df['PotentialPayout'].round(2)

df['BreakEvenPercentage'] = np.where(df['Odds'] > 0, ((100 / (100 + df['CleanedOdds']))), ((df['CleanedOdds'])/(100+(df['CleanedOdds'])))).round(2)
df['BreakEvenPercentage'] = df['BreakEvenPercentage'].apply(pd.to_numeric, errors='coerce')

df['Expected Value'] = np.ceil(df['BreakEvenPercentage'] * df['Amount']) - ((1 - df['BreakEvenPercentage']) * df['Amount'])
df['Expected Value'] = df['Expected Value'].apply(pd.to_numeric, errors='coerce')
df['Expected Value'] = df['Expected Value'].round(2)

df['ActualPayout'] = np.nan
df['ActualPayout'] = df['ActualPayout'].apply(pd.to_numeric, errors='coerce')
df['ActualPayout'] = df['ActualPayout'].astype('float')

for i, row in df.iterrows():
    if row['Result'] == 'L' and row['FreeBet'] == 'N':
        df.at[i, 'ActualPayout'] = row['Amount'] * -1
    elif row['Result'] == 'L' and row['FreeBet'] == 'Y':
        df.at[i, 'ActualPayout'] = 0
    elif row['Result'] == 'W' and row['FreeBet'] == 'Y':
        df.at[i, 'ActualPayout'] = row['PotentialProfit']
    elif row['Result'] == 'W' and row['FreeBet'] == 'N':
        df.at[i, 'ActualPayout'] = row['PotentialPayout']
    elif row['Result'] == 'Pe':
        df.at[i, 'ActualPayout'] = 0
    elif row['Result'] == 'P':
        df.at[i, 'ActualPayout'] = row['PushAmount']

df['ROI'] = (df['ActualPayout']/df['Amount']*100).round(2)

substr1 = 'W'
wins = (df.Result.str.count(substr1).sum())

substr2 = 'L'
losses = (df.Result.str.count(substr2).sum())

squareroot = float((wins + losses) ** (1/2))

gamblerz = (wins - losses)/squareroot

# This line opens a file named "student.txt" in write mode (w)
file = open("gamblerz.txt", "w+")

# This line converts the "student" dictionary to a string using the str() function and writes it to the file
file.write(str(gamblerz))

# This line closes the "student.txt" file
file.close()

df3 = df.groupby(['Sportsbook'])['ActualPayout'].sum().reset_index().round(2)
df4 = df.groupby(['Sport'])['ActualPayout'].sum().reset_index().round(2)
df5 = df.groupby(['System'])['ActualPayout'].sum().reset_index().round(2)
df6 = df.groupby(['BetType'])['ActualPayout'].sum().reset_index().round(2)
df7 = df.groupby(df['Date'].dt.strftime('%Y-%m'))['ActualPayout'].sum().reset_index().round(2).sort_values(by=['Date'])
df8 = df.groupby(['FreeBet'])['ActualPayout'].sum().reset_index().round(2)
df9 = df.groupby(['FreeBet'])['Amount'].sum().reset_index().round(2)
df10 = df.groupby(['BetType'])['Amount'].sum().reset_index().round(2)
df11 = df.groupby(['Sport'])['Amount'].sum().reset_index().round(2)
df12 = df.groupby(['Sportsbook'])['Amount'].sum().reset_index().round(2)

df.to_csv('betlog.csv', index=False)

list_of_dfs = [df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]
with open('analytics.csv','w+') as f:
    for df in list_of_dfs:
        df.to_csv(f, index=False)
        f.write("\n")

