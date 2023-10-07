import pandas as pd

def calculate_and_save_betting_results(data_list, csv_filename):
    # Create a DataFrame with four columns, including the "bet_group" column
    df = pd.DataFrame(data_list, columns=["team", "bet_amount", "odds", "bet_group"])

    # Function to convert American odds to decimal odds
    def american_to_decimal(american_odds):
        if american_odds > 0:
            decimal_odds = 1 + (american_odds / 100)
        else:
            decimal_odds = 1 + (100 / abs(american_odds))
        return decimal_odds

    # Calculate the gross_profit for winning bets
    df["odds"] = df["odds"].apply(lambda x: int(x) if isinstance(x, str) else x)  # Ensure odds are integers
    df["decimal_odds"] = df["odds"].apply(american_to_decimal)
    df["gross_profit"] = df["bet_amount"] * (df["decimal_odds"] - 1)

    # Calculate the net_profit for each bet separately
    df["net_profit"] = df["gross_profit"] - df.groupby("bet_group")["bet_amount"].transform("sum")

    # Calculate the ROI
    df["ROI"] = (100 * (df["net_profit"] / df["bet_amount"]))
    df["ROI"] = df["ROI"].round(2)

    # Format columns as needed
    df["bet_amount"] = df["bet_amount"].map("${:.2f}".format)
    df["gross_profit"] = df["gross_profit"].map("${:.2f}".format)
    df["net_profit"] = df["net_profit"].map("${:.2f}".format)

    # Calculate the minimum and average ROI for each group
    results = df.groupby("bet_group").agg({"ROI": ["min", "mean"]}).reset_index()
    results.columns = ['bet_group', 'Minimum ROI', 'Average ROI']

    # Display and save the results
    with open(csv_filename, 'w', newline='') as file:
        for group_name, group_data in results.iterrows():
            group_name = group_data['bet_group']
            minimum_roi = group_data['Minimum ROI']
            average_roi = group_data['Average ROI']

            print(f"Bet Group: {group_name}")
            print("Betting Results:")
            group_df = df[df['bet_group'] == group_name].drop(columns=['bet_group'])
            print(group_df)
            print("Minimum ROI:", minimum_roi)
            print("Average ROI:", average_roi)
            print("\n")

            group_df.to_csv(file, mode='a', header=file.tell() == 0, index=False)
            file.write('\n')
            file.write(f"Minimum ROI:, {minimum_roi}\n")
            file.write(f"Average ROI:, {average_roi}\n")
            file.write('\n')

# Create or overwrite the CSV file
csv_filename = 'betting_results.csv'
with open(csv_filename, 'w') as file:
    file.write('')  # Create an empty file

# Example usage with different data for multiple groups of bets
data_group1 = [('Tua Tagovailoa', 0.1, 2200, 'NFL MVP'), ('Patrick Mahomes', 0.1, 700, 'NFL MVP'), ('Jalen Hurts', 0.1, 1100, 'NFL MVP'), ('Lamar Jackson', 0.1, 1500, 'NFL MVP'), ('Jamarr Chase', 0.1, 1100, 'Offensive Player of the Year'), ('Justin Jefferson', 0.1, 1300, 'Offensive Player of the Year'), ('Aidan Hutchinson', 0.11, 2500, 'Defensive Player of the Year'), ('Micha Parsons', 0.1, 650, 'Defensive Player of the Year'), ('Matt Eberflus', 0.1, 1100, 'Coach of the Year'), ('Kyle Shanahan', 0.1, 3000, 'Coach of the Year'), ('Tua Tagovailoa', 0.1, 1600, 'Most Passing TDs'), ('Joe Burrow', 0.1, 450, 'Most Passing TDs'), ('Calvin Ridley', 0.1, 5000, 'Most Receiving Yards'), ('Justin Jefferson', 0.1, 550, 'Most Receiving Yards'), ('Tyreek Hill', 0.1, 900, 'Most Receiving Yards'), ('Cooper Kupp', 0.1, 500, 'Most Receptions'), ('Amon-Ra St. Brown', 0.1, 1800, 'Most Receptions'), ('Jordan Addison', 0.1, 300, 'Rookie Receving Yard Leaders'), ('Quentin Johnson', 0.1, 350, 'Rookie Receving Yard Leaders'), ('Rashee Rice', 0.1, 1800, 'Rookie Receving Yard Leaders'), ('Jahmyr Gibbs', 0.1, 3500, 'Rookie Receving Yard Leaders'), ('Russell Wilson', 0.1, 2000, 'Comeback Player of the Year'), ('Lamar Jackson', 0.1, 2500, 'Comeback Player of the Year'), ('Jokic', 0.1, 450, 'NBA MVP'), ('Giannis', 0.1, 550, 'NBA MVP'), ('Embiid', 0.1, 650, 'NBA MVP'), ('Tatum', 0.1, 900, 'NBA MVP'), ('Holmgren', 0.1, 350, 'NBA ROY'), ('Whitmore', 0.1, 2000, 'NBA ROY'), ('Brandon Miller', 0.1, 1200, 'NBA ROY'), ('Henderson', 0.1, 400, 'NBA ROY')]
calculate_and_save_betting_results(data_group1, csv_filename)

