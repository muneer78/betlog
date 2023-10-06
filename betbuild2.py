import pandas as pd
import glob

def create_tuples_from_csv(filename):
    data = pd.read_csv(filename)
    return [(ix, k, v) for ix, row in data.iterrows() for k, v in row.items()]

# Use glob to find all CSV files with 'bet' in the name
csv_files = glob.glob("*betgroup*.csv")

# Create a list of data groups, where each group contains the tuples from a CSV file
data_groups = []
for csv_file in csv_files:
    data_group_name = csv_file.split('.')[0]  # Extract the group name from the file name
    data_group_tuples = create_tuples_from_csv(csv_file)
    data_groups.append((data_group_name, data_group_tuples))

def calculate_and_save_betting_results(group_name, data_list, csv_filename):
    # Create a DataFrame with three columns
    df = pd.DataFrame(data_list, columns=["team", "bet amount", "odds"])

    # Function to convert American odds to decimal odds
    def american_to_decimal(american_odds):
        if american_odds > 0:
            decimal_odds = 1 + (american_odds / 100)
        else:
            decimal_odds = 1 + (100 / abs(american_odds))
        return decimal_odds

    # Calculate the Gross Profit for winning bets
    df["odds"] = df["odds"].apply(lambda x: int(x) if isinstance(x, str) else x)  # Ensure odds are integers
    df["decimal_odds"] = df["odds"].apply(american_to_decimal)
    df["Gross Profit"] = df["bet amount"] * (df["decimal_odds"] - 1)

    # Calculate the Net Profit
    df["Net Profit"] = df.apply(lambda row: row["Gross Profit"] - df[df.index != row.name]["bet amount"].sum(), axis=1)

    # Calculate the ROI
    df["% ROI"] = (100 * (df["Net Profit"] / df["bet amount"]))
    df["% ROI"] = df["% ROI"].round(2)

    # Format columns as needed
    df["bet amount"] = df["bet amount"].map("${:.2f}".format)
    df["Gross Profit"] = df["Gross Profit"].map("${:.2f}".format)
    df["Net Profit"] = df["Net Profit"].map("${:.2f}".format)

    # Calculate the minimum ROI and average ROI
    minimum_roi = df["% ROI"].min()
    minimum_roi = minimum_roi.round(2)
    average_roi = df["% ROI"].mean()
    average_roi = average_roi.round(2)

    # Display the results with the Bet Group Name as the title
    print(f"Bet Group: {group_name}")
    print("Betting Results:")
    print(df)
    print("Minimum ROI:", minimum_roi)
    print("Average ROI:", average_roi)
    print("\n")

    # Append results to the CSV file, separating outputs with a blank row
    with open(csv_filename, 'a', newline='') as file:
        df.to_csv(file, mode='a', header=file.tell() == 0, index=False)
        file.write('\n')
        file.write(f"Minimum ROI:, {minimum_roi}\n")
        file.write(f"Average ROI:, {average_roi}\n")
        file.write('\n')

# Create or overwrite the CSV file
csv_filename = 'betting_results.csv'
with open(csv_filename, 'w') as file:
    file.write('')  # Create an empty file

# Example usage with different data for multiple groups of bets
for group_name, data_group in data_groups:
    calculate_and_save_betting_results(group_name, data_group, csv_filename)
