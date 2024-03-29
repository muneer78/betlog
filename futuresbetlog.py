import numpy as np
import pandas as pd

# Define the data types you want to assign to specific columns
dtype_dict = {
    'Amount': float,
    'Odds': float,
    'CleanedOdds': float,
    'PotentialProfit': float,
    'PotentialPayout': float,
    'ImpliedProbability': float,
    'Expected Value': float,
    'ActualPayout': float,
}

# Read the CSV file and parse the 'Date' column as datetime
df = pd.read_csv('futures.csv', dtype=dtype_dict)

# Format the 'Date' column as '%m/%d/%Y'
df['Date'] = pd.to_datetime(arg=df['Date'], format='%Y-%m-%d')

df['CleanedOdds'] = df['Odds'].abs()

df['PotentialProfit'] = np.where(
    df['Odds'] > 0,
    ((df['CleanedOdds'] / 100) * df['Amount']),
    (100 / df['CleanedOdds']) * df['Amount'])
df['PotentialProfit'] = df['PotentialProfit'].round(2)

cols2 = ['PotentialProfit', 'CleanedOdds']
df[cols2] = df[cols2].apply(pd.to_numeric, errors='coerce', axis=1)

df['PotentialPayout'] = df['PotentialProfit'] + \
    df['Amount'].apply(pd.to_numeric, errors='coerce')
for i, row in df.iterrows():
    if row['FreeBet'] == 'N':
        df.at[i, 'PotentialPayout'] = row['PotentialPayout']
    elif row['FreeBet'] == 'Y':
        df.at[i, 'PotentialPayout'] = row['PotentialProfit']
df['PotentialPayout'] = df['PotentialPayout'].round(2)

df['ImpliedProbability'] = np.where(df['Odds'] > 0,
                                    (100 / (100 + df['CleanedOdds'])),
                                    ((df['CleanedOdds']) / (100 + (df['CleanedOdds'])))).round(2)

df['Expected Value'] = np.ceil(df['ImpliedProbability'] * df['Amount']) - (
    (1 - df['ImpliedProbability']) * df['Amount'])
df['Expected Value'] = df['Expected Value'].apply(
    pd.to_numeric, errors='coerce')
df['Expected Value'] = df['Expected Value'].round(2)

df['ImpliedProbability'] = (
    df['ImpliedProbability'] *
    100).apply(
        pd.to_numeric,
    errors='coerce')
df['ImpliedProbability'] = (df['ImpliedProbability']).round(2)

df['ActualPayout'] = 0
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
    elif row['Result'] == 'P':
        df.at[i, 'ActualPayout'] = 0
    elif row['Result'] == 'C':
        df.at[i, 'ActualPayout'] = row['PushAmount']

for i, row in df.iterrows():
    if row['Date'] == pd.to_datetime('2023-05-29'):
        df.at[i, 'ActualPayout'] = row['PotentialPayout']

df.to_csv('betbuilddata.csv',index=False)

df_copy = df.copy()

currency_columns = [
    'Amount',
    'PushAmount',
    'PotentialProfit',
    'PotentialPayout',
    'Expected Value',
    'ActualPayout']
for col in currency_columns:
    df_copy[col] = df_copy[col].apply(
        lambda x: "${:,.2f}".format(x) if pd.notnull(x) else '')

df_copy.to_csv('futuresbetlog.csv', index=False)

df2 = df[["Sport", "Amount", "ActualPayout"]]
df2 = df2.groupby("Sport").sum().reset_index()
df2["ROI"] = df2["ActualPayout"] / df2["Amount"]
df2["ROI"] = (df2["ROI"] * 100).round(2)
df2 = df2.reindex(columns=["Sport", "ActualPayout", "Amount", "ROI"]).round(2)
df3 = df.groupby(df['Date'].dt.strftime(
    '%Y-%m'))['ActualPayout'].sum().reset_index().sort_values(by=['Date'])
df4 = df[["Sportsbook", "Amount", "ActualPayout"]]
df4 = df4.groupby("Sportsbook").sum().reset_index()
df4["ROI"] = df4["ActualPayout"] / df4["Amount"]
df4["ROI"] = (df4["ROI"] * 100).round(2)
df4 = df4.reindex(
    columns=[
        "Sportsbook",
        "ActualPayout",
        "Amount",
        "ROI"]).round(2)

