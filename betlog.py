import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_theme()

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
df['ActualPayout'] = df['ActualPayout'].apply(pd.to_numeric, errors='coerce')
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

df['ROI'] = (df['ActualPayout']/df['Amount']).round(2)

df2 = pd.DataFrame()
#count1 = df['Result'].str.count("W").apply(pd.to_numeric, errors='coerce')
#count2 = df['Result'].str.count("L").apply(pd.to_numeric, errors='coerce')
#df2['Wins'] = df['Result'].value_counts()['W']
#df2['Losses'] = df['Result'].value_counts()['L']

#df2['Results'] = df.groupby('Result').transform('count')
print(df2)

#df2['GamblerZ'] = (df2['Wins'] - df2['Losses'])/(numpy.sqrt(df2['Wins'] + df2['Losses']))
#df2['GamblerZ'] = sqrt

# Calculate the occurrences of string W in column Wins
#df2['Wins'] = df['Result'].str.count('W').apply(pd.to_numeric, errors='coerce')
#df2['WinsTotal'] = df2.groupby('Wins').sum()

# Calculate the occurrences of string L in column Losses
#df2['Losses'] = df['Result'].str.count('L').apply(pd.to_numeric, errors='coerce')
#df2['LossesTotal'] = df2.groupby('Losses').sum()

# Create GamblerZ column using the provided formula
#df2['GamblerZ'] = (df2['Wins'] - df2['Losses']) / (np.sqrt(df2['Wins'] + df2['Losses']))
#df2['sqrt'] = (df2['WinsTotal'] - df2['LossesTotal'])/(np.sqrt(df2['WinsTotal'] + df2['LossesTotal']))



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

#with open('analytics.csv', 'w') as f:
#    pd.concat([df3, df4, df5, df6, df7, df8, df9, df10, df11, df12], axis=1).to_csv(f, index=False)

list_of_dfs = [df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]
with open('analytics.csv','w+') as f:
    for df in list_of_dfs:
        df.to_csv(f, index=False)
        f.write("\n")

