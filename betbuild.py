import pandas as pd

orig_df = pd.read_csv('betbuilddata.csv')
df = orig_df[orig_df['bet_group'].notnull()]

# Function to convert American odds to decimal odds
def american_to_decimal(american_odds):
    if american_odds > 0:
        decimal_odds = 1 + (american_odds / 100)
    else:
        decimal_odds = 1 + (100 / abs(american_odds))
    return decimal_odds

# Define a function to format currency values
def format_currency(value):
    return "${:,.2f}".format(value)

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
results = df.groupby("bet_group").agg({"ROI": ["min", "mean"], "ActualPayout": "sum"}).reset_index()
results.columns = ['bet_group', 'Minimum ROI', 'Average ROI', 'Total Payout']

# Create or overwrite the CSV file
csv_filename = 'bet_builds.csv'
with open(csv_filename, 'w') as file:
    file.write('')  # Create an empty file

with open(csv_filename, 'w', newline='') as file:
    for group_name, group_data in results.iterrows():
        group_name = group_data['bet_group']

        # Print Bet Group title to console
        print(f"Bet Group: {group_name}")

        # Write Bet Group title to CSV file
        file.write(f"Bet Group: {group_name}\n")

        # Print Betting Results to console
        print("\n")

        # Write Minimum and Average ROI to CSV file if 'P' in Result column, otherwise write only Total Payout
        group_df = df[df['bet_group'] == group_name].drop(columns=['bet_group'])
        if 'P' in group_df['Result'].values:
            minimum_roi = round(group_data['Minimum ROI'], 2) if 'Minimum ROI' in group_data else 'N/A'
            average_roi = round(group_data['Average ROI'], 2) if 'Average ROI' in group_data else 'N/A'
            file.write(f"Minimum ROI:, {minimum_roi}\n")
            file.write(f"Average ROI:, {average_roi}\n")
        else:
            total_payout = format_currency(group_data['Total Payout']) if 'Total Payout' in group_data else 'N/A'
            file.write(f"Total Payout:, {total_payout}\n")

        file.write('\n')

        print("Betting Results:")
        print(group_df)

        # Write Betting Results to CSV file
        group_df.to_csv(file, mode='a', header=file.tell() == 0, index=False)

        if 'P' in group_df['Result'].values:
            # Print Minimum and Average ROI to console
            print("Minimum ROI:", minimum_roi)
            print("Average ROI:", average_roi)
        else:
            # Print only Total Payout if Result is not equal to 'P'
            print("Total Payout:", total_payout)

        print("\n")