df5 = df.groupby(['System'])['ActualPayout'].sum().reset_index().round(2)

df6 = df[["FreeBet", "Amount", "ActualPayout"]]
df6 = df6.groupby("FreeBet").sum().reset_index()
df6["ROI"] = df6["ActualPayout"] / df6["Amount"]
df6["ROI"] = (df6["ROI"] * 100).round(2)
df6 = df6.reindex(
    columns=[
        "FreeBet",
        "ActualPayout",
        "Amount",
        "ROI"]).round(2)

# Sum column values for A, B and C
sum_a = df['ActualPayout'].sum()
sum_b = df['Amount'].sum()

# Write only the sums to new data frame
df7 = pd.DataFrame({'TotalWon': sum_a, 'TotalRisked': sum_b}, index=[0])
columns = ['TotalWon', 'TotalRisked']
df7[columns] = df7[columns].round(2)

# Divide sum of A by sum of B
df7['TotalROI'] = (df7['TotalWon'] / df7['TotalRisked'] * 100).round(2)

substr1 = 'W'
wins = (df.Result.str.count(substr1).sum())

substr2 = 'L'
losses = (df.Result.str.count(substr2).sum())

squareroot = np.sqrt((wins + losses))

df8 = pd.DataFrame({'TotalBetsWon': wins, 'TotalBetsLost': losses}, index=[0])

gamblerz = (wins - losses) / squareroot
df8['gamblerzscore'] = gamblerz.round(2)
winning_pct = (wins / (wins + losses)) * 80
df8['winning_pct'] = winning_pct.round(2)

list_of_dfs = [df2, df3, df4, df5, df6, df7, df8]
for df in list_of_dfs:
    df.rename(
        columns={
            'Amount': 'MoneyRisked',
            'ActualPayout': 'Profit'},
        inplace=True)
    try:
        df["Profit"] = df["Profit"].astype(float).map("${:,.2f}".format)
        df["MoneyRisked"] = df["MoneyRisked"].astype(
            float).map("${:,.2f}".format)
        df["TotalWon"] = df["TotalWon"].astype(float).map("${:,.2f}".format)
        df["TotalRisked"] = df["TotalRisked"].astype(
            float).map("${:,.2f}".format)
    except KeyError:
        pass

titles = [
    "ROI By Sport",
    "Profit by Month",
    "ROI by Sportsbook",
    "Profit by System",
    "Free Bet ROI",
    "Total ROI",
    "Total Win Percentage"]

with open('futuresanalytics.csv', 'w+') as f:
    for i, dfs in enumerate(list_of_dfs):
        f.write(titles[i] + "\n")  # Write the title
        dfs.to_csv(f, index=False)
        f.write("\n")

df9 = pd.read_csv('futures.csv')
filter_df = df9[df9['Result'] == 'P']

# Removed 'CleanedOdds' and 'ActualPayout' from columns_to_drop
columns_to_drop = ['Result', 'PushAmount']
filter_df = filter_df.drop(columns=columns_to_drop)
filter_df.to_csv('pendingfuturesbets.csv', index=False)

filter2 = pd.read_csv('futures.csv')

filter2 = filter2[filter2['Result'] == 'C']
filter2['ActualPayout'] = np.nan
filter2['ActualPayout'] = filter2['ActualPayout'].apply(
    pd.to_numeric, errors='coerce')
filter2['ActualPayout'] = filter2['ActualPayout'].astype('float')
for i, row in filter2.iterrows():
    if row['Result'] == 'C':
        filter2.at[i, 'ActualPayout'] = row['PushAmount']
cols3 = ['Amount', 'ActualPayout']
filter2[cols3] = filter2[cols3].apply(pd.to_numeric, errors='coerce', axis=1)
filter2["ROI"] = filter2["ActualPayout"] / filter2["Amount"]
filter2["ROI"] = (filter2["ROI"] * 100).round(2)
filter2 = filter2.reindex(
    columns=[
        "Pick",
        "Sport",
        "ActualPayout",
        "Amount",
        "ROI"]).round(2)
filter2["Amount"] = filter2["Amount"].astype(float).map("${:,.2f}".format)
filter2["ActualPayout"] = filter2["ActualPayout"].astype(
    float).map("${:,.2f}".format)

filter2.to_csv('futurescashouts.csv')
