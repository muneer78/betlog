import pandas as pd
import numpy as np
import seaborn as sns; sns.set_theme()
import csv
import scipy
from scipy.stats import norm


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

# squareroot = float((wins + losses) ** (1/2))
squareroot = np.sqrt((wins + losses))

gamblerz = (wins - losses)/squareroot
gamblerz = gamblerz.round(2)
gamblerz_str = str(gamblerz)
p_value = scipy.stats.norm.sf(abs(gamblerz))
p_value = p_value.round(2)
p_value_str = str(p_value)
winning_pct = (wins / (wins + losses)) *100
winning_pct = winning_pct.round(2)
win_pct_str = str(winning_pct)

# This line opens a file named "student.txt" in write mode (w)
file = open("gamblerz.txt", "w+")

# This line converts the variables to a string using the str() function and writes it to the file
file.write(str("Your Gambler Z-Score is " + gamblerz_str + "\n"))
file.write(str("Your winning percentage is " + win_pct_str + "%" + "\n"))

# This line closes the "student.txt" file
file.close()

df.to_csv('betlog.csv', index=False)

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

# Sum column values for A, B and C
sum_a = df['ActualPayout'].sum()
sum_b = df['Amount'].sum()

# Write only the sums to new data frame
df13 = pd.DataFrame({'TotalWon':sum_a, 'TotalRisked':sum_b}, index=[0])

# Set the index of the new DataFrame
# df13.index = [0,1,2]

# Divide sum of A by sum of B
df13['TotalROI'] = (df13['TotalWon'] / df13['TotalRisked'] * 100).round(2)

for df in [df9, df10, df11, df12]:
    df.rename(columns={'Amount': 'MoneyRisked'}, inplace=True)

list_of_dfs = [df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13]
with open('analytics.csv','w+') as f:
    for df in list_of_dfs:
        df.to_csv(f, index=False)
        f.write("\n")

