import pandas as pd

def calculate_and_save_betting_results(group_name, data_list, csv_filename):
    # Create a DataFrame with three columns
    df = pd.DataFrame(data_list, columns=["bet", "bet_amount", "odds"])

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

    # Calculate the net_profit
    df["net_profit"] = df.apply(lambda row: row["gross_profit"] - df[df.index != row.name]["bet_amount"].sum(), axis=1)

    # Calculate the ROI
    df["ROI"] = (100 * (df["net_profit"] / df["bet_amount"]))
    df["ROI"] = df["ROI"].round(2)

    # Format columns as needed
    df["bet_amount"] = df["bet_amount"].map("${:.2f}".format)
    df["gross_profit"] = df["gross_profit"].map("${:.2f}".format)
    df["net_profit"] = df["net_profit"].map("${:.2f}".format)

    # Calculate the minimum ROI
    minimum_roi = df["ROI"].min()
    minimum_roi = minimum_roi.round(2)

    # Calculate the average ROI
    average_roi = df["ROI"].mean()
    average_roi = average_roi.round(2)

    # Display the results with the Bet Group Name as the title
    print("Results:")
    print(df)
    print("Minimum ROI:", minimum_roi)
    print("Average ROI:", average_roi)
    print("\n")

#     # Append results to the CSV file, separating outputs with a blank row
#     with open(csv_filename, 'a', newline='') as file:
#         df.to_csv(file, mode='a', header=file.tell() == 0, index=False)
#         file.write('\n')
#         file.write(f"Minimum ROI:, {minimum_roi}\n")
#         file.write(f"Average ROI:, {average_roi}\n")
#         file.write('\n')
#
# # Create or overwrite the CSV file
# csv_filename = 'betting_results.csv'
# with open(csv_filename, 'w') as file:
#     file.write('')  # Create an empty file

# Example usage with different data for multiple groups of bets
data_group1 = [("1 hit", 0.1, "+320"), ("2 hits", 0.1, "+320"), ("3 hits", 0.1, "+320")]
calculate_and_save_betting_results("Group 1", data_group1, csv_filename)

# data_group2 = [("Lions", 0.2, "-150"), ("Packers", 0.2, "+200")]
# calculate_and_save_betting_results("Group 2", data_group2, csv_filename)