import pandas as pd
import numpy as np

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
df = pd.read_csv('recladders.csv', dtype = dtype_dict)

# Format the 'Date' column as '%m/%d/%Y'
df['Date'] = pd.to_datetime(arg=df['Date'],format='%Y-%m-%d')

def american_to_decimal(american_odds):
    if american_odds > 0:
        decimal_odds = 1 + (american_odds / 100)
    else:
        decimal_odds = 1 + (100 / abs(american_odds))
    return decimal_odds

# Calculate the gross_profit for winning bets
df["Odds"] = df["Odds"].apply(lambda x: int(x) if isinstance(x, str) else x)  # Ensure odds are integers
df["decimal_odds"] = df["Odds"].apply(american_to_decimal)
df["gross_profit"] = df["Amount"] * (df["decimal_odds"] - 1)

# Calculate the net_profit for each bet separately
df["net_profit"] = df["gross_profit"] - df.groupby("bet_group")["Amount"].transform("sum")

# Calculate the ROI
df["ROI"] = (100 * (df["net_profit"] / df["Amount"]))
df["ROI"] = df["ROI"].round(2)

# Format columns as needed
df["Amount"] = df["Amount"].map("${:.2f}".format)
df["gross_profit"] = df["gross_profit"].map("${:.2f}".format)
df["net_profit"] = df["net_profit"].map("${:.2f}".format)

# Calculate the minimum and average ROI for each group
results = df.groupby("bet_group").agg({"ROI": ["min", "mean"]}).reset_index()
results.columns = ['bet_group', 'Minimum ROI', 'Average ROI']

df['PotentialProfit'] = (100 / df['Odds']) * df['Amount']
df['PotentialProfit'] = df['PotentialProfit'].round(2)

cols2 = ['PotentialProfit', 'CleanedOdds']
df[cols2] = df[cols2].apply(pd.to_numeric, errors='coerce', axis=1)

df['PotentialPayout'] = df['PotentialProfit'] + df['Amount'].apply(pd.to_numeric, errors='coerce')
df['PotentialPayout'] = df['PotentialPayout'].round(2)

df['ImpliedProbability'] = np.where(df['Odds'] > 0, (100 / (100 + df['CleanedOdds'])), ((df['CleanedOdds'])/(100+(df['CleanedOdds'])))).round(2)

df['Expected Value'] = np.ceil(df['ImpliedProbability'] * df['Amount']) - ((1 - df['ImpliedProbability']) * df['Amount'])
df['Expected Value'] = df['Expected Value'].apply(pd.to_numeric, errors='coerce')
df['Expected Value'] = df['Expected Value'].round(2)

df['ActualPayout'] = np.nan
df['ActualPayout'] = df['ActualPayout'].apply(pd.to_numeric, errors='coerce')
df['ActualPayout'] = df['ActualPayout'].astype('float')

for i, row in df.iterrows():
    if row['Result'] == 'L':
        df.at[i, 'ActualPayout'] = row['Amount'] * -1
    elif row['Result'] == 'W':
        df.at[i, 'ActualPayout'] = row['PotentialPayout']
    elif row['Result'] == 'P':
        df.at[i, 'ActualPayout'] = 0

df_copy = df.copy()

currency_columns = ['Amount', 'PotentialProfit', 'PotentialPayout', 'Expected Value', 'ActualPayout']
for col in currency_columns:
    df_copy[col] = df_copy[col].apply(lambda x: "${:,.2f}".format(x) if pd.notnull(x) else '')

# Create or overwrite the CSV file
csv_filename = 'laddersroi.csv'
with open(csv_filename, 'w') as file:
    file.write('')  # Create an empty file

with open(csv_filename, 'w', newline='') as file:
    for group_name, group_data in results.iterrows():
        group_name = group_data['bet_group']
        minimum_roi = group_data['Minimum ROI']
        average_roi = group_data['Average ROI']

        # Print Bet Group title to console
        print(f"Bet Group: {group_name}")

        # Write Bet Group title to CSV file
        file.write(f"Bet Group: {group_name}\n")

        # Print Betting Results to console
        print("Betting Results:")
        group_df = df[df['bet_group'] == group_name].drop(columns=['bet_group'])
        print(group_df)

        # Write Betting Results to CSV file
        group_df.to_csv(file, mode='a', header=file.tell() == 0, index=False)

        # Print Minimum and Average ROI to console
        print("Minimum ROI:", minimum_roi)
        print("Average ROI:", average_roi)
        print("\n")

        # Write Minimum and Average ROI to CSV file
        file.write(f"Minimum ROI:, {minimum_roi}\n")
        file.write(f"Average ROI:, {average_roi}\n")
        file.write('\n')

df_copy.to_csv('laddersbetlog.csv', index=False)

df2 = df[["Team", "Amount", "ActualPayout"]]
df2 = df2.groupby("Team").sum().reset_index()
df2["ROI"] = df2["ActualPayout"] / df2["Amount"]
df2["ROI"] = (df2["ROI"] * 100).round(2)
df2 = df2.reindex(columns=["Team", "ActualPayout", "Amount", "ROI"]).round(2)
df3 = df.groupby(df['Date'].dt.strftime('%Y-%m-%d'))['ActualPayout'].sum().reset_index().sort_values(by=['Date'])

# Sum column values for A, B and C
sum_a = df['ActualPayout'].sum()
sum_b = df['Amount'].sum()

# Write only the sums to new data frame
df4 = pd.DataFrame({'TotalWon': sum_a, 'TotalRisked': sum_b}, index=[0])
columns = ['TotalWon', 'TotalRisked']
df4[columns] = df4[columns].round(2)

# Divide sum of A by sum of B
df4['TotalROI'] = (df4['TotalWon'] / df4['TotalRisked'] * 100).round(2)

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

list_of_dfs = [df2, df3, df4]
for df in list_of_dfs:
    df.rename(columns={'Amount': 'MoneyRisked', 'ActualPayout': 'Profit'}, inplace=True)
    try:
        df["Profit"] = df["Profit"].astype(float).map("${:,.2f}".format)
        df["MoneyRisked"] = df["MoneyRisked"].astype(float).map("${:,.2f}".format)
        df["TotalWon"] = df["TotalWon"].astype(float).map("${:,.2f}".format)
        df["TotalRisked"] = df["TotalRisked"].astype(float).map("${:,.2f}".format)
    except KeyError:
        pass

titles = ["ROI By Team", "Profit by Month", "Total ROI", "Total Win Percentage"]

with open('laddersanalytics.csv', 'w+') as f:
    for i, dfs in enumerate(list_of_dfs):
        f.write(titles[i] + "\n")  # Write the title
        dfs.to_csv(f, index=False)
        f.write("\n")
