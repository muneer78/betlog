import pandas as pd
import numpy as np
import seaborn as sns; sns.set_theme()

df = pd.read_csv('bet.csv')
cols = ['Amount', 'Odds']
df[cols] = df[cols].astype('float').fillna(0)
df['Date'] = pd.to_datetime(arg=df['Date'],format='%m/%d/%Y')

df['CleanedOdds'] = df['Odds'].abs()

df['PotentialProfit'] = np.where(df['Odds'] > 0, ((df['CleanedOdds'] / 100) * df['Amount']), (100 / df['CleanedOdds']) * df['Amount'])
df['PotentialProfit'] = df['PotentialProfit'].round(2)

cols2 = ['PotentialProfit','CleanedOdds']
df[cols2] = df[cols2].apply(pd.to_numeric, errors='coerce', axis=1)

df['PotentialPayout'] = df['PotentialProfit'] + df['Amount'].apply(pd.to_numeric, errors='coerce')
df['PotentialPayout'] = df['PotentialPayout'].round(2)

df['ImpliedProbability'] = np.where(df['Odds'] > 0, ((100 / (100 + df['CleanedOdds']))), ((df['CleanedOdds'])/(100+(df['CleanedOdds'])))).round(2)

df['Expected Value'] = np.ceil(df['ImpliedProbability'] * df['Amount']) - ((1 - df['ImpliedProbability']) * df['Amount'])
df['Expected Value'] = df['Expected Value'].apply(pd.to_numeric, errors='coerce')
df['Expected Value'] = df['Expected Value'].round(2)

df['ImpliedProbability'] = (df['ImpliedProbability']*100).apply(pd.to_numeric, errors='coerce')
df['ImpliedProbability'] = (df['ImpliedProbability']).round(2)

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

df_copy = df.copy()

currency_columns = ['Amount', 'PushAmount', 'PotentialProfit', 'PotentialPayout', 'Expected Value', 'ActualPayout']
for col in currency_columns:
    df_copy[col] = df_copy[col].apply(lambda x: "${:,.2f}".format(x) if pd.notnull(x) else '')

df_copy.to_csv('betlog.csv', index=False)

df3 = df[["Sport", "Amount", "ActualPayout"]]
df3 = df3.groupby("Sport").sum().reset_index()
df3["ROI"] = df3["ActualPayout"] / df3["Amount"]
df3["ROI"] = (df3["ROI"] * 100).round(2)
df3 = df3.reindex(columns=["Sport", "ActualPayout", "Amount", "ROI"]).round(2)

df4 = df.groupby(['Sport'])['ActualPayout'].sum().reset_index().round(2)
df5 = df.groupby(['Sport'])['Amount'].sum().reset_index().round(2)
df6 = df.groupby(df['Date'].dt.strftime('%Y-%m'))['ActualPayout'].sum().reset_index().round(2).sort_values(by=['Date'])
df7 = df.groupby(['Sportsbook'])['ActualPayout'].sum().reset_index().round(2)
df8 = df.groupby(['Sportsbook'])['Amount'].sum().reset_index().round(2)
df9 = df.groupby(['System'])['ActualPayout'].sum().reset_index().round(2)
df10 = df.groupby(['BetType'])['ActualPayout'].sum().reset_index().round(2)
df11 = df.groupby(['BetType'])['Amount'].sum().reset_index().round(2)
df12 = df.groupby(['FreeBet'])['ActualPayout'].sum().reset_index().round(2)
df13 = df.groupby(['FreeBet'])['Amount'].sum().reset_index().round(2)

# Sum column values for A, B and C
sum_a = df['ActualPayout'].sum()
sum_b = df['Amount'].sum()

# Write only the sums to new data frame
df14 = pd.DataFrame({'TotalWon':sum_a, 'TotalRisked':sum_b}, index=[0])
columns = ['TotalWon', 'TotalRisked']
df14[columns] = df14[columns].round(2)

# Divide sum of A by sum of B
df14['TotalROI'] = (df14['TotalWon'] / df14['TotalRisked'] * 100).round(2)

substr1 = 'W'
wins = (df.Result.str.count(substr1).sum())

substr2 = 'L'
losses = (df.Result.str.count(substr2).sum())

squareroot = np.sqrt((wins + losses))

df15 = pd.DataFrame({'TotalBetsWon': wins, 'TotalBetsLost': losses}, index=[0])

gamblerz = (wins - losses)/squareroot
df15['gamblerzscore'] = gamblerz.round(2)
winning_pct = (wins / (wins + losses)) *100
df15['winning_pct'] = winning_pct.round(2)

list_of_dfs = [df3, df4, df5, df6, df7, df8, df9, df10, df11, df14, df15, df12, df13]
for df in list_of_dfs:
    df.rename(columns={'Amount': 'MoneyRisked', 'ActualPayout': 'Profit',}, inplace=True)
    try:
        df["Profit"] = df["Profit"].astype (float).map ("${:,.2f}".format)
        df["MoneyRisked"] = df["MoneyRisked"].astype (float).map ("${:,.2f}".format)
        df["TotalWon"] = df["TotalWon"].astype (float).map ("${:,.2f}".format)
        df["TotalRisked"] = df["TotalRisked"].astype (float).map ("${:,.2f}".format)
    except KeyError:
        pass

titles = ["ROI By Sport", "Profit by Sport", "Risk by Sport", "Profit by Month", "Profit by Sportsbook", "Risk by Sportsbook", "Profit by System", "Profit by Bet Type", "Risk by Bet Type", "Total ROI", "Total Win Percentage", "Profit by Free Bet vs. Money Bet", "Risk by Free Bet vs. Money Bet"]

with open('analytics.csv', 'w+') as f:
    for i, df in enumerate(list_of_dfs):
        f.write(titles[i] + "\n")  # Write the title
        df.to_csv(f, index=False)
        f.write("\n")