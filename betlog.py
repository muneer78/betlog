import pandas as pd
import numpy as np

df = pd.read_csv('bet.csv')
cols = ['Amount','Odds']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
df['Date'] = pd.to_datetime(arg=df['Date'],format='%m/%d/%Y')

df['CleanedOdds'] = df['Odds'].abs()

df['Winnings'] = np.where(df['Odds'] > 0, ((df['CleanedOdds']/100)*df['Amount']), (100/(df['CleanedOdds'])*df['Amount'])).round(2)

cols2 = ['Winnings','CleanedOdds']
df[cols2] = df[cols2].apply(pd.to_numeric, errors='coerce', axis=1)

df['PotentialPayout'] = df['Winnings'] + df['Amount'].apply(pd.to_numeric, errors='coerce')

df['Break Even Percentage'] = np.where(df['Odds'] > 0, ((100 / (100 + df['CleanedOdds'])*100)), ((df['CleanedOdds'])/(100+(df['CleanedOdds'])))*100).round(2)
df['Break Even Percentage'] = df['Break Even Percentage'].apply(pd.to_numeric, errors='coerce')
df = df.fillna('')

df['ActualPayout'] = np.nan
df['ActualPayout'] = np.where((df['Result'] == 'L'), 0, df['PotentialPayout'])
df['ActualPayout'] = np.where((df['Result'].empty, 0, df['PotentialPayout']))
df['ActualPayout'] = np.where((df['FreeBet'] == 'Yes') & (df['Result'] == 'W'), df['Winnings'], df['ActualPayout'])
#df['ActualPayout'] = np.where((df['FreeBet'] == 'Yes') & (df['WinLoss'] == 'W'), df['Winnings'], df['ActualPayout'])
#df['ActualPayout'] = np.where((df['WinLoss'] == 'L'), 0, df['PotentialPayout'])

df3 = df.groupby(['Sportsbook'])['ActualPayout'].sum().reset_index()
df4 = df.groupby(['Sport'])['ActualPayout'].sum().reset_index()
df5 = df.groupby(['System'])['ActualPayout'].sum().reset_index()
df6 = df.groupby(['BetType'])['ActualPayout'].sum().reset_index()
df7 = df.groupby(df['Date'].dt.strftime('%B %Y'))['ActualPayout'].sum().sort_values()

df.to_csv('betlog.csv')