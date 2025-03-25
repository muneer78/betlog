import pandas as pd

# Read the data from the CSV file into a dataframe
df = pd.read_csv("FantasyPros_Fantasy_Football_2023_Offense_Snap_Count_Analysis.csv")

# Read the "fbexcluded.csv" file into a dataframe
df_excluded = pd.read_csv("fbexcluded.csv")

def clean_player_data(df):
    df.replace(r"[^\w\s]|_\*| Jr| III", "", regex=True, inplace=True)
    return df

# Create a list of excluded player names
excluded_players = df_excluded["PLAYER NAME"].tolist()

# Create dataframe 1 where Pos = QB
df1 = df[df['Pos'] == 'QB']

# Create dataframe 2 where Pos is WR, RB, or TE
df2 = df[df['Pos'] == 'RB']

# Create dataframe 2 where Pos is WR, RB, or TE
df3 = df[df['Pos'] == 'WR']

# Create dataframe 2 where Pos is WR, RB, or TE
df4 = df[df['Pos'] == 'TE']

df1 = clean_player_data(df1)
df2 = clean_player_data(df2)
df3 = clean_player_data(df3)
df4 = clean_player_data(df4)

# Filter out players from df1 and df2 if their names are in the excluded list
df1_filtered = df1[~df1["Player"].isin(excluded_players)]
df2_filtered = df2[~df2["Player"].isin(excluded_players)]
df3_filtered = df3[~df3["Player"].isin(excluded_players)]
df4_filtered = df4[~df4["Player"].isin(excluded_players)]


# Create dataframe 1 where Pos = QB
df1_filtered = df1_filtered[df1_filtered['Pos'] == 'QB']

# Create dataframe 2 where Pos is WR, RB, or TE
df2 = df2_filtered[df2_filtered['Pos'] =='RB']

# Create dataframe 2 where Pos is WR, RB, or TE
df3 = df3_filtered[df3_filtered['Pos'] =='WR']

# Create dataframe 2 where Pos is WR, RB, or TE
df4 = df4_filtered[df4_filtered['Pos'] =='TE']

def sort_data(df):
    df = df.sort_values(by="Fantasy Pts", ascending=False)
    return df

# Store all dataframes in a list
file_path = "fbpickups.csv"
dfs = [df1_filtered, df2_filtered, df3_filtered, df4_filtered]

# Apply the sort_data function to each dataframe using a for loop
for i in range(len(dfs)):
    dfs[i] = sort_data(dfs[i])


# Write df1 to a CSV file with a title
with open("fbpickups.csv", "w", newline="") as csvfile:
    # Write title for df1
    csvfile.write("QB\n")
    # Write headers for df1
    csvfile.write(','.join(df1_filtered.columns) + "\n")
    # Write data for df1
    for _, row in df1_filtered.head(5).iterrows():
        csvfile.write(','.join(map(str, row.values)) + "\n")

# Append df2 to the same CSV file with a title and headers
with open("fbpickups.csv", "a", newline="") as csvfile:
    # Write title for df2
    csvfile.write("RB\n")
    # Write headers for df2
    csvfile.write(','.join(df2_filtered.columns) + "\n")
    # Write data for df2
    for _, row in df2_filtered.head(10).iterrows():
        csvfile.write(','.join(map(str, row.values)) + "\n")

# Append df2 to the same CSV file with a title and headers
with open("fbpickups.csv", "a", newline="") as csvfile:
    # Write title for df3
    csvfile.write("WR\n")
    # Write headers for df3
    csvfile.write(','.join(df2_filtered.columns) + "\n")
    # Write data for df2
    for _, row in df3_filtered.head(10).iterrows():
        csvfile.write(','.join(map(str, row.values)) + "\n")

# Append df2 to the same CSV file with a title and headers
with open("fbpickups.csv", "a", newline="") as csvfile:
    # Write title for df4
    csvfile.write("TE\n")
    # Write headers for df4
    csvfile.write(','.join(df4_filtered.columns) + "\n")
    # Write data for df4
    for _, row in df4_filtered.head(5).iterrows():
        csvfile.write(','.join(map(str, row.values)) + "\n")

titles = ['QB', 'RB', 'WR', 'TE']

print("Here are the weekly recommendations:")
print()
for title, df in zip(titles, dfs):
    column_name = 'Player'  # Replace with the column name you want to extract
    selected_column = df[column_name].head(5)  # Extract the first 5 values

    # Format the output with the specified title
    output = f"{title}: {', '.join(selected_column.astype(str))}"


    # Print the result
    print(output)

    # Print a blank line to separate the outputs
    print()