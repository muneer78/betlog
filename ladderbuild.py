import pandas as pd

df = pd.read_csv('recladders.csv')

# Function to convert American odds to decimal odds
def american_to_decimal(american_odds):
    if american_odds > 0:
        decimal_odds = 1 + (american_odds / 100)
    else:
        decimal_odds = 1 + (100 / abs(american_odds))
    return decimal_odds

# Calculate the gross_profit for winning bets
df["Odds"] = df["Odds"].apply(lambda x: int(x) if isinstance(x, str) else x)  # Ensure odds are integers
df["decimal_odds"] = df["Odds"].apply(american_to_decimal)
df["profit"] = df["Amount"] * (df["decimal_odds"] - 1)

# Calculate the ROI
df["ROI"] = (100 * (df["profit"] / df["Amount"]))
df["ROI"] = df["ROI"].round(2)

# Format columns as needed
df["Amount"] = df["Amount"].map("${:.2f}".format)
df["profit"] = df["profit"].map("${:.2f}".format)

# Calculate the minimum and average ROI for each group
results = df.groupby("bet_group").agg({"ROI": ["min", "mean"]}).reset_index()
results.columns = ['bet_group', 'Minimum ROI', 'Average ROI']

csv_filename = 'ladder_builds.csv'

with open(csv_filename, 'w', newline='') as file:
    for group_name, group_data in results.iterrows():
        group_name = group_data['bet_group']
        minimum_roi = group_data['Minimum ROI']
        average_roi = group_data['Average ROI']

        # Write Bet Group title to CSV file
        file.write(f"Bet Group: {group_name}\n")

        # Write headers to CSV file
        group_df = df[df['bet_group'] == group_name].drop(columns=['bet_group'])
        group_df.to_csv(file, header=True, index=False)

        # Write Minimum and Average ROI to CSV file
        file.write(f"Minimum ROI:, {minimum_roi}\n")
        file.write(f"Average ROI:, {average_roi}\n")
        file.write('\n')
