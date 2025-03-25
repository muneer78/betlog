'''
Need to take output from kcsandlot.py and trim list down before running this script
'''

import pandas as pd

# Read dataframe
df_kcsandlotkeepers = pd.read_csv("sandlotkeeperlist.csv")

# Filter out rows with empty or NaN values in the "Name" column
df_kcsandlotkeepers = df_kcsandlotkeepers.dropna(subset=["Name"])

# Count number of instances where Group = A
count_A = df_kcsandlotkeepers[df_kcsandlotkeepers['Group'] == 'A'].shape[0]

# Count number of instances where Group = A and Position = SP or Position = RP
count_A_pitchers = df_kcsandlotkeepers[(df_kcsandlotkeepers['Group'] == 'A') & ((df_kcsandlotkeepers['Position'] == 'SP') | (df_kcsandlotkeepers['Position'] == 'RP'))].shape[0]

# Count number of instances where Group = B
count_B = df_kcsandlotkeepers[df_kcsandlotkeepers['Group'] == 'B'].shape[0]

# Create a list to hold messages
messages = []

# Check conditions and add messages if necessary
if count_A > 7:
    messages.append(f"You have {count_A} A keepers. You can have up to 7")

if count_A_pitchers > 4:
    messages.append(f"You have {count_A_pitchers} pitchers in group A. You can have up to 4")

if count_B > 6:
    messages.append(f"You have {count_B} B keepers. You can have up to 6")

# Check total number of rows
if df_kcsandlotkeepers.shape[0] > 15:
    messages.append("You have too many keepers listed")

# Create a dataframe to store the messages
df_messages = pd.DataFrame({'Message': messages})

# Print dataframe
print(df_messages)

# Create pivot table
pivot_table = pd.pivot_table(df_kcsandlotkeepers, values=['Name'], index=['Group'], aggfunc='count')

# Print the pivot table to the terminal
print(pivot_table)