import pandas as pd
import numpy as np

df = pd.read_csv('bet.csv')
cols = ['Amount','Odds']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
#df = df.rename(columns = {'Win/Loss':'WinLoss'})
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
df['ActualPayout'] = df['ActualPayout'].astype('float64')

#mask1 = (df["Result"] == "W")
#df.loc[mask1, 'ActualPayout'] = df.loc[mask1, 'PotentialPayout']

#mask2 = ((df['FreeBet'] == 'Y') & (df['Result'] == 'W'))
#df.loc[mask2, 'ActualPayout'] =df.loc[mask3, 'ActualPayout'] = df.loc[mask3, 'PushAmount']
#df.loc[mask2, 'Winnings']

#mask3 = (df["Result"] == "P")

#mask4 = ((df['FreeBet'] == 'Y') & (df['Result'] == 'L'))

#cond = ((df["Result"] == "L") and (df['FreeBet'] == 'Y'))
#df.loc[cond, "ActualPayout"] = 0
#df.loc[df["Result"] == "0", "ActualPayout"] = 0

# create a conditional filter for the desired rows
filter_1 = (df['Result'] == 'L') & (df['FreeBet'] == 'N')
filter_2 = (df['Result'] == 'L') & (df['FreeBet'] == 'Y')
filter_3 = (df['Result'] == 'W') & (df['FreeBet'] == 'Y')
filter_4 = (df['Result'] == 'W') & (df['FreeBet'] == 'N')
filter_5 = (df['Result'] == 'Pe')

# apply the filter using .loc function
df.loc[filter_1, 'Actual Payout'] = df.loc[filter_1]['Wager'] * (-1)
df.loc[filter_2, 'Actual Payout'] = 0
df.loc[filter_3, 'Actual Payout'] = df.loc[filter_3]['Winnings']
df.loc[filter_4, 'Actual Payout'] = df.loc[filter_4]['PotentialPayout']
df.loc[filter_5, 'Actual Payout'] = 0

df3 = df.groupby(['Sportsbook'])['ActualPayout'].sum().reset_index()
df4 = df.groupby(['Sport'])['ActualPayout'].sum().reset_index()
df5 = df.groupby(['System'])['ActualPayout'].sum().reset_index()
df6 = df.groupby(['BetType'])['ActualPayout'].sum().reset_index()
df7 = df.groupby(df['Date'].dt.strftime('%B %Y'))['ActualPayout'].sum().sort_values()