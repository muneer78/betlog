import pandas as pd

# Function to create keys from player names
def create_key(player_name):
    if isinstance(player_name, str):
        return "".join([i[:3] for i in player_name.strip().split(" ")])
    else:
        return ""

# Read dataframes
df_kcsandlotkeepers = pd.read_csv("KC Sandlot Keepers.csv")
df_draftsheet = pd.read_csv("draftsheet.csv")

# Filter out rows with empty or NaN values in the "Name" column
df_kcsandlotkeepers = df_kcsandlotkeepers.dropna(subset=["Name"])
df_draftsheet = df_draftsheet.dropna(subset=["Name"])

def determine_group(service_time):
    if service_time == 0:
        return 'C'
    elif 1 <= service_time <= 4:
        return 'B'
    else:
        return 'A'

# Apply the function to create the 'Group' column
df_kcsandlotkeepers['Group'] = df_kcsandlotkeepers['Service Time'].apply(determine_group)

# Apply the create_key function to add the "Key" column
df_kcsandlotkeepers["Key"] = df_kcsandlotkeepers["Name"].apply(create_key)
df_draftsheet["Key"] = df_draftsheet["Name"].apply(create_key)

# Create a list of dataframes for merging
dflist = [df_draftsheet, df_kcsandlotkeepers]

# Merge the dataframes with suffixes to handle duplicate columns
df1 = df_kcsandlotkeepers.merge(df_draftsheet[["Key", "LRank", "ADP", "Team", "Total Z-Score"]], on=["Key"], how="left")

# Convert specific columns to numeric
cols = ["LRank"]
df1[cols] = df1[cols].apply(pd.to_numeric, errors="coerce", axis=1)

# Select and rename columns
columns = ["Group", "Name", "Team", "Position", "Service Time", "Total Z-Score", "LRank", "ADP"]
df1 = df1[columns]

# Sort the "ZScore" column
df1.sort_values(by=["Group", "LRank", "Total Z-Score"], ascending = [True, True, False], inplace=True)

# Save the dataframe to CSV
df1.to_csv("sandlot.csv", index=False)
